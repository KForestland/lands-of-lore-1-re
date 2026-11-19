#!/usr/bin/env python3
"""LoL1 top-down level map renderer: CMZ -> WLL -> VMP -> VCN.

Each of the 32x32 blocks becomes a square cell (10 px by default):

  - the block's four wall types (faces N, E, S, W) come from LEVELn.CMZ
    (docs/formats/cmz.md);
  - a wall type with WLL vmp_map p > 0 (docs/formats/wll.md) has geometry; it is
    drawn in the average colour of the face the game shows for it straight ahead,
    one square away: piece 7 (16x12 tiles) of VMP wall page p, assembled from its
    VCN tiles with the level's palette (vcn_vmp_reader.wall_piece,
    docs/formats/vcn_vmp.md);
  - a block whose four faces all have geometry (solid rock) is filled with the
    colour of the level's most common wall type; a face that can be seen (its
    neighbour is not solid) and has another type (a window, relief, the
    alternate wall of a two-texture pattern, a switch) adds a strip of its own
    colour on that side;
  - a block with some faces only (doors, gates, part walls) is floor with a strip
    per face that has geometry;
  - floor is the average colour of the floor rows of the area's floor/ceiling
    layout; every wall edge that meets floor gets a dark outline;
  - only brightness is adjusted, never hue: dark wall sets (swamp, mines) are all
    scaled up by one factor until the brightest wall colour reaches 200, and the
    floor is darkened, if brighter, to 30% of the main wall colour's brightness;
  - a wall page beyond the end of the VMP would be drawn grey (none on either
    edition; --check counts them).

The tile set is the first loadLevelGraphics call of LEVELn.INI (with its
override palette, if any), as listed by tileset_mapper.py. This is a map
overview, not the in-game 3D view: one flat colour per wall type, no textures.

  level_renderer.py --level 1 --out-dir maps/     # one PNG
  level_renderer.py --level 1 --out-dir maps/ --schematic
      # drawing from CMZ + WLL only, no game pixels: open squares light, solid dark,
      # mixed (doors, switches, part walls) orange, decorated walls (WLL shape > 0) red marks
  level_renderer.py --out-dir maps/                # all 29
  level_renderer.py --check                        # every wall page resolves; lists wall types
                                                   # missing from the level's WLL; no PNGs written
"""
import os
import struct
import sys
from collections import Counter

import lol1lib as L
import tileset_mapper
import vcn_vmp_reader as V

UNKNOWN = (128, 128, 128)     # wall page past the end of the VMP
OUTLINE = (12, 10, 8)


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


def mean_colour(grid, rgb):
    """Average RGB of the drawn pixels of an assembled grid (None = not drawn)."""
    px = [rgb[v] for v in grid if v is not None and v < len(rgb)]
    if not px:
        return None
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))


def page_colours(words, tiles, col, shift, rgb):
    """{wall page: average colour of its front face (piece 7)} for every page in the VMP."""
    pages = (len(words) - V.FLOOR_WORDS) // V.PAGE_WORDS
    out = {}
    for p in range(1, pages + 1):
        out[p] = mean_colour(V.wall_piece(words, p, V.FRONT_PIECE, tiles, col, shift)[2], rgb) or UNKNOWN
    return out


def floor_colour(words, tiles, col, shift, rgb):
    """Average colour of the bottom 5 rows (the near floor) of the 22x15 floor/ceiling layout."""
    _, _, grid = V.assemble(words, 10 * 22, 22, 5, tiles, col, shift)
    return mean_colour(grid, rgb) or (40, 40, 48)


