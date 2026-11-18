#!/usr/bin/env python3
"""Read a LoL1 area decoration table (KEEP.DAT, FOREST1.DAT, ...).

Layout (ScummVM engines/kyra/engine/scene_lol.cpp:267-296, loadLevelShpDat):
  uint16 count, then count records of 72 bytes (LevelDecorationProperty):
  +0  uint16 shapeIndex[10]  shape in the area .SHP, 0xFFFF = unused
  +20 uint8  scaleFlag[10]
  +30 int16  shapeX[10]
  +50 int16  shapeY[10]
  +70 uint8  next            index of a chained decoration record (0 = none)
  +71 uint8  flags
The ten slots are the views of the decoration at the visible scene
positions. WLL shape_map values > 0 index these records
(scene_lol.cpp:158-164, assignLevelDecorationShapes :180-213).

  dat_reader.py KEEP.DAT [--index 3]
  dat_reader.py --check
"""
import argparse, struct, sys
import lol1lib as L


def parse(b):
    n = struct.unpack_from("<H", b, 0)[0]
    out = []
    for i in range(n):
        o = 2 + i * 72
        out.append({"shapeIndex": list(struct.unpack_from("<10H", b, o)),
                    "scaleFlag": list(b[o + 20:o + 30]),
                    "shapeX": list(struct.unpack_from("<10h", b, o + 30)),
                    "shapeY": list(struct.unpack_from("<10h", b, o + 50)),
                    "next": b[o + 70], "flags": b[o + 71]})
    return n, out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--index", type=int)
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        res = []; bad = []
        for pak, name, b in L.find_all(".DAT", a.data):
            n, recs = parse(b)
            shp = L.find_member(name[:-4] + ".SHP", a.data, pak)[1]
            nshp = struct.unpack_from("<H", shp, 0)[0]
            maxidx = max([s for r in recs for s in r["shapeIndex"] if s != 0xFFFF] or [0])
            nxt_ok = all(r["next"] < n for r in recs)
            ok = len(b) == 2 + 72 * n and maxidx < nshp and nxt_ok
            res.append(f"{name}:{n}")
            if not ok: bad.append(f"{name} size={len(b) == 2 + 72 * n} maxshape={maxidx}/{nshp} next={nxt_ok}")
        print(f"CHECK dat: {len(res)} files, size == 2+72*count, shape indexes < shapes in the area SHP, "
              f"next < count: {len(res)-len(bad)}/{len(res)}; {' '.join(res)}; bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, b = L.find_member(a.name, a.data, a.pak)
    n, recs = parse(b)
    print(f"{a.name} in {pak}: {n} records")
    for i, r in enumerate(recs):
        if a.index is None or a.index == i:
            print(i, r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
