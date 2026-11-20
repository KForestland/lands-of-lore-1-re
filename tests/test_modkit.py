"""Mod kit on synthetic files: unpack, edit, build and verify, refusals and errors."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from decode_dialogue import decode_raw, decode_string1, decode_string2, encode_string, file_strings
from lol1_pak_writer import write_pak
from lol1_script_writer import write_strings
from lol1lib import pak_entries

ARCHIVE = ".PAK"
LINES = ["Welcome to the test keep.\r", "König of the test"]


def make_game(folder):
    stored = [encode_string(line.encode("cp437")).decode("latin-1") for line in LINES]
    first = 2 * len(stored)
    offsets = [first, first + len(stored[0]) + 1]
    text = write_strings({"offsets": offsets, "strings": stored + [""]}, "<")
    (folder / "L01.PAK").write_bytes(write_pak([("LEVEL01.ENG", text), ("OTHER.DAT", bytes(range(40)))]))


def edit(edits):
    name, document = next((n, d) for n, d in edits.items() if d["key"] == "LEVEL01.ENG")
    assert document["value"][:2] == LINES
    document["value"][0] = "Welcome to the much longer test castle.\r"
    return name, document


def check_edit(test, game, out):
    members = {}
    for path in (game, out):
        raw = (path / "L01.PAK").read_bytes()
        members[path] = {name: raw[at:at + size] for name, at, size in pak_entries(raw)}
    test.assertEqual(members[game]["OTHER.DAT"], members[out]["OTHER.DAT"])
    lines = [decode_raw(raw) for raw in file_strings(members[out]["LEVEL01.ENG"])]
    test.assertEqual(lines, ["Welcome to the much longer test castle.\n", "König of the test"])


class BigramText(unittest.TestCase):
    def test_encode_inverts_decode(self):
        for text in (b"Welcome to the test keep.", "König".encode("cp437"), b""):
            stored = encode_string(text)
            self.assertEqual(decode_string2(decode_string1(stored)), text)
        self.assertLess(len(encode_string(b"the stone and the rose")), 22)
        for text in (b"\xff", b"\x1bA"):
            with self.assertRaises(ValueError):
                encode_string(text)



class ModKit(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="mod kit ")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.game = self.root / "my game"
        self.game.mkdir()
        make_game(self.game)
        self.before = {p: p.read_bytes() for p in self.game.rglob("*") if p.is_file()}
        self.work = self.root / "work"
        self.run_kit("unpack", self.game, self.work)

    def tearDown(self):
        self.assertEqual({p: p.read_bytes() for p in self.game.rglob("*") if p.is_file()}, self.before)

    def run_kit(self, *args, ok=True):
        run = subprocess.run([sys.executable, str(TOOLS / "modkit.py"), *map(str, args)],
                             capture_output=True, text=True, cwd=self.root)
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        if not ok:
            self.assertNotIn("Traceback", run.stderr)
            self.assertEqual(len(run.stderr.strip().splitlines()), 1, run.stderr)
        return run.stdout + run.stderr

    def edits(self):
        return {path.name: json.loads(path.read_text(encoding="utf-8"))
                for path in sorted((self.work / "edits").iterdir())}

    def save(self, name, document):
        (self.work / "edits" / name).write_text(json.dumps(document), encoding="utf-8")

    def test_unchanged_build_is_byte_identical(self):
        out = self.root / "out"
        self.assertIn("0 changed", self.run_kit("build", self.game, self.work, out))
        self.assertIn("0 changed", self.run_kit("verify", self.game, self.work, out))
        for path in out.rglob("*"):
            if path.is_file():
                self.assertEqual(path.read_bytes(), (self.game / path.relative_to(out)).read_bytes())

    def test_edit_builds_and_reads_back(self):
        name, document = edit(self.edits())
        self.save(name, document)
        out = self.root / "out"
        self.assertIn("1 changed", self.run_kit("build", self.game, self.work, out))
        self.assertIn("1 changed", self.run_kit("verify", self.game, self.work, out))
        check_edit(self, self.game, out)
        target = out / document["file"]
        damaged = bytearray(target.read_bytes())
        damaged[-1] ^= 0xFF
        target.write_bytes(bytes(damaged))
        self.assertIn("differs", self.run_kit("verify", self.game, self.work, out, ok=False))

    def test_refused_outputs(self):
        archives = self.root / "archives"
        archives.mkdir()
        shutil.copy(next(p for p in self.game.rglob("*") if p.suffix.upper() == ARCHIVE), archives)
        for place in (self.game, self.game / "out", self.work, self.work / "out", archives / "out",
                      TOOLS.parent / "out"):
            self.assertIn("outside", self.run_kit("build", self.game, self.work, place, ok=False))
            self.assertFalse((self.game / "out").exists() or (archives / "out").exists())
        self.assertIn("outside", self.run_kit("unpack", self.game, self.game / "work", ok=False))

    def test_errors_are_one_line(self):
        out = self.root / "out"
        self.assertIn("not found", self.run_kit("unpack", self.root / "missing", self.root / "w", ok=False))
        empty = self.root / "empty"
        empty.mkdir()
        self.assertIn("nothing to unpack", self.run_kit("unpack", empty, self.root / "w", ok=False))
        name = sorted(self.edits())[0]
        (self.work / "edits" / name).write_text("{", encoding="utf-8")
        self.assertIn("not valid JSON", self.run_kit("build", self.game, self.work, out, ok=False))
        (self.work / "edits" / name).unlink()
        self.assertIn("is missing", self.run_kit("build", self.game, self.work, out, ok=False))
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
