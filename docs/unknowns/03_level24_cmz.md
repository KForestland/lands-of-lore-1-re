# Q3. Level 24's extra five bytes per block

`LEVEL24.CMZ` stores 9 bytes per block. Every other level stores 4. The two routines in each edition's `MAIN.EXE` that walk the block records copy 4 bytes and step by the length word. The extra 5 are not copied. What they mean is still open.

## What the file holds

CONFIRMED. Both editions, `LEVEL24.CMZ` is 549 bytes and the two files are byte-identical. Decompressed image is 9222 bytes. Image bytes 0-5 are `20 00 20 00 09 00`: uint16 32, uint16 32, uint16 length 9. Payload is 1024 records of 9 bytes starting at image offset 6. Every other level's length word is 4 and the image is 4102 bytes. Same layout as round 1, rechecked on both trees.

The first four bytes of a record are the wall types, north, east, south, west. The last five are the tail. Nine tails occur:

| Tail | Blocks | Where it sits |
| --- | --- | --- |
| `01 01 01 01 01` | 759 | wall bytes are only `(2,2,1,1)` (384) or `(1,1,2,2)` (375) |
| `00 00 00 00 00` | 230 | wall bytes are `(0,0,0,0)` on every one of them |
| `04 00 a4 19 04` | 26 | block indexes 176, 232, 284, 302, 331, 337, 395, 443, 462, 511, 538, 566, 575, 659, 666, 685, 715, 724, 730, 739, 780, 824, 828, 847, 873, 877 |
| `04 00 ec 16 04` | 3 | blocks 610, 657, 746 |
| `04 00 ea 16 04` | 2 | blocks 272 and 273, walls all 57 |
| `3a 3a 3a 3a 3a` | 1 | block 427, walls all 58 |
| `38 38 38 38 38` | 1 | block 642, walls all 56 |
| `4d 4d 4d 4d 4d` | 1 | block 689, walls all 77 |
| `3f 3f 3f 3f 3f` | 1 | block 942, walls all 63 |

Reading bytes 2-3 of a `04 00` tail as a little-endian uint16 gives 6564, 5868, or 5866. None of those is a block index from 0 to 1023.

`LEVEL24.WLL` is 698 bytes, 58 records after the 2-byte header, area index 1 (`FOREST1`). It defines 49 wall-type ids, from 0 through 77 with gaps. Every wall byte in the 1024 records is one of those 49 ids. CONFIRMED. The tail is not standing in for a wall type missing from this level's WLL. Levels 2 and 3 are the levels whose CMZ uses types their own WLL does not define (Q11).

## Who reads the record

CONFIRMED for ScummVM. `LoLEngine::loadBlockProperties` (`engines/kyra/engine/scene_lol.cpp:246-251`) reads the uint16 at image offset 4 and copies `p[i * len + 0..3]` for `i` in 0..1023. The save and restore path does the same (`engines/kyra/gui/saveload_rpg.cpp:50-60` and `:74-84`). Neither function tests the level number.

CONFIRMED for the DOS executables. Each `MAIN.EXE` has two loops that do this and no third one was found.

CD `DATA/HARDRIVE/MAIN.EXE`, 356928 bytes:

- File `0x48540`: `mov ax, es:[bx+4]` (the length word). File `0x48549`: `push 4`. File `0x4855e`: `imul` that length by the block index. File `0x48567`: `add dx, 6`. File `0x48578`: `cmp si, 0x400`. The call between the pushes copies 4 bytes from image+6+index*length onto image+index*4.
- File `0x48764` through `0x487a0`: the same copy, with `push 4` at `0x4876d` and `add dx, 6` at `0x4878b`.

floppy `MAIN.EXE`, 373872 bytes:

- File `0x51c10`: `mov ax, es:[bx+4]`. File `0x51c19`: `push 4`. File `0x51c2e`: `imul` the length. File `0x51c37`: `add dx, 6`. File `0x51c48`: `cmp si, 0x400`.
- File `0x51e34` through `0x51e70`: the same copy, `push 4` at `0x51e3d`, `add dx, 6` at `0x51e5b`.

The format string those functions print is `level%d.cmz` (CD file `0x329f6`, floppy file `0x388da` and `0x38900`). One function writes `_LEVEL%d.TMP`. The other reads it back. Both still go back to `level%d.cmz` for the original four wall bytes.

After the copy, the floppy load function clears `0x2800` bytes (1024 times 10) at `ds:0xB6A3` (file `0x51e72`). The CD load function clears the same `0x2800` bytes at `ds:0x8203` (file `0x487a2`). That array is 10 bytes per block. The loops that follow write bytes 0-3 and byte 9 of each slot from the temp-file delta XOR-combined with the four wall bytes. Bytes 4-8 of the slot are left 0. The temp file's own 5-byte-per-block blob is `0x1400` bytes (1024 times 5): four XOR bytes plus slot byte 9. That is the live block record, not the CMZ tail.

A search of both executables for `add dx, 6` next to a compare against `0x400`, and for `mov ax, es:[bx+4]`, found no other stride loop. `LANDS.EXE` and `FINALE.EXE` do not contain `level%d.cmz`.

## What the level 24 scripts do with these blocks

CONFIRMED as a negative. CD `LEVEL24.INF` (9242 bytes) pushes some of the block indexes: 746 five times, 273 three times, 395 twice, 427 once, 715 once. CD `LEVEL24.INI` (888 bytes) pushes 232 once. The tail words 6564, 5868, and 5866 are not push immediates in either script. floppy `LEVEL24.INF` is 8840 bytes, not a copy of the CD script, while the CMZ files are byte-identical, so those three numbers are not offsets into the script file either.

`LEVEL24.ENG` has 39 strings and `LANDS.ENG` has 735. 6564 is outside both tables, so it is not a string id in those files.

## What was tried and did not name the tail

- Tail byte 0 is not the automap byte, the flags byte, or the special byte of wall 0. Against `LEVEL24.WLL` those match on 0, 0, and 230 blocks of 1024. The 230 are the open blocks, whose special byte is already 0.
- 28 blocks have a wall whose WLL special byte is not 0. Twenty-six of them carry `04 00 a4 19 04`. Seven other blocks carry a non-trivial tail while every side's special byte is 0 (blocks 272, 273, 610, 642, 657, 689, 942). Special-byte 1 does not define the tail.
- The four repeated-byte tails equal the wall type on all four sides and in the tail. The other tails do not.

## Other measurements

- The decompressed `LEVEL24.CMZ` image begins `20 00 20 00 09 00 00 00 00 00 00 00 00 00 00 02` (both editions). CONFIRMED.
- `LEVEL24.INI` in both editions names `FOREST1` and `LEVEL24.CMZ` (TEXT strings 1 and 3), and `LEVEL24.WLL` selects area 1 (FOREST1): a forest map stored with a longer block record. CONFIRMED.
- The 26 blocks with tail `04 00 a4 19 04` sit on wall types 46, 47, 51, 53, 54, 55, 57, 65 and 69, not on the plain `(1, 1, 2, 2)` corridors. CONFIRMED.
- Compressed CMZ sizes match between CD and floppy on levels 1-28. `LEVEL29.CMZ` is 765 bytes on CD and 767 on floppy; both decompress to 4102 bytes with length 4. CONFIRMED.

## What would settle it

A routine that reads image byte `6 + index * length + 4` (or further) and uses it. The two `MAIN.EXE` loops and the two ScummVM functions do not. A note from the original editor that assigned those bytes would also settle it. Until one of those turns up, the tail stays UNCONFIRMED.
