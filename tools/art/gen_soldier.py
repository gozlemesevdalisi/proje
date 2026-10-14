"""Örnek asker: bozkır mızrakçısı. Parçalı kukla düzeninde."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f  # noqa: E402
from charkit import Defs, ink, lit, shade, limb, path, line, group  # noqa: E402

OUT = sys.argv[1]

SKIN = "#B67E50"
HAIR = "#231A14"
COAT = "#2E4F7E"
SASH = "#C9962E"
LINEN = "#D9CCAE"
WRAP = "#BFAE8C"
BOOT = "#7A5232"
FELT = "#E2DACA"
WICKER = "#C9A66B"
STEEL = "#9AA4AE"
SHAFT = "#7A4E2A"

d = Defs("s")
parts = []

# ------------------------------------------------------------ arka kol ve hasır kalkan
sh, el, wr = (104, 148), (94, 212), (104, 252)
parts.append(group("arm-upper-back", [path(limb(sh, el, 34, 28, 2), d.cylinder(shade(COAT, 0.18), sh, el, 34), ink(COAT))]))
parts.append(group("arm-lower-back", [path(limb(el, wr, 27, 22), d.cylinder(shade(COAT, 0.18), el, wr, 27), ink(COAT))]))
cx, cy, r = 86, 262, 38
shield = [path(f"M{cx - r} {cy} C{cx - r} {cy - r * 0.55} {cx - r * 0.55} {cy - r} {cx} {cy - r} "
               f"C{cx + r * 0.55} {cy - r} {cx + r} {cy - r * 0.55} {cx + r} {cy} "
               f"C{cx + r} {cy + r * 0.55} {cx + r * 0.55} {cy + r} {cx} {cy + r} "
               f"C{cx - r * 0.55} {cy + r} {cx - r} {cy + r * 0.55} {cx - r} {cy} Z",
               d.volume(WICKER, cx - r, cy - r, cx + r, cy + r, 0.25, 0.32), ink(WICKER))]
# Hasır örgüsü: iç içe halkalar
for k in (0.78, 0.56, 0.34):
    rr = r * k
    shield.append(line(f"M{f(cx - rr)} {cy} C{f(cx - rr)} {f(cy - rr * 0.55)} {f(cx - rr * 0.55)} {f(cy - rr)} {cx} {f(cy - rr)} "
                       f"C{f(cx + rr * 0.55)} {f(cy - rr)} {f(cx + rr)} {f(cy - rr * 0.55)} {f(cx + rr)} {cy} "
                       f"C{f(cx + rr)} {f(cy + rr * 0.55)} {f(cx + rr * 0.55)} {f(cy + rr)} {cx} {f(cy + rr)} "
                       f"C{f(cx - rr * 0.55)} {f(cy + rr)} {f(cx - rr)} {f(cy + rr * 0.55)} {f(cx - rr)} {cy} Z",
                       shade(WICKER, 0.35), 2, 0.8))
shield.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{shade(WICKER, 0.25)}" stroke="{ink(WICKER)}" stroke-width="3"/>')
parts.append(group("shield", shield, "Hasır kalkan"))

# ------------------------------------------------------------ bacaklar
for side, hip, knee, ank, tone in [("back", (132, 268), (122, 380), (116, 474), 0.16),
                                   ("front", (164, 268), (178, 378), (186, 474), 0.0)]:
    trouser = shade(LINEN, tone)
    wrap = shade(WRAP, tone)
    boot = shade(BOOT, tone)
    parts.append(group(f"leg-upper-{side}", [
        path(limb(hip, knee, 46, 36, 4), d.cylinder(trouser, hip, knee, 46), ink(LINEN)),
    ]))
    lower = [path(limb((knee[0], knee[1] + 4), ank, 34, 26), d.cylinder(wrap, knee, ank, 34), ink(WRAP))]
    # Dolama bantları
    for i in range(6):
        t = 0.22 + i * 0.13
        y = knee[1] + (ank[1] - knee[1]) * t
        x = knee[0] + (ank[0] - knee[0]) * t
        w = 17 - 4 * t
        lower.append(line(f"M{f(x - w)} {f(y - 3)} Q{f(x)} {f(y + 4)} {f(x + w)} {f(y + 2)}", ink(WRAP, 0.55), 1.8, 0.8))
    parts.append(group(f"leg-lower-{side}", lower))
    fx = ank[0]
    parts.append(group(f"foot-{side}", [
        path(f"M{fx - 13} {ank[1] - 6} L{fx - 15} 499 L{fx + 26} 500 C{fx + 36} 500 {fx + 40} 494 {fx + 40} 488 "
             f"C{fx + 30} 486 {fx + 20} 482 {fx + 14} {ank[1] - 4} Z",
             d.volume(boot, fx - 15, ank[1] - 6, fx + 40, 500), ink(BOOT)),
    ]))

# ------------------------------------------------------------ gövde: kapitone kaftan, kuşak
torso = []
coat = ("M136 124 C118 126 104 132 100 148 C96 176 104 214 110 246 C108 280 104 310 100 334 "
        "C128 344 168 346 198 334 C194 306 190 280 188 246 C196 214 202 176 198 152 C196 136 184 126 166 124 Z")
torso.append(path(coat, d.volume(COAT, 100, 124, 200, 344), ink(COAT)))
# Kapitone dikişler
for x0 in range(112, 196, 12):
    torso.append(line(f"M{x0} {150 if 118 < x0 < 186 else 170} C{x0 + 1} 210 {x0 - 1} 270 {x0 - 4 + (x0 - 150) * 0.06} 334",
                      ink(COAT, 0.55), 1.6, 0.55))
# Önden kapanan yaka ve etek kenarı (keçe şerit)
torso.append(line("M144 126 C152 150 160 176 162 246 L160 336", lit(FELT, 0.05), 6))
torso.append(line("M103 330 C130 342 168 344 196 330", lit(FELT, 0.05), 6))
# Işık: sol üst
torso.append(path("M108 150 C116 138 128 132 140 130 C130 160 120 196 112 230 C106 204 104 176 108 150 Z", "#FFFFFF", extra=' opacity="0.12"'))
# Kuşak
torso.append(path("M107 238 C140 246 162 246 191 238 L192 258 C162 266 140 266 106 258 Z",
                  d.volume(SASH, 106, 238, 192, 266, 0.3, 0.3), ink(SASH)))
torso.append(path("M150 258 L162 258 L166 296 L156 300 L148 294 Z", d.volume(SASH, 148, 258, 166, 300, 0.25, 0.3), ink(SASH), 3))
parts.append(group("torso", torso, "Kapitone kaftan ve kuşak"))

# ------------------------------------------------------------ baş
head = []
head.append(path(limb((150, 112), (148, 132), 22, 26), d.volume(shade(SKIN, 0.12), 136, 112, 162, 132), ink(SKIN)))
face = ("M138 56 C152 50 168 54 173 66 C176 72 176 77 176 81 C177 86 182 92 184 97 C182 101 178 102 175 101 "
        "C176 104 177 106 176 108 C175 110 175 111 176 113 C176 117 173 120 170 121 C163 125 150 124 140 118 "
        "C132 114 128 106 126 98 C122 86 124 66 138 56 Z")
head.append(path(face, d.volume(SKIN, 128, 60, 184, 124, 0.22, 0.26), ink(SKIN)))
head.append(path("M126 72 C122 86 124 100 130 108 C134 102 136 94 136 84 C138 78 136 72 134 68 Z",
                 d.volume(HAIR, 122, 70, 138, 108, 0.25, 0.1), ink(HAIR, 0.6), 2.5))
head.append(path("M134 90 C128 86 126 96 129 102 C131 106 136 106 138 102 Z", d.volume(SKIN, 126, 86, 138, 106), ink(SKIN), 2.5))
head.append(path("M156 87 Q162 83 168 86 Q163 90 156 87 Z", HAIR))
head.append(path("M152 79 Q161 75 171 78 L170 81 Q162 79 153 82 Z", HAIR))
head.append(line("M164 108 C168 106 172 106 176 108", HAIR, 2.2))  # ince bıyık
head.append(line("M168 114 L174 113", ink(SKIN, 0.55), 1.6, 0.8))
head.append(path("M150 100 C156 106 164 108 170 104 C166 112 156 112 150 106 Z", shade(SKIN, 0.18), extra=' opacity="0.5"'))
# Sivri keçe külah, kalkık kenar
head.append(path("M128 66 C130 44 146 18 168 12 C166 26 168 44 178 66 Z", d.volume(FELT, 128, 12, 178, 66, 0.15, 0.3), ink(FELT, 0.5)))
head.append(path("M122 70 C124 58 140 56 152 58 C164 56 180 58 184 66 C182 74 164 72 152 72 C140 72 126 76 122 70 Z",
                 d.volume(lit(FELT, 0.05), 122, 56, 184, 74, 0.2, 0.3), ink(FELT, 0.5)))
head.append(line("M136 50 C146 40 156 30 164 22", shade(FELT, 0.25), 2, 0.6))
parts.append(group("head", head, "Baş: genç yüz, ince bıyık, keçe külah"))

# ------------------------------------------------------------ ön kol, mızrak
sh2, el2, wr2 = (190, 150), (208, 208), (204, 236)
parts.append(group("arm-upper-front", [path(limb(sh2, el2, 36, 30, 2), d.cylinder(COAT, sh2, el2, 36), ink(COAT))]))
spear = [
    path("M205 18 L211 18 L212 496 L204 496 Z", d.lin(204, 0, 212, 0, [(0, lit(SHAFT, 0.25)), (1, shade(SHAFT, 0.2))]), ink(SHAFT), 3),
    path("M208 -2 C214 10 218 24 214 44 L208 52 L202 44 C198 24 202 10 208 -2 Z",
         d.lin(200, 0, 216, 0, [(0, "#F4F7FA"), (0.5, "#C9D1D9"), (1, "#6E7882")]), ink(STEEL), 3),
    line("M208 4 L208 44", "#8E98A2", 1.4, 0.9),
    path("M203 52 L213 52 L214 60 L202 60 Z", shade(STEEL, 0.2), ink(STEEL), 2.5),
    path("M206 60 C200 68 198 78 202 86 C206 80 208 72 210 64 C212 72 214 80 218 84 C220 76 216 66 210 60 Z",
         d.volume("#C8372D", 198, 60, 220, 86, 0.25, 0.3), ink("#C8372D"), 2.5),
]
parts.append(group("weapon", spear, "Mızrak"))
parts.append(group("arm-lower-front", [path(limb(el2, wr2, 28, 24), d.cylinder(COAT, el2, wr2, 28), ink(COAT))]))
parts.append(group("hand-front", [
    path("M196 222 C198 214 214 214 218 220 C222 228 222 238 216 244 C208 248 198 246 196 238 Z",
         d.volume(SKIN, 196, 214, 222, 248), ink(SKIN)),
    line("M200 226 L216 225 M199 233 L218 233 M201 240 L215 240", ink(SKIN, 0.55), 1.6, 0.8),
]))

body = "\n  ".join(parts)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="520" viewBox="0 0 300 520">\n'
       f'  <!-- Örnek asker: bozkır mızrakçısı. Baş 64 birim, boy ~7 baş; ayak tabanı y=500. '
       f'Parçalar ayrı gruplardır (kukla için). -->\n'
       f'  <defs>\n    ' + "\n    ".join(d.items) + f'\n  </defs>\n  {body}\n</svg>\n')
with open(OUT, "w") as fh:
    fh.write(svg)
