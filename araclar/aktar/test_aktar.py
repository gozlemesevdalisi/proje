"""Aktarım aracının birim testleri. SWF dosyası gerektirmez: girdiler elle kurulur.

Çalıştırma (depo kökünden):  python3 -m unittest discover -s araclar/aktar -p 'test_*.py'
"""
import os
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aktar  # noqa: E402
import envanter  # noqa: E402
import swf  # noqa: E402
from swfstats import Bits  # noqa: E402


class BitWriter:
    """SWF bit alanlarını yazmak için (testlerde girdi kurmak)."""

    def __init__(self):
        self.bits = []

    def ub(self, n, v):
        self.bits += [(v >> (n - 1 - i)) & 1 for i in range(n)]

    def sb(self, n, v):
        self.ub(n, v & ((1 << n) - 1))

    def bytes(self):
        bits = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


def matrix_bytes(scale=None, rotate=None, tx=0, ty=0):
    w = BitWriter()
    for pair in (scale, rotate):
        if pair is None:
            w.ub(1, 0)
        else:
            w.ub(1, 1)
            w.ub(5, 20)
            for v in pair:
                w.sb(20, round(v * 65536))
    w.ub(5, 16)
    w.sb(16, round(tx * 20))
    w.sb(16, round(ty * 20))
    return w.bytes()


def cxform_bytes(mul, add):
    w = BitWriter()
    w.ub(1, 1)
    w.ub(1, 1)
    w.ub(4, 10)
    for v in mul:
        w.sb(10, round(v * 256))
    for v in add:
        w.sb(10, v)
    return w.bytes()


class Records(unittest.TestCase):
    def test_matrix(self):
        m = swf.read_matrix(Bits(matrix_bytes(scale=(2, 0.5), rotate=(0.25, -0.25), tx=10.5, ty=-3)))
        self.assertEqual(m, [2.0, 0.25, -0.25, 0.5, 10.5, -3.0])

    def test_identity_matrix(self):
        self.assertEqual(swf.read_matrix(Bits(matrix_bytes())), [1.0, 0.0, 0.0, 1.0, 0.0, 0.0])

    def test_cxform(self):
        c = swf.read_cxform(Bits(cxform_bytes([0.5, 1, 1, 0.25], [255, 0, -255, 0])))
        self.assertEqual(c, [[0.5, 1.0, 1.0, 0.25], [1.0, 0.0, -1.0, 0.0]])

    def test_place_object2(self):
        # Bayraklar: karakter, matris, ad, kırpma derinliği
        flags = 0x02 | 0x04 | 0x20 | 0x40
        body = bytes([flags]) + struct.pack("<HH", 7, 42) + matrix_bytes(tx=5, ty=6) + b"arm\0" + struct.pack("<H", 9)
        op = swf.read_place(body, 26)
        self.assertEqual(op, {"depth": 7, "char": 42, "matrix": [1.0, 0.0, 0.0, 1.0, 5.0, 6.0], "name": "arm",
                              "clip": 9})

    def test_place_move_with_ratio_and_cxform(self):
        body = bytes([0x01 | 0x08 | 0x10]) + struct.pack("<H", 3) + cxform_bytes([1, 1, 1, 0.5], [0, 0, 0, 0]) \
            + struct.pack("<H", 65535)
        op = swf.read_place(body, 26)
        self.assertTrue(op["move"])
        self.assertEqual(op["cxform"][0][3], 0.5)
        self.assertEqual(op["ratio"], 1.0)

    def test_place_object3_glow_and_blend(self):
        glow = bytes([1, 2]) + bytes([255, 200, 0, 255]) + struct.pack("<iih", 4 * 65536, 4 * 65536, 512) + bytes([0x80])
        body = bytes([0x02, 0x01 | 0x02]) + struct.pack("<HH", 1, 5) + glow + bytes([3])
        op = swf.read_place(body, 70)
        self.assertEqual(op["char"], 5)
        self.assertEqual(op["filters"][0]["type"], "glow")
        self.assertEqual(op["filters"][0]["blur"], [4.0, 4.0])
        self.assertTrue(op["filters"][0]["inner"])
        self.assertEqual(op["blend"], "multiply")

    def test_timeline_frames_labels_and_remove(self):
        t = swf.Timeline()
        place = bytes([0x02]) + struct.pack("<HH", 1, 10)
        t.add_tag(26, place)
        t.add_tag(43, b"walk\0")
        t.add_tag(1, b"")
        t.add_tag(28, struct.pack("<H", 1))
        t.add_tag(1, b"")
        t.finish()
        self.assertEqual(t.frames, [[{"depth": 1, "char": 10}], [{"remove": 1}]])
        self.assertEqual(t.labels, {"walk": 0})
        self.assertEqual(t.characters(), {10})

    def test_button_records(self):
        rec = bytes([0x01 | 0x08]) + struct.pack("<HH", 12, 1) + matrix_bytes(tx=2) + cxform_bytes([1, 1, 1, 1], [0] * 4)
        body = struct.pack("<H", 99) + b"\0" + struct.pack("<H", 0) + rec + b"\0"
        bid, records = swf.read_button(body)
        self.assertEqual(bid, 99)
        self.assertEqual(records[0]["states"], [True, False, False, True])
        self.assertEqual(records[0]["char"], 12)
        self.assertEqual(records[0]["matrix"][4], 2.0)


