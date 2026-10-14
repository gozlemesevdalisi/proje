"""Sert kenarlı (cel) vektör çizim yardımcıları: dış hatsız, düz renk + sert gölge şekilleri."""
import colorsys
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f, mix  # noqa: E402


def hexrgb(c):
    return [int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def rgbhex(r, g, b):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02X}" for v in (r, g, b))


def tone(c, dv=0.0, ds=0.0, dh=0.0):
    """Rengin parlaklığını (dv), doygunluğunu (ds) ve tonunu (dh) değiştirir."""
    h, s, v = colorsys.rgb_to_hsv(*hexrgb(c))
    return rgbhex(*colorsys.hsv_to_rgb((h + dh) % 1.0, max(0, min(1, s + ds)), max(0, min(1, v + dv))))


def dark(c, k=0.22):
    """Sert gölge tonu: koyu, biraz daha doygun, tonu sıcağa (kırmızıya) kayık."""
    return tone(c, -k, 0.08, -0.012)


def light(c, k=0.12):
    """Işık tonu: açık, biraz daha az doygun."""
    return tone(c, k, -0.08, 0.008)


def P(points, close=True):
    """Köşeli çokgen yolu."""
    d = f"M{f(points[0][0])} {f(points[0][1])} " + " ".join(f"L{f(x)} {f(y)}" for x, y in points[1:])
    return d + (" Z" if close else "")


def Q(*segs):
    """Karışık yol: ("M",x,y) ("L",x,y) ("Q",cx,cy,x,y) ("C",c1x,c1y,c2x,c2y,x,y)."""
    out = []
    for s in segs:
        out.append(s[0] + " ".join(f(v) for v in s[1:]))
    return " ".join(out) + " Z"


def fill(d, color, opacity=None):
    o = "" if opacity is None else f' opacity="{opacity}"'
    return f'<path d="{d}" fill="{color}"{o}/>'


def taper(p0, p1, w0, w1, bulge=0.0, bulge_at=0.4, cut0=0.0, cut1=0.0):
    """İki eklem arasında sivrilen, köşeli uzuv (dörtgen + hafif kas kavisi).

    `bulge`: dış kenardaki kas çıkıntısı (sola doğru normal yönünde pozitif).
    `cut0`/`cut1`: uçların eğik kesimi (yen ve paça gibi)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    a0 = (p0[0] + nx * w0 / 2 + ux * cut0, p0[1] + ny * w0 / 2 + uy * cut0)
    b0 = (p0[0] - nx * w0 / 2 - ux * cut0, p0[1] - ny * w0 / 2 - uy * cut0)
    a1 = (p1[0] + nx * w1 / 2 + ux * cut1, p1[1] + ny * w1 / 2 + uy * cut1)
    b1 = (p1[0] - nx * w1 / 2 - ux * cut1, p1[1] - ny * w1 / 2 - uy * cut1)
    wm = (w0 + w1) / 4
    m = (p0[0] + dx * bulge_at, p0[1] + dy * bulge_at)
    ca = (m[0] + nx * (wm + max(bulge, 0) * 2), m[1] + ny * (wm + max(bulge, 0) * 2))
    cb = (m[0] - nx * (wm + max(-bulge, 0) * 2 + abs(bulge) * 0.6), m[1] - ny * (wm + max(-bulge, 0) * 2 + abs(bulge) * 0.6))
    return (f"M{f(a0[0])} {f(a0[1])} Q{f(ca[0])} {f(ca[1])} {f(a1[0])} {f(a1[1])} "
            f"L{f(b1[0])} {f(b1[1])} Q{f(cb[0])} {f(cb[1])} {f(b0[0])} {f(b0[1])} Z")


def taper_shadow(p0, p1, w0, w1, frac=0.42, side=-1, bulge=0.0, bulge_at=0.4, cut0=0.0, cut1=0.0):
    """Uzvun ışıktan uzak yanındaki sert kenarlı gölge şeridi (genişliğin `frac` kadarı).

    `side`=-1: normalin ters yanı (ışık sol üstten geldiği için genellikle sağ/alt yan)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy * side, ux * side
    e0 = (p0[0] + nx * w0 / 2 + ux * cut0 * side, p0[1] + ny * w0 / 2 + uy * cut0 * side)
    e1 = (p1[0] + nx * w1 / 2 + ux * cut1 * side, p1[1] + ny * w1 / 2 + uy * cut1 * side)
    i0 = (p0[0] + nx * w0 * (0.5 - frac), p0[1] + ny * w0 * (0.5 - frac))
    i1 = (p1[0] + nx * w1 * (0.5 - frac), p1[1] + ny * w1 * (0.5 - frac))
    m = (p0[0] + dx * bulge_at, p0[1] + dy * bulge_at)
    wm = (w0 + w1) / 4 + abs(bulge) * 2
    ce = (m[0] + nx * wm, m[1] + ny * wm)
    ci = (m[0] + nx * ((w0 + w1) / 2 * (0.5 - frac) + 2), m[1] + ny * ((w0 + w1) / 2 * (0.5 - frac) + 2))
    return (f"M{f(i0[0])} {f(i0[1])} Q{f(ci[0])} {f(ci[1])} {f(i1[0])} {f(i1[1])} "
            f"L{f(e1[0])} {f(e1[1])} Q{f(ce[0])} {f(ce[1])} {f(e0[0])} {f(e0[1])} Z")


