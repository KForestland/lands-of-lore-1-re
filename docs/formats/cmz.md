# CMZ level maps

**What:** the 32x32 block map of a level: four wall-type bytes per block (north, east, south, west).

**Edition read:** CD `DATA/` (29), floppy (29).

## Layout

The file is a bitmap container ([cps.md](cps.md) header, Frame4). Decompressed:

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | 0x0020 on all 29 levels, both editions read (CD checked) — OPEN, see below |
| 2 | uint16 | 0x0020 on all 29 levels — OPEN |
| 4 | uint16 | len = bytes per block |
| 6 | 1024 x len | block records; bytes 0-3 = walls[N, E, S, W] (uint8 wall type, see [wll.md](wll.md)) |

Source: `LoLEngine::loadBlockProperties` `engines/kyra/engine/scene_lol.cpp:242-260` (reads `h[4]` as len and the first 4 bytes of each block; bytes 0-3 of the header and bytes 4.. of each block are not read there). The file name is passed by the level script (`olol_loadBlockProperties`, `engines/kyra/script/script_lol.cpp:214-216`); `getBlockFileData` loads `LEVEL%d.CMZ` directly (`scene_lol.cpp:262-265`).

## Confirmed

- len = 4 for 28 levels, len = 9 for `LEVEL24.CMZ`; decompressed size = 6 + 1024 x len for all 29. CONFIRMED (CD, `lol1lib.load_bitmap`).
- Header bytes 0-3 = `20 00 20 00` on all 29. CONFIRMED (CD). The same on all 29 levels of floppy. No engine code reads them (`loadBlockProperties`, and the save code `engines/kyra/gui/saveload_rpg.cpp:49-60`, start at offset 4). Reading them as width = 32, height = 32 fits the grid; that is a reading of the values, not of code ([Q2](../OPEN_QUESTIONS.md), answered as far as the data allows; [`../unknowns/02_wll_header.md`](../unknowns/02_wll_header.md)). (The bytes called "unknown" in `docs/level_tileset_map.md` are these CMZ header bytes; WLL has only a 2-byte header.)
- Level 24 has 9 bytes per block, i.e. 5 extra bytes; `LEVEL24.CMZ` (549 bytes) is byte-identical in both editions and decompresses to 9222 = 6 + 1024 x 9. The engine copies the 4 wall bytes and steps over the rest, with no level test. The 5 tail bytes take nine patterns: `01 01 01 01 01` on 759 blocks (all solid `(2,2,1,1)`/`(1,1,2,2)` blocks), `00 00 00 00 00` on 230 (all open), `04 00 a4 19 04` on 26, `04 00 ec 16 04` on 3, `04 00 ea 16 04` on 2, and four single blocks whose nine bytes all repeat one value (0x3A, 0x38, 0x4D, 0x3F). CONFIRMED. Both editions' `MAIN.EXE` copy only the 4 wall bytes of each block and step over the tail (CD `MAIN.EXE+0x48540`, `+0x48764`; floppy `+0x51C10`, `+0x51E34`), so the game never reads it. CONFIRMED (disassembled). What the level's author stored there is OPEN, [Q3](../OPEN_QUESTIONS.md); measurements and everything tried: [`../unknowns/03_level24_cmz.md`](../unknowns/03_level24_cmz.md). The 26 `04 00 a4 19 04` blocks sit on wall types 46, 53-57 and others; the same wall-type numbers appear undefined on levels 2 and 3 ([Q11](../OPEN_QUESTIONS.md)), also FOREST1 levels.


## Worked example

CD `LEVEL1.CMZ` starts `36 01  04  00  06 10 00 00  00 00 …`: 0x136 + 2 = 312 bytes on file, Frame4, 0x1006 = 4102 bytes decompressed, no palette. The decompressed image:

| Image bytes | Meaning |
|-------------|---------|
| `20 00 20 00` | 32, 32 (not read by the engine) |
| `04 00` | 4 bytes per block |
| `01 01 02 02` | block 0 (x 0, y 0): walls N 1, E 1, S 2, W 2: solid wall |
| block 429 `44 44 44 44` | x 13, y 13 (429 = 13 + 13 x 32): wall type 0x44 on all four sides. The automap legend ([xxx.md](xxx.md)) puts its symbol on this square |

## Tool

`tools/lol1lib.py: load_bitmap()`; `tools/cmz_analyzer.py` (wall-type statistics, `--check`), `tools/level_renderer.py` (map PNGs, `--check`).

## Correction: `data/wall_type_analysis.json`

The March 2026 file was produced with the old LCW decoder (closure memo, section B.4) and had wrong wall counts on every level (headers were right). It was regenerated on 2026-11-18 with `cmz_analyzer.py`. On level 1 the solid blocks now show the expected pattern: (2,2,1,1) and (1,1,2,2) alternate 470/469 times, which is the checkerboard the floor/ceiling drawing uses (`scene_rpg.cpp:152-157`). CONFIRMED.

## Open

- [Q11](../OPEN_QUESTIONS.md): wall types used in the CMZ that the level's own WLL does not define: level 2 (46, 53-57, 59, 60), level 3 (58, 61, 63, 66, 67), level 21 (42); on the floppy also level 29 (57). CONFIRMED on CD (`level_renderer.py --check`). ScummVM zero-fills the wall arrays once at start-up (`engines/kyra/engine/kyra_rpg.cpp:190`) and `loadLevelWallData` does not clear them, so such a wall keeps whatever an earlier level set, or 0. The original loader also leaves the property rows in place ([Q11 answered](../unknowns/11_undefined_walls.md)).
