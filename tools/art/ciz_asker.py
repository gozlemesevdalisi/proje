"""Örnek asker: mızrakçı (savaş kuklası). İki kişi: gazi ve genç.

Savaş kuklası kuralları (docs/SANAT.md): her parça 2 düz ton (ana renk ve keskin kenarlı gölge);
degrade yalnızca metalde; kontur yok. Baş 64 birim, boy 7 baş; omuz baş kütlesinin ~2,9 katı;
mızrak iki elle ~32° çapraz; kalkan sırtta (siluette sağ çıkıntı); A duruşu.

Çalıştır: python3 tools/art/ciz_asker.py  →  content/art/samples/characters/soldier-{1,2}.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cizim import KOK, Cizim, ayna, daire, egri, elips  # noqa: E402

GEN, YUK = 300, 520
YER = 500
X = 150  # gövde ekseni

KISILER = {
    "soldier-1": {  # gazi: kısa sakallı, açık tenli, miğferinde kırmızı püskül
        "ten": "ten", "ten-gölge": "ten-gölge", "kıl": "siyah-ışık", "sakal": True, "püskül": True,
        "kalkan": "kırmızı", "kalkan-gölge": "kırmızı-koyu", "damga": "altın", "kaş": 14,
    },
    "soldier-2": {  # genç: sakalsız, kızıl bıyıklı, buğday tenli
        "ten": "ten-buğday", "ten-gölge": "ten-gölge", "kıl": "saç-kızıl-gölge", "sakal": False, "püskül": False,
        "kalkan": "beyaz", "kalkan-gölge": "gri-açık", "damga": "kırmızı", "kaş": 8,
    },
}


def ciz(ad, k):
    c = Cizim(GEN, YUK, "s" + ad[-1])

    # --- Sırttaki kalkan (sol omzun arkasından taşar) -------------------------------------
    with c.grup("shield"):
        cx, cy, rr = 214, 168, 46
        c.sekil(daire(cx, cy, rr), "kahve")
        c.sekil(daire(cx, cy, rr - 6), k["kalkan"])
        c.sekil(egri([(cx + 30, cy - 24), (cx + 38, cy + 2), (cx + 28, cy + 26), (cx + 4, cy + 38), (cx - 18, cy + 34),
                      (cx + 6, cy + 28), (cx + 26, cy + 10)], sivri=(0, 4)), k["kalkan-gölge"])
        for yon in (-1, 1):
            b = [(cx + yon * 3, cy - 4), (cx + yon * 8, cy - 18), (cx + yon * 20, cy - 21), (cx + yon * 26, cy - 11),
                 (cx + yon * 20, cy), (cx + yon * 13, cy - 5), (cx + yon * 18, cy - 10), (cx + yon * 19, cy - 14),
                 (cx + yon * 13, cy - 15), (cx + yon * 9, cy - 3)]
            c.sekil(egri(b if yon < 0 else list(reversed(b)), sivri=(0, 5) if yon < 0 else (4, 9)), k["damga"])
        c.sekil(daire(cx, cy + 2, 7), c.yatay(cx - 7, cx + 7, "çelik-parlak", "çelik-gölge"))

    # --- Bacaklar: beyaz şalvar, iki tonlu sargı bantları, sivri burunlu çarık ---------------
    with c.grup("legs"):
        for yon in (-1, 1):
            def m(p):
                return p if yon < 0 else ayna(p, X)
            salvar = [(104, 290), (148, 290), (144, 350), (136, 404), (106, 406), (96, 350)]
            c.sekil(egri(m(salvar), sivri=(0, 1, 3, 4) if yon < 0 else (1, 2, 4, 5)), "kırmızı-koyu")
            golge = [(128, 292), (148, 290), (144, 350), (136, 404), (124, 404), (132, 350)]
            c.sekil(egri(m(golge), sivri=(0, 1, 3, 4) if yon < 0 else (1, 2, 4, 5)), "kırmızı-gölge")
            # Baldır ve sargılar
            baldir = [(106, 400), (136, 400), (136, 430), (130, 476), (110, 476), (104, 430)]
            c.sekil(egri(m(baldir), sivri=(0, 1, 3, 4) if yon < 0 else (1, 2, 4, 5)), "deri-açık")
            for i, y in enumerate((410, 432, 454)):
                bant = [(104, y), (137, y - 4), (136, y + 10), (105, y + 14)]
                c.sekil(egri(m(bant), sivri=(0, 1, 2, 3)), "kahve")
            c.sekil(egri(m([(124, 402), (136, 400), (136, 430), (130, 476), (122, 476), (128, 430)]), sivri=(0, 1, 3, 4) if yon < 0 else (1, 2, 4, 5)), "deri-gölge")
            # Çarık: burnu dışa bakar
            ayak = [(108, 472), (134, 472), (136, 490), (134, YER), (90, YER), (80, 492), (98, 484)]
            c.sekil(egri(m(ayak), sivri=(0, 1, 3, 4, 5) if yon < 0 else (1, 2, 3, 5, 6)), "kahve")
            c.sekil(egri(m([(118, 474), (132, 472), (136, 490), (132, YER), (112, YER), (120, 488)]), sivri=(0, 1, 3, 4) if yon < 0 else (1, 2, 4, 5)), "kahve-koyu")

    # --- Gövde: mavi gömlek (kısa kollu), altın yaka ve etek şeridi, deri kemer ----------
    with c.grup("torso"):
        govde = [(136, 128), (104, 132), (80, 146), (76, 174), (100, 178), (106, 240), (98, 300), (96, 322), (150, 328, 0.5),
                 (204, 322), (202, 300), (194, 240), (200, 178), (224, 174), (220, 146), (196, 132), (164, 128)]
        c.sekil(egri(govde, sivri=(0, 3, 4, 5, 7, 9, 11, 12, 13, 16)), "gök")
        c.sekil(egri([(176, 132), (196, 132), (220, 146), (224, 174), (200, 178), (194, 240), (202, 300), (204, 322), (180, 326),
                      (176, 260), (184, 200)], sivri=(0, 3, 4, 5, 7, 8)), "mavi")
        # Etek şeridi ve yırtmaç
        c.sekil(egri([(96, 310), (150, 316, 0.5), (204, 310), (204, 322), (150, 328, 0.5), (96, 322)], sivri=(0, 2, 3, 5)), "altın")
        c.sekil(egri([(176, 314), (204, 310), (204, 322), (178, 326)], sivri=(0, 1, 2, 3)), "altın-hardal")
        c.sekil(egri([(146, 262), (154, 262), (156, 324), (144, 324)], sivri=(0, 1, 2, 3)), "mavi")
        # Yaka: boyun çevresinde altın şerit, göğse inen kısa yarık
        c.sekil(egri([(132, 126), (168, 126), (162, 142), (150, 160), (138, 142)], sivri=(0, 1, 3)), "altın")
        c.sekil(egri([(140, 128), (160, 128), (156, 138), (150, 150), (144, 138)], sivri=(0, 1, 3)), k["ten"])
        # Kemer
        c.sekil(egri([(104, 236), (150, 242, 0.5), (196, 236), (196, 252), (150, 258, 0.5), (104, 252)], sivri=(0, 2, 3, 5)), "kahve-koyu")
        c.sekil(egri([(142, 240), (158, 240), (158, 256), (142, 256)], sivri=(0, 1, 2, 3)), "altın")

    # --- Kollar: beyaz gömlek kolu; her kol tek parça, dirsekte sivri kırılır -----------------
    with c.grup("arms"):
        # Arkadaki (izleyicinin sağı) kol: dirsek dışarıda, el göğüs hizasında mızrağı tutar
        c.sekil(egri([(196, 148), (222, 150), (236, 178), (238, 208), (226, 216), (196, 190), (184, 182), (190, 168),
                      (214, 182), (212, 168), (200, 160)], sivri=(3, 4, 6, 8)), "beyaz")
        c.sekil(egri([(226, 216), (196, 190), (184, 182), (186, 178), (200, 188), (238, 208)], sivri=(0, 2, 3, 5)), "gri-açık")
        c.sekil(egri([(214, 182), (212, 168), (222, 160), (232, 190), (226, 196)], sivri=(0, 4)), "gri-açık")
        # Öndeki (izleyicinin solu) kol: dirsek dışarıda, el kalça hizasında
        c.sekil(egri([(108, 148), (82, 150), (72, 180), (74, 220), (100, 260), (124, 262), (126, 246), (104, 216),
                      (108, 184), (112, 160)], sivri=(3, 5, 6, 7)), "beyaz")
        c.sekil(egri([(104, 216), (108, 184), (112, 160), (104, 160), (96, 190), (96, 222), (118, 250), (126, 246)],
                     sivri=(0, 2, 7)), "gri-açık")

        # Kısa kolluklar kolların üstüne biner; ağızlarında altın şerit
        c.sekil(egri([(110, 134), (84, 142), (72, 166), (72, 180), (104, 182), (110, 160)], sivri=(3, 4)), "gök")
        c.sekil(egri([(104, 150), (110, 160), (104, 182), (94, 181), (98, 160)], sivri=(2, 3)), "mavi")
        c.sekil(egri([(72, 172), (104, 176), (104, 184), (71, 181)], sivri=(0, 1, 2, 3)), "altın")
        c.sekil(egri([(190, 134), (216, 142), (228, 166), (230, 180), (198, 182), (190, 160)], sivri=(3, 4)), "mavi")
        c.sekil(egri([(198, 176), (230, 172), (231, 181), (198, 184)], sivri=(0, 1, 2, 3)), "altın-hardal")

    # --- Mızrak: dişbudak sap, yaprak biçimli çelik uç, kırmızı flama ------------------------
    with c.grup("spear"):
        a, b = (58, 360), (256, 40)
        import math
        dx, dy = b[0] - a[0], b[1] - a[1]
        uz = math.hypot(dx, dy)
        nx, ny = -dy / uz, dx / uz
        w = 3.2
        c.sekil(egri([(a[0] + nx * w, a[1] + ny * w), (b[0] + nx * w, b[1] + ny * w), (b[0] - nx * w, b[1] - ny * w),
                      (a[0] - nx * w, a[1] - ny * w)], sivri=(0, 1, 2, 3)), "sap")
        c.sekil(egri([(a[0], a[1]), (b[0], b[1]), (b[0] - nx * w, b[1] - ny * w), (a[0] - nx * w, a[1] - ny * w)], sivri=(0, 1, 2, 3)), "kahve")
        ux, uy = dx / uz, dy / uz
        uc = (b[0] + ux * 44, b[1] + uy * 44)
        gov = (b[0] + ux * 16, b[1] + uy * 16)
        sol = (gov[0] + nx * 9, gov[1] + ny * 9)
        sag = (gov[0] - nx * 9, gov[1] - ny * 9)
        c.sekil(egri([(b[0] + nx * 4, b[1] + ny * 4), sol, uc, sag, (b[0] - nx * 4, b[1] - ny * 4)], sivri=(0, 2, 4)),
                "çelik-lavanta")
        c.sekil(egri([b, uc, sag, (b[0] - nx * 4, b[1] - ny * 4)], sivri=(0, 1, 3)), "gri")
        # Flama: sapın altında iki dilli
        f0 = (b[0] - ux * 2, b[1] - uy * 2)
        f1 = (b[0] - ux * 30, b[1] - uy * 30)
        c.sekil(egri([f0, (f0[0] + 40, f0[1] + 10), (f0[0] + 30, f0[1] + 22), (f0[0] + 44, f0[1] + 34), f1],
                     sivri=(0, 1, 2, 3, 4)), "kırmızı")
        c.sekil(egri([(f0[0] + 18, f0[1] + 18), (f0[0] + 30, f0[1] + 22), (f0[0] + 44, f0[1] + 34), f1],
                     sivri=(0, 1, 2, 3)), "kırmızı-koyu")
        # Dip demiri
        c.sekil(egri([(a[0] + nx * 4, a[1] + ny * 4), (a[0] - nx * 4, a[1] - ny * 4), (a[0] - ux * 10, a[1] - uy * 10)], sivri=(0, 1, 2)), "çelik-gölge")

    # --- Eller: mızrağı saran iri yumruklar --------------------------------------------------
    with c.grup("hands"):
        for (hx, hy) in ((118, 256), (184, 176)):
            c.sekil(egri([(hx - 14, hy - 10), (hx + 10, hy - 14), (hx + 16, hy - 2), (hx + 12, hy + 12), (hx - 6, hy + 14),
                          (hx - 16, hy + 4)], sivri=(1, 4)), k["ten"])
            c.sekil(egri([(hx + 2, hy - 2), (hx + 16, hy - 2), (hx + 12, hy + 12), (hx - 6, hy + 14), (hx, hy + 6)],
                         sivri=(0, 3)), k["ten-gölge"])

    # --- Baş: miğfer, zırh perdesi, yüz ------------------------------------------------------
    with c.grup("head"):
        # Zırh perdesi: miğferin altından omuzlara iner (düz iki ton, örgü dokusu yok)
        c.sekil(egri([(124, 70), (176, 70), (182, 104), (186, 132), (166, 136), (150, 124), (134, 136), (114, 132), (118, 104)],
                     sivri=(0, 1, 3, 4, 6, 7)), "çelik-açık")
        c.sekil(egri([(160, 72), (176, 70), (182, 104), (186, 132), (166, 136), (162, 112)], sivri=(0, 1, 3, 4)), "çelik-gölge")
        # Yüz (miğfer kenarından çeneye); köşeli çene
        yuz = [(130, 70), (129, 92), (134, 106), (142, 116), (158, 116), (166, 106), (171, 92), (170, 70)]
        c.sekil(egri(yuz, sivri=(0, 2, 3, 4, 5, 7)), k["ten"])
        c.sekil(egri([(156, 80), (159, 92), (162, 97), (157, 99.5), (152, 98), (156, 95)], sivri=(0, 2, 3, 4)), k["ten-gölge"])
        for ex in (141, 159):
            c.sekil(egri([(ex - 5.5, 86.5), (ex, 83.2), (ex + 5.5, 86), (ex, 88.6)], sivri=(0, 2)), "beyaz")
            c.sekil(daire(ex + 0.6, 85.8, 2.3), "siyah")
            c.sekil(egri([(ex - 6.5, 86.8), (ex - 1, 82.4), (ex + 6, 85.4), (ex + 5.4, 86.2), (ex, 83.8), (ex - 5.4, 87)],
                         sivri=(0, 2, 3, 5)), "siyah-ışık")
        e = k["kaş"] / 10
        c.sekil(egri([(133, 78 - e), (141, 76.5 - e), (148, 80), (147, 82.4), (141, 79.6 - e), (134, 81 - e)], sivri=(0, 2, 3, 5)), k["kıl"])
        c.sekil(egri([(167, 78 - e), (159, 76.5 - e), (152, 80), (153, 82.4), (159, 79.6 - e), (166, 81 - e)], sivri=(0, 2, 3, 5)), k["kıl"])
        c.sekil(egri([(145, 106), (155, 106), (153.5, 109.5), (146.5, 109.5)], sivri=(0, 1)), "dudak-açık")
        if k["sakal"]:
            # Kısa, köşeli sakal ve bıyık
            c.sekil(egri([(130, 92), (136, 104), (144, 104.5), (150, 103), (156, 104.5), (164, 104), (170, 92), (170, 104),
                          (162, 118), (150, 122), (138, 118), (130, 104)], sivri=(0, 6, 7, 9, 11)), k["kıl"])
            c.sekil(egri([(143, 101), (150, 99.5), (157, 101), (160, 105), (150, 104), (140, 105)], sivri=(3, 5)), k["kıl"])
            c.sekil(egri([(145, 107), (155, 107), (153.5, 110), (146.5, 110)], sivri=(0, 1)), "dudak-açık")
        else:
            c.sekil(egri([(150, 100), (142, 101), (138, 106), (143, 104), (150, 103.5), (157, 104), (162, 106), (158, 101)],
                         sivri=(0, 2, 6)), k["kıl"])
        # Miğfer: sivri tepeli çelik; kenarında altın bant
        migfer = [(122, 72), (126, 50), (138, 38), (150, 26), (162, 38), (174, 50), (178, 72)]
        c.sekil(egri(migfer, sivri=(0, 3, 6)), c.yatay(122, 178, "çelik-parlak", "çelik-gölge"))
        c.sekil(egri([(150, 26), (162, 38), (174, 50), (178, 72), (160, 72), (158, 46)], sivri=(0, 3, 4)), "çelik-koyu")
        c.sekil(egri([(132, 46), (140, 38), (146, 34), (140, 48), (134, 62)], sivri=(2, 4)), "beyaz")
        c.sekil(egri([(120, 66), (150, 63, 0.5), (180, 66), (180, 75), (150, 72, 0.5), (120, 75)], sivri=(0, 2, 3, 5)), "altın")
        c.sekil(egri([(160, 64), (180, 66), (180, 75), (162, 73)], sivri=(0, 1, 2, 3)), "altın-hardal")
        if k["püskül"]:
            c.sekil(egri([(148, 28), (152, 28), (164, 6), (160, 16), (168, 12), (156, 30)], sivri=(0, 1, 2, 4, 5)), "kırmızı")
            c.sekil(egri([(152, 28), (164, 6), (160, 16), (168, 12), (156, 30)], sivri=(0, 1, 3, 4)), "kırmızı-koyu")
        c.sekil(daire(150, 26, 3.5), "altın")

    yol = os.path.join(KOK, "content", "art", "samples", "characters", f"{ad}.svg")
    c.kaydet(yol, f"Örnek asker ({ad}). tools/art/ciz_asker.py ile üretildi; elle düzenleme.")
    return yol


def golge():
    """Ayak altı gölgesi: düz, keskin kenarlı, yarı saydam siyah elips. Merkez (100, 20)."""
    c = Cizim(200, 40, "g")
    c.sekil(elips(100, 20, 100, 20), "siyah", saydam=0.35)
    yol = os.path.join(KOK, "content", "art", "samples", "shadow.svg")
    c.kaydet(yol, "Karakterlerin ayak altı gölgesi. tools/art/ciz_asker.py ile üretildi; elle düzenleme.")
    return yol


if __name__ == "__main__":
    for ad, k in KISILER.items():
        print(ciz(ad, k))
    print(golge())