class Details(unittest.TestCase):
    def test_sound(self):
        # MP3 (2), 11 kHz (1), 16 bit, mono; 11025 örnek = 1 saniye
        body = struct.pack("<H", 530) + bytes([(2 << 4) | (1 << 2) | 0b10]) + struct.pack("<I", 11025) + b"x" * 100
        snd = swf.read_sound(body)
        self.assertEqual((snd["id"], snd["format"], snd["rate"], snd["stereo"]), (530, "MP3", 11025, False))
        self.assertAlmostEqual(snd["seconds"], 1.0)

    def test_font_codes(self):
        # DefineFont3, dar ofsetler, geniş kodlar; iki glif ('A', 'b'), boş glif şekilleri
        name = b"Arial"
        offsets = struct.pack("<HH", 6, 6) + struct.pack("<H", 6)  # 2 glif ofseti + kod tablosu ofseti
        body = struct.pack("<H", 45) + bytes([0x04 | 0x01, 1, len(name)]) + name + struct.pack("<H", 2) + offsets \
            + struct.pack("<HH", ord("A"), ord("b"))
        fid, fname, bold, italic, codes = swf.read_font(body)
        self.assertEqual((fid, fname, bold, italic, codes), (45, "Arial", True, False, [65, 98]))

    def test_text_records_decode(self):
        w = BitWriter()
        w.ub(5, 1)
        for _ in range(4):
            w.sb(1, 0)
        rect = w.bytes()
        glyphs = BitWriter()
        for g in (0, 1):
            glyphs.ub(4, g)
            glyphs.sb(8, 10)
        record = bytes([0x80 | 0x08 | 0x02]) + struct.pack("<Hh", 45, 20) + struct.pack("<H", 240) + bytes([2]) + glyphs.bytes()
        body = struct.pack("<H", 160) + rect + matrix_bytes() + bytes([4, 8]) + record + b"\0"
        tid, lines = swf.read_text(body, False)
        self.assertEqual(tid, 160)
        self.assertEqual(swf.decode_text(lines, {45: [ord("O"), ord("K")]}), "OK")

    def test_edit_text_initial_value(self):
        w = BitWriter()
        w.ub(5, 1)
        for _ in range(4):
            w.sb(1, 0)
        body = struct.pack("<H", 799) + w.bytes() + bytes([0x80 | 0x01, 0]) + struct.pack("<HH", 2, 360) + b"\0" + b"OK\0"
        self.assertEqual(swf.read_edit_text(body), {"id": 799, "font_height": 18.0, "variable": "", "text": "OK"})

    def test_jpeg_size(self):
        jpeg = b"\xff\xd8" + b"\xff\xe0" + struct.pack(">H", 4) + b"ab" + b"\xff\xc0" + struct.pack(">HBHH", 17, 8, 200, 800)
        self.assertEqual(swf.jpeg_size(jpeg), (800, 200))
        self.assertIsNone(swf.jpeg_size(b"\xff\xd8\xff\xd9"))


