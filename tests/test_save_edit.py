"""Save editor on synthetic LoL1 slots: fields, read-back, refused outputs and one-line errors."""
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import save_edit

NUMBER = "money"


def source_slot():
    original = bytearray(0x1427F)
    original[60:76] = b"CD04\0V CD1.02 D\0"
    original[0x269] = 1
    original[0x460] = 4
    return bytes(original)


class SaveEditTest(unittest.TestCase):
    def test_party_money_and_oil(self):
        raw = source_slot()
        moved, change = save_edit.edit(raw, "block", "113")
        self.assertEqual(change, "block 0 -> 113")
        self.assertEqual(struct.unpack_from("<3H", moved, 0x254), (113, 4480, 896))
        self.assertEqual(moved[0x25A:], raw[0x25A:])
        oiled, change = save_edit.edit(moved, "lamp-oil", "26")
        self.assertEqual(change, "lamp-oil 0 -> 26")
        self.assertEqual(oiled[0x460:0x463], bytes([4, 26, 4]))
        self.assertEqual(oiled[0x463:], raw[0x463:])
        rich, change = save_edit.edit(raw, "money", "5000")
        self.assertEqual(change, "money 0 -> 5000")
        self.assertEqual(struct.unpack_from("<H", rich, 0x254 + 528)[0], 5000)
        with self.assertRaisesRegex(ValueError, "0 to 1023"):
            save_edit.edit(raw, "block", "1024")
        self.assertIn("CONFIRMED", save_edit.status(raw, "block"))
        self.assertIn("UNCONFIRMED", save_edit.status(raw, "money"))

    def test_floppy_offsets(self):
        raw = bytearray(0x1426E)
        raw[60:65] = b".13\0_"
        result, change = save_edit.edit(bytes(raw), "facing", "3")
        self.assertEqual(change, "facing 0 -> 3")
        self.assertEqual(result[0x258:0x25A], b"\x03\0")
        self.assertEqual(result[0x25A:], raw[0x25A:])
        self.assertIn("UNCONFIRMED", save_edit.status(bytes(raw), "facing"))


WORDS = ("Traceback", "Errno", "int()", "codec", "Expecting")


class OutputTest(unittest.TestCase):
    def run_edit(self, *args, ok=True):
        run = subprocess.run([sys.executable, str(ROOT / "tools" / "save_edit.py"), "set", *map(str, args)],
                             capture_output=True, text=True, cwd=tempfile.gettempdir())
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        if not ok:
            self.assertEqual(len(run.stderr.strip().splitlines()), 1, run.stderr)
            for word in WORDS:
                self.assertNotIn(word, run.stderr)
        return run.stdout + run.stderr

    def test_new_file_only(self):
        with tempfile.TemporaryDirectory(prefix="save edit ") as temp:
            saves, out = Path(temp) / "my saves", Path(temp) / "edited"
            saves.mkdir()
            out.mkdir()
            original = saves / "slot one"
            raw = source_slot()
            original.write_bytes(raw)
            said = self.run_edit(original, "name", "Synthetic", "--out", out / "new slot")
            self.assertIn("name ", said)
            self.assertIn(" -> 'Synthetic'", said)
            self.assertEqual(original.read_bytes(), raw)
            self.assertEqual((out / "new slot").read_bytes(), b"Synthetic\0" + raw[10:])
            for args, message in (
                    ((original, "name", "Synthetic", "--out", original), "outside"),
                    ((original, "name", "Synthetic", "--out", saves / "beside"), "outside"),
                    ((original, "name", "Synthetic", "--out", out / "new slot"), "already exists"),
                    ((original, "name", "Sünthetic", "--out", out / "a"), "plain ASCII"),
                    ((original, NUMBER, "lots", "--out", out / "b"), "whole number"),
                    ((original, NUMBER, "99999999", "--out", out / "c"), "whole number"),
                    ((saves / "missing", "name", "X", "--out", out / "d"), "save not found"),
                    ((original, "name", "X", "--out", out / "no folder" / "e"), "does not exist")):
                said = self.run_edit(*args, ok=False)
                self.assertIn(message, said, args)
            damaged = saves / "damaged"
            damaged.write_bytes(raw[:200])
            self.run_edit(damaged, "name", "X", "--out", out / "g", ok=False)
            self.assertEqual(sorted(p.name for p in out.iterdir()), ["new slot"])
            self.assertEqual(original.read_bytes(), raw)

    def test_leading_zero_and_hex(self):
        self.assertEqual(save_edit.integer("08", 0, 9), 8)
        self.assertEqual(save_edit.integer("0x10", 0, 99), 16)


if __name__ == "__main__":
    unittest.main()
