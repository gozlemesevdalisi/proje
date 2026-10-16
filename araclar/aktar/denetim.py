"""Ayıklama denetimi: oyuna aktarılanı, FFDec'in kendi ayrıştırıcısıyla ürettiği XML dökümüyle
(referans/<oyun>/tam/swf.xml) kayıt kayıt karşılaştırır. İki ayrı ayrıştırıcı (bizimki ve FFDec'inki)
aynı sonucu vermelidir.

Denetlenen:
  1. etiket türlerinin sayıları (en dış düzey ve sprite'ların içi);
  2. karakter kimlikleri (türüne göre) ve her birinin listede (manifest) bir yeri olması;
  3. bütün zaman çizelgeleri: kare kare her yerleştirme (karakter, derinlik, matris, renk dönüşümü,
     oran, ad, kırpma derinliği, klip eylemi, süzgeç, karışım), kaldırma, kare etiketi, ses başlatma;
  4. düğmeler, dışa aktarılan adlar, sabit yazılar (glif glif), yazı alanları;
  5. sesler (dosya baytları SWF'deki veriyle aynı mı), resimler (açılıyor mu, boyutu doğru mu);
  6. şekiller: motorun çizdiği ile FFDec'in çizdiği piksel piksel; morph başlangıç ve bitişleri;
  7. kod parçalarının sayısı.

Kullanım (depo kökünden; önce cikar.sh ve aktar.py):
    python3 araclar/aktar/denetim.py [--gorsel]     → docs/AYIKLAMA_DENETIMI.md
`--gorsel` şekillerin piksel karşılaştırmasını da yapar (birkaç dakika sürer).
"""
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aktar  # noqa: E402
import ceviri  # noqa: E402
import swf  # noqa: E402

ROOT = aktar.ROOT
TOL = 1e-3  # sayısal karşılaştırma payı (JSON'da 4 basamağa yuvarlanır)
XML_NAME = {"CSMSettings": "CSMTextSettings"}


# --- XML dökümünü okuma -------------------------------------------------------------------------

def xml_matrix(el):
    if el is None:
        return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    a = float(el.get("scaleX")) if el.get("hasScale") == "true" else 1.0
    d = float(el.get("scaleY")) if el.get("hasScale") == "true" else 1.0
    b = float(el.get("rotateSkew0")) if el.get("hasRotate") == "true" else 0.0
    c = float(el.get("rotateSkew1")) if el.get("hasRotate") == "true" else 0.0
    return [a, b, c, d, int(el.get("translateX")) / 20, int(el.get("translateY")) / 20]


def xml_cxform(el):
    if el is None:
        return [[1.0] * 4, [0.0] * 4]
    keys = ("red", "green", "blue", "alpha")
    mul = [int(el.get(k + "MultTerm", 256)) / 256 if el.get("hasMultTerms") == "true" else 1.0 for k in keys]
    add = [int(el.get(k + "AddTerm", 0)) / 255 if el.get("hasAddTerms") == "true" else 0.0 for k in keys]
    if el.get("type") == "CXFORM":
        mul[3], add[3] = 1.0, 0.0
    return [mul, add]


FILTER_TYPES = {"DROPSHADOWFILTER": "drop_shadow", "BLURFILTER": "blur", "GLOWFILTER": "glow",
                "BEVELFILTER": "bevel", "GRADIENTGLOWFILTER": "gradient_glow", "CONVOLUTIONFILTER": "convolution",
                "COLORMATRIXFILTER": "color_matrix", "GRADIENTBEVELFILTER": "gradient_bevel"}


def xml_place(el):
    op = {"depth": int(el.get("depth"))}
    if el.get("placeFlagMove") == "true":
        op["move"] = True
    if el.get("placeFlagHasCharacter") == "true":
        op["char"] = int(el.get("characterId"))
    if el.get("placeFlagHasMatrix") == "true":
        op["matrix"] = xml_matrix(el.find("matrix"))
    if el.get("placeFlagHasColorTransform") == "true":
        op["cxform"] = xml_cxform(el.find("colorTransform"))
    if el.get("placeFlagHasRatio") == "true":
        op["ratio"] = int(el.get("ratio")) / 65535
    if el.get("placeFlagHasName") == "true":
        op["name"] = el.get("name")
    if el.get("placeFlagHasClipDepth") == "true":
        op["clip"] = int(el.get("clipDepth"))
    if el.get("placeFlagHasClipActions") == "true":
        op["clip_actions"] = True
    if el.get("placeFlagHasFilterList") == "true":
        op["filters"] = [FILTER_TYPES.get(f.get("type"), f.get("type")) for f in el.find("surfaceFilterList")]
    if el.get("placeFlagHasBlendMode") == "true":
        op["blend"] = swf.BLEND_MODES.get(int(el.get("blendMode")), "normal")
    return op


def xml_sound_info(el):
    """SOUNDINFO → library.json'daki biçim: yalnız varsayılandan farklı alanlar (bkz. swf.read_sound_info)."""
    info = {}
    if el is None:
        return info
    if el.get("syncStop") == "true":
        info["stop"] = True
    if el.get("syncNoMultiple") == "true":
        info["no_multiple"] = True
    for flag, key, attr in (("hasInPoint", "in", "inPoint"), ("hasOutPoint", "out", "outPoint"),
                            ("hasLoops", "loops", "loopCount")):
        if el.get(flag) == "true":
            info[key] = int(el.get(attr))
    if el.get("hasEnvelope") == "true":
        records = el.find("envelopeRecords")
        info["envelope"] = [[int(r.get("pos44")), int(r.get("leftLevel")), int(r.get("rightLevel"))]
                            for r in (records if records is not None else [])]
    return info


class XmlTimeline:
    def __init__(self):
        self.frames = [[]]
        self.labels = {}
        self.sounds = {}
        self.counts = {}

    def add(self, el):
        kind = el.get("type")[:-3] if el.get("type", "").endswith("Tag") else el.get("type")
        kind = XML_NAME.get(kind, kind)
        self.counts[kind] = self.counts.get(kind, 0) + 1
        if kind in ("PlaceObject2", "PlaceObject3"):
            self.frames[-1].append(xml_place(el))
        elif kind == "RemoveObject2":
            self.frames[-1].append({"remove": int(el.get("depth"))})
        elif kind == "FrameLabel":
            self.labels[el.get("name")] = len(self.frames) - 1
        elif kind == "StartSound":
            self.sounds.setdefault(len(self.frames) - 1, []).append(
                {"id": int(el.get("soundId")), **xml_sound_info(el.find("soundInfo"))})
        elif kind == "ShowFrame":
            self.frames.append([])

    def finish(self):
        if self.frames and not self.frames[-1]:
            self.frames.pop()


