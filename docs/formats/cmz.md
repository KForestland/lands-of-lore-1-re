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

`tools/lol1lib.py: load_bitmap()`; `tools/cmz_analyzer.py`, `tools/level_renderer.py` (need path edits).
