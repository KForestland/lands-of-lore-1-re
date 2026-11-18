# TLC transparency tables (CD only)

**What:** `LEVELnn.TLC`, one per level, CD edition only: two lookup tables used to draw see-through colours (glass, ghosts, effect colours) over the scene.

**Edition read:** CD (29 files). floppy has none (CONFIRMED: `tlc_reader.py --check` finds 0).

## Correction to the closure memo

The memo says "21 × 256-byte remap tables per level (lighting/effect remaps)". The size (5376 = 21 x 256) is right; the structure and use are not lighting:

Source: `engines/kyra/engine/scene_lol.cpp:458-462` (CD edition only, `_flags.isTalkie`: read 256 bytes into `_transparencyTable1`, 5120 into `_transparencyTable2`); floppy builds the same tables at run time in `LoLEngine::createTransparencyTables` `engines/kyra/engine/lol.cpp:1844-1879` from `FXPAL.COL` and the colour list in `FXPAL.SHP`, using `Screen_LoL::createTransparencyTablesIntern` `engines/kyra/graphics/screen_lol.cpp:144-185` (20 slots, weight 70).

| Offset | Size | Meaning |
|--------|------|---------|
| 0 | 256 | table1: for each colour, its effect slot 0..19, or 0xFF = opaque |
| 256 | 20 x 256 | table2: for slot i, row i maps the screen colour under the pixel to the blended colour |

Drawing: `screen.cpp:2314-2331` (`_dsTransparencyTable1[cmd]`, then `_dsTransparencyTable2[slot << 8 | *dst]`); used for item and monster shapes (`sprites_lol.cpp:908-980`) and TIM animations (`graphics/animator_tim.cpp:212`).

## Confirmed

`tools/tlc_reader.py --check` (CD): `29 files, all 5376 bytes and table1 values <20: 29/29, distinct table1 maps: 1`. Table1 is identical in all 29 files (the same effect colours everywhere); table2 comes in 15 distinct versions over the 29 levels (CONFIRMED, CD), consistent with blending against each area's palette. The cause of the differences is UNCONFIRMED (expected from `screen_lol.cpp:170-178`, not recomputed here).


## Worked example

CD `LEVEL01.TLC` starts `00 ff 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e …`:

| Colour | table1 | Meaning |
|--------|--------|---------|
| 0 | `00` | slot 0 |
| 1 | `ff` | opaque, drawn normally |
| 2 … 15 | `01` … `0e` | slots 1-14 |

Byte 256 starts table2 row 0, which is all zeros (`00 00 00 …`). Slot 0 belongs to colour 0, and createTransparencyTablesIntern leaves a zero row for colour 0 (`engines/kyra/graphics/screen_lol.cpp:181-182`).

## Tool

`tools/tlc_reader.py LEVEL01.TLC`, `--check`.
