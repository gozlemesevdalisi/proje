"""SWF dosyasını okur: sahne bilgisi, karakter tanımları ve zaman çizelgeleri.

Yalnızca aktarımın gerektirdiği kadarını çözer. Şekillerin kendisi FFDec'in SVG çıktısından alınır
(bkz. aktar.py); burada şekillerin yalnızca kimliği ve türü tutulur.

Zaman çizelgesi SWF'deki gibi kare kare "işlem" olarak saklanır: yerleştir, taşı, kaldır. Oynatıcı
bunları sırayla uygulayarak her karenin görüntü listesini kurar.
"""
import hashlib
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "olcum"))
from swfstats import Bits, tags  # noqa: E402

SHAPE_TAGS = {2, 22, 32, 83}
MORPH_TAGS = {46, 84}
BITMAP_TAGS = {6, 20, 21, 35, 36, 90}
TEXT_TAGS = {11, 33}
FONT_TAGS = {10, 48, 75}
BLEND_MODES = {0: "normal", 1: "normal", 2: "layer", 3: "multiply", 4: "screen", 5: "lighten", 6: "darken",
               7: "difference", 8: "add", 9: "subtract", 10: "invert", 11: "alpha", 12: "erase",
               13: "overlay", 14: "hardlight"}


def load(path):
    """SWF'yi açar: (sürüm, sahne genişliği, sahne yüksekliği, kare hızı, veri, ilk etiketin yeri)."""
    with open(path, "rb") as f:
        raw = f.read()
    sig, version = raw[:3], raw[3]
    if sig == b"CWS":
        data = raw[:8] + zlib.decompress(raw[8:])
    elif sig == b"FWS":
        data = raw
    else:
        raise ValueError(f"desteklenmeyen SWF imzası: {sig!r}")
    b = Bits(data, 8)
    nbits = b.ub(5)
    xmin, xmax, ymin, ymax = (b.sb(nbits) for _ in range(4))
    b.align()
    rate = struct.unpack_from("<H", data, b.pos)[0] / 256
    pos = b.pos + 4
    return version, (xmax - xmin) / 20, (ymax - ymin) / 20, rate, data, pos


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def read_matrix(b):
    """MATRIX → [a, b, c, d, tx, ty]; öteleme piksel."""
    b.align()
    a = d = 1.0
    bb = c = 0.0
    if b.ub(1):
        n = b.ub(5)
        a = b.sb(n) / 65536
        d = b.sb(n) / 65536
    if b.ub(1):
        n = b.ub(5)
        bb = b.sb(n) / 65536
        c = b.sb(n) / 65536
    n = b.ub(5)
    tx = b.sb(n) / 20
    ty = b.sb(n) / 20
    b.align()
    return [a, bb, c, d, tx, ty]


def read_cxform(b, alpha=True):
    """CXFORM(WITHALPHA) → [[çarpanlar r, g, b, a], [ekler r, g, b, a]]; çarpan 1 = değişmez,
    ek 0..1 aralığında (255'e bölünmüş)."""
    b.align()
    has_add = b.ub(1)
    has_mul = b.ub(1)
    n = b.ub(4)
    count = 4 if alpha else 3
    mul = [1.0, 1.0, 1.0, 1.0]
    add = [0.0, 0.0, 0.0, 0.0]
    if has_mul:
        for i in range(count):
            mul[i] = b.sb(n) / 256
    if has_add:
        for i in range(count):
            add[i] = b.sb(n) / 255
    b.align()
    return [mul, add]


