# DAT area decoration tables

**What:** `AREA.DAT` (KEEP.DAT, CAVE1.DAT, …): how each wall decoration is drawn at each visible position, as shape indexes into the matching `AREA.SHP`.

**Edition read:** CD (12), LANDSoL (12).

## Layout

Source: `LoLEngine::loadLevelShpDat` `engines/kyra/engine/scene_lol.cpp:267-298`; selection through WLL in `loadLevelWallData` `:158-164` and `assignLevelDecorationShapes` `:180-214`.

uint16 count, then count x 72-byte `LevelDecorationProperty`:

| Off | Type | Field |
|-----|------|-------|
| 0 | uint16[10] | shapeIndex (into AREA.SHP; 0xFFFF = none) |
| 20 | uint8[10] | scaleFlag |
| 30 | int16[10] | shapeX |
| 50 | int16[10] | shapeY |
| 70 | uint8 | next: another record drawn with this one (0 = none) |
| 71 | uint8 | flags |

The ten slots are the views at the ten scene positions where a decoration can be seen (UNCONFIRMED: the slot-to-position order is in the drawing code, `scene_lol.cpp:1418-1470`, not traced here; [Q13](../OPEN_QUESTIONS.md)).

## Confirmed

`tools/dat_reader.py --check` (CD): `12 files, size == 2+72*count, shape indexes < shapes in the area SHP, next < count: 12/12; CATWALK.DAT:68 CAVE1.DAT:78 CIMMERIA.DAT:114 FOREST1.DAT:43 KEEP.DAT:26 MANOR.DAT:31 MINE1.DAT:82 RUIN.DAT:33 SWAMP.DAT:40 TOWER1.DAT:66 URBISH.DAT:68 YVEL1.DAT:32`. LANDSoL: same 12 counts.

There is no YVEL2.DAT; Level 22, the only level that uses YVEL2, takes its decorations from YVEL1.DAT via its WLL area (index 8). Whether anything changes when the scripts switch to YVEL2 is [Q4](../OPEN_QUESTIONS.md).

## Tool

`tools/dat_reader.py KEEP.DAT [--index n]`, `--check`.
