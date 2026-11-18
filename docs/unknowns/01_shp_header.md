# SHP header, CD and LANDSoL

The retail shape header is 10 bytes. Both trees use it. The 2-byte prefix in `docs/closure_memo.md` is the demo alt-header flag, and neither tree here contains a demo disc.

Sources read: the CD `DATA` tree and the LANDSoL tree. PAK names below are the archive that held the file. A later PAK does not replace an earlier file of the same name.

## What the engine reads

CONFIRMED. `Screen_v2::getPtrToShape` (`engines/kyra/graphics/screen_v2.cpp:192-200`) reads a little-endian uint16 count, then a little-endian uint32 at `count_table + shape_index * 4 + 2`, and returns `table + that_uint32 + 2`.

CONFIRMED. `getShapeSize` (`screen_v2.cpp:228-231`) reads a little-endian uint16 at `shape + 6`.

CONFIRMED. The encoder in `Screen::encodeShape` (`engines/kyra/graphics/screen.cpp:2834-2859`) writes 10 bytes when `useAltShapeHeader` is clear, and 12 bytes when it is set. The 10 bytes are:

| Offset | Type | Field |
| --- | --- | --- |
| 0 | uint16 | flags. `drawShape` (`screen.cpp:1640-1641`) sets compact drawing when bit 0 is set. |
| 2 | uint8 | height |
| 3 | uint16 | width |
| 5 | uint8 | height again |
| 6 | uint16 | size used by `getShapeSize` |
| 8 | uint16 | uncompressed size |

CONFIRMED. With the alt flag set, `drawShape` (`screen.cpp:1637-1638`) skips 2 bytes before reading flags, and the encoder (`screen.cpp:2851-2852`) writes 2 bytes and then the same 10-byte record. `detection.h:51` describes that flag as "alternative shape header (uses 2 bytes more, those are unused though)".

CONFIRMED. The flag is the second bool in `GameFlags` (`detection.h:50-51`). `LOL_CD_FLAGS` and `LOL_FLOPPY_FLAGS` (`detection_tables.h:56` and `:58`) both pass false for it. `LOL_DEMO_FLAGS` (`detection_tables.h:63`) passes true. No demo disc is in either tree, so the demo's two extra bytes are UNCONFIRMED on data.

Monster palette copy starts at `shape + 10` (`engines/kyra/engine/sprites_lol.cpp:88-90`). That matches a 10-byte header. CONFIRMED.

Area files such as `FOREST1.SHP` are this table stored raw. Monster and UI files are a bitmap whose decompressed image is the same table. `Screen::loadBitmap` (`screen.cpp:3368-3392`) reads compression at file byte 2, image size as uint32 at file byte 4, palette size as uint16 at file byte 8, and the payload at `10 + palette_size`. Compression 4 is Frame4. CONFIRMED.

## Three shapes, CD

`FOREST1.SHP` in `FOREST1.PAK`, 77136 bytes, raw table, count 92. File bytes 0-15 are `5c 00 74 01 00 00 f9 07 00 00 0b 0e 00 00 48 14`.

| Shape | File offset of the 10 bytes | Bytes | flags, h, w, h2, size, uncomp |
| --- | --- | --- | --- |
| 0 | 374 | `01 00 2f 3e 00 2f 85 06 ce 0a` | 1, 47, 62, 47, 1669, 2766 |
| 46 | 24097 | `00 00 52 60 00 52 f6 0d b3 1d` | 0, 82, 96, 82, 3574, 7603 |
| 91 | 75504 | `01 00 32 44 00 32 60 06 b8 0b` | 1, 50, 68, 50, 1632, 3000 |

The stored uint32 for shape 0 is 372. `getPtrToShape` adds 2, which lands on file offset 374. Reading the 10-byte record two bytes later fails the same checks (height 1..200, height duplicated, width 1..320, flags at most 7). CONFIRMED. Same result for shapes 46 and 91.

