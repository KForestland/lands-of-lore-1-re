import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from lol1_xmi_writer import CHUNK, read_chunks, read_events, write_chunks, write_events


class XmiWriteTests(unittest.TestCase):
    def test_event_delay_width_and_post_end_byte(self):
        original = b"\x01\x7f\x91\x20\x30\x80\x05\xff\x2f\x00\x35"
        rows, tail = read_events(original)
        self.assertEqual(rows[0]["delay"], [1, 127])
        self.assertEqual(rows[0]["duration"], (5, 2))
        self.assertEqual(write_events(rows, tail), original)
        rows[0]["duration"] = (6, 2)
        self.assertEqual(write_events(rows, tail), original[:6] + b"\x06" + original[7:])

    def test_chunks_keep_padding_and_opaque_payloads(self):
        frame = CHUNK.pack(b"TEST", 1) + b"xb"
        fields = b"XMID" + frame
        source = CHUNK.pack(b"FORM", len(fields)) + fields
        chunks = read_chunks(source)
        self.assertEqual(chunks[0][0][1][1][0], [(b"TEST", b"x", b"b")])
        self.assertEqual(write_chunks(*chunks), source)
