# XXX automap legend

**What:** `LEVELn.XXX`: the legend lines and symbols the automap shows for a level.

**Edition read:** CD (29 files, 73 records), floppy (29, 73).

## Layout

Source: `LoLEngine::loadMapLegendData` `engines/kyra/engine/lol.cpp:4250-4280`; use in the map drawing at `:4363-4387`.

Up to 32 records (the loader caps at 32) of 12 bytes:

| Off | Type | Engine slot | Meaning |
|-----|------|-------------|---------|
| 0 | uint16 | l[3] | x of the square where the symbol is drawn |
| 2 | uint16 | l[4] | y of that square |
| 4 | uint16 | l[5] | automap shape index (`_automapShapes[l[5] << 2]`), 0xFFFF = no symbol |
| 6 | uint16 | l[0] | x of the square that must be explored |
| 8 | uint16 | l[1] | y of that square |
| 10 | uint16 | l[2] | string id of the legend text, 0xFFFF = none |

The legend line is printed only when square (l[0], l[1]) is fully explored (`flags & 7 == 7`); drawing the symbol also marks square (l[3], l[4]) as explored. Block index = x + y x 32.

The memo's field names (shapeDrawX, shapeDrawY, shapeIndex, labelBlockX, labelBlockY, stringID) are in the right order. CONFIRMED.

## Confirmed

`tools/xxx_reader.py --check` (CD): `29 files, 73 records (all sizes multiple of 12, <=32 records), 0 without shape, string-id top bits [1, 3], bad=none`. All coordinates are < 32. String ids carry bit 0x4000 (global `LANDS` strings) on 71 records; the other 2 are 0xFFFF (no text, skipped by the draw). No real id has bit 0x8000 in either edition: the `3` in the check output is those two 0xFFFF ids. CONFIRMED (both editions), [Q12](../OPEN_QUESTIONS.md) answered ([`../unknowns/12_legend_bit.md`](../unknowns/12_legend_bit.md)).


## Worked example

CD `LEVEL1.XXX` (72 bytes = 6 records), record 0 and 1:

```
0d 00 0d 00 01 00 0d 00 0e 00 d0 41     12 00 08 00 04 00 10 00 08 00 d1 41
```

| Record 0 | Meaning |
|----------|---------|
| `0d 00`, `0d 00` | symbol on square x 13, y 13 |
| `01 00` | automap symbol 1 |
| `0d 00`, `0e 00` | shown once square x 13, y 14 is explored |
| `d0 41` | string 0x41D0: bit 0x4000 = global strings (`LANDS.ENG`), index 0x1D0 = 464 = "FOUNTAIN" |

Record 1 the same way: symbol 4 at (18, 8), shown after (16, 8) is explored, string 465 = "THRONE ROOM".

## Tool

`tools/xxx_reader.py LEVEL1.XXX`, `--check`.
