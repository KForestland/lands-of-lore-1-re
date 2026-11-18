# CMZ level maps

**What:** the 32x32 block map of a level: four wall-type bytes per block (north, east, south, west).

**Edition read:** CD `DATA/` (29), LANDSoL (29).

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
- Header bytes 0-3 = `20 00 20 00` on all 29. CONFIRMED (CD). Reading them as width = 32, height = 32 fits the grid but no reader is known: UNCONFIRMED, Grok item 2. (The lead order calls this "WLL header bytes 0-3"; the unknown bytes in `docs/level_tileset_map.md` are the CMZ header ones. WLL has a 2-byte header only.)
- Level 24's 5 extra bytes per block: OPEN, Grok item 3.

## Tool

`tools/lol1lib.py: load_bitmap()`; `tools/cmz_analyzer.py` (wall-type statistics, `--check`), `tools/level_renderer.py` (map PNGs, `--check`).

## Correction: `data/wall_type_analysis.json`

The March file was produced with the old LCW decoder (memo B.4) and had wrong wall counts on every level (headers were right). It was regenerated on 2026-11-18 with `cmz_analyzer.py`. On level 1 the solid blocks now show the expected pattern: (2,2,1,1) and (1,1,2,2) alternate 470/469 times, which is the checkerboard the floor/ceiling drawing uses (`scene_rpg.cpp:152-157`). CONFIRMED.

## Open

- Wall types used in the CMZ that the level's own WLL does not define: level 2 (46, 53-57, 59, 60), level 3 (58, 61, 63, 66, 67), level 21 (42). CONFIRMED on CD (`level_renderer.py --check`). ScummVM zero-fills the wall arrays once at start-up (`engines/kyra/engine/kyra_rpg.cpp:190`) and `loadLevelWallData` does not clear them, so such a wall keeps whatever an earlier level set, or 0. Whether the original behaves the same, and whether scripts replace these walls before they are seen, is UNCONFIRMED.
