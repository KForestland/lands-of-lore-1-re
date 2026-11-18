# Level 24 CMZ, 9 bytes per block

Level 24 is the only map whose CMZ length word is 9. The other 28 levels use 4. ScummVM copies the first four bytes of each block and steps over the rest. What the extra five bytes mean, and why only this level was written that way, is UNCONFIRMED.

## The files

A CMZ is a compression-4 bitmap. `Screen::loadBitmap` (`engines/kyra/graphics/screen.cpp:3368-3392`) decompresses it. `loadBlockProperties` (`engines/kyra/engine/scene_lol.cpp:242-251`) then reads:

| Image offset | Type | Use |
| --- | --- | --- |
| 0 | uint16 | 32 on every level. Not read. |
| 2 | uint16 | 32 on every level. Not read. |
| 4 | uint16 | bytes per block |
| 6 | 1024 records | `walls[0..3]` are the first four bytes. The step is the length at offset 4. |

CONFIRMED. CD and LANDSoL, levels 1-23 and 25-29: length 4, decompressed size 4102, and `6 + 1024 * 4 = 4102`. Level 24: length 9, decompressed size 9222, and `6 + 1024 * 9 = 9222`.

CD `LEVEL24.CMZ` in `L24.PAK` is 549 bytes. LANDSoL `LEVEL24.CMZ` in `CHAPTER6.PAK` is 549 bytes. The two files are byte-identical. The decompressed image begins `20 00 20 00 09 00 00 00 00 00 00 00 00 00 00 02`. CONFIRMED.

There is no level-number test around this read. The same loop is used for every level (`scene_lol.cpp:249-251`). The save path reads the same four wall bytes (`engines/kyra/gui/saveload_rpg.cpp:49-60`). Those two functions are the readers found for this file. CONFIRMED that they do not use bytes 4 through 8 of a block. What those bytes mean is UNCONFIRMED.

`LEVEL24.INI` in both editions names `FOREST1` and `LEVEL24.CMZ` (TEXT strings 1 and 3). `LEVEL24.WLL` selects area index 1, FOREST1 (`02_wll_header.md`). So this is a forest map stored with a longer block record. Why the record is longer is UNCONFIRMED: nothing in the reader treats level 24 as a special case.

CD and LANDSoL compressed sizes match on levels 1-28. `LEVEL29.CMZ` is 765 bytes on CD and 767 bytes on LANDSoL. Both still decompress to 4102 bytes with length 4. CONFIRMED.

## The extra five bytes

Counted on the shared level 24 image, 1024 blocks. The five bytes after the four wall bytes take nine patterns. CONFIRMED.

| Count | Five bytes | Wall bytes beside them |
| --- | --- | --- |
| 759 | `01 01 01 01 01` | `(2, 2, 1, 1)` on 384 blocks, `(1, 1, 2, 2)` on 375 blocks |
| 230 | `00 00 00 00 00` | `(0, 0, 0, 0)` on all 230 |
| 26 | `04 00 a4 19 04` | mixed wall types, listed below |
| 3 | `04 00 ec 16 04` | blocks 610, 657, 746 |
| 2 | `04 00 ea 16 04` | blocks 272 and 273, walls `(57, 57, 57, 57)` |
| 1 | `3a 3a 3a 3a 3a` | block 427 `(x=11, y=13)`, walls all 58 |
| 1 | `38 38 38 38 38` | block 642 `(x=2, y=20)`, walls all 56 |
| 1 | `4d 4d 4d 4d 4d` | block 689 `(x=17, y=21)`, walls all 77 |
| 1 | `3f 3f 3f 3f 3f` | block 942 `(x=14, y=29)`, walls all 63 |

Block index `i` is `x = i % 32`, `y = i // 32`. The four repeated-byte blocks repeat that same byte through all nine record bytes, walls included. CONFIRMED.

The 26 blocks with `04 00 a4 19 04` sit on wall types 46, 47, 51, 53, 54, 55, 57, 65, and 69, not on the plain `(1, 1, 2, 2)` corridors. Their indexes are 176, 232, 284, 302, 331, 337, 395, 443, 462, 511, 538, 566, 575, 659, 666, 685, 715, 724, 730, 739, 780, 824, 828, 847, 873, 877. CONFIRMED as the pairing of wall bytes and tail bytes. No field names are given to the five bytes: no code reads them.

Reading tail bytes 2 and 3 as a little-endian uint16 gives 6564, 5868, and 5866. None of those is a block index in 0..1023. That arithmetic is CONFIRMED. It does not identify the field. UNCONFIRMED.
