"""Write or verify the check and test counts shown in the guide."""
import argparse
from pathlib import Path
import sys
import unittest

from check_all import check_counts

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("README.md", "docs/STATUS.md", "docs/START_HERE.md", "tools/README.md")
BEGIN = "<!-- suite-counts:begin -->"
END = "<!-- suite-counts:end -->"


def test_count(folder, top):
    loader = unittest.TestLoader()
    suite = loader.discover(str(folder), top_level_dir=str(top))
    if loader.errors:
        raise ValueError("\n".join(loader.errors))
    return suite.countTestCases()


def render():
    full, quick = check_counts()
    count = test_count(ROOT / "tests", ROOT)
    lines = [
        f"- **Original game files.** {full} checks with the required files and dependencies. Quick mode selects {quick}.",
        f"- **Synthetic data.** {count} unit tests.",
    ]
    geometry = ROOT / "tools" / "history" / "draracle"
    if geometry.is_dir():
        lines.append(f"- **Historical cave geometry.** {test_count(geometry, geometry)} additional unit tests.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail if a page disagrees with the suites")
    mode.add_argument("--write", action="store_true", help="refresh the marked sections")
    args = parser.parse_args()
    block = render()
    bad = []
    for page in PAGES:
        path = ROOT / page
        text = path.read_text(encoding="utf-8")
        if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
            bad.append(f"{page}: expected exactly one suite-counts section")
            continue
        start = text.index(BEGIN) + len(BEGIN)
        end = text.index(END)
        updated = text[:start] + "\n" + block + "\n" + text[end:]
        if updated == text:
            continue
        if args.write:
            path.write_text(updated, encoding="utf-8")
        else:
            bad.append(f"{page}: stale suite counts")
    if bad:
        for message in bad:
            print(message, file=sys.stderr)
        print("Run python tools/suite_counts.py --write to refresh the pages.", file=sys.stderr)
        return 1
    print(f"CHECK suite counts: {len(PAGES)} pages match the test and check suites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
