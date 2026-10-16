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
import os
import re
import sys

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


def build(game, swf_path, ref_dir, out_dir):
    movie = swf.Movie(swf_path)
    excluded = EXCLUDED[game]
    exports = {n: c for n, c in movie.exports.items() if not is_component_export(n) and c not in excluded}
    root_chars = movie.root.characters() - set(excluded)
    keep = movie.reachable(root_chars | set(exports.values())) - set(excluded)
    # Dışarıda bırakılanların yalnız onlarca kullanılan alt karakterleri de düşer
    shapes_dir = os.path.join(out_dir, "shapes")
    os.makedirs(shapes_dir, exist_ok=True)
    for old in os.listdir(shapes_dir):
        os.remove(os.path.join(shapes_dir, old))
    shapes = {}
    bitmap_shapes = []
    for sid in sorted(c for c in keep if movie.kind(c) == "shape"):
        with open(os.path.join(ref_dir, "svg", f"{sid}.svg"), encoding="utf-8") as f:
            converted = convert_shape(f.read())
        if converted is None:
            bitmap_shapes.append(sid)
            continue
        text, origin = converted
        with open(os.path.join(shapes_dir, f"{sid}.svg"), "w", encoding="utf-8") as f:
            f.write(text)
        shapes[str(sid)] = round_list(origin, 3)
    actions = scripts_by_sprite(os.path.join(ref_dir, "kod", "scripts"))
    root_actions = read_frame_actions(os.path.join(ref_dir, "kod", "scripts"))
    sprites = {str(cid): timeline_json(movie.sprites[cid], actions.get(cid))
               for cid in sorted(c for c in keep if movie.kind(c) == "sprite")}
    buttons = {}
    for bid in sorted(c for c in keep if movie.kind(c) == "button"):
        recs = []
        for r in movie.buttons[bid]:
            rec = {"states": [s for s, on in zip(("up", "over", "down", "hit"), r["states"]) if on],
                   "char": r["char"], "depth": r["depth"]}
            rec.update(clean_op({k: r[k] for k in ("matrix", "cxform", "filters", "blend") if k in r}))
            recs.append(rec)
        buttons[str(bid)] = recs

    def ids(kind):
        return sorted(c for c in keep if movie.kind(c) == kind)

    library = {
        "description": "Feudalism görselleri; araclar/aktar/aktar.py üretir, elle değiştirmeyin.",
        "source": {"file": os.path.basename(swf_path), "sha256": swf.sha256(swf_path)},
        "stage": {"width": movie.width, "height": movie.height, "fps": movie.rate, "background": movie.background},
        "exports": dict(sorted(exports.items())),
        "shapes": shapes,
        "sprites": sprites,
        "buttons": buttons,
        "root": timeline_json(movie.root, root_actions),
        "not_yet_supported": {
            # Resimler yerleştirilmez, şekillerin bit eşlem dolgusunda kullanılır: hepsi listelenir
            "bitmap_filled_shapes": bitmap_shapes, "morph_shapes": ids("morph"), "bitmaps": sorted(movie.bitmaps),
            "texts": ids("text"), "edit_texts": ids("edit_text"), "sounds": sorted(movie.sounds),
        },
        "excluded": {str(k): v for k, v in sorted(excluded.items())},
    }
    with open(os.path.join(out_dir, "library.json"), "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        f.write("\n")
    dropped = {c for c in set(movie.sprites) | movie.shapes | set(movie.buttons) if c not in keep}
    return library, dropped


def main(argv):
    swf_root = argv[0] if argv else os.environ.get("SWF_KOK", os.path.join(ROOT, "..", "swf-oyunlar"))
    for game, rel in GAMES.items():
        out_dir = os.path.join(ROOT, "content", "feudalism", game)
        os.makedirs(out_dir, exist_ok=True)
        lib, dropped = build(game, os.path.join(swf_root, rel), os.path.join(ROOT, "referans", game), out_dir)
        n = lib["not_yet_supported"]
        print(f"{game}: {len(lib['shapes'])} şekil, {len(lib['sprites'])} sprite, {len(lib['buttons'])} düğme, "
              f"{len(lib['root']['frames'])} kök kare; aktarılmayan karakter {len(dropped)}; "
              f"bekleyen: bit eşlem dolgulu {len(n['bitmap_filled_shapes'])}, morph {len(n['morph_shapes'])}, "
              f"resim {len(n['bitmaps'])}, yazı {len(n['texts'])}")


if __name__ == "__main__":
    main(sys.argv[1:])
