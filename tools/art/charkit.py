"""Karakter çizimi yardımcıları: uzuv şekilleri, gölge degradeleri, dış hat rengi."""
import colorsys
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import f, mix  # noqa: E402

OUTLINE_W = 4.0
DETAIL_W = 2.0
LIGHT = "#FFF6D2"
SHADOW = "#2A2A55"


def hexrgb(c):
    return [int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def rgbhex(r, g, b):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02X}" for v in (r, g, b))


def ink(c, k=0.36):
    """Dış hat rengi: rengin koyulaştırılmış, tonu hafif kırmızıya kaymış hâli (siyah değil)."""
    h, s, v = colorsys.rgb_to_hsv(*hexrgb(c))
    h = (h - 0.02) % 1.0
    return rgbhex(*colorsys.hsv_to_rgb(h, min(1.0, s * 1.05 + 0.12), max(0.09, v * k)))


def lit(c, t=0.2):
    return mix(c, LIGHT, t)


def shade(c, t=0.28):
    return mix(c, SHADOW, t)


class Defs:
    def __init__(self, prefix):
        self.items = []
        self.prefix = prefix
        self.n = 0

    def _id(self):
        self.n += 1
        return f"{self.prefix}{self.n}"

    def lin(self, x1, y1, x2, y2, stops):
        gid = self._id()
        s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        self.items.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" '
                          f'x2="{f(x2)}" y2="{f(y2)}">{s}</linearGradient>')
        return f"url(#{gid})"

    def rad(self, cx, cy, r, stops, fx=None, fy=None):
        gid = self._id()
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
                    for o, c, a in [(st + (1,))[:3] for st in stops])
        foc = "" if fx is None else f' fx="{f(fx)}" fy="{f(fy)}"'
        self.items.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" '
                          f'r="{f(r)}"{foc}>{s}</radialGradient>')
        return f"url(#{gid})"

    def volume(self, base, x1, y1, x2, y2, light=0.22, dark=0.3):
        """Hacim degradesi: aydınlık uç (x1,y1) tarafında (sol üst), gölge (x2,y2) tarafında."""
        return self.lin(x1, y1, x2, y2, [(0, lit(base, light)), (0.45, base), (1, shade(base, dark))])

    def cylinder(self, base, p0, p1, width):
        """Silindir parçada (kol, bacak) enine degrade: ışık soldan üçte birde."""
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        if nx > 0:  # normal ışığa (sola) baksın
            nx, ny = -nx, -ny
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        h = width / 2
        return self.lin(mx + nx * h, my + ny * h, mx - nx * h, my - ny * h,
                        [(0, lit(base, 0.12)), (0.3, lit(base, 0.2)), (0.6, base), (1, shade(base, 0.32))])


def limb(p0, p1, w0, w1, bulge=0.0):
    """İki eklem arasında, uçları yuvarlak, sivrilen uzuv şekli."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    a0 = (p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2)
    a1 = (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2)
    b1 = (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2)
    b0 = (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    wm = (w0 + w1) / 4 + bulge
    ca = (mid[0] + nx * wm, mid[1] + ny * wm)
    cb = (mid[0] - nx * wm, mid[1] - ny * wm)
    k = 0.55

    def cap(pa, pb, center, r, ux_, uy_):
        c1 = (pa[0] + ux_ * r * k * 1.8, pa[1] + uy_ * r * k * 1.8)
        c2 = (pb[0] + ux_ * r * k * 1.8, pb[1] + uy_ * r * k * 1.8)
        return f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(pb[0])} {f(pb[1])}"

    return (f"M{f(a0[0])} {f(a0[1])} Q{f(ca[0])} {f(ca[1])} {f(a1[0])} {f(a1[1])} "
            + cap(a1, b1, p1, w1 / 2, ux, uy)
            + f" Q{f(cb[0])} {f(cb[1])} {f(b0[0])} {f(b0[1])} "
            + cap(b0, a0, p0, w0 / 2, -ux, -uy) + " Z")


def path(d, fill, stroke=None, width=OUTLINE_W, extra=""):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'
    return s + f"{extra}/>"


def line(d, color, width=DETAIL_W, opacity=None):
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"{o}/>')


def group(id_, items, comment=None):
    c = f"<!-- {comment} -->" if comment else ""
    return f'<g id="{id_}">{c}' + "".join(items) + "</g>"
