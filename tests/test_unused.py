"""Check that the unused-opcode summary agrees with the EMC2 opcode table."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from emc2_decompile import OPCODES


def summary():
    page = (ROOT / "docs/UNUSED.md").read_text(encoding="utf-8")
    line = next(line for line in page.splitlines() if "VM opcodes" in line)
    observed, total = map(int, re.search(r"use (\d+) of (\d+) VM opcodes", line).groups())
    absent = {int(code, 16) for code in re.findall(r"`0x([0-9A-F]{2})`", line)}
    return observed, total, absent


class UnusedClaims(unittest.TestCase):
    def test_opcode_summary(self):
        observed, total, absent = summary()
        self.assertEqual(total, len(OPCODES))
        self.assertEqual(observed, total - len(absent))
        self.assertTrue(absent <= set(range(total)))
