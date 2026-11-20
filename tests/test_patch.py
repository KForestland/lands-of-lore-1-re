"""Patch tool on synthetic files: make, apply, undo, file names, program patches and errors.

The same file is used in the three repositories; the synthetic game comes from test_modkit.py.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TESTS = Path(__file__).resolve().parent
TOOLS = TESTS.parent / "tools"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TESTS))

import modkit
import patch as patch_tool
from test_modkit import check_edit, edit, make_game

GAME = modkit.GAME
PROGRAM = {"lol1": "MAIN.EXE", "lol2": "LOLG.DAT", "lol3": "LOL3.DAT"}[GAME]
TEXT = b"Synthetic program text: Hello adventurer.\0"
WORDS = ("Traceback", "Errno", "int()", "codec", "Expecting", "JSONDecodeError")


def files(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


def program_image(text=TEXT):
    return b"MZ" + bytes(range(62)) + bytes(64) + text + bytes(32)


class PatchTool(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="patch tool ")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.game = self.root / "my game"
        self.game.mkdir()
        make_game(self.game)
        self.before = files(self.game)

    def tearDown(self):
        self.assertEqual(files(self.game), self.before)

    def run_tool(self, tool, *args, ok=True):
        run = subprocess.run([sys.executable, str(TOOLS / tool), *map(str, args)],
                             capture_output=True, text=True, cwd=self.root)
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        if not ok:
            self.assertEqual(len(run.stderr.strip().splitlines()), 1, run.stderr)
            for word in WORDS:
                self.assertNotIn(word, run.stderr)
        return run.stdout + run.stderr

    def built(self, game, data=None):
        """Unpack the game with the mod kit, make the test edit and build it."""
        work, out = self.root / "my work", self.root / "my output"
        self.run_tool("modkit.py", "unpack", data or game, work)
        name, document = edit({p.name: json.loads(p.read_text(encoding="utf-8"))
                               for p in (work / "edits").iterdir()})
        (work / "edits" / name).write_text(json.dumps(document), encoding="utf-8")
        self.run_tool("modkit.py", "build", data or game, work, out)
        return out

    def install(self, game, output, name):
        copy = self.root / name
        shutil.copytree(game, copy)
        for path, raw in files(output).items():
            if path != patch_tool.UNDO:
                (copy / path).write_bytes(raw)
        return copy

    def test_number_patch_applies_and_undoes(self):
        out = self.built(self.game)
        patch_file = self.root / "my patch.json"
        said = self.run_tool("patch.py", "make", "--data", self.game, out, "--title", "Test edit",
                             "--out", patch_file)
        patch = json.loads(patch_file.read_text(encoding="utf-8"))
        self.assertEqual((patch["format"], patch["game"], patch["kind"]), ("lol-patch-3", GAME, "data"))
        self.assertTrue(all("old" not in change and "old_sha256" in change for change in patch["changes"]))
        self.assertIn("in 1 file (", said)
        self.assertNotIn("1 files", said)
        patched = self.root / "patched files"
        said = self.run_tool("patch.py", "apply", "--data", self.game, patch_file, "--out", patched)
        self.assertIn("apply: 1 file (", said)
        check_edit(self, self.game, patched)
        undo = json.loads((patched / patch_tool.UNDO).read_text(encoding="utf-8"))
        self.assertEqual(undo["format"], "lol-patch-undo-1")
        self.assertIn("Do not share", undo["description"])
        self.assertTrue(all("old" not in change for change in undo["changes"]))
        copy = self.install(self.game, patched, "game copy")
        # The same patch on the patched copy is refused: the old bytes are gone.
        again = self.root / "again"
        said = self.run_tool("patch.py", "apply", "--data", copy, patch_file, "--out", again, ok=False)
        self.assertIn("already applied", said)
        self.assertFalse(again.exists())
        # The positional game folder is an alias for --data.
        restored = self.root / "restored files"
        self.run_tool("patch.py", "apply", copy, patched / patch_tool.UNDO, "--out", restored)
        copy = self.install(copy, restored, "game copy restored")
        self.assertEqual(files(copy), self.before)

    def test_names_start_at_the_installation_folder(self):
        # LoL2 and LoL3 ship some archives twice, in DAT and beside it; LoL1's CD keeps
        # its archives in DATA. A patch made from either folder names the same file.
        if GAME == "lol1":
            install = self.root / "lol1 install"
            inner = install / "DATA"
            shutil.copytree(self.game, inner)
            (install / "INSTALL.EXE").write_bytes(b"MZ")
            prefix = ""
        else:
            install, inner, prefix = self.game, self.game / "DAT", "DAT/"
        out = self.built(install, inner)
        for path in list(files(inner)):
            if GAME != "lol1" and "/" not in path:
                (install / path).write_bytes((inner / path).read_bytes())  # identical duplicate
        self.before = files(self.game)
        # The changed files laid out as in the inner folder and as in the installation folder.
        layouts = {}
        for layout, rename in (("inner", lambda p: p[len("DAT/"):] if GAME != "lol1" else p),
                               ("install", lambda p: "DATA/" + p if GAME == "lol1" else p)):
            folder = layouts[layout] = self.root / f"changed {layout}"
            for path, raw in files(out).items():
                if GAME != "lol1" and not path.startswith("DAT/"):
                    continue
                target = folder / rename(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
        made = []
        for number, (data, folder) in enumerate(((inner, layouts["inner"]), (install, layouts["install"]))):
            patch_file = self.root / f"patch {number}.json"
            self.run_tool("patch.py", "make", "--data", data, folder, "--title", "Test edit",
                          "--out", patch_file)
            made.append(json.loads(patch_file.read_text(encoding="utf-8")))
        self.assertEqual(made[0], made[1])
        names = sorted({change["file"] for change in made[0]["changes"]})
        self.assertTrue(names and all(n.startswith(prefix) and n.count("/") == prefix.count("/")
                                      for n in names), names)
        if GAME != "lol1":
            # Both copies changed, laid out as modkit.py build writes them: two files, never one.
            both = self.root / "changed both copies"
            shutil.copytree(layouts["install"], both)
            for path, raw in files(layouts["inner"]).items():
                (both / path).write_bytes(raw)
            self.run_tool("patch.py", "make", "--data", inner, both, "--title", "Both copies",
                          "--out", self.root / "both.json")
            twice = json.loads((self.root / "both.json").read_text(encoding="utf-8"))
            doubled = sorted({change["file"] for change in twice["changes"]})
            self.assertEqual(doubled, sorted({n[len(prefix):] for n in names} | set(names)))
        for number, data in enumerate((install, inner)):
            patched = self.root / f"patched {number}"
            self.run_tool("patch.py", "apply", "--data", data, self.root / "patch 0.json", "--out", patched)
            self.assertEqual(sorted(p for p in files(patched) if p != patch_tool.UNDO), names)
        # No output inside the installation folder, also when given its DAT or DATA folder.
        self.run_tool("patch.py", "apply", "--data", inner, self.root / "patch 0.json",
                      "--out", install / "new", ok=False)
        self.assertFalse((install / "new").exists())

    def test_program_patch(self):
        (self.game / PROGRAM).write_bytes(program_image())
        self.before = files(self.game)
        changed = self.root / "changed program"
        changed.mkdir()
        (changed / PROGRAM).write_bytes(program_image(TEXT.replace(b"Hello", b"Jello")))
        patch_file = self.root / "program patch.json"
        self.run_tool("patch.py", "make", "--data", self.game, changed, "--title", "One letter",
                      "--out", patch_file)
        patch = json.loads(patch_file.read_text(encoding="utf-8"))
        self.assertEqual(patch["kind"], "program")
        self.assertEqual(set(patch["sha256"]), {PROGRAM})
        self.assertEqual([(c["old_length"], c["old_sha256"], c["new"]) for c in patch["changes"]],
                         [(1, patch_tool.digest(b"H"), "4a")])
        patched = self.root / "patched program"
        self.run_tool("patch.py", "apply", "--data", self.game, patch_file, "--out", patched)
        self.assertEqual((patched / PROGRAM).read_bytes(), (changed / PROGRAM).read_bytes())
        # A program whose bytes differ elsewhere has another SHA-256 and is refused.
        other = self.root / "other version"
        shutil.copytree(self.game, other)
        (other / PROGRAM).write_bytes(program_image() + b"\0")
        refused = self.root / "refused"
        said = self.run_tool("patch.py", "apply", "--data", other, patch_file, "--out", refused, ok=False)
        self.assertIn("SHA-256", said)
        self.assertFalse(refused.exists())
        copy = self.install(self.game, patched, "program copy")
        restored = self.root / "restored program"
        self.run_tool("patch.py", "apply", "--data", copy, patched / patch_tool.UNDO, "--out", restored)
        self.assertEqual((restored / PROGRAM).read_bytes(), program_image())
        # Spans are capped, and a program keeps its length.
        (changed / PROGRAM).write_bytes(program_image(TEXT.replace(b"Synthetic program", b"x" * 17)))
        self.run_tool("patch.py", "make", "--data", self.game, changed, "--title", "Too long",
                      "--out", self.root / "long.json", ok=False)
        (changed / PROGRAM).write_bytes(program_image() + b"\0")
        self.run_tool("patch.py", "make", "--data", self.game, changed, "--title", "Longer",
                      "--out", self.root / "longer.json", ok=False)
        self.assertFalse((self.root / "long.json").exists() or (self.root / "longer.json").exists())

    def test_caps(self):
        def change(old, new, offset=0):
            return patch_tool.record("DAT/X", 0, offset, old, new)
        data = patch_tool.document("data", "T", "D", [change(b"a" * 256, b"b" * 256)])
        patch_tool.check_document(data)
        for changes in ([change(b"a" * 257, b"b")],
                        [change(b"a" * 200, b"b", at * 300) for at in range(21)]):
            with self.assertRaisesRegex(ValueError, "at most"):
                patch_tool.check_document(patch_tool.document("data", "T", "D", changes))
        program = patch_tool.document("program", "T", "D", [change(b"a" * 17, b"b" * 17)], {"DAT/X": "0" * 64})
        with self.assertRaisesRegex(ValueError, "at most 16 bytes"):
            patch_tool.check_document(program)
        program["changes"] = [change(b"a", b"bb")]
        with self.assertRaisesRegex(ValueError, "same number of bytes"):
            patch_tool.check_document(program)

    def test_legacy_patch_stays_readable_and_undoes(self):
        original = program_image()
        (self.game / PROGRAM).write_bytes(original)
        self.before = files(self.game)
        change = {"file": PROGRAM, "entry": 0, "offset": original.index(b"Hello"),
                  "old": b"Hello".hex(), "new": b"Jello".hex()}
        legacy = patch_tool.document("program", "Test", "Legacy test", [change],
                                     {PROGRAM: patch_tool.digest(original)}, version="lol-patch-2")
        path = self.root / "legacy.json"
        path.write_text(json.dumps(legacy), encoding="utf-8")
        out = self.root / "patched legacy"
        self.run_tool("patch.py", "apply", "--data", self.game, path, "--out", out)
        self.assertEqual((out / PROGRAM).read_bytes(), original.replace(b"Hello", b"Jello"))
        undo = self.root / "undid legacy"
        self.run_tool("patch.py", "apply", "--data", out, out / patch_tool.UNDO, "--out", undo)
        self.assertEqual((undo / PROGRAM).read_bytes(), original)

    def test_v3_span_matching_and_trimming_on_resize(self):
        old = b"p" * 1700 + b"Here!Here!" + b"s" * 5300
        new = b"p" * 1700 + b"!!Here!Here!??" + b"s" * 5300
        changes = list(patch_tool.byte_deltas("DAT/X", 0, old, new))
        self.assertEqual([(row["offset"], row["old_length"], row["new"]) for row in changes],
                         [(1700, 0, "2121"), (1710, 0, "3f3f")])
        patch = patch_tool.document("data", "Synthetic", "Resize", changes)
        edits = patch_tool.check_document(patch)["DAT/X"][0]
        output, undo = patch_tool.splice("DAT/X", 0, old, edits)
        self.assertEqual(output, new)
        inverse = patch_tool.document("data", "Undo", "Synthetic", undo, version=patch_tool.UNDO_FORMAT)
        edits = patch_tool.check_document(inverse)["DAT/X"][0]
        self.assertEqual(patch_tool.splice("DAT/X", 0, new, edits)[0], old)
        with self.assertRaisesRegex(ValueError, "does not hold the bytes"):
            patch_tool.splice("DAT/X", 0, new.replace(b"??", b"XX"), edits)

    def test_make_refuses_long_shared_runs(self):
        old, new = b"XABCDEFGHY", b"ZQABCDEFGH"
        original = program_image() + old
        (self.game / PROGRAM).write_bytes(original)
        self.before = files(self.game)
        changed = self.root / "change with a shared run"
        changed.mkdir()
        (changed / PROGRAM).write_bytes(program_image() + new)
        with self.assertRaisesRegex(ValueError, "8 or more shared bytes"):
            patch_tool.make(self.game, changed, "Synthetic", "Shared run")

    def test_v3_span_refuses_equal_edges_and_bad_hash(self):
        change = patch_tool.record("DAT/X", 0, 0, b"aBc", b"aDc")
        patch = patch_tool.document("data", "Synthetic", "Equal edges", [change])
        edits = patch_tool.check_document(patch)["DAT/X"][0]
        with self.assertRaisesRegex(ValueError, "trim matching bytes"):
            patch_tool.splice("DAT/X", 0, b"aBc", edits)
        with self.assertRaisesRegex(ValueError, "does not hold the bytes"):
            patch_tool.splice("DAT/X", 0, b"aEc", edits)
        change["old_sha256"] = "missing"
        with self.assertRaisesRegex(ValueError, "64 lowercase hexadecimal digits"):
            patch_tool.check_document(patch)

    def test_errors_are_one_sentence(self):
        out = self.built(self.game)
        good = self.root / "good.json"
        self.run_tool("patch.py", "make", "--data", self.game, out, "--title", "T", "--out", good)
        patch = json.loads(good.read_text(encoding="utf-8"))
        unchanged = self.root / "unchanged"
        shutil.copytree(self.game, unchanged)
        bad = self.root / "bad.json"
        bad.write_text("{'format': 1,", encoding="utf-8")
        other = self.root / "other game.json"
        other.write_text(json.dumps(dict(patch, game="lol1" if GAME != "lol1" else "lol2")), encoding="utf-8")
        missing = self.root / "missing file.json"
        missing.write_text(json.dumps(dict(patch, changes=[dict(c, file="DAT/NOPE.ARC") for c in patch["changes"]])),
                           encoding="utf-8")
        large = self.root / "large.json"
        large.write_text(json.dumps(dict(patch, changes=[dict(patch["changes"][0], old_length=300)])),
                         encoding="utf-8")
        target = self.root / "never written"
        cases = [
            (("make", "--data", self.game, self.root / "nowhere", "--title", "T"), "changed folder not found"),
            (("make", "--data", self.game, unchanged, "--title", "T"), "no differences"),
            (("make", "--data", self.root / "no game", out, "--title", "T"), "does not exist"),
            (("apply", "--data", self.game, self.root / "nowhere.json"), "patch file not found"),
            (("apply", "--data", self.game, bad), "not a patch file"),
            (("apply", "--data", self.game, other), "this patch is for"),
            (("apply", "--data", self.game, missing), "which is not in"),
            (("apply", "--data", self.game, large), "at most 256 bytes"),
        ]
        for args, message in cases:
            said = self.run_tool("patch.py", *args, "--out", target, ok=False)
            self.assertIn(message, said, args)
            self.assertFalse(target.exists())
        for place in (self.game / "out", self.root / "no folder" / "out", good):
            self.run_tool("patch.py", "apply", "--data", self.game, good, "--out", place, ok=False)
        self.assertFalse((self.game / "out").exists() or (self.root / "no folder").exists())


if __name__ == "__main__":
    unittest.main()
