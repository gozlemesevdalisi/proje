"""Feudalism 1 ve 2'de ne var, ne yok: içerik dökümü (docs/FEUDALISM_ICERIK.md).

Her içerik türü için sayı, ayrıntı ve aktarım durumu: aktarıldı, bekliyor ya da aktarılmayacak (ve
nedeni). Yazılar ve sesler tek tek listelenir.

Kullanım (depo kökünden):  python3 araclar/aktar/envanter.py [swf-oyunlar klasörü]
"""
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aktar  # noqa: E402
import swf  # noqa: E402
from swfstats import tags  # noqa: E402

NAMES = {"f1": "Feudalism", "f2": "Feudalism 2"}
# Kök filmdeki ekran etiketlerinin Türkçesi
SCREENS = {"TOWN_SCREEN": "kamp / kasaba", "WORLD_MAP": "dünya haritası", "SPLASH_SCREEN": "savaşa hazırlık",
           "GAME_LOAD": "kayıt yükleme", "GAME_OVER": "oyun bitti", "VICTORY": "zafer", "STOLEN": "korsan kopya uyarısı",
           "BATTLE_TUT": "savaş öğreticisi", "TUTORIAL": "öğretici"}


class Details:
    """Bir SWF'nin döküm ayrıntıları: sesler, yazı tipleri, yazılar, alanlar, resimler."""

    def __init__(self, path):
        _, _, _, _, data, pos = swf.load(path)
        self.sounds, self.fonts, self.texts, self.edit_texts, self.images = [], {}, [], [], []
        font_codes = {}
        all_tags = list(tags(data, pos))
        for code, body in all_tags:
            if code in (48, 75):
                fid, name, bold, italic, codes = swf.read_font(body)
                font_codes[fid] = codes
                self.fonts[fid] = {"name": name, "bold": bold, "italic": italic, "glyphs": len(codes)}
        for code, body in all_tags:
            if code == 14:
                self.sounds.append(swf.read_sound(body))
            elif code in (11, 33):
                tid, lines = swf.read_text(body, code == 33)
                self.texts.append((tid, swf.decode_text(lines, font_codes)))
            elif code == 37:
                self.edit_texts.append(swf.read_edit_text(body))
            elif code in (6, 21, 35):
                bid = struct.unpack_from("<H", body, 0)[0]
                jpeg = body[6:6 + struct.unpack_from("<I", body, 2)[0]] if code == 35 else body[2:]
                self.images.append({"id": bid, "size": swf.jpeg_size(jpeg), "bytes": len(body)})
            elif code in (20, 36):
                bid = struct.unpack_from("<H", body, 0)[0]
                w, h = struct.unpack_from("<HH", body, 3)
                self.images.append({"id": bid, "size": (w, h), "bytes": len(body)})


def sprite_names(movie):
    """Sprite kimliği → okunur ad: dışa aktarılan ad ya da üst sprite'taki örnek adı."""
    names = {c: n for n, c in movie.exports.items()}
    for pid, t in movie.sprites.items():
        for ops in t.frames:
            for op in ops:
                if "char" in op and "name" in op and op["char"] not in names:
                    parent = names.get(pid, f"#{pid}")
                    names[op["char"]] = f"{parent}.{op['name']}"
    return names


def sound_uses(movie, names):
    """Ses kimliği → [kullanıldığı yer (sprite, kare etiketi)]."""
    out = {}
    for sid, t in sorted(movie.sprites.items()):
        for frame, ids in t.sounds.items():
            label = max(((lb, f) for lb, f in t.labels.items() if f <= frame), key=lambda x: x[1], default=(None, 0))[0]
            where = names.get(sid, f"#{sid}") + (f" / {label}" if label else "") + f" / kare {frame + 1}"
            for s in ids:
                out.setdefault(s, []).append(where)
    return out


def md_escape(text):
    return text.replace("|", "\\|").replace("\r", "").replace("\n", " / ").strip()


