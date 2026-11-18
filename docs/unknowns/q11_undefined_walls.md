# Q11. Wall types the level file never defines

Levels 2, 3 and 21 name wall types in the map that their own wall file does not define. The wall-property tables are not cleared when a level loads, so those types keep whatever row was written last. The level scripts do not assign these type numbers.

## The missing types

CONFIRMED. Both editions. The map and the wall file of each of these three levels are byte-identical across the two editions. A type is missing when a map wall byte is not the wall-type id of any 12-byte record in that level's wall file. A repeated record for the same id counts as defined: the later record replaces the earlier one (`loadLevelWallData` writes by id, `engines/kyra/engine/scene_lol.cpp:153-172`).

Level 2. Wall file 494 bytes, area index 1, 41 records, 39 distinct ids. The map uses eight ids that are not among them, on 18 blocks:

| Block | x, y | Walls, north east south west | Missing ids |
| --- | --- | --- | --- |
| 520 | 8, 16 | 1, 1, 54, 2 | 54 |
| 526 | 14, 16 | 60, 60, 60, 60 | 60 |
| 586 | 10, 18 | 46, 1, 2, 2 | 46 |
| 641 | 1, 20 | 55, 2, 1, 1 | 55 |
| 642 | 2, 20 | 1, 1, 54, 2 | 54 |
| 648 | 8, 20 | 46, 1, 2, 2 | 46 |
| 688 | 16, 21 | 56, 56, 56, 56 | 56 |
| 712 | 8, 22 | 57, 57, 57, 57 | 57 |
| 713 | 9, 22 | 2, 55, 1, 1 | 55 |
| 718 | 14, 22 | 1, 1, 2, 54 | 54 |
| 741 | 5, 23 | 53, 1, 2, 2 | 53 |
| 748 | 12, 23 | 2, 53, 1, 1 | 53 |
| 771 | 3, 24 | 2, 2, 1, 46 | 46 |
| 804 | 4, 25 | 59, 59, 59, 59 | 59 |
| 810 | 10, 25 | 55, 2, 1, 1 | 55 |
| 839 | 7, 26 | 53, 2, 1, 1 | 53 |
| 849 | 17, 26 | 55, 2, 1, 1 | 55 |
| 867 | 3, 27 | 53, 1, 2, 2 | 53 |

Face counts: 46 three times, 53 four, 54 three, 55 four, 56 four, 57 four, 59 four, 60 four.

Level 3. Wall file 530 bytes, area index 1, 44 records, 42 distinct ids. Five blocks, each with the same missing type on all four sides:

| Block | x, y | Type on all four sides |
| --- | --- | --- |
| 13 | 13, 0 | 66 |
| 96 | 0, 3 | 63 |
| 106 | 10, 3 | 58 |
| 301 | 13, 9 | 67 |
| 328 | 8, 10 | 61 |

Level 21. Wall file 794 bytes, area index 7, 66 records, 64 distinct ids. One block: 245 (x 21, y 7), walls 42, 0, 42, 0. Type 42 is the only missing id. Two faces.

Level 24's wall file defines every wall byte in its map, including 56, 57, 58 and 63. The note that types 46 and 53-57 are undefined belongs to level 2, not to level 24. Level 1 has no missing types.

LANDSoL level 29 has one extra undefined face that the CD map does not. Block 876 (x 12, y 27), east wall, type 57. The wall files are byte-identical (1094 bytes, area 11). The maps are not (CD 765 bytes, LANDSoL 767). CONFIRMED as a difference between the editions. It is outside the three levels in the question.

## The property row is left in place

CONFIRMED for ScummVM. The four property arrays are allocated once, filled with 0 (`engines/kyra/engine/kyra_rpg.cpp:190-193`). `loadLevelWallData` writes one row per record and does not clear the arrays first (`scene_lol.cpp:153-172`). A type the new file does not mention keeps the previous level's row, or 0 if no level has written it.

CONFIRMED for the LANDSoL loader's body. `MAIN.EXE` (373872 bytes) reads the 12-byte records at file `0x50b33-0x50c04`. That span contains no `rep stos`. The CD `MAIN.EXE` (356928 bytes) has the same `level%00d.wll` format string. Its loader body was not opened. The wall files of these levels are byte-identical, so the rows the CD program would read are the same bytes.