def luma(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def readable(colours, floor, main_page, top=200, floor_share=0.3):
    """Keep the hues, fix the brightness so walls read as walls: if the brightest wall
    colour is darker than `top`, scale every wall colour up by the same factor; then
    darken the floor (if needed) to `floor_share` of the main wall colour's brightness."""
    peak = max((max(c) for c in colours.values()), default=0)
    k = top / peak if 0 < peak < top else 1.0
    colours = {p: tuple(min(255, int(v * k)) for v in c) for p, c in colours.items()}
    target = floor_share * luma(colours.get(main_page, UNKNOWN))
    if luma(floor) > target:
        f = target / max(luma(floor), 1)
        floor = tuple(int(v * f) for v in floor)
    return colours, floor


def classify(blocks, vmp, npages):
    """Per block: (pages of the four faces, 0 = no geometry, -1 = page past the VMP end)."""
    out = []
    for walls in blocks:
        faces = []
        for w in walls:
            p = vmp.get(w) or 0
            faces.append(-1 if p > npages else p)
        out.append(faces)
    return out


def draw_map(faces, colours, floor, cell=10):
    """Draw the map from per-block face pages and {page: colour} (pure; used by the unit test)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (32 * cell, 32 * cell), floor)
    d = ImageDraw.Draw(img)
    colour = lambda p: UNKNOWN if p < 0 else colours.get(p, UNKNOWN)
    strip = max(2, cell // 4)
    solid = [all(f != 0 for f in fs) for fs in faces]
    count = Counter(p for i, fs in enumerate(faces) if solid[i] for p in fs)
    main = count.most_common(1)[0][0] if count else 1
    sides = ((0, -1), (1, 0), (0, 1), (-1, 0))      # N, E, S, W
    for i, fs in enumerate(faces):
        bx, by = i % 32, i // 32
        x, y = bx * cell, by * cell
        rects = [(x, y, x + cell - 1, y + strip - 1), (x + cell - strip, y, x + cell - 1, y + cell - 1),
                 (x, y + cell - strip, x + cell - 1, y + cell - 1), (x, y, x + strip - 1, y + cell - 1)]
        if solid[i]:
            # rock is the level's main wall colour; a face that can be seen (its neighbour
            # is not solid) and is of another type shows as a strip on that side
            d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=colour(main))
            for side, p in enumerate(fs):
                nx, ny = bx + sides[side][0], by + sides[side][1]
                seen = 0 <= nx < 32 and 0 <= ny < 32 and not solid[ny * 32 + nx]
                if p != main and seen:
                    d.rectangle(rects[side], fill=colour(p))
        else:
            for side, p in enumerate(fs):
                if p:
                    d.rectangle(rects[side], fill=colour(p))
    # dark outline where a solid block meets a block that is not solid
    for i in range(1024):
        if not solid[i]:
            continue
        bx, by = i % 32, i // 32
        x, y = bx * cell, by * cell
        for dx, dy, line in ((0, -1, (x, y, x + cell - 1, y)), (1, 0, (x + cell - 1, y, x + cell - 1, y + cell - 1)),
                             (0, 1, (x, y + cell - 1, x + cell - 1, y + cell - 1)), (-1, 0, (x, y, x, y + cell - 1))):
            nx, ny = bx + dx, by + dy
            if 0 <= nx < 32 and 0 <= ny < 32 and not solid[ny * 32 + nx]:
                d.line(line, fill=OUTLINE)
    return img


def render(level, data_dir, check_only=False, cell=10):
    g = tileset_mapper.build(data_dir)[level]["loadLevelGraphics"]
    name, palname = g[0]["vcn_vmp"], g[0]["palette"]
    ntiles, shift, col, pal, tiles, words = area_set(name, data_dir)
    if palname:
        pal = L.find_member(palname, data_dir)[1][:384]
    vmp = wll_vmp(level, data_dir)
    blocks = level_blocks(level, data_dir)
    npages = (len(words) - V.FLOOR_WORDS) // V.PAGE_WORDS
    undefined = {w for walls in blocks for w in walls if w not in vmp}
    faces = classify(blocks, vmp, npages)
    problems = sorted({("page", vmp[w]) for walls in blocks for w in walls if (vmp.get(w) or 0) > npages})
    if check_only:
        return name, problems, undefined
    rgb = L.vga_palette(pal)
    colours = page_colours(words, tiles, col, shift, rgb)
    used = Counter(p for fs in faces if all(fs) for p in fs)
    main = used.most_common(1)[0][0] if used else 1
    colours, floor = readable(colours, floor_colour(words, tiles, col, shift, rgb), main)
    img = draw_map(faces, colours, floor, cell)
    return name, img


def wll_records(level, data_dir):
    b = L.level_member(level, "WLL", data_dir)
    out = {}
    for i in range((len(b) - 2) // 12):
        o = 2 + i * 12
        out[struct.unpack_from("<H", b, o)[0]] = (b[o + 2], struct.unpack_from("<h", b, o + 4)[0])
    return out


def render_schematic(level, data_dir, cell=10):
    """Map drawing that uses only the CMZ wall bytes and the WLL table (no game pixels).

    open square (no wall with geometry): light; solid square (all four walls have
    geometry): dark; mixed square (doors, switches, niches, part walls): orange;
    a wall with a decoration (WLL shape > 0) adds a red mark on that side.
    """
    from PIL import Image, ImageDraw
    rec = wll_records(level, data_dir)
    blocks = level_blocks(level, data_dir)
    geo = lambda w: rec.get(w, (0, 0))[0] > 0
    deco = lambda w: rec.get(w, (0, 0))[1] > 0
    img = Image.new("RGB", (32 * cell, 32 * cell), (40, 40, 48))
    d = ImageDraw.Draw(img)
    for i, walls in enumerate(blocks):
        x, y = (i % 32) * cell, (i // 32) * cell
        n = sum(geo(w) for w in walls)
        colour = (235, 232, 220) if n == 0 else (40, 40, 48) if n == 4 else (230, 150, 50)
        d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=colour)
        marks = [(x + cell // 2, y + 1), (x + cell - 2, y + cell // 2), (x + cell // 2, y + cell - 2), (x + 1, y + cell // 2)]
        for side, w in enumerate(walls):     # walls[N, E, S, W] (docs/formats/cmz.md)
            if deco(w):
                mx, my = marks[side]
                d.rectangle([mx - 1, my - 1, mx + 1, my + 1], fill=(200, 30, 30))
    return img


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("--level", type=int, help="1..29 (default: all)")
    ap.add_argument("--out-dir", help="folder for levelNN_<area>.png (required to write; nothing is written without it)")
    ap.add_argument("--schematic", action="store_true", help="line drawing without game pixels")
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
    if not a.out_dir:
        ap.error("--out-dir is required to write map images")
    os.makedirs(a.out_dir, exist_ok=True)
    for lv in levels:
        if a.schematic:
            img = render_schematic(lv, a.data)
            p = os.path.join(a.out_dir, f"level{lv:02d}_schematic.png")
            img.save(p); print("wrote", p); continue
        name, img = render(lv, a.data)
        p = os.path.join(a.out_dir, f"level{lv:02d}_{name.lower()}.png")
        img.save(p)
        print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
