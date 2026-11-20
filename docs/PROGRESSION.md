# Progression

Made by `tools/lol1_progression.py` from each level's `LEVEL<n>.INF` and `LEVEL<n>.INI` (CD edition). One row is one static call. `loadNewLevel` (function 0x3C) is the level change: level, block, facing. Door calls are `triggerDoorSwitch` (0x31), `setDoorState` (0x33) and `blockDoor` (0x86). The word column is the DATA word of that call. The entries column lists every script entry whose call graph reaches the call, through jumps, both arms of `ifNotJmp` (only the arm taken when the tested value is a constant argument), and calls. A return ends that path, so a later subroutine is not credited to the entry. The conditions column lists the `ifNotJmp` tests still open on a path that reaches the call, outermost first. Paths that differ only in the arm of one test are merged, so a test whose two arms both lead to the call is not listed. `flag 41 == 0` means that arm of the compare. `hand item type` is `getItemPara` selector 4 on the item in hand (its type index) and `hand item shape` is selector 8 (its shape index), CONFIRMED by the selector jump table of the CD handler (`MAIN.EXE+0x13888`, table at `+0x139B6`). `finds item` is argument 2 of `findInventoryItem`. `item` is argument 1 of `checkPartyForItemType`. `computed` is a test that is not a flag, an item, a party member, credits, a hand-item type or shape, or facing. `none` means no such test is open. An entry cell of `none` means the instruction is in the script and no entry reaches it. A call in a shared subroutine is one row. Where callers pass different constants, the argument cells list each combination in the same order, separated by ` or `. A column that is the same in every combination is written once. Item and flag numbers are the script arguments.

71 level changes and 136 door calls across levels 1 to 29.

## Level to level

