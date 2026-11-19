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

A wall page holds nine pieces, one per position of a wall face in the
22x15-tile view. Piece i is (columns x rows) 3x5, 1x5, 6x5, 2x6, 2x8, 10x8,
3x12, 16x12, 3x15 (the numBlocks arguments of the generateVmpTileData calls,
scene_rpg.cpp:161-267) and starts at word 102, 97, 129, 117, 81, 159, 45,
239, 0 of the page (_vmpOffsetsDefault, resource/staticres_rpg.cpp:53; the
pieces tile the 431 words without gap or overlap). Piece 7 (16x12, 128x96 px)
is the wall straight ahead, one square away; piece 5 the one two squares
away; pieces 0-4, 6, 8 are side walls seen at an angle.

  vcn_vmp_reader.py KEEP [--png tiles.png]       # 8x8 tiles in file order
  vcn_vmp_reader.py KEEP --walls-png walls.png   # wall pages assembled: one row per page,
                                                 # its nine pieces as drawn on screen
                                                 # (floor/ceiling 22x15 first)
  vcn_vmp_reader.py --check
"""
import argparse, struct, sys
import lol1lib as L

# (columns, rows) of the nine pieces of a 431-word wall page, in storage order
VIS_PIECES = [(3, 5), (1, 5), (6, 5), (2, 6), (2, 8), (10, 8), (3, 12), (16, 12), (3, 15)]
VIS_OFFS = [102, 97, 129, 117, 81, 159, 45, 239, 0]
PAGE_WORDS = 431
FLOOR_WORDS = 330          # 22 x 15
FRONT_PIECE = 7            # 16x12, the wall face one square ahead


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


def tile_pixels(tiles, col, shift, t, flip=False):
    """64 palette indices of VCN tile t (8 rows of 8), as vcnDraw_fw/bw_4bit draw them."""
    out = []
    for y in range(8):
        row = []
        for x in range(4):
            b = tiles[t * 32 + y * 4 + x]
            row += [col[(b >> 4) | shift[t]], col[(b & 15) | shift[t]]]
        out += row[::-1] if flip else row
    return out


def assemble(words, start, cols, rows, tiles, col, shift):
    """Assemble cols x rows VMP words from word index start into a (cols*8) x (rows*8)
    grid of palette indices; None = nothing drawn (word 0, or a colour-0 pixel of a
    bit-0x8000 tile, which is drawn transparent over the floor; scene_rpg.cpp:359-363, :417)."""
    w, h = cols * 8, rows * 8
    grid = [None] * (w * h)
    for r in range(rows):
        for c in range(cols):
            i = start + r * cols + c
            word = words[i] if 0 <= i < len(words) else 0
            if not word:
                continue
            trans = bool(word & 0x8000)
            word &= 0x7FFF
            t = word & 0x3FFF
            if t >= len(shift):
                continue
            px = tile_pixels(tiles, col, shift, t, bool(word & 0x4000))
            for k, v in enumerate(px):
                if trans and v == 0:
                    continue
                grid[(r * 8 + k // 8) * w + c * 8 + k % 8] = v
    return w, h, grid


def wall_piece(words, page, piece, tiles, col, shift):
    """Piece `piece` (0-8) of wall page `page` (1-based WLL vmp_map value)."""
    cols, rows = VIS_PIECES[piece]
    return assemble(words, FLOOR_WORDS + (page - 1) * PAGE_WORDS + VIS_OFFS[piece], cols, rows, tiles, col, shift)


def walls_image(words, tiles, col, shift, pal, scale=2, bg=(40, 40, 52)):
    """One row per wall page (floor/ceiling first), pieces side by side as drawn on screen."""
    from PIL import Image
    rgb = L.vga_palette(pal)
    pages = (len(words) - FLOOR_WORDS) // PAGE_WORDS
    rows = [[assemble(words, 0, 22, 15, tiles, col, shift)]]
    for p in range(1, pages + 1):
        rows.append([wall_piece(words, p, i, tiles, col, shift) for i in range(len(VIS_PIECES))])
    gap = 6
    width = max(sum(w for w, _, _ in r) + gap * (len(r) + 1) for r in rows)
    height = sum(max(h for _, h, _ in r) for r in rows) + gap * (len(rows) + 1)
    img = Image.new("RGB", (width, height), bg)
    y = gap
    for r in rows:
        x = gap
        for w, h, grid in r:
            for k, v in enumerate(grid):
                if v is not None:
                    img.putpixel((x + k % w, y + k // w), rgb[v] if v < len(rgb) else (255, 0, 255))
            x += w + gap
        y += max(h for _, h, _ in r) + gap
    return img.resize((width * scale, height * scale), Image.NEAREST)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("area", nargs="?", help="area name, e.g. KEEP, CAVE1, YVEL2")
    ap.add_argument("--png", help="write the 8x8 tiles in file order (32 per row) here")
    ap.add_argument("--walls-png", help="write the wall pages assembled from the VMP here: one row per page, "
                    "the floor/ceiling layout first, then the nine pieces of each wall page as drawn on screen")
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
    if a.walls_png:
        walls_image(words, tiles, col, shift, pal).save(a.walls_png)
        print("wrote", a.walls_png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
