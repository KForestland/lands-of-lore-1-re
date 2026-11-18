#!/usr/bin/env python3
"""LoL1 top-down level map renderer: CMZ -> WLL -> VMP -> VCN.

Rewritten 2026-11-18 on top of the checked readers (lol1lib, vcn_vmp_reader,
tileset_mapper). Each of the 32x32 blocks becomes an 8x8 cell:

  - the block's four wall types come from LEVELn.CMZ (docs/formats/cmz.md);
  - a wall type with WLL vmp_map p > 0 (docs/formats/wll.md) is drawn with a
    representative VCN tile of wall page p: VMP word 330 + (p-1)*431 + 165,
    i.e. a tile from the middle of that page (docs/formats/vcn_vmp.md);
  - pixel colour = VCN colour table[nibble | shift[tile]], then the VCN (or
    override .PAL) palette, as ScummVM drawVcnBlocks does
    (engines/kyra/engine/scene_rpg.cpp:429-449);
  - blocks whose four walls have no geometry are dark floor.

The tile set is the first loadLevelGraphics call of LEVELn.INI (with its
override palette, if any), as listed by tileset_mapper.py. This is a map
overview, not the in-game 3D view.

  level_renderer.py --level 1 --out-dir maps/     # one PNG
  level_renderer.py --out-dir maps/                # all 29
  level_renderer.py --check                        # every wall page resolves; lists wall types
                                                   # missing from the level's WLL; no PNGs written
"""
import os
import struct
import sys

import lol1lib as L
import tileset_mapper
import vcn_vmp_reader as V


def area_set(name, data_dir, cache={}):
    key = (name.upper(), data_dir)
    if key not in cache:
        pak, vcn = L.find_member(name + ".VCN", data_dir)
        info, shift, col, pal, tiles = V.read_vcn(vcn)
        m, _, words = V.read_vmp(L.find_member(name + ".VMP", data_dir, pak)[1])
        cache[key] = (info["tiles"], shift, col, pal, tiles, words)
    return cache[key]


def level_blocks(level, data_dir):
    d = L.load_bitmap(L.level_member(level, "CMZ", data_dir))[2]
    ln = struct.unpack_from("<H", d, 4)[0]
    return [tuple(d[6 + i * ln:10 + i * ln]) for i in range(1024)]


def wll_vmp(level, data_dir):
    b = L.level_member(level, "WLL", data_dir)
    return {struct.unpack_from("<H", b, 2 + i * 12)[0]: b[4 + i * 12] for i in range((len(b) - 2) // 12)}


def render(level, data_dir, check_only=False):
    g = tileset_mapper.build(data_dir)[level]["loadLevelGraphics"]
    name, palname = g[0]["vcn_vmp"], g[0]["palette"]
    ntiles, shift, col, pal, tiles, words = area_set(name, data_dir)
    if palname:
        pal = L.find_member(palname, data_dir)[1][:384]
    vmp = wll_vmp(level, data_dir)
    blocks = level_blocks(level, data_dir)
    problems = []
    undefined = set()   # wall types in the CMZ with no record in this level's WLL: drawn as no geometry
    cells = []
    for walls in blocks:
        pages = [vmp.get(w) for w in walls]
        for w, p in zip(walls, pages):
            if p is None:
                undefined.add(w)
        page = max((p or 0) for p in pages)
        if page == 0:
            cells.append(None); continue
        idx = 330 + (page - 1) * 431 + 165
        if idx >= len(words):
            problems.append(("page", page)); cells.append(None); continue
        t = words[idx] & 0x3FFF
        cells.append(t if 0 < t < ntiles else None)
    if check_only:
        return name, problems, undefined
    from PIL import Image
    img = Image.new("RGB", (256, 256), (20, 20, 30))
    rgb = L.vga_palette(pal)
    for i, t in enumerate(cells):
        if t is None:
            continue
        bx, by = (i % 32) * 8, (i // 32) * 8
        for p in range(64):
            v = tiles[t * 32 + p // 2]
            v = (v >> 4) if not p & 1 else (v & 15)
            c = col[v | shift[t]]
            img.putpixel((bx + p % 8, by + p // 8), rgb[c] if c < len(rgb) else (255, 0, 255))
    return name, img


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("--level", type=int, help="1..29 (default: all)")
    ap.add_argument("--out-dir", default=".", help="folder for levelNN_<area>.png")
    a = ap.parse_args()
    levels = [a.level] if a.level else range(1, 30)
    if a.check:
        bad = []; undef = {}
        for lv in levels:
            name, problems, undefined = render(lv, a.data, check_only=True)
            if problems:
                bad.append(f"L{lv}:{len(problems)}")
            if undefined:
                undef[lv] = sorted(undefined)
        print(f"CHECK level_renderer: {len(levels)} levels, every wall page inside the VMP: "
              f"{len(levels)-len(bad)}/{len(levels)}, bad={bad or 'none'}; "
              f"CMZ wall types without a WLL record (open point, drawn empty): {undef or 'none'}")
        return 0 if not bad else 1
    os.makedirs(a.out_dir, exist_ok=True)
    for lv in levels:
        name, img = render(lv, a.data)
        p = os.path.join(a.out_dir, f"level{lv:02d}_{name.lower()}.png")
        img.save(p)
        print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