class Reachability(unittest.TestCase):
    def test_children_and_reachable(self):
        m = swf.Movie.__new__(swf.Movie)
        m.shapes, m.morphs, m.bitmaps, m.texts, m.edit_texts, m.fonts, m.sounds = {1, 2}, set(), set(), set(), set(), set(), set()
        a, b = swf.Timeline(), swf.Timeline()
        a.frames = [[{"depth": 1, "char": 1}, {"depth": 2, "char": 11}]]
        b.frames = [[{"depth": 1, "char": 2}]]
        m.sprites = {10: a, 11: b}
        m.buttons = {}
        self.assertEqual(m.reachable({10}), {10, 11, 1, 2})
        self.assertEqual(m.kind(11), "sprite")
        self.assertIsNone(m.kind(99))


class Actions(unittest.TestCase):
    def test_simple_commands(self):
        src = 'stop();\nthis._parent.directHit();\ngotoAndPlay(2);\ngotoAndStop("sword");\nplay();\n'
        self.assertEqual(aktar.parse_actions(src), [{"stop": True}, {"event": "directHit"},
                                                    {"goto": 2, "play": True}, {"goto": "sword", "play": False},
                                                    {"play": True}])

    def test_commands_inside_blocks_are_ignored(self):
        src = "if(play_count > 0)\n{\n   gotoAndPlay(2);\n}\nthis.onRelease = function()\n{\n   stop();\n};\n"
        self.assertEqual(aktar.parse_actions(src), [])

    def test_script_folder_ids(self):
        self.assertEqual(aktar.script_dir_id("DefineSprite_547_Human"), 547)
        self.assertEqual(aktar.script_dir_id("DefineSprite_12"), 12)
        self.assertIsNone(aktar.script_dir_id("frame_3"))

    def test_read_frame_actions(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "frame_40"))
            with open(os.path.join(d, "frame_40", "DoAction.as"), "w", encoding="utf-8") as f:
                f.write("stop();\n")
            self.assertEqual(aktar.read_frame_actions(d), {39: [{"stop": True}]})


class Shapes(unittest.TestCase):
    def test_convert_shape_keeps_paths_and_finds_origin(self):
        svg = ('<?xml version="1.0"?>\n<svg xmlns:ffdec="https://www.free-decompiler.com/flash" ffdec:objectType="shape" '
               'width="10px" height="5px" xmlns="http://www.w3.org/2000/svg">\n  '
               '<g transform="matrix(1.0, 0.0, 0.0, 1.0, 49.55, -3.5)">\n    <path d="M0 0 L1 1" fill="#ff0000"/>\n  </g>\n</svg>')
        text, origin = aktar.convert_shape(svg)
        self.assertEqual(origin, (-49.55, 3.5))
        self.assertNotIn("ffdec", text)
        self.assertNotIn("<?xml", text)
        self.assertIn('<path d="M0 0 L1 1" fill="#ff0000"/>', text)

    def test_hyphenated_ffdec_attributes_are_removed(self):
        svg = ('<svg xmlns:ffdec="x"><g transform="matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)"><path d="M0 0" stroke="#000000" '
               'ffdec:has-small-stroke="true" ffdec:original-stroke-width="0.5"/></g></svg>')
        self.assertNotIn("ffdec", aktar.convert_shape(svg)[0])

    def test_bitmap_filled_shape_is_skipped(self):
        self.assertIsNone(aktar.convert_shape('<svg><pattern><image href="x"/></pattern></svg>'))