class XmlDump:
    """FFDec XML dökümünden denetimin gerektirdiği her şey (akış hâlinde okunur)."""

    def __init__(self, path):
        self.counts = {}
        self.sprite_counts = {}
        self.chars = {}  # kimlik → tür
        self.sprites = {}
        self.root = XmlTimeline()
        self.buttons = {}
        self.exports = {}
        self.texts = {}
        self.edit_texts = {}
        self.sounds = {}
        self.sound_samples = {}
        self.images = {}
        self.jpeg_tables = b""
        self.morph_bounds = {}
        self.bitmap_fills = {}  # şekil → [(resim kimliği, desen matrisi piksel biriminde)]
        self.scripts = {"DoAction": 0, "DoInitAction": 0, "BUTTONCONDACTION": 0, "CLIPACTIONRECORD": 0}
        self.root_counts = {}
        depth = 0
        for event, el in ET.iterparse(path, events=("start", "end")):
            if event == "start":
                depth += 1
                continue
            depth -= 1
            if el.tag != "item" or depth != 2:
                continue
            self.top_level(el)
            el.clear()
        self.root.finish()
        self.counts = self.root_counts

    def top_level(self, el):
        t = el.get("type", "")
        kind = XML_NAME.get(t[:-3], t[:-3]) if t.endswith("Tag") else t
        self.root_counts[kind] = self.root_counts.get(kind, 0) + 1
        self.count_scripts(el)
        cid = None
        for key in ("shapeId", "spriteId", "buttonId", "characterID", "characterId", "soundId", "fontId",
                    "fontID"):
            if el.get(key) is not None and kind.startswith("Define"):
                cid = int(el.get(key))
                break
        if kind.startswith("DefineShape"):
            self.chars[cid] = "shape"
            fills = bitmap_fills(el)
            if fills:
                self.bitmap_fills[cid] = fills
        elif kind.startswith("DefineMorphShape"):
            self.chars[cid] = "morph"
            self.morph_bounds[cid] = {end: [int(el.find(f"{end}Bounds").get(k)) / 20
                                            for k in ("Xmin", "Ymin", "Xmax", "Ymax")] for end in ("start", "end")}
        elif kind.startswith("DefineBits") and kind != "DefineBitsTag":
            self.chars[cid] = "bitmap"
            self.images[cid] = el
        elif kind in ("DefineText", "DefineText2"):
            self.chars[cid] = "text"
            self.texts[cid] = text_records(el)
        elif kind == "DefineEditText":
            self.chars[cid] = "edit_text"
            self.edit_texts[cid] = dict(el.attrib)
        elif kind.startswith("DefineFont") and kind not in ("DefineFontAlignZones", "DefineFontInfo",
                                                           "DefineFontInfo2", "DefineFontName"):
            self.chars[cid] = "font"
        elif kind == "DefineSound":
            self.chars[cid] = "sound"
            self.sounds[cid] = bytes.fromhex(el.get("soundData", ""))
            self.sound_samples[cid] = int(el.get("soundSampleCount", "0"))
        elif kind == "DefineButton2":
            self.chars[cid] = "button"
            self.buttons[cid] = [button_record(r) for r in el.find("characters")]
        elif kind == "DefineSprite":
            self.chars[cid] = "sprite"
            t = XmlTimeline()
            for sub in el.find("subTags"):
                t.add(sub)
                k = sub.get("type", "")
                k = XML_NAME.get(k[:-3], k[:-3]) if k.endswith("Tag") else k
                self.sprite_counts[k] = self.sprite_counts.get(k, 0) + 1
            t.finish()
            self.sprites[cid] = t
        elif kind == "ExportAssets":
            ids = [int(i.text) for i in el.find("tags")]
            names = [n.text for n in el.find("names")]
            self.exports.update(dict(zip(names, ids)))
        elif kind == "JPEGTables":
            self.jpeg_tables = bytes.fromhex(el.get("jpegData", ""))
        if kind == "DefineBits":
            self.chars[cid] = "bitmap"
            self.images[cid] = el
        self.root.add(el)

    def count_scripts(self, el):
        for sub in el.iter("item"):
            t = sub.get("type", "")
            if t in ("DoActionTag", "DoInitActionTag"):
                self.scripts[t[:-3]] += 1
            elif t in ("BUTTONCONDACTION", "CLIPACTIONRECORD"):
                self.scripts[t] += 1


BITMAP_FILL_TYPES = (0x40, 0x41, 0x42, 0x43)  # tekrarlı, kırpılmış, yumuşatmasız tekrarlı, yumuşatmasız kırpılmış


def fill_style_items(parent):
    """Bir şeklin ya da stil değişim kaydının dolgu stilleri (XML öğeleri, sırayla)."""
    outer = parent.find("fillStyles")
    inner = outer.find("fillStyles") if outer is not None else None
    return list(inner) if inner is not None else []


def bitmap_fills(el):
    """Şeklin kenarlarının kullandığı resim dolguları: [(resim kimliği, [a, b, c, d, tx, ty])]. Stil
    değişim kaydı yeni stil dizisi getirebilir; sonraki dolgu numaraları o diziyi gösterir. SWF'de dolgu
    matrisi resim pikselini twip'e taşır; 20'ye bölünce SVG desen matrisi (piksel) çıkar. Hiçbir kenarın
    kullanmadığı dolgu (ör. "resim yok" anlamındaki 65535) çizilmez, listeye girmez."""
    shapes = el.find("shapes")
    if shapes is None:
        return []
    arrays = [fill_style_items(shapes)]
    used = []
    records = shapes.find("shapeRecords")
    for r in records if records is not None else []:
        if r.get("type") != "StyleChangeRecord":
            continue
        if r.get("stateNewStyles") == "true":
            arrays.append(fill_style_items(r))
        for k in ("0", "1"):
            index = int(r.get("fillStyle" + k, "0"))
            if r.get("stateFillStyle" + k) == "true" and 0 < index <= len(arrays[-1]):
                key = (len(arrays) - 1, index - 1)
                if key not in used:
                    used.append(key)
    out = []
    for a, i in sorted(used):
        fs = arrays[a][i]
        if int(fs.get("fillStyleType", "0")) in BITMAP_FILL_TYPES:
            m = xml_matrix(fs.find("bitmapMatrix"))
            out.append((int(fs.get("bitmapId")), [v / 20 for v in m[:4]] + m[4:]))
    return out


