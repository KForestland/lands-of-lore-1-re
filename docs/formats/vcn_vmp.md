# VCN and VMP wall tile sets

**What:** per area (KEEP, FOREST1, …, plus YVEL2): `AREA.VCN` holds 8x8 4-bit tiles with their colour mapping; `AREA.VMP` holds the tile layouts for the floor/ceiling and for each wall page. Together with CMZ and WLL they draw the 3D view.

**Edition read:** CD `DATA/` (13 sets) and LANDSoL (13 sets).

Both files are bitmap containers ([cps.md](cps.md) header, Frame4, no palette in the header).

## VCN, decompressed (VGA path)

Source: `LoLEngine::loadLevelGraphics` `engines/kyra/engine/scene_lol.cpp:300-389`.

| Offset | Size | Meaning |
|--------|------|---------|
| 0 | uint16 | tile count n |
| 2 | n | shift table `_vcnShift`: per tile, ORed into the colour-table index (`engines/kyra/engine/scene_rpg.cpp:386`, `:429-449`) |
| 2+n | 128 | colour table `_vcnColTable` (16 entries per shift value) |
| 130+n | 384 | palette: 128 colours, 6-bit RGB (replaced when the script passes an override `.PAL`, `scene_lol.cpp:360-367`) |
| 514+n | 32 x n | tiles: 8x8 pixels, 4 bits each (`tlen << 5`), high nibble = left pixel (`scene_rpg.cpp:429-430`) |

Decompressed size = 514 + 33n exactly. CONFIRMED on all 13 sets, CD and LANDSoL.

**Correction to `docs/level_tileset_map.md`:** "OR tile_count × 64 bytes (8×8 @ 8bpp)" — the LoL loader always copies `tlen << 5` = 32 bytes per tile (`scene_lol.cpp:345-346`); the 8-bit variant belongs to other engines (`_vcnSrcBitsPerPixel`, `scene_rpg.cpp:373`). Not seen on either LoL1 edition. CONFIRMED (sizes).

## VMP, decompressed

Source: `scene_lol.cpp:390-402` (load), `scene_rpg.cpp:150-157` (floor/ceiling), `:270-305` (`generateVmpTileData`, `…Flipped`).

| Words | Meaning |
|-------|---------|
| 0 | uint16 word count m |
| 1 .. 330 | floor and ceiling layout of the 22x15-tile (176x120 px) view; drawn mirrored on every other square (`scene_rpg.cpp:152-157`) |
| then 431 per page | wall layout page p (WLL `vmp_map` value p, 1-based) at word 330 + (p − 1) x 431; positions within a page come from `_vmpVisOffs` (executable table) |

Each word: tile index into the VCN; bit 0x4000 = mirror horizontally (`scene_rpg.cpp:297`, `:365-368`); 0 = transparent (keep what is below).

m = 330 + 431 x pages on every set. CONFIRMED, `tools/vcn_vmp_reader.py --check` (CD):
`CATWALK:1845t/2485w/5p CAVE1:1822t/2485w/5p CIMMERIA:1085t/2916w/6p FOREST1:960t/1192w/2p KEEP:1282t/2916w/6p MANOR:1240t/2054w/4p MINE1:1903t/2916w/6p RUIN:1250t/2054w/4p SWAMP:1505t/1623w/3p TOWER1:1331t/2485w/5p URBISH:1890t/2916w/6p YVEL1:1487t/2054w/4p YVEL2:1379t/2054w/4p` (t = tiles, w = VMP words, p = wall pages). LANDSoL gives the same numbers. Every VMP tile index is below the VCN tile count.

The memo's "431-entry pages, stride = 22×15 viewport + overhead" is now precise: 330 words (= 22 x 15) of floor/ceiling first, then 431-word wall pages. The memo's YVEL2 VMP figure "2054 entries" matches.

## Open

- [Q4](../OPEN_QUESTIONS.md): when YVEL2 is switched in. Static scan (`tools/tileset_mapper.py`): only level 22 names YVEL2: `LEVEL22.INI` calls `loadLevelGraphics` with YVEL1, YVEL2, YVEL1 and `LEVEL22.INF` with YVEL2, YVEL1, YVEL1, YVEL2. CONFIRMED (calls on CD); when each runs is open. (`loadLevelGraphics` is called by script function `olol_loadLevelGraphics`, `engines/kyra/script/script_lol.cpp:208-212`, with the file name as a string; `scene_lol.cpp:315` names YVEL2 for the 16-colour mode.)
- The shift table values on KEEP are 0, 16, …, 112 (CONFIRMED, `vcn_vmp_reader.py KEEP`): each tile picks one of 8 banks of 16 entries in the 128-byte colour table. What decides the bank per tile (artist choice vs. lighting) is UNCONFIRMED, [Q16](../OPEN_QUESTIONS.md).

## Which level uses which set

The VCN/VMP set is chosen by the level script, not by the WLL area index: `loadLevelGraphics` (script function 0x09) names it. `tools/tileset_mapper.py` lists every call (35 on CD, the same as the call count of function 0x09 in the script function table). CONFIRMED on CD:

| Levels | Set (+ override palette) |
|--------|--------------------------|
| 1 | KEEP |
| 2 | FOREST1 + ALTPAL2.PAL |
| 3, 24 | FOREST1 + ALTPAL1.PAL |
| 10, 17 | FOREST1 |
| 4 | MANOR |
| 5-9 | CAVE1 |
| 11 | SWAMP |
| 12 | URBISH |
| 13-16 | MINE1 |
| 18-21 | TOWER1 |
| 22 | YVEL1 and YVEL2 (switched by the scripts) |
| 23 | CATWALK |
| **25** | **CAVE1 + CAV_PLT3.PAL** (its WLL area, and so its SHP/DAT, is CATWALK) |
| 26 | RUIN |
| 27-29 | CIMMERIA |

Correction: `docs/level_tileset_map.md` lists level 25 under CATWALK for VCN/VMP; that holds only for its decorations (SHP/DAT).

## Tool

`tools/vcn_vmp_reader.py AREA [--png tiles.png]`, `--check`. Level maps: `tools/level_renderer.py --level N --out-dir d/` (top-down overview, `--check`). Level-to-set table: `tools/tileset_mapper.py` (`data/tileset_mapping.json`).