class Morphs(unittest.TestCase):
    SVG = ('<svg xmlns="http://www.w3.org/2000/svg"><g><path d="M0 0" fill="url(#g)">'
           '<animate attributeName="d" values="M0 0 L1 1;M0 0 L2 2"/></path></g><defs>'
           '<linearGradient id="g" gradientTransform="matrix(2, 0, 0, 2, 10, 20)">'
           '<animateTransform additive="replace" attributeName="gradientTransform" from="1" to="1" type="scale"/>'
           '<animateTransform additive="sum" attributeName="gradientTransform" from="10 20" to="30 40" type="translate"/>'
           '<animateTransform additive="sum" attributeName="gradientTransform" from="0" to="90" type="rotate"/>'
           '<animateTransform additive="sum" attributeName="gradientTransform" from="2 2" to="1 1" type="scale"/>'
           '<stop offset="0" stop-color="#000000"><animate attributeName="stop-color" values="#000000;#FFFFFF"/></stop>'
           '</linearGradient></defs></svg>')

    def test_start_and_end(self):
        start = aktar.apply_animates(self.SVG, 0)
        end = aktar.apply_animates(self.SVG, 1)
        self.assertNotIn("animate", start + end)
        self.assertIn('d="M0 0 L1 1"', start)
        self.assertIn('d="M0 0 L2 2"', end)
        self.assertIn('gradientTransform="matrix(2, 0, 0, 2, 10, 20)"', start)
        self.assertIn('gradientTransform="matrix(0, 1, -1, 0, 30, 40)"', end)
        self.assertIn('stop-color="#FFFFFF"', end)

    def test_transform_matrix(self):
        self.assertEqual(aktar.transform_matrix("translate", "3 4"), (1.0, 0.0, 0.0, 1.0, 3.0, 4.0))
        self.assertEqual(aktar.transform_matrix("scale", "2"), (2.0, 0.0, 0.0, 2.0, 0.0, 0.0))
        a, b, c, d, e, f = aktar.transform_matrix("skewX", "45")
        self.assertAlmostEqual(c, 1.0)
        with self.assertRaises(ValueError):
            aktar.transform_matrix("wobble", "1")


class TextRecords(unittest.TestCase):
    def test_decode_records_lines_and_font_carry_over(self):
        records = [{"font": 1, "y": 10, "glyphs": [[0, 5], [1, 5]]}, {"glyphs": [[2, 5]]}, {"y": 30, "glyphs": [[1, 5]]}]
        self.assertEqual(aktar.decode_records(records, {1: [ord("O"), ord("K"), ord("!")]}), "OK!\nK")

    def test_csm(self):
        body = struct.pack("<H", 7) + bytes([(1 << 6) | (1 << 3)]) + struct.pack("<ff", 0.5, -1.0) + b"\0"
        self.assertEqual(swf.read_csm(body), {"text": 7, "flash_type": True, "grid_fit": "pixel", "thickness": 0.5,
                                              "sharpness": -1.0})

    def test_clip_actions_flag(self):
        body = bytes([0x02 | 0x80]) + struct.pack("<HH", 1, 9) + b"\0\0"
        self.assertTrue(swf.read_place(body, 26)["clip_actions"])


class Files(unittest.TestCase):
    def test_find_file_by_id_or_id_and_name(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ("930_slash.wav.mp3", "93.mp3", "530.mp3"):
                open(os.path.join(d, name), "w").close()
            self.assertTrue(aktar.find_file(d, 930, {".mp3"}).endswith("930_slash.wav.mp3"))
            self.assertTrue(aktar.find_file(d, 93, {".mp3"}).endswith("93.mp3"))
            self.assertIsNone(aktar.find_file(d, 5, {".mp3"}))


class Inventory(unittest.TestCase):
    def test_strip_html(self):
        html = '<p align="left"><font face="_sans"><b>Lv. 5</b><sbr />next</font></p>It&apos;s'
        self.assertEqual(envanter.strip_html(html), "Lv. 5\nnext\nIt's")


class Filters(unittest.TestCase):
    def test_component_exports(self):
        for name in ("ScrollThumbTopUp", "Button", "UIObject", "__Packages.mx.core.View", "ComboBox"):
            self.assertTrue(aktar.is_component_export(name), name)
        for name in ("Human", "Tree_1", "WorldMap", "BarracksUnit"):
            self.assertFalse(aktar.is_component_export(name), name)

    def test_clean_op_drops_identity_values(self):
        op = {"depth": 1, "matrix": [1.0, 0.0, 0.0, 1.0, 0.0, 0.0], "cxform": [[1.0] * 4, [0.0] * 4],
              "ratio": 0.123456}
        self.assertEqual(aktar.clean_op(op), {"depth": 1, "ratio": 0.12346})


if __name__ == "__main__":
    unittest.main()
