"""Feudalism 1 ve 2'nin görsellerini oyunun içerik klasörüne aktarır.

Görseller hak sahibinin izniyle kullanılır (bkz. docs/LISANSLAR.md). Aktarılan:

- şekiller: FFDec'in SVG çıktısı, motorun okuduğu biçimde (`content/feudalism/<oyun>/shapes/<id>.svg`);
- sembol kütüphanesi (`content/feudalism/<oyun>/library.json`): sahne bilgisi, dışa aktarılan adlar,
  sprite ve kök film zaman çizelgeleri (kare kare yerleştir / taşı / kaldır işlemleri), kare
  etiketleri, kare betiklerinden çıkarılan basit komutlar (dur, oynat, git, olay), düğmeler.

Aktarılmayan (hak sahibinin olmayan ya da lisansı ayrı olan):

- sponsor logoları (ArcadeTown, Newgrounds): `EXCLUDED`;
- Macromedia/Adobe arayüz bileşenleri (mx.*): `is_component_export`;
- gömülü yazı tipleri (yazı tiplerinin lisansı yazı tipi yapımcısındadır).

Henüz aktarılmayan (sonraki adımlar): bit eşlem dolgulu şekiller, resimler, morph şekiller, yazılar,
sesler. Kütüphanede kimlikleriyle listelenirler; oynatıcı onları şimdilik çizmez.

Kullanım (depo kökünden; önce araclar/olcum/cikar.sh çalıştırılmış olmalı):
    python3 araclar/aktar/aktar.py [swf-oyunlar klasörü]
"""
import json
import math
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swf  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GAMES = {
    "f1": "oyunlar/feudalism/feudalism-orijinal.swf",
    "f2": "oyunlar/feudalism-2/feudalism-2-orijinal.swf",
}
# Oyunun yazarına ait olmayan, aktarılmayan karakterler (kimlik → neden)
EXCLUDED = {
    "f1": {140: "açılıştaki ArcadeTown ve Newgrounds logoları (sponsor)"},
    "f2": {},
}
# Macromedia/Adobe v2 arayüz bileşenlerinin dışa aktarılan adları
COMPONENT_EXPORTS = re.compile(
    r"^(Border|BoundingBox|Brdr\w+|Btn\w*Arrow|Button|ButtonSkin|Combo\w+|CustomBorder|Data\w+|Defaults|"
    r"Focus\w+|HScrollBar|List|NumericStepper\w*|RectBorder|Scroll\w+|SelectableRow|SimpleButton\w*|"
    r"Step\w+|TextInput|Thumb\w+|UI\w+|VScrollBar|View)$")


def is_component_export(name):
    return name.startswith("__Packages.") or bool(COMPONENT_EXPORTS.match(name))


def round_list(values, digits=4):
    return [round(v, digits) for v in values]


def clean_op(op):
    """Zaman çizelgesi işlemini JSON için sadeleştirir (yuvarlama, birim değerleri atma)."""
    out = {}
    for k, v in op.items():
        if k == "matrix":
            if v != [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]:
                out[k] = round_list(v)
        elif k == "cxform":
            if v != [[1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]]:
                out[k] = [round_list(v[0]), round_list(v[1])]
        elif k == "ratio":
            out[k] = round(v, 5)
        else:
            out[k] = v
    return out


# --- Kare betikleri ------------------------------------------------------------------------------

GOTO = re.compile(r"^(?:this\.)?goto(AndPlay|AndStop)\((\"[^\"]*\"|\d+)\);?$")
EVENT = re.compile(r"^this\._parent\.(\w+)\(\);?$")


