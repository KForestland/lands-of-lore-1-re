# DAT area decoration tables

**What:** `AREA.DAT` (KEEP.DAT, CAVE1.DAT, …): how each wall decoration is drawn at each visible position, as shape indexes into the matching `AREA.SHP`.

**Edition read:** CD (12), floppy (12).

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

The ten slots are the views at the ten scene positions where a decoration can be seen (the slot-to-position order is traced in both executables: [Q13 answered](../unknowns/13_decoration_positions.md)).

## Confirmed

`tools/dat_reader.py --check` (CD): `12 files, size == 2+72*count, shape indexes < shapes in the area SHP, next < count: 12/12; CATWALK.DAT:68 CAVE1.DAT:78 CIMMERIA.DAT:114 FOREST1.DAT:43 KEEP.DAT:26 MANOR.DAT:31 MINE1.DAT:82 RUIN.DAT:33 SWAMP.DAT:40 TOWER1.DAT:66 URBISH.DAT:68 YVEL1.DAT:32`. floppy: same 12 counts.

The measured archives contain `YVEL1.DAT` and `YVEL1.SHP`. There is no `YVEL2.DAT`. In both editions the Level 22 WLL starts with area index 8, the YVEL1 decoration set.


## Worked example

CD `KEEP.DAT` starts `1a 00`: 26 records. Record 1 (bytes 74-145), read with `tools/dat_reader.py KEEP.DAT --index 1`:

| Field | Values (slots 0-9) |
|-------|-------------------|
| shapeIndex | –, 17, 20, 21, –, –, –, –, –, – (– = 0xFFFF, not drawn) |
| scaleFlag | all 0 |
| shapeX | 0, 99, 65, 40, 0, … |
| shapeY | 0, 41, 27, 18, 0, … |
| next, flags | 0, 8 |

So this decoration has views at three of the ten positions (shapes 17, 20 and 21 of `KEEP.SHP`), each with its own screen offset.

## Tool

`tools/dat_reader.py KEEP.DAT [--index n]`, `--check`.