| From | To | Block | Facing | Word | Entries | Event | Conditions |
|---:|---|---|---|---:|---|---|---|
| 1 | 2 | 106 | 2 | 0x130C | 621 | party steps in, wall clicked | computed; facing == 2 |
| 2 | 1 | 589 | 0 | 0x01F0 | 74 | party steps in, wall clicked | computed; (facing == 0) and (flag 41 == 0); flag 67 != 1 or computed; flag 41 == 0; flag 67 != 1 |
| 2 | 3 | 526 | 2 | 0x0729 | 392 | wall clicked | computed; flag 41 == 0; hand item shape == 40 |
| 2 | 6 | 449 | 0 | 0x08E9 | 13 | party steps in, party arrives (second path), wall clicked, item put down | computed |
| 2 | 10 | 713 | 0 | 0x0AD6 | 300, 301 | 300: party steps in, party arrives (second path), party leaves, wall clicked, bit 0x4000; 301: party steps in, wall clicked | computed; facing == 1; flag 67 == 1 or flag 67 == 1; computed |
| 2 | 5 | 260 | 3 | 0x0CFB | 99 | party steps in, bit 0x4000 | facing == 3; flag 35 != 1; computed |
| 2 | 5 | 260 | 3 | 0x0DA9 | 96 | party steps in, party arrives (second path), wall clicked, item put down | computed; facing == 3 |
| 3 | 2 | 328 | 0 | 0x029A | 494 | party steps in, wall clicked | computed; ((flag 27 != 0) or (flag 29 != 0)) or (flag 192 != 0); flag 29 != 0; party member 2 != 1; credits >= 100 or computed; ((flag 27 != 0) or (flag 29 != 0)) or (flag 192 != 0); flag 29 != 0; party member 2 == 1; credits >= 200 or computed; facing == 0; ((flag 27 != 0) or (flag 29 != 0)) or (flag 192 != 0); flag 29 != 0; party member 2 != 1; credits >= 100 or computed; facing == 0; ((flag 27 != 0) or (flag 29 != 0)) or (flag 192 != 0); flag 29 != 0; party member 2 == 1; credits >= 200 |
| 3 | 4 | 167 | 0 | 0x0C65 | 772 | party steps in, wall clicked | computed; facing == 0 |
| 4 | 3 | 804 | 2 | 0x02D3 | 199 | party steps in, party arrives (second path), item put down | computed; facing == 2 |
| 5 | 2 | 97 | 1 | 0x02FE | 261 | party steps in, party arrives (second path), item put down | (computed) or (facing == 1); computed |
| 6 | 7 | 258 or 86 | 0 | 0x003F | 118, 258 | 118: party steps in, party arrives (second path), item put down; 258: party steps in, party arrives (second path), wall clicked, item put down | computed; facing == 0 |
| 6 | 7 | 162 or 163 or 194 or 195 or 225 | ? | 0x008B | 161, 162, 163, 194, 195, 225, 256, 258, 289, 455 | 161: party arrives (second path); 162: party arrives (second path), item put down; 163: party arrives (second path), item put down; 194: party arrives (second path), item put down; 195: party arrives (second path), item put down; 225: party arrives (second path), item put down; 256: wall clicked; 258: party steps in, party arrives (second path), wall clicked, item put down; 289: wall clicked; 455: party arrives (second path), item put down | computed |
| 6 | 7 | 162 or 163 or 194 or 195 or 225 or 455 | ? | 0x0132 | 162, 163, 194, 195, 225, 455 | party arrives (second path), item put down | computed |
| 6 | 2 | 45 | 2 | 0x0314 | 481 | party steps in, party arrives (second path), item put down | computed; facing == 2 |
| 7 | 6 or 6 or 8 or 8 or 8 | 150 or 322 or 156 or 208 or 527 | 2 or 2 or 2 or 1 or 2 | 0x0060 | 118, 124, 207, 290, 495 | party steps in, party arrives (second path), item put down | computed; facing == 1 or computed; facing == 2 |
| 7 | 8 | 367 or 430 or 431 or 432 | ? | 0x01D3 | 366, 430, 431, 433 | 366: wall clicked, thrown item hits; 430: party arrives (second path), item put down; 431: party arrives (second path), item put down; 433: wall clicked, thrown item hits | computed |
| 7 | 8 | 367 or 430 or 431 or 432 | ? | 0x021D | 367, 430, 431, 432 | party arrives (second path), item put down | computed |
| 8 | 7 or 7 or 7 or 9 or 9 | 206 or 463 or 92 or 217 or 477 | 3 or 0 or 0 or 3 or 0 | 0x045B | 124, 207, 218, 495, 509 | party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 3 |
| 9 | 8 | 219 or 541 | 1 or 2 | 0x00A9 | 218, 509 | party steps in, party arrives (second path), item put down | computed; facing == 1 or computed; facing == 2 |
| 10 | 11 or 12 | 641 or 412 | 0 or 1 | 0x04EC | 129, 703 | 129: party steps in, party arrives (second path), item put down; 703: party steps in, party arrives (second path), wall clicked | computed; facing == 0 or computed; facing == 1 |
| 11 | 10 or 17 | 161 or 705 | 2 or 1 | 0x0192 | 673, 735 | party steps in, party arrives (second path), item put down | computed; facing == 1 or computed; facing == 2 |
| 11 | 11 | 109 | 3 | 0x1860 | 45 | wall clicked | flag 84 == 0; computed; flag 282 == 0 |
| 12 | 10 or 13 or 17 | 702 or 111 or 760 | 3 or 0 or 0 | 0x06CB | 92, 175, 411 | party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 3 |
| 13 | 14 | 442 or 444 or 483 | ? | 0x0070 | 313, 349, 356 | wall clicked | computed |
| 13 | 12 or 14 | 246 or 332 | ? | 0x009F | 116 | party steps in, party arrives (second path), item put down | computed |
| 13 | 12 or 14 | 207 or 323 | 2 or 0 | 0x0104 | 143, 227 | party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 2 |
| 13 | 14 | 180 or 442 or 444 or 483 | ? | 0x018C | 52, 314, 316, 355 | party arrives (second path), item put down | computed |
| 14 | 15 | 324 or 355 | ? | 0x0064 | 419 | party arrives (second path), party leaves (second path), item put down, item taken | computed |
| 14 | 12 | 246 | ? | 0x03A5 | 413 | party steps in, party arrives (second path), item put down | computed |
| 14 | 13 or 15 | 259 or 262 | 2 or 3 | 0x040A | 355, 359 | 355: party steps in, party arrives (second path), item put down; 359: party steps in, party arrives (second path), wall clicked, item put down | computed; facing == 2 or computed; facing == 3 |
| 14 | 15 | 324 or 355 or 53 or 54 | ? | 0x0439 | 149, 181, 182, 420, 451 | 149: wall clicked; 181: party arrives (second path), item put down; 182: party arrives (second path), item put down; 420: party arrives (second path), item put down; 451: party arrives (second path), item put down | computed |
| 15 | 14 or 16 | 360 or 292 | 1 or 3 | 0x04C0 | 263, 328 | party steps in, party arrives (second path), item put down | computed; facing == 1 or computed; facing == 3 |
| 15 | 12 | 246 | ? | 0x04F5 | 52 | party steps in, party arrives (second path), item put down | computed |
| 16 | 12 or 14 | 246 or 332 | ? | 0x0067 | 174, 238 | party steps in, party arrives (second path), item put down | computed |
| 16 | 15 | 329 | 1 | 0x00CC | 293 | party steps in, party arrives (second path), item put down | computed; facing == 1 |
| 17 | 11 or 12 or 24 | 734 or 124 or 910 | 3 or 2 or 0 | 0x01B0 | 78, 704, 792 | 78: party steps in, party arrives (second path), item put down; 704: party steps in, party arrives (second path); 792: party steps in, party arrives (second path), wall clicked | computed; facing == 0 or computed; facing == 2 or computed; facing == 3 |
| 18 | 19 or 20 or 20 or 24 | 198 or 329 or 335 or 689 | 2 or 3 or 1 or 2 | 0x017B | 330, 334, 449, 620 | 330: party steps in, party arrives (second path), item put down; 334: party steps in, party arrives (second path), item put down; 449: party steps in, party arrives (second path), item put down; 620: party steps in, party arrives (second path), item put down, fireball passes | computed; facing == 1 or computed; facing == 2 or computed; facing == 3 |
| 19 | 18 | 417 | 0 | 0x0120 | 166 | party steps in, party arrives (second path), item put down | computed; facing == 0 |
| 19 | ? | ? | ? | 0x014C | none | none | none |
| 20 | 18 | 401 or 495 | ? | 0x0040 | 397, 559 | wall clicked | computed |
| 20 | 18 or 18 or 21 | 331 or 333 or 586 | 1 or 3 or 1 | 0x00C2 | 330, 334, 584 | party steps in, party arrives (second path), item put down | computed; facing == 1 or computed; facing == 3 |
| 20 | 18 | 401 or 430 or 431 or 433 or 465 or 495 | ? | 0x0136 | 401, 430, 431, 433, 465, 495 | party arrives (second path), item put down | computed |
| 21 | 20 | 583 | 3 | 0x00F9 | 585 | party steps in, party arrives (second path), item put down | computed; facing == 3 |
| 21 | 20 | 199 | ? | 0x092D | 199 | party arrives (second path), item put down | computed |
| 22 | 23 | 977 | 0 | 0x02EB | 27 | party steps in, party arrives (second path), item put down | computed; facing == 0 |
| 22 | 24 | 674 | 2 | 0x0949 | 1003 | party steps in, wall clicked | facing == 2 |
| 23 | 25 | 674 or 706 or 736 or 738 or 768 | ? | 0x0061 | 705, 739, 767, 772 | wall clicked | computed |
| 23 | 22 or 25 | 59 or 293 | 2 or 0 | 0x00A3 | 325, 1009 | party steps in, party arrives (second path), item put down | computed; facing == 2 |
| 23 | 26 | 211 or 910 | ? | 0x00CC | 792, 920 | party arrives (second path), item put down | computed |
| 23 | 25 | 227 or 291 or 674 or 706 or 736 or 738 or 768 or 769 | ? | 0x04FF | 227, 291, 674, 706, 736, 738, 768, 769 | 227: party arrives (second path), item put down; 291: party arrives (second path), item put down; 674: party arrives (second path); 706: party arrives (second path); 736: party arrives (second path); 738: party arrives (second path); 768: party arrives (second path); 769: party arrives (second path) | computed |
| 23 | ? | ? | ? | 0x051D | none | none | none |
| 24 | 17 or 18 | 110 or 588 | 2 or 0 | 0x0109 | 657, 942 | 657: party steps in, party arrives (second path), wall clicked; 942: party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 2 |
| 24 | 22 | 971 | 0 | 0x0699 | 642 | party steps in, party arrives (second path), item put down | computed |
| 24 | 26 | 427 | 2 | 0x0718 | 427 | party arrives (second path), wall clicked, item put down, fireball passes, thrown item hits | computed; facing == 2 |
| 25 | 23 | 801 | ? | 0x0026 | 771 | party steps in, party arrives (second path), item put down | computed |
| 25 | 23 | 293 | 0 | 0x0068 | 325 | party steps in, party arrives (second path), item put down | computed; facing == 2 |
| 26 | 24 or 27 | 395 or 437 | 0 | 0x0614 | 254, 469 | party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 1 |
| 26 | 23 | 857 | ? | 0x1132 | 734 | party arrives (second path), item put down | computed |
| 27 | 26 | 104 or 742 or 746 or 810 or 816 or 818 or 840 | ? | 0x0340 | 71, 72, 678, 682, 786, 806, 816, 842, 850 | 71: wall clicked; 72: party arrives (second path); 678: party arrives (second path), party leaves (second path), item put down, item taken; 682: party arrives (second path), party leaves (second path), item put down, item taken; 786: wall clicked; 806: party arrives (second path), party leaves (second path), item put down, item taken; 816: party arrives (second path), item put down; 842: party arrives (second path), party leaves (second path), item put down, item taken; 850: wall clicked | computed |
| 27 | 26 | 104 or 677 or 680 or 681 or 711 or 713 or 715 or 741 or 742 or 746 or 776 or 805 or 807 or 809 or 810 or 811 or 816 or 818 or 840 | ? | 0x03C9 | 104, 677, 680, 681, 711, 713, 715, 741, 742, 746, 776, 805, 807, 809, 810, 811, 816, 818, 840 | party arrives (second path), item put down | computed |
| 27 | ? | ? | ? | 0x0418 | none | none | none |
| 27 | 26 | 503 | ? | 0x0469 | 650, 683 | party steps in, party arrives (second path), item put down | computed |
| 27 | 26 or 28 | 501 or 936 | 2 | 0x04CA | 469, 936 | party steps in, party arrives (second path), item put down | computed; facing == 2 |
| 28 | 26 or 27 or 27 or 27 | 517 or 169 or 618 or 649 | ? | 0x03B3 | 171, 202, 549, 650, 652 | 171: party arrives (second path); 202: wall clicked; 549: wall clicked; 650: item put down, item taken; 652: party arrives (second path), party leaves (second path), item put down, item taken | computed |
| 28 | 27 | 169 or 618 | ? | 0x03DC | 169, 618 | party arrives (second path), item put down | computed |
| 28 | 26 | 517 | ? | 0x0413 | 517 | party arrives (second path), item put down | computed |
| 28 | 27 or 29 | 904 or 721 | 0 or 2 | 0x045E | 657, 904 | party steps in, party arrives (second path), item put down | computed; facing == 0 or computed; facing == 2 |
| 29 | ? | ? | ? | 0x02F6 | none | none | none |
| 29 | 28 | 873 or 878 or 889 | ? | 0x031F | 873, 878, 889 | party arrives (second path), item put down | computed |
| 29 | 28 | 625 | 0 | 0x036A | 689 | party steps in, party arrives (second path), item put down | computed; facing == 0 |

