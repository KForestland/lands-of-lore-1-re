"""Synthetic witnesses for the format writers."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from lol1_pak_writer import write_pak
from lol1lib import pak_entries


class PakRoundTrip(unittest.TestCase):
    def test_order_duplicates_and_terminator(self):
        archive = write_pak([("a", b"1"), ("a", b""), ("\u00e9", b"23")])
        self.assertEqual(pak_entries(archive), [("a", 27, 1), ("a", 28, 0), ("\u00e9", 28, 2)])
        self.assertEqual(archive[18:27], struct.pack("<I5x", 30))
        self.assertEqual(archive[27:], b"123")

    def test_invalid_names_and_final_empty_entry(self):
        for members in ([], [("", b"a")], [("a\0b", b"a")], [("a", b"")]):
            with self.subTest(members=members), self.assertRaises(ValueError):
                write_pak(members)


class CompressionRoundTrip(unittest.TestCase):
    def test_frame4_literals_fills_references_and_end(self):
        from lol1_compression_writer import encode_frame4, encode_frame4_matches
        from lol1lib import decode_frame4
        for data in (b"", bytes(range(256)), b"\xff" * 70000, bytes(range(19)) * 1500):
            for encoder in (encode_frame4, encode_frame4_matches):
                with self.subTest(encoder=encoder.__name__, length=len(data)):
                    self.assertEqual(decode_frame4(encoder(data), len(data) + 1), data)

    def test_wsa_delta_skip_and_closing_record(self):
        from collections import Counter
        from lol1_compression_writer import encode_delta, encode_frame4, write_wsa
        from wsa_extract import delta_xor, frames
        before = bytes(40000)
        after = before[:-1] + b"\x17"
        out = bytearray(before)
        self.assertTrue(delta_xor(out, encode_delta(before, after), len(out)))
        self.assertEqual(out, after)

        start = bytes(4)
        frame = b"\x01\x02\0\0"
        chunks = [encode_frame4(encode_delta(before, after))
                  for before, after in ((start, frame), (frame, start))]
        header = struct.pack("<HhhHHHH3I", 1, 0, 0, 2, 2, 16, 0, 26,
                             26 + len(chunks[0]), 26 + sum(map(len, chunks)))
        counts = Counter()
        self.assertEqual(list(frames(write_wsa(header + b"".join(chunks), counts))), [(0, frame, True)])
        self.assertEqual(counts["wsa deltas"], 2)

    def test_shape_reads_palette_and_long_transparent_run(self):
        from collections import Counter
        from lol1_compression_writer import write_shp
        from shp_renderer import read_shp
        palette = bytes([0, 29]) + bytes(14)
        lines = bytes([1, 0, 255, 0, 4])
        header = struct.pack("<HIHBHBHH", 1, 4, 3, 1, 260, 1, 10 + 16 + len(lines), len(lines))
        original = header + palette + lines
        rebuilt = write_shp(original, Counter())
        self.assertEqual(read_shp(rebuilt)[0]["pixels"], bytes([29]) + bytes(259))
        self.assertTrue(read_shp(rebuilt)[0]["exact"])