def read_filters(data, p):
    """FILTERLIST → ([{tür, ...}], yeni konum). Süzgeçler kaydedilir; oynatıcı şimdilik çizmez."""
    count = data[p]
    p += 1
    out = []
    for _ in range(count):
        kind = data[p]
        p += 1
        if kind == 0:  # DropShadow
            rgba = list(data[p:p + 4])
            bx, by, ang, dist, strength = struct.unpack_from("<iiiih", data, p + 4)
            out.append({"type": "drop_shadow", "color": rgba, "blur": [bx / 65536, by / 65536],
                        "angle": ang / 65536, "distance": dist / 65536, "strength": strength / 256})
            p += 4 + 16 + 2 + 1
        elif kind == 1:  # Blur
            bx, by = struct.unpack_from("<ii", data, p)
            out.append({"type": "blur", "blur": [bx / 65536, by / 65536]})
            p += 9
        elif kind == 2:  # Glow
            rgba = list(data[p:p + 4])
            bx, by, strength = struct.unpack_from("<iih", data, p + 4)
            out.append({"type": "glow", "color": rgba, "blur": [bx / 65536, by / 65536], "strength": strength / 256,
                        "inner": bool(data[p + 14] & 0x80), "knockout": bool(data[p + 14] & 0x40)})
            p += 15
        elif kind == 3:  # Bevel
            out.append({"type": "bevel"})
            p += 4 + 4 + 16 + 2 + 1 + 4
        elif kind in (4, 7):  # GradientGlow, GradientBevel
            n = data[p]
            p += 1 + n * 5 + 4 * 4 + 2 + 1
            out.append({"type": "gradient_glow" if kind == 4 else "gradient_bevel"})
        elif kind == 5:  # Convolution
            mx, my = data[p], data[p + 1]
            p += 2 + 4 + 4 + mx * my * 4 + 4 + 1
            out.append({"type": "convolution"})
        elif kind == 6:  # ColorMatrix
            values = struct.unpack_from("<20f", data, p)
            out.append({"type": "color_matrix", "matrix": [round(v, 5) for v in values]})
            p += 80
        else:
            raise ValueError(f"bilinmeyen süzgeç türü: {kind}")
    return out, p


def read_place(body, code):
    """PlaceObject2 (26) / PlaceObject3 (70) → işlem sözlüğü.

    Anahtarlar: depth, move (var olanı değiştir), char, matrix, cxform, ratio, name, clip (kırpma
    derinliği: bu nesne, derinliği clip'e kadar olanlar için maske olur), filters, blend."""
    flags = body[0]
    p = 1
    flags2 = 0
    if code == 70:
        flags2 = body[1]
        p = 2
    op = {"depth": struct.unpack_from("<H", body, p)[0]}
    p += 2
    if flags & 1:
        op["move"] = True
    if code == 70 and (flags2 & 0x08 or (flags2 & 0x10 and flags & 0x02)):
        p = body.index(b"\0", p) + 1  # sınıf adı
    if flags & 0x02:
        op["char"] = struct.unpack_from("<H", body, p)[0]
        p += 2
    if flags & 0x04:
        b = Bits(body, p)
        op["matrix"] = read_matrix(b)
        p = b.pos
    if flags & 0x08:
        b = Bits(body, p)
        op["cxform"] = read_cxform(b)
        p = b.pos
    if flags & 0x10:
        op["ratio"] = struct.unpack_from("<H", body, p)[0] / 65535
        p += 2
    if flags & 0x20:
        e = body.index(b"\0", p)
        op["name"] = body[p:e].decode("latin1")
        p = e + 1
    if flags & 0x40:
        op["clip"] = struct.unpack_from("<H", body, p)[0]
        p += 2
    if code == 70:
        if flags2 & 0x01:
            op["filters"], p = read_filters(body, p)
        if flags2 & 0x02:
            op["blend"] = BLEND_MODES.get(body[p], "normal")
            p += 1
        if flags2 & 0x04:
            p += 1  # bit eşlem önbelleği: çizimi değiştirmez
    return op


class Timeline:
    """Bir sprite'ın ya da kök filmin zaman çizelgesi."""

    def __init__(self):
        self.frames = [[]]  # her kare: işlem listesi
        self.labels = {}  # etiket → kare sırası (0'dan)
        self.sounds = {}  # kare sırası → [ses kimliği]

    def add_tag(self, code, body):
        ops = self.frames[-1]
        if code in (26, 70):
            ops.append(read_place(body, code))
        elif code == 28:  # RemoveObject2
            ops.append({"remove": struct.unpack_from("<H", body, 0)[0]})
        elif code == 5:  # RemoveObject
            ops.append({"remove": struct.unpack_from("<H", body, 2)[0]})
        elif code == 43:  # FrameLabel
            self.labels[body[:body.index(b"\0")].decode("latin1")] = len(self.frames) - 1
        elif code == 15:  # StartSound
            self.sounds.setdefault(len(self.frames) - 1, []).append(struct.unpack_from("<H", body, 0)[0])
        elif code == 1:  # ShowFrame
            self.frames.append([])

    def finish(self):
        # Son ShowFrame'den sonra açılan boş kare atılır
        if self.frames and not self.frames[-1]:
            self.frames.pop()
        return self

    def characters(self):
        return {op["char"] for ops in self.frames for op in ops if "char" in op}


