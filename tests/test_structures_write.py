"""Synthetic witnesses for script and field assembly."""
import json
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from lol1_script_writer import assemble, listing


def form(kind, chunks, bias):
    body = kind + b"".join(tag + struct.pack(">I", len(data)) + data + pad for tag, data, pad in chunks)
    return b"FORM" + struct.pack(">I", 8 + len(body) - bias) + body


class ScriptAssembly(unittest.TestCase):
    def test_duplicate_mnemonic_uses_original_opcode(self):
        original = form(b"EMC2", [(b"ORDR", struct.pack(">H", 0), b""),
                                  (b"DATA", struct.pack(">3H", 0xABCD, 0x44FF, 0x1200), b"")], 0)
        source = json.loads(json.dumps(listing(original)))
        self.assertEqual(assemble(source), original)
        source["chunks"][1]["fields"][1]["argument"] = -2
        self.assertEqual(assemble(source)[-4:], b"\x44\xfe\x12\x00")

    def test_tim_unknown_tail_and_alignment_byte(self):
        original = form(b"AVFS", [(b"AVTL", struct.pack("<5H", 1, 3, 7, 0x118, 0xCDCD), b""),
                                  (b"TEXT", b"\x02\0AB\0", b"\xa5")], 12)
        source = listing(original)
        self.assertEqual(source["chunks"][0]["fields"][-1], {"at": 4, "unread": [0xCDCD]})
        self.assertEqual(assemble(source), original)

    def test_output_refused_beside_game_archives(self):
        import subprocess
        import tempfile
        tool = Path(__file__).resolve().parents[1] / "tools" / "lol1_script_writer.py"
        with tempfile.TemporaryDirectory() as folder:
            data = Path(folder) / "DATA"
            (data / "ENG").mkdir(parents=True)
            (data / "FAKE.PAK").write_bytes(b"")
            listing_path = Path(folder) / "listing.json"
            script = form(b"EMC2", [(b"ORDR", struct.pack(">H", 0), b""),
                                    (b"DATA", struct.pack(">3H", 0xABCD, 0x44FF, 0x1200), b"")], 0)
            listing_path.write_text(json.dumps(listing(script)))
            for target in (data / "NEW.INF", data / "ENG" / "NEW.INF"):
                done = subprocess.run([sys.executable, str(tool), str(listing_path), "--out", str(target)],
                                      capture_output=True, text=True, env={"PATH": ""})
                self.assertEqual(done.returncode, 2)
                self.assertFalse(target.exists())
            fine = Path(folder) / "NEW.INF"
            subprocess.run([sys.executable, str(tool), str(listing_path), "--out", str(fine)], check=True,
                           capture_output=True, env={"PATH": ""})
            self.assertTrue(fine.exists())


class LevelFieldAssembly(unittest.TestCase):
    def test_maze_keeps_skipped_block_bytes_and_frame4_choices(self):
        from lol1_compression_writer import encode_frame4
        from lol1_level_writer import parse_maze, write_maze
        raw = struct.pack("<3H", 32, 32, 9) + b"\x01\x02\x03\x04EXTRA" * 1024
        compressed = encode_frame4(raw)
        blob = struct.pack("<HBBIH", len(compressed) + 8, 4, 0, len(raw), 0) + compressed
        fields = parse_maze(blob)
        self.assertEqual(fields[3][10], ((1, 2, 3, 4), b"EXTRA"))
        self.assertEqual(write_maze(fields), blob)

    def test_wall_word_high_bytes_and_duplicate_text_offsets(self):
        from lol1_level_writer import parse_walls, write_walls
        from lol1_script_writer import binary_strings, write_strings
        wall = struct.pack("<3Hh3H", 2, 7, 0x1211, -2, 0x4322, 0x6533, 0xFFFF)
        self.assertEqual(parse_walls(wall)[1][0][1], 0x1211)
        self.assertEqual(write_walls(parse_walls(wall)), wall)
        text = b"\x04\x00\x04\x00x\0tail"
        self.assertEqual(write_strings(binary_strings(text, "<"), "<"), text)

    def test_edited_maze_wall_compresses_afresh_and_reads_back(self):
        from lol1_compression_writer import encode_frame4
        from lol1_level_writer import parse_maze, write_maze
        raw = struct.pack("<3H", 32, 32, 4) + bytes(range(4)) * 1024
        compressed = encode_frame4(raw)
        blob = struct.pack("<HBBIH", len(compressed) + 8, 4, 0, len(raw), 0) + compressed
        header, palette, grid, rows, storage = parse_maze(blob)
        rows[7] = ((9, 1, 2, 3), b"")
        edited = write_maze((header, palette, grid, rows, storage))
        self.assertNotEqual(edited, blob)
        self.assertEqual(parse_maze(edited)[3][7][0], (9, 1, 2, 3))
        self.assertEqual(struct.unpack_from("<H", edited)[0], len(edited) - 2)

    def test_edited_string_moves_later_offsets(self):
        from decode_dialogue import file_strings
        from lol1_level_writer import replace_string
        from lol1_script_writer import binary_strings, write_strings
        text = b"\x06\x00\x08\x00\x0a\x00a\0b\0c\0"
        edited = write_strings(replace_string(binary_strings(text, "<"), 1, "bbb"), "<")
        self.assertEqual(file_strings(edited), [b"a", b"bbb", b"c"])
