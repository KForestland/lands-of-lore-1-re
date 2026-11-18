# Level 23

Made by `tools/level_report.py` from `LEVEL23.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 9 = CATWALK (decorations `CATWALK.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CATWALK (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1822 | — | — |  | 0x80 | 63 |
| 1 | 957 | 1 | — |  | 0x07 | 255 |
| 2 | 956 | 2 | — |  | 0x07 | 255 |
| 8 | 32 | 3 | — |  | 0xaf | 13 |
| 12 | 2 | 3 | — |  | 0x98 | 13 |
| 18 | 12 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 25 | 36 | — | — |  | 0x84 | 63 |
| 26 | 20 | — | — |  | 0x84 | 63 |
| 27 | 104 | — | 2 |  | 0x80 | 10 |
| 29 | 1 | 2 | 4 | 2 lever (to on) | 0x07 | 207 |
| 32 | 2 | 1 | 8 | 1 clickable wall | 0x07 | 210 |
| 36 | 22 | 2 | — |  | 0x84 | 214 |
| 37 | 7 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 38 | 1 | 2 | 12 | 6 niche | 0x87 | 255 |
| 40 | 20 | — | — |  | 0x80 | 17 |
| 42 | 1 | 2 | 43 | 2 lever (to on) | 0x07 | 207 |
| 44 | 16 | 1 | 52 | 2 lever (to on) | 0x07 | 207 |
| 47 | 20 | — | 38 |  | 0x84 | 11 |
| 48 | 2 | 2 | 51 | 1 clickable wall | 0x07 | 207 |
| 49 | 46 | 1 | 59 |  | 0x07 | 255 |
| 50 | 6 | 2 | 15 | 1 clickable wall | 0x07 | 255 |
| 51 | 1 | 1 | 16 | 6 niche | 0x87 | 14 |
| 61 | 1 | 2 | 60 | 1 clickable wall | 0x07 | 255 |
| 62 | 1 | 2 | 61 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 41 (x 9, y 1) | north | 44 | lever (to on) |
| 43 (x 11, y 1) | north | 44 | lever (to on) |
| 46 (x 14, y 1) | west | 44 | lever (to on) |
| 55 (x 23, y 1) | north | 37 | clickable wall |
| 57 (x 25, y 1) | north | 37 | clickable wall |
| 68 (x 4, y 2) | south | 42 | lever (to on) |
| 73 (x 9, y 2) | south | 50 | clickable wall |
| 81 (x 17, y 2) | south | 51 | niche |
| 89 (x 25, y 2) | south | 50 | clickable wall |
| 114 (x 18, y 3) | west | 44 | lever (to on) |
| 137 (x 9, y 4) | north | 50 | clickable wall |
| 153 (x 25, y 4) | north | 50 | clickable wall |
| 231 (x 7, y 7) | south | 37 | clickable wall |
| 237 (x 13, y 7) | south | 32 | clickable wall |
| 321 (x 1, y 10) | east | 44 | lever (to on) |
| 341 (x 21, y 10) | east | 44 | lever (to on) |
| 368 (x 16, y 11) | east | 50 | clickable wall |
| 370 (x 18, y 11) | west | 50 | clickable wall |
| 405 (x 21, y 12) | east | 44 | lever (to on) |
| 481 (x 1, y 15) | north | 44 | lever (to on) |
| 485 (x 5, y 15) | north | 44 | lever (to on) |
| 533 (x 21, y 16) | east | 37 | clickable wall |
| 705 (x 1, y 22) | east | 44 | lever (to on) |
| 739 (x 3, y 23) | west | 44 | lever (to on) |
| 761 (x 25, y 23) | south | 61 | clickable wall |
| 767 (x 31, y 23) | east | 44 | lever (to on) |
| 772 (x 4, y 24) | west | 44 | lever (to on) |
| 784 (x 16, y 24) | south | 38 | niche |
| 797 (x 29, y 24) | west | 44 | lever (to on) |
| 809 (x 9, y 25) | east | 37 | clickable wall |
| 823 (x 23, y 25) | west | 48 | clickable wall |
| 832 (x 0, y 26) | south | 44 | lever (to on) |
| 859 (x 27, y 26) | south | 32 | clickable wall |
| 861 (x 29, y 26) | west | 44 | lever (to on) |
| 887 (x 23, y 27) | west | 48 | clickable wall |
| 933 (x 5, y 29) | south | 37 | clickable wall |
| 939 (x 11, y 29) | north | 29 | lever (to on) |
| 953 (x 25, y 29) | north | 62 | clickable wall |
| 964 (x 4, y 30) | east | 37 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL23.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CATWALK; loads monster sprites CABAL.SHP into slot 0; loads monster sprites DRKCMNDR.SHP into slot 1; loads monster sprites NECROSAP.SHP into slot 1; defines monster type 1; defines monster type 0; defines monster type 2; tests game flag 577 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 943; places a monster (slot 1) on block 946; places a monster (slot 1) on block 843; places a monster (slot 1) on block 846; places a monster (slot 1) on block 819; places a monster (slot 1) on block 866; places a monster (slot 1) on block 898; places a monster (slot 2) on block 737 … |

### LEVEL23.INF

| Entry | Events | What it does |
|---|---|---|
| block 9 (x 9, y 0) | party arrives (second path) | clears game flag 408 |
| block 11 (x 11, y 0) | party arrives (second path) | sets game flag 408 |
| block 23 (x 23, y 0) | party arrives (second path) | sets game flag 408 |
| block 25 (x 25, y 0) | party arrives (second path) | clears game flag 408 |
| block 41 (x 9, y 1) | wall clicked | operates the door at block 10 |
| block 43 (x 11, y 1) | wall clicked | operates the door at block 10 |
| block 46 (x 14, y 1) | wall clicked | operates the door at block 78 |
| block 55 (x 23, y 1) | wall clicked | operates the door at block 24; a character speaks |
| block 57 (x 25, y 1) | wall clicked | operates the door at block 24; a character speaks |
| block 68 (x 4, y 2) | wall clicked | operates the door at block 131; operates the door at block 387 |
| block 70 (x 6, y 2) | party arrives (second path) | set global var |
| block 73 (x 9, y 2) | wall clicked | deals damage; a character speaks; plays a sound |
| block 79 (x 15, y 2) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 79 to type 28; operates the door at block 78; checks a wall of block 79; plays a sound |
| block 83 (x 19, y 2) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 83 to type 28; operates the door at block 84; checks a wall of block 83; plays a sound |
| block 85 (x 21, y 2) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 85 to type 28; operates the door at block 84; checks a wall of block 85; plays a sound |
| block 89 (x 25, y 2) | wall clicked | deals damage; a character speaks; plays a sound |
| block 102 (x 6, y 3) | party arrives (second path) | set global var |
| block 105 (x 9, y 3) | monster leaves | sets the south wall of block 81 to type ?; changes a monster; plays a sound |
| block 114 (x 18, y 3) | wall clicked | places item ? (?) on block 81; sets game flag 579; tests game flag 579; checks a wall of block 81 |
| block 121 (x 25, y 3) | monster leaves | sets the south wall of block 81 to type ?; changes a monster; plays a sound |
| block 137 (x 9, y 4) | wall clicked | deals damage; a character speaks; plays a sound |
| block 153 (x 25, y 4) | wall clicked | deals damage; a character speaks; plays a sound |
| block 154 (x 26, y 4) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 154 to type 28; operates the door at block 186; checks a wall of block 154; plays a sound |
| block 162 (x 2, y 5) | party arrives (second path), item put down | checks a wall of block 162 |
| block 169 (x 9, y 5) | monster leaves | delete monsters from block; tests game flag 408 |
| block 201 (x 9, y 6) | monster leaves | delete monsters from block; tests game flag 408 |
| block 218 (x 26, y 6) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 218 to type 28; operates the door at block 186; checks a wall of block 218; plays a sound |
| block 226 (x 2, y 7) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 226 to type 28; toggles the west wall of block 162 between types 0 and 40; checks a wall of block 226; plays a sound |
| block 227 (x 3, y 7) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 25, block 227; sets game flag 46; moves objects from block 227 to block 227; checks a wall of block 227 |
| block 231 (x 7, y 7) | wall clicked | operates the door at block 262; a character speaks |
| block 237 (x 13, y 7) | wall clicked | gives item 114 (Death Stick); gives item 218 (Ginseng); gives item 150 (George's kite shield); gives item 215 (Bannon's reserve); gives item 188 (Yellow Key); gives item 238 (Mist of Doom scroll); sets game flag 400; checks a wall of block 192 … |
| block 258 (x 2, y 8) | party steps in, party arrives (second path), item put down | sets the west wall of block 162 to type 40; sets the west wall of block 162 to type 0; sets the west wall of block 290 to type 28; toggles the west wall of block 356 between types 0 and 40; toggles the west wall of block 354 between types 0 and 40; sets the west wall of block 226 to type 28; toggles the west wall of block 162 between types 0 and 40; tests game flag 404 … |
| block 269 (x 13, y 8) | bits 0x400 (no engine caller found) | sets game flag 400; checks a wall of block 192; tests game flag 400 |
| block 290 (x 2, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 290 to type 28; toggles the west wall of block 356 between types 0 and 40; toggles the west wall of block 354 between types 0 and 40; checks a wall of block 290; plays a sound |
| block 291 (x 3, y 9) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 25, block 291; sets game flag 46; moves objects from block 291 to block 291; checks a wall of block 291 |
| block 295 (x 7, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 295 to type 28; operates the door at block 327; checks a wall of block 295; plays a sound |
| block 308 (x 20, y 9) | party arrives (second path) | set global var |
| block 309 (x 21, y 9) | party arrives (second path) | set global var |
| block 312 (x 24, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 312 to type 28; operates the door at block 313; checks a wall of block 312; plays a sound |
| block 314 (x 26, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 314 to type 28; operates the door at block 313; checks a wall of block 314; plays a sound |
| block 321 (x 1, y 10) | wall clicked | toggles the west wall of block 354 between types 0 and 40; toggles the west wall of block 356 between types 0 and 40; sets/clears game flag 407; tests game flag 407 |
| block 325 (x 5, y 10) | party steps in, party arrives (second path), item put down | moves objects from block 325 to block 293 |
| block 341 (x 21, y 10) | wall clicked | operates the door at block 374 |
| block 354 (x 2, y 11) | party arrives (second path), item put down | checks a wall of block 354 |
| block 356 (x 4, y 11) | party arrives (second path), item put down | places a monster (slot 2) on block 483; checks a wall of block 356 |
| block 359 (x 7, y 11) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 359 to type 28; operates the door at block 327; checks a wall of block 359; plays a sound |
| block 368 (x 16, y 11) | wall clicked | deals damage; a character speaks; plays a sound |
| block 369 (x 17, y 11) | monster leaves | sets the south wall of block 81 to type ?; changes a monster; plays a sound |
| block 370 (x 18, y 11) | wall clicked | deals damage; a character speaks; plays a sound |
| block 405 (x 21, y 12) | wall clicked | operates the door at block 374 |
| block 408 (x 24, y 12) | monster leaves | delete monsters from block; tests game flag 408 |
| block 412 (x 28, y 12) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 412 to type 28; operates the door at block 444; checks a wall of block 412; plays a sound |
| block 417 (x 1, y 13) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 417 to type 28; sets the west wall of block 162 to type 40; sets the west wall of block 162 to type 0; sets/clears game flag 404; checks a wall of block 417; plays a sound; tests game flag 404; tests game flag 405 … |
| block 419 (x 3, y 13) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 419 to type 28; sets the west wall of block 162 to type 40; sets the west wall of block 162 to type 0; sets/clears game flag 405; checks a wall of block 419; plays a sound; tests game flag 404; tests game flag 405 … |
| block 421 (x 5, y 13) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 421 to type 28; sets the west wall of block 162 to type 40; sets the west wall of block 162 to type 0; sets/clears game flag 406; checks a wall of block 421; plays a sound; tests game flag 404; tests game flag 405 … |
| block 426 (x 10, y 13) | party arrives (second path) | character surprise feedback; move party |
| block 430 (x 14, y 13) | party arrives (second path) | character surprise feedback; move party |
| block 451 (x 3, y 14) | party arrives (second path) | operates the door at block 450; operates the door at block 452 |
| block 465 (x 17, y 14) | party arrives (second path) | character surprise feedback; move party |
| block 474 (x 26, y 14) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 474 to type 28; operates the door at block 506; checks a wall of block 474; plays a sound |
| block 476 (x 28, y 14) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 476 to type 28; operates the door at block 444; checks a wall of block 476; plays a sound |
| block 481 (x 1, y 15) | wall clicked | operates the door at block 450 |
| block 485 (x 5, y 15) | wall clicked | operates the door at block 452 |
| block 487 (x 7, y 15) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 487 to type 28; operates the door at block 518; checks a wall of block 487; plays a sound |
| block 494 (x 14, y 15) | party arrives (second path) | character surprise feedback; move party |
| block 515 (x 3, y 16) | party arrives (second path), item put down | places a monster (slot 2) on block 483; checks a wall of block 515 |
| block 522 (x 10, y 16) | party arrives (second path) | character surprise feedback; move party |
| block 528 (x 16, y 16) | party arrives (second path) | character surprise feedback; move party |
| block 532 (x 20, y 16) | party steps in, party arrives (second path), item put down | checks a wall of block 532 |
| block 533 (x 21, y 16) | wall clicked | operates the door at block 502; a character speaks |
| block 538 (x 26, y 16) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 538 to type 28; operates the door at block 506; checks a wall of block 538; plays a sound |
| block 582 (x 6, y 18) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 582 to type 28; operates the door at block 518; checks a wall of block 582; plays a sound |
| block 586 (x 10, y 18) | party arrives (second path) | character surprise feedback; move party |
| block 593 (x 17, y 18) | party arrives (second path) | character surprise feedback; move party |
| block 604 (x 28, y 18) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 604 to type 28; operates the door at block 636; checks a wall of block 604; plays a sound |
| block 631 (x 23, y 19) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 631 to type 28; operates the door at block 632; checks a wall of block 631; plays a sound |
| block 633 (x 25, y 19) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 633 to type 28; operates the door at block 632; checks a wall of block 633; plays a sound |
| block 645 (x 5, y 20) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 645 to type 28; operates the door at block 677; checks a wall of block 645; plays a sound |
| block 650 (x 10, y 20) | party arrives (second path) | character surprise feedback; move party |
| block 668 (x 28, y 20) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 668 to type 28; operates the door at block 636; checks a wall of block 668; plays a sound |
| block 674 (x 2, y 21) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 674; sets game flag 46; moves objects from block 674 to block 674; checks a wall of block 674 |
| block 687 (x 15, y 21) | party arrives (second path) | character surprise feedback; move party |
| block 705 (x 1, y 22) | wall clicked | sets the west wall of block 738 to type 0; sets the west wall of block 738 to type 47; drops the party through a pit; deals damage; moves the party to level 25, block 738; sets the west wall of block 674 to type 0; sets the west wall of block 674 to type 47; moves the party to level 25, block 674 … |
| block 706 (x 2, y 22) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 706; sets game flag 46; moves objects from block 706 to block 706; checks a wall of block 706 |
| block 709 (x 5, y 22) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 709 to type 28; operates the door at block 677; checks a wall of block 709; plays a sound |
| block 725 (x 21, y 22) | party arrives (second path) | set global var |
| block 736 (x 0, y 23) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 736; sets game flag 46; moves objects from block 736 to block 736; checks a wall of block 736 |
| block 738 (x 2, y 23) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 738; sets game flag 46; moves objects from block 738 to block 738; checks a wall of block 738 |
| block 739 (x 3, y 23) | wall clicked | sets the west wall of block 706 to type 0; sets the west wall of block 706 to type 47; drops the party through a pit; deals damage; moves the party to level 25, block 706; sets the west wall of block 674 to type 0; sets the west wall of block 674 to type 47; moves the party to level 25, block 674 … |
| block 748 (x 12, y 23) | wall clicked | a character speaks; set global var; tests game flag 419 |
| block 761 (x 25, y 23) | wall clicked | a character speaks |
| block 767 (x 31, y 23) | wall clicked | sets the west wall of block 706 to type 0; sets the west wall of block 706 to type 47; drops the party through a pit; deals damage; moves the party to level 25, block 706; sets the west wall of block 738 to type 0; sets the west wall of block 738 to type 47; moves the party to level 25, block 738 … |
| block 768 (x 0, y 24) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 768; sets game flag 46; moves objects from block 768 to block 768; checks a wall of block 768 |
| block 769 (x 1, y 24) | party arrives (second path) | drops the party through a pit; deals damage; moves the party to level 25, block 769; sets game flag 46; moves objects from block 769 to block 769; checks a wall of block 769 |
| block 772 (x 4, y 24) | wall clicked | sets the west wall of block 736 to type 0; sets the west wall of block 736 to type 47; drops the party through a pit; deals damage; moves the party to level 25, block 736; sets the west wall of block 768 to type 0; sets the west wall of block 768 to type 47; moves the party to level 25, block 768 … |
| block 780 (x 12, y 24) | party steps in, party arrives (second path), item put down | places a monster (slot 1) on block 812; places a monster (slot 0) on block 780; moves objects from block 780 to block 812; shows a message; sets game flag 419; a character speaks; loads monster sprites DRKCMNDR.SHP into slot 1; defines monster type 0 … |
| block 784 (x 16, y 24) | item put down | sets the west wall of block 852 to type 0; checks a wall of block 852; plays a sound |
| block 789 (x 21, y 24) | party arrives (second path) | set global var |
| block 792 (x 24, y 24) | party arrives (second path), item put down | sets game flag 582; moves objects from block 792 to block 910; tests game flag 583 |
| block 797 (x 29, y 24) | wall clicked | operates the door at block 828 |
| block 809 (x 9, y 25) | wall clicked | sets the west wall of block 841 to type 0; a character speaks; checks a wall of block 841; plays a sound |
| block 823 (x 23, y 25) | wall clicked | operates the door at block 856; a character speaks; sets game flag 402; tests game flag 403 |
| block 832 (x 0, y 26) | wall clicked | operates the door at block 833 |
| block 840 (x 8, y 26) | party arrives (second path) | sets the west wall of block 841 to type 1; checks a wall of block 841; plays a sound |
| block 846 (x 14, y 26) | monster leaves | delete monsters from block; tests game flag 408 |
| block 857 (x 25, y 26) | party arrives (second path) | a character speaks; sets game flag 420; tests game flag 420 |
| block 859 (x 27, y 26) | wall clicked | gives item 53 (Great axe "Master"); gives item 248 (Oil Flask); gives item 215 (Bannon's reserve); gives item 189 (Small Key); gives item 269 (Guardian) |
| block 861 (x 29, y 26) | wall clicked | operates the door at block 828 |
| block 887 (x 23, y 27) | wall clicked | operates the door at block 856; a character speaks; sets game flag 403; tests game flag 402 |
| block 891 (x 27, y 27) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 902 (x 6, y 28) | party arrives (second path) | sets the west wall of block 934 to type 1; checks a wall of block 934; plays a sound |
| block 920 (x 24, y 28) | party arrives (second path), item put down | sets game flag 583; moves objects from block 920 to block 211; tests game flag 582 |
| block 933 (x 5, y 29) | wall clicked | sets the west wall of block 934 to type 0; a character speaks; checks a wall of block 934; plays a sound |
| block 939 (x 11, y 29) | wall clicked | sets the east wall of block 906 to type 31; checks a wall of block 906; plays a sound |
| block 942 (x 14, y 29) | monster leaves | delete monsters from block; tests game flag 408 |
| block 953 (x 25, y 29) | wall clicked | a character speaks |
| block 964 (x 4, y 30) | wall clicked | sets the west wall of block 996 to type 0; a character speaks; checks a wall of block 996; plays a sound |
| block 995 (x 3, y 31) | party arrives (second path) | sets the west wall of block 996 to type 1; checks a wall of block 996; plays a sound |
| block 1009 (x 17, y 31) | party steps in, party arrives (second path), item put down | moves objects from block 1009 to block 59 |
| `0x400` level loaded | — | starts script timer 0; starts script timer 1 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 659; places a monster (slot 1) on block 344; places a monster (slot 1) on block 732; places a monster (slot 2) on block 12; places a monster (slot 2) on block 22; tests game flag 419; tests game flag 408 |
| `0x402` script timer 1 | — | places a monster (slot 1) on block 591; places a monster (slot 1) on block 520; tests game flag 419; tests game flag 408 |
| `0x404` a monster died | — | clears game flag 577; loads monster sprites NECROSAP.SHP into slot 1 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 216 | Salve | 23 | 906 |
| INI entry 1 (runs when the level loads) | 276 | Note | 23 | 81 |
| block 114 (x 18, y 3) | ? | ? | 23 | 81 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 943 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 943 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 843 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 843 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 846 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 846 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 819 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 819 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 866 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 898 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 737 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 673 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 545 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 546 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 240 | 3 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 241 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 242 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 774 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 774 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 680 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 680 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 728 | 3 | 1 | 4 |
| block 356 (x 4, y 11) | 483 | 0 | 2 | 4 |
| block 515 (x 3, y 16) | 483 | 0 | 2 | 4 |
| block 780 (x 12, y 24) | 812 | 2 | 1 | 7 |
| block 780 (x 12, y 24) | 812 | 2 | 1 | 7 |
| block 780 (x 12, y 24) | 780 | 2 | 0 | 7 |
| `0x401` script timer 0 | 659 | 3 | 1 | 4 |
| `0x401` script timer 0 | 659 | 3 | 1 | 4 |
| `0x401` script timer 0 | 344 | 3 | 1 | 4 |
| `0x401` script timer 0 | 344 | 3 | 1 | 4 |
| `0x401` script timer 0 | 732 | 2 | 1 | 4 |
| `0x401` script timer 0 | 732 | 2 | 1 | 4 |
| `0x401` script timer 0 | 12 | 1 | 2 | 4 |
| `0x401` script timer 0 | 22 | 3 | 2 | 4 |
| `0x402` script timer 1 | 591 | 2 | 1 | 4 |
| `0x402` script timer 1 | 591 | 2 | 1 | 4 |
| `0x402` script timer 1 | 520 | 1 | 1 | 4 |
| `0x402` script timer 1 | 520 | 1 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 12, y 25 | 8 | x 11, y 24 | 0x41fb | COMMANDER'S AREA |
| x 25, y 29 | 4 | x 25, y 29 | 0x41fc | XEOBS SYMBOL |
| x 25, y 23 | 3 | x 25, y 23 | 0x41fd | KNOWLES SYMBOL |
| x 26, y 26 | 1 | x 26, y 26 | 0x41fe | THE SUMMONING |

## Text shown by the scripts (ids only)

- Level text file `LEVEL23.<lang>`: 12 ids: 2, 3, 4, 6, 13, 15, 24, 29, 30, 31, 32, 33.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL23.ENG --index N`.