def parse_actions(source):
    """Kare betiğinden oynatıcının anlayacağı komutlar: stop, play, goto (kare ya da etiket, oynat/dur),
    event (üst sprite'a bildirilen an, ör. vuruş). Yalnızca en dış düzeydeki satırlar okunur: bir
    koşulun ya da işlevin içindeki komut her karede çalışmaz. Öbür satırlar oyunun kendi mantığıdır."""
    out = []
    depth = 0
    for line in source.splitlines():
        s = line.strip()
        if depth == 0:
            if s in ("stop();", "this.stop();"):
                out.append({"stop": True})
            elif s in ("play();", "this.play();"):
                out.append({"play": True})
            elif m := GOTO.match(s):
                target = m.group(2)
                target = target.strip('"') if target.startswith('"') else int(target)
                out.append({"goto": target, "play": m.group(1) == "AndPlay"})
            elif m := EVENT.match(s):
                out.append({"event": m.group(1)})
        depth += s.count("{") - s.count("}")
    return out


def script_dir_id(name):
    """FFDec betik klasörünün adından karakter kimliği: DefineSprite_547 ya da DefineSprite_547_Human."""
    m = re.match(r"DefineSprite_(\d+)", name)
    return int(m.group(1)) if m else None


def read_frame_actions(folder):
    """{kare sırası (0'dan): [komut]} — FFDec'in frame_<n>/DoAction*.as dosyalarından."""
    out = {}
    if not os.path.isdir(folder):
        return out
    for entry in sorted(os.listdir(folder)):
        m = re.match(r"frame_(\d+)$", entry)
        if not m:
            continue
        cmds = []
        for f in sorted(os.listdir(os.path.join(folder, entry))):
            if f.startswith("DoAction") and f.endswith(".as"):
                with open(os.path.join(folder, entry, f), encoding="utf-8") as fh:
                    cmds += parse_actions(fh.read())
        if cmds:
            out[int(m.group(1)) - 1] = cmds
    return out


def scripts_by_sprite(scripts):
    out = {}
    if not os.path.isdir(scripts):
        return out
    for name in os.listdir(scripts):
        cid = script_dir_id(name)
        if cid is not None:
            out[cid] = read_frame_actions(os.path.join(scripts, name))
    return out


# --- Şekiller ------------------------------------------------------------------------------------

FFDEC_ATTR = re.compile(r'\s+(?:xmlns:)?ffdec(?::[\w-]+)?="[^"]*"')
TRANSLATE = re.compile(r'<g transform="matrix\(1\.0, 0\.0, 0\.0, 1\.0, (-?[\d.]+), (-?[\d.]+)\)">')


def convert_shape(svg):
    """FFDec şekil SVG'si → (motorun okuyacağı SVG, şeklin kendi koordinatlarında sol üst köşesi).

    FFDec şekli `translate(-xmin, -ymin)` ile kaydırır; oynatıcı şekli kendi koordinatlarında
    çizebilmek için bu köşeyi bilir. Bit eşlem dolgulu şekiller (<image>) için None döner."""
    if "<image" in svg or "<pattern" in svg:
        return None
    m = TRANSLATE.search(svg)
    origin = (-float(m.group(1)), -float(m.group(2))) if m else (0.0, 0.0)
    out = FFDEC_ATTR.sub("", svg)
    out = re.sub(r"<\?xml[^>]*\?>\s*", "", out)
    out = re.sub(r">\s+<", "><", out).strip() + "\n"
    return out, origin


# --- Aktarım -----------------------------------------------------------------------------------

def timeline_json(t, actions=None):
    out = {"frames": [[clean_op(op) for op in ops] for ops in t.frames]}
    if t.labels:
        out["labels"] = dict(sorted(t.labels.items(), key=lambda x: (x[1], x[0])))
    if actions:
        out["actions"] = {str(k): v for k, v in sorted(actions.items())}
    if t.sounds:
        out["sounds"] = {str(k): v for k, v in sorted(t.sounds.items())}
    return out


# --- Morph şekiller ------------------------------------------------------------------------------

