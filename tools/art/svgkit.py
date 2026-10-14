"""SVG üretmek için küçük yardımcılar (yalnızca çizim hazırlarken kullanılır)."""
import math
import random


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def smooth_path(points, closed=False, tension=1.0):
    """Noktalardan geçen yumuşak eğri (Catmull-Rom → kübik Bézier)."""
    pts = points
    n = len(pts)
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    rng = range(n if closed else n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    if closed:
        d.append("Z")
    return " ".join(d)


def ridge(x0, x1, base, amp, n, rng, sharp=0.0):
    """Tepe sırtı için noktalar."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = base - amp * (0.5 + 0.5 * math.sin(i * 1.7 + rng.random() * 2)) * (0.6 + 0.4 * rng.random())
        pts.append((x, y))
    return pts


def hill_shape(ridge_pts, bottom):
    """Sırttan aşağı inen kapalı tepe şekli."""
    x0 = ridge_pts[0][0]
    x1 = ridge_pts[-1][0]
    d = smooth_path(ridge_pts)
    return d + f" L{f(x1)} {f(bottom)} L{f(x0)} {f(bottom)} Z"


def blob(cx, cy, rx, ry, n, rng, jitter=0.18):
    """Düzensiz, yumuşak kenarlı leke."""
    pts = []
    phase = rng.random() * math.tau
    for i in range(n):
        a = phase + math.tau * i / n
        r = 1 + (rng.random() - 0.5) * 2 * jitter
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return smooth_path(pts, closed=True)


def linear(id_, x1, y1, x2, y2, stops):
    s = "".join(
        f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
        for o, c, a in [(st + (1,))[:3] for st in stops]
    )
    return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" '
            f'x2="{f(x2)}" y2="{f(y2)}">{s}</linearGradient>')


def radial(id_, cx, cy, r, stops, fx=None, fy=None):
    s = "".join(
        f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else "") + "/>"
        for o, c, a in [(st + (1,))[:3] for st in stops]
    )
    foc = "" if fx is None else f' fx="{f(fx)}" fy="{f(fy)}"'
    return (f'<radialGradient id="{id_}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" '
            f'r="{f(r)}"{foc}>{s}</radialGradient>')


def svg(w, h, defs, body, comment):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'  <!-- {comment} -->\n  <defs>\n    ' + "\n    ".join(defs) + "\n  </defs>\n  "
            + "\n  ".join(body) + "\n</svg>\n")
