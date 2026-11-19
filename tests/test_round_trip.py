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
