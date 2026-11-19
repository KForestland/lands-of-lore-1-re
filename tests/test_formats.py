"""Reader tests on synthetic bytes: no game files needed (python3 -m unittest discover -s tests)."""
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import lol1lib
import exe_tables
import fnt_reader
import palette_reader
import parse_tim
import tlc_reader
import voc_reader
import wll_parser
import xxx_reader


def palette_768():
    raw = bytearray(768)
    raw[6:9] = bytes([63, 51, 52])      # colour 2, the palette.md worked example
    raw[9:12] = bytes([63, 36, 37])
    return bytes(raw)


class PaletteTests(unittest.TestCase):
    def test_pal_rows_6_and_8_bit(self):
        r = palette_reader.rows(palette_768())
        self.assertEqual(len(r), 256)
        self.assertEqual(r[2], (2, (63, 51, 52), (255, 206, 210)))
        self.assertEqual(r[3][2], (255, 145, 149))

    def test_cps_palette(self):
        pal = palette_768()
        pixels = bytes(range(10))
        cps = struct.pack("<HBBIH", 0, 0, 0, len(pixels), len(pal)) + pal + pixels
        self.assertEqual(palette_reader.palette_bytes("X.CPS", cps), pal)
        h, p, px = lol1lib.load_bitmap(cps)
        self.assertEqual((h["palette_size"], bytes(px)), (768, pixels))

    def test_swatch_png(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "s.png"
            palette_reader.swatch(palette_768(), str(path), cell=2)
            img = Image.open(path).convert("RGB")
            self.assertEqual(img.size, (32, 32))
            self.assertEqual(img.getpixel((4, 0)), (255, 206, 210))


class WllTlcXxxTests(unittest.TestCase):
    def test_wll_records(self):
        # wll.md worked example: area 0, wall type 0 and wall type 1
        data = bytes.fromhex("0000" "000000000000000080003f00" "010001000000000007 00ffff".replace(" ", ""))
        parsed = wll_parser.parse_wll(data)
        self.assertEqual(parsed["n_records"], 2)
        self.assertEqual(parsed["records"][0], {"vmp_map": 0, "shape_map": 0, "special_type": 0,
                                                "wall_flags": 0x80, "automap_data": 0x3F})
        self.assertEqual(parsed["records"][1]["automap_data"], 0xFF)
        lines = wll_parser.record_lines(data)
        self.assertTrue(lines[0].startswith("area 0 (KEEP), 2 records"))
        self.assertTrue(lines[3].rstrip().endswith("00 00 00 FF"))

    def test_tlc_tables(self):
        t1 = bytes([0, 0xFF, 1]) + b"\xff" * 253
        t2 = bytearray(5120)
        t2[256 + 5] = 9
        slots = tlc_reader.parse(t1 + bytes(t2))[2]
        self.assertEqual(slots, {0: 0, 2: 1})
        rows = tlc_reader.full_rows(bytes(t2[256:512]))
        self.assertEqual(len(rows), 16)
        self.assertEqual(rows[0], "    0: 00 00 00 00 00 09 " + " ".join(["00"] * 10))

    def test_xxx_records(self):
        data = struct.pack("<6H", 13, 13, 1, 13, 14, 0x41D0) + struct.pack("<6H", 1, 2, 0xFFFF, 3, 4, 0xFFFF)
        r = xxx_reader.parse(data)
        self.assertEqual(r[0], {"symbol_x": 13, "symbol_y": 13, "symbol": 1, "reveal_x": 13, "reveal_y": 14,
                                "string_id": 0x41D0})
        self.assertEqual(r[1]["symbol"], 0xFFFF)


class FntVocTests(unittest.TestCase):
    def test_fnt_header_and_glyphs(self):
        # header 14 bytes, descriptor at 14 (6 bytes), offsets at 20, widths at 24, heights at 26
        n = 2
        b = bytearray(40)
        struct.pack_into("<7H", b, 0, 40, 0x500, 14, 20, 24, 0, 26)
        b[14 + 3], b[14 + 4], b[14 + 5] = n - 1, 9, 8
        struct.pack_into("<2H", b, 20, 0, 30)
        b[24:26] = bytes([0, 4])
        b[26:30] = bytes([0, 0, 1, 5])
        h, g = fnt_reader.parse(bytes(b))
        self.assertEqual(h, {"size_field": 40, "signature": "0x500", "glyphs": 2, "height": 9, "width": 8})
        self.assertEqual(g[1], {"offset": 30, "width": 4, "top": 1, "rows": 5})

    def test_voc_header_and_block(self):
        ver = 0x10A
        head = b"Creative Voice File\x1a" + struct.pack("<HHH", 26, ver, (~ver + 0x1234) & 0xFFFF)
        body = bytes([0xA6, 0]) + bytes(range(5))
        blob = head + bytes([1]) + struct.pack("<I", len(body))[:3] + body + b"\0"
        info, pcm = voc_reader.parse(blob)
        self.assertEqual((info["header_size"], info["check_ok"], info["rate"], info["samples"]), (26, True, 11025, 5))
        self.assertEqual(info["blocks"], [(1, 7)])
        with self.assertRaises(ValueError):
            voc_reader.parse(b"not a voc" + bytes(30))


def tim_file(avtl_words, text=None):
    def chunk(tag, body):
        return tag + struct.pack(">I", len(body)) + body + b"\0" * (len(body) & 1)
    body = b"AVFS" + (chunk(b"TEXT", text) if text is not None else b"") + \
        chunk(b"AVTL", struct.pack(f"<{len(avtl_words)}H", *avtl_words))
    return b"FORM" + struct.pack(">I", len(body)) + body


class TimTests(unittest.TestCase):
    def test_framing_walk_and_listing(self):
        # one function at word 1: return 1; initWSA slot 0 "BOOK"; nested 0x0E sound 92; stop all
        words = [1, 3, 0, 0x0118, 9, 0, 0x0102, 0, 0, 288, 32, 0, 40, 5, 6, 0x0119, 0x0E, 92, 3, 0, 0x0101]
        text = struct.pack("<H", 2) + b"BOOK\0"
        data = tim_file(words, text)
        ch = parse_tim.tim_chunks(data)
        self.assertEqual(sorted(ch), ["AVTL", "TEXT"])
        self.assertEqual(parse_tim.tim_text(ch["TEXT"], 0), "BOOK")
        instrs, stops = parse_tim.walk_avtl(words)
        self.assertEqual(stops, 0)
        self.assertEqual([i[4] & 0xFF for i in instrs], [0x18, 0x02, 0x19, 0x01])
        lines = parse_tim.tim_listing("TEST.TIM", data)
        self.assertIn('cmd_initWSA index=0 string_id=0 "BOOK" x=288 y=32 offscreen=0 flags=40', lines[3])
        self.assertIn("nested 0x0E tlol_playSoundEffect args [92]", lines[4])
        self.assertTrue(lines[-1].endswith("walk stops before the end of AVTL: 0"))

    def test_walk_stops_and_entries(self):
        # two functions at words 2 and 5; the second ends on a bad opcode-word high byte
        words = [2, 5, 3, 0, 0x0101, 3, 0, 0x0201]
        instrs, stops = parse_tim.walk_avtl(words)
        self.assertEqual([(i[0], i[1]) for i in instrs], [(0, 2)])
        self.assertEqual(stops, 1)
        self.assertEqual(parse_tim.tim_function_count([3, 10, 20, 3]), 3)


class ExeTablesTests(unittest.TestCase):
    def image(self):
        exe = bytearray(0x40000)
        exe[:2] = b"MZ"
        struct.pack_into("<H", exe, 8, 0x380)                  # header 0x3800 bytes
        base, mods = 0x29D60, 0x2B4D2
        for i, row in enumerate([0, 0, 0, 1, 0, 0, 1, 2, 4]):
            r = base + i * 0x82
            exe[r + 2:r + 6] = b"Test"
            target = mods + row * 18 - 0x3800                  # far pointer to the modifier row
            struct.pack_into("<HH", exe, r + 0x13, target & 0xF, target >> 4)
            struct.pack_into("<hH", exe, r + 0x39, 50, 60)
        struct.pack_into("<14H", exe, 0x2B5E0, 0x4034, 5, 10, 15, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0x100)
        e = 0x33D68                                            # timer slot 0
        struct.pack_into("<HHIIHHHB", exe, e, 0x4A, 0xBBC, 15, 0, 0, 0x3858, 0x2E2D, 1)
        return bytes(exe)

    def test_characters_spells_timers(self):
        exe = self.image()
        self.assertEqual(exe_tables.header_size(exe), 0x3800)
        chars = exe_tables.characters(exe, 0x29D60)
        self.assertEqual([exe_tables.char_row(exe, "cd", r) for r in chars], [0, 0, 0, 1, 0, 0, 1, 2, 4])
        self.assertEqual((chars[0]["name"], chars[0]["current HP"], chars[0]["max HP"]), ("Test", 50, 60))
        sp = exe_tables.spells(exe, 0x2B5E0)
        self.assertEqual((sp[0]["name id"], sp[0]["MP"], sp[0]["property"]), (0x4034, [5, 10, 15, 25], 0x100))
        self.assertIn("raw+0A", sp[0])                         # UNCONFIRMED words stay unnamed
        t = exe_tables.timers(exe, 0x33D68)[0]
        self.assertEqual((t["callback file"], t["period"], t["clock"], t["enable"]), (0xF40A, 15, (0x3858, 0x2E2D), 1))

    def test_find_images_by_size(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "MAIN.EXE").write_bytes(b"MZ" + bytes(0x5B470 - 2))
            found = exe_tables.find_images(d)
            self.assertEqual([(k, label) for k, label, _, _ in found], [("floppy", "floppy MAIN.EXE")])
            (Path(d) / "MAIN.EXE").write_bytes(b"MZ" + bytes(100))
            self.assertEqual(exe_tables.find_images(d), [])


if __name__ == "__main__":
    unittest.main()