def group(id_, items, comment=None):
    c = f"<!-- {comment} -->" if comment else ""
    return f'<g id="{id_}">{c}' + "".join(items) + "</g>"


class Defs:
    def __init__(self, prefix):
        self.items = []
        self.prefix = prefix
        self.n = 0

    def lin(self, x1, y1, x2, y2, stops):
        self.n += 1
        gid = f"{self.prefix}{self.n}"
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
                    for o, c, a in [(st + (1,))[:3] for st in stops])
        self.items.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" '
                          f'x2="{f(x2)}" y2="{f(y2)}">{s}</linearGradient>')
        return f"url(#{gid})"

    def rad(self, cx, cy, r, stops):
        self.n += 1
        gid = f"{self.prefix}{self.n}"
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
                    for o, c, a in [(st + (1,))[:3] for st in stops])
        self.items.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" '
                          f'r="{f(r)}">{s}</radialGradient>')
        return f"url(#{gid})"

    def subtle(self, base, x1, y1, x2, y2, k=0.05):
        """Çok hafif hacim degradesi (esin kaynağındaki gibi; ton farkı küçük)."""
        return self.lin(x1, y1, x2, y2, [(0, tone(base, k, -0.03)), (1, tone(base, -k, 0.03))])


def S(points, sharp=(), closed=True, tension=1.0):
    """Noktalardan akıcı eğriyle geçen yol; `sharp` içindeki sıralarda sivri köşe yapar.

    Esin kaynağındaki gibi: hatlar eğri ve akıcı, kenarlar keskin; köşeler yalnızca istenen yerde."""
    n = len(points)
    sharp = set(i % n for i in sharp)

    def tangent(i):
        if i in sharp or (not closed and (i == 0 or i == n - 1)):
            return (0.0, 0.0)
        p0 = points[(i - 1) % n]
        p2 = points[(i + 1) % n]
        return ((p2[0] - p0[0]) / 6 * tension, (p2[1] - p0[1]) / 6 * tension)

    d = [f"M{f(points[0][0])} {f(points[0][1])}"]
    segs = n if closed else n - 1
    for i in range(segs):
        a = points[i]
        b = points[(i + 1) % n]
        ta = tangent(i)
        tb = tangent((i + 1) % n)
        c1 = (a[0] + ta[0], a[1] + ta[1])
        c2 = (b[0] - tb[0], b[1] - tb[1])
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(b[0])} {f(b[1])}")
    if closed:
        d.append("Z")
    return " ".join(d)