def read_button(body):
    """DefineButton2 → (kimlik, kayıtlar). Kayıt: {states: [up, over, down, hit], char, depth, matrix, cxform}."""
    bid = struct.unpack_from("<H", body, 0)[0]
    p = 2 + 1 + 2  # kimlik, izleme bayrağı, eylem kaydırması
    records = []
    while body[p] != 0:
        flags = body[p]
        p += 1
        rec = {"states": [bool(flags & 1), bool(flags & 2), bool(flags & 4), bool(flags & 8)],
               "char": struct.unpack_from("<H", body, p)[0], "depth": struct.unpack_from("<H", body, p + 2)[0]}
        p += 4
        b = Bits(body, p)
        rec["matrix"] = read_matrix(b)
        rec["cxform"] = read_cxform(b)
        p = b.pos
        if flags & 0x10:
            rec["filters"], p = read_filters(body, p)
        if flags & 0x20:
            rec["blend"] = BLEND_MODES.get(body[p], "normal")
            p += 1
        records.append(rec)
    return bid, records


class Movie:
    """Bütün SWF: sahne, karakterler, zaman çizelgeleri, dışa aktarılan adlar."""

    def __init__(self, path):
        self.version, self.width, self.height, self.rate, data, pos = load(path)
        self.background = None
        self.shapes = set()
        self.morphs = set()
        self.bitmaps = set()
        self.texts = set()
        self.edit_texts = set()
        self.fonts = set()
        self.sounds = set()
        self.sprites = {}
        self.buttons = {}
        self.exports = {}
        self.root = Timeline()
        for code, body in tags(data, pos):
            cid = struct.unpack_from("<H", body, 0)[0] if len(body) >= 2 else None
            if code == 9:
                self.background = "#%02X%02X%02X" % tuple(body[:3])
            elif code in SHAPE_TAGS:
                self.shapes.add(cid)
            elif code in MORPH_TAGS:
                self.morphs.add(cid)
            elif code in BITMAP_TAGS:
                self.bitmaps.add(cid)
            elif code in TEXT_TAGS:
                self.texts.add(cid)
            elif code == 37:
                self.edit_texts.add(cid)
            elif code in FONT_TAGS:
                self.fonts.add(cid)
            elif code == 14:
                self.sounds.add(cid)
            elif code == 34:
                bid, records = read_button(body)
                self.buttons[bid] = records
            elif code == 39:
                t = Timeline()
                for c2, b2 in tags(body, 4):
                    t.add_tag(c2, b2)
                self.sprites[cid] = t.finish()
            elif code == 56:
                n = cid
                p = 2
                for _ in range(n):
                    char = struct.unpack_from("<H", body, p)[0]
                    p += 2
                    e = body.index(b"\0", p)
                    self.exports[body[p:e].decode("latin1")] = char
                    p = e + 1
            else:
                self.root.add_tag(code, body)
        self.root.finish()

    def kind(self, cid):
        """Karakterin türü: shape, morph, bitmap, text, edit_text, font, sound, sprite, button ya da None."""
        for name, ids in (("shape", self.shapes), ("morph", self.morphs), ("bitmap", self.bitmaps),
                          ("text", self.texts), ("edit_text", self.edit_texts), ("font", self.fonts),
                          ("sound", self.sounds)):
            if cid in ids:
                return name
        if cid in self.sprites:
            return "sprite"
        if cid in self.buttons:
            return "button"
        return None

    def children(self, cid):
        """Bir karakterin doğrudan kullandığı karakterler."""
        if cid in self.sprites:
            return self.sprites[cid].characters()
        if cid in self.buttons:
            return {r["char"] for r in self.buttons[cid]}
        return set()

    def reachable(self, roots):
        """Köklerden (karakter kimlikleri) ulaşılan bütün karakterler."""
        seen = set()
        stack = list(roots)
        while stack:
            cid = stack.pop()
            if cid in seen:
                continue
            seen.add(cid)
            stack.extend(self.children(cid) - seen)
        return seen
