"""Run the public tools together against files made entirely in this test suite."""
import csv
from importlib.util import find_spec
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

from tests import kit_fixture as fixture
from tests.test_modkit import edit

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def files(folder):
    return {path.relative_to(folder).as_posix(): path.read_bytes()
            for path in folder.rglob("*") if path.is_file()}


class ToolKit(unittest.TestCase):
    lowercase = False

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="tool kit ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.game = self.root / "Test Land"
        self.slot = self.game / "slot.dat"
        self.slot.write_bytes(fixture.make_fixture(self.game))
        if self.lowercase:
            fixture.lowercase(self.game)
        self.original = files(self.game)
        self.addCleanup(lambda: self.assertEqual(files(self.game), self.original))
        self.data = self.game / (fixture.DATA.lower() if self.lowercase else fixture.DATA)
        self.base = self.data if fixture.DATA == "DATA" else self.game
        self.archive = fixture.ARCHIVE.lower() if self.lowercase else fixture.ARCHIVE

    def run_tool(self, tool, *args, ok=True):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        run = subprocess.run([sys.executable, str(TOOLS / tool), *map(str, args)],
                             capture_output=True, encoding="utf-8", env=env, cwd=self.root, timeout=90)
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        return run.stdout if ok else run.stderr

    def job(self, *args):
        return self.run_tool("lol.py", *args)

    def test_all_job_help(self):
        self.assertIn("Choose a job", self.job("--help"))
        for name in fixture.JOBS:
            with self.subTest(job=name):
                self.assertIn(f"usage: lol.py {name}", self.job(name, "--help"))

    def test_read_only_and_media_jobs(self):
        fixture.inspect_jobs(self)

    def test_mod_patch_and_private_undo(self):
        work, built, applied, reverted = [self.root / name for name in ("work", "built", "applied", "reverted")]
        self.assertIn("editable entries", self.job("mod", "unpack", self.game, work))
        edits = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted((work / "edits").iterdir())}
        name, document = edit(edits)
        (work / "edits" / name).write_text(json.dumps(document), encoding="utf-8")
        self.assertIn("1 changed", self.job("mod", "build", self.base, work, built))
        self.assertIn("1 changed", self.job("mod", "verify", self.data, work, built))
        expected = (built / self.archive).read_bytes()
        original = (self.base / self.archive).read_bytes()
        self.assertNotEqual(expected, original)

        share = self.root / "share.json"
        self.assertIn("data patch", self.job("patch", "make", built, "--data", self.base,
                                           "--title", "Fixture change", "--out", share))
        patch = json.loads(share.read_text(encoding="utf-8"))
        self.assertEqual(patch["format"], "lol-patch-3")
        if self.lowercase:
            # A patch authored against an uppercase installation still applies.
            for change in patch["changes"]:
                change["file"] = change["file"].upper()
            share.write_text(json.dumps(patch), encoding="utf-8")
        self.assertNotIn('"old":', share.read_text(encoding="utf-8"))
        self.assertIn("keep undo.json private", self.job("patch", "apply", share, "--data", self.base, "--out", applied))
        self.assertEqual((applied / self.archive).read_bytes(), expected)

        changed = self.root / "another copy"
        shutil.copytree(self.base, changed)
        (changed / self.archive).write_bytes(expected)
        undo = applied / "undo.json"
        self.assertIn("1 file", self.job("patch", "apply", undo, "--data", changed, "--out", reverted))
        self.assertEqual((reverted / self.archive).read_bytes(), original)

    def test_translate_edit_build_and_verify(self):
        work, built = self.root / "translation", self.root / "translated files"
        self.job("translate", "export", "--data", self.game, "--out", work)
        manifest = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
        replacement = "A new test line"
        match = None
        for entry in manifest["tables"]:
            sheet = work / entry["name"]
            with sheet.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            for row in rows[1:]:
                if row[1] == fixture.TRANSLATE_FROM:
                    self.assertIsNone(match)
                    row[2] = replacement
                    match = entry["file"]
                    with sheet.open("w", encoding="utf-8-sig", newline="") as stream:
                        csv.writer(stream).writerows(rows)
        self.assertIsNotNone(match)
        self.job("translate", "build", "--data", self.game, "--work", work, "--out", built)
        self.job("translate", "verify", "--data", self.game, "--work", work, "--out", built)
        self.assertEqual(set(files(built)), {match})
        self.assertNotEqual((built / match).read_bytes(), (self.base / match).read_bytes())

    def test_level_editor_check(self):
        self.assertIn("byte-identical", self.run_tool("level_edit.py", "--data", self.game, "--check"))

    def test_level_editor_refuses_a_different_source(self):
        edits = self.root / "foreign.json"
        edits.write_text(json.dumps(fixture.foreign_level_edit()), encoding="utf-8")
        out = self.root / "foreign result"
        error = self.run_tool("level_edit.py", edits, "--data", self.data, "--out", out, ok=False)
        self.assertIn("different", error)
        self.assertFalse(out.exists())

    def test_level_viewer_check_and_page(self):
        if fixture.DATA == "DATA" and find_spec("PIL") is None:
            self.skipTest("LoL1's level viewer requires Pillow")
        self.assertIn("CHECK level viewer", self.job("level", "--data", self.game, "--level", fixture.LEVEL, "--check"))
        out = self.root / "level pages"
        self.assertIn("Wrote 1 level page", self.job("level", "--data", self.data.with_name(fixture.DATA),
                                                    "--level", fixture.LEVEL, "--out", out))
        page, = out.glob("*.html")
        self.assertIn("level plan", page.read_text(encoding="utf-8").lower())

    def test_save_set_and_page(self):
        new_slot = self.root / "changed slot.dat"
        self.job("save", "set", self.slot, fixture.SAVE_FIELD, "9029", "--out", new_slot)
        at = fixture.SAVE_AT
        original = self.original["slot.dat"]
        self.assertEqual(new_slot.read_bytes(), original[:at] + struct.pack("<H", 9029) + original[at + 2:])
        page = self.root / "saved game.html"
        self.job("save", "page", self.slot, "--out", page)
        self.assertIn(fixture.SAVE_FIELD, page.read_text(encoding="utf-8").lower())


class LowercaseToolKit(ToolKit):
    lowercase = True
