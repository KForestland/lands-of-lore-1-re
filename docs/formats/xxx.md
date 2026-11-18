# XXX automap legend

**What:** `LEVELn.XXX`: the legend lines and symbols the automap shows for a level.

**Edition read:** CD (29 files, 73 records), LANDSoL (29, 73).

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

`tools/xxx_reader.py --check` (CD): `29 files, 73 records (all sizes multiple of 12, <=32 records), 0 without shape, string-id top bits [1, 3], bad=none`. All coordinates are < 32. String ids carry bit 0x4000 (global `LANDS` strings) and some also 0x8000; what 0x8000 means here is UNCONFIRMED (`printMapText` not traced), [Q12](../OPEN_QUESTIONS.md).

## Tool

`tools/xxx_reader.py LEVEL1.XXX`, `--check`.
