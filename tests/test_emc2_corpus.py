#!/usr/bin/env python3
"""Decompile and check every original LoL1 script in a DOS PAK corpus."""

import argparse
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from emc2_decompile import format_listing, pak_entries, read_entry, read_script


EXPECTED = {"ITEM.INF", "ONETIME.INF"} | {
    f"LEVEL{level}.{extension}" for level in range(1, 30) for extension in ("INF", "INI")
}


def check_corpus(root):
    counts = Counter()
    seen = set()
    for path in sorted(root.iterdir()):
        if path.suffix.upper() != ".PAK":
            continue
        for name, offset, size in pak_entries(path):
            name = name.upper()
            if Path(name).suffix not in (".INF", ".INI"):
                continue
            raw = read_entry(path, offset, size)
            if raw[:4] != b"FORM" or raw[8:12] != b"EMC2":
                continue
            witness = f"{path.name}/{name} at PAK+0x{offset:X}"
            if name in seen:
                raise ValueError(f"duplicate corpus entry {witness}")
            seen.add(name)
            try:
                script = read_script(raw)
                listing = "\n".join(format_listing(script, witness))
                if name == "LEVEL1.INI":
                    # Original TEXT index 0 points to its first actual filename.
                    if script.strings[0] != (0x14, b"KEEP") or 'TEXT[0] +0x0014 "KEEP"' not in listing:
                        raise ValueError("first TEXT string decoded incorrectly")
                if name == "ONETIME.INF" and "setItemProperty" not in listing:
                    raise ValueError("item syscall names missing from listing")
            except ValueError as error:
                raise ValueError(f"{witness}: {error}") from error
            counts.update(scripts=1, words=len(script.words), instructions=len(script.instructions),
                          strings=len(script.strings))
    if seen != EXPECTED:
        raise ValueError(f"missing {sorted(EXPECTED - seen)}, unexpected {sorted(seen - EXPECTED)}")
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, nargs="+", help="One or more directories of original PAKs")
    args = parser.parse_args()
    for root in args.data:
        counts = check_corpus(root)
        print(f"{root}: PASS {counts['scripts']}/60 scripts, {counts['words']} DATA words, "
              f"{counts['instructions']} instructions, {counts['strings']} TEXT strings, "
              "0 unknown opcodes/functions")


if __name__ == "__main__":
    main()