`GUARD.SHP` in `L01.PAK`, 24909 bytes. File bytes 0-15 are `4b 61 04 00 c0 7a 00 00 00 00 a8 31 00 cc 00 00`: compression 4, image size 31424, palette size 0. The image begins `31 00 cc 00 00 00 73 08`, count 49. Header offsets below are in that image.

| Shape | Image offset | Bytes | flags, h, w, h2, size, uncomp |
| --- | --- | --- | --- |
| 0 | 206 | `05 00 60 38 00 60 a3 07 1e 0b` | 5, 96, 56, 96, 1955, 2846 |
| 24 | 29580 | `01 00 60 38 00 60 66 00 f5 00` | 1, 96, 56, 96, 102, 245 |
| 48 | 31297 | `01 00 60 38 00 60 7f 00 13 01` | 1, 96, 56, 96, 127, 275 |

`ITEMICN.SHP` in `STARTUP.PAK`, 22733 bytes. File bytes 0-5 are `cb 58 04 00 49 6e`: compression 4, image size 28233. Image begins `8a 00 2c 02`, count 138. `LoLEngine::loadItemIconShapes` (`engines/kyra/engine/lol.cpp:616-621`) loads this file as a bitmap and copies shapes with `makeShapeCopy`, which uses `getPtrToShape`. CONFIRMED.

| Shape | Image offset | Bytes | flags, h, w, h2, size, uncomp |
| --- | --- | --- | --- |
| 0 | 558 | `01 00 14 14 00 14 72 00 6e 00` | 1, 20, 20, 20, 114, 110 |
| 69 | 14137 | `01 00 14 14 00 14 52 01 77 01` | 1, 20, 20, 20, 338, 375 |
| 137 | 27929 | `01 00 14 14 00 14 30 01 3c 01` | 1, 20, 20, 20, 304, 316 |

## Three shapes, LANDSoL

`FOREST1.SHP` in `CHAPTER1.PAK` is byte-identical to the CD file, including the three headers above. CONFIRMED.

`GUARD.SHP` in `CHAPTER1.PAK`, 24987 bytes. File bytes 0-7 are `99 61 04 00 ef 7f 00 00`: compression 4, image size 32751. The image still begins `31 00 cc 00`, count 49. Shape 0 is the same 10 bytes at image offset 206. Shape 24 is the same 10 bytes at image offset 30122. Shape 48 is the same 10 bytes at image offset 32624. CONFIRMED.

`ITEMICN.SHP` in `GENERAL.PAK` is byte-identical to the CD file. CONFIRMED.

## Every shape

A shape counted as the 10-byte header when flags were at most 7, both height bytes matched, height was 1..200, width was 1..320, and the size at byte 6 fit in the table. The alt test was the same check two bytes later, and only when the first check failed.

CONFIRMED. CD: 89 `.SHP` names, 3492 shapes, 3492 pass at `stored + 2`, 0 pass only at `stored + 4`. LANDSoL, first copy of each name: 90 names, 3487 shapes, 3487 pass at `stored + 2`, 0 pass only at `stored + 4`.

The five-shape gap is two files. CD `GAMESHP.SHP` in `STARTUP.PAK` has count 89. LANDSoL `GAMESHP.SHP` in `GENERAL.PAK` has count 83. LANDSoL also has `DOOR.SHP` in `FINALE1.PAK`, count 1, which the CD tree does not have. 3492 - 6 + 1 = 3487. CONFIRMED.

LANDSoL stores a second copy of five names. Summing every `.SHP` member, including those copies, is 3601 shapes, and all 3601 pass the 10-byte check. The extra 114 are `FACE01.SHP` 28, `FACE05.SHP` 28, `FACE08.SHP` 28, `FACE09.SHP` 28 (each in `GENERAL.PAK` and again in `INTRO.PAK`), and `ITEMICN.SHP` in `INTRO.PAK` with count 2. CONFIRMED. The unique-name count and the every-member count are both 10-byte headers.

Flag values other than bit 0 are not fully specified here. `GUARD` shape 0 has flags 5, so bit 2 is set in that word. What bit 2 means is UNCONFIRMED.
