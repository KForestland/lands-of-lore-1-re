# WLL wall-type tables

**What:** per level, what each wall-type number means: which VMP wall layout, which decoration, special type, flags, automap symbol.

**Edition read:** CD (29). floppy (29, count only).

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
| 8 | uint8 (byte 9 skipped) | `_wllWallFlags[c]` (bits used e.g. 1, 2, 7, 8, 0x20: `scene_lol.cpp:522-534`, `sprites_lol.cpp:1367-1408`, `lol.cpp:2580`, `:3007-3010`) |
| 10 | uint8 (byte 11 skipped) | `_wllAutomapData[c]` (17 = special in `loadBlockProperties`; `& 0xC0` tested by the automap, `lol.cpp:4228-4342`) |

The skipped odd bytes are the high bytes of 16-bit fields. ScummVM keeps only the low byte, and so does the original loader: it reads each 12-byte record and stores only the low bytes of the VMP, special, flags and automap words (CD `MAIN.EXE` file offsets 0x473AE-0x473FA, floppy 0x50B91-0x50BDD; see also [native rules](../unknowns/07_native_rules.md)). On the data, bytes 3, 7 and 9 are 0 in all 1726 records of both editions. Byte 11 is 0xFF in 430 records, always together with byte 10 = 0xFF (automap word 0xFFFF), and 0 in the rest. CONFIRMED (both editions).

## Confirmed

All 29 files: (size − 2) % 12 == 0; area indexes 0..11 all used. CONFIRMED (CD scan). Full per-level parse: `data/wll_parsed.json` (from March 2026, rebuilt exactly by `tools/wll_parser.py`).

The meaning of each flag bit and special type is game logic, not file format: [Q7](../OPEN_QUESTIONS.md).


## Worked example

CD `LEVEL1.WLL` starts:

```
00 00   00 00 00 00 00 00 00 00 80 00 3f 00   01 00 01 00 00 00 00 00 07 00 ff ff   02 00 …
```

| Bytes | Meaning |
|-------|---------|
| `00 00` | area 0: `KEEP.SHP` / `KEEP.DAT` |
| record 0: `00 00 00 00 00 00 00 00 80 00 3f 00` | wall type 0: no geometry, no shape, special 0, flags 0x80, automap 0x3F |
| record 1: `01 00 01 00 00 00 00 00 07 00 ff ff` | wall type 1: VMP page 1, shape 1, special 0, flags 7, automap word 0xFFFF (low byte 0xFF stored) |

## Tool

`tools/wll_parser.py` (summary, `--out`, `--check` rebuilds `data/wll_parsed.json` exactly: 29 files, 1726 records). Wall types used by a CMZ but missing from its WLL: see [cmz.md](cmz.md#open).
