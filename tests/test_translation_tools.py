"""Data-free copy and browser data checks for the translator and save page."""
import csv
from pathlib import Path
import struct
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import modkit
from modkit_core import local_path
from save_page import render
import translate
from translate_fonts import coverage


def glyph_file():
    # One 1x1 glyph, indexed at zero. The glyph table is followed by widths,
    # two height bytes and one packed pixel.
    return struct.pack("<7H", 26, 0x500, 14, 20, 22, 25, 23) + bytes((
        0x12, 0x10, 0, 0, 1, 1, 25, 0, 1, 0, 1, 1,
    ))


def source(game):
    if modkit.GAME == "lol1":
        from decode_dialogue import encode_string
        from lol1_pak_writer import write_pak
        (game / "GENERAL.PAK").write_bytes(write_pak([("WORDS.ENG", b"\x02\x00" + encode_string(b"Novel") + b"\0")]))
    else:
        (game / "DAT").mkdir()
        if modkit.GAME == "lol2":
            from lol2_text_writer import write_trr
        else:
            from lol3_text_writer import write_trr
        (game / "WORDS.TRR").write_bytes(write_trr([(42, b"Novel")]))


class TranslationTools(unittest.TestCase):
    def test_workspace_paths_accept_an_alias_to_the_parent(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            parent = base / "parent"
            work = parent / "private tables"
            work.mkdir(parents=True)
            plain = work / "words.csv"
            plain.write_text("ordinary file", encoding="utf-8")
            alias = base / "alias"
            try:
                alias.symlink_to(parent, target_is_directory=True)
                (work / "linked.csv").symlink_to(plain)
            except (OSError, NotImplementedError):
                self.skipTest("creating symlinks is unavailable")

            aliased_work = alias / work.name
            self.assertEqual(local_path(aliased_work, plain.name).read_text(encoding="utf-8"), "ordinary file")
            with self.assertRaisesRegex(ValueError, "symbolic links"):
                local_path(aliased_work, "linked.csv")

    def test_copy_rebuild_with_growing_text_and_tamper(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            game, work, output = (base / folder for folder in ("original", "private tables", "output"))
            game.mkdir()
            source(game)
            before = {file: file.read_bytes() for file in game.iterdir() if file.is_file()}
            self.assertEqual(translate.export(game, work), (1, 1))
            table, = work.glob("*.csv")
            with table.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.reader(f))
            self.assertEqual(rows[1][1:3], ["Novel", ""])
            original_id = rows[1][0]
            rows[1][0] = "Replaced ID"
            with table.open("w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
            with self.assertRaisesRegex(ValueError, "Keep the ID"):
                translate.build(game, work, output)
            self.assertFalse(output.exists())
            rows[1][0] = original_id
            rows[1][2] = "A longer invented line."
            with table.open("w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows(rows)
            with patch("translate.fonts.installed", return_value=[("font", set(range(32, 127)))]):
                self.assertEqual(translate.build(game, work, output), 1)
            self.assertEqual(translate.verify(game, work, output), 1)
            extra = output / "extra.txt"
            extra.write_text("unexpected", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unexpected files"):
                translate.verify(game, work, output)
            extra.unlink()
            for path, raw in before.items():
                self.assertEqual(path.read_bytes(), raw)
            changed, = output.iterdir()
            changed.write_bytes(changed.read_bytes() + b"!")
            with self.assertRaisesRegex(ValueError, "differs"):
                translate.verify(game, work, output)

    def test_font_reads_bitmap_and_rejects_truncation(self):
        raw = glyph_file()
        self.assertEqual(coverage(raw), {0})
        with self.assertRaises(ValueError):
            coverage(raw[:-1])

    def test_save_page_escapes_original_values(self):
        html = render(Path("someone's test & save.000"), "LoL", [
            ("name", "Name", "</script>", "A name", 43, "Read confirmed")
        ], [("Position", "<10 / 20>")])
        self.assertIn(r"\u003c/script>", html)
        self.assertIn("&lt;10 / 20&gt;", html)
        self.assertIn("someone&#x27;s test &amp; save.000</p>", html)
        self.assertIn("tools/lol.py save set --out", html)
        self.assertIn('value="../edited-save.000"', html)


    def test_unencodable_character_names_the_csv_row(self):
        with TemporaryDirectory() as tmp:
            game = Path(tmp) / "original"
            game.mkdir()
            source(game)
            work = game.parent / "work"
            translate.export(game, work)
            table, = work.glob("*.csv")
            with table.open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            rows[1][2] = "œ"
            with table.open("w", encoding="utf-8-sig", newline="") as stream:
                csv.writer(stream).writerows(rows)
            with self.assertRaisesRegex(ValueError, "row 2.*œ.*Try 'oe'"):
                translate.build(game, work, game.parent / "copy")

    def test_gameplay_text_excludes_prologue_fonts(self):
        from translate_data import warning_fonts

        selects = warning_fonts("STARTUP.PAK", "LANDS.ENG")
        self.assertTrue(selects("STARTUP.PAK/FONT9P.FNT"))
        self.assertFalse(selects("ENG/STARTUP.PAK/INTRO.FNT"))
        self.assertFalse(selects("INTRO.PAK/FONT9P.FNT"))
