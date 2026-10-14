"""Örnek kahraman: bozkır beyi. Parçalı kukla düzeninde (her parça ayrı grup)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f, mix  # noqa: E402
from charkit import Defs, ink, lit, shade, limb, path, line, group, OUTLINE_W, DETAIL_W  # noqa: E402

OUT = sys.argv[1]

SKIN = "#E0B07E"
HAIR = "#231A14"
RED = "#A3241A"
GOLD = "#E8B22C"
NAVY = "#23406E"
LEATHER = "#8B5A2B"
BOOT = "#5C3A1B"
STEEL = "#9AA4AE"
FUR = "#6B4E2A"

d = Defs("h")
parts = []

# ------------------------------------------------------------ saç örgüsü (gövdenin arkasında)
braid = []
for i in range(6):
    cx, cy = 150 - i * 3.2, 96 + i * 13
    braid.append(path(f"M{f(cx - 7)} {f(cy)} C{f(cx - 8)} {f(cy - 9)} {f(cx + 8)} {f(cy - 9)} {f(cx + 7)} {f(cy)} "
                      f"C{f(cx + 6)} {f(cy + 9)} {f(cx - 6)} {f(cy + 9)} {f(cx - 7)} {f(cy)} Z",
                      d.volume(HAIR, cx - 7, cy - 8, cx + 7, cy + 8, 0.25, 0.1), ink(HAIR, 0.6), 3))
braid.append(path("M128 168 L140 168 L139 178 L129 178 Z", GOLD, ink(GOLD), 3))
parts.append(group("hair-back", braid, "Arkaya sarkan örgü"))

# ------------------------------------------------------------ arka kol ve kalkan
p_sh, p_el, p_wr = (118, 138), (104, 206), (128, 244)
parts.append(group("arm-upper-back", [
    path(limb(p_sh, p_el, 40, 32, 2), d.cylinder(shade(RED, 0.18), p_sh, p_el, 40), ink(RED)),
]))
parts.append(group("arm-lower-back", [
    path(limb(p_el, p_wr, 30, 24), d.cylinder(shade(LEATHER, 0.18), p_el, p_wr, 30), ink(LEATHER)),
]))
shield = []
cx, cy = 96, 238
shield.append(path(f"M{cx} {cy - 64} C{cx + 36} {cy - 64} {cx + 56} {cy - 34} {cx + 56} {cy} "
                   f"C{cx + 56} {cy + 36} {cx + 34} {cy + 64} {cx} {cy + 64} "
                   f"C{cx - 34} {cy + 64} {cx - 56} {cy + 36} {cx - 56} {cy} "
                   f"C{cx - 56} {cy - 34} {cx - 36} {cy - 64} {cx} {cy - 64} Z",
                   d.volume("#B5832E", cx - 50, cy - 60, cx + 50, cy + 60, 0.3, 0.35), ink("#B5832E")))
shield.append(path(f"M{cx} {cy - 52} C{cx + 30} {cy - 52} {cx + 45} {cy - 27} {cx + 45} {cy} "
                   f"C{cx + 45} {cy + 29} {cx + 27} {cy + 52} {cx} {cy + 52} "
                   f"C{cx - 28} {cy + 52} {cx - 45} {cy + 28} {cx - 45} {cy} "
                   f"C{cx - 45} {cy - 27} {cx - 30} {cy - 52} {cx} {cy - 52} Z",
                   d.volume(NAVY, cx - 40, cy - 50, cx + 40, cy + 50, 0.22, 0.35), ink(NAVY), 3))
# Altın kollar ve kurt dişi deseni
for a in range(4):
    ang = math.radians(45 + a * 90)
    x1, y1 = cx + math.cos(ang) * 14, cy + math.sin(ang) * 16
    x2, y2 = cx + math.cos(ang) * 43, cy + math.sin(ang) * 50
    shield.append(line(f"M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}", GOLD, 5))
for a in range(16):
    ang = math.radians(a * 22.5)
    shield.append(f'<circle cx="{f(cx + math.cos(ang) * 50)}" cy="{f(cy + math.sin(ang) * 58)}" r="2.6" fill="{lit(GOLD, 0.3)}"/>')
shield.append(path(f"M{cx - 15} {cy} C{cx - 15} {cy - 10} {cx - 8} {cy - 16} {cx} {cy - 16} C{cx + 8} {cy - 16} {cx + 15} {cy - 10} "
                   f"{cx + 15} {cy} C{cx + 15} {cy + 10} {cx + 8} {cy + 16} {cx} {cy + 16} C{cx - 8} {cy + 16} {cx - 15} {cy + 10} {cx - 15} {cy} Z",
                   d.rad(cx - 5, cy - 6, 18, [(0, "#F0F4F8"), (0.5, STEEL), (1, shade(STEEL, 0.4))]), ink(STEEL), 3))
parts.append(group("shield", shield, "Kalkan: arka kolda"))

# ------------------------------------------------------------ arka bacak
hip_b, knee_b, ank_b = (150, 262), (132, 378), (122, 474)
parts.append(group("leg-upper-back", [
    path(limb(hip_b, knee_b, 48, 36, 3), d.cylinder(shade(NAVY, 0.15), hip_b, knee_b, 48), ink(NAVY)),
]))
parts.append(group("leg-lower-back", [
    path(limb((131, 384), ank_b, 38, 30), d.cylinder(shade(BOOT, 0.12), (131, 384), ank_b, 38), ink(BOOT)),
    path("M110 380 Q131 372 152 382 L150 398 Q131 390 112 396 Z", d.volume(LEATHER, 110, 372, 152, 398), ink(LEATHER), 3.5),
]))
parts.append(group("foot-back", [
    path("M108 466 L106 499 L150 500 C160 500 166 494 168 484 C156 486 146 482 138 470 Z",
         d.volume(shade(BOOT, 0.12), 106, 466, 168, 500), ink(BOOT)),
]))


# ------------------------------------------------------------ ön bacak
hip_f, knee_f, ank_f = (190, 262), (214, 372), (226, 474)
parts.append(group("leg-upper-front", [
    path(limb(hip_f, knee_f, 52, 38, 3), d.cylinder(NAVY, hip_f, knee_f, 52), ink(NAVY)),
]))
parts.append(group("leg-lower-front", [
    path(limb((214, 378), ank_f, 40, 31), d.cylinder(BOOT, (214, 378), ank_f, 40), ink(BOOT)),
    path("M191 374 Q214 366 237 376 L236 393 Q214 385 193 391 Z", d.volume(lit(LEATHER, 0.1), 191, 366, 237, 393), ink(LEATHER), 3.5),
    line("M220 400 C224 430 226 452 226 468", lit(BOOT, 0.25), 3, 0.7),
]))
parts.append(group("foot-front", [
    path("M210 466 L208 499 L258 500 C270 500 276 492 278 480 C264 484 252 480 244 470 Z",
         d.volume(BOOT, 208, 466, 278, 500), ink(BOOT)),
    line("M232 470 L234 498", ink(BOOT, 0.7), 2),
]))

# ------------------------------------------------------------ kaftanın eteği (bacakların önünde)
parts.append(group("coat-back", [
    path("M126 244 L200 246 C201 300 201 350 200 394 C168 400 136 394 108 382 C114 334 120 288 126 244 Z",
         d.volume(shade(RED, 0.16), 110, 246, 200, 398), ink(RED)),
    line("M114 372 C140 384 170 388 196 386", GOLD, 6),
    line("M150 262 C146 300 140 340 134 378", shade(RED, 0.4), 2, 0.7),
]))

# ------------------------------------------------------------ kaftanın ön eteği
parts.append(group("coat-front", [
    path("M186 248 L204 246 C218 290 232 330 248 372 C230 388 212 394 196 394 C194 340 190 294 186 248 Z",
         d.volume(RED, 186, 246, 248, 394), ink(RED)),
    line("M200 384 C220 384 234 378 242 368", GOLD, 6),
    line("M206 268 C214 304 224 338 234 362", lit(RED, 0.25), 2, 0.6),
]))

# ------------------------------------------------------------ gövde
torso = []
torso.append(path("M150 116 C132 116 112 120 106 138 C100 160 112 210 124 244 L198 246 "
                  "C208 222 224 196 224 164 C224 146 222 132 212 124 C202 116 190 114 182 116 Z",
                  d.volume(RED, 108, 118, 224, 246), ink(RED)))
# Pullu göğüslük
torso.append(path("M126 142 Q170 130 214 142 C216 176 212 206 206 232 Q170 238 132 234 C126 206 124 172 126 142 Z",
                  d.volume(STEEL, 126, 132, 214, 236, 0.3, 0.38), ink(STEEL)))
for i, y in enumerate(range(150, 232, 13)):
    xs = 129 if i % 2 == 0 else 134
    scallop = f"M{xs} {y}"
    x = xs
    while x < 208:
        scallop += f" Q{x + 5} {y + 7} {x + 10} {y}"
        x += 10
    torso.append(line(scallop, ink(STEEL, 0.55), 2))
# Göğüslüğe vuran ışık (sol üst)
torso.append(path("M132 146 Q150 140 168 140 C160 160 150 186 136 206 C130 186 130 164 132 146 Z", "#FFFFFF", extra=' opacity="0.18"'))
# Yaka: altın kenar
torso.append(line("M150 119 C158 132 168 140 178 141 C186 136 192 126 196 118", GOLD, 7))
# Kemer ve toka
torso.append(path("M122 228 L202 230 L200 250 L124 248 Z", d.volume("#6B4423", 122, 228, 202, 250), ink(LEATHER)))
torso.append(path("M172 228 L192 229 L191 251 L171 250 Z", d.volume(GOLD, 171, 228, 192, 251, 0.35, 0.3), ink(GOLD), 3))
torso.append(path("M177 234 L186 234 L186 245 L177 245 Z", shade(GOLD, 0.4)))
torso.append(path("M180 250 L188 250 L190 276 L182 276 Z", d.volume("#6B4423", 180, 250, 190, 276), ink(LEATHER), 3))
torso.append(path("M181 272 L191 272 L192 282 L182 282 Z", GOLD, ink(GOLD), 2.5))
parts.append(group("torso", torso, "Gövde: kaftan, pullu göğüslük, kemer"))

# ------------------------------------------------------------ baş
head = []
head.append(path(limb((172, 102), (170, 122), 24, 28), d.volume(shade(SKIN, 0.12), 158, 102, 184, 122), ink(SKIN)))
face = ("M160 42 C176 36 192 40 197 52 C200 58 200 63 200 67 C201 72 205 79 208 84 C206 87 202 88 199 88 "
        "C200 90 201 92 200 94 C199 96 199 97 200 99 C200 103 198 106 195 108 C188 112 174 112 162 106 "
        "C154 102 150 96 148 88 C144 76 146 54 160 42 Z")
head.append(path(face, d.volume(SKIN, 150, 50, 206, 110, 0.2, 0.26), ink(SKIN)))
# Saç (başın arkası, börkün altında)
head.append(path("M147 60 C142 74 144 90 152 98 C156 92 158 84 158 74 C160 66 158 60 156 56 Z",
                 d.volume(HAIR, 144, 58, 160, 98, 0.25, 0.1), ink(HAIR, 0.6), 3))
# Kulak
head.append(path("M156 76 C150 72 148 82 151 88 C153 92 158 92 160 88 Z", d.volume(SKIN, 148, 72, 160, 92), ink(SKIN), 3))
# Yanak gölgesi ve elmacık
head.append(path("M176 88 C184 94 190 96 196 92 C192 100 184 102 176 98 Z", shade(SKIN, 0.18), extra=' opacity="0.6"'))
# Göz, kaş
head.append(path("M180 72 Q186 68 192 71 Q187 76 180 72 Z", HAIR))
head.append(path("M175 64 Q186 58 199 63 L198 67 Q187 63 177 68 Z", HAIR))
head.append(line("M181 76 Q186 78 191 76", ink(SKIN, 0.55), 1.6, 0.7))
# Sakal ve bıyık
head.append(path("M153 90 C157 102 168 111 183 112 C191 112 196 109 199 103 L196 100 C190 104 182 105 175 102 "
                 "C167 99 161 94 157 88 Z", d.volume(HAIR, 153, 88, 199, 112, 0.22, 0.1), ink(HAIR, 0.6), 2.5))
head.append(path("M187 94 C192 91 198 91 202 95 C202 100 200 105 196 108 C195 102 192 98 187 97 Z",
                 d.volume(HAIR, 187, 91, 202, 108, 0.25, 0.1), ink(HAIR, 0.6), 2))
# Börk: kırmızı keçe tepe, kürk kenar, altın bant, tüy
head.append(path("M164 30 C164 22 154 10 142 6 C146 14 150 22 155 32 Z", d.volume("#F4F1E6", 142, 6, 166, 32, 0.1, 0.25), ink("#D8D2C2", 0.55), 2.2))
head.append(line("M161 30 C157 20 151 13 144 8", "#9A938A", 1.4))
head.append(path("M152 48 C156 26 170 10 186 6 C190 14 194 28 200 48 Z", d.volume(RED, 152, 4, 200, 48, 0.25, 0.3), ink(RED)))
head.append(path("M153 40 L199 40 L200 47 L152 47 Z", GOLD, ink(GOLD), 2.5))
head.append(f'<circle cx="186" cy="5" r="4.5" fill="{GOLD}" stroke="{ink(GOLD)}" stroke-width="2.2"/>')
fur = "M142 62 C138 50 150 42 172 42 C194 42 208 48 208 58"
x = 208
for i in range(9):
    nx = 208 - (i + 1) * 7.3
    fur += f" Q{f(x - 3.6)} {f(66 + (i % 2) * 2)} {f(nx)} {f(62 + (i % 3))}"
    x = nx
head.append(path(fur + " Z", d.volume(FUR, 140, 42, 208, 66, 0.3, 0.25), ink(FUR)))
head.append(line("M150 52 Q160 48 170 50 M178 48 Q188 46 198 50", lit(FUR, 0.35), 2, 0.8))
parts.append(group("head", head, "Baş: yüz, sakal, börk"))

# ------------------------------------------------------------ ön kol ve kılıç
p_sh2, p_el2, p_wr2 = (222, 138), (236, 206), (248, 250)
parts.append(group("arm-upper-front", [
    path(limb(p_sh2, p_el2, 42, 34, 2), d.cylinder(RED, p_sh2, p_el2, 42), ink(RED)),
    line("M218 180 Q232 176 244 182", GOLD, 6),
]))
parts.append(group("arm-lower-front", [
    path(limb(p_el2, p_wr2, 32, 26), d.cylinder(LEATHER, p_el2, p_wr2, 32), ink(LEATHER)),
    line("M233 220 Q244 216 252 222", GOLD, 4),
]))
sword = []
sword.append(path("M250 278 C262 334 284 392 318 450 C300 404 286 356 268 276 Z",
                  d.lin(250, 300, 272, 296, [(0, "#F4F7FA"), (0.45, "#C9D1D9"), (1, "#6E7882")]), ink(STEEL)))
sword.append(line("M258 290 C270 340 286 384 306 424", "#8E98A2", 1.6, 0.9))
sword.append(path("M242 270 L276 266 L278 276 L244 280 Z", d.volume(GOLD, 242, 266, 278, 280, 0.35, 0.3), ink(GOLD), 3))
sword.append(path(limb((244, 234), (256, 268), 12, 12), d.volume("#4A3019", 244, 234, 256, 268), ink("#4A3019"), 3))
sword.append(f'<circle cx="243" cy="232" r="7" fill="{GOLD}" stroke="{ink(GOLD)}" stroke-width="3"/>')
parts.append(group("weapon", sword, "Eğri kılıç"))
parts.append(group("hand-front", [
    path("M238 246 C240 238 256 236 262 242 C266 250 266 262 260 268 C252 272 242 270 238 262 Z",
         d.volume(SKIN, 238, 238, 266, 270), ink(SKIN)),
    line("M246 248 L260 246 M244 256 L262 255 M245 263 L259 263", ink(SKIN, 0.55), 1.8, 0.8),
]))

body = "\n  ".join(parts)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="520" viewBox="0 0 360 520">\n'
       f'  <!-- Örnek kahraman: bozkır beyi. Baş 64 birim, boy ~7,25 baş; ayak tabanı y=500. '
       f'Parçalar ayrı gruplardır (kukla için). -->\n'
       f'  <defs>\n    ' + "\n    ".join(d.items) + f'\n  </defs>\n  {body}\n</svg>\n')
with open(OUT, "w") as fh:
    fh.write(svg)
