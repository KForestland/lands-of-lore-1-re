"""Check the documentation scanner without requiring the game files."""
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

import page_facts
from page_facts_auto import observed, probes, x86_operand


class PageFactsTests(unittest.TestCase):
    def test_multiline_measurements_and_excluded_examples(self):
        text = """# Example

**CONFIRMED.** The offset is
`0xE4` and there are 9 records.

```
CONFIRMED `OUTSIDE.DAT` has 2 records.
```

| `GAMES.DAT` | 48 bytes | CONFIRMED |
| `OPEN.DAT` | 49 bytes | UNCONFIRMED |
"""
        result = dict(page_facts.measured_lines(text))
        self.assertEqual(set(result), {3, 4, 10})

    def test_confirmed_prefix_of_a_mixed_label_line_is_inventoried(self):
        body = "CONFIRMED. The string is at 0x70. UNCONFIRMED. The date is unknown."
        self.assertEqual(dict(page_facts.measured_lines(body)), {1: "CONFIRMED. The string is at 0x70."})

    def test_mutation_reports_the_original_page_line(self):
        with tempfile.TemporaryDirectory() as kind:
            root = pathlib.Path(kind)
            (root / "docs").mkdir()
            page = root / "docs" / "table.md"
            page.write_text("# Table\n\nCONFIRMED. Frame size is 75 bytes.\n", encoding="utf-8")
            _, accepted, _, _, _ = page_facts.scan(root, {})
            page.write_text("# Table\n\nCONFIRMED. Frame size is 76 bytes.\n", encoding="utf-8")
            _, altered, _, _, _ = page_facts.scan(root, {})
            self.assertIn("docs/table.md:3: unreviewed literal or changed prose-only claim",
                          list(page_facts.inventory_errors(altered, accepted)))

    def test_insertion_before_an_unchanged_passage(self):
        with tempfile.TemporaryDirectory() as kind:
            root = pathlib.Path(kind)
            (root / "docs").mkdir()
            page = root / "docs" / "table.md"
            body = "# Table\n\nCONFIRMED. Frame size is 75 bytes.\n"
            page.write_text(body, encoding="utf-8")
            _, accepted, _, _, _ = page_facts.scan(root, {})
            page.write_text(body.replace("# Table\n", "# Table\n\nOne sentence.\n"), encoding="utf-8")
            _, moved, _, _, _ = page_facts.scan(root, {})
            self.assertEqual(list(page_facts.inventory_errors(moved, accepted)), [])

    def test_exact_anchor_returns_value_even_if_wrong(self):
        anchor = {"before": "first at `", "after": "`", "kind": "hex"}
        self.assertEqual(page_facts.locate("# Table\n\nfirst at `0xBED`", anchor), (3, "0xBED"))
        with self.assertRaisesRegex(ValueError, r"3: expected one anchor"):
            page_facts.locate("# Table\n\nfirst at `unknown`", anchor)


    def test_measured_record_size_is_checked_independently_of_inventory(self):
        body = "CONFIRMED. A table of 147-byte creature definitions. Its 136-byte body is followed by a 12-byte tag."
        claim, = probes(body, {1: body}, {})
        self.assertEqual(claim.expected, 136)
        self.assertEqual(observed(claim, None, None, None)[0], 135)

    def test_cited_original_bytes_and_string(self):
        with tempfile.TemporaryDirectory() as folder:
            original = pathlib.Path(folder) / "EXAMPLE.DAT"
            original.write_bytes(b"\x02\0.odf\0")
            body = "CONFIRMED. `EXAMPLE.DAT+0x0` holds `02 00`. The suffix `.obf` is from another field."
            body += "\nIt reads suffix `.obf` from `EXAMPLE.DAT+0x2`."
            got = probes(body, dict(page_facts.measured_lines(body)), {})
            values = [observed(claim, original.parent, None, lambda root, name: root / name)[0] for claim in got]
            self.assertEqual(values, [b"\x02\0", ".odf"])

    def test_malformed_byte_citations_are_scan_errors_without_game_data(self):
        body = """CONFIRMED. `EXAMPLE.DAT+0x20` with `00 01 FQ FF`.
`EXAMPLE.DAT+0x30` contains bytes `GG`.
LE `+0x2` and `+0x4` (file `+0x102` and `+0x104`, bytes `AB CD` and `EF FQ`).
`EXAMPLE.DAT+0x40` holds `OK`.
"""
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            (root / "docs").mkdir()
            (root / "docs" / "example.md").write_text(body, encoding="utf-8")
            _, _, _, errors, claims = page_facts.scan(root, {}, {"executable": "EXAMPLE.DAT"})
        self.assertEqual(errors, [
            "docs/example.md:1: malformed hexadecimal byte list '00 01 FQ FF' at EXAMPLE.DAT+0x20",
            "docs/example.md:2: malformed hexadecimal byte list 'GG' at EXAMPLE.DAT+0x30",
            "docs/example.md:3: malformed hexadecimal byte list 'EF FQ' at EXAMPLE.DAT+0x104",
        ])
        self.assertEqual([claim.expected for _, claim in claims], ["OK", b"\xab\xcd"])


    def test_common_citation_forms_read_the_independent_sources(self):
        body = '''CONFIRMED. `EXAMPLE.DAT+0x0` holds `02 00`.
The string `example` is stored at `EXAMPLE.DAT+0x2`.
`EXAMPLE.DAT` (10 bytes) is the executable.
`reader_demo.py --check` walks 34 rows.
`-DEMO` occurs in `EXAMPLE.DAT`.
The pointer is at `0x1234` (`0x1000`).
'''
        config = {"executable": "EXAMPLE.DAT", "loose_files": ["*.DAT"],
                  "absolute_operands": True, "counts": {"reader_demo.py": {"rows": "entries"}}}
        found = probes(body, dict(page_facts.measured_lines(body)), config)
        self.assertEqual([claim.reader[0] for claim in found],
                         ["bytes_at", "string_at", "file_size", "absolute_operand", "string_in", "check_count"])
        with tempfile.TemporaryDirectory() as folder:
            data = pathlib.Path(folder)
            path = data / "EXAMPLE.DAT"
            path.write_bytes(b"\x02\0example\0-DEMO\0")
            file_for = lambda root, name: root / name
            operand = lambda root, spec: (0x5678, "fixture instruction")
            with patch("page_facts_auto.check_output", return_value="CHECK: 33 entries"):
                values = [observed(claim, data, operand, file_for)[0] for claim in found]
        self.assertEqual(values, [b"\x02\0", "example", 16, 0x5678, "-DEMO", 33])

    def test_absolute_operands_use_the_original_instruction_width(self):
        self.assertEqual(x86_operand(bytes.fromhex("68 34 12"), 2), 0x1234)
        self.assertEqual(x86_operand(bytes.fromhex("8b 05 78 56 34 12"), 4), 0x12345678)
        self.assertEqual(x86_operand(bytes.fromhex("c7 00 74 25 02 00"), 4), 0x22574)
        with self.assertRaisesRegex(ValueError, "unsupported"):
            x86_operand(bytes.fromhex("eb 00"), 4)


if __name__ == "__main__":
    unittest.main()
