"""Unit tests for the wall assembler, the level map drawing, the monster scan's
folder handling, the EMC2 listing's broken-pipe handling and the blend-table
palette mix, and the sound-driver entry tables. Synthetic bytes only;
no game files needed."""
import os
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import vcn_vmp_reader as V

try:
    import PIL  # noqa: F401
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def synthetic_set():
    """Three VCN tiles: tile 0 unused, tile 1 nibbles 0..7 per row, tile 2 all nibble 0.
    Colour table: entry i -> i + 100 (bank 0), i + 200 (bank 16, tile 2 uses it)."""
    tile1 = bytes([0x01, 0x23, 0x45, 0x67] * 8)
    tiles = bytes(32) + tile1 + bytes(32)
    shift = bytes([0, 0, 16])
    col = bytes([(i + 100) if i < 16 else (i - 16 + 200) for i in range(32)] + [0] * 96)
    return tiles, shift, col


class WallAssemblyTests(unittest.TestCase):
    def test_pieces_fill_a_page_exactly(self):
        used = []
        for (w, h), off in zip(V.VIS_PIECES, V.VIS_OFFS):
            used += range(off, off + w * h)
        self.assertEqual(sorted(used), list(range(V.PAGE_WORDS)))
        self.assertEqual(V.VIS_PIECES[V.FRONT_PIECE], (16, 12))

    def test_tile_pixels_colour_bank_and_mirror(self):
        tiles, shift, col = synthetic_set()
        px = V.tile_pixels(tiles, col, shift, 1)
        self.assertEqual(px[:8], [100, 101, 102, 103, 104, 105, 106, 107])
        self.assertEqual(V.tile_pixels(tiles, col, shift, 1, flip=True)[:8], [107, 106, 105, 104, 103, 102, 101, 100])
        self.assertEqual(set(V.tile_pixels(tiles, col, shift, 2)), {200})

    def test_assemble_transparent_words(self):
        tiles, shift, col = synthetic_set()
        # word 0: nothing; 0x4001: tile 1 mirrored; 0x8001: tile 1 over the floor, colour-0 pixels skipped
        col0 = bytes([0]) + col[1:]
        w, h, grid = V.assemble([0, 0x4001, 0x8001], 0, 3, 1, tiles, col0, shift)
        self.assertEqual((w, h), (24, 8))
        self.assertTrue(all(v is None for v in grid[0:8]))
        self.assertEqual(grid[8:16], [107, 106, 105, 104, 103, 102, 101, 0])
        self.assertEqual(grid[16:24], [None, 101, 102, 103, 104, 105, 106, 107])

    def test_wall_piece_reads_its_page(self):
        tiles, shift, col = synthetic_set()
        words = [0] * (V.FLOOR_WORDS + 2 * V.PAGE_WORDS)
        start = V.FLOOR_WORDS + V.PAGE_WORDS + V.VIS_OFFS[V.FRONT_PIECE]
        for i in range(16 * 12):
            words[start + i] = 2
        w, h, grid = V.wall_piece(words, 2, V.FRONT_PIECE, tiles, col, shift)
        self.assertEqual((w, h), (128, 96))
        self.assertEqual(set(grid), {200})
        self.assertEqual(set(V.wall_piece(words, 1, V.FRONT_PIECE, tiles, col, shift)[2]), {None})

    @unittest.skipUnless(HAVE_PIL, "Pillow not installed")
    def test_walls_image_size(self):
        tiles, shift, col = synthetic_set()
        words = [1] * (V.FLOOR_WORDS + V.PAGE_WORDS)
        pal = bytes([63, 0, 0] * 128)
        img = V.walls_image(words, tiles, col, shift, pal, scale=1)
        # rows: floor/ceiling 176x120, one page whose widest row is the nine pieces side by side
        width = sum(c * 8 for c, _ in V.VIS_PIECES) + 6 * 10
        self.assertEqual(img.size, (width, 120 + 120 + 18))
        self.assertEqual(img.getpixel((6, 6)), (255, 0, 0))


