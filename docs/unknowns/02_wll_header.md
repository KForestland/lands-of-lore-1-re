# WLL bytes 0-3

`LEVEL*.WLL` has a 2-byte header. Bytes 0-1 are the area index. Bytes 2-3 are the wall-type id of the first 12-byte record, and that id is 0 on every level in both editions.

The word "unknown" in `docs/level_tileset_map.md:46` is the first four bytes of a decompressed CMZ, not the WLL. Those four bytes are below. Level 24's longer block record is `03_level24_cmz.md`.

## Who reads the WLL

CONFIRMED. `LoLEngine::loadLevelWallData` (`engines/kyra/engine/scene_lol.cpp:142-173`) does this:

1. Byte 0, as a little-endian uint16, indexes `_levelShpList` and `_levelDatList` (`scene_lol.cpp:148-149`).
2. The rest of the file is records of 12 bytes. The count is `(file_size - 2) / 12` (`scene_lol.cpp:151-152`).
3. Each record is uint16 wall type, uint8 VMP page, one skipped byte, int16 shape, uint8 special, one skipped byte, uint8 flags, one skipped byte, uint8 automap, one skipped byte (`scene_lol.cpp:154-172`).

The DOS and CD name lists are the same 12 strings (`devtools/create_kyradat/resources/lol_dos.h:669-682` and `lol_dos_cd.h:723-736`). Index 0 is `KEEP.SHP`. Index 8 is `YVEL1.SHP`. There is no `YVEL2` entry. CONFIRMED.

## Bytes on every level

CONFIRMED on CD (`L01.PAK` through `L29.PAK`) and on floppy (`CHAPTER1.PAK` through `CHAPTER8.PAK`), levels 1 through 29:

- `(file_size - 2) % 12 == 0`. A 4-byte header would leave a remainder of 10, and it does: `(file_size - 4) % 12 == 10` on all 58 files.
- The uint16 at file offset 2 is 0. That is the wall-type id of record 0, read at `scene_lol.cpp:154`.

`LEVEL1.WLL` is 626 bytes in `L01.PAK` and in `CHAPTER1.PAK`. Bytes 0-11 are `00 00 00 00 00 00 00 00 00 00 80 00`. Index 0 selects KEEP. Record 0 has wall type 0, and its flags byte (file offset 10) is 0x80.

`LEVEL24.WLL` is 698 bytes in `L24.PAK` and in `CHAPTER6.PAK`. Bytes 0-11 are `01 00 00 00 00 00 00 00 00 00 80 00`. Index 1 selects FOREST1.

`LEVEL22.WLL` is 794 bytes in `L22.PAK` and in `CHAPTER6.PAK`. Bytes 0-1 are `08 00`, index 8, YVEL1. Bytes 2-3 are `00 00`.

The other levels use indexes 0 through 11 as already listed in `docs/level_tileset_map.md`. Sizes match across the two editions. CONFIRMED.

## The four bytes the tileset note calls unknown

CONFIRMED. `docs/level_tileset_map.md:46` marks decompressed CMZ bytes 0-3 as unknown. `loadBlockProperties` (`scene_lol.cpp:242-251`) does not read them. It reads a little-endian uint16 at image offset 4 and then takes four wall bytes per block from image offset 6, stepping by that length.

On all 29 levels, both editions, image bytes 0-3 are `20 00 20 00`: uint16 32, uint16 32. The image is `6 + 1024 * length`. For length 4 that is 4102 bytes, which is a 32 by 32 grid of 4-byte blocks. CONFIRMED as the values in the file. The reader ignores them, so calling them width and height is a reading of the data, not a line of code. `gui/saveload_rpg.cpp:49-60` reads the same length word and the same four wall bytes.

Level 24's length word is 9. That is the next note.
