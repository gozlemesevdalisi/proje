"""Örnek arayüz penceresi: demirci dükkânı. Yazılar motorda çizilir."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f, smooth_path, blob  # noqa: E402
from charkit import Defs, ink, lit, shade, path, line  # noqa: E402

OUT = sys.argv[1]
W, H = 800, 560
PARCH = "#F1E3C2"
EDGE = "#CDB284"
DARK = "#8C6B3F"
GOLD = "#E8B22C"
RED = "#A3241A"
NAVY = "#23406E"

d = Defs("u")
rng = random.Random(5)
b = []

# ------------------------------------------------------------ parşömen yaprak
top = [(52, 70), (200, 64), (400, 72), (600, 63), (748, 70)]
right = [(748, 70), (756, 200), (746, 330), (754, 500)]
bottom = [(754, 500), (600, 508), (400, 498), (200, 509), (46, 502)]
left = [(46, 502), (54, 360), (44, 220), (52, 70)]
sheet = smooth_path(top)
for seg in (right, bottom, left):
    sheet += " " + smooth_path(seg)[smooth_path(seg).index("C"):]
sheet += " Z"
b.append(path(sheet, d.rad(380, 270, 470, [(0, "#FAF1DA"), (0.45, PARCH), (0.82, "#DCC497"), (1, EDGE)]), DARK, 2.5))
# Lekeler (eski kâğıt)
for _ in range(7):
    b.append(path(blob(rng.uniform(110, 690), rng.uniform(120, 460), rng.uniform(30, 70), rng.uniform(16, 34), 9, rng, 0.25),
                  "#B89A68", extra=' opacity="0.08"'))
# Kıvrık köşeler: sol üst ve sağ alt
b.append(path("M52 70 C70 66 92 70 104 78 C88 86 70 98 60 116 C52 104 48 86 52 70 Z",
              d.volume(EDGE, 52, 66, 104, 116, 0.35, 0.2), DARK, 2.5))
b.append(path("M60 116 C70 98 88 86 104 78 C98 92 92 104 88 116 Z", shade(EDGE, 0.25), DARK, 2))
b.append(path("M754 500 C736 504 712 502 700 494 C716 486 734 472 744 454 C752 466 756 484 754 500 Z",
              d.volume(EDGE, 700, 454, 756, 504, 0.1, 0.35), DARK, 2.5))

# ------------------------------------------------------------ altın çerçeve ve köşe süsleri
frame = "M84 104 L716 104 Q724 104 724 112 L724 456 Q724 464 716 464 L84 464 Q76 464 76 456 L76 112 Q76 104 84 104 Z"
b.append(path(frame, "none", d.lin(76, 104, 724, 464, [(0, "#FFE38A"), (0.5, GOLD), (1, "#A6781C")]), 4))
b.append(path("M90 116 L710 116 L710 452 L90 452 Z", "none", "#A6781C", 1.4, ' opacity="0.7"'))
for (x, y, sx, sy) in [(76, 104, 1, 1), (724, 104, -1, 1), (76, 464, 1, -1), (724, 464, -1, -1)]:
    orn = (f"M{x} {y} L{x + 26 * sx} {y} C{x + 34 * sx} {y} {x + 38 * sx} {y + 8 * sy} {x + 32 * sx} {y + 12 * sy} "
           f"C{x + 26 * sx} {y + 16 * sy} {x + 18 * sx} {y + 10 * sy} {x + 22 * sx} {y + 6 * sy} "
           f"M{x} {y} L{x} {y + 26 * sy} C{x} {y + 34 * sy} {x + 8 * sx} {y + 38 * sy} {x + 12 * sx} {y + 32 * sy} "
           f"C{x + 16 * sx} {y + 26 * sy} {x + 10 * sx} {y + 18 * sy} {x + 6 * sx} {y + 22 * sy}")
    b.append(line(orn, GOLD, 3.2))
    b.append(path(f"M{x} {y - 8 * sy} L{x + 8 * sx} {y} L{x} {y + 8 * sy} L{x - 8 * sx} {y} Z",
                  d.volume(GOLD, x - 8, y - 8, x + 8, y + 8, 0.4, 0.3), ink(GOLD), 2))

# ------------------------------------------------------------ kurdele başlık
rib_l, rib_r, ry0, ry1 = 190, 610, 22, 82
b.append(path(f"M{rib_l - 70} {ry0 + 18} L{rib_l + 10} {ry0 + 18} L{rib_l + 10} {ry1 + 16} L{rib_l - 70} {ry1 + 16} "
              f"L{rib_l - 48} {(ry0 + ry1) / 2 + 17} Z", d.volume(shade(RED, 0.2), rib_l - 70, ry0, rib_l + 10, ry1 + 16), ink(RED)))
b.append(path(f"M{rib_r - 10} {ry0 + 18} L{rib_r + 70} {ry0 + 18} L{rib_r + 48} {(ry0 + ry1) / 2 + 17} L{rib_r + 70} {ry1 + 16} "
              f"L{rib_r - 10} {ry1 + 16} Z", d.volume(shade(RED, 0.2), rib_r - 10, ry0, rib_r + 70, ry1 + 16), ink(RED)))
b.append(path(f"M{rib_l} {ry1} L{rib_l + 12} {ry1 + 16} L{rib_l + 12} {ry1} Z", shade(RED, 0.5)))
b.append(path(f"M{rib_r} {ry1} L{rib_r - 12} {ry1 + 16} L{rib_r - 12} {ry1} Z", shade(RED, 0.5)))
b.append(path(f"M{rib_l} {ry0} Q400 {ry0 - 10} {rib_r} {ry0} L{rib_r} {ry1} Q400 {ry1 - 10} {rib_l} {ry1} Z",
              d.lin(0, ry0 - 6, 0, ry1, [(0, lit(RED, 0.3)), (0.4, RED), (1, shade(RED, 0.3))]), ink(RED)))
b.append(line(f"M{rib_l + 8} {ry0 + 7} Q400 {ry0 - 3} {rib_r - 8} {ry0 + 7}", GOLD, 2.5, 0.9))
b.append(line(f"M{rib_l + 8} {ry1 - 7} Q400 {ry1 - 17} {rib_r - 8} {ry1 - 7}", GOLD, 2.5, 0.9))

# ------------------------------------------------------------ eşya yuvaları ve simgeler
SLOT = 96
slots = [(110 + c * 108, 140 + r * 108) for r in range(2) for c in range(3)]


def potion(cx, cy):
    g = d.rad(cx - 8, cy + 2, 30, [(0, "#E8574A"), (0.6, "#B3261C"), (1, "#6E140F")])
    return [
        path(f"M{cx - 7} {cy - 30} L{cx + 7} {cy - 30} L{cx + 7} {cy - 14} C{cx + 24} {cy - 10} {cx + 28} {cy + 6} {cx + 26} {cy + 16} "
             f"C{cx + 22} {cy + 32} {cx - 22} {cy + 32} {cx - 26} {cy + 16} C{cx - 28} {cy + 6} {cx - 24} {cy - 10} {cx - 7} {cy - 14} Z",
             "#D9E7EE", "#4A5A66", 2.5, ' opacity="0.95"'),
        path(f"M{cx - 24} {cy + 4} C{cx - 12} {cy} {cx + 12} {cy + 8} {cx + 24} {cy + 4} C{cx + 26} {cy + 12} {cx + 24} {cy + 22} "
             f"{cx + 16} {cy + 26} C{cx + 6} {cy + 30} {cx - 6} {cy + 30} {cx - 16} {cy + 26} C{cx - 24} {cy + 22} {cx - 26} {cy + 12} {cx - 24} {cy + 4} Z", g),
        path(f"M{cx - 16} {cy - 4} C{cx - 14} {cy - 10} {cx - 8} {cy - 12} {cx - 4} {cy - 11} C{cx - 10} {cy - 6} {cx - 13} {cy + 2} {cx - 13} {cy + 8} Z",
             "#FFFFFF", extra=' opacity="0.7"'),
        path(f"M{cx - 9} {cy - 38} L{cx + 9} {cy - 38} L{cx + 8} {cy - 28} L{cx - 8} {cy - 28} Z",
             d.volume("#9C6A3C", cx - 9, cy - 38, cx + 9, cy - 28), ink("#9C6A3C"), 2),
        line(f"M{cx - 8} {cy - 20} Q{cx} {cy - 16} {cx + 8} {cy - 20} L{cx + 12} {cy - 8}", "#C9962E", 2),
    ]


def scroll(cx, cy):
    return [
        path(f"M{cx - 26} {cy - 20} L{cx + 22} {cy - 26} L{cx + 26} {cy + 18} L{cx - 22} {cy + 24} Z",
             d.volume(PARCH, cx - 26, cy - 26, cx + 26, cy + 24, 0.3, 0.25), DARK, 2.5),
        path(f"M{cx - 30} {cy - 24} C{cx - 36} {cy - 18} {cx - 32} {cy - 10} {cx - 24} {cy - 12} L{cx + 24} {cy - 18} "
             f"C{cx + 30} {cy - 20} {cx + 30} {cy - 30} {cx + 22} {cy - 30} Z", d.volume(EDGE, cx - 34, cy - 30, cx + 30, cy - 10), DARK, 2.5),
        path(f"M{cx - 26} {cy + 20} C{cx - 32} {cy + 26} {cx - 28} {cy + 34} {cx - 20} {cy + 32} L{cx + 28} {cy + 26} "
             f"C{cx + 34} {cy + 24} {cx + 34} {cy + 14} {cx + 26} {cy + 14} Z", d.volume(EDGE, cx - 30, cy + 14, cx + 34, cy + 34), DARK, 2.5),
        line(f"M{cx - 16} {cy - 8} L{cx + 14} {cy - 12} M{cx - 15} {cy} L{cx + 15} {cy - 4} M{cx - 14} {cy + 8} L{cx + 8} {cy + 5}",
             "#6B5A44", 2, 0.7),
        path(f"M{cx - 4} {cy + 10} L{cx + 6} {cy + 9} L{cx + 10} {cy + 30} L{cx + 2} {cy + 24} L{cx - 4} {cy + 32} Z", RED, ink(RED), 2),
    ]


def sword(cx, cy):
    return [
        path(f"M{cx - 4} {cy + 8} L{cx + 24} {cy - 26} L{cx + 30} {cy - 32} L{cx + 28} {cy - 22} L{cx + 2} {cy + 12} Z",
             d.lin(cx, cy, cx + 6, cy + 6, [(0, "#F4F7FA"), (1, "#7E8892")]), "#4A5A66", 2.5),
        path(f"M{cx - 16} {cy + 2} L{cx + 2} {cy + 20} L{cx - 2} {cy + 24} L{cx - 20} {cy + 6} Z",
             d.volume(GOLD, cx - 20, cy, cx + 2, cy + 24), ink(GOLD), 2),
        path(f"M{cx - 8} {cy + 16} L{cx - 22} {cy + 30} L{cx - 18} {cy + 34} L{cx - 4} {cy + 20} Z", "#4A3019", ink("#4A3019"), 2),
        f'<circle cx="{cx - 23}" cy="{cy + 35}" r="5" fill="{GOLD}" stroke="{ink(GOLD)}" stroke-width="2"/>',
    ]


def shield_icon(cx, cy):
    s = (f"M{cx - 24} {cy - 26} L{cx + 24} {cy - 26} C{cx + 26} {cy} {cx + 18} {cy + 20} {cx} {cy + 32} "
         f"C{cx - 18} {cy + 20} {cx - 26} {cy} {cx - 24} {cy - 26} Z")
    return [
        path(s, d.volume(RED, cx - 24, cy - 26, cx + 24, cy + 32), ink(RED), 2.5),
        f'<circle cx="{cx}" cy="{cy - 2}" r="9" fill="{GOLD}" stroke="{ink(GOLD)}" stroke-width="2"/>',
        line(" ".join(f"M{f(cx + math.cos(a) * 12)} {f(cy - 2 + math.sin(a) * 12)} L{f(cx + math.cos(a) * 18)} {f(cy - 2 + math.sin(a) * 18)}"
                      for a in [k * math.tau / 8 for k in range(8)]), GOLD, 3),
        path(s, "none", GOLD, 2, ' opacity="0.9"'),
    ]


def bow(cx, cy):
    return [
        path(f"M{cx - 10} {cy - 34} C{cx + 24} {cy - 26} {cx + 24} {cy + 26} {cx - 10} {cy + 34} "
             f"C{cx + 14} {cy + 22} {cx + 14} {cy - 22} {cx - 10} {cy - 34} Z", d.volume("#9C6A3C", cx - 10, cy - 34, cx + 20, cy + 34), ink("#9C6A3C"), 2.5),
        line(f"M{cx - 10} {cy - 33} L{cx - 10} {cy + 33}", "#E6DCC3", 1.6),
        path(f"M{cx - 4} {cy - 6} C{cx} {cy - 8} {cx + 6} {cy - 8} {cx + 8} {cy - 4} L{cx + 8} {cy + 6} C{cx + 4} {cy + 8} {cx} {cy + 8} {cx - 4} {cy + 6} Z",
             "#5C3A1B"),
    ]


def pouch(cx, cy):
    return [
        path(f"M{cx - 10} {cy - 18} C{cx - 30} {cy - 8} {cx - 30} {cy + 26} {cx} {cy + 28} C{cx + 30} {cy + 26} {cx + 30} {cy - 8} {cx + 10} {cy - 18} Z",
             d.volume("#8B5A2B", cx - 28, cy - 18, cx + 28, cy + 28), ink("#8B5A2B"), 2.5),
        path(f"M{cx - 12} {cy - 26} L{cx + 12} {cy - 26} L{cx + 10} {cy - 16} L{cx - 10} {cy - 16} Z", shade("#8B5A2B", 0.2), ink("#8B5A2B"), 2),
        line(f"M{cx - 12} {cy - 17} Q{cx} {cy - 12} {cx + 12} {cy - 17}", "#C9962E", 2.5),
        f'<ellipse cx="{cx + 20}" cy="{cy + 26}" rx="11" ry="5" fill="{GOLD}" stroke="{ink(GOLD)}" stroke-width="2"/>',
        f'<ellipse cx="{cx + 28}" cy="{cy + 21}" rx="9" ry="4" fill="{lit(GOLD, 0.2)}" stroke="{ink(GOLD)}" stroke-width="2"/>',
    ]


icons = [potion, scroll, sword, shield_icon, bow, pouch]
for i, ((x, y), icon) in enumerate(zip(slots, icons)):
    if i == 0:  # seçili yuva: altın parıltı
        b.append(path(f"M{x - 10} {y - 10} L{x + SLOT + 10} {y - 10} L{x + SLOT + 10} {y + SLOT + 10} L{x - 10} {y + SLOT + 10} Z",
                      d.rad(x + SLOT / 2, y + SLOT / 2, 72, [(0.55, "#FFE38A", 0.9), (1, "#FFE38A", 0)])))
    b.append(path(f"M{x + 8} {y} L{x + SLOT - 8} {y} Q{x + SLOT} {y} {x + SLOT} {y + 8} L{x + SLOT} {y + SLOT - 8} "
                  f"Q{x + SLOT} {y + SLOT} {x + SLOT - 8} {y + SLOT} L{x + 8} {y + SLOT} Q{x} {y + SLOT} {x} {y + SLOT - 8} "
                  f"L{x} {y + 8} Q{x} {y} {x + 8} {y} Z",
                  d.lin(x, y, x + SLOT, y + SLOT, [(0, "#C9AE7C"), (0.25, "#E2CFA3"), (1, "#F2E5C6")]),
                  GOLD if i == 0 else DARK, 3 if i == 0 else 2))
    b += icon(x + SLOT / 2, y + SLOT / 2)

# Açıklama alanının ayracı
b.append(line("M440 214 C520 208 620 216 700 210", DARK, 2, 0.5))
b.append(path("M562 206 L570 212 L562 218 L554 212 Z", GOLD, ink(GOLD), 1.5))

# ------------------------------------------------------------ düğmeler
# Kalkan biçimli "Geri" düğmesi (ok simgesi)
sx, sy = 156, 396
sh = (f"M{sx - 44} {sy - 40} L{sx + 44} {sy - 40} C{sx + 48} {sy + 4} {sx + 30} {sy + 34} {sx} {sy + 52} "
      f"C{sx - 30} {sy + 34} {sx - 48} {sy + 4} {sx - 44} {sy - 40} Z")
b.append(path(sh, d.volume(NAVY, sx - 44, sy - 40, sx + 44, sy + 52, 0.25, 0.3), ink(NAVY), 3))
b.append(path(sh, "none", d.lin(sx - 44, sy - 40, sx + 44, sy + 52, [(0, "#FFE38A"), (1, "#A6781C")]), 3.5,
              ' transform="translate(0 0)"'))
b.append(path(f"M{sx + 22} {sy - 4} L{sx - 6} {sy - 4} L{sx - 6} {sy - 18} L{sx - 28} {sy + 2} L{sx - 6} {sy + 22} L{sx - 6} {sy + 8} "
              f"L{sx + 22} {sy + 8} Z", d.volume(GOLD, sx - 28, sy - 18, sx + 22, sy + 22, 0.35, 0.25), ink(GOLD), 2.5))
# Kırmızı mühür "Al" düğmesi: dalgalı kenarlı
mx, my = 628, 394
pts = []
for k in range(36):
    a = k * math.tau / 36
    rr = 44 + (4 if k % 2 == 0 else -1) + rng.uniform(-1.5, 1.5)
    pts.append((mx + math.cos(a) * rr, my + math.sin(a) * rr * 0.92))
b.append(path(smooth_path(pts, closed=True), d.rad(mx - 14, my - 16, 64, [(0, "#D2463A"), (0.55, RED), (1, "#5E0E0A")]), ink(RED, 0.5), 2.5))
b.append(path(f"M{mx - 38} {my} C{mx - 38} {my - 22} {mx - 20} {my - 36} {mx} {my - 36} C{mx + 22} {my - 36} {mx + 38} {my - 20} {mx + 38} {my} "
              f"C{mx + 38} {my + 22} {mx + 22} {my + 34} {mx} {my + 34} C{mx - 20} {my + 34} {mx - 38} {my + 22} {mx - 38} {my} Z",
              "none", "#6E140F", 2.5, ' opacity="0.8"'))
b.append(path(f"M{mx - 30} {my - 20} C{mx - 22} {my - 32} {mx - 4} {my - 38} {mx + 10} {my - 34} C{mx - 6} {my - 30} {mx - 20} {my - 22} {mx - 28} {my - 10} Z",
              "#FFFFFF", extra=' opacity="0.25"'))
# Mührün akan damlası
b.append(path(f"M{mx + 30} {my + 34} C{mx + 34} {my + 44} {mx + 32} {my + 56} {mx + 26} {my + 58} C{mx + 20} {my + 56} {mx + 20} {my + 46} {mx + 22} {my + 38} Z",
              d.volume(RED, mx + 20, my + 34, mx + 34, my + 58), ink(RED, 0.5), 2))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
       f'  <!-- Örnek arayüz penceresi: demirci dükkânı. 1 birim = 1 mantıksal piksel. Yazılar motorda çizilir. -->\n'
       f'  <defs>\n    ' + "\n    ".join(d.items) + "\n  </defs>\n  " + "\n  ".join(b) + "\n</svg>\n")
with open(OUT, "w") as fh:
    fh.write(svg)
