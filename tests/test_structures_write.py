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
