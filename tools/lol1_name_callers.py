#!/usr/bin/env python3
"""Re-prove who names 00000.VOC and the three unused palettes.

On the CD edition:
  ENG/FINALE.EXE holds one catalog row for 00000.VOC and no other copy of that name.
  The three palette names are catalog strings, not payload text, and no program
  or the installer beside DATA contains them.

  lol1_name_callers.py --data DATA --check
"""
import os
import struct

import lol1lib as L

PALETTES = (b"CAV_PLT2.PAL", b"CAV_PLT4.PAL", b"ALTPAL3.PAL")
CONTROLS = (b"ALTPAL1.PAL", b"ALTPAL2.PAL", b"CAV_PLT3.PAL")
FDT_AT = {b"CAV_PLT2.PAL": 0x6B67, b"CAV_PLT4.PAL": 0x6B81, b"ALTPAL3.PAL": 0x67C4}
# English finale. French and German are checked when those files are present.
FINALE_ROW = 0x1D1D0
FINALE_NAME = 0x1E080
OTHERS = {"FRE": 0x1E782, "GER": 0x1E7DC}


def fail(message):
    print(f"CHECK name_callers FAILED: {message}")
    return 1


def payload_hits(data_dir, needle):
    hits = 0
    for dirpath, _, files in os.walk(data_dir):
        for name in files:
            upper = name.upper()
            if not (upper.endswith(".PAK") or upper.endswith(".TLK")):
                continue
            try:
                members = L.read_pak(os.path.join(dirpath, name))
            except (OSError, ValueError, struct.error):
                continue
            for blob in members.values():
                hits += blob.count(needle)
    return hits


def exe_hits(data_dir, needle):
    hits = []
    for dirpath, _, files in os.walk(data_dir):
        for name in files:
            if not name.upper().endswith((".EXE", ".COM")):
                continue
            path = os.path.join(dirpath, name)
            data = open(path, "rb").read()
            start = 0
            while True:
                at = data.find(needle, start)
                if at < 0:
                    break
                hits.append((os.path.relpath(path, data_dir), at))
                start = at + 1
    install = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "INSTALL.EXE")
    if os.path.isfile(install):
        data = open(install, "rb").read()
        start = 0
        while True:
            at = data.find(needle, start)
            if at < 0:
                break
            hits.append(("INSTALL.EXE", at))
            start = at + 1
    return hits


def finale_row(data, name_at):
    """Return the catalog row that points at name_at, or None."""
    if data[:2] != b"MZ":
        return None
    hdr = struct.unpack_from("<H", data, 8)[0] * 16
    reln = struct.unpack_from("<H", data, 6)[0]
    reloff = struct.unpack_from("<H", data, 0x18)[0]
    image = name_at - hdr
    for index in range(reln):
        roff, rseg = struct.unpack_from("<HH", data, reloff + 4 * index)
        loc = hdr + rseg * 16 + roff
        if loc < 2 or loc + 18 > len(data):
            continue
        ptroff, ptrseg = struct.unpack_from("<HH", data, loc - 2)
        if ptrseg * 16 + ptroff != image:
            continue
        row = data[loc - 2:loc - 2 + 20]
        return loc - 2, rseg, roff - 2, struct.unpack_from("<I", row, 4)[0], struct.unpack_from("<H", row, 0x12)[0]
    return None


def check_english(data):
    if len(data) != 132328 or data[FINALE_NAME:FINALE_NAME + 10] != b"00000.VOC\x00":
        return "ENG/FINALE.EXE does not hold 00000.VOC at 0x1E080"
    if data.count(b"00000") != 1 or data.count(b"\xd0\x08") != 1:
        return "the name or its DS offset 0x08D0 occurs more than once"
    hdr = struct.unpack_from("<H", data, 8)[0] * 16
    if data[hdr:hdr + 3] != b"\xba\x5b\x1b":
        return "startup does not set DS from 0x1B5B"
    got = finale_row(data, FINALE_NAME)
    if got != (FINALE_ROW, 0x1ACB, 0x320, 44115, 0x1000):
        return f"catalog row is {got}, not file 0x1D1D0 segment 0x1ACB offset 0x320 size 44115"
    lookup = data[0xCDD1:0xCDD1 + 8]
    if lookup != bytes.fromhex("ba1400f7eabacb1a"):
        return "the index*20 lookup is not at file 0xCDD1"
    return None


def main():
    parser = L.tool_args(__doc__)
    args = parser.parse_args()
    if not args.check:
        parser.error("this tool only checks; pass --check")
    data_dir = args.data
    if not L.is_cd_layout(data_dir):
        print("CHECK name_callers: floppy layout, CD finale catalog is not in this folder")
        return 0
    finale_path = os.path.join(data_dir, "ENG", "FINALE.EXE")
    try:
        finale = open(finale_path, "rb").read()
    except OSError as exc:
        return fail(str(exc))
    error = check_english(finale)
    if error:
        return fail(error)
    for lang, name_at in OTHERS.items():
        path = os.path.join(data_dir, lang, "FINALE.EXE")
        if not os.path.isfile(path):
            continue
        other = open(path, "rb").read()
        if other.count(b"00000.VOC") != 1 or other[name_at:name_at + 10] != b"00000.VOC\x00":
            return fail(f"{lang}/FINALE.EXE does not hold one 00000.VOC at {name_at:#x}")
        got = finale_row(other, name_at)
        if got is None or got[3] != 44115 or got[4] != 0x1000:
            return fail(f"{lang} catalog row is {got}")
    install = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "INSTALL.EXE")
    if not os.path.isfile(install):
        return fail("INSTALL.EXE is not beside DATA")
    for needle in PALETTES + (b"00000.VOC",):
        if needle in open(install, "rb").read():
            return fail(f"INSTALL.EXE contains {needle.decode()}")
    for needle in PALETTES:
        hits = exe_hits(data_dir, needle)
        if hits:
            return fail(f"{needle.decode()} is in {hits[:3]}")
        if payload_hits(data_dir, needle):
            return fail(f"{needle.decode()} is inside an archive payload")
    for needle in CONTROLS:
        if payload_hits(data_dir, needle) < 1:
            return fail(f"control name {needle.decode()} is missing from script text")
    if payload_hits(data_dir, b"00000.VOC"):
        return fail("00000.VOC is inside an archive payload")
    fdt_path = os.path.join(data_dir, "FILEDATA.FDT")
    fdt = open(fdt_path, "rb").read()
    for needle, at in FDT_AT.items():
        if fdt[at:at + len(needle) + 1] != needle + b"\x00":
            return fail(f"{needle.decode()} is not at FILEDATA.FDT+{at:#x}")
    print("CHECK name_callers: FINALE.EXE+0x1D1D0 is the 00000.VOC catalog row (44115 bytes); "
          "no instruction pushes the name; the three palettes are catalog names only, installer included")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
