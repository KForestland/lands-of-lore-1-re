"""Local file-tool checks with synthetic records only."""
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from level_html import Plan
from modkit_core import output_folder


class ReaderTools(unittest.TestCase):
    def test_plan_records_and_escape(self):
        plan = Plan("Example & test", [(0, 0), (8, 8)], "Synthetic layout")
        plan.polygon([(0, 0), (8, 0), (8, 8), (0, 8)], "region-0", "Region 0", "Regions",
                     {"Offset": "0x10"})
        plan.note("exit-1", "Exit 1", "Exits", {"Gate": "<test> </script>"}, "region-0")
        html = plan.render()
        self.assertIn("<title>Example &amp; test</title>", html)
        record_json = re.search(r'<script id="records" type="application/json">([^<]+)</script>', html)[1]
        region, exit_row = json.loads(record_json)
        self.assertEqual(region["id"], exit_row["target"])
        self.assertEqual(exit_row["details"]["Gate"], "<test> </script>")
        self.assertIn('id="region-0"', html)

    def test_schematic_refuses_empty_data_before_output(self):
        with TemporaryDirectory(prefix="schematic tools ") as tmp:
            data = Path(tmp) / "empty installation"
            data.mkdir()
            out = Path(tmp) / "drawing"
            command = [sys.executable, str(TOOLS / "level_renderer.py"), "--data", str(data),
                       "--out", str(out), "--level", "level01"]
            trial = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(trial.returncode, 0)
            self.assertIn(str(data.resolve()), trial.stderr)
            self.assertEqual(len(trial.stderr.rstrip().splitlines()), 1)
            self.assertFalse(out.exists())

    def test_unplaced_exit_and_output_errors(self):
        plan = Plan("Test", [(0, 0), (8, 8)], "Synthetic layout")
        plan.note("exit-1", "Exit 1", "Exits", {"Gate": "none"})
        self.assertIn("1 exit", plan.render())
        self.assertEqual(plan.records[0]["details"]["Location"], "No location on the plan.")
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            with self.assertRaisesRegex(ValueError, "Create it or choose another folder"):
                with output_folder(folder / "missing" / "output", folder / "game"):
                    self.fail("a missing parent unexpectedly allowed an output")
            with self.assertRaisesRegex(ValueError, "Choose a new folder name"):
                with output_folder(folder, folder / "game"):
                    self.fail("an existing folder unexpectedly allowed an output")

    def test_job_menu_and_missing_game_path(self):
        command = [sys.executable, str(TOOLS / "lol.py")]
        menu = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertIn("Look at an interactive level plan", menu.stdout)
        help_text = subprocess.run(command + ["text", "--help"], capture_output=True, text=True, check=True)
        self.assertIn("usage: lol.py text ", help_text.stdout)
        self.assertNotIn("bigram formula", help_text.stdout)
        self.assertNotIn("--samples", help_text.stdout)
        self.assertNotIn("{cache,", help_text.stdout)
        with TemporaryDirectory(prefix="reader tools ") as tmp:
            data = Path(tmp) / "game folder"
            data.mkdir()
            out = Path(tmp) / "output folder"
            trial = subprocess.run(command + ["level", "--data", str(data), "--out", str(out)],
                                   capture_output=True, text=True)
            self.assertNotEqual(trial.returncode, 0)
            self.assertTrue(trial.stderr.startswith("lol.py level: "))
            self.assertIn("Give --data the game folder", trial.stderr)
            self.assertIn(str(data.resolve()), trial.stderr)
            self.assertEqual(len(trial.stderr.rstrip().splitlines()), 1)
            self.assertFalse(out.exists())