def text_records(el):
    out = []
    for r in el.find("textRecords"):
        rec = {}
        if r.get("styleFlagsHasFont") == "true":
            rec["font"] = int(r.get("fontId"))
            rec["height"] = int(r.get("textHeight")) / 20
        if r.get("styleFlagsHasColor") == "true":
            c = r.find("textColor")
            rec["color"] = "#%02X%02X%02X" % (int(c.get("red")), int(c.get("green")), int(c.get("blue")))
        if r.get("styleFlagsHasXOffset") == "true":
            rec["x"] = int(r.get("xOffset")) / 20
        if r.get("styleFlagsHasYOffset") == "true":
            rec["y"] = int(r.get("yOffset")) / 20
        rec["glyphs"] = [[int(g.get("glyphIndex")), int(g.get("glyphAdvance")) / 20] for g in r.find("glyphEntries")]
        out.append(rec)
    return out


def button_record(r):
    states = [s for s, key in (("up", "buttonStateUp"), ("over", "buttonStateOver"), ("down", "buttonStateDown"),
                               ("hit", "buttonStateHitTest")) if r.get(key) == "true"]
    rec = {"states": states, "char": int(r.get("characterId")), "depth": int(r.get("placeDepth")),
           "matrix": xml_matrix(r.find("placeMatrix")), "cxform": xml_cxform(r.find("colorTransform"))}
    if r.get("buttonHasBlendMode") == "true":
        rec["blend"] = swf.BLEND_MODES.get(int(r.get("blendMode")), "normal")
    return rec


# --- Karşılaştırma ------------------------------------------------------------------------------

def ffdec_plain_text(formatted):
    """FFDec'in biçimli yazı dökümü: her kaydın önünde [ ... ] ayar bloğu ve [space N] aralıkları
    vardır; aradaki yazı parçaları birleştirilir. Yazıdaki köşeli ayraç ters bölüyle kaçırılır (\\[),
    ayar bloğundaki tırnaklı değerler köşeli ayraç içerebilir."""
    out = []
    block = quote = False
    i = 0
    while i < len(formatted):
        ch = formatted[i]
        if ch == "\\" and i + 1 < len(formatted):
            if not block:
                out.append(formatted[i + 1])
            i += 2
            continue
        if block:
            if ch == '"':
                quote = not quote
            elif ch == "]" and not quote:
                block = False
        elif ch == "[":
            block = True
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def xml_unescape(text):
    """FFDec XML'i satır sonlarını ters bölüyle yazar (\\r, \\n, \\t)."""
    out = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            out.append({"r": "\r", "n": "\n", "t": "\t", "\\": "\\"}.get(text[i + 1], text[i + 1]))
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def close(a, b):
    """Sayılar TOL payıyla, listeler öğe öğe, geri kalan her şey birebir karşılaştırılır (doğru/yanlış
    değeri bir sayıya eşit sayılmaz)."""
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= TOL * max(1.0, abs(b))
    return a == b


def normalize_ours(op):
    """library.json işlemi → XML'deki biçim (atılmış birim matris ve renk dönüşümü geri eklenmez:
    XML'de bayrak varsa ve değer birimse eşit sayılır)."""
    out = dict(op)
    if "filters" in out:
        out["filters"] = [f["type"] if isinstance(f, dict) else f for f in out["filters"]]
    return out


IDENTITY = {"matrix": [1.0, 0.0, 0.0, 1.0, 0.0, 0.0], "cxform": [[1.0] * 4, [0.0] * 4]}


def same_op(ours, theirs):
    ours = normalize_ours(ours)
    keys = set(ours) | set(theirs)
    for k in keys:
        if k in IDENTITY:
            a = ours.get(k, IDENTITY[k] if k in theirs else None)
            b = theirs.get(k, IDENTITY[k] if k in ours else None)
            if not close(a, b):
                return f"{k}: bizim {ours.get(k)} / FFDec {theirs.get(k)}"
        elif not close(ours.get(k), theirs.get(k)):
            return f"{k}: bizim {ours.get(k)} / FFDec {theirs.get(k)}"
    return None


def compare_timeline(name, ours, theirs, problems):
    """ours: library.json zaman çizelgesi; theirs: XmlTimeline."""
    if len(ours["frames"]) != len(theirs.frames):
        problems.append(f"{name}: kare sayısı bizim {len(ours['frames'])} / FFDec {len(theirs.frames)}")
        return 0
    checked = 0
    for i, (a, b) in enumerate(zip(ours["frames"], theirs.frames)):
        if len(a) != len(b):
            problems.append(f"{name} kare {i + 1}: işlem sayısı bizim {len(a)} / FFDec {len(b)}")
            continue
        for x, y in zip(a, b):
            diff = same_op(x, y)
            checked += 1
            if diff:
                problems.append(f"{name} kare {i + 1} derinlik {y.get('depth', y.get('remove'))}: {diff}")
    if ours.get("labels", {}) != theirs.labels:
        problems.append(f"{name}: etiketler farklı")
    if {int(k): v for k, v in ours.get("sounds", {}).items()} != theirs.sounds:
        problems.append(f"{name}: ses başlatmaları farklı")
    return checked


