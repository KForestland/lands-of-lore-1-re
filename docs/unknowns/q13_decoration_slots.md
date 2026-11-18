# Q13. Which scene position each decoration slot is

The ten slots are ten distances and wall faces, not a left-to-right order. Slot 0 is on the party's own square. Slots 1, 2 and 3 are the front wall one, two and three steps ahead. Slots 4 through 9 are the side walls at those same distances. A negative index in the draw table is the same slot, mirrored.

## Where the number is stored

A decoration record is 72 bytes (`LEVEL*.DAT`). The first 20 bytes are ten little-endian uint16 shape indexes, slots 0 through 9. `0xFFFF` means that slot is empty. The draw does not read a position out of the record. It reads the shape, the scale flag, and the x and y nudge for whichever slot the scene table names.

The scene is 18 cells. The party stands in cell 16 and looks toward the top of this map (`engines/kyra/engine/scene_rpg.cpp:133-148`):

```
00 | 01 | 02 | 03 | 04 | 05 | 06
   | 07 | 08 | 09 | 10 | 11 |
      | 12 | 13 | 14 |
         15 | 16 | 17
            | (P) |
```

`drawDecorations` (`engines/kyra/engine/scene_lol.cpp:1443-1457`) walks the two entries of one cell. Entry `s` uses `_dscShapeIndex[s]` as the slot, and `(_currentDirection + _dscWalls[s]) & 3` as the wall of that cell. Wall 0 is north, 1 east, 2 south, 3 west. A scale of 0 skips the entry (`scene_lol.cpp:1454-1455`). A negative shape index mirrors the shape (`scene_lol.cpp:1508-1517`). The byte `0xFF` in the wall table is -1, and -1 mod 4 is 3, so it is the west face when the party faces north. It is not a skip.

The depth byte `_dscDimMap` (`devtools/create_kyradat/resources/lol_dos_cd.h:1042-1045`) is 0, 1, 2 or 3 and only picks an overlay. It is not a slot number.

## The tables

CONFIRMED. The floppy and CD copies in ScummVM are the same 36 bytes. Shape index: `lol_dos.h:757-763` and `lol_dos_cd.h:822-828`. Wall delta: `lol_dos.h:748-753` and `lol_dos_cd.h:812-817`. Both `MAIN.EXE` files contain that pair of tables once. In the CD executable (356928 bytes) the wall bytes are at file `0x32017` and the shape bytes at file `0x3203b`. In the LANDSoL executable (373872 bytes) they are at file `0x37e29` and `0x37e4d`.

Shape bytes, one pair per cell, as signed values. The second of the pair is drawn first:

| Cell | Slots | Wall deltas, facing north |
| --- | --- | --- |
| 0 | 3, 9 | west, west |
| 1 | 3, 8 | south, east |
| 2 | 3, 7 | south, east |
| 3 | 3, 3 | south, west |
| 4 | 3, -7 | south, west |
| 5 | 3, -8 | south, west |
| 6 | 3, -9 | west, west |
| 7 | 2, 9 | south, east |
| 8 | 2, 6 | south, east |
| 9 | 2, 2 | south, west |
| 10 | 2, -6 | south, west |
| 11 | 2, -9 | south, west |
| 12 | 1, 5 | south, east |
| 13 | 1, 1 | south, west |
| 14 | 1, -5 | south, west |
| 15 | 0, 4 | west, east |
| 16 | 0, 0 | south, west |
| 17 | 0, -4 | west, west |

A scale of 0 drops the second entry of cells 0, 3, 6, 9 and 13, the first entry of cells 15 and 17, and the second entry of cell 16. Those entries are present in the index and never drawn.

Facing north, the draws that remain:

| Slot | Where it is drawn |
| --- | --- |
| 0 | Cell 16, the south face of the party's own square. That is the wall behind the party. |
| 1 | Cells 12, 13 and 14, the south face. One step ahead, left, centre and right. |
| 2 | Cells 7 through 11, the south face. Two steps ahead. |
| 3 | Cells 1 through 5, the south face, three steps ahead. Also the west face of cell 0 and of cell 6, the two far corners. |
| 4 | Cell 15 east face, and cell 17 west face, mirrored. The two faces immediately beside the party. |
| 5 | Cell 12 east face, and cell 14 west face, mirrored. Side walls, one step ahead. |
| 6 | Cell 8 east face, and cell 10 west face, mirrored. Inner side walls, two steps ahead. |
| 7 | Cell 2 east face, and cell 4 west face, mirrored. Inner side walls, three steps ahead. |
| 8 | Cell 1 east face, and cell 5 west face, mirrored. Outer side walls, three steps ahead. |
| 9 | Cell 7 east face, and cell 11 west face, mirrored. Outer side walls, two steps ahead. |

Any other facing adds the facing to the wall delta and uses the same slot. The mirror stays on the right-hand cells.

## Worked example

CD `KEEP.DAT` has 26 records of 72 bytes. Record 1's ten shape indexes are `FFFF`, `0011`, `0014`, `0015`, then six times `FFFF`. Slot 0 is empty. Slot 1 is shape 17, slot 2 is shape 20, slot 3 is shape 21. Slots 4 through 9 are empty. That decoration is drawn on the front wall only, at one, two and three steps, and not on a side wall.

The screen x of a draw is the table base (`lol_dos_cd.h:859-866`; the floppy copy matches) plus the record's own x nudge for that slot, plus 112 (`scene_lol.cpp:1521`).