## Door calls

| Level | Call | Block | Argument | Word | Entries | Event | Conditions |
|---:|---|---|---|---:|---|---|---|
| 1 | door switch | 361 | 1 | 0x026D | 394 | wall clicked | computed; hand item type == 185 |
| 6 | door switch | 165 | 1 | 0x04CC | 132 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 6 | door switch | 165 | -1 | 0x04E6 | 132 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 7 | door switch | 293 | 0 | 0x084E | 261 | wall clicked | none |
| 12 | door switch | 295 | 1 | 0x0948 | 296 | wall clicked | computed; (hand item type == -1) or (hand item type == 245); hand item type != 245 or computed; (hand item type == -1) or (hand item type == 245); hand item type == 245 |
| 12 | block door | 1 | - | 0x09FB | 340 | wall clicked | computed |
| 12 | block door | 1 | - | 0x0A0A | 371 | wall clicked | computed |
| 13 | door switch | 323 or 49 | 1 | 0x013E | 81, 324 | wall clicked | computed; hand item type == 173 or computed; hand item type == 174 |
| 13 | door state | 116 | 0 | 0x03FF | 83 | wall clicked | computed |
| 13 | door state | 116 | 1 | 0x0413 | 83 | wall clicked | computed |
| 13 | door state | 116 | 0 | 0x0426 | 83 | wall clicked | computed |
| 13 | door state | 116 | 1 | 0x043A | 83 | wall clicked | computed |
| 14 | door switch | 37 | -1 | 0x05B8 | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; flag 296 == 0 |
| 14 | door switch | 47 | -1 | 0x05BC | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; flag 296 == 0 |
| 14 | door switch | 37 | -1 | 0x05CE | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; computed |
| 14 | door switch | 37 | 1 | 0x05E1 | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; computed |
| 14 | door switch | 47 | -1 | 0x05F3 | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; flag 296 == 0; computed |
| 14 | door switch | 47 | 1 | 0x05F8 | 10, 42 | 10: wall clicked; 42: party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bit 0x4000 | flag 295 == 1; flag 296 == 0; computed |
| 14 | door state | 413 | 1 | 0x0622 | 379, 411 | 379: wall clicked; 411: party arrives (second path), party leaves (second path), item put down, item taken | computed |
| 14 | door state | 413 | 0 | 0x0645 | 379, 411 | 379: wall clicked; 411: party arrives (second path), party leaves (second path), item put down, item taken | computed |
| 14 | door switch | 291 | 1 | 0x07E5 | 292 | wall clicked | facing == 2; computed; (hand item type == 177) or (hand item type == 245); hand item type != 245 |
| 14 | door switch | 246 | -1 | 0x0A01 | 248 | party arrives (second path), party leaves (second path), item put down, item taken | flag 286 == 0 |
| 14 | door switch | 246 | 1 | 0x0A62 | 445 | item taken | computed |
| 14 | door switch | 47 | -1 | 0x0A7A | 47 | party leaves (second path) | computed |
| 14 | door switch | 37 | -1 | 0x0BF4 | 6 | wall clicked | computed |
| 14 | door switch | 47 | -1 | 0x0C10 | 49 | wall clicked, thrown item hits | computed; (flag 297 == 0) and (computed) |
| 14 | door switch | 47 | -1 | 0x0C3F | 49 | wall clicked, thrown item hits | computed |
| 15 | door switch | 518 | 1 | 0x00E4 | 431 | party steps in | flag 217 != 1; facing == 2; flag 216 == 1; computed |
| 15 | door switch | 535 | 1 | 0x0168 | 431 | party steps in | flag 217 != 1; facing == 2; flag 216 == 1; computed |
| 15 | door switch | 911 | 1 | 0x01E4 | 431 | party steps in | flag 217 != 1; facing == 2; flag 216 == 1; computed |
| 15 | door switch | 367 | 1 | 0x0260 | 847 | party steps in | flag 217 != 1; (computed) or (facing == 0); flag 216 == 1 |
| 15 | door switch | 367 | 1 | 0x02E4 | 516 | party steps in | flag 217 != 1; (computed) or (facing == 3); flag 216 == 1 |
| 15 | door switch | 367 | 1 | 0x0368 | 537 | party steps in | flag 217 != 1; (computed) or (facing == 1); flag 216 == 1 |
| 15 | door switch | 367 | -1 | 0x07E8 | 368 | wall clicked | computed |
| 15 | door switch | 367 | 1 | 0x080F | 368 | wall clicked | computed or computed; hand item type == 224 |
| 15 | door switch | 425 | 1 | 0x09D4 | 424 | wall clicked | computed; hand item type == 245 |
| 15 | door switch | 425 | -1 | 0x09FB | 393 | party arrives (second path) | flag 549 == 0 |
| 15 | door switch | 425 | 1 | 0x0A13 | 330 | party arrives (second path) | flag 550 == 0 |
| 15 | door state | 52 | 1 | 0x00EB | INI 0 | level load | none |
| 16 | door switch | 359 | 1 | 0x01FE | 358, 360 | wall clicked | (computed) and (flag 220 != 1); hand item type != 245; hand item type == 209; (flag 220 != 0) and (flag 221 != 0) or (computed) and (flag 221 != 1); hand item type != 245; hand item type == 210; (flag 220 != 0) and (flag 221 != 0) |
| 16 | door state | 259 | 0 | 0x02D1 | 260 | wall clicked | computed |
| 16 | door state | 259 | 1 | 0x02DD | 260 | wall clicked | computed |
| 16 | door switch | 205 | 1 | 0x056E | 236 | wall clicked | computed; hand item type != 245; hand item type == 176 |
| 16 | door state | 174 | 1 | 0x00EB | INI 0 | level load | none |
| 16 | door state | 207 | 1 | 0x00F0 | INI 0 | level load | none |
| 16 | door state | 238 | 1 | 0x00F5 | INI 0 | level load | none |
| 16 | door state | 141 | 1 | 0x00FA | INI 0 | level load | none |
| 18 | door switch | 136 or 205 or 385 or 421 or 485 | 1 | 0x045E | 137, 206, 386, 389, 518 | wall clicked | computed; (hand item type == -1) or (hand item type == 245); hand item type != 245 or computed; (hand item type == -1) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 184) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 192) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 192) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 193) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 193) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 197) or (hand item type == 245); hand item type != 245 |
| 18 | door switch | 429 | -1 | 0x059F | 397 | wall clicked | facing != 1; computed |
| 18 | door switch | 429 | 1 | 0x05B1 | 397 | wall clicked | facing != 1; computed |
| 18 | door switch | 108 | 1 | 0x0666 | 140 | wall clicked | computed |
| 18 | door switch | 108 | -1 | 0x0671 | 140 | wall clicked | computed |
| 18 | door switch | 337 | 1 | 0x0699 | 336 | wall clicked | computed |
| 18 | door switch | 337 | -1 | 0x069F | 336 | wall clicked | computed |
| 18 | door switch | 526 | 1 | 0x06B3 | 559 | wall clicked | computed |
| 18 | door switch | 526 | -1 | 0x06B9 | 559 | wall clicked | computed |
| 19 | door switch | 138 | 1 | 0x01F3 | 137 | wall clicked | computed; (hand item type == 194) or (hand item type == 245); hand item type != 245 |
| 20 | door switch | 423 or 493 or 582 | 1 | 0x01DA | 391, 461, 526, 550 | wall clicked | computed; (hand item type == -1) or (hand item type == 245); hand item type != 245 or computed; (hand item type == -1) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 195) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 196) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 197) or (hand item type == 245); hand item type != 245 |
| 20 | door switch | 493 | -1 | 0x07D7 | 494 | party arrives (second path) | computed |
| 21 | door switch | 523 or 70 or 76 | 1 | 0x019E | 103, 107, 524 | wall clicked | computed; (hand item type == -1) or (hand item type == 245); hand item type != 245 or computed; (hand item type == -1) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 195) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 196) or (hand item type == 245); hand item type != 245 |
| 21 | door switch | 296 or 424 | -1 | 0x0585 | 263, 455 | wall clicked | computed |
| 21 | door switch | 296 or 424 | 1 | 0x0595 | 263, 455 | wall clicked | computed |
| 21 | block door | 1 | - | 0x08F1 | 239 | wall clicked | flag 361 == 0; (item 260 == 0) and (hand item type != 260) |
| 22 | door switch | ? | ? | 0x038F | none | none | none |
| 23 | door switch | ? | ? | 0x0313 | none | none | none |
| 23 | door switch | 833 | 0 | 0x0998 | 832 | wall clicked | none |
| 23 | door switch | 518 | 0 | 0x0A30 | 582 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 518 | 0 | 0x0A44 | 487 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 327 | 0 | 0x0A58 | 359 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 327 | 0 | 0x0A6C | 295 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 262 | 0 | 0x0A80 | 231 | wall clicked | hand item type == 254 |
| 23 | door switch | 450 | 0 | 0x0B56 | 481 | wall clicked | none |
| 23 | door switch | 452 | 0 | 0x0B5D | 485 | wall clicked | none |
| 23 | door switch | 450 | -1 | 0x0BC0 | 451 | party arrives (second path) | none |
| 23 | door switch | 452 | -1 | 0x0BC5 | 451 | party arrives (second path) | none |
| 23 | door switch | 131 | 0 | 0x0C20 | 68 | wall clicked | none |
| 23 | door switch | 387 | 0 | 0x0C25 | 68 | wall clicked | none |
| 23 | door switch | 10 | 0 | 0x0CC6 | 41 | wall clicked | none |
| 23 | door switch | 10 | 0 | 0x0CE8 | 43 | wall clicked | none |
| 23 | door switch | 78 | 0 | 0x0CEE | 46 | wall clicked | none |
| 23 | door switch | 78 | -1 | 0x0D00 | 79 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 84 | 1 | 0x0DA1 | 83 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 84 | -1 | 0x0DB3 | 85 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 24 | 0 | 0x0DC6 | 55 | wall clicked | hand item type == 254 |
| 23 | door switch | 24 | 0 | 0x0DDF | 57 | wall clicked | hand item type == 254 |
| 23 | door switch | 856 | 1 | 0x0E0C | 823 | wall clicked | flag 403 == 1 |
| 23 | door switch | 856 | 1 | 0x0E33 | 887 | wall clicked | flag 402 == 1 |
| 23 | door switch | 677 | 0 | 0x1152 | 709 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 677 | 0 | 0x1166 | 645 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 502 | 0 | 0x11C9 | 533 | wall clicked | hand item type == 254 |
| 23 | door switch | 186 | 0 | 0x11EB | 154 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 186 | 0 | 0x11FF | 218 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 313 | 0 | 0x1213 | 312 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 313 | 0 | 0x1227 | 314 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 374 | 0 | 0x122E | 341 | wall clicked | none |
| 23 | door switch | 374 | 0 | 0x1235 | 405 | wall clicked | none |
| 23 | door switch | 444 | 0 | 0x1249 | 412 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 444 | 0 | 0x125D | 476 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 506 | 0 | 0x1271 | 474 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 506 | 0 | 0x1285 | 538 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 636 | 0 | 0x1299 | 604 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 636 | 0 | 0x12AD | 668 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 632 | 0 | 0x12C1 | 631 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 632 | 0 | 0x12D5 | 633 | party arrives (second path), party leaves (second path), item put down, item taken | none |
| 23 | door switch | 828 | 0 | 0x12DC | 797 | wall clicked | none |
| 23 | door switch | 828 | 0 | 0x12E3 | 861 | wall clicked | none |
| 26 | door switch | 446 or 533 or 568 or 663 or 723 or 866 | 1 | 0x0274 | 479, 566, 599, 691, 696, 867 | wall clicked | computed; (hand item type == 171) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 171) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 178) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 178) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 179) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 183) or (hand item type == 245); hand item type != 245 or hand item type != 180; computed; (hand item type == 181) or (hand item type == 245); hand item type != 245 or hand item type == 180; computed; (hand item type == 180) or (hand item type == 245); hand item type != 245 |
| 26 | door switch | 592 | 0 | 0x087F | 625 | wall clicked | none |
| 27 | door switch | ? | ? | 0x02E2 | none | none | none |
| 27 | door state | 301 | 0 | 0x0353 | 332 | wall clicked | computed |
| 27 | door state | 301 | 1 | 0x035D | 332 | wall clicked | computed |
| 27 | block door | 1 | - | 0x0779 | 361 | wall clicked | none |
| 27 | door switch | 197 | 1 | 0x07AB | 230 | wall clicked | none |
| 27 | door switch | 169 | 0 | 0x0843 | 233 | wall clicked | none |
| 27 | block door | 1 | - | 0x08CF | 236 | wall clicked | flag 430 == 0 |
| 27 | door switch | 141 | 0 | 0x091E | 77 | wall clicked, item put down, thrown item hits | none |
| 27 | door switch | 145 | 0 | 0x097E | 81 | wall clicked, item put down, thrown item hits | none |
| 27 | block door | 1 | - | 0x09A8 | 343 | wall clicked | computed |
| 27 | door switch | 655 | -1 | 0x0A3D | 654 | party arrives (second path) | none |
| 27 | door switch | 341 | 0 | 0x0D3E | 338 | wall clicked | none |
| 28 | door switch | 249 or 520 or 733 or 821 | 1 | 0x01AD | 217, 487, 702, 822 | wall clicked | computed; (hand item type == -1) or (hand item type == 245); hand item type != 245 or computed; (hand item type == -1) or (hand item type == 245); hand item type == 245 or computed; (hand item type == 206) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 208) or (hand item type == 245); hand item type != 245 or computed; (hand item type == 208) or (hand item type == 245); hand item type == 245 |
| 28 | door switch | 932 | 0 | 0x0656 | 999 | wall clicked | none |
| 28 | door switch | 932 | 0 | 0x0664 | 868 | wall clicked | none |
| 28 | door switch | 342 | 0 | 0x07EA | 343 | wall clicked | flag 438 == 1 |
| 28 | door switch | 372 | 0 | 0x0826 | 341 | wall clicked | none |
| 28 | door switch | 338 | 0 | 0x0830 | 339 | wall clicked | none |
| 28 | door switch | 207 | 0 | 0x0961 | 143 | wall clicked | none |
| 28 | block door | 1 | - | 0x0964 | 143 | wall clicked | none |
| 28 | door switch | 143 | 0 | 0x096B | 207 | wall clicked | none |
| 28 | block door | 1 | - | 0x096E | 207 | wall clicked | none |
| 28 | block door | 1 | - | 0x0AB6 | 644 | wall clicked | computed |
| 29 | door switch | ? | ? | 0x00F8 | none | none | none |
| 29 | door switch | 803 | -1 | 0x0C1C | 867 | party arrives (second path), party leaves (second path), item put down, item taken | computed |
| 29 | door switch | 803 | 1 | 0x0C2C | 995 | item taken | computed |
| 29 | door switch | 591 | -1 | 0x0D8C | 559 | party arrives (second path) | computed |
| 29 | block door | 1 | - | 0x0DD2 | 591 | wall clicked | computed; (flag 472 == 0) or (flag 473 == 0) |