@unittest.skipUnless(HAVE_PIL, "Pillow not installed")
class LevelMapTests(unittest.TestCase):
    def test_solid_mixed_and_open_blocks(self):
        import level_renderer as R
        faces = [[0, 0, 0, 0]] * 1024
        faces = [list(f) for f in faces]
        faces[0] = [1, 1, 1, 1]          # solid, page 1
        faces[1] = [1, 1, 2, 1]          # solid, south face page 2 (e.g. a window)
        faces[33] = [3, 0, 3, 0]         # door block: strips north and south
        faces[2] = [-1, -1, -1, -1]      # page past the VMP end
        faces[3] = [2, 1, 1, 1]          # north face off the map: never seen, no strip
        colours = {1: (200, 0, 0), 2: (0, 200, 0), 3: (0, 0, 200)}
        floor = (10, 10, 10)
        img = R.draw_map(faces, colours, floor, cell=10)
        self.assertEqual(img.size, (320, 320))
        self.assertEqual(img.getpixel((5, 5)), (200, 0, 0))            # solid block fill
        self.assertEqual(img.getpixel((15, 8)), (0, 200, 0))           # its south strip
        self.assertEqual(img.getpixel((15, 9)), R.OUTLINE)             # edge towards the door block
        self.assertEqual(img.getpixel((15, 3)), (200, 0, 0))
        self.assertEqual(img.getpixel((25, 5)), (200, 0, 0))           # every solid block: main colour
        self.assertEqual(img.getpixel((35, 1)), (200, 0, 0))
        self.assertEqual(img.getpixel((15, 11)), (0, 0, 200))          # door strip north
        self.assertEqual(img.getpixel((15, 15)), floor)                # door middle is floor
        self.assertEqual(img.getpixel((15, 19)), (0, 0, 200))          # door strip south
        self.assertEqual(img.getpixel((50, 50)), floor)                # open floor

    def test_readable_keeps_hue(self):
        import level_renderer as R
        colours, floor = R.readable({1: (50, 40, 10), 2: (20, 20, 20)}, (60, 60, 60), 1)
        self.assertEqual(colours[1], (200, 160, 40))                  # x4: brightest channel to 200
        self.assertEqual(colours[2], (80, 80, 80))
        self.assertLessEqual(R.luma(floor), 0.3 * R.luma(colours[1]) + 1)