def strip_html(text):
    """Flash'ın HTML yazı alanlarından düz yazı: etiketler atılır, <sbr/> ve </p> satır sonu olur."""
    text = re.sub(r"<sbr\s*/?>|</p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.replace("&apos;", "'").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def game_section(game, path):
    movie = swf.Movie(path)
    det = Details(path)
    with open(os.path.join(aktar.ROOT, "content", "feudalism", game, "library.json"), encoding="utf-8") as f:
        lib = json.load(f)
    names = sprite_names(movie)
    pending = lib["not_yet_supported"]
    game_exports = sorted(n for n in movie.exports if not aktar.is_component_export(n))
    components = sorted(n for n in movie.exports if aktar.is_component_export(n) and not n.startswith("__Packages."))
    classes = sorted(n[len("__Packages."):] for n in movie.exports if n.startswith("__Packages.")
                     and not n.startswith("__Packages.mx."))
    s = [f"## {NAMES[game]} ({game})", "",
         f"Sahne {movie.width:.0f}×{movie.height:.0f} piksel, saniyede {movie.rate:.0f} kare, arka plan "
         f"`{movie.background}`. Kaynak: `{lib['source']['file']}`.", "",
         "| İçerik | Sayı | Durum |", "|---|---|---|",
         f"| Şekil (vektör çizim) | {len(movie.shapes)} | {len(lib['shapes'])} aktarıldı; "
         f"{len(pending['bitmap_filled_shapes'])} resim dolgulu şekil bekliyor |",
         f"| Sprite (hareketli sembol) | {len(movie.sprites)} | {len(lib['sprites'])} aktarıldı (zaman çizelgesiyle) |",
         f"| Düğme | {len(movie.buttons)} | {len(lib['buttons'])} aktarıldı |",
         f"| Ekran (kök film karesi) | {len(movie.root.frames)} | aktarıldı |",
         f"| Morph (biçim değiştiren şekil) | {len(movie.morphs)} | bekliyor |",
         f"| Resim (bit eşlem) | {len(det.images)} | bekliyor |",
         f"| Ses | {len(det.sounds)} | bekliyor |",
         f"| Müzik | 0 | oyunda müzik yok |",
         f"| Sabit yazı | {len(det.texts)} | bekliyor (Türkçeye çevrilip kendi yazı tiplerimizle çizilecek) |",
         f"| Yazı alanı (oyunun doldurduğu) | {len(det.edit_texts)} | bekliyor |",
         f"| Yazı tipi | {len(det.fonts)} | aktarılmayacak: lisansları yazı tipi yapımcılarında |",
         f"| Oyun kodu (ActionScript 2 sınıfı) | {len(classes)} | görsel değil; oyun mantığı kendi kodumuzla yazılır |",
         f"| Macromedia arayüz bileşeni | {len(components)} | aktarılmayacak: Adobe'nin; oyunda kullanılmıyor |",
         f"| Sponsor logosu | {len(lib['excluded'])} | aktarılmayacak: sponsorun |", ""]
    # Ekranlar
    s += ["### Ekranlar (kök film)", "", "| Kare | Ne |", "|---|---|"]
    labels = {f: lb for lb, f in movie.root.labels.items()}
    first_label = min(movie.root.labels.values()) if movie.root.labels else len(movie.root.frames)
    s.append(f"| 1–3 | açılış: yükleme, sponsor logoları{' (aktarılmadı)' if game == 'f1' else ''}, giriş animasyonu |")
    s.append(f"| 4 | ana menü |")
    s.append(f"| 5–{first_label} | savaş alanı arka planları ({first_label - 4} kare) |")
    for f in sorted(labels):
        s.append(f"| {f + 1} | {SCREENS.get(labels[f], labels[f])} (`{labels[f]}`) |")
    s.append("")
    # Semboller
    s += ["### Dışa aktarılan semboller (oyunun kodla çağırdığı)", "",
          ", ".join(f"`{n}`" for n in game_exports if not n.startswith("__Packages.")), ""]
    # Sesler
    uses = sound_uses(movie, names)
    s += ["### Sesler", "", "Hepsi kısa ses efekti; müzik yok.", "",
          "| Kimlik | Ad | Süre | Biçim | Nerede çalıyor |", "|---|---|---|---|---|"]
    for snd in det.sounds:
        name = next((n for n, c in movie.exports.items() if c == snd["id"]), "")
        where = "; ".join(uses.get(snd["id"], [])) or ("kodla çalınır" if name else "kullanılmıyor")
        s.append(f"| {snd['id']} | {name} | {snd['seconds']:.1f} sn | {snd['format']} {snd['rate']:.0f} Hz "
                 f"{'stereo' if snd['stereo'] else 'mono'} | {md_escape(where)} |")
    s.append("")
    # Resimler
    s += ["### Resimler", "", "| Kimlik | Boyut | Not |", "|---|---|---|"]
    for img in det.images:
        size = f"{img['size'][0]}×{img['size'][1]}" if img["size"] else "?"
        note = "savaş alanı zemin dokusu" if img["size"] == (800, 200) else ""
        s.append(f"| {img['id']} | {size} | {note} |")
    s.append("")
    # Yazı tipleri
    s += ["### Yazı tipleri (aktarılmayacak)", "", "| Kimlik | Ad | Biçem | Gömülü glif |", "|---|---|---|---|"]
    for fid, fo in sorted(det.fonts.items()):
        style = ", ".join(x for x, on in (("kalın", fo["bold"]), ("italik", fo["italic"])) if on) or "normal"
        s.append(f"| {fid} | {fo['name']} | {style} | {fo['glyphs'] or 'yok (sistem yazı tipi)'} |")
    s.append("")
    # Oyun kodu
    s += ["### Oyun kodunun sınıfları", "", ", ".join(f"`{c}`" for c in classes), ""]
    return s, det


def main(argv):
    swf_root = argv[0] if argv else os.environ.get("SWF_KOK", os.path.join(aktar.ROOT, "..", "swf-oyunlar"))
    out = ["# Feudalism 1 ve 2: içerik dökümü", "",
           "`python3 araclar/aktar/envanter.py` üretir; elle değiştirmeyin. Oyunların neyi var, neyi yok ve",
           "her birinin oyunumuza aktarılma durumu. Görseller hak sahibinin izniyle kullanılır",
           "(bkz. `docs/LISANSLAR.md`).", ""]
    texts = {}
    for game, rel in aktar.GAMES.items():
        section, det = game_section(game, os.path.join(swf_root, rel))
        out += section
        texts[game] = det
    out += ["## Ek: oyunlardaki sabit yazılar", "",
            "Ekranlarda çizili İngilizce yazılar (çeviri için). Yazı alanlarının başlangıç değerleri ayrıca listelenir.", ""]
    for game, det in texts.items():
        out += [f"### {NAMES[game]}", "", "| Kimlik | Yazı |", "|---|---|"]
        out += [f"| {tid} | {md_escape(t)} |" for tid, t in det.texts if t.strip()]
        out.append("")
        initial = [(e["id"], strip_html(e["text"])) for e in det.edit_texts if strip_html(e.get("text", "")).strip()]
        if initial:
            out += [f"Yazı alanlarının başlangıç değerleri ({NAMES[game]}): oyun bunların çoğunu çalışırken "
                    "değiştirir; burada tasarımdaki örnek değerleri var.", "", "| Kimlik | Yazı |", "|---|---|"]
            out += [f"| {tid} | {md_escape(t)} |" for tid, t in initial]
            out.append("")
    path = os.path.join(aktar.ROOT, "docs", "FEUDALISM_ICERIK.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")
    print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