def apply_animates(svg, which):
    """FFDec morph SVG'sinde her öznitelik <animate values="başlangıç;bitiş"> ile verilir. `which`
    (0 başlangıç, 1 bitiş) değeri öğenin özniteliğine yazılır, <animate>'ler silinir. İki ucun yol
    yapısı aynıdır; oynatıcı aradaki hâli oranla hesaplar."""
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    ET.register_namespace("ffdec", "https://www.free-decompiler.com/flash")
    root = ET.fromstring(re.sub(r"<\?xml[^>]*\?>", "", svg).strip())
    ns = "{http://www.w3.org/2000/svg}"
    for parent in list(root.iter()):
        for anim in [c for c in parent if c.tag == ns + "animate"]:
            values = anim.get("values", "").split(";")
            parent.set(anim.get("attributeName"), values[which] if which < len(values) else values[-1])
            parent.remove(anim)
        transforms = [c for c in parent if c.tag == ns + "animateTransform"]
        if transforms:
            # Sırayla uygulanır: "replace" baştan başlatır, "sum" öncekinin ardına ekler
            m = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
            for anim in transforms:
                t = transform_matrix(anim.get("type"), anim.get("from" if which == 0 else "to"))
                m = t if anim.get("additive") == "replace" else multiply(m, t)
                parent.remove(anim)
            parent.set(transforms[0].get("attributeName"),
                       "matrix(" + ", ".join(f"{round(v, 6):g}" for v in m) + ")")
    return ET.tostring(root, encoding="unicode")


