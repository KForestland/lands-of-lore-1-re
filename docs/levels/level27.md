# Level 27

Made by `tools/level_report.py` from `LEVEL27.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 11 = CIMMERIA (decorations `CIMMERIA.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CIMMERIA (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 856 | — | — |  | 0x80 | 63 |
| 1 | 1472 | 1 | 4 |  | 0x07 | 255 |
| 2 | 1488 | 2 | 5 |  | 0x07 | 255 |
| 3 | 37 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 5 | 3 | 4 |  | 0xaf | 13 |
| 12 | 2 | 3 | 4 |  | 0x98 | 13 |
| 18 | 4 | 3 | 4 |  | 0xaf | 13 |
| 23 | 4 | 4 | 4 |  | 0x84 | 25 |
| 24 | 4 | 5 | 4 |  | 0x84 | 26 |
| 27 | 16 | — | 15 |  | 0x80 | 10 |
| 29 | 1 | 1 | 20 | 2 lever (to on) | 0x07 | 207 |
| 31 | 1 | 2 | 6 | 6 niche | 0x87 | 14 |
| 32 | 1 | 2 | 11 | 1 clickable wall | 0x07 | 210 |
| 36 | 8 | 2 | 5 |  | 0x84 | 214 |
| 38 | 7 | 2 | 41 | 2 lever (to on) | 0x07 | 207 |
| 40 | 6 | 2 | 18 | 2 lever (to on) | 0x07 | 207 |
| 42 | 76 | — | 17 |  | 0x80 | 11 |
| 43 | 1 | 2 | 45 | 1 clickable wall | 0x07 | 207 |
| 44 | 47 | 1 | 37 |  | 0x07 | 255 |
| 51 | 1 | 2 | 22 | 2 lever (to on) | 0x07 | 207 |
| 53 | 1 | 1 | 24 | 2 lever (to on) | 0x07 | 207 |
| 55 | 2 | 1 | 26 | 2 lever (to on) | 0x07 | 207 |
| 57 | 1 | 2 | 28 | 2 lever (to on) | 0x07 | 207 |
| 59 | 1 | 2 | 30 | 2 lever (to on) | 0x07 | 207 |
| 61 | 1 | 2 | 32 | 2 lever (to on) | 0x07 | 207 |
| 67 | 4 | — | 1 | 1 clickable wall | 0x07 | 63 |
| 70 | 1 | 2 | 36 | 1 clickable wall | 0x07 | 255 |
| 74 | 26 | 6 | 47 | 6 niche | 0x87 | 255 |
| 75 | 4 | 2 | 53 | 1 clickable wall | 0x07 | 255 |
| 76 | 18 | 1 | 61 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 40 (x 8, y 1) | south | 40 | lever (to on) |
| 43 (x 11, y 1) | south | 74 | niche |
| 45 (x 13, y 1) | east | 70 | clickable wall |
| 71 (x 7, y 2) | east | 51 | lever (to on) |
| 73 (x 9, y 2) | west | 76 | clickable wall |
| 74 (x 10, y 2) | east | 74 | niche |
| 76 (x 12, y 2) | west | 74 | niche |
| 77 (x 13, y 2) | south | 40 | lever (to on) |
| 81 (x 17, y 2) | south | 40 | lever (to on) |
| 83 (x 19, y 2) | south | 76 | clickable wall |
| 112 (x 16, y 3) | west | 76 | clickable wall |
| 116 (x 20, y 3) | south | 74 | niche |
| 133 (x 5, y 4) | south | 32 | clickable wall |
| 134 (x 6, y 4) | east | 76 | clickable wall |
| 149 (x 21, y 4) | west | 74 | niche |
| 172 (x 12, y 5) | south | 76 | clickable wall |
| 180 (x 20, y 5) | north | 74 | niche |
| 195 (x 3, y 6) | north | 3 | door / door switch |
| 195 (x 3, y 6) | south | 3 | door / door switch |
| 196 (x 4, y 6) | south | 75 | clickable wall |
| 226 (x 2, y 7) | east | 38 | lever (to on) |
| 230 (x 6, y 7) | west | 43 | clickable wall |
| 233 (x 9, y 7) | north | 38 | lever (to on) |
| 236 (x 12, y 7) | north | 3 | door / door switch |
| 236 (x 12, y 7) | south | 3 | door / door switch |
| 239 (x 15, y 7) | north | 3 | door / door switch |
| 239 (x 15, y 7) | south | 3 | door / door switch |
| 241 (x 17, y 7) | north | 76 | clickable wall |
| 244 (x 20, y 7) | east | 3 | door / door switch |
| 244 (x 20, y 7) | west | 3 | door / door switch |
| 264 (x 8, y 8) | east | 3 | door / door switch |
| 264 (x 8, y 8) | west | 3 | door / door switch |
| 274 (x 18, y 8) | east | 3 | door / door switch |
| 274 (x 18, y 8) | west | 3 | door / door switch |
| 276 (x 20, y 8) | west | 38 | lever (to on) |
| 277 (x 21, y 8) | east | 74 | niche |
| 279 (x 23, y 8) | west | 74 | niche |
| 290 (x 2, y 9) | east | 75 | clickable wall |
| 292 (x 4, y 9) | south | 29 | lever (to on) |
| 310 (x 22, y 9) | north | 74 | niche |
| 326 (x 6, y 10) | east | 3 | door / door switch |
| 326 (x 6, y 10) | west | 3 | door / door switch |
| 332 (x 12, y 10) | north | 53 | lever (to on) |
| 338 (x 18, y 10) | east | 40 | lever (to on) |
| 341 (x 21, y 10) | east | 3 | door / door switch |
| 341 (x 21, y 10) | west | 3 | door / door switch |
| 343 (x 23, y 10) | east | 3 | door / door switch |
| 343 (x 23, y 10) | west | 3 | door / door switch |
| 347 (x 27, y 10) | west | 76 | clickable wall |
| 361 (x 9, y 11) | north | 3 | door / door switch |
| 361 (x 9, y 11) | south | 3 | door / door switch |
| 364 (x 12, y 11) | south | 76 | clickable wall |
| 369 (x 17, y 11) | north | 3 | door / door switch |
| 369 (x 17, y 11) | south | 3 | door / door switch |
| 373 (x 21, y 11) | south | 75 | clickable wall |
| 377 (x 25, y 11) | north | 67 | clickable wall |
| 377 (x 25, y 11) | east | 67 | clickable wall |
| 377 (x 25, y 11) | south | 67 | clickable wall |
| 377 (x 25, y 11) | west | 67 | clickable wall |
| 388 (x 4, y 12) | east | 3 | door / door switch |
| 388 (x 4, y 12) | west | 3 | door / door switch |
| 398 (x 14, y 12) | east | 76 | clickable wall |
| 411 (x 27, y 12) | west | 76 | clickable wall |
| 427 (x 11, y 13) | north | 3 | door / door switch |
| 427 (x 11, y 13) | south | 3 | door / door switch |
| 434 (x 18, y 13) | north | 3 | door / door switch |
| 434 (x 18, y 13) | south | 3 | door / door switch |
| 441 (x 25, y 13) | north | 76 | clickable wall |
| 488 (x 8, y 15) | north | 3 | door / door switch |
| 488 (x 8, y 15) | south | 3 | door / door switch |
| 489 (x 9, y 15) | south | 74 | niche |
| 519 (x 7, y 16) | east | 74 | niche |
| 523 (x 11, y 16) | north | 40 | lever (to on) |
| 528 (x 16, y 16) | north | 3 | door / door switch |
| 528 (x 16, y 16) | south | 3 | door / door switch |
| 530 (x 18, y 16) | north | 3 | door / door switch |
| 530 (x 18, y 16) | south | 3 | door / door switch |
| 554 (x 10, y 17) | west | 74 | niche |
| 559 (x 15, y 17) | east | 74 | niche |
| 561 (x 17, y 17) | east | 74 | niche |
| 561 (x 17, y 17) | west | 74 | niche |
| 563 (x 19, y 17) | west | 74 | niche |
| 584 (x 8, y 18) | north | 74 | niche |
| 585 (x 9, y 18) | north | 74 | niche |
| 592 (x 16, y 18) | north | 74 | niche |
| 594 (x 18, y 18) | north | 74 | niche |
| 615 (x 7, y 19) | south | 75 | clickable wall |
| 619 (x 11, y 19) | south | 38 | lever (to on) |
| 621 (x 13, y 19) | south | 38 | lever (to on) |
| 655 (x 15, y 20) | east | 3 | door / door switch |
| 659 (x 19, y 20) | south | 76 | clickable wall |
| 684 (x 12, y 21) | north | 38 | lever (to on) |
| 686 (x 14, y 21) | north | 38 | lever (to on) |
| 731 (x 27, y 22) | west | 76 | clickable wall |
| 748 (x 12, y 23) | west | 76 | clickable wall |
| 761 (x 25, y 23) | east | 3 | door / door switch |
| 761 (x 25, y 23) | west | 3 | door / door switch |
| 786 (x 18, y 24) | north | 55 | lever (to on) |
| 793 (x 25, y 24) | east | 74 | niche |
| 795 (x 27, y 24) | west | 74 | niche |
| 813 (x 13, y 25) | east | 31 | niche |
| 823 (x 23, y 25) | north | 76 | clickable wall |
| 826 (x 26, y 25) | north | 74 | niche |
| 836 (x 4, y 26) | east | 76 | clickable wall |
| 845 (x 13, y 26) | east | 55 | lever (to on) |
| 850 (x 18, y 26) | south | 57 | lever (to on) |
| 880 (x 16, y 27) | east | 74 | niche |
| 906 (x 10, y 28) | north | 61 | lever (to on) |
| 912 (x 16, y 28) | east | 76 | clickable wall |
| 915 (x 19, y 28) | west | 74 | niche |
| 933 (x 5, y 29) | east | 76 | clickable wall |
| 945 (x 17, y 29) | north | 74 | niche |
| 971 (x 11, y 30) | west | 40 | lever (to on) |
| 1002 (x 10, y 31) | north | 59 | lever (to on) |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL27.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CIMMERIA; loads monster sprites TCABAL.SHP into slot 0; loads monster sprites HATCHETS.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 499; places a monster (slot 2) on block 496; places a monster (slot 1) on block 429; places a monster (slot 2) on block 374; places a monster (slot 1) on block 344; places a monster (slot 1) on block 934; places a monster (slot 1) on block 938; places a monster (slot 2) on block 266 … |

### LEVEL27.INF

| Entry | Events | What it does |
|---|---|---|
| block 40 (x 8, y 1) | wall clicked | toggles the west wall of block 73 between types 31 and 1; plays a sound |
| block 45 (x 13, y 1) | wall clicked | gives item 73 (Great sword "Doom"); deals damage; sets game flag 431; a character speaks; tests game flag 431 |
| block 71 (x 7, y 2) | wall clicked | sets the west wall of block 104 to type 0; sets the west wall of block 104 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 104; moves objects from block 104 to block 104; sets game flag 46; checks a wall of block 73 … |
| block 72 (x 8, y 2) | party arrives (second path) | sets the west wall of block 104 to type 0; sets the west wall of block 104 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 104; moves objects from block 104 to block 104; sets game flag 46; checks a wall of block 104 … |
| block 77 (x 13, y 2) | wall clicked, item put down, thrown item hits | operates the door at block 141 |
| block 81 (x 17, y 2) | wall clicked, item put down, thrown item hits | operates the door at block 145 |
| block 104 (x 8, y 3) | party arrives (second path), item put down | sets the west wall of block 200 to type 0; sets the west wall of block 203 to type 0; drops the party through a pit; deals damage; sets the west wall of block 104 to type 0; moves the party to level 26, block 104; sets game flag 46; checks a wall of block 104 |
| block 133 (x 5, y 4) | wall clicked | gives item 38 (Bow "Tempest"); gives item 216 (Salve); gives item 230 (Zephyr ring); gives item 215 (Bannon's reserve); sets game flag 427; checks a wall of block 0; tests game flag 427 |
| block 165 (x 5, y 5) | bits 0x400 (no engine caller found) | sets game flag 427; checks a wall of block 0; tests game flag 427 |
| block 202 (x 10, y 6) | party arrives (second path) | sets the west wall of block 200 to type 1; sets the west wall of block 203 to type 1; checks a wall of block 200; plays a sound |
| block 205 (x 13, y 6) | party arrives (second path) | places a monster (slot 1) on block 109; make item; give item to monster; sets game flag 428; tests game flag 428 |
| block 209 (x 17, y 6) | party arrives (second path) | places a monster (slot 1) on block 113; make item; give item to monster; sets game flag 432; tests game flag 432 |
| block 226 (x 2, y 7) | wall clicked | sets/clears game flag 425; tests game flag 425 |
| block 230 (x 6, y 7) | wall clicked | operates the door at block 197; a character speaks |
| block 233 (x 9, y 7) | wall clicked | operates the door at block 169 |
| block 236 (x 12, y 7) | wall clicked | sets game flag 430; block door; clears game flag 430; tests game flag 430 |
| block 276 (x 20, y 8) | wall clicked | sets the west wall of block 403 to type 1; sets the east wall of block 403 to type 29; checks a wall of block 403; plays a sound |
| block 292 (x 4, y 9) | wall clicked | clears game flag 425 |
| block 301 (x 13, y 9) | party steps in, party arrives (second path), item put down | checks a wall of block 301 |
| block 323 (x 3, y 10) | party arrives (second path) | sets game flag 425 |
| block 332 (x 12, y 10) | wall clicked | sets the west wall of block 301 to type 0; operates the door at block 301; sets the west wall of block 301 to type 37; moves objects from block 301 to block 730; checks a wall of block 301; plays a sound; set global var |
| block 338 (x 18, y 10) | wall clicked | operates the door at block 341; starts cut-scene ?.TIM; starts cut-scene ESCAPE.TIM; sets the west wall of block 377 to type 69; starts a dialogue; a character speaks; sets game flag 450; sets game flag 451 … |
| block 343 (x 23, y 10) | wall clicked | block door; checks a wall of block 341 |
| block 361 (x 9, y 11) | wall clicked | places a monster (slot 1) on block 331; a character speaks; block door |
| block 377 (x 25, y 11) | wall clicked | starts cut-scene ESCAPE.TIM; sets the west wall of block 377 to type 69; delete hand item; sets game flag 451; a character speaks; sets game flag 450; tests game flag 451; tests game flag 452 … |
| block 403 (x 19, y 12) | wall clicked | sets the west wall of block 403 to type 0; plays a sound |
| block 469 (x 21, y 14) | party steps in, party arrives (second path), item put down | moves objects from block 469 to block 501 |
| block 523 (x 11, y 16) | wall clicked | places a monster (slot 2) on block 459; plays a sound |
| block 619 (x 11, y 19) | wall clicked | plays a sound |
| block 621 (x 13, y 19) | wall clicked | plays a sound |
| block 647 (x 7, y 20) | party arrives (second path) | character surprise feedback; move party |
| block 648 (x 8, y 20) | party arrives (second path) | character surprise feedback; move party |
| block 650 (x 10, y 20) | party steps in, party arrives (second path), item put down | moves objects from block 650 to block 744; moves objects from block 650 to block 503; moves objects from block 650 to block 730; checks a wall of block 621; checks a wall of block 619; plays a sound |
| block 652 (x 12, y 20) | party arrives (second path) | starts cut-scene AUTOMAP.TIM; starts cut-scene AUTOMAP2.TIM; palette flash; sets game flag 252; clears game flag 252; set global var; tests game flag 252 |
| block 653 (x 13, y 20) | party arrives (second path) | starts cut-scene AUTOMAP.TIM; starts cut-scene AUTOMAP2.TIM; sets game flag 252; clears game flag 252; set global var; tests game flag 252 |
| block 654 (x 14, y 20) | party arrives (second path) | operates the door at block 655 |
| block 677 (x 5, y 21) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 677 to type 0; moves the party to level 26, block 677; sets game flag 46; checks a wall of block 677 |
| block 678 (x 6, y 21) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 678 to type 28; sets the west wall of block 810 to type 0; sets the west wall of block 810 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 810; moves objects from block 810 to block 810; sets game flag 46 … |
| block 679 (x 7, y 21) | party arrives (second path) | character surprise feedback; move party |
| block 680 (x 8, y 21) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 680 to type 0; moves the party to level 26, block 680; sets game flag 46; checks a wall of block 680 |
| block 681 (x 9, y 21) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 681 to type 0; moves the party to level 26, block 681; sets game flag 46; checks a wall of block 681 |
| block 682 (x 10, y 21) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 682 to type 28; sets the west wall of block 742 to type 0; sets the west wall of block 742 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 742; moves objects from block 742 to block 742; sets game flag 46 … |
| block 683 (x 11, y 21) | party steps in, party arrives (second path), item put down | moves objects from block 683 to block 744; moves objects from block 683 to block 503; moves objects from block 683 to block 730; checks a wall of block 684; checks a wall of block 686; checks a wall of block 619; plays a sound |
| block 684 (x 12, y 21) | wall clicked | plays a sound |
| block 686 (x 14, y 21) | wall clicked | plays a sound |
| block 709 (x 5, y 22) | party arrives (second path) | character surprise feedback; move party |
| block 710 (x 6, y 22) | party arrives (second path) | character surprise feedback; move party |
| block 711 (x 7, y 22) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 711 to type 0; moves the party to level 26, block 711; sets game flag 46; checks a wall of block 711 |
| block 712 (x 8, y 22) | party arrives (second path) | character surprise feedback; move party |
| block 713 (x 9, y 22) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 713 to type 0; moves the party to level 26, block 713; sets game flag 46; checks a wall of block 713 |
| block 714 (x 10, y 22) | party arrives (second path) | character surprise feedback; move party |
| block 715 (x 11, y 22) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 715 to type 0; moves the party to level 26, block 715; sets game flag 46; checks a wall of block 715 |
| block 741 (x 5, y 23) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 741 to type 0; moves the party to level 26, block 741; sets game flag 46; checks a wall of block 741 |
| block 742 (x 6, y 23) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 742 to type 0; moves the party to level 26, block 742; sets game flag 46; checks a wall of block 742 |
| block 743 (x 7, y 23) | party arrives (second path) | character surprise feedback; move party |
| block 745 (x 9, y 23) | party arrives (second path) | character surprise feedback; move party |
| block 746 (x 10, y 23) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 746 to type 0; moves the party to level 26, block 746; sets game flag 46; checks a wall of block 746 |
| block 747 (x 11, y 23) | party arrives (second path) | character surprise feedback; move party |
| block 774 (x 6, y 24) | party arrives (second path) | character surprise feedback; move party |
| block 775 (x 7, y 24) | party arrives (second path) | character surprise feedback; move party |
| block 776 (x 8, y 24) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 776 to type 0; moves the party to level 26, block 776; sets game flag 46; checks a wall of block 776 |
| block 778 (x 10, y 24) | party arrives (second path) | character surprise feedback; move party |
| block 786 (x 18, y 24) | wall clicked | sets the west wall of block 818 to type 0; sets the west wall of block 818 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 818; moves objects from block 818 to block 818; sets game flag 46; checks a wall of block 786 … |
| block 805 (x 5, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 805 to type 0; moves the party to level 26, block 805; sets game flag 46; checks a wall of block 805 |
| block 806 (x 6, y 25) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 806 to type 28; sets the west wall of block 746 to type 0; sets the west wall of block 746 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 746; moves objects from block 746 to block 746; sets game flag 46 … |
| block 807 (x 7, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 807 to type 0; moves the party to level 26, block 807; sets game flag 46; checks a wall of block 807 |
| block 808 (x 8, y 25) | party arrives (second path) | character surprise feedback; move party |
| block 809 (x 9, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 809 to type 0; moves the party to level 26, block 809; sets game flag 46; checks a wall of block 809 |
| block 810 (x 10, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 810 to type 0; moves the party to level 26, block 810; sets game flag 46; checks a wall of block 810 |
| block 811 (x 11, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 811 to type 0; moves the party to level 26, block 811; sets game flag 46; checks a wall of block 811 |
| block 813 (x 13, y 25) | item put down | sets the east wall of block 813 to type 1; places item 243 (Coin Purse) on block 813; delete level item; plays a sound |
| block 816 (x 16, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 816 to type 0; moves the party to level 26, block 816; sets the west wall of block 816 to type 42; sets game flag 46; moves objects from block 816 to block 816; checks a wall of block 816 … |
| block 818 (x 18, y 25) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 818 to type 0; moves the party to level 26, block 818; sets game flag 46; checks a wall of block 818 |
| block 839 (x 7, y 26) | party arrives (second path) | character surprise feedback; move party |
| block 840 (x 8, y 26) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 840 to type 0; moves the party to level 26, block 840; sets game flag 46; checks a wall of block 840 |
| block 841 (x 9, y 26) | party arrives (second path) | character surprise feedback; move party |
| block 842 (x 10, y 26) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 842 to type 28; sets the west wall of block 840 to type 0; sets the west wall of block 840 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 840; moves objects from block 840 to block 840; sets game flag 46 … |
| block 845 (x 13, y 26) | wall clicked | toggles the east wall of block 813 between types 31 and 1; plays a sound |
| block 850 (x 18, y 26) | wall clicked | sets the west wall of block 818 to type 0; sets the west wall of block 818 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 818; moves objects from block 818 to block 818; sets game flag 46; checks a wall of block 786 … |
| block 904 (x 8, y 28) | party arrives (second path) | starts cut-scene AUTOMAP.TIM; starts cut-scene AUTOMAP2.TIM; sets game flag 252; clears game flag 252; set global var; tests game flag 252 |
| block 906 (x 10, y 28) | wall clicked | sets the west wall of block 906 to type 0; plays a sound |
| block 936 (x 8, y 29) | party steps in, party arrives (second path), item put down | moves objects from block 936 to block 936 |
| block 970 (x 10, y 30) | party arrives (second path) | sets the west wall of block 906 to type 1; sets the north wall of block 906 to type 29; checks a wall of block 906; plays a sound |
| block 971 (x 11, y 30) | wall clicked | toggles the east wall of block 969 between types 31 and 1; plays a sound |
| block 1002 (x 10, y 31) | wall clicked | sets the west wall of block 906 to type 0; checks a wall of block 969; plays a sound |
| `0x400` level loaded | — | starts script timer 1; starts script timer 0; starts script timer 2 |
| `0x401` script timer 0 | — | sets the west wall of block 259 to type 71; sets the west wall of block 259 to type 12; sets the west wall of block 259 to type 72; sets game flag 426; clears game flag 426; tests game flag 425; checks a wall of block 259; plays a sound … |
| `0x402` script timer 1 | — | places a monster (slot 2) on block 135; places a monster (slot 2) on block 147; places a monster (slot 1) on block 331; places a monster (slot 2) on block 783; sets game flag 429; clears game flag 429; tests game flag 429; checks a wall of block 145 |
| `0x403` script timer 2 | — | update block animations2; starts script timer 2; tests game flag 474; checks a wall of block 134; checks a wall of block 172; checks a wall of block 241; checks a wall of block 83; checks a wall of block 364 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 20 | Cobra figurine | 27 | 73 |
| INI entry 1 (runs when the level loads) | 21 | Dragon figurine | 27 | 969 |
| INI entry 1 (runs when the level loads) | 189 | Small Key | 27 | 336 |
| block 813 (x 13, y 25) | 243 | Coin Purse | 27 | 813 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 499 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 499 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 496 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 429 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 429 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 374 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 344 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 344 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 934 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 938 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 266 | 3 | 2 | 3 |
| block 205 (x 13, y 6) | 109 | 2 | 1 | 4 |
| block 205 (x 13, y 6) | 109 | 2 | 1 | 4 |
| block 209 (x 17, y 6) | 113 | 2 | 1 | 4 |
| block 209 (x 17, y 6) | 113 | 2 | 1 | 4 |
| block 361 (x 9, y 11) | 331 | 3 | 1 | 4 |
| block 361 (x 9, y 11) | 331 | 3 | 1 | 4 |
| block 523 (x 11, y 16) | 459 | 2 | 2 | 4 |
| block 523 (x 11, y 16) | 459 | 2 | 2 | 4 |
| block 523 (x 11, y 16) | 459 | 2 | 2 | 4 |
| block 523 (x 11, y 16) | 459 | 2 | 2 | 4 |
| `0x402` script timer 1 | 135 | 1 | 2 | 4 |
| `0x402` script timer 1 | 147 | 0 | 2 | 4 |
| `0x402` script timer 1 | 147 | 0 | 2 | 4 |
| `0x402` script timer 1 | 331 | 3 | 1 | 4 |
| `0x402` script timer 1 | 783 | 2 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 25, y 11 | 3 | x 25, y 11 | 0x4204 | CRYSTAL BALL |

## Text shown by the scripts (ids only)

- Level text file `LEVEL27.<lang>`: 10 ids: 6, 7, 8, 9, 10, 16, 17, 22, 24, 25.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL27.ENG --index N`.
