#!/usr/bin/env python3
"""Read a LoL1 DATA folder and write inventory, level and text reports."""
import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from cli_errors import ReaderArgumentParser, run_cli
from extract_dialogue import LANG_EXTENSIONS, extract_strings
import lol1_loose
import lol1lib
from rating import pak_covered


def inventory(data):
    rows = []
    cd = lol1lib.is_cd_layout(data)
    for path in sorted(data.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in (".pak", ".tlk"):
            reader = "rating.pak_covered"
            complete = pak_covered(path)
        elif cd:
            reader = "lol1_loose.covered"
            complete = lol1_loose.covered(path)
        else:
            reader = ""
            complete = False
        rows.append((path.relative_to(data).as_posix(), path.stat().st_size,
                     reader, "complete" if complete else "open"))
    return rows


def text_counts(data):
    return sorted((pak, name, len(extract_strings(blob)))
                  for pak, name, blob in lol1lib.find_all("", data)
                  if name.endswith(LANG_EXTENSIONS))


def write_tsv(path, headings, rows):
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        writer.writerow(headings)
        writer.writerows(rows)


def main():
    parser = ReaderArgumentParser(description=__doc__)
    default_data = os.environ.get("LOL1_DATA")
    parser.add_argument("--data", type=Path, default=default_data, required=default_data is None,
                        help="the game's DATA folder (default: $LOL1_DATA)")
    parser.add_argument("--out", type=Path, required=True, help="report folder outside the game and repository")
    args = parser.parse_args()
    data = args.data.resolve()
    out = args.out.resolve()
    repository = Path(__file__).resolve().parents[1]
    if any(out == root or root in out.parents for root in (repository, data.parent)):
        parser.error("--out must be outside the game and repository")
    out.mkdir(parents=True, exist_ok=True)
    names = ("inventory.tsv", "text-counts.tsv", "levels")
    # Keep a failed level read from publishing a half-written report.
    with tempfile.TemporaryDirectory(dir=out, prefix=".report-") as staging:
        occupied = [name for name in names if (out / name).exists() or (out / name).is_symlink()]
        if occupied:
            raise ValueError(f"output already contains {', '.join(occupied)}")
        report = Path(staging)
        files = inventory(data)
        text = text_counts(data)
        level_reader = Path(__file__).with_name("level_report.py")
        result = subprocess.run([sys.executable, str(level_reader), "--data", str(data),
                                 "--out", str(report / "levels")], capture_output=True, text=True)
        if result.returncode:
            raise ValueError((result.stderr or result.stdout).strip() or "level reader failed")
        levels = len(list((report / "levels").glob("*.md"))) - 1  # Exclude the index.
        if levels < 1:
            raise ValueError("no level sheets were generated")
        write_tsv(report / names[0], ("file", "bytes", "reader", "result"), files)
        write_tsv(report / names[1], ("source", "table", "records"), text)
        for name in ("levels", *names[:2]):
            (report / name).rename(out / name)
    print(f"wrote {len(files)} inventory rows, {levels} level sheets and {len(text)} text counts to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
