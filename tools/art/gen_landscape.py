"""Örnek manzara: Bozkır Beylikleri'nde bir savaş alanı, altı paralaks katmanı."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f, mix, smooth_path, hill_shape, blob, linear, radial, svg  # noqa: E402

OUT = sys.argv[1]
W, H = 2560, 1080
SKY_HORIZON = "#9FCBEA"
HAZE = "#B9D3EA"


def hazed(c, t):
    return mix(c, HAZE, t)


def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content)


# ---------------------------------------------------------------- 1. Gök
def cloud(cx, cy, w, h, rng, gid):
    # Üstü kabarık, altı düz bulut.
    n = 6
    pts = [(cx - w / 2, cy)]
    for i in range(n):
        t = (i + 0.5) / n
        x = cx - w / 2 + w * t
        bump = math.sin(t * math.pi) ** 0.7
        y = cy - h * (0.45 + 0.55 * bump) * (0.8 + 0.35 * rng.random())
        pts.append((x, y))
    pts.append((cx + w / 2, cy))
    top = smooth_path(pts, tension=1.2)
    bottom = f" Q{f(cx + w * 0.3)} {f(cy + h * 0.16)} {f(cx)} {f(cy + h * 0.14)} Q{f(cx - w * 0.3)} {f(cy + h * 0.16)} {f(cx - w / 2)} {f(cy)} Z"
    return top + bottom


def sky():
    rng = random.Random(3)
    defs = [
        linear("gok", 0, 0, 0, 740, [(0, "#1B4A9E"), (0.38, "#2E66B9"), (0.7, "#5C93D2"),
                                     (0.9, "#9FCBEA"), (1, "#EFE3BB")]),
        radial("parilti", 840, 210, 520, [(0, "#FFFBE6", 0.95), (0.18, "#FFF1C2", 0.6), (0.45, "#D7E8F7", 0.28), (1, "#BFD9F2", 0)]),
        radial("gunes", 840, 210, 56, [(0, "#FFFFF4"), (0.7, "#FFF6D2"), (1, "#FCEBB0")]),
    ]
    body = ['<rect width="2560" height="1080" fill="url(#gok)"/>',
            '<rect width="2560" height="1080" fill="url(#parilti)"/>',
            '<circle cx="840" cy="210" r="56" fill="url(#gunes)"/>']
    clouds = [(1560, 250, 470, 95), (2230, 170, 330, 70), (330, 330, 300, 62), (1180, 440, 240, 42),
              (1960, 470, 200, 34), (60, 150, 260, 55)]
    for i, (cx, cy, w, h) in enumerate(clouds):
        gid = f"bulut{i}"
        # Uzaktaki (alçaktaki) bulutlar ufka karışır.
        far = min(1.0, max(0.0, (cy - 200) / 320))
        top = mix("#FFFFFF", "#F3F0E6", far * 0.5)
        bottom = mix("#D6E2EF", "#C9D9EA", far)
        defs.append(linear(gid, 0, cy - h, 0, cy + h * 0.2, [(0, top), (0.55, top), (1, bottom)]))
        body.append(f'<path d="{cloud(cx, cy, w, h, rng, gid)}" fill="url(#{gid})" opacity="{0.95 - far * 0.25:.2f}"/>')
    return svg(W, H, defs, body, "Gök: gündüz, güneş sol üstte. Paralaks 0,05.")


# ---------------------------------------------------------------- 2. Uzak dağlar
def mountain_range(peaks, base, rng):
    """Zirve listesinden (x, y) dağ sırası; zirveler hafif yuvarlak."""
    pts = [(-40, base)]
    for i, (x, y) in enumerate(peaks):
        if i > 0:
            px, py = peaks[i - 1]
            vx = (px + x) / 2 + (rng.random() - 0.5) * 40
            vy = max(py, y) + (base - max(py, y)) * (0.35 + 0.3 * rng.random())
            pts.append((vx, vy))
        pts.append((x, y))
    pts.append((W + 40, base))
    return pts


def far():
    rng = random.Random(7)
    defs = [
        linear("arka", 0, 470, 0, 760, [(0, "#A9C1DA"), (1, "#C4D7EA")]),
        linear("on", 0, 520, 0, 780, [(0, "#8CA5C2"), (1, "#B2C8DE")]),
    ]
    body = []
    back_peaks = [(120, 560), (420, 500), (700, 545), (980, 470), (1300, 530), (1620, 455), (1900, 520),
                  (2200, 480), (2480, 540)]
    pts = mountain_range(back_peaks, 760, rng)
    body.append(f'<path d="{smooth_path(pts, tension=0.55)} L{W + 40} 1080 L-40 1080 Z" fill="url(#arka)"/>')
    front_peaks = [(0, 640), (260, 590), (560, 625), (860, 560), (1150, 610), (1460, 575), (1760, 630),
                   (2060, 585), (2380, 620), (2600, 600)]
    pts2 = mountain_range(front_peaks, 800, rng)
    body.append(f'<path d="{smooth_path(pts2, tension=0.55)} L{W + 40} 1080 L-40 1080 Z" fill="url(#on)"/>')
    # Işık sol üstten: zirvelerin sağ yamacı bir ton koyu, en yüksek zirvelerde kar.
    for i, (x, y) in enumerate(back_peaks):
        nx = back_peaks[i + 1][0] if i + 1 < len(back_peaks) else x + 260
        body.append(f'<path d="M{f(x)} {f(y + 2)} Q{f(x + (nx - x) * 0.3)} {f(y + 70)} {f(x + (nx - x) * 0.48)} {f(y + 150)} '
                    f'L{f(x + 26)} {f(y + 190)} Q{f(x + 6)} {f(y + 90)} {f(x)} {f(y + 2)} Z" fill="#90A9C5" opacity="0.6"/>')
        if y < 500:
            body.append(f'<path d="M{f(x - 34)} {f(y + 34)} Q{f(x - 12)} {f(y + 4)} {f(x)} {f(y + 1)} '
                        f'Q{f(x + 14)} {f(y + 4)} {f(x + 40)} {f(y + 38)} L{f(x + 22)} {f(y + 30)} L{f(x + 8)} {f(y + 44)} '
                        f'L{f(x - 8)} {f(y + 30)} L{f(x - 20)} {f(y + 42)} Z" fill="#E6EEF6"/>')
    for i, (x, y) in enumerate(front_peaks):
        nx = front_peaks[i + 1][0] if i + 1 < len(front_peaks) else x + 260
        body.append(f'<path d="M{f(x)} {f(y + 2)} Q{f(x + (nx - x) * 0.3)} {f(y + 60)} {f(x + (nx - x) * 0.45)} {f(y + 140)} '
                    f'L{f(x + 30)} {f(y + 200)} Q{f(x + 8)} {f(y + 90)} {f(x)} {f(y + 2)} Z" fill="#7891AF" opacity="0.5"/>')
    return svg(W, H, defs, body, "Uzak dağlar: göğe karışmış, soluk mavi. Paralaks 0,15.")


# ---------------------------------------------------------------- 3. Orta tepeler
def poplar(x, base, h, w, light, dark):
    leaf = (f'M{f(x)} {f(base - h)} C{f(x + w * 0.9)} {f(base - h * 0.7)} {f(x + w * 0.8)} {f(base - h * 0.15)} '
            f'{f(x)} {f(base - h * 0.08)} C{f(x - w * 0.8)} {f(base - h * 0.15)} {f(x - w * 0.9)} {f(base - h * 0.7)} '
            f'{f(x)} {f(base - h)} Z')
    shade = (f'M{f(x)} {f(base - h)} C{f(x + w * 0.9)} {f(base - h * 0.7)} {f(x + w * 0.8)} {f(base - h * 0.15)} '
             f'{f(x)} {f(base - h * 0.08)} C{f(x + w * 0.25)} {f(base - h * 0.4)} {f(x + w * 0.2)} {f(base - h * 0.75)} Z')
    trunk = f'<rect x="{f(x - 2.5)}" y="{f(base - h * 0.12)}" width="5" height="{f(h * 0.12)}" fill="{dark}"/>'
    return [trunk, f'<path d="{leaf}" fill="{light}"/>', f'<path d="{shade}" fill="{dark}"/>']


def yurt(x, base, r):
    felt = hazed("#EDE6D3", 0.2)
    felt_dark = hazed("#C9BFA6", 0.2)
    band = hazed("#B44A3A", 0.25)
    door = hazed("#5A3A22", 0.3)
    body = [
        f'<path d="M{f(x - r)} {f(base)} L{f(x - r)} {f(base - r * 0.55)} Q{f(x - r * 0.9)} {f(base - r * 1.15)} '
        f'{f(x)} {f(base - r * 1.25)} Q{f(x + r * 0.9)} {f(base - r * 1.15)} {f(x + r)} {f(base - r * 0.55)} '
        f'L{f(x + r)} {f(base)} Z" fill="{felt}"/>',
        f'<path d="M{f(x + r * 0.15)} {f(base - r * 1.22)} Q{f(x + r * 0.85)} {f(base - r * 1.1)} {f(x + r)} {f(base - r * 0.55)} '
        f'L{f(x + r)} {f(base)} L{f(x + r * 0.35)} {f(base)} Z" fill="{felt_dark}" opacity="0.7"/>',
        f'<path d="M{f(x - r)} {f(base - r * 0.62)} L{f(x + r)} {f(base - r * 0.62)} L{f(x + r)} {f(base - r * 0.5)} '
        f'L{f(x - r)} {f(base - r * 0.5)} Z" fill="{band}"/>',
        f'<path d="M{f(x - r * 0.18)} {f(base)} L{f(x - r * 0.18)} {f(base - r * 0.42)} L{f(x + r * 0.18)} '
        f'{f(base - r * 0.42)} L{f(x + r * 0.18)} {f(base)} Z" fill="{door}"/>',
        f'<circle cx="{f(x)}" cy="{f(base - r * 1.25)}" r="{f(r * 0.1)}" fill="{band}"/>',
    ]
    return body


def fortress(x, base):
    stone = hazed("#9AA3AD", 0.25)
    lit = hazed("#B7BEC6", 0.25)
    dark = hazed("#7C8794", 0.25)
    roof = hazed("#8A4A3A", 0.35)
    b = []
    # Sur duvarı
    b.append(f'<path d="M{x - 150} {base} L{x - 150} {base - 46} L{x + 150} {base - 52} L{x + 150} {base} Z" fill="{stone}"/>')
    for i in range(12):
        cx = x - 146 + i * 25
        b.append(f'<rect x="{cx}" y="{f(base - 58 - i * 0.5)}" width="13" height="12" fill="{stone}"/>')
    # Kuleler: aydınlık sol yüz, gölgeli sağ yüz
    for tx, th, tw in [(-150, 96, 44), (-30, 128, 52), (150, 102, 44)]:
        cx = x + tx
        b.append(f'<rect x="{cx - tw / 2}" y="{base - th}" width="{tw}" height="{th}" fill="{lit}"/>')
        b.append(f'<rect x="{cx}" y="{base - th}" width="{tw / 2}" height="{th}" fill="{dark}"/>')
        b.append(f'<path d="M{cx - tw / 2 - 5} {base - th} L{cx} {base - th - tw * 0.95} L{cx + tw / 2 + 5} {base - th} Z" fill="{roof}"/>')
        b.append(f'<rect x="{cx - 4}" y="{base - th + 22}" width="8" height="14" rx="4" fill="{dark}"/>')
    return b


def mid():
    rng = random.Random(11)
    defs = [
        linear("tepe1", 0, 600, 0, 860, [(0, hazed("#B9B356", 0.35)), (1, hazed("#9AA04A", 0.3))]),
        linear("tepe2", 0, 650, 0, 880, [(0, hazed("#A6B04E", 0.25)), (1, hazed("#86983F", 0.22))]),
    ]
    body = []
    r1 = [(-40, 690), (300, 650), (620, 676), (900, 640), (1250, 668), (1580, 628), (1900, 618), (2250, 662), (2600, 640)]
    body.append(f'<path d="{hill_shape(r1, 1080)}" fill="url(#tepe1)"/>')
    # Uzak kale (orta katmanın üstünde, bir tepe sırtında)
    body += fortress(1900, 626)
    # Kavak sıraları
    light, dark = hazed("#5E8A45", 0.35), hazed("#3F6A36", 0.35)
    for i, x in enumerate(range(1060, 1430, 34)):
        h = 70 + rng.random() * 26
        body += poplar(x, 672 - (x - 1060) * 0.05 + rng.random() * 4, h, 15, light, dark)
    for x in range(140, 360, 30):
        h = 60 + rng.random() * 20
        body += poplar(x, 664 + rng.random() * 4, h, 13, light, dark)
    r2 = [(-40, 742), (260, 712), (560, 730), (880, 700), (1180, 724), (1500, 706), (1820, 734), (2150, 708), (2600, 726)]
    body.append(f'<path d="{hill_shape(r2, 1080)}" fill="url(#tepe2)"/>')
    mb = smooth_path(r2) + " L" + smooth_path([(x, y + 9) for x, y in reversed(r2)])[1:] + " Z"
    body.append(f'<path d="{mb}" fill="{hazed("#C9CC7A", 0.3)}" opacity="0.6"/>')
    # Oba: keçe çadırlar
    for x, r in [(560, 30), (640, 36), (722, 28), (1610, 26)]:
        base = 731 if x < 1000 else 712
        body += yurt(x, base, r)
    # Kurgan (yığma tepe) ve kıyıda aydınlık sırt
    body.append(f'<path d="M2060 716 Q2140 664 2230 714 Z" fill="{hazed("#A7A955", 0.25)}"/>')
    return svg(W, H, defs, body, "Orta tepeler: kavak sıraları, uzak kale, oba. Paralaks 0,35.")


# ---------------------------------------------------------------- 4. Yakın tepeler
def tree(x, base, s, rng):
    trunk = "#6E4B2A"
    trunk_dark = "#4A3019"
    b = [f'<path d="M{f(x - 7 * s)} {f(base)} L{f(x - 4 * s)} {f(base - 70 * s)} L{f(x + 5 * s)} {f(base - 70 * s)} '
         f'L{f(x + 8 * s)} {f(base)} Z" fill="{trunk}"/>',
         f'<path d="M{f(x + 1 * s)} {f(base)} L{f(x + 1 * s)} {f(base - 70 * s)} L{f(x + 5 * s)} {f(base - 70 * s)} '
         f'L{f(x + 8 * s)} {f(base)} Z" fill="{trunk_dark}"/>']
    crowns = [(-40, -110, 62, 50), (36, -118, 58, 48), (-4, -160, 66, 54), (-58, -150, 42, 36), (52, -158, 40, 34)]
    # Önce gölge tonu, sonra orta, en son ışık (sol üst)
    for (dx, dy, rx, ry) in crowns:
        b.append(f'<path d="{blob(x + dx * s + 6 * s, base + dy * s + 8 * s, rx * s, ry * s, 9, rng, 0.12)}" fill="#2F5E2A"/>')
    for (dx, dy, rx, ry) in crowns:
        b.append(f'<path d="{blob(x + dx * s, base + dy * s, rx * s * 0.92, ry * s * 0.9, 9, rng, 0.12)}" fill="#4C8A3A"/>')
    for (dx, dy, rx, ry) in crowns[:3]:
        b.append(f'<path d="{blob(x + dx * s - 14 * s, base + dy * s - 14 * s, rx * s * 0.5, ry * s * 0.42, 8, rng, 0.15)}" '
                 f'fill="#7DB246"/>')
    return b


def balbal(x, base):
    stone, lit, dark = "#A39E92", "#BDB8AC", "#7D776C"
    return [
        f'<path d="M{x - 26} {base} L{x - 24} {base - 92} Q{x - 22} {base - 128} {x} {base - 130} '
        f'Q{x + 22} {base - 128} {x + 24} {base - 92} L{x + 26} {base} Z" fill="{stone}"/>',
        f'<path d="M{x - 24} {base - 92} Q{x - 22} {base - 128} {x} {base - 130} L{x - 4} {base - 60} L{x - 25} {base - 30} Z" '
        f'fill="{lit}" opacity="0.6"/>',
        f'<path d="M{x + 6} {base - 128} Q{x + 22} {base - 126} {x + 24} {base - 92} L{x + 26} {base} L{x + 10} {base} Z" '
        f'fill="{dark}" opacity="0.55"/>',
        # Oyma yüz ve kollar: kaş, burun, bıyık, kadeh tutan eller
        f'<path d="M{x - 14} {base - 104} Q{x - 7} {base - 109} {x - 1} {base - 104} M{x + 3} {base - 104} '
        f'Q{x + 9} {base - 109} {x + 15} {base - 104}" fill="none" stroke="{dark}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M{x + 1} {base - 102} L{x + 1} {base - 90} M{x - 9} {base - 84} Q{x + 1} {base - 90} {x + 11} {base - 84}" '
        f'fill="none" stroke="{dark}" stroke-width="2.5" stroke-linecap="round"/>',
        f'<path d="M{x - 18} {base - 66} Q{x - 6} {base - 54} {x + 2} {base - 60} M{x + 18} {base - 70} Q{x + 10} {base - 56} {x + 2} {base - 60}" '
        f'fill="none" stroke="{dark}" stroke-width="3" stroke-linecap="round"/>',
    ]


def near():
    rng = random.Random(21)
    defs = [
        linear("yakin", 0, 700, 0, 900, [(0, "#93BE4F"), (1, "#6B9F3E")]),
        linear("yakin2", 0, 730, 0, 900, [(0, "#86B548"), (1, "#5E9A3A")]),
    ]
    body = []
    r = [(-40, 770), (220, 735), (520, 760), (800, 744), (1060, 772), (1320, 742), (1640, 768), (1960, 738), (2300, 762), (2600, 748)]
    body.append(f'<path d="{hill_shape(r, 1080)}" fill="url(#yakin)"/>')
    # Sırtta güneşe bakan açık bir bant (kontur değil, ışık)
    band = smooth_path(r) + " L" + smooth_path([(x, y + 14) for x, y in reversed(r)])[1:] + " Z"
    body.append(f'<path d="{band}" fill="#B5D66A" opacity="0.55"/>')
    r2 = [(-40, 800), (400, 788), (900, 806), (1400, 790), (1900, 808), (2600, 792)]
    body.append(f'<path d="{hill_shape(r2, 1080)}" fill="url(#yakin2)"/>')
    band2 = smooth_path(r2) + " L" + smooth_path([(x, y + 10) for x, y in reversed(r2)])[1:] + " Z"
    body.append(f'<path d="{band2}" fill="#A6CC5E" opacity="0.5"/>')
    for x, base, s in [(150, 742, 1.0), (300, 752, 0.75), (2230, 752, 1.1), (2390, 760, 0.8), (1720, 770, 0.7)]:
        body += tree(x, base, s, rng)
    body.append('<g transform="translate(1460 784) scale(0.72) translate(-1460 -784)">' + ''.join(balbal(1460, 784)) + '</g>')
    return svg(W, H, defs, body, "Yakın tepeler: meşeler ve bir balbal taşı. Paralaks 0,65.")


# ---------------------------------------------------------------- 5. Savaş zemini
def ground():
    rng = random.Random(31)
    defs = [
        linear("zemin", 0, 780, 0, 1080, [(0, "#8FB84E"), (0.45, "#6A9E3F"), (1, "#3F7430")]),
        linear("yol", 0, 790, 0, 1080, [(0, "#CDB27A"), (1, "#B89463")]),
    ]
    body = []
    edge = [(-40, 812), (300, 800), (700, 816), (1100, 804), (1500, 818), (1900, 802), (2300, 814), (2600, 806)]
    body.append(f'<path d="{hill_shape(edge, 1080)}" fill="url(#zemin)"/>')
    # Lekeler: açık çimen, koyu çimen, kuru ot
    for _ in range(26):
        x = rng.uniform(0, W)
        y = rng.uniform(840, 1060)
        depth = (y - 800) / 280
        rx = rng.uniform(120, 260) * (0.6 + depth)
        ry = rx * rng.uniform(0.18, 0.28)
        kind = rng.random()
        if kind < 0.4:
            c, a = "#9BC75A", 0.45
        elif kind < 0.75:
            c, a = "#4E8A36", 0.45
        else:
            c, a = "#B8A23C", 0.35 * (1 - depth * 0.5)
        body.append(f'<path d="{blob(x, y, rx, ry, 10, rng, 0.22)}" fill="{c}" opacity="{a:.2f}"/>')
    # Yol: soldan aşağıdan ufka kıvrılan toprak yol
    road_l = [(380, 1100), (560, 1000), (820, 930), (1120, 880), (1460, 846), (1800, 826), (2120, 812)]
    road_r = [(2160, 813), (1840, 830), (1520, 856), (1220, 900), (960, 960), (760, 1040), (640, 1100)]
    d = smooth_path(road_l) + " L" + " ".join(f"{f(x)} {f(y)}" for x, y in road_r[:1]) + " " + smooth_path(road_r)[1:] + " Z"
    body.append(f'<path d="{d}" fill="url(#yol)"/>')
    # Yolun sağ kenarı gölgeli, tekerlek izleri
    body.append(f'<path d="{smooth_path(road_r)}" fill="none" stroke="#9C7C4E" stroke-width="5" opacity="0.6"/>')
    ruts = [(520, 1060), (720, 975), (1000, 910), (1330, 864), (1680, 836), (2000, 819)]
    body.append(f'<path d="{smooth_path(ruts)}" fill="none" stroke="#A88A57" stroke-width="4" opacity="0.55" stroke-linecap="round"/>')
    ruts2 = [(600, 1070), (800, 985), (1080, 918), (1400, 869), (1730, 839), (2040, 821)]
    body.append(f'<path d="{smooth_path(ruts2)}" fill="none" stroke="#A88A57" stroke-width="3" opacity="0.45" stroke-linecap="round"/>')
    # Taşlar
    for _ in range(14):
        x = rng.uniform(0, W)
        y = rng.uniform(850, 1060)
        s = 0.5 + (y - 830) / 230
        body.append(f'<ellipse cx="{f(x + 3 * s)}" cy="{f(y + 4 * s)}" rx="{f(13 * s)}" ry="{f(4 * s)}" fill="#2F5A26" opacity="0.35"/>')
        body.append(f'<path d="M{f(x - 12 * s)} {f(y + 3 * s)} Q{f(x - 10 * s)} {f(y - 8 * s)} {f(x)} {f(y - 9 * s)} '
                    f'Q{f(x + 11 * s)} {f(y - 8 * s)} {f(x + 12 * s)} {f(y + 3 * s)} Z" fill="#A39E92"/>')
        body.append(f'<path d="M{f(x + 1 * s)} {f(y - 9 * s)} Q{f(x + 11 * s)} {f(y - 8 * s)} {f(x + 12 * s)} {f(y + 3 * s)} '
                    f'L{f(x + 2 * s)} {f(y + 3 * s)} Z" fill="#7D776C" opacity="0.7"/>')
    # Çimen öbekleri (küçük, uzakta daha küçük)
    for _ in range(40):
        x = rng.uniform(0, W)
        y = rng.uniform(830, 1070)
        s = 0.35 + (y - 820) / 300
        c = rng.choice(["#4E8A36", "#3B6E2C", "#7DB246"])
        blades = []
        for k in range(5):
            bx = x + (k - 2) * 5 * s
            tip = (bx + (k - 2) * 4 * s + rng.uniform(-2, 2) * s, y - rng.uniform(14, 24) * s)
            blades.append(f'M{f(bx - 2.5 * s)} {f(y)} Q{f(bx - 1 * s)} {f(y - 8 * s)} {f(tip[0])} {f(tip[1])} '
                          f'Q{f(bx + 1 * s)} {f(y - 8 * s)} {f(bx + 2.5 * s)} {f(y)} Z')
        body.append(f'<path d="{" ".join(blades)}" fill="{c}"/>')
    return svg(W, H, defs, body, "Savaş zemini: lekeli çayır, toprak yol, taşlar. Paralaks 1.")


# ---------------------------------------------------------------- 6. Ön plan
def tuft(x, y, s, rng, colors):
    out = []
    for layer, c in enumerate(colors):
        blades = []
        for k in range(9):
            bx = x + (k - 4) * 9 * s + rng.uniform(-3, 3) * s
            h = rng.uniform(60, 120) * s * (1 - layer * 0.15)
            lean = (k - 4) * 6 * s + rng.uniform(-8, 8) * s
            blades.append(f'M{f(bx - 6 * s)} {f(y)} Q{f(bx - 2 * s)} {f(y - h * 0.55)} {f(bx + lean)} {f(y - h)} '
                          f'Q{f(bx + 3 * s)} {f(y - h * 0.5)} {f(bx + 6 * s)} {f(y)} Z')
        out.append(f'<path d="{" ".join(blades)}" fill="{c}"/>')
    return out


def front():
    rng = random.Random(41)
    defs = []
    body = []
    for x, y, s in [(360, 1090, 1.3), (470, 1100, 1.0), (260, 1095, 0.9), (2200, 1092, 1.25), (2320, 1100, 1.0),
                    (2090, 1100, 0.85)]:
        body += tuft(x, y, s, rng, ["#24461F", "#3B6E2C", "#5E9A3A"])
    # Çalı: koyu yuvarlak yapraklar, üstünde ışık
    for (cx, cy, r) in [(330, 1050, 70), (400, 1030, 60), (290, 1020, 48)]:
        body.append(f'<path d="{blob(cx + 6, cy + 8, r, r * 0.8, 10, rng, 0.12)}" fill="#1F3D1B"/>')
        body.append(f'<path d="{blob(cx, cy, r * 0.9, r * 0.72, 10, rng, 0.12)}" fill="#2F5A26"/>')
        body.append(f'<path d="{blob(cx - r * 0.3, cy - r * 0.3, r * 0.42, r * 0.3, 8, rng, 0.15)}" fill="#4C8A3A"/>')
    # Çiçekler
    for _ in range(9):
        x = rng.choice([rng.uniform(200, 520), rng.uniform(2060, 2380)])
        y = rng.uniform(990, 1050)
        c = rng.choice(["#C8372D", "#F2C744", "#C8372D"])
        body.append(f'<path d="M{f(x)} {f(y + 40)} Q{f(x - 4)} {f(y + 20)} {f(x)} {f(y)}" fill="none" stroke="#2F5A26" stroke-width="3"/>')
        for k in range(5):
            a = k * math.tau / 5
            body.append(f'<circle cx="{f(x + math.cos(a) * 6)}" cy="{f(y + math.sin(a) * 6)}" r="5" fill="{c}"/>')
        body.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.5" fill="#F7E7A0"/>')
    return svg(W, H, defs, body, "Ön plan: köşelerde uzun çimen, çalı ve çiçekler. Paralaks 1,3.")


LAYERS = [("1-gok.svg", sky), ("2-uzak.svg", far), ("3-orta.svg", mid), ("4-yakin.svg", near),
          ("5-zemin.svg", ground), ("6-on.svg", front)]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in LAYERS:
        write(name, fn())
    # Önizleme: bütün katmanlar kamera sıfırdayken (x = -320)
    parts = []
    for name, _ in LAYERS:
        with open(os.path.join(OUT, name)) as fh:
            s = fh.read()
        inner = s.split("<defs>", 1)[1]
        defs, body = inner.split("</defs>", 1)
        body = body.rsplit("</svg>", 1)[0]
        prefix = name.split("-")[0]
        defs = defs.replace('id="', f'id="k{prefix}')
        body = body.replace('url(#', f'url(#k{prefix}')
        parts.append(f'<defs>{defs}</defs><g transform="translate(-320 0)">{body}</g>')
    with open(sys.argv[2], "w") as fh:
        fh.write('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
                 + "".join(parts) + "</svg>")
