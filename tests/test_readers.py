import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from emc2_decompile import pak_entries, read_script
from lol1lib import decode_frame4
from save_reader import read_original_save


class ReaderTests(unittest.TestCase):
    def test_pak_directory(self):
        name, payload = b"TEST.TXT\0", b"test"
        start = 4 + len(name) + 4
        archive = struct.pack("<I", start) + name + struct.pack("<I", 0) + payload
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.pak"
            path.write_bytes(archive)
            self.assertEqual(list(pak_entries(path)), [("TEST.TXT", start, len(payload))])

    def test_frame4_literal_overlap_and_fill(self):
        packed = b"\x82ab\x00\x02\xfe\x02\x00!\x80"
        self.assertEqual(bytes(decode_frame4(packed, 12)), b"ababa!!")

    def test_emc2_entry_and_strings(self):
        def chunk(tag, body):
            return struct.pack(">4sI", tag, len(body)) + body + b"\0" * (len(body) % 2)

        chunks = (
            chunk(b"ORDR", struct.pack(">H", 0))
            + chunk(b"DATA", struct.pack(">3H", 0, 0x43FF, 0x4E00))
            + chunk(b"TEXT", b"\0\x02ok\0")
        )
        data = b"FORM" + struct.pack(">I", 4 + len(chunks)) + b"EMC2" + chunks
        script = read_script(data)
        self.assertEqual(script.entries, {0: [0]})
        self.assertEqual(script.strings, [(2, b"ok")])
        self.assertEqual([(i.opcode, i.argument) for i in script.instructions], [(3, -1), (14, 0)])
        with self.assertRaises(ValueError):
            read_script(data[:-1])

    def test_floppy_save_header_and_options(self):
        data = bytearray(65 + 4 * 130 + 557 + 400 * 16 + 30 * 2500)
        data[:6] = b"Sample"
        data[60:63] = b".13"
        struct.pack_into("<H", data, 65 + 4 * 130 + 10, 0x23)
        save = read_original_save(data)
        self.assertEqual((save["edition"], save["description"], save["tag"]), ("floppy", "Sample", ".13"))
        self.assertTrue(save["size_ok"])
        self.assertEqual(save["state"]["options"]["difficulty"], 2)
        self.assertTrue(save["state"]["options"]["music"])