The row is not the same number on every level that defines the id. Worked example, type 60, the four walls of level 2 block 526. Level 2 has no record. Level 1 does. Its 12 bytes are `3c 00 06 00 03 00 04 00 06 00 0d 00`: type 60, VMP page 6, shape 3, flags 4, special 6, automap 0x0D. If level 1 was the last level that wrote type 60, those are the bytes the drawer still holds. No later file in a level-1-then-level-2 load replaces them.

Who already has a row (CD wall files; LANDSoL matches on levels 1, 2 and 24):

| Type | Defined on level 1 | Defined on level 2 | Also defined on |
| --- | --- | --- | --- |
| 46 | no | no | 3, 7, 8, 10, 12-15, 17, 18, 20-29 |
| 53 | yes | no | 3-5, 7-17, 20-24, 26-29 |
| 54 | yes | no | 3, 4, 6, 7, 10-18, 20, 22-24, 26-29 |
| 55 | yes | no | same levels as 54 |
| 56 | no | no | 3, 4, 6, 11-15, 18-20, 22-24, 26-29 |
| 57 | yes | no | 3, 4, 6, 11-15, 18, 20-24, 26-28 |
| 58 | yes | yes, different bytes | level 3 does not define it |
| 59 | yes | no | level 2 does not |
| 60 | yes | no | not on level 2 or 24 |
| 61 | yes | yes, different bytes | level 3 does not |
| 63 | yes | yes, different bytes | level 3 does not |
| 66 | yes | yes, different bytes | level 3 does not |
| 67 | yes | yes, different bytes | level 3 does not |
| 42 | no | no | 4-9, 12, 14-16, 18, 20, 22, 23, 26-29. Not level 21 |

Level 1's type 58 is `3a 00 05 00 00 00 04 00 07 00 ff ff`. Level 2's type 58 is `3a 00 00 00 03 00 00 00 06 00 3f 00`. Same id, different shape and flags. A level 3 wall of type 58 therefore looks like level 2 if level 2 was loaded more recently, and like level 1 if only level 1 was. Which order a game actually loads is UNCONFIRMED.

Types 46 and 56 are in neither level 1 nor level 2. A path that has loaded only those two has not written a row for them. Level 3 does define both. Levels 18 and 20 share area index 7 with level 21 and both define type 42.

Level 2 stores two records each for types 1 and 2. Record index 1 is type 1 with shape 0 (`01 00 01 00 00 00 00 00 07 00 ff ff`). Record index 27 is type 1 with shape 8 (`01 00 01 00 08 00 00 00 07 00 ff ff`). The later record is the one left in the table. The same pair exists for type 2, shapes 0 then 9. CONFIRMED, both editions, the files are identical.

## Scripts do not assign the missing ids

CONFIRMED for the immediates in the script. System call 0 is `olol_setWallType` (`engines/kyra/script/script_lol.cpp:95-102`, opcode 0 at `script_lol.cpp:2689`). It calls `setWallType` (`scene_lol.cpp:1240-1254`), which writes the wall byte and does not write a property row. Arguments are last-push-first: block, wall, new type.

Level 2 and level 3 init scripts, and level 3's map script, contain no system-call-0 word. Level 2's map script (CD 9794 bytes) has one, at file offset 4960: push 63, push 2, push 13, system call 0. LANDSoL's copy (9628 bytes) has the same four words at file offset 5012. A walk from every function entry, following jumps, does not reach it, and no jump operand in the file points at it. The next function entry begins at data word 1287, after this word. Type 63 is defined in level 2's wall file, so the call would not paint a missing id even if something did reach it.

Level 21's map script has 40 words that are system call 0 (34 of them reached from the function table, 6 not). The init script has 10, none of them reached by that walk. The type immediate on those words is never 42. The reached calls recover the immediates 0, 1, 28, 29, 32, 33, 34, 35, 36, 38, 40, 57, 71, 77, 79, -1 and -2. Four reached calls pass the type in a register, so the number is not in the instruction. The six unreached map-script sites push types 0, 67, 68 or 74. The ten init-script sites push -1, 0 or 28. None of those is 42, and 67, 68 and 74 are ids level 21 does define.

## What would settle the picture on screen

Which level was loaded last, on a real path into level 2, level 3 or level 21. The missing ids, the fact that the loader does not clear the tables, and the script immediates are measured. The CD loader body, and the four level-21 calls whose type sits in a register, are the two checks still open. Until a play trace names the previous level, the row a missing type shows stays UNCONFIRMED.
