"""Denetim aracının birim testleri. SWF dosyası ve FFDec gerektirmez: girdiler elle kurulur.

Çalıştırma (depo kökünden):  python3 -m unittest discover -s araclar/aktar -p 'test_*.py'

`render_all`, `compare_shapes`, `compare_morphs`, `check_game` ve `main` motorun çizicisini, SWF'yi ve
yerel arşivi gerektirir; onları denetimin kendisi çalıştırır (`denetim.py --gorsel`).
"""
import base64
import hashlib
import io
import json
import os
import sys
import tempfile
import types
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import denetim  # noqa: E402


def el(xml):
    return ET.fromstring(xml)


def png_bytes(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


class XmlReadingTest(unittest.TestCase):
    def test_sound_info_keeps_only_flagged_fields_like_the_importer(self):
        self.assertEqual(denetim.xml_sound_info(None), {})
        plain = el('<soundInfo syncStop="false" syncNoMultiple="false" hasInPoint="false" hasOutPoint="false" '
                   'hasLoops="false" hasEnvelope="false" inPoint="0" outPoint="0" loopCount="0"/>')
        self.assertEqual(denetim.xml_sound_info(plain), {})
        full = el('<soundInfo syncStop="true" syncNoMultiple="true" hasInPoint="true" inPoint="441" '
                  'hasOutPoint="true" outPoint="8820" hasLoops="true" loopCount="3" hasEnvelope="true">'
                  '<envelopeRecords><item pos44="0" leftLevel="0" rightLevel="32768"/>'
                  '<item pos44="4410" leftLevel="32768" rightLevel="0"/></envelopeRecords></soundInfo>')
        self.assertEqual(denetim.xml_sound_info(full), {"stop": True, "no_multiple": True, "in": 441, "out": 8820,
                                                        "loops": 3, "envelope": [[0, 0, 32768], [4410, 32768, 0]]})

    def test_matrix_defaults_to_identity_and_divides_translation_by_twenty(self):
        self.assertEqual(denetim.xml_matrix(None), [1.0, 0.0, 0.0, 1.0, 0.0, 0.0])
        m = el('<matrix hasScale="true" scaleX="2.0" scaleY="0.5" hasRotate="true" rotateSkew0="0.25" '
               'rotateSkew1="-0.25" translateX="40" translateY="-30"/>')
        self.assertEqual(denetim.xml_matrix(m), [2.0, 0.25, -0.25, 0.5, 2.0, -1.5])
        only_move = el('<matrix hasScale="false" hasRotate="false" translateX="20" translateY="0"/>')
        self.assertEqual(denetim.xml_matrix(only_move), [1.0, 0.0, 0.0, 1.0, 1.0, 0.0])

    def test_colour_transform_scales_terms_and_ignores_alpha_without_it(self):
        self.assertEqual(denetim.xml_cxform(None), [[1.0] * 4, [0.0] * 4])
        c = el('<colorTransform type="CXFORMWITHALPHA" hasMultTerms="true" redMultTerm="128" greenMultTerm="256" '
               'blueMultTerm="0" alphaMultTerm="64" hasAddTerms="true" redAddTerm="255" greenAddTerm="0" '
               'blueAddTerm="0" alphaAddTerm="0"/>')
        self.assertEqual(denetim.xml_cxform(c), [[0.5, 1.0, 0.0, 0.25], [1.0, 0.0, 0.0, 0.0]])
        no_alpha = el('<colorTransform type="CXFORM" hasMultTerms="true" redMultTerm="256" greenMultTerm="256" '
                      'blueMultTerm="256" alphaMultTerm="0" hasAddTerms="false"/>')
        self.assertEqual(denetim.xml_cxform(no_alpha), [[1.0, 1.0, 1.0, 1.0], [0.0] * 4])

    def test_place_reads_only_flagged_fields(self):
        p = el('<item type="PlaceObject3Tag" depth="4" placeFlagMove="true" placeFlagHasCharacter="true" '
               'characterId="12" placeFlagHasRatio="true" ratio="65535" placeFlagHasName="true" name="kale" '
               'placeFlagHasClipDepth="true" clipDepth="9" placeFlagHasClipActions="true" '
               'placeFlagHasFilterList="true" placeFlagHasBlendMode="true" blendMode="3">'
               '<surfaceFilterList><item type="GLOWFILTER"/></surfaceFilterList></item>')
        self.assertEqual(denetim.xml_place(p), {"depth": 4, "move": True, "char": 12, "ratio": 1.0, "name": "kale",
                                                "clip": 9, "clip_actions": True, "filters": ["glow"],
                                                "blend": "multiply"})
        self.assertEqual(denetim.xml_place(el('<item depth="2"/>')), {"depth": 2})

    def test_timeline_splits_frames_and_keeps_labels_and_sounds(self):
        t = denetim.XmlTimeline()
        for x in ('<item type="PlaceObject2Tag" depth="1" placeFlagHasCharacter="true" characterId="5"/>',
                  '<item type="FrameLabelTag" name="giris"/>', '<item type="ShowFrameTag"/>',
                  '<item type="StartSoundTag" soundId="9"/>', '<item type="RemoveObject2Tag" depth="1"/>',
                  '<item type="ShowFrameTag"/>'):
            t.add(el(x))
        t.finish()
        self.assertEqual(t.frames, [[{"depth": 1, "char": 5}], [{"remove": 1}]])
        self.assertEqual(t.labels, {"giris": 0})
        self.assertEqual(t.sounds, {1: [{"id": 9}]})
        self.assertEqual(t.counts["ShowFrame"], 2)

    def test_dump_reads_characters_bounds_sounds_exports_and_root(self):
        xml = ('<swf><tags>'
               '<item type="DefineShapeTag" shapeId="5"><shapes/></item>'
               '<item type="DefineMorphShapeTag" characterId="6">'
               '<startBounds Xmin="-20" Ymin="-40" Xmax="20" Ymax="0"/>'
               '<endBounds Xmin="0" Ymin="0" Xmax="40" Ymax="60"/></item>'
               '<item type="DefineSoundTag" soundId="9" soundSampleCount="15763" soundData="0001fffb"/>'
               '<item type="DoActionTag"/>'
               '<item type="PlaceObject2Tag" depth="1" placeFlagHasCharacter="true" characterId="5"/>'
               '<item type="FrameLabelTag" name="giris"/>'
               '<item type="ShowFrameTag"/>'
               '<item type="ExportAssetsTag"><tags><item>5</item></tags><names><item>Kale</item></names></item>'
               '</tags></swf>')
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "swf.xml")
            with open(path, "w", encoding="utf-8") as f:
                f.write(xml)
            dump = denetim.XmlDump(path)
        self.assertEqual(dump.chars, {5: "shape", 6: "morph", 9: "sound"})
        self.assertEqual(dump.morph_bounds[6], {"start": [-1.0, -2.0, 1.0, 0.0], "end": [0.0, 0.0, 2.0, 3.0]})
        self.assertEqual(dump.sounds[9], b"\x00\x01\xff\xfb")
        self.assertEqual(dump.sound_samples[9], 15763)
        self.assertEqual(dump.exports, {"Kale": 5})
        self.assertEqual(dump.root.frames, [[{"depth": 1, "char": 5}]])
        self.assertEqual(dump.root.labels, {"giris": 0})
        self.assertEqual(dump.scripts["DoAction"], 1)
        self.assertEqual(dump.counts["DefineShape"], 1)
        self.assertEqual(dump.bitmap_fills, {})

    def test_text_records_read_style_and_glyphs(self):
        t = el('<item><textRecords><item styleFlagsHasFont="true" fontId="3" textHeight="240" '
               'styleFlagsHasColor="true" styleFlagsHasXOffset="true" xOffset="20" styleFlagsHasYOffset="false">'
               '<textColor red="255" green="0" blue="16"/><glyphEntries>'
               '<item glyphIndex="7" glyphAdvance="100"/></glyphEntries></item></textRecords></item>')
        self.assertEqual(denetim.text_records(t), [{"font": 3, "height": 12.0, "color": "#FF0010", "x": 1.0,
                                                    "glyphs": [[7, 5.0]]}])

    def test_button_record_lists_states_and_placement(self):
        r = el('<item buttonStateUp="true" buttonStateHitTest="true" characterId="8" placeDepth="2" '
               'buttonHasBlendMode="true" blendMode="8"/>')
        self.assertEqual(denetim.button_record(r), {"states": ["up", "hit"], "char": 8, "depth": 2,
                                                    "matrix": [1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                                                    "cxform": [[1.0] * 4, [0.0] * 4], "blend": "add"})


BITMAP_SHAPE = (
    '<item type="DefineShapeTag" shapeId="5"><shapes>'
    '<fillStyles><fillStyles>'
    '<item type="FILLSTYLE" fillStyleType="66" bitmapId="65535"><bitmapMatrix hasScale="false" '
    'hasRotate="false" translateX="0" translateY="0"/></item>'
    '<item type="FILLSTYLE" fillStyleType="64" bitmapId="7"><bitmapMatrix hasScale="true" scaleX="10" '
    'scaleY="20" hasRotate="true" rotateSkew0="0" rotateSkew1="-2" translateX="200" translateY="-40"/></item>'
    '<item type="FILLSTYLE" fillStyleType="0"/>'
    '</fillStyles></fillStyles>'
    '<shapeRecords>'
    '<item type="StyleChangeRecord" stateFillStyle1="true" fillStyle1="2" fillStyle0="1"/>'
    '<item type="StraightEdgeRecord"/>'
    '<item type="StyleChangeRecord" stateNewStyles="true" stateFillStyle0="true" fillStyle0="2" '
    'stateFillStyle1="true" fillStyle1="1">'
    '<fillStyles><fillStyles>'
    '<item type="FILLSTYLE" fillStyleType="0"/>'
    '<item type="FILLSTYLE" fillStyleType="67" bitmapId="8"><bitmapMatrix hasScale="false" hasRotate="false" '
    'translateX="20" translateY="20"/></item>'
    '</fillStyles></fillStyles></item>'
    '</shapeRecords></shapes></item>')


class BitmapFillTest(unittest.TestCase):
    def test_fill_style_items_reads_nested_array(self):
        self.assertEqual(len(denetim.fill_style_items(el(BITMAP_SHAPE).find("shapes"))), 3)
        self.assertEqual(denetim.fill_style_items(el("<item/>")), [])

    def test_only_bitmap_fills_used_by_edges_are_listed_in_matrix_pixels(self):
        # 65535 ("resim yok") birinci dizide durur ama hiçbir kenar kullanmaz; düz renk dolgusu resim değildir;
        # yeni stil dizisinden sonraki numaralar yeni diziyi gösterir.
        self.assertEqual(denetim.bitmap_fills(el(BITMAP_SHAPE)), [
            (7, [0.5, 0.0, -0.1, 1.0, 10.0, -2.0]),
            (8, [0.05, 0.0, 0.0, 0.05, 1.0, 1.0]),
        ])
        self.assertEqual(denetim.bitmap_fills(el('<item type="DefineShapeTag"/>')), [])

    def test_svg_patterns_read_matrix_and_image(self):
        svg = ('<svg><pattern id="P" patternTransform="matrix(0.5, 0.0, -0.1, 1.0, 10.0, -2.0)">'
               '<image xlink:href="data:image/PNG;base64,' + base64.b64encode(b"abc").decode() + '"/></pattern>'
               '<pattern id="Q"></pattern></svg>')
        self.assertEqual(denetim.svg_patterns(svg), [([0.5, 0.0, -0.1, 1.0, 10.0, -2.0], b"abc"),
                                                     ([1.0, 0.0, 0.0, 1.0, 0.0, 0.0], b"")])

    def test_image_difference_is_largest_channel_difference(self):
        a = Image.new("RGB", (2, 2), (10, 20, 30))
        b = a.copy()
        b.putpixel((1, 1), (13, 20, 30))
        self.assertEqual(denetim.image_difference(png_bytes(a), png_bytes(a)), 0)
        self.assertEqual(denetim.image_difference(png_bytes(a), png_bytes(b)), 3)
        self.assertIsNone(denetim.image_difference(png_bytes(a), png_bytes(Image.new("RGB", (3, 2)))))

    def test_bitmap_shape_problems_find_wrong_matrix_image_and_missing_shape(self):
        texture = Image.new("RGB", (2, 2), (200, 100, 50))
        other = Image.new("RGB", (2, 2), (0, 0, 0))
        m = [0.5, 0.0, -0.1, 1.0, 10.0, -2.0]

        def pattern(matrix, im):
            return (f'<pattern patternTransform="matrix({", ".join(map(str, matrix))})">'
                    f'<image xlink:href="data:image/PNG;base64,{base64.b64encode(png_bytes(im)).decode()}"/>'
                    '</pattern>')
        old_root = denetim.ROOT
        with tempfile.TemporaryDirectory() as td:
            denetim.ROOT = td
            try:
                base = os.path.join(td, "content", "feudalism", "t")
                os.makedirs(os.path.join(base, "shapes-bitmap"))
                os.makedirs(os.path.join(base, "images"))
                texture.save(os.path.join(base, "images", "7.png"))
                with open(os.path.join(base, "shapes-bitmap", "5.svg"), "w", encoding="utf-8") as f:
                    f.write("<svg>" + pattern(m, texture) + "</svg>")
                lib = {"excluded": {}, "bitmap_shapes": {"5": [0, 0]}, "images": {"7": "images/7.png"}}
                dump = types.SimpleNamespace(bitmap_fills={5: [(7, m)]})
                self.assertEqual(denetim.bitmap_shape_problems("t", lib, dump), [])
                # Aktarılmamış resim dolgulu şekil, uymayan matris, farklı resim
                dump.bitmap_fills[11] = [(7, m)]
                with open(os.path.join(base, "shapes-bitmap", "5.svg"), "w", encoding="utf-8") as f:
                    f.write("<svg>" + pattern([1, 0, 0, 1, 0, 0], texture) + pattern(m, other) + "</svg>")
                probs = denetim.bitmap_shape_problems("t", lib, dump)
            finally:
                denetim.ROOT = old_root
        self.assertEqual(len(probs), 3, probs)
        self.assertIn("şekil 11", probs[0])
        self.assertIn("desen 1: matrisi", probs[1])
        self.assertIn("desen 2: resmi", probs[2])


class ComparisonTest(unittest.TestCase):
    def test_plain_text_drops_style_blocks_and_keeps_escaped_brackets(self):
        formatted = '[font 1 height 20 color "#FF0000" name "a]b"]Kale [space 5]\\[1\\] kapısı'
        self.assertEqual(denetim.ffdec_plain_text(formatted), "Kale [1] kapısı")

    def test_xml_unescape_turns_backslash_codes_into_characters(self):
        self.assertEqual(denetim.xml_unescape("a\\rb\\nc\\td\\\\e\\x"), "a\rb\nc\td\\ex")

    def test_close_compares_numbers_with_tolerance_and_lists_by_item(self):
        self.assertTrue(denetim.close(1.0, 1.0005))
        self.assertFalse(denetim.close(1.0, 1.01))
        self.assertTrue(denetim.close([1, [2.0, 3]], [1.0, [2.0, 3.0]]))
        self.assertFalse(denetim.close([1, 2], [1]))
        self.assertTrue(denetim.close("a", "a"))
        self.assertFalse(denetim.close(True, 1.0))

    def test_normalize_ours_reduces_filters_to_types(self):
        self.assertEqual(denetim.normalize_ours({"depth": 1, "filters": [{"type": "blur", "x": 4}, "glow"]}),
                         {"depth": 1, "filters": ["blur", "glow"]})

    def test_same_op_treats_missing_matrix_as_identity_only_when_other_side_has_it(self):
        identity = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        self.assertIsNone(denetim.same_op({"depth": 1}, {"depth": 1, "matrix": identity}))
        self.assertIsNotNone(denetim.same_op({"depth": 1}, {"depth": 1, "matrix": [2.0] + identity[1:]}))
        self.assertIsNotNone(denetim.same_op({"depth": 1, "char": 3}, {"depth": 1, "char": 4}))
        self.assertIsNotNone(denetim.same_op({"depth": 1}, {"depth": 1, "name": "a"}))

    def test_compare_timeline_counts_checked_operations_and_reports_differences(self):
        theirs = denetim.XmlTimeline()
        theirs.frames = [[{"depth": 1, "char": 5}], [{"remove": 1}]]
        theirs.labels = {"giris": 0}
        theirs.sounds = {1: [{"id": 9}]}
        ours = {"frames": [[{"depth": 1, "char": 5}], [{"remove": 1}]], "labels": {"giris": 0},
                "sounds": {"1": [{"id": 9}]}}
        problems = []
        self.assertEqual(denetim.compare_timeline("s", ours, theirs, problems), 2)
        self.assertEqual(problems, [])
        ours["labels"] = {}
        ours["frames"][0][0]["char"] = 6
        denetim.compare_timeline("s", ours, theirs, problems)
        self.assertEqual(len(problems), 2, problems)
        # Sesi durduran kayıt başlatan kayıtla aynı sayılmaz
        problems = []
        ours = {"frames": [[{"depth": 1, "char": 5}], [{"remove": 1}]], "labels": {"giris": 0},
                "sounds": {"1": [{"id": 9}]}}
        theirs.sounds = {1: [{"id": 9, "stop": True}]}
        denetim.compare_timeline("s", ours, theirs, problems)
        self.assertEqual(problems, ["s: ses başlatmaları farklı"])
        problems = []
        self.assertEqual(denetim.compare_timeline("s", {"frames": [[]]}, theirs, problems), 0)
        self.assertIn("kare sayısı", problems[0])


class PixelTest(unittest.TestCase):
    def test_pixel_difference_places_images_on_white_without_resizing(self):
        black = Image.new("RGBA", (2, 2), (0, 0, 0, 255))
        self.assertEqual(denetim.pixel_difference(black, black), 0)
        white = Image.new("RGBA", (2, 2), (255, 255, 255, 255))
        self.assertEqual(denetim.pixel_difference(black, white), 100)
        # Yan yana konunca 4×2'lik tuvalin yarısı farklı
        self.assertEqual(denetim.pixel_difference(black, black, (0, 0), (2, 0)), 100)
        clear = Image.new("RGBA", (2, 2), (0, 0, 0, 0))
        self.assertEqual(denetim.pixel_difference(clear, white), 0)

    def test_ink_centre_weights_dark_opaque_pixels(self):
        im = Image.new("RGBA", (6, 4), (255, 255, 255, 0))
        im.putpixel((3, 2), (0, 0, 0, 255))
        self.assertEqual(denetim.ink_centre(im), (3.0, 2.0))
        self.assertIsNone(denetim.ink_centre(Image.new("RGBA", (2, 2), (0, 0, 0, 0))))

    def test_best_offset_finds_where_the_second_drawing_sits(self):
        a = Image.new("RGBA", (40, 30), (255, 255, 255, 255))
        for x in range(10, 20):
            for y in range(5, 25):
                a.putpixel((x, y), (0, 0, 0, 255) if (x + y) % 3 else (120, 0, 0, 255))
        # b: aynı çizim, kendi tuvalinde 7 piksel sağa, 3 piksel aşağıya kaymış (belgelenmemiş pay gibi)
        b = Image.new("RGBA", (50, 40), (255, 255, 255, 0))
        b.paste(a.crop((10, 5, 20, 25)), (17, 8))
        self.assertEqual(denetim.best_offset(a, b), (-7, -3))
        self.assertEqual(denetim.best_offset(a, Image.new("RGBA", (5, 5))), (0, 0))

    def test_compare_rendered_reports_missing_and_different_drawings(self):
        with tempfile.TemporaryDirectory() as td:
            black, grey = os.path.join(td, "a.png"), os.path.join(td, "b.png")
            Image.new("RGBA", (4, 4), (0, 0, 0, 255)).save(black)
            Image.new("RGBA", (4, 4), (40, 40, 40, 255)).save(grey)
            pairs = [("aynı", black, (0, 0), black, (0, 0)), ("farklı", black, (0, 0), grey, (0, 0)),
                     ("yok", os.path.join(td, "yok.png"), (0, 0), black, (0, 0)),
                     ("ffdec yok", black, (0, 0), os.path.join(td, "yok.png"), (0, 0))]
            probs, worst = denetim.compare_rendered(pairs)
        self.assertEqual(len(probs), 3, probs)
        self.assertTrue(probs[0].startswith("farklı: piksel farkı"))
        self.assertIn("motor çizemedi", probs[1])
        self.assertIn("FFDec'in çizimi yok", probs[2])
        self.assertAlmostEqual(worst, 100 * 40 / 255, places=3)

    def test_hairline_svg_draws_thin_strokes_at_least_one_pixel_wide(self):
        svg = ('<path d="M0 0" data-hairline="true" data-original-stroke-width="0.25" stroke-width="1.0"/>'
               '<path d="M0 0" data-hairline="true" data-original-stroke-width="0.5" stroke-width="1.0"/>'
               '<path d="M0 0" stroke-width="1.0"/>')
        out = denetim.hairline_svg(svg, 4)
        self.assertEqual(out.count(' stroke-width="0.25"'), 1)
        self.assertEqual(out.count(' stroke-width="0.5"'), 1)
        self.assertTrue(out.endswith('<path d="M0 0" stroke-width="1.0"/>'))
        # 1× çizimde 1 pikselden ince olan çizgi 1 piksel olur
        self.assertEqual(denetim.hairline_svg(svg, 1).count(' stroke-width="1"'), 2)

    def test_hairline_problems_compare_markers_with_ffdec_and_list(self):
        old_root = denetim.ROOT
        with tempfile.TemporaryDirectory() as td:
            denetim.ROOT = td
            try:
                ours = os.path.join(td, "content", "feudalism", "t", "shapes")
                theirs = os.path.join(td, "arsiv", "shapes")
                os.makedirs(ours)
                os.makedirs(theirs)
                os.makedirs(os.path.join(td, "content", "feudalism", "t", "shapes-bitmap"))
                for sid, n_ours, n_theirs in (("1", 2, 2), ("2", 0, 1)):
                    with open(os.path.join(ours, f"{sid}.svg"), "w", encoding="utf-8") as f:
                        f.write('<path data-hairline="true"/>' * n_ours)
                    with open(os.path.join(theirs, f"{sid}.svg"), "w", encoding="utf-8") as f:
                        f.write('<path ffdec:has-small-stroke="true"/>' * n_theirs)
                lib = {"shapes": {"1": [0, 0], "2": [0, 0]}, "bitmap_shapes": {},
                       "hairlines": {"1": [[0, 0.25], [1, 0.25]]}}
                probs = denetim.hairline_problems("t", lib, os.path.join(td, "arsiv"))
                lib["hairlines"]["1"].pop()
                more = denetim.hairline_problems("t", lib, os.path.join(td, "arsiv"))
            finally:
                denetim.ROOT = old_root
        self.assertEqual(probs, ["t şekil 2: ince çizgi bizim 0 / listede 0 / FFDec 1"])
        self.assertEqual(len(more), 2)

    def test_file_hash_and_tree_files_read_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            os.makedirs(os.path.join(td, "a"))
            with open(os.path.join(td, "a", "b.as"), "wb") as f:
                f.write(b"stop();")
            self.assertEqual(denetim.tree_files(td), {"a/b.as": b"stop();"})
            self.assertEqual(denetim.file_hash(os.path.join(td, "a", "b.as")), hashlib.sha256(b"stop();").hexdigest())

    def test_translation_problems_compare_with_source_dump_and_tool(self):
        old_root = denetim.ROOT
        with tempfile.TemporaryDirectory() as td:
            denetim.ROOT = os.path.join(td, "proje")
            try:
                root = os.path.join(td, "swf-oyunlar")
                src = os.path.join(root, "oyunlar", "feudalism", "ceviri")
                os.makedirs(src)
                data = {"adlar": {"silahlar": {}, "zirhlar": {}, "birlikler": {}}, "kod": {},
                        "sabit": {"160": {"parcalar": ["Yerini Koru", "ikinci"]}}, "kutular": {"46": "ıska"},
                        "yazitipleri": {"45": {"kaynak": "yazitipleri/LiberationSans-Bold.ttf"}},
                        "sekiller": {"2019": {"metin": "Öldün..."}}}
                content = os.path.join(denetim.ROOT, "content")
                os.makedirs(os.path.join(content, "feudalism", "f1", "ceviri"))
                os.makedirs(os.path.join(content, "fonts"))
                for name, value in data.items():
                    for folder in (src, os.path.join(content, "feudalism", "f1", "ceviri")):
                        with open(os.path.join(folder, f"{name}.json"), "w", encoding="utf-8") as f:
                            json.dump(value, f, ensure_ascii=False)
                os.makedirs(os.path.join(root, "yazitipleri"))
                for folder in (os.path.join(root, "yazitipleri"), os.path.join(content, "fonts")):
                    with open(os.path.join(folder, "LiberationSans-Bold.ttf"), "wb") as f:
                        f.write(b"ttf")
                with open(os.path.join(content, "fonts", "OFL-Liberation.txt"), "w") as f:
                    f.write("OFL")
                # Kod aracı: hiçbir dosyayı çevirmez
                os.makedirs(os.path.join(root, "araclar"))
                with open(os.path.join(root, "araclar", "kod_cevir.py"), "w") as f:
                    f.write("import os, sys\nos.makedirs(sys.argv[3])\n")
                archive = os.path.join(td, "tam")
                os.makedirs(os.path.join(archive, "scripts"))
                os.makedirs(os.path.join(denetim.ROOT, "kaynak", "feudalism", "f1", "kod-tr"))
                dump = types.SimpleNamespace(texts={160: [{}, {}]}, edit_texts={46: {}}, chars={45: "font", 2019: "shape"})
                lib = {"translation": {"drawn_texts": {"2019": {"file": "ceviri/sekiller/2019.svg"}}}}
                texts = {"fonts": {"45": {"name": "Arial", "bold": True, "file": "fonts/LiberationSans-Bold.ttf"}}}
                clean = denetim.translation_problems("f1", lib, texts, dump, root, archive)
                # Bozulmuş durum: tablo değişmiş, kayıt sayısı tutmuyor, yazı tipi farklı, fazladan çevrilmiş kod
                with open(os.path.join(content, "feudalism", "f1", "ceviri", "kutular.json"), "w") as f:
                    f.write("{}")
                dump.texts[160] = [{}]
                with open(os.path.join(content, "fonts", "LiberationSans-Bold.ttf"), "wb") as f:
                    f.write(b"baska")
                with open(os.path.join(denetim.ROOT, "kaynak", "feudalism", "f1", "kod-tr", "x.as"), "w") as f:
                    f.write("x")
                broken = denetim.translation_problems("f1", lib, texts, dump, root, archive)
            finally:
                denetim.ROOT = old_root
        self.assertEqual(clean, ([], [], [], []))
        self.assertEqual([len(p) for p in broken], [1, 1, 1, 1], broken)
        self.assertIn("kutular.json", broken[0][0])
        self.assertIn("sabit yazı 160", broken[1][0])
        self.assertIn("x.as", broken[2][0])
        self.assertIn("kaynağıyla aynı değil", broken[3][0])

    def test_morph_bounds_problems_compare_canvas_with_union_of_both_ends(self):
        dump = types.SimpleNamespace(morph_bounds={6: {"start": [-1.0, -2.0, 1.0, 0.0], "end": [0.0, 0.0, 2.0, 3.0]}})
        old_root = denetim.ROOT
        with tempfile.TemporaryDirectory() as td:
            denetim.ROOT = td
            try:
                d = os.path.join(td, "content", "feudalism", "t", "morphs")
                os.makedirs(d)
                for end, w in (("start", "3.0"), ("end", "2.0")):
                    with open(os.path.join(d, f"6.{end}.svg"), "w", encoding="utf-8") as f:
                        f.write(f'<svg height="5.0px" width="{w}px"></svg>')
                probs = denetim.morph_bounds_problems("t", {"morphs": {"6": [-1.0, -2.0]}}, dump)
                wrong_origin = denetim.morph_bounds_problems("t", {"morphs": {"6": [0.0, -2.0]}}, dump)
            finally:
                denetim.ROOT = old_root
        self.assertEqual(len(probs), 1, probs)
        self.assertIn("6 end: boyut", probs[0])
        self.assertIn("başlangıç noktası", wrong_origin[0])


if __name__ == "__main__":
    unittest.main()
