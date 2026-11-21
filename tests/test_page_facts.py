"""Check the documentation scanner without requiring the game files."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))

import page_facts


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

    def test_mutation_reports_the_original_page_line(self):
        with tempfile.TemporaryDirectory() as kind:
            root = pathlib.Path(kind)
            (root / "docs").mkdir()
            page = root / "docs" / "table.md"
            page.write_text("# Table\n\nCONFIRMED. Frame size is 75 bytes.\n", encoding="utf-8")
            _, accepted, _, _ = page_facts.scan(root, {})
            page.write_text("# Table\n\nCONFIRMED. Frame size is 76 bytes.\n", encoding="utf-8")
            _, altered, _, _ = page_facts.scan(root, {})
            self.assertIn("docs/table.md:3: unreviewed literal or changed prose-only claim",
                          list(page_facts.inventory_errors(altered, accepted)))

    def test_insertion_before_an_unchanged_passage(self):
        with tempfile.TemporaryDirectory() as kind:
            root = pathlib.Path(kind)
            (root / "docs").mkdir()
            page = root / "docs" / "table.md"
            body = "# Table\n\nCONFIRMED. Frame size is 75 bytes.\n"
            page.write_text(body, encoding="utf-8")
            _, accepted, _, _ = page_facts.scan(root, {})
            page.write_text(body.replace("# Table\n", "# Table\n\nOne sentence.\n"), encoding="utf-8")
            _, moved, _, _ = page_facts.scan(root, {})
            self.assertEqual(list(page_facts.inventory_errors(moved, accepted)), [])

    def test_exact_anchor_returns_value_even_if_wrong(self):
        anchor = {"before": "first at `", "after": "`", "kind": "hex"}
        self.assertEqual(page_facts.locate("# Table\n\nfirst at `0xBED`", anchor), (3, "0xBED"))
        with self.assertRaisesRegex(ValueError, r"3: expected one anchor"):
            page_facts.locate("# Table\n\nfirst at `unknown`", anchor)


if __name__ == "__main__":
    unittest.main()
