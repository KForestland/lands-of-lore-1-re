#!/usr/bin/env python3
"""Read a LoL1 wall tile set: AREA.VCN (tiles) and AREA.VMP (tile layouts).

Both files go through Screen::loadBitmap (10-byte header, Frame4 payload;
see cps_reader.py). After decompression (ScummVM
engines/kyra/engine/scene_lol.cpp:338-401, loadLevelGraphics, VGA path):

VCN  uint16 tile count n
     n bytes     shift table (_vcnShift: per-tile palette bank, ORed into
                 the colour-table index; scene_rpg.cpp:386, :429)
     128 bytes   colour table (_vcnColTable)
     384 bytes   palette, 128 colours x 6-bit RGB (unless an override .PAL)
     n x 32      tile pixels, 8x8 at 4 bits (_vcnBlocks; tlen << 5)
VMP  uint16 entry count m, then m x uint16 tile words. The wall layout for
     WLL vmp_map value p starts at (p - 1) * 431 (scene_rpg.cpp:273); the
     word is a VCN tile index, bit 0x4000 = mirrored (scene_rpg.cpp:297).

  vcn_vmp_reader.py KEEP [--png tiles.png]
  vcn_vmp_reader.py --check
"""
import argparse, struct, sys
import lol1lib as L


def read_vcn(b):
    _, _, d = L.load_bitmap(b)
    n = struct.unpack_from("<H", d, 0)[0]
    shift = d[2:2 + n]; col = d[2 + n:130 + n]; pal = d[130 + n:514 + n]
    tiles = d[514 + n:514 + n + 32 * n]
    return {"tiles": n, "decoded": len(d), "expected": 514 + 33 * n}, shift, col, pal, tiles


def read_vmp(b):
    _, _, d = L.load_bitmap(b)
    m = struct.unpack_from("<H", d, 0)[0]
    words = struct.unpack_from(f"<{m}H", d, 2)
    return m, len(d), words


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("area", nargs="?", help="area name, e.g. KEEP, CAVE1, YVEL2")
    ap.add_argument("--png")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        rows = []; bad = []
        for pak, name, b in L.find_all(".VCN", a.data):
            area = name[:-4]
            info, shift, col, pal, tiles = read_vcn(b)
            m, dl, words = read_vmp(L.find_member(area + ".VMP", a.data, pak)[1])
            maxtile = max((w & 0x3FFF) for w in words)
            ok = info["decoded"] == info["expected"] and dl == 2 + 2 * m and maxtile < info["tiles"] \
                and max(shift) < 128
            rows.append(f"{area}:{info['tiles']}t/{m}w/{m//431}p")
            if not ok: bad.append(f"{area} {info} vmp={dl}/{m} maxtile={maxtile}")
        print(f"CHECK vcn/vmp: {len(rows)} sets; VCN size == 514+33n, VMP size == 2+2m, all VMP tiles < n: "
              f"{len(rows)-len(bad)}/{len(rows)}; {' '.join(rows)}; bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.area:
        ap.print_help(); return 2
    pak, b = L.find_member(a.area + ".VCN", a.data, a.pak)
    info, shift, col, pal, tiles = read_vcn(b)
    m, dl, words = read_vmp(L.find_member(a.area + ".VMP", a.data, pak)[1])
    print(f"{a.area} ({pak}): VCN {info}, shift values {sorted(set(shift))}; VMP {m} words = 330 floor/ceiling + {(m-330)/431:g} wall pages of 431")
    if a.png:
        from PIL import Image
        n = info["tiles"]; cols = 32
        img = Image.new("P", (cols * 8, ((n + cols - 1) // cols) * 8))
        flat = [c for rgb in L.vga_palette(pal) for c in rgb]
        img.putpalette(flat + [0] * (768 - len(flat)))
        for t in range(n):
            for p in range(64):
                v = tiles[t * 32 + p // 2]
                v = (v >> 4) if not p & 1 else (v & 15)
                img.putpixel(((t % cols) * 8 + p % 8, (t // cols) * 8 + p // 8), col[v | shift[t]])
        img.save(a.png); print("wrote", a.png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