def check_game(game, visual):
    swf_path = os.path.join(os.environ.get("SWF_KOK", os.path.join(ROOT, "..", "swf-oyunlar")), aktar.GAMES[game])
    archive = os.path.join(ROOT, "referans", game, "tam")
    content = os.path.join(ROOT, "content", "feudalism", game)
    with open(os.path.join(content, "library.json"), encoding="utf-8") as f:
        lib = json.load(f)
    with open(os.path.join(content, "texts.json"), encoding="utf-8") as f:
        texts = json.load(f)
    with open(os.path.join(ROOT, "kaynak", "feudalism", game, "manifest.json"), encoding="utf-8") as f:
        man = json.load(f)
    movie = swf.Movie(swf_path)
    dump = XmlDump(os.path.join(archive, "swf.xml"))
    rows = []
    problems = []

    def row(name, count, probs):
        rows.append((name, count, len(probs)))
        problems.extend(probs)

    # 1. Etiket sayıları
    ours_top = {k: v for k, v in aktar.named_counts(movie.tag_counts).items() if k != "End"}
    ours_in = {k: v for k, v in aktar.named_counts(movie.sprite_tag_counts).items() if k != "End"}
    probs = [f"en dış düzey {k}: bizim {ours_top.get(k)} / FFDec {dump.counts.get(k)}"
             for k in sorted(set(ours_top) | set(dump.counts)) if ours_top.get(k) != dump.counts.get(k)]
    probs += [f"sprite içi {k}: bizim {ours_in.get(k)} / FFDec {dump.sprite_counts.get(k)}"
              for k in sorted(set(ours_in) | set(dump.sprite_counts)) if ours_in.get(k) != dump.sprite_counts.get(k)]
    row("Etiket türlerinin sayıları", sum(ours_top.values()) + sum(ours_in.values()), probs)
    # 2. Karakterler
    ours_chars = {int(k): v["type"] for k, v in man["characters"].items()}
    probs = [f"karakter {c}: bizim {ours_chars.get(c)} / FFDec {dump.chars.get(c)}"
             for c in sorted(set(ours_chars) | set(dump.chars)) if ours_chars.get(c) != dump.chars.get(c)]
    probs += [f"karakter {c}: listede yeri yok" for c, v in man["characters"].items()
              if v["where"] in ("EKSİK", "") or not v["where"]]
    for c, v in man["characters"].items():
        w = v["where"]
        if not w.startswith("yalnız yerel") and w not in ("library.json", "texts.json") \
                and not os.path.exists(os.path.join(content, w)):
            probs.append(f"karakter {c}: dosyası yok ({w})")
    row("Karakterler (tür ve yer)", len(ours_chars), probs)
    # 3. Zaman çizelgeleri
    probs = []
    checked = compare_timeline("kök film", lib["root"], dump.root, probs)
    for sid, t in lib["sprites"].items():
        checked += compare_timeline(f"sprite {sid}", t, dump.sprites[int(sid)], probs)
    excluded = {int(k) for k in lib["excluded"]}
    missing = [s for s in dump.sprites if str(s) not in lib["sprites"] and s not in excluded]
    probs += [f"sprite {s}: library.json'da yok ve yerel arşiv listesinde de değil" for s in missing]
    row("Zaman çizelgeleri: her yerleştirme ve kaldırma, etiketler, sesler (durdurma, tekrar, zarf dahil)",
        checked, probs)
    # 4. Düğmeler
    probs = []
    for bid, recs in lib["buttons"].items():
        theirs = dump.buttons[int(bid)]
        if len(recs) != len(theirs):
            probs.append(f"düğme {bid}: kayıt sayısı {len(recs)} / {len(theirs)}")
            continue
        for a, b in zip(recs, theirs):
            diff = same_op({k: v for k, v in a.items()}, b)
            if diff:
                probs.append(f"düğme {bid}: {diff}")
    row("Düğmeler (her kayıt)", sum(len(r) for r in lib["buttons"].values()), probs)
    # Dışa aktarılan adlar
    expected = {n: c for n, c in dump.exports.items() if not aktar.is_component_export(n) and c not in excluded}
    probs = [f"dışa aktarılan {n}: bizim {lib['exports'].get(n)} / FFDec {expected.get(n)}"
             for n in sorted(set(expected) | set(lib["exports"])) if lib["exports"].get(n) != expected.get(n)]
    row("Dışa aktarılan adlar", len(dump.exports), probs)
    # Sabit yazılar
    probs = []
    for tid, t in texts["texts"].items():
        theirs = dump.texts[int(tid)]
        ours = [{k: v for k, v in r.items() if k != "alpha"} for r in t["records"]]
        if len(ours) != len(theirs):
            probs.append(f"yazı {tid}: kayıt sayısı farklı")
            continue
        for a, b in zip(ours, theirs):
            if not close(a.get("glyphs"), b.get("glyphs")) or any(not close(a.get(k), b.get(k))
                                                                     for k in ("font", "height", "color", "x", "y")):
                probs.append(f"yazı {tid}: kayıt farklı")
    probs += [f"yazı {t}: texts.json'da yok" for t in dump.texts if str(t) not in texts["texts"]
              and man["characters"][str(t)]["where"] != "yalnız yerel arşiv"
              and not man["characters"][str(t)]["where"].startswith("yalnız yerel")]
    # Çözülmüş yazı FFDec'in düz yazı dökümüyle aynı mı
    for tid, t in texts["texts"].items():
        path = os.path.join(archive, "texts", f"{tid}.txt")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                plain = ffdec_plain_text(f.read())
            if "".join(plain.split()) != "".join(t["text"].split()):
                probs.append(f"yazı {tid}: çözülen yazı FFDec'inkinden farklı: {t['text']!r} / {plain!r}")
    row("Sabit yazılar (glif glif ve çözülmüş yazı)", sum(len(t["records"]) for t in texts["texts"].values()), probs)
    # Yazı alanları
    probs = []
    for eid, e in texts["edit_texts"].items():
        x = dump.edit_texts[int(eid)]
        if e.get("variable", "") != xml_unescape(x.get("variableName", "")):
            probs.append(f"yazı alanı {eid}: değişken adı farklı")
        if x.get("hasText") == "true" and e.get("text", "") != xml_unescape(x.get("initialText", "")):
            probs.append(f"yazı alanı {eid}: başlangıç yazısı farklı")
        if x.get("hasFont") == "true" and (e.get("font") != int(x["fontId"])
                                           or not close(e.get("font_height"), int(x["fontHeight"]) / 20)):
            probs.append(f"yazı alanı {eid}: yazı tipi ya da boyu farklı")
    row("Yazı alanları (değişken, yazı, yazı tipi, boy)", len(texts["edit_texts"]), probs)
    # 5. Sesler
    probs = []
    for sid, s in lib["sounds"].items():
        with open(os.path.join(content, s["file"]), "rb") as f:
            data = f.read()
        raw = dump.sounds[int(sid)]
        if data != raw[2:]:
            probs.append(f"ses {sid}: dosya SWF'deki MP3 verisiyle aynı değil")
        seek = int.from_bytes(raw[:2], "little", signed=True)
        if s.get("seek") != seek or s.get("samples") != dump.sound_samples[int(sid)] or s.get("bytes") != len(data):
            probs.append(f"ses {sid}: gecikme, örnek sayısı ya da boyut farklı ({s.get('seek')}/{seek}, "
                         f"{s.get('samples')}/{dump.sound_samples[int(sid)]}, {s.get('bytes')}/{len(data)})")
        if not data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xe3", b"\xff\xf2", b"\xff\xfa") and data[:3] != b"ID3":
            probs.append(f"ses {sid}: MP3 çerçeve başlığı yok")
    row("Sesler (baytlar, örnek sayısı ve MP3 gecikmesi SWF'dekiyle aynı)", len(lib["sounds"]), probs)
    # Resimler
    probs = []
    from PIL import Image
    for bid, rel in lib["images"].items():
        el = dump.images[int(bid)]
        jpeg = bytes.fromhex(el.get("jpegData") or el.get("imageData") or "")
        size = swf.jpeg_size(jpeg) or swf.jpeg_size(dump.jpeg_tables + jpeg)
        try:
            with Image.open(os.path.join(content, rel)) as im:
                im.load()
                if size and im.size != size:
                    probs.append(f"resim {bid}: boyut {im.size} / SWF {size}")
        except Exception as e:  # noqa: BLE001 - denetim her hatayı rapor eder
            probs.append(f"resim {bid}: açılamadı ({e})")
    row("Resimler (açılıyor, boyutu SWF'dekiyle aynı)", len(lib["images"]), probs)
    # 7. Kod: FFDec her kod parçasını ayrı .as dosyasına yazar (kare kodu, sınıf, düğme, klip eylemi)
    files = sum(1 for _, _, names in os.walk(os.path.join(ROOT, "kaynak", "feudalism", game, "kod"))
                for n in names if n.endswith(".as"))
    expected = sum(dump.scripts.values())
    probs = [] if files == expected else [f"kod dosyası {files} / SWF'deki kod parçası {expected} {dump.scripts}"]
    row("Kod parçaları (kare, sınıf, düğme, klip eylemleri)", expected, probs)
    row("Resim dolgulu şekiller (desen matrisi ve resmi SWF'dekiyle aynı)", len(lib["bitmap_shapes"]),
        bitmap_shape_problems(game, lib, dump))
    row("İnce çizgi işaretleri (FFDec'in SVG'sindekilerle aynı)", len(lib["shapes"]) + len(lib["bitmap_shapes"]),
        hairline_problems(game, lib, archive))
    swf_root = os.environ.get("SWF_KOK", os.path.join(ROOT, "..", "swf-oyunlar"))
    t_probs, g_probs, c_probs, f_probs = translation_problems(game, lib, texts, dump, swf_root, archive)
    row("Türkçe çeviri tabloları (kaynağıyla bayt bayt aynı)", len(ceviri.TABLES), t_probs)
    row("Çeviri hedefleri (her yazı, kutu, yazı tipi ve çizim SWF'de; parça sayısı kayıt sayısıyla aynı)",
        sum(lib.get("translation", {}).get("counts", {}).get(k, 0) for k in ("texts", "edit_texts", "drawn_texts")),
        g_probs)
    row("Koddaki çeviriler (çevirinin aracı FFDec'in kod dökümüne yeniden uygulanınca aynı)",
        lib.get("translation", {}).get("counts", {}).get("code_files", 0), c_probs)
    row("Yazı tiplerinin açık lisanslı karşılıkları (dosya kaynağıyla aynı, lisansı yanında)", len(texts["fonts"]),
        f_probs)
    row("Morph sınırları (iki ucun SWF'deki sınırlarının birleşimi)", len(lib["morphs"]),
        morph_bounds_problems(game, lib, dump))
    # 6. Şekillerin görsel karşılaştırması
    if visual:
        probs, worst = compare_shapes(game, lib, archive)
        row(f"Şekiller: motorun çizimi FFDec'inkiyle piksel piksel (en kötü fark %{worst:.2f})",
            len(lib["shapes"]), probs)
        probs, worst = compare_morphs(game, lib, archive)
        row(f"Morph başlangıç ve bitişleri piksel piksel (en kötü fark %{worst:.2f})", 2 * len(lib["morphs"]), probs)
        probs, worst = compare_drawn_texts(game, lib)
        row(f"Çizilmiş yazıların Türkçe hâlleri, Türkçe SWF'nin çizimiyle (en kötü fark %{worst:.2f})",
            len(lib.get("translation", {}).get("drawn_texts", {})), probs)
    return rows, problems


