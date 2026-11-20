#!/usr/bin/env python3
"""Read entry tables in DRIVERS.PAK from the LoL1 CD and floppy editions.

  lol1_driver_tables.py --data DATA          # print entry ids and offsets
  lol1_driver_tables.py --data DATA --check  # verify the shipped tables

The CD DATA folder has a second DRIVERS.PAK, identical in ENG, FRE and GER;
--data reads those copies too.
"""
from pathlib import Path
from struct import unpack_from

from cli_errors import run_cli
import lol1lib as L

ADV_NAMES = ("ALGDIG.ADV", "MT32MPU.ADV", "PCSPKR.ADV", "SBDIG.ADV",
             "SBPDIG.ADV", "TANDYDIG.ADV")
ADV_COPYRIGHT = b"Copyright (C) 1991,1992 Miles Design, Inc."


def adv_entries(driver):
    """Return the directory offset and (id, code offset) pairs of an ADV."""
    if not driver[2:].startswith(ADV_COPYRIGHT):
        raise ValueError("missing ADV copyright at +2")
    start = unpack_from("<H", driver)[0]
    cursor = start
    rows = []
    while cursor + 2 <= len(driver):
        code = unpack_from("<H", driver, cursor)[0]
        if code == 0xFFFF:
            if not rows or len({key for key, _ in rows}) != len(rows):
                raise ValueError("empty or repeated ADV entry id")
            if any(not cursor + 2 <= target < len(driver) or
                   driver[target:target + 3] != b"\x55\x8b\xec" for _, target in rows):
                raise ValueError("ADV entry lacks its routine prologue")
            return start, rows
        rows.append((code, unpack_from("<H", driver, cursor + 2)[0]))
        cursor += 4
    raise ValueError("ADV entry table has no terminator")


def alfx_entries(driver):
    """Follow the first ALFX jump and read its BX-indexed dispatch table."""
    if driver[:1] != b"\xe9" or driver[3:4] != b"\xe9":
        raise ValueError("ALFX header lacks its two near jumps")
    dispatch = 3 + unpack_from("<h", driver, 1)[0]
    helper = 6 + unpack_from("<h", driver, 4)[0]
    code = driver[dispatch:dispatch + 12]
    if not (6 <= dispatch <= len(driver) - 12 and len(code) == 12
            and code[:2] == b"\x83\xfb" and code[3] == 0x77
            and code[5:10] == b"\xd1\xe3\x2e\xff\xa7"):
        raise ValueError("unexpected ALFX dispatch instructions")
    count = code[2] + 1
    table = unpack_from("<H", code, 10)[0]
    otherwise = dispatch + 5 + unpack_from("<b", code, 4)[0]
    if not (6 <= helper < otherwise == table - 1 and table + 2 * count == dispatch
            and driver[otherwise] == 0xCF):
        raise ValueError("ALFX table boundaries differ")
    targets = unpack_from(f"<{count}H", driver, table)
    ordered = sorted(targets)
    if (len(set(ordered)) != count or not 6 <= ordered[0] <= ordered[-1] < otherwise
            or any(driver[end - 1] != 0xCF for end in ordered[1:] + [otherwise])):
        raise ValueError("ALFX wrapper boundaries differ")
    return table, list(enumerate(targets)), dispatch, helper


LANGUAGE_DIRS = ("ENG", "FRE", "GER")
# Per archive: ALFX dispatch and +3 entry, then (table offset, entry count) of the six ADV files.
WITNESSES = {
    "CD": (0x1A8E, 0xC76, ((63, 20), (45, 38), (45, 38), (63, 18), (63, 18), (63, 18))),
    "CD language": (0x1A8E, 0xC76, ((54, 19), (45, 38), (45, 38), (54, 17), (54, 17), (54, 17))),
    "floppy": (0x18D7, 0xB4E, ((54, 19), (45, 38), (45, 38), (54, 17), (54, 17), (54, 17))),
}


def read_drivers(original, show=False):
    """Read the seven members of one DRIVERS.PAK image; return its witness and wrapper count."""
    rows_by_name = {}
    dispatch = helper = None
    for name, at, size in L.pak_entries(original):
        driver = original[at:at + size]
        if name in ADV_NAMES:
            table, rows = adv_entries(driver)
        elif name == "ALFX.DRV":
            table, rows, dispatch, helper = alfx_entries(driver)
        else:
            raise ValueError(f"unexpected driver {name}")
        if name in rows_by_name:
            raise ValueError(f"repeated driver {name}")
        rows_by_name[name] = (table, len(rows))
        if show:
            print(f"{name}  PAK+0x{at:X}  member table +0x{table:X}")
            for key, offset in rows:
                print(f"  {key:3d}  member +0x{offset:X}")
    if set(rows_by_name) != {*ADV_NAMES, "ALFX.DRV"}:
        raise ValueError("DRIVERS.PAK does not have the seven shipped members")
    adv = tuple(rows_by_name[name] for name in ADV_NAMES)
    return (dispatch, helper, adv), rows_by_name["ALFX.DRV"][1]


def main():
    parser = L.tool_args(__doc__, writes=False)
    args = parser.parse_args()
    paths = [Path(args.pak) if args.pak else Path(args.data) / "DRIVERS.PAK"]
    if not args.pak:
        paths += [path for path in (Path(args.data) / lang / "DRIVERS.PAK" for lang in LANGUAGE_DIRS)
                  if path.is_file()]
    images = [path.read_bytes() for path in paths]
    found = []
    for path, image in zip(paths, images):
        if not args.check:
            print(f"== {path}")
        found.append(read_drivers(image, show=not args.check))
    if args.check:
        labels = [next((label for label, row in WITNESSES.items() if row == witness), None)
                  for witness, _ in found]
        expected = ["CD", "CD language", "CD language", "CD language"] if len(paths) == 4 else None
        if labels not in (expected, ["CD"], ["CD language"], ["floppy"]) or any(image != images[-1] for image in images[1:]):
            raise ValueError("driver directory differs from the checked editions")
        parts = []
        for index, (label, (witness, count)) in enumerate(zip(labels, found)):
            if index > 1:
                continue  # the later language copies are byte-identical to the first
            parts.append(f"{label} {sum(n for _, n in witness[2])} entries, "
                         f"ALFX +0x{witness[0]:X} {count} wrappers")
        same = f"; {len(paths) - 1} identical language copies" if len(paths) > 1 else ""
        print(f"CHECK drivers: 6 ADV tables per archive; {'; '.join(parts)}{same}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
