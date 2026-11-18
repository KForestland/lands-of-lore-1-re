# Q16. What picks the 16-colour bank of a wall tile

The VCN file stores one byte per tile. ScummVM copies that byte and ORs it into the colour index. It does not recompute the bank from the light.

## The byte in the file

A 256-colour VCN, after the usual bitmap wrapper, starts with a little-endian uint16 tile count. Then, in order: that many shift bytes, a 128-byte colour table, a 384-byte palette, and the tile bytes (`engines/kyra/engine/scene_lol.cpp:339-367`).

`loadLevelGraphics` allocates a shift array of `tlen` bytes and copies the file bytes into it (`scene_lol.cpp:351-355`). Nothing else writes `_vcnShift`. The constructor sets the pointer to null (`engines/kyra/engine/kyra_rpg.cpp:50`) and sets `_wllVcnOffset` to 0 (`kyra_rpg.cpp:59`). The Lands of Lore loader always allocates the table, so the null case does not run in this game.

## How the drawer uses it

CONFIRMED for ScummVM. `drawVcnBlocks` (`engines/kyra/engine/scene_rpg.cpp:386`) sets

```
_vcnShiftVal = _vcnShift[vcnOffset]
```

and the fallback `_blockBrightness` only when `_vcnShift` is null. Before the wall path it also sets `_wllVcnOffset2 = _wllVcnOffset` (`scene_rpg.cpp:374`), which Lands of Lore left at 0. The four 4-bit drawers build the colour index as

```
(nibble + _wllVcnOffset2) | _vcnShiftVal
```

(`scene_rpg.cpp:429-430`, and the same OR at `:438-439`, `:448-449` and `:471-472`). The bank is the file byte. Light does not change it.

Two other bits on a VMP word are not this bank. `0x8000` draws a wall over the transparent pixels of a floor or ceiling tile (`scene_rpg.cpp:359-363`). `0x4000` flips the tile (`scene_rpg.cpp:366-368`). The shift byte is a separate array, indexed by the tile number after those bits are removed.

The 16-colour path in `loadLevelGraphics` (`scene_lol.cpp:311` and `:351`) does not load this table. That path is off for the CD and the floppy. `LOL_CD_FLAGS` and `LOL_FLOPPY_FLAGS` leave `use16ColorMode` clear (`engines/kyra/detection_tables.h:56` and `:58`). It is on for the PC-98 flags.

## Worked example

CD and LANDSoL `KEEP.VCN` decompress to the same 42820-byte image. The first two bytes are `02 05`, tile count 1282. The next 1282 bytes are the shift table, and they begin `70 70 70 70`. `0x70` is 112, which is bank 7 (112 = 7 times 16). The only values in the table are the eight multiples of 16:

| Shift byte | Bank | Tiles |
| --- | --- | --- |
| 0 | 0 | 298 |
| 16 | 1 | 181 |
| 32 | 2 | 77 |
| 48 | 3 | 133 |
| 64 | 4 | 124 |
| 80 | 5 | 219 |
| 96 | 6 | 160 |
| 112 | 7 | 90 |

298 + 181 + 77 + 133 + 124 + 219 + 160 + 90 = 1282. The image size matches the layout: 2 + 1282 + 128 + 384 + 1282 times 32 = 42820.

Tile 0 therefore draws with `_vcnShiftVal` 112. A nibble of 3 becomes `3 | 112` = 115, then that index goes through the 128-byte colour table. The DOS drawer was not opened, so whether the original program also uses the byte unchanged stays UNCONFIRMED. The file byte, and ScummVM's use of it, are CONFIRMED.