# --- Görsel karşılaştırma -------------------------------------------------------------------------

PIXEL_LIMIT = 2.0  # izin verilen ortalama renk farkı (%, 0–100); kenar yumuşatma farkları için pay


def pixel_difference(a, b, offset_a=(0, 0), offset_b=(0, 0)):
    """İki RGBA resmin ortalama renk farkı (%, 0–100). Resimler gerilmez: her biri kendi kaymasıyla
    (piksel, aynı koordinat düzleminde) beyaz bir tuvale konur, tuvalin tamamı karşılaştırılır."""
    from PIL import Image, ImageChops
    x0 = min(offset_a[0], offset_b[0])
    y0 = min(offset_a[1], offset_b[1])
    x1 = max(offset_a[0] + a.width, offset_b[0] + b.width)
    y1 = max(offset_a[1] + a.height, offset_b[1] + b.height)
    size = (int(round(x1 - x0)), int(round(y1 - y0)))

    def place(im, off):
        canvas = Image.new("RGBA", size, (255, 255, 255, 255))
        canvas.alpha_composite(im.convert("RGBA"), (int(round(off[0] - x0)), int(round(off[1] - y0))))
        return canvas.convert("RGB")
    diff = ImageChops.difference(place(a, offset_a), place(b, offset_b)).convert("L")
    total = sum(i * n for i, n in enumerate(diff.histogram()))
    return 100 * total / (255 * size[0] * size[1])


