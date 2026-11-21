"""The aggregate check keeps the failing child's diagnostics."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_all


class CheckAllTests(unittest.TestCase):
    def test_failing_checks_print_only_the_last_twenty_stderr_lines(self):
        diagnostics = "\n".join(f"detail {index:02}" for index in range(23)) + "\n"

        def run(command, **kwargs):
            name = Path(command[1]).stem
            if name == "broken":
                return CompletedProcess(command, 1, "", diagnostics)
            if name == "test_emc2_corpus":
                return CompletedProcess(command, 1, "CHECK emc2: bad script\n", diagnostics)
            return CompletedProcess(command, 0, "CHECK success\n", "quiet warning\n")

        tool_list = "READERS" if hasattr(check_all, "READERS") else "TOOLS"
        output = StringIO()
        with TemporaryDirectory() as data, patch.object(check_all, tool_list, ["success", "broken"]), patch.object(
                sys, "argv", ["check_all.py", "--data", data]), patch.object(
                check_all.subprocess, "run", side_effect=run), redirect_stdout(output):
            self.assertNotEqual(check_all.main(), 0)

        lines = output.getvalue().splitlines()
        self.assertNotIn("quiet warning", output.getvalue())
        self.assertTrue(lines[0].startswith("CHECK success ["))
        self.assertTrue(lines[1].startswith("broken: exit 1 ["))
        tail = [f"  detail {index:02}" for index in range(3, 23)]
        self.assertEqual(lines[2:22], tail)
        if tool_list == "READERS":
            self.assertTrue(lines[22].startswith("CHECK emc2: bad script ["))
            self.assertEqual(lines[23:43], tail)
        self.assertIn("FAILED: broken", lines[-1])
