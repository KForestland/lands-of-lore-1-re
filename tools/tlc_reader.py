#!/usr/bin/env python3
"""Read a LoL1 CD-edition transparency table file LEVELnn.TLC.

Layout (ScummVM engines/kyra/engine/scene_lol.cpp:458-462): 5376 bytes =
  table1: 256 bytes  colour -> effect colour slot (0..19) or 0xFF (opaque)
  table2: 20 x 256   for slot i, screen colour -> blended colour
Only the talkie (CD) edition reads the file; the floppy edition computes the
same tables at run time from FXPAL.COL and FXPAL.SHP
(lol.cpp:1844-1879, Screen_LoL::createTransparencyTablesIntern
screen_lol.cpp:144-185, 20 slots, weight 70).
Used when drawing shapes and TIM animations with transparency
(screen.cpp:2314-2331, sprites_lol.cpp:908-980, animator_tim.cpp:212).

  tlc_reader.py LEVEL01.TLC
  tlc_reader.py LEVEL01.TLC --full   # table1 and all 20 rows of table2, 256 values each (hex)
  tlc_reader.py --check
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, struct
import lol1lib as L

# Weight 70 -> (70 << 6) // 100 = 44 parts screen colour, 20 parts effect colour.
BLEND_SCREEN = 44
BLEND_EFFECT = 20
BLEND_MATCH = 3611


def level01_blend(data):
    """Return (table1 from FXPAL.SHP, how many LEVEL01 table2 bytes the weight-70 mix hits)."""
    fx = L.find_member("FXPAL.COL", data)[1]
    shp = L.load_bitmap(L.find_member("FXPAL.SHP", data)[1])[2]
    off = struct.unpack_from("<I", shp, 2)[0]
    ovl = shp[off + 2 + 11:off + 2 + 31]
    if list(ovl) != [0, *range(2, 21)]:
        raise ValueError("FXPAL.SHP colour list changed")
    table1 = bytearray([0xFF]) * 256
    for slot, colour in enumerate(ovl):
        table1[colour] = slot
    vcn = L.load_bitmap(L.find_member("KEEP.VCN", data)[1])[2]
    tiles = struct.unpack_from("<H", vcn, 0)[0]
    screen = bytearray(768)
    screen[:384] = vcn[130 + tiles:130 + tiles + 384]
    play = L.load_bitmap(L.find_member("PLAYFLD.CPS", data)[1])[1]
    screen[384:768] = play[384:768]
    tlc = L.find_member("LEVEL01.TLC", data)[1]
    if tlc[:256] != table1:
        raise ValueError("LEVEL01.TLC table1 is not the FXPAL.SHP colour list")
    palette = [screen[j * 3:j * 3 + 3] for j in range(128)]
    body = tlc[256:]
    matched = 0
    for slot, colour in enumerate(ovl):
        row = body[slot * 256:(slot + 1) * 256]
        if colour == 0:
            matched += row.count(0)
            continue
        effect = fx[3 * colour:3 * colour + 3]
        for index in range(256):
            mixed = [
                ((effect[channel] * BLEND_EFFECT) >> 6)
                + ((screen[index * 3 + channel] * BLEND_SCREEN) >> 6)
                for channel in range(3)
            ]
            best_distance = 0x7FFFFFFF
            best = 0
            for candidate, entry in enumerate(palette):
                distance = sum((mixed[channel] - entry[channel]) ** 2 for channel in range(3))
                if distance <= best_distance:
                    best_distance = distance
                    best = candidate
            if best == row[index]:
                matched += 1
    return bytes(table1), matched


def parse(b):
    t1 = b[:256]; t2 = b[256:256 + 5120]
    slots = {c: t1[c] for c in range(256) if t1[c] != 0xFF}
    return t1, t2, slots


def full_rows(table):
    """16 lines of 16 hex values; each line starts with the colour index of its first value."""
    return [f"  {r * 16:3d}: " + " ".join(f"{v:02x}" for v in table[r * 16:r * 16 + 16]) for r in range(16)]


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--full", action="store_true", help="print table1 and every table2 row in full")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        n = 0; bad = []; slotsets = set()
        if not list(L.find_all(".TLC", a.data)):
            print("CHECK tlc: 0 TLC files in this copy (the floppy edition has none); nothing to compare")
            return 0
        try:
            table1, matched = level01_blend(a.data)
        except (ValueError, FileNotFoundError) as error:
            print(f"CHECK tlc: {error}")
            return 1
        if matched != BLEND_MATCH:
            print(f"CHECK tlc: LEVEL01 weight-70 mix matched {matched} bytes")
            return 1
        for pak, name, b in L.find_all(".TLC", a.data):
            n += 1
            t1, t2, slots = parse(b)
            ok = len(b) == 5376 and all(v < 20 for v in slots.values()) and t1 == table1
            # a slot whose effect colour is 0 has an all-zero row
            zero_rows = [i for i in range(20) if not any(t2[i * 256:(i + 1) * 256])]
            slotsets.add(tuple(sorted(slots.items())))
            if not ok: bad.append(name)
        print(f"CHECK tlc: {n} files, all 5376 bytes and table1 values <20: {n-len(bad)}/{n}, "
              f"distinct table1 maps: {len(slotsets)}, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, b = L.find_member(a.name, a.data, a.pak)
    t1, t2, slots = parse(b)
    print(f"{a.name} in {pak}: {len(b)} bytes; effect colours -> slot: {slots}")
    if a.full:
        for title, table in [("table1 (colour -> slot, ff = opaque)", t1)] + \
                [(f"table2 row {i} (screen colour -> blended colour)", t2[i * 256:(i + 1) * 256]) for i in range(20)]:
            print(title)
            for line in full_rows(table):
                print(line)
        return 0
    for i in sorted(set(slots.values())):
        print(f"slot {i}: first 16 of row = {list(t2[i*256:i*256+16])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
