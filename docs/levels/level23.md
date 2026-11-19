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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL23.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CATWALK; loads monster sprites CABAL.SHP into slot 0; loads monster sprites DRKCMNDR.SHP into slot 1; loads monster sprites NECROSAP.SHP into slot 1; defines monster type 1; defines monster type 0; defines monster type 2; tests game flag 577 |
| INI entry 1 (runs when the level loads) | `0x010C` | — | places a monster of type slot 1 on block 943 in mode 4; places a monster of type slot 1 on block 946 in mode 3; places a monster of type slot 1 on block 843 in mode 3; places a monster of type slot 1 on block 846 in mode 3; places a monster of type slot 1 on block 819 in mode 3; places a monster of type slot 1 on block 866 in mode 3; places a monster of type slot 1 on block 898 in mode 3; places a monster of type slot 2 on block 737 in mode 3 … |

### LEVEL23.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 9 (x 9, y 0) | `0x0CC9` | party arrives (second path) | clears game flag 408 |
| block 11 (x 11, y 0) | `0x0CD0` | party arrives (second path) | sets game flag 408 |
| block 23 (x 23, y 0) | `0x0CD7` | party arrives (second path) | sets game flag 408 |
| block 25 (x 25, y 0) | `0x0CDE` | party arrives (second path) | clears game flag 408 |
| block 41 (x 9, y 1) | `0x0CC3` | wall clicked | operates the door switch at block 10 with action 0 |
| block 43 (x 11, y 1) | `0x0CE5` | wall clicked | operates the door switch at block 10 with action 0 |
| block 46 (x 14, y 1) | `0x0CEB` | wall clicked | operates the door switch at block 78 with action 0 |
| block 55 (x 23, y 1) | `0x0DB6` | wall clicked | operates the door switch at block 24 with action 0; plays chat/dialogue text ID 0x001d |
| block 57 (x 25, y 1) | `0x0DCF` | wall clicked | operates the door switch at block 24 with action 0; plays chat/dialogue text ID 0x001d |
| block 68 (x 4, y 2) | `0x0C1C` | wall clicked | operates the door switch at block 131 with action 0; operates the door switch at block 387 with action 0 |
| block 70 (x 6, y 2) | `0x0C28` | party arrives (second path) | requests engine global change, selector 12, operands 0, 0 |
| block 73 (x 9, y 2) | `0x1424` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 79 (x 15, y 2) | `0x0CF1` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 79 to type 28; operates the door switch at block 78 with action -1; checks the north wall of block 79; plays a sound (ID 80) |
| block 83 (x 19, y 2) | `0x0D92` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 83 to type 28; operates the door switch at block 84 with action 1; checks the north wall of block 83; plays a sound (ID 80) |
| block 85 (x 21, y 2) | `0x0DA4` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 85 to type 28; operates the door switch at block 84 with action -1; checks the north wall of block 85; plays a sound (ID 80) |
| block 89 (x 25, y 2) | `0x13B0` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 102 (x 6, y 3) | `0x0C2C` | party arrives (second path) | requests engine global change, selector 12, operands 1, 0 |
| block 105 (x 9, y 3) | `0x0D03` | monster leaves | sets the south wall of block 81 to type ?; sets monster ? mode to 11; plays a sound (ID 88); plays a sound (ID 87); plays a sound (ID 94) |
| block 114 (x 18, y 3) | `0x0D4C` | wall clicked | places item ? (?) on block 81; sets game flag 579; tests game flag 579; checks the south wall of block 81 |
| block 121 (x 25, y 3) | `0x0D1B` | monster leaves | sets the south wall of block 81 to type ?; sets monster ? mode to 11; plays a sound (ID 88); plays a sound (ID 87); plays a sound (ID 94) |
| block 137 (x 9, y 4) | `0x1441` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 153 (x 25, y 4) | `0x13CD` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 154 (x 26, y 4) | `0x11DA` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 154 to type 28; operates the door switch at block 186 with action 0; checks the north wall of block 154; plays a sound (ID 80) |
| block 162 (x 2, y 5) | `0x0AEF` | party arrives (second path), item put down | checks the north wall of block 162 |
| block 169 (x 9, y 5) | `0x135C` | monster leaves | delete monsters from block; tests game flag 408 |
| block 201 (x 9, y 6) | `0x1355` | monster leaves | delete monsters from block; tests game flag 408 |
| block 218 (x 26, y 6) | `0x11EE` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 218 to type 28; operates the door switch at block 186 with action 0; checks the north wall of block 218; plays a sound (ID 80) |
| block 226 (x 2, y 7) | `0x0BE1` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 226 to type 28; toggles all four walls of block 162 between types 0 and 40; checks the north wall of block 226; plays a sound (ID 80) |
| block 227 (x 3, y 7) | `0x0B60` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 227, facing ?; removes monsters from block 227; sets game flag 46; moves items from block 227 to level 25, block 227; checks the north wall of block 227 |
| block 231 (x 7, y 7) | `0x0A6F` | wall clicked | operates the door switch at block 262 with action 0; plays chat/dialogue text ID 0x001d |
| block 237 (x 13, y 7) | `0x0C58` | wall clicked | puts item 114 (Death Stick) on an empty cursor; puts item 218 (Ginseng) on an empty cursor; puts item 150 (George's kite shield) on an empty cursor; puts item 215 (Bannon's reserve) on an empty cursor; puts item 188 (Yellow Key) on an empty cursor; puts item 238 (Mist of Doom scroll) on an empty cursor; sets game flag 400; checks the south wall of block 192 … |
| block 258 (x 2, y 8) | `0x0A97` | party steps in, party arrives (second path), item put down | sets all four walls of block 162 to type 40; sets all four walls of block 162 to type 0; sets all four walls of block 290 to type 28; toggles all four walls of block 356 between types 0 and 40; toggles all four walls of block 354 between types 0 and 40; sets all four walls of block 226 to type 28; toggles all four walls of block 162 between types 0 and 40; requests engine global change, selector 0, operands 0, 290 … |
| block 269 (x 13, y 8) | `0x0C30` | bits 0x400 (no engine caller found) | sets game flag 400; checks the south wall of block 192; tests game flag 400 |
| block 290 (x 2, y 9) | `0x0BFB` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 290 to type 28; toggles all four walls of block 356 between types 0 and 40; toggles all four walls of block 354 between types 0 and 40; checks the north wall of block 290; plays a sound (ID 80) |
| block 291 (x 3, y 9) | `0x0B6A` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 291, facing ?; removes monsters from block 291; sets game flag 46; moves items from block 291 to level 25, block 291; checks the north wall of block 291 |
| block 295 (x 7, y 9) | `0x0A5B` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 295 to type 28; operates the door switch at block 327 with action 0; checks the north wall of block 295; plays a sound (ID 80) |
| block 308 (x 20, y 9) | `0x11D2` | party arrives (second path) | requests engine global change, selector 12, operands 0, 0 |
| block 309 (x 21, y 9) | `0x11D6` | party arrives (second path) | requests engine global change, selector 12, operands 1, 0 |
| block 312 (x 24, y 9) | `0x1202` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 312 to type 28; operates the door switch at block 313 with action 0; checks the north wall of block 312; plays a sound (ID 80) |
| block 314 (x 26, y 9) | `0x1216` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 314 to type 28; operates the door switch at block 313 with action 0; checks the north wall of block 314; plays a sound (ID 80) |
| block 321 (x 1, y 10) | `0x0BC8` | wall clicked | toggles all four walls of block 354 between types 0 and 40; toggles all four walls of block 356 between types 0 and 40; sets/clears game flag 407; tests game flag 407 |
| block 325 (x 5, y 10) | `0x0A89` | party steps in, party arrives (second path), item put down | moves items from block 325 to level 25, block 293 |
| block 341 (x 21, y 10) | `0x122A` | wall clicked | operates the door switch at block 374 with action 0 |
| block 354 (x 2, y 11) | `0x0AF9` | party arrives (second path), item put down | checks the north wall of block 354 |
| block 356 (x 4, y 11) | `0x0B04` | party arrives (second path), item put down | places a monster of type slot 2 on block 483 in mode 4; checks the north wall of block 356 |
| block 359 (x 7, y 11) | `0x0A47` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 359 to type 28; operates the door switch at block 327 with action 0; checks the north wall of block 359; plays a sound (ID 80) |
| block 368 (x 16, y 11) | `0x13EA` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 369 (x 17, y 11) | `0x0D33` | monster leaves | sets the south wall of block 81 to type ?; sets monster ? mode to 11; plays a sound (ID 88); plays a sound (ID 87); plays a sound (ID 94) |
| block 370 (x 18, y 11) | `0x1407` | wall clicked | deals damage to target ? (amount ?); plays chat/dialogue text ID 0x001e; plays a sound (ID 162) |
| block 405 (x 21, y 12) | `0x1231` | wall clicked | operates the door switch at block 374 with action 0 |
| block 408 (x 24, y 12) | `0x1363` | monster leaves | delete monsters from block; tests game flag 408 |
| block 412 (x 28, y 12) | `0x1238` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 412 to type 28; operates the door switch at block 444 with action 0; checks the north wall of block 412; plays a sound (ID 80) |
| block 417 (x 1, y 13) | `0x0B74` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 417 to type 28; sets all four walls of block 162 to type 40; sets all four walls of block 162 to type 0; sets/clears game flag 404; checks the north wall of block 417; plays a sound (ID 80); tests game flag 404; tests game flag 405 … |
| block 419 (x 3, y 13) | `0x0B8C` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 419 to type 28; sets all four walls of block 162 to type 40; sets all four walls of block 162 to type 0; sets/clears game flag 405; checks the north wall of block 419; plays a sound (ID 80); tests game flag 404; tests game flag 405 … |
| block 421 (x 5, y 13) | `0x0BA4` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 421 to type 28; sets all four walls of block 162 to type 40; sets all four walls of block 162 to type 0; sets/clears game flag 406; checks the north wall of block 421; plays a sound (ID 80); tests game flag 404; tests game flag 405 … |
| block 426 (x 10, y 13) | `0x119C` | party arrives (second path) | character surprise feedback; move party |
| block 430 (x 14, y 13) | `0x11A2` | party arrives (second path) | character surprise feedback; move party |
| block 451 (x 3, y 14) | `0x0BBC` | party arrives (second path) | operates the door switch at block 450 with action -1; operates the door switch at block 452 with action -1 |
| block 465 (x 17, y 14) | `0x11A8` | party arrives (second path) | character surprise feedback; move party |
| block 474 (x 26, y 14) | `0x1260` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 474 to type 28; operates the door switch at block 506 with action 0; checks the north wall of block 474; plays a sound (ID 80) |
| block 476 (x 28, y 14) | `0x124C` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 476 to type 28; operates the door switch at block 444 with action 0; checks the north wall of block 476; plays a sound (ID 80) |
| block 481 (x 1, y 15) | `0x0B52` | wall clicked | operates the door switch at block 450 with action 0 |
| block 485 (x 5, y 15) | `0x0B59` | wall clicked | operates the door switch at block 452 with action 0 |
| block 487 (x 7, y 15) | `0x0A33` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 487 to type 28; operates the door switch at block 518 with action 0; checks the north wall of block 487; plays a sound (ID 80) |
| block 494 (x 14, y 15) | `0x1190` | party arrives (second path) | character surprise feedback; move party |
| block 515 (x 3, y 16) | `0x0B2B` | party arrives (second path), item put down | places a monster of type slot 2 on block 483 in mode 4; checks the north wall of block 515 |
| block 522 (x 10, y 16) | `0x1187` | party arrives (second path) | character surprise feedback; move party |
| block 528 (x 16, y 16) | `0x1196` | party arrives (second path) | character surprise feedback; move party |
| block 532 (x 20, y 16) | `0x11AE` | party steps in, party arrives (second path), item put down | checks the north wall of block 532 |
| block 533 (x 21, y 16) | `0x11B8` | wall clicked | operates the door switch at block 502 with action 0; plays chat/dialogue text ID 0x001d |
| block 538 (x 26, y 16) | `0x1274` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 538 to type 28; operates the door switch at block 506 with action 0; checks the north wall of block 538; plays a sound (ID 80) |
| block 582 (x 6, y 18) | `0x0A1F` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 582 to type 28; operates the door switch at block 518 with action 0; checks the north wall of block 582; plays a sound (ID 80) |
| block 586 (x 10, y 18) | `0x1175` | party arrives (second path) | character surprise feedback; move party |
| block 593 (x 17, y 18) | `0x117E` | party arrives (second path) | character surprise feedback; move party |
| block 604 (x 28, y 18) | `0x1288` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 604 to type 28; operates the door switch at block 636 with action 0; checks the north wall of block 604; plays a sound (ID 80) |
| block 631 (x 23, y 19) | `0x12B0` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 631 to type 28; operates the door switch at block 632 with action 0; checks the north wall of block 631; plays a sound (ID 80) |
| block 633 (x 25, y 19) | `0x12C4` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 633 to type 28; operates the door switch at block 632 with action 0; checks the north wall of block 633; plays a sound (ID 80) |
| block 645 (x 5, y 20) | `0x1155` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 645 to type 28; operates the door switch at block 677 with action 0; checks the north wall of block 645; plays a sound (ID 80) |
| block 650 (x 10, y 20) | `0x1169` | party arrives (second path) | character surprise feedback; move party |
| block 668 (x 28, y 20) | `0x129C` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 668 to type 28; operates the door switch at block 636 with action 0; checks the north wall of block 668; plays a sound (ID 80) |
| block 674 (x 2, y 21) | `0x09CD` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 674, facing ?; removes monsters from block 674; sets game flag 46; moves items from block 674 to level 25, block 674; checks the north wall of block 674 |
| block 687 (x 15, y 21) | `0x116F` | party arrives (second path) | character surprise feedback; move party |
| block 705 (x 1, y 22) | `0x0A0D` | wall clicked | sets all four walls of block 738 to type 0; sets all four walls of block 738 to type 47; removes monsters from block 738; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 738, facing ?; sets all four walls of block 674 to type 0; sets all four walls of block 674 to type 47 … |
| block 706 (x 2, y 22) | `0x09C3` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 706, facing ?; removes monsters from block 706; sets game flag 46; moves items from block 706 to level 25, block 706; checks the north wall of block 706 |
| block 709 (x 5, y 22) | `0x1141` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 709 to type 28; operates the door switch at block 677 with action 0; checks the north wall of block 709; plays a sound (ID 80) |
| block 725 (x 21, y 22) | `0x134D` | party arrives (second path) | requests engine global change, selector 12, operands 1, 0 |
| block 736 (x 0, y 23) | `0x09A5` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 736, facing ?; removes monsters from block 736; sets game flag 46; moves items from block 736 to level 25, block 736; checks the north wall of block 736 |
| block 738 (x 2, y 23) | `0x09B9` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 738, facing ?; removes monsters from block 738; sets game flag 46; moves items from block 738 to level 25, block 738; checks the north wall of block 738 |
| block 739 (x 3, y 23) | `0x09FB` | wall clicked | sets all four walls of block 706 to type 0; sets all four walls of block 706 to type 47; removes monsters from block 706; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 706, facing ?; sets all four walls of block 674 to type 0; sets all four walls of block 674 to type 47 … |
| block 748 (x 12, y 23) | `0x08C7` | wall clicked | requests engine global change, selector 0, operands 0, 812; plays chat/dialogue text ID 0x0021; tests game flag 419 |
| block 761 (x 25, y 23) | `0x145E` | wall clicked | plays chat/dialogue text ID 0x001f |
| block 767 (x 31, y 23) | `0x09D7` | wall clicked | sets all four walls of block 706 to type 0; sets all four walls of block 706 to type 47; removes monsters from block 706; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 706, facing ?; sets all four walls of block 738 to type 0; sets all four walls of block 738 to type 47 … |
| block 768 (x 0, y 24) | `0x099B` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 768, facing ?; removes monsters from block 768; sets game flag 46; moves items from block 768 to level 25, block 768; checks the north wall of block 768 |
| block 769 (x 1, y 24) | `0x09AF` | party arrives (second path) | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 769, facing ?; removes monsters from block 769; sets game flag 46; moves items from block 769 to level 25, block 769; checks the north wall of block 769 |
| block 772 (x 4, y 24) | `0x09E9` | wall clicked | sets all four walls of block 736 to type 0; sets all four walls of block 736 to type 47; removes monsters from block 736; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 25, block 736, facing ?; sets all four walls of block 768 to type 0; sets all four walls of block 768 to type 47 … |
| block 780 (x 12, y 24) | `0x0709` | party steps in, party arrives (second path), item put down | places a monster of type slot 1 on block 812 in mode 7; places a monster of type slot 0 on block 780 in mode 7; moves items from block 780 to level 23, block 812; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 812; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 10, operands 0, 2; sets game flag 419 … |
| block 784 (x 16, y 24) | `0x06EA` | item put down | sets all four walls of block 852 to type 0; checks the north wall of block 852; plays a sound (ID 38) |
| block 789 (x 21, y 24) | `0x1351` | party arrives (second path) | requests engine global change, selector 12, operands 0, 0 |
| block 792 (x 24, y 24) | `0x10FC` | party arrives (second path), item put down | removes monsters from block 792; sets game flag 582; moves items from block 792 to level 26, block 910; tests game flag 583 |
| block 797 (x 29, y 24) | `0x12D8` | wall clicked | operates the door switch at block 828 with action 0 |
| block 809 (x 9, y 25) | `0x08F2` | wall clicked | sets all four walls of block 841 to type 0; plays chat/dialogue text ID 0x001d; checks the north wall of block 841; plays a sound (ID 38) |
| block 823 (x 23, y 25) | `0x0DE8` | wall clicked | operates the door switch at block 856 with action 1; plays chat/dialogue text ID 0x0018; sets game flag 402; tests game flag 403 |
| block 832 (x 0, y 26) | `0x0994` | wall clicked | operates the door switch at block 833 with action 0 |
| block 840 (x 8, y 26) | `0x091A` | party arrives (second path) | sets all four walls of block 841 to type 1; checks the north wall of block 841; plays a sound (ID 38) |
| block 846 (x 14, y 26) | `0x136A` | monster leaves | delete monsters from block; tests game flag 408 |
| block 857 (x 25, y 26) | `0x0ECC` | party arrives (second path) | plays music track 324; plays chat/dialogue text ID 0x000d; plays chat/dialogue text ID 0x000f; sets game flag 420; plays music track 268; tests game flag 420 |
| block 859 (x 27, y 26) | `0x12F8` | wall clicked | puts item 53 (Great axe "Master") on an empty cursor; puts item 248 (Oil Flask) on an empty cursor; puts item 215 (Bannon's reserve) on an empty cursor; puts item 189 (Small Key) on an empty cursor; puts item 269 (Guardian) on an empty cursor |
| block 861 (x 29, y 26) | `0x12DF` | wall clicked | operates the door switch at block 828 with action 0 |
| block 887 (x 23, y 27) | `0x0E0F` | wall clicked | operates the door switch at block 856 with action 1; plays chat/dialogue text ID 0x0018; sets game flag 403; tests game flag 402 |
| block 891 (x 27, y 27) | `0x12E6` | bits 0x400 (no engine caller found) | no action summarized |
| block 902 (x 6, y 28) | `0x112C` | party arrives (second path) | sets all four walls of block 934 to type 1; checks the north wall of block 934; plays a sound (ID 38) |
| block 920 (x 24, y 28) | `0x1114` | party arrives (second path), item put down | removes monsters from block 920; sets game flag 583; moves items from block 920 to level 26, block 211; tests game flag 582 |
| block 933 (x 5, y 29) | `0x0957` | wall clicked | sets all four walls of block 934 to type 0; plays chat/dialogue text ID 0x001d; checks the north wall of block 934; plays a sound (ID 38) |
| block 939 (x 11, y 29) | `0x06D5` | wall clicked | sets the east wall of block 906 to type 31; checks the east wall of block 906; plays a sound (ID 38) |
| block 942 (x 14, y 29) | `0x1371` | monster leaves | delete monsters from block; tests game flag 408 |
| block 953 (x 25, y 29) | `0x1465` | wall clicked | plays chat/dialogue text ID 0x0020 |
| block 964 (x 4, y 30) | `0x092F` | wall clicked | sets all four walls of block 996 to type 0; plays chat/dialogue text ID 0x001d; checks the north wall of block 996; plays a sound (ID 38) |
| block 995 (x 3, y 31) | `0x097F` | party arrives (second path) | sets all four walls of block 996 to type 1; checks the north wall of block 996; plays a sound (ID 38) |
| block 1009 (x 17, y 31) | `0x06C8` | party steps in, party arrives (second path), item put down | moves items from block 1009 to level 22, block 59 |
| `0x400` level loaded | `0x05A6` | — | sets music theme 268; sets script timer 0 to 7200 ticks; sets script timer 1 to 10800 ticks |
| `0x401` script timer 0 | `0x061A` | — | places a monster of type slot 1 on block 659 in mode 4; places a monster of type slot 1 on block 344 in mode 4; places a monster of type slot 1 on block 732 in mode 4; places a monster of type slot 2 on block 12 in mode 4; places a monster of type slot 2 on block 22 in mode 4; tests game flag 419; tests game flag 408 |
| `0x402` script timer 1 | `0x05B9` | — | places a monster of type slot 1 on block 591 in mode 4; places a monster of type slot 1 on block 520 in mode 4; tests game flag 419; tests game flag 408 |
| `0x404` a monster died | `0x059A` | — | clears game flag 577; loads monster sprites NECROSAP.SHP into slot 1 |

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