def multiply(m1, m2):
    """m1 · m2 (önce m2 uygulanır)."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
            a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1)


def transform_matrix(kind, value):
    """SVG animateTransform türü ve değeri → matris."""
    v = [float(x) for x in re.split(r"[\s,]+", (value or "").strip()) if x]
    if kind == "translate":
        return (1.0, 0.0, 0.0, 1.0, v[0], v[1] if len(v) > 1 else 0.0)
    if kind == "scale":
        return (v[0], 0.0, 0.0, v[1] if len(v) > 1 else v[0], 0.0, 0.0)
    if kind == "rotate":
        a = math.radians(v[0])
        r = (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0.0, 0.0)
        if len(v) == 3:
            return multiply(multiply((1.0, 0.0, 0.0, 1.0, v[1], v[2]), r), (1.0, 0.0, 0.0, 1.0, -v[1], -v[2]))
        return r
    if kind == "skewX":
        return (1.0, 0.0, math.tan(math.radians(v[0])), 1.0, 0.0, 0.0)
    if kind == "skewY":
        return (1.0, math.tan(math.radians(v[0])), 0.0, 1.0, 0.0, 0.0)
    raise ValueError(f"bilinmeyen dönüşüm türü: {kind}")


def clean_svg(svg):
    out = FFDEC_ATTR.sub("", svg)
    out = re.sub(r"<\?xml[^>]*\?>\s*", "", out)
    out = re.sub(r">\s+<", "><", out).strip() + "\n"
    # ElementTree'nin yazdığı ad alanı öneki (ns0:) varsa düz SVG'ye çevrilir
    return out.replace("ns0:", "").replace(":ns0", "")


def svg_origin(svg):
    m = TRANSLATE.search(svg)
    return (-float(m.group(1)), -float(m.group(2))) if m else (0.0, 0.0)


# --- Aktarım -----------------------------------------------------------------------------------

TAG_NAMES = {0: "End", 1: "ShowFrame", 2: "DefineShape", 4: "PlaceObject", 5: "RemoveObject", 6: "DefineBits",
             8: "JPEGTables", 9: "SetBackgroundColor", 10: "DefineFont", 11: "DefineText", 12: "DoAction",
             13: "DefineFontInfo", 14: "DefineSound", 15: "StartSound", 17: "DefineButtonSound",
             18: "SoundStreamHead", 19: "SoundStreamBlock", 20: "DefineBitsLossless", 21: "DefineBitsJPEG2",
             22: "DefineShape2", 24: "Protect", 26: "PlaceObject2", 28: "RemoveObject2", 32: "DefineShape3",
             33: "DefineText2", 34: "DefineButton2", 35: "DefineBitsJPEG3", 36: "DefineBitsLossless2",
             37: "DefineEditText", 39: "DefineSprite", 41: "ProductInfo", 43: "FrameLabel", 45: "SoundStreamHead2",
             46: "DefineMorphShape", 48: "DefineFont2", 56: "ExportAssets", 58: "EnableDebugger", 59: "DoInitAction",
             62: "DefineFontInfo2", 64: "EnableDebugger2", 65: "ScriptLimits", 69: "FileAttributes",
             70: "PlaceObject3", 73: "DefineFontAlignZones", 74: "CSMTextSettings", 75: "DefineFont3",
             77: "Metadata", 83: "DefineShape4", 84: "DefineMorphShape2"}
# Her etiket türünün nereye gittiği
DISPOSITION = {
    "End": "dosya sonu işareti; içerik taşımaz",
    "ShowFrame": "kare sınırı → library.json zaman çizelgeleri",
    "DefineShape": "shapes/<id>.svg (resim dolgulular shapes-bitmap/<id>.svg)",
    "DefineShape2": "shapes/<id>.svg (resim dolgulular shapes-bitmap/<id>.svg)",
    "DefineShape3": "shapes/<id>.svg (resim dolgulular shapes-bitmap/<id>.svg)",
    "DefineShape4": "shapes/<id>.svg (resim dolgulular shapes-bitmap/<id>.svg)",
    "DefineMorphShape": "morphs/<id>.svg, <id>.start.svg, <id>.end.svg",
    "DefineMorphShape2": "morphs/<id>.svg, <id>.start.svg, <id>.end.svg",
    "DefineBits": "images/<id>.jpg",
    "DefineBitsJPEG2": "images/<id>.jpg",
    "DefineBitsJPEG3": "images/<id>.png (saydamlıklı)",
    "DefineBitsLossless": "images/<id>.png",
    "DefineBitsLossless2": "images/<id>.png",
    "JPEGTables": "JPEG tabloları; images/ içindeki resimlere katıldı",
    "DefineSound": "sounds/<id>.mp3",
    "StartSound": "library.json → zaman çizelgesi 'sounds'",
    "SoundStreamHead": "boş ses akışı başlığı (akış verisi yok)",
    "SoundStreamHead2": "boş ses akışı başlığı (akış verisi yok)",
    "DefineText": "texts.json → texts (yerleşim + çözülmüş yazı)",
    "DefineText2": "texts.json → texts (yerleşim + çözülmüş yazı)",
    "DefineEditText": "texts.json → edit_texts (bütün özellikler)",
    "CSMTextSettings": "texts.json → csm (kenar yumuşatma ayarı)",
    "DefineFont": "yazı tipi: yalnız yerel arşivde (lisans yazı tipi yapımcısında); kodları texts.json → fonts",
    "DefineFont2": "yazı tipi: yalnız yerel arşivde (lisans yazı tipi yapımcısında); kodları texts.json → fonts",
    "DefineFont3": "yazı tipi: yalnız yerel arşivde (lisans yazı tipi yapımcısında); kodları texts.json → fonts",
    "DefineFontAlignZones": "yazı tipi hizalama ipucu: yalnız yerel arşivde (yazı tipiyle birlikte)",
    "DefineButton2": "library.json → buttons (eylemleri kaynak/feudalism/<oyun>/kod/)",
    "DefineSprite": "library.json → sprites",
    "PlaceObject2": "library.json → zaman çizelgeleri (klip eylemleri kaynak/.../kod/)",
    "PlaceObject3": "library.json → zaman çizelgeleri (süzgeç, karışım dahil)",
    "RemoveObject2": "library.json → zaman çizelgeleri",
    "FrameLabel": "library.json → zaman çizelgeleri 'labels'",
    "DoAction": "kaynak/feudalism/<oyun>/kod/ (basit komutlar library.json 'actions')",
    "DoInitAction": "kaynak/feudalism/<oyun>/kod/ (sınıf kodu)",
    "ExportAssets": "library.json → exports",
    "SetBackgroundColor": "library.json → stage.background",
    "FileAttributes": "dosya bilgisi (manifest.json → file_info)",
}


def third_party(game, movie):
    """Oyunun yazarına ait olmayan karakterler: sponsor ve Macromedia bileşen ağaçları (oyunun kendi
    sembollerince de kullanılanlar hariç). Kimlik → neden."""
    game_roots = (movie.root.characters() - set(EXCLUDED[game])) | {
        c for n, c in movie.exports.items() if not is_component_export(n) and c not in EXCLUDED[game]}
    used_by_game = movie.reachable(game_roots)
    out = {}
    for cid in movie.reachable(set(EXCLUDED[game])) - used_by_game:
        out[cid] = "sponsor: " + EXCLUDED[game][min(EXCLUDED[game])]
    comp = {c for n, c in movie.exports.items() if is_component_export(n) and not n.startswith("__Packages.")}
    for cid in movie.reachable(comp) - used_by_game:
        out[cid] = "Macromedia/Adobe arayüz bileşeni (oyunda kullanılmıyor)"
    return out


def reset_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def find_file(folder, cid, exts):
    """FFDec çıktısında karakterin dosyası: <id>.<uzantı> ya da <id>_<ad>.<uzantı>."""
    for name in sorted(os.listdir(folder)):
        stem, ext = os.path.splitext(name)
        if ext.lower() in exts and (stem == str(cid) or stem.startswith(f"{cid}_")):
            return os.path.join(folder, name)
    return None


def build(game, swf_path, archive, out_dir, code_dir):
    """Bir oyunu aktarır. `archive`: FFDec'in tam dökümü (referans/<oyun>/tam). Dönen: manifest."""
    movie = swf.Movie(swf_path)
    tp = third_party(game, movie)
    exports = {n: c for n, c in movie.exports.items() if not is_component_export(n) and c not in tp}

    def keep(kind):
        return sorted(c for c in movie.reachable(set(movie.sprites) | movie.shapes | movie.morphs | set(movie.buttons))
                      | movie.bitmaps | movie.sounds | movie.texts | movie.edit_texts
                      if movie.kind(c) == kind and c not in tp)

    where = {}
    for sub in ("shapes", "shapes-bitmap", "morphs", "images", "sounds"):
        reset_dir(os.path.join(out_dir, sub))
    # Şekiller
    shapes, bitmap_shapes = {}, {}
    for sid in keep("shape"):
        with open(os.path.join(archive, "shapes", f"{sid}.svg"), encoding="utf-8") as f:
            raw = f.read()
        converted = convert_shape(raw)
        if converted is None:
            text, origin, sub = clean_svg(raw), svg_origin(raw), "shapes-bitmap"
            bitmap_shapes[str(sid)] = round_list(origin, 3)
        else:
            (text, origin), sub = converted, "shapes"
            shapes[str(sid)] = round_list(origin, 3)
        with open(os.path.join(out_dir, sub, f"{sid}.svg"), "w", encoding="utf-8") as f:
            f.write(text)
        where[sid] = f"{sub}/{sid}.svg"
    # Morph şekiller: özgün (canlandırmalı) ve başlangıç / bitiş
    morphs = {}
    for mid in keep("morph"):
        with open(os.path.join(archive, "morphshapes", f"{mid}.svg"), encoding="utf-8") as f:
            raw = f.read()
        start, end = apply_animates(raw, 0), apply_animates(raw, 1)
        for suffix, text in (("", raw), (".start", start), (".end", end)):
            with open(os.path.join(out_dir, "morphs", f"{mid}{suffix}.svg"), "w", encoding="utf-8") as f:
                f.write(clean_svg(text))
        morphs[str(mid)] = round_list(svg_origin(raw), 3)
        where[mid] = f"morphs/{mid}.svg"
    # Resimler
    images = {}
    for bid in sorted(movie.bitmaps):
        src = find_file(os.path.join(archive, "images"), bid, {".jpg", ".png", ".gif"})
        if src is None:
            raise FileNotFoundError(f"{game}: resim {bid} FFDec dökümünde yok")
        name = f"{bid}{os.path.splitext(src)[1].lower()}"
        shutil.copyfile(src, os.path.join(out_dir, "images", name))
        images[str(bid)] = f"images/{name}"
        where[bid] = images[str(bid)]
    # Sesler
    sounds = {}
    for sid in sorted(movie.sounds):
        src = find_file(os.path.join(archive, "sounds"), sid, {".mp3", ".wav"})
        if src is None:
            raise FileNotFoundError(f"{game}: ses {sid} FFDec dökümünde yok")
        name = f"{sid}{os.path.splitext(src)[1].lower()}"
        shutil.copyfile(src, os.path.join(out_dir, "sounds", name))
        export = next((n for n, c in movie.exports.items() if c == sid), None)
        sounds[str(sid)] = {"file": f"sounds/{name}", **({"export": export} if export else {}),
                            **{k: v for k, v in swf.read_sound(sound_body(movie, sid)).items() if k != "id"}}
        where[sid] = sounds[str(sid)]["file"]
    # Yazılar ve yazı alanları
    fonts = {}
    for fid, (code, body) in sorted(movie.font_bodies.items()):
        _, name, bold, italic, codes = swf.read_font(body)
        fonts[str(fid)] = {"name": name, "bold": bold, "italic": italic, "codes": codes}
        where[fid] = "yalnız yerel arşiv (yazı tipi lisansı); kodlar texts.json"
    font_codes = {int(k): v["codes"] for k, v in fonts.items()}
    texts = {}
    for tid in keep("text"):
        code, body = movie.text_bodies[tid]
        full = swf.read_text_full(body, code == 33)
        full["text"] = decode_records(full["records"], font_codes)
        texts[str(tid)] = full
        where[tid] = "texts.json"
    edit_texts = {str(eid): swf.read_edit_text_full(movie.edit_text_bodies[eid]) for eid in keep("edit_text")}
    for eid in edit_texts:
        where[int(eid)] = "texts.json"
    with open(os.path.join(out_dir, "texts.json"), "w", encoding="utf-8") as f:
        json.dump({"description": "Feudalism yazıları; araclar/aktar/aktar.py üretir, elle değiştirmeyin.",
                   "fonts": fonts, "texts": texts, "edit_texts": edit_texts,
                   "csm": {str(k): v for k, v in sorted(movie.csm.items())}}, f, ensure_ascii=False,
                  separators=(",", ":"))
        f.write("\n")
    # Zaman çizelgeleri, düğmeler
    actions = scripts_by_sprite(os.path.join(archive, "scripts"))
    root_actions = read_frame_actions(os.path.join(archive, "scripts"))
    sprites = {str(cid): timeline_json(movie.sprites[cid], actions.get(cid)) for cid in keep("sprite")}
    for cid in sprites:
        where[int(cid)] = "library.json"
    buttons = {}
    for bid in keep("button"):
        recs = []
        for r in movie.buttons[bid]:
            rec = {"states": [s for s, on in zip(("up", "over", "down", "hit"), r["states"]) if on],
                   "char": r["char"], "depth": r["depth"]}
            rec.update(clean_op({k: r[k] for k in ("matrix", "cxform", "filters", "blend") if k in r}))
            recs.append(rec)
        buttons[str(bid)] = recs
        where[bid] = "library.json"
    library = {
        "description": "Feudalism görselleri; araclar/aktar/aktar.py üretir, elle değiştirmeyin.",
        "source": {"file": os.path.basename(swf_path), "sha256": swf.sha256(swf_path)},
        "stage": {"width": movie.width, "height": movie.height, "fps": movie.rate, "background": movie.background},
        "exports": dict(sorted(exports.items())),
        "shapes": shapes,
        "bitmap_shapes": bitmap_shapes,
        "morphs": morphs,
        "images": images,
        "sounds": sounds,
        "sprites": sprites,
        "buttons": buttons,
        "root": timeline_json(movie.root, root_actions),
        "excluded": {str(k): v for k, v in sorted(tp.items())},
    }
    with open(os.path.join(out_dir, "library.json"), "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    # Oyunun kodu (görsel değil; oyunun kurallarını yazarken başvuru)
    reset_dir(code_dir)
    shutil.copytree(os.path.join(archive, "scripts"), os.path.join(code_dir, "kod"))
    # Manifest: her karakterin ve her etiket türünün nereye gittiği
    for cid, reason in tp.items():
        where[cid] = "yalnız yerel arşiv: " + reason
    all_chars = (set(movie.sprites) | movie.shapes | movie.morphs | movie.bitmaps | movie.sounds | movie.texts
                 | movie.edit_texts | movie.fonts | set(movie.buttons))
    missing = sorted(c for c in all_chars if c not in where)
    manifest = {
        "description": "Ayıklama listesi: SWF'deki her etiket türünün ve her karakterin nereye gittiği. "
                       "araclar/aktar/aktar.py üretir.",
        "source": library["source"],
        "tags": {"top_level": named_counts(movie.tag_counts), "inside_sprites": named_counts(movie.sprite_tag_counts)},
        "dispositions": {n: DISPOSITION.get(n, "TANINMAYAN ETİKET") for n in
                         sorted(set(named_counts(movie.tag_counts)) | set(named_counts(movie.sprite_tag_counts)))},
        "characters": {str(c): {"type": movie.kind(c), "where": where.get(c, "EKSİK")} for c in sorted(all_chars)},
        "missing": missing,
        "file_info": file_info(movie),
    }
    with open(os.path.join(code_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return library, manifest


def sound_body(movie, sid):
    return movie.sound_bodies[sid]


def decode_records(records, font_codes):
    """Kayıtlar → satırlar; y'si verilen kayıt yeni satır başlatır, yazı tipi verilmeyen kayıt öncekini
    sürdürür."""
    lines = []
    font = None
    for rec in records:
        font = rec.get("font", font)
        codes = font_codes.get(font, [])
        piece = "".join(chr(codes[g]) if g < len(codes) else "?" for g, _ in rec["glyphs"])
        if "y" in rec or not lines:
            lines.append(piece)
        else:
            lines[-1] += piece
    return "\n".join(lines)


def named_counts(counts):
    return {TAG_NAMES.get(k, f"etiket {k}"): v for k, v in sorted(counts.items(), key=lambda x: TAG_NAMES.get(x[0], str(x[0])))}


def file_info(movie):
    info = {"swf_version": movie.version}
    for code, body in movie.other:
        if code == 69:
            fl = body[0]
            info["file_attributes"] = {"use_network": bool(fl & 1), "actionscript3": bool(fl & 8),
                                       "has_metadata": bool(fl & 16), "use_gpu": bool(fl & 32),
                                       "use_direct_blit": bool(fl & 64)}
        elif code == 8:
            info["jpeg_tables_bytes"] = len(body)
        else:
            info[TAG_NAMES.get(code, str(code))] = body.hex()[:200]
    return info


def main(argv):
    swf_root = argv[0] if argv else os.environ.get("SWF_KOK", os.path.join(ROOT, "..", "swf-oyunlar"))
    for game, rel in GAMES.items():
        out_dir = os.path.join(ROOT, "content", "feudalism", game)
        code_dir = os.path.join(ROOT, "kaynak", "feudalism", game)
        os.makedirs(out_dir, exist_ok=True)
        lib, man = build(game, os.path.join(swf_root, rel), os.path.join(ROOT, "referans", game, "tam"), out_dir,
                         code_dir)
        print(f"{game}: şekil {len(lib['shapes'])} + resim dolgulu {len(lib['bitmap_shapes'])}, morph {len(lib['morphs'])}, "
              f"resim {len(lib['images'])}, ses {len(lib['sounds'])}, sprite {len(lib['sprites'])}, "
              f"düğme {len(lib['buttons'])}, kök kare {len(lib['root']['frames'])}; yerel arşivde kalan "
              f"{len(lib['excluded'])}; eksik {len(man['missing'])}; tanınmayan etiket "
              f"{sum(1 for v in man['dispositions'].values() if v == 'TANINMAYAN ETİKET')}")


if __name__ == "__main__":
    main(sys.argv[1:])
