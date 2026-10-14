"""Örnek kahraman (sert kenarlı tarz): bozkır beyi. Dış hat yok; düz renk + sert gölge şekilleri."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f  # noqa: E402
from hardkit import Defs, P, Q, S, fill, taper, taper_shadow, group, dark, light, tone  # noqa: E402

OUT = sys.argv[1]

SKIN = "#F2BE8C"
HAIR = "#1C1410"
RED = "#B8141C"
GOLD = "#FFC21A"
NAVY = "#1F3F7A"
LEATHER = "#7A4A22"
BOOT = "#4E2E14"
STEEL = "#B9C3CC"
FUR = "#5E3E1E"
WHITE = "#F4EEE0"

d = Defs("h")
parts = []

# ------------------------------------------------------------ örgü (arkada)
braid = []
for i in range(6):
    cx, cy = 152 - i * 2.6, 108 + i * 12
    braid.append(fill(P([(cx - 6, cy - 6), (cx + 6, cy - 6), (cx + 7, cy + 3), (cx, cy + 8), (cx - 7, cy + 3)]), HAIR))
    braid.append(fill(P([(cx - 5, cy - 5), (cx + 1, cy - 5), (cx - 4, cy + 2)]), "#3A2C22"))
braid.append(fill(P([(130, 176), (142, 176), (141, 186), (131, 186)]), GOLD))
parts.append(group("hair-back", braid, "Arkaya sarkan örgü"))

# ------------------------------------------------------------ arka kol ve kalkan
sh, el, wr = (120, 146), (110, 210), (130, 246)
parts.append(group("arm-upper-back", [
    fill(taper(sh, el, 32, 24, bulge=2), dark(RED, 0.12)),
    fill(taper_shadow(sh, el, 32, 24, 0.45, bulge=2), dark(RED, 0.3)),
]))
parts.append(group("arm-lower-back", [
    fill(taper(el, wr, 24, 19), dark(LEATHER, 0.08)),
    fill(taper_shadow(el, wr, 24, 19, 0.45), dark(LEATHER, 0.22)),
]))
cx, cy, rx, ry = 98, 240, 54, 62
shield = []


def ell(cx, cy, rx, ry):
    k = 0.5523
    return (f"M{f(cx)} {f(cy - ry)} C{f(cx + rx * k)} {f(cy - ry)} {f(cx + rx)} {f(cy - ry * k)} {f(cx + rx)} {f(cy)} "
            f"C{f(cx + rx)} {f(cy + ry * k)} {f(cx + rx * k)} {f(cy + ry)} {f(cx)} {f(cy + ry)} "
            f"C{f(cx - rx * k)} {f(cy + ry)} {f(cx - rx)} {f(cy + ry * k)} {f(cx - rx)} {f(cy)} "
            f"C{f(cx - rx)} {f(cy - ry * k)} {f(cx - rx * k)} {f(cy - ry)} {f(cx)} {f(cy - ry)} Z")


shield.append(fill(ell(cx, cy, rx, ry), "#B07A1E"))
shield.append(fill(ell(cx, cy, rx - 8, ry - 9), NAVY))
# Kalkanın sağ alt yarısı gölgede (sert kenar)
shield.append(fill(Q(("M", cx + rx * 0.75, cy - ry * 0.66), ("C", cx + rx * 1.1, cy - ry * 0.2, cx + rx * 0.9, cy + ry * 0.7, cx + rx * 0.2, cy + ry * 0.98),
                     ("C", cx + rx * 0.5, cy + ry * 0.4, cx + rx * 0.62, cy - ry * 0.1, cx + rx * 0.75, cy - ry * 0.66)), "#000000", 0.28))
for a in range(4):
    ang = math.radians(45 + a * 90)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    x1, y1 = cx + ux * 14, cy + uy * 16
    x2, y2 = cx + ux * 44, cy + uy * 51
    shield.append(fill(P([(x1 + px * 3, y1 + py * 3), (x2 + px * 4, y2 + py * 4), (x2 - px * 4, y2 - py * 4), (x1 - px * 3, y1 - py * 3)]), GOLD))
for a in range(16):
    ang = math.radians(a * 22.5)
    shield.append(f'<circle cx="{f(cx + math.cos(ang) * (rx - 4))}" cy="{f(cy + math.sin(ang) * (ry - 4))}" r="2.4" fill="{light(GOLD, 0.2)}"/>')
shield.append(fill(ell(cx, cy, 15, 17), "#8D98A3"))
shield.append(fill(ell(cx - 3, cy - 4, 10, 11), STEEL))
shield.append(fill(ell(cx - 6, cy - 8, 4, 4.5), "#FFFFFF", 0.85))
parts.append(group("shield", shield, "Kalkan"))

# ------------------------------------------------------------ bacaklar
for side, hip, knee, ank, t in [("back", (150, 268), (136, 382), (128, 470), 0.12), ("front", (186, 268), (206, 378), (218, 470), 0.0)]:
    base = dark(NAVY, t) if t else NAVY
    bt = dark(BOOT, t) if t else BOOT
    parts.append(group(f"leg-upper-{side}", [
        fill(taper(hip, knee, 34, 24, bulge=3, bulge_at=0.35), base),
        fill(taper_shadow(hip, knee, 34, 24, 0.42, bulge=3, bulge_at=0.35), dark(base, 0.16)),
    ]))
    kx, ky = knee
    lower = [
        fill(taper((kx, ky - 4), ank, 26, 18, bulge=2, bulge_at=0.25), bt),
        fill(taper_shadow((kx, ky - 4), ank, 26, 18, 0.4, bulge=2, bulge_at=0.25), dark(bt, 0.12)),
        # Çizme ağzı: köşeli, açık deri
        fill(P([(kx - 16, ky - 8), (kx + 16, ky - 12), (kx + 15, ky + 6), (kx - 15, ky + 8)]), tone(LEATHER, -t)),
        fill(P([(kx + 2, ky - 10), (kx + 16, ky - 12), (kx + 15, ky + 6), (kx + 2, ky + 7)]), dark(LEATHER, 0.15 + t)),
        # Işık şeridi
        fill(P([(kx - 9, ky + 12), (kx - 5, ky + 12), (ank[0] - 5, ank[1] - 14), (ank[0] - 8, ank[1] - 14)]), light(bt, 0.12)),
    ]
    parts.append(group(f"leg-lower-{side}", lower))
    ax, ay = ank
    parts.append(group(f"foot-{side}", [
        fill(S([(ax - 10, ay - 4), (ax + 9, ay - 6), (ax + 18, ay + 12), (ax + 38, ay + 20), (ax + 52, ay + 10), (ax + 48, 498),
                (ax - 12, 500)], sharp=(0, 1, 4, 5, 6)), bt),
        fill(S([(ax + 2, ay + 20), (ax + 38, ay + 24), (ax + 48, 498), (ax - 12, 500), (ax - 12, ay + 26)], sharp=(2, 3)), dark(bt, 0.12)),
        fill(P([(ax - 13, 496), (ax + 46, 496), (ax + 46, 500), (ax - 13, 500)]), "#2A1608"),
    ]))

# ------------------------------------------------------------ kaftan eteği (tek parça, önden yırtmaçlı)
coat = []
coat.append(fill(S([(128, 242), (200, 246), (210, 290), (232, 340), (246, 384), (214, 394), (190, 390), (160, 396), (130, 392), (112, 382), (120, 320)],
                   sharp=(0, 1, 4, 6, 9)), RED))
# Işıktan uzak yan ve yırtmacın gölgesi: sert kenarlı şekiller
coat.append(fill(S([(196, 248), (210, 290), (232, 340), (246, 384), (226, 390), (214, 330), (200, 290)], sharp=(0, 3, 4)), dark(RED, 0.2)))
coat.append(fill(S([(184, 252), (192, 252), (196, 330), (192, 392), (186, 392), (188, 320)], sharp=(0, 1, 3, 4)), dark(RED, 0.32)))
coat.append(fill(S([(130, 260), (150, 256), (138, 320), (124, 372), (118, 360)], sharp=(0, 1, 3)), light(RED, 0.1)))
# Altın etek kenarı
coat.append(fill(S([(112, 382), (130, 392), (160, 396), (190, 390), (214, 394), (246, 384), (244, 376), (214, 386), (190, 382), (160, 388), (130, 384), (114, 374)],
                   sharp=(0, 5, 6, 11)), GOLD))
parts.append(group("coat-back", [], "Etek tek parça: coat-front grubunda"))
front = coat

# ------------------------------------------------------------ gövde
torso = []
torso.append(fill(S([(150, 124), (122, 130), (110, 150), (114, 198), (128, 244), (200, 246), (214, 206), (224, 166), (226, 142), (214, 128), (186, 124)], sharp=(4, 5)), RED))
torso.append(fill(S([(198, 128), (214, 128), (226, 142), (224, 166), (214, 206), (200, 246), (186, 244), (202, 200), (206, 160)], sharp=(5, 6)), dark(RED, 0.2)))
torso.append(fill(S([(120, 132), (138, 128), (126, 160), (118, 200), (114, 196), (110, 150)], sharp=(1, 3)), light(RED, 0.1)))
# Pullu göğüslük: düz çelik + sert gölge + sıra sıra pullar
lam = [(128, 146), (168, 136), (214, 146), (212, 190), (206, 232), (168, 238), (132, 234), (126, 190)]
torso.append(fill(S(lam, sharp=(0, 2, 4, 6)), STEEL))
torso.append(fill(S([(190, 140), (214, 146), (212, 190), (206, 232), (184, 236), (196, 190)], sharp=(1, 3, 4)), dark(STEEL, 0.2)))
for row, y in enumerate(range(150, 232, 11)):
    x = 130 + (row % 2) * 5
    while x < 206:
        sx = x + 9
        shade_col = dark(STEEL, 0.32) if x > 188 else dark(STEEL, 0.18)
        torso.append(fill(P([(x, y + 7), (sx, y + 7), (sx - 1, y + 10), (x + 1, y + 10)]), shade_col))
        x += 10
torso.append(fill(P([(134, 150), (160, 141), (150, 170), (136, 200)]), "#FFFFFF", 0.35))
# Yaka: keskin V, altın şerit
torso.append(fill(P([(148, 122), (156, 120), (172, 142), (188, 120), (196, 122), (174, 152)]), GOLD))
torso.append(fill(P([(156, 120), (188, 120), (172, 142)]), dark(SKIN, 0.12)))
# Kemer, toka, sarkan uç
torso.append(fill(P([(124, 232), (204, 234), (202, 252), (126, 250)]), LEATHER))
torso.append(fill(P([(124, 246), (202, 248), (202, 252), (126, 250)]), dark(LEATHER, 0.15)))
torso.append(fill(P([(170, 230), (192, 231), (191, 254), (169, 253)]), GOLD))
torso.append(fill(P([(176, 236), (186, 236), (186, 248), (176, 248)]), dark(GOLD, 0.35)))
torso.append(fill(P([(180, 253), (190, 253), (192, 282), (186, 288), (180, 282)]), LEATHER))
torso.append(fill(P([(180, 278), (192, 278), (186, 290)]), GOLD))
parts.append(group("coat-front", front, "Kaftanın ön eteği"))
parts.append(group("torso", torso, "Gövde: kaftan, pullu göğüslük, kemer"))

# ------------------------------------------------------------ baş
head = []
head.append(fill(P([(162, 102), (184, 104), (186, 128), (160, 128)]), dark(SKIN, 0.12)))
face = [(162, 50), (186, 48), (198, 58), (201, 70), (203, 78), (210, 90), (204, 94), (204, 100), (203, 106),
        (198, 116), (186, 120), (170, 118), (158, 108), (152, 94), (150, 74), (154, 58)]
head.append(fill(S(face, sharp=(5, 6, 9)), SKIN))
# Yüzün gölgeli yanı yok (yüz sağa bakıyor, ışık soldan): çene altı ve elmacık gölgesi
head.append(fill(P([(170, 118), (186, 120), (198, 116), (196, 110), (184, 112), (172, 110)]), dark(SKIN, 0.16)))
head.append(fill(P([(203, 78), (210, 90), (204, 94), (200, 92)]), dark(SKIN, 0.2)))  # burun altı
# Saç
head.append(fill(S([(152, 60), (166, 52), (164, 72), (160, 100), (154, 104), (148, 88)], sharp=(1, 4)), HAIR))
head.append(fill(P([(154, 66), (160, 60), (156, 84)]), "#4A3A30"))
# Kulak
head.append(fill(P([(160, 82), (167, 80), (169, 92), (164, 98), (159, 94)]), SKIN))
head.append(fill(P([(163, 85), (166, 85), (165, 93)]), dark(SKIN, 0.2)))
# Göz: ak, bebek; kaş: keskin
head.append(fill(P([(186, 76), (194, 74), (198, 78), (192, 80)]), "#FFFFFF"))
head.append(fill(P([(191, 75), (195, 75), (195, 79), (192, 80)]), HAIR))
head.append(fill(P([(182, 70), (200, 66), (201, 70), (184, 74)]), HAIR))
# Sakal ve bıyık: sivri uçlu
head.append(fill(S([(158, 100), (168, 112), (184, 116), (198, 112), (200, 120), (190, 134), (180, 126), (166, 120), (156, 108)], sharp=(0, 3, 5)), HAIR))
head.append(fill(S([(190, 98), (204, 96), (206, 102), (201, 113), (196, 104)], sharp=(0, 3)), HAIR))
head.append(fill(P([(186, 120), (196, 118), (190, 128)]), "#3A2C22"))
# Börk: kırmızı keçe, kürk kenar, altın bant, beyaz tüy
head.append(fill(P([(170, 34), (146, 6), (152, 8), (176, 30)]), WHITE))
head.append(fill(P([(170, 34), (150, 8), (152, 8), (173, 32)]), "#B8B0A0"))
head.append(fill(S([(154, 52), (162, 26), (186, 6), (196, 30), (200, 52)], sharp=(0, 2, 4)), RED))
head.append(fill(P([(178, 10), (186, 6), (200, 52), (184, 52)]), dark(RED, 0.2)))
head.append(fill(P([(158, 40), (168, 18), (172, 18), (164, 40)]), light(RED, 0.12)))
head.append(fill(P([(155, 44), (199, 44), (200, 51), (154, 51)]), GOLD))
head.append(f'<circle cx="186" cy="6" r="4.5" fill="{GOLD}"/>')
fur = [(146, 66), (144, 56), (152, 48), (176, 46), (204, 50), (210, 60), (206, 66)]
for i in range(8):
    fur.append((206 - (i + 1) * 7.5, 66 + (3 if i % 2 == 0 else 0)))
head.append(fill(S(fur, sharp=tuple(range(6, len(fur)))), FUR))
head.append(fill(P([(186, 48), (204, 50), (210, 60), (206, 66), (190, 62)]), dark(FUR, 0.12)))
head.append(fill(P([(150, 54), (172, 48), (166, 54), (152, 58)]), light(FUR, 0.15)))
parts.append(group("head", head, "Baş: yüz, sakal, börk"))

# ------------------------------------------------------------ ön kol ve kılıç
sh2, el2, wr2 = (220, 144), (238, 208), (250, 250)
parts.append(group("arm-upper-front", [
    fill(taper(sh2, el2, 34, 26, bulge=3), RED),
    fill(taper_shadow(sh2, el2, 34, 26, 0.42, bulge=3), dark(RED, 0.2)),
    fill(P([(220, 186), (246, 182), (248, 190), (222, 194)]), GOLD),
]))
parts.append(group("arm-lower-front", [
    fill(taper(el2, wr2, 26, 20, bulge=2, bulge_at=0.3), LEATHER),
    fill(taper_shadow(el2, wr2, 26, 20, 0.42, bulge=2, bulge_at=0.3), dark(LEATHER, 0.18)),
    fill(P([(234, 222), (252, 218), (253, 224), (235, 228)]), GOLD),
]))
sword = [
    fill(Q(("M", 252, 278), ("C", 262, 334, 284, 392, 320, 452), ("C", 300, 404, 286, 356, 268, 276)), "#DDE4EA"),
    fill(Q(("M", 261, 278), ("C", 270, 334, 290, 390, 320, 452), ("C", 300, 404, 286, 356, 268, 276)), "#8C97A2"),
    fill(Q(("M", 256, 280), ("C", 266, 330, 280, 372, 300, 416), ("C", 284, 376, 270, 334, 259, 280)), "#FFFFFF", 0.8),
    fill(P([(242, 270), (276, 264), (279, 272), (245, 279)]), GOLD),
    fill(P([(258, 268), (276, 264), (279, 272), (260, 276)]), dark(GOLD, 0.2)),
    fill(taper((244, 236), (256, 268), 11, 10), "#3A220E"),
    f'<circle cx="243" cy="233" r="6.5" fill="{GOLD}"/>',
]
parts.append(group("weapon", sword, "Eğri kılıç"))
parts.append(group("hand-front", [
    fill(P([(240, 244), (252, 238), (264, 242), (266, 258), (260, 270), (244, 268), (238, 258)]), SKIN),
    fill(P([(258, 242), (264, 242), (266, 258), (260, 270), (254, 268), (258, 256)]), dark(SKIN, 0.15)),
    fill(P([(242, 250), (258, 248), (258, 251), (242, 253)]), dark(SKIN, 0.2)),
    fill(P([(242, 259), (258, 258), (258, 261), (242, 262)]), dark(SKIN, 0.2)),
]))

body = "\n  ".join(parts)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="520" viewBox="0 0 360 520">\n'
       f'  <!-- Örnek kahraman: bozkır beyi (sert kenarlı tarz, dış hatsız). Ayak tabanı y=500. '
       f'Parçalar ayrı gruplardır (kukla için). -->\n'
       f'  <defs>\n    ' + "\n    ".join(d.items) + f'\n  </defs>\n  {body}\n</svg>\n')
with open(OUT, "w") as fh:
    fh.write(svg)