class MonsterScanArgsTests(unittest.TestCase):
    def test_finds_main_exe_without_capstone(self):
        import monster_reference_scan as M
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "cd", "HARDRIVE"))
            Path(d, "cd", "HARDRIVE", "MAIN.EXE").write_bytes(b"MZ")
            os.makedirs(os.path.join(d, "floppy"))
            Path(d, "floppy", "MAIN.EXE").write_bytes(b"MZ")
            self.assertEqual(M.main_exe(os.path.join(d, "cd"))[0], "CD")
            self.assertEqual(M.main_exe(os.path.join(d, "floppy"))[0], "floppy")
            with self.assertRaises(OSError):
                M.main_exe(d)

    def test_help_changes_nothing(self):
        p = subprocess.run([sys.executable, str(TOOLS / "monster_reference_scan.py"), "--help"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("--data", p.stdout)


class ShpHelpTests(unittest.TestCase):
    def test_interface_example_names_an_interface_shape(self):
        p = subprocess.run([sys.executable, str(TOOLS / "shp_renderer.py"), "--help"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("GAMESHP.SHP --out-dir shapes/ --pal-from PLAYFLD.CPS", p.stdout)
        self.assertNotIn("KEEP.SHP --out-dir shapes/ [--pal-from", p.stdout)


class Emc2PipeTests(unittest.TestCase):
    def test_closed_pipe_is_quiet(self):
        def chunk(tag, body):
            return struct.pack(">4sI", tag, len(body)) + body + b"\0" * (len(body) % 2)
        words = [0x43FF] * 20000          # about 0.5 MB of listing, more than a pipe buffer
        chunks = chunk(b"ORDR", struct.pack(">H", 0)) + chunk(b"DATA", struct.pack(f">{len(words)}H", *words))
        data = b"FORM" + struct.pack(">I", 4 + len(chunks)) + b"EMC2" + chunks
        with tempfile.TemporaryDirectory() as d:
            path = Path(d, "big.inf")
            path.write_bytes(data)
            p = subprocess.Popen([sys.executable, str(TOOLS / "emc2_decompile.py"), str(path)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            first = p.stdout.readline()
            p.stdout.close()
            err = p.stderr.read()
            p.stderr.close()
            rc = p.wait()
        self.assertTrue(first.startswith(b"; big.inf"))
        self.assertEqual((rc, err), (0, b""))


class BlendModelTests(unittest.TestCase):
    """lol1_loose.blend_model on a four-colour palette: black, white and red twice."""

    PALETTE = bytes([0, 0, 0, 63, 63, 63, 63, 0, 0, 63, 0, 0])

    def test_nearest_tie_goes_to_later_index(self):
        import lol1_loose
        rgb = lol1_loose.palette_rgb(self.PALETTE)
        self.assertEqual(lol1_loose.nearest_colour((41, 0, 0), rgb), 3)
        self.assertEqual(lol1_loose.nearest_colour((21, 21, 21), rgb), 0)

    def test_mix_22_42(self):
        import lol1_loose
        table = lol1_loose.blend_model(self.PALETTE)
        self.assertEqual(len(table), 16)
        # row 0: (0) + (col*42)>>6; white 63 -> 41, red -> (41, 0, 0)
        self.assertEqual(list(table[0:4]), [0, 1, 3, 3])
        # row 1: white*22>>6 = 21 per channel
        self.assertEqual(list(table[4:7]), [0, 1, 3])
        # row 2: red*22>>6 = (21, 0, 0)
        self.assertEqual(list(table[8:11]), [0, 1, 3])


class DriverTableTests(unittest.TestCase):
    """A synthetic ADV and ALFX member in the shipped layout."""

    @staticmethod
    def adv(target_prologue=b"\x55\x8b\xec"):
        import lol1_driver_tables as D
        head = D.ADV_COPYRIGHT + b"\x1a"
        table = 2 + len(head)
        code = table + 12
        rows = struct.pack("<4H", 100, code, 101, code + 3) + b"\xff\xff\x00\x00"
        return struct.pack("<H", table) + head + rows + target_prologue + b"\x55\x8b\xec"

    def test_adv_rows(self):
        import lol1_driver_tables as D
        start, rows = D.adv_entries(self.adv())
        self.assertEqual(start, 45)
        self.assertEqual(rows, [(100, 57), (101, 60)])

    def test_adv_without_prologue_fails(self):
        import lol1_driver_tables as D
        with self.assertRaises(ValueError):
            D.adv_entries(self.adv(b"\x90\x90\x90"))

    def test_alfx_dispatch(self):
        import lol1_driver_tables as D
        # +0 jmp dispatch, +3 jmp helper, helper iret at 6, two wrappers, out-of-range iret, table, dispatcher
        body = bytearray(b"\xe9\x00\x00\xe9\x00\x00")
        body += b"\xcf"                      # +6 helper
        body += b"\x0e\xcf" + b"\x0e\xcf"    # +7, +9 wrappers
        body += b"\xcf"                      # +0xB otherwise
        table = len(body)
        body += struct.pack("<2H", 7, 9)
        dispatch = len(body)
        body += b"\x83\xfb\x01\x77" + bytes([(0xB - (dispatch + 5)) & 0xFF])
        body += b"\xd1\xe3\x2e\xff\xa7" + struct.pack("<H", table)
        struct.pack_into("<h", body, 1, dispatch - 3)
        struct.pack_into("<h", body, 4, 6 - 6)
        got_table, rows, got_dispatch, helper = D.alfx_entries(bytes(body))
        self.assertEqual((got_table, rows, got_dispatch, helper), (table, [(0, 7), (1, 9)], dispatch, 6))


if __name__ == "__main__":
    unittest.main()
