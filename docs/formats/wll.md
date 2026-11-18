# WLL wall-type tables

**What:** per level, what each wall-type number means: which VMP wall layout, which decoration, special type, flags, automap symbol.

**Edition read:** CD (29). LANDSoL (29, count only).

## Layout

Source: `LoLEngine::loadLevelWallData` `engines/kyra/engine/scene_lol.cpp:142-178`.

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | area index into `_levelShpList` / `_levelDatList` (which `AREA.SHP` + `AREA.DAT`, `scene_lol.cpp:147-149`; lists from the executable, `resource/staticres_lol.cpp:282-283`) |
| 2 | 12-byte records, (size − 2) / 12 of them | |

Record:

| Off | Read as | Field |
|-----|---------|-------|
| 0 | uint16 | wall type number c (index of the arrays below) |
| 2 | uint8 (byte 3 skipped) | `_wllVmpMap[c]`: VMP wall layout (page) 1..6, 0 = none |
| 4 | int16 | shape map: > 0 = index into `AREA.DAT` ([dat.md](dat.md)) via `assignLevelDecorationShapes`; else the low byte is stored |
| 6 | uint8 (byte 7 skipped) | `_specialWallTypes[c]` |
| 8 | uint8 (byte 9 skipped) | `_wllWallFlags[c]` (bits used e.g. 1, 2, 7, 8, 0x20: `scene_lol.cpp:522-534`, `sprites_lol.cpp:1367-1408`, `lol.cpp:2633`, `:3060-3063`) |
| 10 | uint8 (byte 11 skipped) | `_wllAutomapData[c]` (17 = special in `loadBlockProperties`; `& 0xC0` tested by the automap, `lol.cpp:4281-4395`) |

The skipped odd bytes are the high bytes of 16-bit fields; ScummVM keeps only the low byte. Whether the original ever sets them is UNCONFIRMED.

## Confirmed

All 29 files: (size − 2) % 12 == 0; area indexes 0..11 all used. CONFIRMED (CD scan). Full per-level parse: `data/wll_parsed.json` (memo).

The meaning of each flag bit and special type is game logic, not file format: Sol item 8b.

## Tool

`tools/wll_parser.py` (needs path edits, see STATUS).
