"""File reader commands report bad inputs without Python tracebacks."""
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"


class ReaderErrors(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.data = self.root / "data"
        self.data.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if key not in ("LOL1_DATA", "LOL2_DAT", "LOL3_DAT")}

    def assert_bad(self, tool, *args):
        run = subprocess.run([sys.executable, str(TOOLS / tool), *map(str, args)],
                             cwd=self.root, env=self.env, capture_output=True, text=True, timeout=10)
        self.assertNotEqual(run.returncode, 0, run.stdout)
        output = run.stderr or run.stdout
        self.assertNotIn("Traceback", run.stdout + run.stderr)
        self.assertEqual(len(output.strip().splitlines()), 1, output)

    def bad_files(self, name, short, tool, *args):
        file = self.data / name
        for kind, content in (("empty", b""), ("short", short)):
            with self.subTest(tool=tool, input=kind):
                file.write_bytes(content)
                self.assert_bad(tool, *args)

    def test_missing_data_folder(self):
        self.assert_bad("check_all.py", "--data", self.root / "missing")

    def test_archive(self):
        self.bad_files("A.PAK", struct.pack("<I", 32) + b"A\0",
                       "pak_reader.py", "--data", self.data, "list", "A.PAK")

    def test_audio(self):
        head = b"Creative Voice File\x1a" + struct.pack("<HHH", 26, 0x114, 0)
        self.bad_files("A.VOC", head + b"\x01\x05\0\0\x01\0",
                       "voc_reader.py", "--data", self.data, "A.VOC")

    def test_bitmap(self):
        short = struct.pack("<HBBIH", 12, 0, 0, 4, 0) + b"x"
        self.bad_files("A.CPS", short, "cps_reader.py", "--data", self.data, "A.CPS")

    def test_palette(self):
        self.bad_files("A.PAL", b"\x10\x20", "palette_reader.py", "--data", self.data, "A.PAL")

    def test_level(self):
        member = b"LEVEL1.CMZ\0"
        begin = 8 + len(member)
        for payload in (b"", struct.pack("<I", 130) + b"x"):
            pak = struct.pack("<I", begin) + member + struct.pack("<I", 0) + payload
            (self.data / "L01.PAK").write_bytes(pak)
            with self.subTest(size=len(payload)):
                self.assert_bad("cmz_analyzer.py", "--data", self.data)

    def test_executable(self):
        self.bad_files("MAIN.EXE", b"MZ\x01", "exe_tables.py", "--data", self.data)

    def test_script(self):
        self.bad_files("A.INI", b"FORM\0\0\0\x12EMC2",
                       "emc2_decompile.py", self.data / "A.INI")

    def test_save(self):
        self.bad_files("_SAVE000.DAT", b"short", "save_reader.py", self.data / "_SAVE000.DAT")
