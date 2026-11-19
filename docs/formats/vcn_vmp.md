# VCN and VMP wall tile sets

**What:** per area (KEEP, FOREST1, …, plus YVEL2): `AREA.VCN` holds 8x8 4-bit tiles with their colour mapping; `AREA.VMP` holds the tile layouts for the floor/ceiling and for each wall page. Together with CMZ and WLL they draw the 3D view.

**Edition read:** CD `DATA/` (13 sets) and floppy (13 sets).

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

Decompressed size = 514 + 33n exactly. CONFIRMED on all 13 sets, CD and floppy.

**Correction to `docs/level_tileset_map.md`:** "OR tile_count × 64 bytes (8×8 @ 8bpp)" — the LoL loader always copies `tlen << 5` = 32 bytes per tile (`scene_lol.cpp:345-346`); the 8-bit variant belongs to other engines (`_vcnSrcBitsPerPixel`, `scene_rpg.cpp:373`). Not seen on either LoL1 edition. CONFIRMED (sizes).

## VMP, decompressed

Source: `scene_lol.cpp:390-402` (load), `scene_rpg.cpp:150-157` (floor/ceiling), `:270-305` (`generateVmpTileData`, `…Flipped`).

| Words | Meaning |
|-------|---------|
| 0 | uint16 word count m |
| 1 .. 330 | floor and ceiling layout of the 22x15-tile (176x120 px) view; drawn mirrored on every other square (`scene_rpg.cpp:152-157`) |
| then 431 per page | wall layout page p (WLL `vmp_map` value p, 1-based) at word 330 + (p − 1) x 431; positions within a page come from `_vmpVisOffs` (executable table) |

Pieces of a wall page. The view draws a wall face with one of nine pieces (side walls at four depths, walls facing the player at three depths); each position has its own pre-drawn piece in the page. Sizes are the `numBlocks` arguments of the `generateVmpTileData` calls (`scene_rpg.cpp:161-267`); start offsets within the page are ScummVM's `_vmpOffsetsDefault` (`engines/kyra/resource/staticres_rpg.cpp:53`, used for every platform but Sega CD):

| Piece | Columns x rows (8 px tiles) | Words | Start in page | Drawn at (tile column, row) |
|-------|-----------------------------|-------|---------------|------------------------------|
| 0 | 3 x 5 | 15 | 102 | side walls three squares ahead, outer (-2 and 2, row 3; mirrored at 21 and 17) |
| 1 | 1 x 5 | 5 | 97 | side walls three squares ahead, inner (8, row 3; mirrored at 13) |
| 2 | 6 x 5 | 30 | 129 | walls three squares ahead (-4, 2, 8, 14, 20, row 3) |
| 3 | 2 x 6 | 12 | 117 | side walls two squares ahead, outer (0, row 3; mirrored at 20) |
| 4 | 2 x 8 | 16 | 81 | side walls two squares ahead, inner (6, row 2; mirrored at 14) |
| 5 | 10 x 8 | 80 | 159 | walls two squares ahead (-4, 6, 16, row 2) |
| 6 | 3 x 12 | 36 | 45 | side walls of the square ahead (3, row 1; mirrored at 16) |
| 7 | 16 x 12 | 192 | 239 | walls one square ahead (3, row 1; also -13 and 19, cut by the view edge) |
| 8 | 3 x 15 | 45 | 0 | side walls of the player's own square (0, row 0; mirrored at 19) |

The nine pieces tile the 431 words exactly, without gap or overlap. CONFIRMED as a layout by drawing: `tools/vcn_vmp_reader.py AREA --walls-png` assembles every piece of every page on KEEP, CAVE1, RUIN and SWAMP (CD and floppy) into clean perspective wall faces (KEEP page 1 plain stone, 2 window, 3 open archway, 4 bird relief, 5 fountain niche, 6 double door). The offset table itself was not found as nine consecutive 16-bit words in either `MAIN.EXE` (it may sit in the code as immediates); UNCONFIRMED in the program.

Each word: tile index into the VCN; bit 0x4000 = mirror horizontally (`scene_rpg.cpp:297`, `:365-368`); 0 = transparent (keep what is below).

m = 330 + 431 x pages on every set. CONFIRMED, `tools/vcn_vmp_reader.py --check` (CD):
`CATWALK:1845t/2485w/5p CAVE1:1822t/2485w/5p CIMMERIA:1085t/2916w/6p FOREST1:960t/1192w/2p KEEP:1282t/2916w/6p MANOR:1240t/2054w/4p MINE1:1903t/2916w/6p RUIN:1250t/2054w/4p SWAMP:1505t/1623w/3p TOWER1:1331t/2485w/5p URBISH:1890t/2916w/6p YVEL1:1487t/2054w/4p YVEL2:1379t/2054w/4p` (t = tiles, w = VMP words, p = wall pages). floppy gives the same numbers. Every VMP tile index is below the VCN tile count.

