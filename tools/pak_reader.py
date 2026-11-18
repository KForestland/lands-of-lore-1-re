#!/usr/bin/env python3
"""List or extract members of a LoL1 PAK container (also the CD .TLK files).

Format (ScummVM engines/kyra/resource/resource_intern.cpp:296-380,
ResLoaderPak::load): repeated [uint32 LE start offset][NUL-terminated name];
the directory ends at an empty name or when an offset equals the file size.
A member runs from its own offset to the next member's offset.

The CD speech files NN.TLK use the same layout: LoLEngine::loadTalkFile
opens "%02d.TLK" with loadPakFile (engines/kyra/engine/lol.cpp:1892-1902).

  pak_reader.py list GENERAL.PAK
  pak_reader.py extract GENERAL.PAK PARCH.CPS -o /tmp/out
  pak_reader.py --check      # parse every .PAK and .TLK in the DATA folder
"""
import argparse, os, sys
import lol1lib as L


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=["list", "extract"])
    ap.add_argument("container", nargs="?", help="PAK or TLK file name in the DATA folder")
    ap.add_argument("member", nargs="?", help="member to extract")
    ap.add_argument("-o", "--out", help="output folder for extract")
    ap.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None)
    ap.add_argument("--check", action="store_true", help="parse all containers and print one summary line")
    a = ap.parse_args()
    if a.check:
        names = sorted(n for n in os.listdir(a.data) if n.upper().endswith((".PAK", ".TLK")))
        total = 0; bad = []
        for n in names:
            d = open(os.path.join(a.data, n), "rb").read()
            e = L.pak_entries(d)
            total += len(e)
            # members must tile the file after the directory exactly
            if not e or e[-1][1] + e[-1][2] != len(d) or any(x[2] < 0 for x in e):
                bad.append(n)
        print(f"CHECK pak: {len(names)} containers, {total} members, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.cmd or not a.container:
        ap.print_help(); return 2
    d = open(os.path.join(a.data, a.container), "rb").read()
    e = L.pak_entries(d)
    if a.cmd == "list":
        for name, off, sz in e:
            print(f"{off:10d} {sz:9d}  {name}")
        return 0
    for name, off, sz in e:
        if a.member is None or name.upper() == a.member.upper():
            os.makedirs(a.out or ".", exist_ok=True)
            with open(os.path.join(a.out or ".", name), "wb") as f:
                f.write(d[off:off + sz])
    return 0


if __name__ == "__main__":
    sys.exit(main())