def render_all(jobs):
    """[(svg, png, ölçek)] → motorun toplu çizicisiyle (tek süreç) PNG'ler."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("\n".join(f"{a}\t{b}\t{c}" for a, b, c in jobs) + "\n")
        name = f.name
    try:
        subprocess.run([os.path.join(ROOT, "target", "release", "examples", "svg-batch"), name], check=True,
                       capture_output=True)
    finally:
        os.remove(name)


def ink_centre(im):
    """Resmin mürekkep (beyazdan uzaklık × örtücülük) ağırlıklı merkezi, piksel olarak; boş resimde None."""
    import numpy as np
    rgba = np.asarray(im.convert("RGBA"), dtype=np.float64) / 255.0
    ink = (1.0 - rgba[..., :3].mean(axis=2)) * rgba[..., 3]
    total = ink.sum()
    if total <= 0:
        return None
    ys, xs = np.indices(ink.shape)
    return (float((xs * ink).sum() / total), float((ys * ink).sum() / total))


def best_offset(a, b, window=3):
    """b'nin a'ya göre kaymasını bulur: önce iki resmin mürekkep merkezleri üst üste konur, sonra
    çevresinde ±window piksel içinde en iyi örtüşme aranır (FFDec'in morph PNG dökümleri sınıra
    belgelenmemiş bir pay ekler; bu yüzden yer resmin kendisinden ölçülür)."""
    import numpy as np
    from PIL import Image

    def gray(im):
        white = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return np.asarray(Image.alpha_composite(white, im.convert("RGBA")).convert("L"), dtype=np.float32)
    ca, cb = ink_centre(a), ink_centre(b)
    if ca is None or cb is None:
        return (0, 0)
    ga, gb = gray(a), gray(b)
    gx, gy = int(round(ca[0] - cb[0])), int(round(ca[1] - cb[1]))
    best = None
    for dy in range(-window, window + 1):
        for dx in range(-window, window + 1):
            ox, oy = gx + dx, gy + dy
            x0, y0 = max(0, ox), max(0, oy)
            x1, y1 = min(ga.shape[1], ox + gb.shape[1]), min(ga.shape[0], oy + gb.shape[0])
            if x1 <= x0 or y1 <= y0:
                continue
            # Örtüşmeyen kısımlar beyaz sayılır: bütün mürekkep karşılaştırılmış olur
            d = float(np.abs(ga[y0:y1, x0:x1] - gb[y0 - oy:y1 - oy, x0 - ox:x1 - ox]).sum()
                      + (255 - ga).sum() - (255 - ga[y0:y1, x0:x1]).sum()
                      + (255 - gb).sum() - (255 - gb[y0 - oy:y1 - oy, x0 - ox:x1 - ox]).sum())
            if best is None or d < best[0]:
                best = (d, ox, oy)
    return (best[1], best[2]) if best else (gx, gy)


PATTERN = re.compile(r"<pattern\b.*?</pattern>", re.S)


def svg_patterns(svg):
    """SVG'deki desenler: [(desen matrisi, desenin resim baytları)]."""
    out = []
    for m in PATTERN.finditer(svg):
        tag = m.group(0)
        mat = re.search(r'patternTransform="matrix\(([^)]*)\)"', tag)
        data = re.search(r"base64,([A-Za-z0-9+/=]+)", tag)
        out.append(([float(v) for v in mat.group(1).split(",")] if mat else [1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                    base64.b64decode(data.group(1)) if data else b""))
    return out


def image_difference(a, b):
    """İki resmin piksel piksel en büyük kanal farkı (0–255); boyutlar farklıysa None."""
    import numpy as np
    from PIL import Image
    with Image.open(io.BytesIO(a) if isinstance(a, bytes) else a) as ia, \
            Image.open(io.BytesIO(b) if isinstance(b, bytes) else b) as ib:
        if ia.size != ib.size:
            return None
        return int(np.abs(np.asarray(ia.convert("RGBA"), dtype=np.int16)
                          - np.asarray(ib.convert("RGBA"), dtype=np.int16)).max())


IMAGE_TOLERANCE = 2  # JPEG çözücüleri arasında izin verilen en büyük kanal farkı


def bitmap_shape_problems(game, lib, dump):
    """Resim dolgulu şekiller: SWF'de resim dolgusu olan her şekil aktarılmış mı; her desenin matrisi SWF'deki
    dolgu matrisi mi; desenin resmi, aktardığımız resim dosyasıyla piksel piksel aynı mı."""
    probs = []
    excluded = {int(k) for k in lib["excluded"]}
    content = os.path.join(ROOT, "content", "feudalism", game)
    for sid in sorted(set(dump.bitmap_fills) - {int(k) for k in lib["bitmap_shapes"]} - excluded):
        probs.append(f"{game} şekil {sid}: SWF'de resim dolgusu var ama resim dolgulu şekiller arasında yok")
    for sid in lib["bitmap_shapes"]:
        fills = dump.bitmap_fills.get(int(sid), [])
        if not fills:
            probs.append(f"{game} şekil {sid}: SWF'de resim dolgusu yok")
            continue
        with open(os.path.join(content, "shapes-bitmap", f"{sid}.svg"), encoding="utf-8") as f:
            patterns = svg_patterns(f.read())
        used = set()
        for k, (matrix, data) in enumerate(patterns, 1):
            match = [i for i, (_, m) in enumerate(fills) if close(m, matrix)]
            if not match:
                probs.append(f"{game} şekil {sid} desen {k}: matrisi SWF'deki hiçbir resim dolgusuna uymuyor")
                continue
            used.update(match)
            bid = fills[match[0]][0]
            rel = lib["images"].get(str(bid))
            if rel is None:
                probs.append(f"{game} şekil {sid} desen {k}: resim {bid} aktarılmamış")
                continue
            d = image_difference(data, os.path.join(content, rel))
            if d is None or d > IMAGE_TOLERANCE:
                probs.append(f"{game} şekil {sid} desen {k}: resmi {rel} ile aynı değil (fark {d})")
        probs += [f"{game} şekil {sid}: SWF'deki resim dolgusu {i + 1} (resim {fills[i][0]}) SVG'de yok"
                  for i in range(len(fills)) if i not in used]
    return probs


def compare_rendered(pairs, search=False):
    """[(ad, bizim png, bizim kayma, FFDec png, FFDec kayma)] → (sorunlar, en kötü fark). `search`:
    FFDec çiziminin yerini en iyi örtüşmeyle bul."""
    from PIL import Image
    probs, worst = [], 0.0
    for name, ours, off_ours, theirs, off_theirs in pairs:
        if not os.path.exists(ours):
            probs.append(f"{name}: motor çizemedi")
            continue
        if not os.path.exists(theirs):
            probs.append(f"{name}: FFDec'in çizimi yok")
            continue
        with Image.open(ours) as a, Image.open(theirs) as b:
            if search:
                off_ours, off_theirs = (0, 0), best_offset(a, b)
            d = pixel_difference(a, b, off_ours, off_theirs)
        worst = max(worst, d)
        if d > PIXEL_LIMIT:
            probs.append(f"{name}: piksel farkı %{d:.2f}")
    return probs, worst


HAIRLINE_PATH = re.compile(r'<path\b[^>]*\bdata-hairline="true"[^>]*>')


def hairline_svg(svg, scale):
    """Flash'ın ince çizgi kuralını SVG'ye uygular: 1 pikselden ince çizgi ekranda 1 piksel çizilir,
    yani kalınlık = en büyüğü(asıl kalınlık, 1 / ölçek). Motor bu kuralı oynatıcıda uygulayacak
    (library.json'daki "hairlines"); denetim, ayıklanan verinin doğruluğunu aynı kuralla çizerek sınar."""
    def fix(m):
        tag = m.group(0)
        original = re.search(r'data-original-stroke-width="([\d.]+)"', tag)
        if not original:
            return tag
        width = max(float(original.group(1)), 1.0 / scale)
        return re.sub(r'stroke-width="[\d.]+"', f'stroke-width="{width:g}"', tag)
    return HAIRLINE_PATH.sub(fix, svg)


def compare_shapes(game, lib, archive):
    """Şekiller 4 kat büyütülerek çizilir; iki çizim de şeklin sınırının sol üst köşesinden başlar.
    İnce çizgili şekiller `hairline_svg` kuralıyla çizilir."""
    ref_png = os.path.join(ROOT, "referans", game, "png")
    scale = 4
    with tempfile.TemporaryDirectory() as td:
        jobs = []
        for sid in lib["shapes"]:
            src = os.path.join(ROOT, "content", "feudalism", game, "shapes", f"{sid}.svg")
            if str(sid) in lib.get("hairlines", {}):
                with open(src, encoding="utf-8") as f:
                    svg = hairline_svg(f.read(), scale)
                src = os.path.join(td, f"{sid}.svg")
                with open(src, "w", encoding="utf-8") as f:
                    f.write(svg)
            jobs.append((src, os.path.join(td, f"{sid}.png"), scale))
        render_all(jobs)
        return compare_rendered([(f"{game} şekil {sid}", os.path.join(td, f"{sid}.png"), (0, 0),
                                  os.path.join(ref_png, f"{sid}.png"), (0, 0)) for sid in lib["shapes"]])


def hairline_problems(game, lib, archive):
    """Her şeklin ince çizgi işaretleri FFDec'in SVG'sindekilerle aynı sayıda mı, library.json'daki
    "hairlines" listesi de SVG'deki işaretlerle aynı mı."""
    probs = []
    content = os.path.join(ROOT, "content", "feudalism", game)
    for folder, ids in (("shapes", lib["shapes"]), ("shapes-bitmap", lib["bitmap_shapes"])):
        for sid in ids:
            with open(os.path.join(content, folder, f"{sid}.svg"), encoding="utf-8") as f:
                ours = f.read().count('data-hairline="true"')
            with open(os.path.join(archive, "shapes", f"{sid}.svg"), encoding="utf-8") as f:
                theirs = f.read().count('ffdec:has-small-stroke="true"')
            listed = len(lib.get("hairlines", {}).get(str(sid), []))
            if ours != theirs or listed != ours:
                probs.append(f"{game} şekil {sid}: ince çizgi bizim {ours} / listede {listed} / FFDec {theirs}")
    return probs


def file_hash(path):
    import hashlib
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tree_files(folder):
    """Klasördeki dosyalar: göreli yol → içerik."""
    out = {}
    for d, _, names in os.walk(folder):
        for n in names:
            with open(os.path.join(d, n), "rb") as f:
                out[os.path.relpath(os.path.join(d, n), folder).replace(os.sep, "/")] = f.read()
    return out


def translation_problems(game, lib, texts, dump, swf_root, archive):
    """Türkçe çeviri: tablolar kaynağıyla bayt bayt aynı mı; her girdinin hedefi FFDec'in dökümünde var mı
    ve sabit yazıların parça sayısı XML'deki kayıt sayısıyla aynı mı; kod çevirisi, çevirinin aracı FFDec'in
    kod dökümüne yeniden uygulandığında aynı mı; her yazı tipinin açık lisanslı karşılığı ve lisansı yerinde
    mi. Dönen: (tablo sorunları, hedef sorunları, kod sorunları, yazı tipi sorunları)."""
    src = os.path.join(swf_root, ceviri.TRANSLATIONS[game], "ceviri")
    content = os.path.join(ROOT, "content", "feudalism", game)
    tables_probs = []
    for name in ceviri.TABLES:
        ours = os.path.join(content, "ceviri", f"{name}.json")
        if not os.path.exists(ours) or file_hash(ours) != file_hash(os.path.join(src, f"{name}.json")):
            tables_probs.append(f"{game} çeviri {name}.json: kaynağıyla aynı değil")
    tables = ceviri.load_tables(src)
    target_probs = []
    for tid, entry in ceviri.entries(tables["sabit"]).items():
        if int(tid) not in dump.texts:
            target_probs.append(f"{game} sabit yazı {tid}: SWF'de yok")
        elif len(entry["parcalar"]) != len(dump.texts[int(tid)]):
            target_probs.append(f"{game} sabit yazı {tid}: çeviride {len(entry['parcalar'])} parça, SWF'de "
                                f"{len(dump.texts[int(tid)])} kayıt")
    target_probs += [f"{game} ekran kutusu {eid}: SWF'de yok" for eid in ceviri.entries(tables["kutular"])
                     if int(eid) not in dump.edit_texts]
    target_probs += [f"{game} yazı tipi {fid}: SWF'de yok" for fid in ceviri.entries(tables["yazitipleri"])
                     if dump.chars.get(int(fid)) != "font"]
    for sid in ceviri.entries(tables["sekiller"]):
        if dump.chars.get(int(sid)) != "shape":
            target_probs.append(f"{game} çizilmiş yazı {sid}: SWF'de şekil değil")
        if lib.get("translation", {}).get("drawn_texts", {}).get(sid, {}).get("file") != f"ceviri/sekiller/{sid}.svg":
            target_probs.append(f"{game} çizilmiş yazı {sid}: library.json'da yok")
    with tempfile.TemporaryDirectory() as td:
        try:
            ceviri.translate_code(swf_root, os.path.join(archive, "scripts"), src, os.path.join(td, "kod-tr"))
            expected = tree_files(os.path.join(td, "kod-tr"))
        except ValueError as e:
            expected = None
            code_probs = [f"{game} kod çevirisi FFDec'in kod dökümüne uygulanamadı: {e}"]
    if expected is not None:
        ours = tree_files(os.path.join(ROOT, "kaynak", "feudalism", game, "kod-tr"))
        code_probs = [f"{game} çevrilmiş kod {n}: yeniden üretilenle aynı değil" for n in sorted(set(expected) | set(ours))
                      if expected.get(n) != ours.get(n)]
    font_probs = []
    table = tables["yazitipleri"]
    for fid, font in texts["fonts"].items():
        rel = ceviri.font_file(fid, font, table)
        path = os.path.join(ROOT, "content", font.get("file", "?"))
        if rel is None or font.get("file") != f"fonts/{os.path.basename(rel)}":
            font_probs.append(f"{game} yazı tipi {fid}: karşılığı yanlış ({font.get('file')} / {rel})")
        elif not os.path.exists(path) or file_hash(path) != file_hash(os.path.join(swf_root, rel)):
            font_probs.append(f"{game} yazı tipi {fid}: {font['file']} kaynağıyla aynı değil")
        else:
            lic = next((name for prefix, (_, name) in ceviri.FONT_LICENSES.items()
                        if os.path.basename(rel).startswith(prefix)), None)
            if lic is None or not os.path.exists(os.path.join(ROOT, "content", "fonts", lic)):
                font_probs.append(f"{game} yazı tipi {fid}: lisans metni yok")
    return tables_probs, target_probs, code_probs, font_probs


def compare_drawn_texts(game, lib):
    """Çizilmiş yazıların Türkçe hâlleri: motorun çizimi, Türkçe SWF'nin FFDec çizimiyle (4×)."""
    drawn = lib.get("translation", {}).get("drawn_texts", {})
    with tempfile.TemporaryDirectory() as td:
        jobs = [(os.path.join(ROOT, "content", "feudalism", game, d["file"]), os.path.join(td, f"{sid}.png"), 4)
                for sid, d in drawn.items()]
        render_all(jobs)
        return compare_rendered([(f"{game} çizilmiş yazı {sid}", os.path.join(td, f"{sid}.png"), (0, 0),
                                  os.path.join(ROOT, "referans", game, "tr", "png", f"{sid}.png"), (0, 0))
                                 for sid in drawn])


def morph_bounds_problems(game, lib, dump):
    """Morph uçlarımızın tuvali iki ucun SWF'deki sınırlarının birleşimi mi (başlangıç noktası ve boyut)."""
    probs = []
    for mid, origin in lib["morphs"].items():
        b = dump.morph_bounds[int(mid)]
        x0, y0 = min(b["start"][0], b["end"][0]), min(b["start"][1], b["end"][1])
        x1, y1 = max(b["start"][2], b["end"][2]), max(b["start"][3], b["end"][3])
        if not close(origin, [x0, y0]):
            probs.append(f"{game} morph {mid}: başlangıç noktası {origin} / SWF {[x0, y0]}")
        for end in ("start", "end"):
            with open(os.path.join(ROOT, "content", "feudalism", game, "morphs", f"{mid}.{end}.svg"),
                      encoding="utf-8") as f:
                head = f.read(400)
            size = [float(re.search(rf'{k}="([\d.]+)px"', head).group(1)) for k in ("width", "height")]
            if not close(size, [x1 - x0, y1 - y0]):
                probs.append(f"{game} morph {mid} {end}: boyut {size} / SWF {[x1 - x0, y1 - y0]}")
    return probs


def compare_morphs(game, lib, archive):
    """Morph uçları şekiller gibi 4 kat büyütülerek çizilir. FFDec'in morph PNG'leri sınıra belgelenmemiş
    bir pay eklediği için iki çizim, mürekkep merkezleri ve en iyi örtüşmeyle hizalanır (sınırın
    kendisi `morph_bounds_problems` ile sayısal olarak ayrıca denetlenir)."""
    with tempfile.TemporaryDirectory() as td:
        jobs, pairs = [], []
        for mid in lib["morphs"]:
            for end in ("start", "end"):
                out = os.path.join(td, f"{mid}.{end}.png")
                jobs.append((os.path.join(ROOT, "content", "feudalism", game, "morphs", f"{mid}.{end}.svg"), out, 4))
                pairs.append((f"{game} morph {mid} {end}", out, (0, 0),
                              os.path.join(archive, "morph-png", f"{mid}.{end}.png"), (0, 0)))
        render_all(jobs)
        return compare_rendered(pairs, search=True)


def main(argv):
    visual = "--gorsel" in argv
    out = ["# Ayıklama denetimi", "",
           "`python3 araclar/aktar/denetim.py --gorsel` üretir. Oyuna aktarılanı FFDec'in kendi",
           "ayrıştırıcısıyla ürettiği XML dökümüyle kayıt kayıt karşılaştırır; şekilleri motorun çizimiyle",
           "FFDec'in çizimi arasında piksel piksel karşılaştırır.", ""]
    all_problems = 0
    for game in ("f1", "f2"):
        rows, problems = check_game(game, visual)
        all_problems += len(problems)
        out += [f"## {'Feudalism' if game == 'f1' else 'Feudalism 2'} ({game})", "",
                "| Denetim | Denetlenen | Sorun |", "|---|---|---|"]
        out += [f"| {n} | {c} | {p} |" for n, c, p in rows]
        out.append("")
        if problems:
            out += ["Sorunlar:", ""] + [f"- {p}" for p in problems[:300]]
            if len(problems) > 300:
                out.append(f"- … ve {len(problems) - 300} sorun daha")
            out.append("")
        print(game, " | ".join(f"{n}: {p}" for n, c, p in rows))
    out.append(f"Toplam sorun: {all_problems}.")
    out += ["", "## Yöntem ve sınırlar", "",
            "- Kaynak: SWF'yi bizim ayrıştırıcımızdan bağımsız okuyan FFDec 24.1.1'in XML dökümü (`-swf2xml`)",
            "  ve FFDec'in kendi PNG çizimleri (şekiller ve morph uçları 4× büyütülmüş).",
            "- Piksel farkı: iki çizim beyaz tuvale gerilmeden konur, ortalama renk farkı %2'yi aşarsa sorun",
            "  sayılır (kenar yumuşatma farkları için pay).",
            "- İnce çizgiler: Flash 1 pikselden ince çizgiyi ekranda 1 piksel çizer. Bu çizgiler",
            "  `data-hairline` ile işaretli aktarılır ve library.json'da listelenir; denetim onları bu kuralla",
            "  çizer. Motor kuralı oynatıcıda uygulayacak (Faz B).",
            "- Morph uçları: FFDec'in morph PNG'leri sınıra belgelenmemiş bir pay ekler; çizimler mürekkep",
            "  merkezi ve en iyi örtüşmeyle hizalanır. Sınırın kendisi XML'deki iki ucun sınırıyla sayısal",
            "  olarak ayrıca denetlenir.",
            "- Resim dolgulu şekiller (zemin dokuları): motor resim dolgusunu henüz çizmediği için sayısal",
            "  denetlenir: kenarların kullandığı her resim dolgusunun SVG'deki desen matrisi SWF'deki dolgu",
            "  matrisiyle, desenin resmi aktarılan resim dosyasıyla piksel piksel aynıdır. Görsel karşılaştırma",
            "  motor resim dolgusunu çizdiğinde eklenecek (Faz B).",
            "- Sesler: dosyalar SWF'deki MP3 verisiyle bayt bayt, örnek sayısı ve MP3 başlangıç gecikmesi",
            "  XML'deki değerlerle aynıdır. Zaman çizelgelerindeki ses kayıtları durdurma, tekrar, giriş/çıkış",
            "  noktası ve zarf bilgisiyle karşılaştırılır.",
            "- Türkçe çeviri: tablolar kaynağıyla (swf-oyunlar) bayt bayt aynıdır; her girdinin hedefi FFDec'in",
            "  dökümünde aranır, sabit yazıların parça sayısı XML'deki kayıt sayısıyla karşılaştırılır. Kod",
            "  çevirisi, çevirinin kendi aracı FFDec'in kod dökümüne yeniden uygulanarak sınanır. \"Öldün...\"",
            "  çizimi Türkçe SWF'nin FFDec çizimiyle piksel piksel karşılaştırılır.",
            "- Aktarılmayanlar (yerel arşivde): sponsor logoları, Macromedia/Adobe arayüz bileşenleri, gömülü",
            "  yazı tipleri (yerine açık lisanslı karşılıkları). Listesi ve nedenleri",
            "  `kaynak/feudalism/<oyun>/manifest.json` içindedir."]
    with open(os.path.join(ROOT, "docs", "AYIKLAMA_DENETIMI.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