The memo's "431-entry pages, stride = 22×15 viewport + overhead" is now precise: 330 words (= 22 x 15) of floor/ceiling first, then 431-word wall pages. The memo's YVEL2 VMP figure "2054 entries" matches.

## Open

- [Q4](../OPEN_QUESTIONS.md), answered ([`../unknowns/04_yvel2.md`](../unknowns/04_yvel2.md)): `LEVEL22.INI` tests game flag 357; if set it loads YVEL1 and then YVEL2 (the second load replaces the first), otherwise YVEL1. In `LEVEL22.INF`, a mouse click inside a screen rectangle while the north wall of block 145 has type 8 loads YVEL2 and sets flag 357; another event path loads YVEL1 and clears it. All calls pass special colour 102, weight 12, VCN length 50000 and VMP length 4500 (larger than YVEL2's own data). What the loader does with them is CONFIRMED in both programs (CD `MAIN.EXE` loader at file offset 0x464DB; floppy the same code, tests at 0x4FD34 and 0x4FF45): a length other than 0xFFFF is a byte count. The level loader frees both buffers first (CD 0x46EB2-0x46EEE, called at 0x470AD before the WLL load at 0x47109 and the `level%d.ini` run). The first call then allocates each buffer with the requested size (CD 0x4658A-0x465A4, 0x466F4-0x4670E) and every call copies exactly that many bytes (CD 0x46685-0x46692, 0x46711-0x4672A). So level 22 keeps 50000 VCN bytes (YVEL2 has 44128 tile bytes, YVEL1 47584; the rest is whatever follows the file in the load buffer) and 4500 VMP bytes, which is 2250 words; both YVEL files have 2054. ScummVM reads the VMP length as a count of words instead. The extra words matter for one wall: `LEVEL22.WLL` gives wall type 24 VMP page 5 (words 2054-2484 by ScummVM's indexing, past the 4 pages of both YVEL sets), and the map uses type 24 on all four faces of block 27 (both editions). What the view shows there is UNCONFIRMED; settle it by looking at block 27 of level 22 in a running game. Both editions. Static scan (`tools/tileset_mapper.py`): only level 22 names YVEL2: `LEVEL22.INI` calls `loadLevelGraphics` with YVEL1, YVEL2, YVEL1 and `LEVEL22.INF` with YVEL2, YVEL1, YVEL1, YVEL2. CONFIRMED. (`loadLevelGraphics` is called by script function `olol_loadLevelGraphics`, `engines/kyra/script/script_lol.cpp:208-212`, with the file name as a string; `scene_lol.cpp:315` names YVEL2 for the 16-colour mode.)
- The shift table values on KEEP are 0, 16, …, 112 (CONFIRMED, `vcn_vmp_reader.py KEEP`): each tile picks one of 8 banks of 16 entries in the 128-byte colour table. The bank is the per-tile shift byte in the VCN, ORed into each pixel nibble by the DOS drawer ([Q16 answered](../unknowns/16_vcn_colour_banks.md)).

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


## Worked example

CD `KEEP.VCN` decompressed starts `02 05  70 70 70 …`: 0x502 = 1282 tiles, then the per-tile shift bytes (0x70 = 112, bank 7). The file is 2 + 1282 + 128 + 384 + 1282 x 32 = 42820 bytes, as decompressed.

CD `KEEP.VMP` decompressed starts `64 0b  01 00 02 00 03 00 04 00 05 00 …`: 0xB64 = 2916 words = 330 + 6 x 431. Words 0-329 are the floor and ceiling: tiles 1, 2, 3, … in reading order. Word 330, the start of wall page 1, is `fa 00` = tile 250; the next words `fb 80`, `fc 80` have bit 15 set (0x80FB): in the drawing code that bit marks a tile drawn over the floor/ceiling instead of replacing it (`engines/kyra/engine/scene_rpg.cpp:359-363`).

## Tool

`tools/vcn_vmp_reader.py AREA [--png tiles.png] [--walls-png walls.png]`, `--check`. `--png` writes the tiles in file order, `--walls-png` the wall pages assembled as above. Level maps: `tools/level_renderer.py --level N --out-dir d/` (top-down overview: one flat colour per wall type, the average of that type's piece 7; `--check`). Level-to-set table: `tools/tileset_mapper.py` (`data/tileset_mapping.json`).
