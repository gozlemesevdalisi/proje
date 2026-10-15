"""Örnek kahraman: bozkır beyi (seçim ekranı ölçeğinde büyük resim).

Kurallar docs/SANAT.md'den: kontur yok; ten düz; kumaşta keskin kenarlı tek gölge şekli ve hafif
2 duraklı degrade; çelik ortadan bölünmüş iki ton; baş 64 birim, boy 7,3 baş; omuz baş
kütlesinin ~3,3 katı; ön kol ve yumruk yüz genişliğine yakın; A duruşu, pala 36° çapraz.

Çalıştır: python3 tools/art/ciz_kahraman.py  →  content/art/samples/characters/hero.svg
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cizim import KOK, Cizim, ara, ayna, daire, egri, uzuv  # noqa: E402

GEN, YUK = 400, 520
YER = 500  # ayak tabanı
c = Cizim(GEN, YUK, "kh")


def ok_tuyleri():
    """Sırttaki sadaktan omzun üstünde görünen oklar (siluette sağ çıkıntı)."""
    with c.grup("quiver"):
        # Sadak sırtta çapraz durur; omzun üstünde yalnızca ağzı ve okları görünür
        c.sekil(egri([(252, 128), (262, 84), (290, 90), (282, 132)], sivri=(0, 1, 2, 3)), c.yatay(256, 290, "deri-açık", "deri"))
        c.sekil(egri([(261, 88), (263, 80), (292, 86), (290, 94)], sivri=(0, 1, 2, 3)), "altın")
        c.sekil(egri([(278, 84), (292, 86), (290, 94), (276, 92)], sivri=(0, 1, 2, 3)), "altın-hardal")
        for x, y, renk, golge in [(266, 44, "kırmızı", "kırmızı-koyu"), (282, 40, "beyaz", "gri-açık"), (276, 52, "kırmızı", "kırmızı-koyu")]:
            # Ok gövdesi ve iki yapraklı sivri tüy
            c.sekil(egri([(x + 2, y + 40), (x + 5, y + 40), (x + 5, y + 8), (x + 2, y + 8)], sivri=(0, 1, 2, 3)), "sap")
            c.sekil(egri([(x + 3.5, y), (x + 10, y + 12), (x + 9, y + 28), (x + 3.5, y + 22)], sivri=(0, 2, 3)), renk)
            c.sekil(egri([(x + 3.5, y), (x - 3, y + 12), (x - 2, y + 28), (x + 3.5, y + 22)], sivri=(0, 2, 3)), golge)


def orgu():
    """Sol omuzdan göğse düşen siyah örgü; ucunda kırmızı bağ."""
    with c.grup("braid"):
        bogum = [(180, 92), (176, 106), (173, 120), (171, 134), (170, 148)]
        for i, (x, y) in enumerate(bogum):
            c.sekil(egri([(x, y - 9), (x + 7, y - 2), (x + 1, y + 8), (x - 6, y + 1)], sivri=(0, 2)), "siyah-ışık")
            c.sekil(egri([(x - 1, y - 7), (x + 4, y - 3), (x, y + 2), (x - 4, y - 1)], sivri=(0, 2)), "kömür")
        c.sekil(egri([(165, 154), (175, 153), (174, 161), (166, 162)], sivri=(0, 1, 2, 3)), "kırmızı")
        c.sekil(egri([(166, 161), (173, 160), (176, 178), (170, 172), (163, 180)], sivri=(0, 1, 2, 3, 4)), "siyah-ışık")


def bacaklar():
    with c.grup("legs"):
        sol_salvar = [(150, 296), (198, 296), (196, 352), (188, 398), (178, 406), (158, 408), (138, 402), (138, 352)]
        sol_golge = [(178, 296), (198, 296), (196, 352), (188, 398), (178, 406), (172, 404), (180, 352)]
        sol_cizme = [(140, 398), (180, 398), (183, 430), (176, 466), (178, 486), (176, 500), (122, 500),
                     (108, 494), (100, 480), (118, 482), (136, 474), (142, 462), (135, 428)]
        sol_cizme_golge = [(166, 400), (180, 398), (183, 430), (176, 466), (178, 486), (168, 486), (168, 462), (172, 430)]
        for yon in (-1, 1):
            def m(pts):
                return pts if yon < 0 else ayna(pts, 200)
            # Şalvar: bol; diz altında çizmenin üstüne sarkar
            c.sekil(egri(m(sol_salvar), sivri=(0, 1, 3, 6) if yon < 0 else (1, 4, 6, 7)), "kırmızı")
            c.sekil(egri(sol_golge if yon < 0 else [(222, 296), (238, 296), (258, 352), (262, 402), (244, 408), (246, 360)],
                         sivri=(0, 1, 3, 4) if yon < 0 else (0, 1, 3, 4)), "kırmızı-koyu")
            # Çizme: baldırda şişkin, bilekte daralır; burnu dışa bakar ve hafif kalkıktır
            bx0, bx1 = (140, 183) if yon < 0 else (217, 260)
            c.sekil(egri(m(sol_cizme), sivri=(0, 1, 5, 6, 8, 9) if yon < 0 else (3, 4, 6, 7, 11, 12)),
                    c.yatay(bx0, bx1, "deri-açık", "deri"))
            if yon < 0:
                c.sekil(egri(sol_cizme_golge, sivri=(0, 1, 4, 5)), "deri-gölge")
            else:
                c.sekil(egri([(244, 400), (260, 398), (265, 430), (258, 466), (264, 474), (282, 482), (300, 480), (292, 494), (278, 500), (252, 494), (252, 462), (254, 430)],
                             sivri=(0, 1, 6, 9)), "deri-gölge")
            # Taban ve konç ağzı
            taban = [(118, 497), (178, 497), (176, 501), (120, 501)]
            c.sekil(egri(m(taban), sivri=(0, 1, 2, 3)), "kahve-siyah")
            agiz = [(137, 394), (183, 394), (183, 406), (137, 406)]
            c.sekil(egri(m(agiz), sivri=(0, 1, 2, 3)), "kahve-koyu")


def etek():
    """Kaftanın eteği: önden yırtmaçlı iki parça; altın etek ve yırtmaç şeridi."""
    with c.grup("skirt"):
        sol = [(150, 226), (198, 232), (196, 300, 0.6), (192, 362), (150, 360), (122, 352), (136, 290)]
        sag = ayna(sol, 200)
        renk = c.dikey(226, 362, "gök-ufuk", "gök")
        c.sekil(egri(sol, sivri=(0, 1, 3, 5)), renk)
        c.sekil(egri(sag, sivri=(1, 3, 5, 6)), renk)
        # Gölge: sağ parçanın dış yanı ve sol parçanın yırtmaç kenarı
        c.sekil(egri([(232, 234), (250, 228), (264, 290), (278, 352), (246, 358), (244, 300, 0.6)], sivri=(0, 1, 3, 4)), "mavi")
        c.sekil(egri([(176, 234), (198, 232), (196, 300, 0.6), (192, 362), (178, 361), (182, 300, 0.6)], sivri=(0, 1, 3, 4)), "mavi")
        # Altın şeritler: etek ucu ve yırtmaç kenarı
        for yon in (-1, 1):
            if yon < 0:
                serit = [(122, 352), (150, 360), (192, 362), (192, 352), (152, 350), (125, 342)]
                kenar = [(198, 232), (196, 300, 0.6), (192, 362), (184, 362), (188, 300, 0.6), (190, 233)]
            else:
                serit = ayna([(122, 352), (150, 360), (192, 362), (192, 352), (152, 350), (125, 342)], 200)
                kenar = ayna([(198, 232), (196, 300, 0.6), (192, 362), (184, 362), (188, 300, 0.6), (190, 233)], 200)
            c.sekil(egri(serit, sivri=(0, 2, 3, 5)), "altın")
            c.sekil(egri(kenar, sivri=(0, 2, 3, 5)), "altın")
        # Sağdaki altın şeritlerin gölge yanı
        c.sekil(egri([(244, 352), (275, 343), (278, 352), (246, 360)], sivri=(0, 1, 2, 3)), "altın-hardal")


def govde():
    """Kaftanın üst bedeni: geniş göğüs, altın yaka şeridi çapraz iner."""
    with c.grup("torso"):
        beden = [(186, 108), (154, 114), (130, 126), (140, 168), (153, 214), (200, 220, 0.5), (247, 214), (260, 168), (270, 126), (246, 114), (214, 108)]
        c.sekil(egri(beden, sivri=(0, 2, 4, 6, 8, 10)), c.dikey(108, 220, "gök-ufuk", "gök"))
        # Gölge: sağ yan (ışık sol üstten) ve göğüs altı
        c.sekil(egri([(236, 118), (262, 122), (270, 126), (262, 168), (252, 214), (226, 216), (238, 168)], sivri=(0, 2, 4, 5)), "mavi")
        # Boyun açıklığı: ten (göğüs üstü), yakanın altında
        c.sekil(egri([(186, 108), (214, 108), (208, 128), (198, 136)], sivri=(0, 1, 3)), "ten-sarı")
        # Altın yaka: boynun sağından bele çapraz (kalın şerit, kontrast ΔL ≈ 50)
        c.sekil(egri([(212, 106), (222, 108), (196, 168, 0.6), (162, 216), (148, 214), (186, 160, 0.6), (204, 120)], sivri=(0, 1, 3, 4)), "altın")
        c.sekil(egri([(216, 108), (222, 108), (196, 168, 0.6), (162, 216), (155, 215), (190, 164, 0.6)], sivri=(0, 1, 3, 4)), "altın-hardal")
        # Dik yaka (boyun çevresi), sol yanı altın
        c.sekil(egri([(184, 104), (190, 112), (198, 136), (186, 112, 0.5), (180, 110)], sivri=(0, 2, 4)), "altın")


def kusak():
    """Kırmızı kuşak; sol kalçada düğüm ve sivri uçlu sarkan iki uç."""
    with c.grup("sash"):
        c.sekil(egri([(146, 208), (200, 214, 0.5), (254, 208), (256, 232), (200, 238, 0.5), (146, 232)], sivri=(0, 2, 3, 5)), "kırmızı")
        c.sekil(egri([(214, 236), (254, 230), (256, 232), (254, 210), (240, 212)], sivri=(0, 1, 2, 3)), "kırmızı-koyu")
        c.sekil(egri([(146, 230), (200, 236, 0.5), (254, 230), (254, 234), (200, 240, 0.5), (146, 234)], sivri=(0, 2, 3, 5)), "kırmızı-koyu")
        # Sarkan uçlar
        c.sekil(egri([(156, 226), (168, 228), (172, 270), (176, 302), (166, 292), (160, 300), (158, 262)], sivri=(0, 1, 3, 4, 5)), "kırmızı")
        c.sekil(egri([(168, 228), (172, 270), (176, 302), (170, 296), (166, 262)], sivri=(0, 2, 3)), "kırmızı-koyu")
        c.sekil(egri([(146, 228), (156, 230), (152, 268), (148, 288), (142, 280), (136, 288), (140, 258)], sivri=(0, 1, 3, 4, 5)), "kırmızı")
        # Düğüm
        c.sekil(egri([(150, 214), (166, 212), (170, 230), (160, 238), (148, 232)], sivri=(1, 3)), "kırmızı")
        c.sekil(egri([(162, 216), (166, 212), (170, 230), (160, 238), (164, 226)], sivri=(1, 3)), "kırmızı-koyu")


def kol_sag():
    """İzleyicinin solundaki kol: kolluk mavi, altın yen; iri ön kol; yumruk palayı tutar."""
    with c.grup("arm-front"):
        # Ön kol (ten, düz): dirsekten bileğe daralır, pazı yanı şişkin
        on = uzuv((118, 196), (106, 256), 34, 23, sis=5, sis_yer=0.35, sis_yan=1, w_orta=38)
        c.sekil(egri(on, sivri=(0, 2, 3, 5)), "ten-sarı")
        c.sekil(egri([(122, 204), (134, 200), (126, 236), (117, 256), (114, 250), (122, 230)], sivri=(0, 1, 3, 4)), "ten-sarı-gölge")
        # Bilek sargısı
        c.sekil(egri([(93, 246), (118, 248), (118, 258), (93, 256)], sivri=(0, 1, 2, 3)), "kahve-koyu")
        # Kolluk (üst kol): omuz başı yuvarlak ve yüksek
        ust = [(156, 114), (132, 115), (112, 127), (101, 150), (100, 174), (104, 190), (102, 200), (138, 204), (143, 180), (150, 150)]
        c.sekil(egri(ust, sivri=(6, 7)), c.dikey(114, 204, "gök-ufuk", "gök"))
        # Gölge: pazının iç yanı (gövdeye bakan)
        c.sekil(egri([(128, 150), (143, 140), (150, 150), (143, 180), (138, 204), (124, 202), (130, 176)], sivri=(4, 5)), "mavi")
        c.sekil(egri([(102, 188), (142, 192), (140, 207), (101, 202)], sivri=(0, 1, 2, 3)), "altın")
        c.sekil(egri([(126, 190), (142, 192), (140, 207), (124, 205)], sivri=(0, 1, 2, 3)), "altın-hardal")


def bicak(taban, uc, w, yelman=1.25, egim=10):
    """Pala ağzı: tabandan uca eğri; sırt ve ağız noktaları. Uca yakın yelman genişler."""
    import math
    dx, dy = uc[0] - taban[0], uc[1] - taban[1]
    uz = math.hypot(dx, dy)
    ux, uy = dx / uz, dy / uz
    nx, ny = -uy, ux  # sol yan (sırt)
    sirt, agiz = [], []
    for t, gen in [(0, w), (0.3, w * 0.95), (0.6, w * 0.9), (0.8, w * yelman), (0.9, w * yelman * 0.8)]:
        bel = math.sin(t * math.pi) * egim
        cx, cy = taban[0] + dx * t + nx * bel, taban[1] + dy * t + ny * bel
        sirt.append((cx + nx * gen * 0.45, cy + ny * gen * 0.45))
        agiz.append((cx - nx * gen * 0.55, cy - ny * gen * 0.55))
    orta = [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(sirt, agiz)]
    return sirt, agiz, orta


def pala():
    """Pala: kabza yumruğun içinden geçer, ağız sol üste ~30° çapraz uzanır; çelik iki ton."""
    with c.grup("sabre"):
        c.sekil(egri([(98, 246), (106, 244), (116, 292), (108, 294)], sivri=(0, 1, 2, 3)), "kahve-koyu")
        c.sekil(daire(113, 296, 6), "altın")
        c.sekil(daire(111, 294, 2.2), "altın-parlama")
        taban, uc = (101, 238), (30, 100)
        sirt, agiz, orta = bicak(taban, uc, 13)
        tum = sirt + [uc] + list(reversed(agiz))
        c.sekil(egri(tum, sivri=(0, 5, 10)), "çelik-lavanta")
        koyu = orta + [uc] + list(reversed(agiz))
        c.sekil(egri(koyu, sivri=(0, 5, 10)), "gri")
        # Parlama: sırt boyunca ince beyaz şerit
        par = [ara(s, o, 0.25) for s, o in zip(sirt[1:4], orta[1:4])]
        c.sekil(egri(sirt[1:4] + list(reversed(par)), sivri=(0, 2, 3, 5)), "beyaz")
        # Balçak: kısa, uçları topuzlu
        c.sekil(egri([(88, 250), (104, 240), (116, 234), (118, 241), (106, 248), (90, 257)], sivri=(0, 2, 3, 5)), "altın")
        c.sekil(egri([(104, 246), (116, 239), (118, 241), (106, 249)], sivri=(0, 1, 2, 3)), "altın-hardal")
        c.sekil(daire(88, 254, 4.5), "altın")
        c.sekil(daire(118, 237, 4.5), "altın-hardal")


def yumruk():
    with c.grup("fist-front"):
        # İri yumruk (yüz genişliğinin ~0,9'u): parmaklar kabzayı sarar, başparmak üstte
        c.sekil(egri([(87, 256), (110, 250), (124, 257), (126, 276), (118, 288), (96, 289), (86, 280), (84, 266)], sivri=(1, 5)), "ten-sarı")
        # Bükülmüş parmaklar: tek gölge şekli, araları sivri çentikli
        c.sekil(egri([(112, 262), (125, 262), (126, 276), (118, 288), (96, 289), (100, 284), (104, 280), (108, 284),
                      (110, 278), (114, 281), (114, 272)], sivri=(0, 3, 4, 5, 6, 7, 8, 9, 10)), "ten-sarı-gölge")
        # Başparmak kabzanın üstünden geçer
        c.sekil(egri([(86, 258), (104, 251), (112, 256), (108, 262), (92, 266)], sivri=(1, 3)), "ten-sarı")
        c.sekil(egri([(92, 266), (108, 262), (112, 256), (111, 263), (96, 269)], sivri=(1, 2, 4)), "ten-sarı-gölge")


def kol_sol():
    """İzleyicinin sağındaki kol: kalkanı tutar; ön kol kalkanın arkasında kalır."""
    with c.grup("arm-back"):
        ust = ayna([(156, 114), (132, 115), (112, 127), (101, 150), (100, 174), (104, 190), (102, 200), (138, 204), (143, 180), (150, 150)], 200)
        c.sekil(egri(ust, sivri=(2, 3)), "gök")
        c.sekil(egri([(262, 128), (288, 128), (300, 150), (300, 176), (296, 190), (298, 200), (276, 202), (280, 170)], sivri=(5, 6)), "mavi")
        c.sekil(egri(ayna([(102, 188), (142, 192), (140, 207), (101, 202)], 200), sivri=(0, 1, 2, 3)), "altın-hardal")
        on = uzuv((284, 202), (270, 236), 32, 26, w_orta=34)
        c.sekil(egri(on, sivri=(0, 2, 3, 5)), "ten-sarı-gölge")


def kalkan():
    """Yuvarlak kalkan: kırmızı yüz, altın kenar, altın koçboynuzu damgası, çelik göbek."""
    with c.grup("shield"):
        cx, cy, rr = 270, 268, 54
        c.sekil(daire(cx, cy, rr), c.dikey(cy - rr, cy + rr, "altın", "altın-hardal"))
        c.sekil(daire(cx, cy, rr - 7), c.dikey(cy - rr, cy + rr, "kırmızı-degrade-açık", "kırmızı-degrade-koyu"))
        # Keskin kenarlı gölge hilali (sağ alt)
        c.sekil(egri([(cx + 38, cy - 27), (cx + 47, cy + 2), (cx + 36, cy + 30), (cx + 2, cy + 47), (cx - 26, cy + 41),
                      (cx + 4, cy + 36), (cx + 30, cy + 16)], sivri=(0, 4)), "kırmızı-gölge")
        # Koçboynuzu damgası: ortada çelik göbek, üstünde iki yana kıvrılan boynuzlar, altında sap
        for yon in (-1, 1):
            boynuz = [(cx + yon * 4, cy - 8), (cx + yon * 10, cy - 26), (cx + yon * 26, cy - 30), (cx + yon * 35, cy - 16),
                      (cx + yon * 28, cy - 2), (cx + yon * 18, cy - 8), (cx + yon * 24, cy - 14), (cx + yon * 26, cy - 20),
                      (cx + yon * 18, cy - 21), (cx + yon * 12, cy - 6)]
            if yon > 0:
                boynuz = list(reversed(boynuz))
            c.sekil(egri(boynuz, sivri=(0, 5) if yon < 0 else (4, 9)), "altın")
        c.sekil(egri([(cx - 5, cy + 4), (cx + 5, cy + 4), (cx + 6, cy + 32), (cx, cy + 40), (cx - 6, cy + 32)], sivri=(0, 1, 3)), "altın")
        c.sekil(egri([(cx + 1, cy + 4), (cx + 5, cy + 4), (cx + 6, cy + 32), (cx, cy + 40), (cx + 2, cy + 30)], sivri=(0, 1, 3)), "altın-hardal")
        c.sekil(daire(cx, cy, 11), c.yatay(cx - 11, cx + 11, "çelik-parlak", "çelik-gölge"))
        c.sekil(daire(cx - 3.5, cy - 3.5, 3.2), "beyaz")


def bas():
    """Baş: 64 birim (33–97). Yüz düz ten; burun tek gölge; göz akı ve iris; çatık kaş; pala bıyık."""
    with c.grup("head"):
        # Boyun: kalın; çene altında gölge
        c.sekil(egri([(185, 86), (215, 86), (216, 112), (200, 116, 0.5), (184, 112)], sivri=(0, 1, 2, 4)), "ten-sarı")
        c.sekil(egri([(186, 92), (214, 92), (215, 104), (200, 100, 0.5), (186, 104)], sivri=(0, 1, 2, 4)), "ten-sarı-gölge")
        # Kulaklar
        for yon in (-1, 1):
            k = [(200 + yon * 20, 62), (200 + yon * 26, 64), (200 + yon * 25, 76), (200 + yon * 20, 80)]
            c.sekil(egri(k if yon < 0 else list(reversed(k)), sivri=(0, 3) if yon < 0 else (0, 3)), "ten-sarı" if yon < 0 else "ten-sarı-gölge")
        # Yüz: köşeli çene
        yuz = [(179, 46), (178, 70), (183, 87), (191, 97), (209, 97), (217, 87), (222, 70), (221, 46)]
        c.sekil(egri(yuz, sivri=(0, 2, 3, 4, 5, 7)), "ten-sarı")
        # Favori (saç) kulak önünde
        for yon in (-1, 1):
            fav = [(200 + yon * 22, 46), (200 + yon * 17, 46), (200 + yon * 18, 66), (200 + yon * 21, 74)]
            c.sekil(egri(fav if yon < 0 else list(reversed(fav)), sivri=(0, 1, 3) if yon < 0 else (0, 2, 3)), "siyah-ışık")
        # Burun: sağ yanda tek gölge şekli
        c.sekil(egri([(201, 64), (204, 74), (207, 79), (202, 81.5), (197, 80), (201, 77)], sivri=(0, 2, 3, 4)), "ten-sarı-gölge")
        # Gözler: badem göz akı, iris üst kapağa değer, koyu üst kapak
        for ex in (190.5, 209.5):
            c.sekil(egri([(ex - 5.5, 66.5), (ex, 63.2), (ex + 5.5, 66), (ex, 68.6)], sivri=(0, 2)), "beyaz")
            c.sekil(daire(ex + 0.6, 65.8, 2.3), "siyah")
            c.sekil(egri([(ex - 6.5, 66.8), (ex - 1, 62.4), (ex + 6, 65.4), (ex + 5.4, 66.2), (ex, 63.8), (ex - 5.4, 67)], sivri=(0, 2, 3, 5)), "siyah-ışık")
        # Kaşlar: kalın, buruna doğru iner (kararlı bakış)
        c.sekil(egri([(182, 58.5), (190, 56), (198, 59.5), (197, 62), (190, 59.6), (183, 61)], sivri=(0, 2, 3, 5)), "siyah-ışık")
        c.sekil(egri([(218, 58.5), (210, 56), (202, 59.5), (203, 62), (210, 59.6), (217, 61)], sivri=(0, 2, 3, 5)), "siyah-ışık")
        # Ağız: küçük dudak şekli
        c.sekil(egri([(194.5, 87), (205.5, 87), (204, 91), (196, 91)], sivri=(0, 1)), "dudak-açık")
        # Pala bıyık: üst dudağı örter, iki yanda çenenin altına kadar sarkar (imza öğe)
        sol = [(200, 80.8), (192, 81.2), (186.5, 84), (183.5, 90), (183, 98), (187, 92), (190.5, 87.6), (195, 86.4), (200, 87)]
        c.sekil(egri(sol, sivri=(0, 4, 8)), "siyah-ışık")
        c.sekil(egri(ayna(sol, 200), sivri=(0, 4, 8)), "siyah-ışık")


def bork():
    """Börk: beyaz keçe külah, kahverengi kürk kenar, altın tepe topuzu."""
    with c.grup("hat"):
        kulah = [(177, 46), (181, 26), (196, 14), (216, 9), (219, 22), (224, 46)]
        c.sekil(egri(kulah, sivri=(0, 3, 5)), c.yatay(177, 224, "beyaz", "beyaz-gölge"))
        c.sekil(egri([(204, 16), (216, 9), (219, 22), (224, 46), (209, 46), (210, 28)], sivri=(1, 3, 4)), "gri-açık")
        c.sekil(daire(216, 9, 4.5), "altın")
        c.sekil(daire(214.6, 7.6, 1.6), "altın-parlama")
        # Kürk kenar: dolgun bir bant; alt kenarı sığ tümsekli, sağ yanı gölgede
        kurk = [(171, 47), (178, 39), (200, 36, 0.6), (222, 39), (229, 47), (229, 53), (220, 56), (210, 54), (200, 56),
                (190, 54), (180, 56), (171, 53)]
        c.sekil(egri(kurk, sivri=(0, 4, 5, 7, 9, 11)), "kahve")
        c.sekil(egri([(210, 38), (222, 39), (229, 47), (229, 53), (220, 56), (210, 54), (212, 47)], sivri=(2, 3, 5)), "kahve-koyu")
        c.sekil(egri([(175, 45), (182, 40), (194, 39), (186, 45), (177, 49)], sivri=(1, 2)), "deri-açık")


def ciz():
    ok_tuyleri()
    orgu_arka = False
    bacaklar()
    etek()
    kol_sol()
    govde()
    kusak()
    if not orgu_arka:
        orgu()
    kol_sag()
    pala()
    yumruk()
    kalkan()
    bas()
    bork()
    yol = os.path.join(KOK, "content", "art", "samples", "characters", "hero.svg")
    c.kaydet(yol, "Örnek kahraman: bozkır beyi. tools/art/ciz_kahraman.py ile üretildi; elle düzenleme.")
    return yol


if __name__ == "__main__":
    print(ciz())