## Graph

An edge is a constant destination level on a `loadNewLevel` row that a script entry reaches. All 29 levels are listed. Several rows can share one edge.

| From | To |
|---:|---|
| 1 | 2 |
| 2 | 1, 3, 5, 6, 10 |
| 3 | 2, 4 |
| 4 | 3 |
| 5 | 2 |
| 6 | 2, 7 |
| 7 | 6, 8 |
| 8 | 7, 9 |
| 9 | 8 |
| 10 | 11, 12 |
| 11 | 10, 11, 17 |
| 12 | 10, 13, 17 |
| 13 | 12, 14 |
| 14 | 12, 13, 15 |
| 15 | 12, 14, 16 |
| 16 | 12, 14, 15 |
| 17 | 11, 12, 24 |
| 18 | 19, 20, 24 |
| 19 | 18 |
| 20 | 18, 21 |
| 21 | 20 |
| 22 | 23, 24 |
| 23 | 22, 25, 26 |
| 24 | 17, 18, 22, 26 |
| 25 | 23 |
| 26 | 23, 24, 27 |
| 27 | 26, 28 |
| 28 | 26, 27, 29 |
| 29 | 28 |

Constant destinations from the reached sites leave every level on a path from level 1, and every level has an edge out. 
UNCONFIRMED: this graph is not a play trace. A static edge does not show that the party can walk it, and no level is marked unreachable or a dead end from these sites alone.

## Walk limit

The walk stops following one entry after 1000 visits to one address with different register values (a loop). It stopped for level 1 INF entries 401, 465; level 2 INF entry 0x400 level loaded; level 3 INF entry 690; level 3 INI entry INI 1; level 11 INF entries 45, 104, 135, 455, 475, 515, 660, 668; level 12 INF entries 35, 36, 38, 51, 85, 117, 131, 226; level 15 INF entry 431; level 18 INF entry 40; level 22 INF entry 376; level 24 INF entries 274, 276; level 28 INF entry 491; level 29 INF entry 0x401 script timer 0. For those entries the entry, argument and condition cells can be incomplete.
