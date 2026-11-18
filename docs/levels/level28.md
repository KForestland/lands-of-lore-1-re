# Level 28

Made by `tools/level_report.py` from `LEVEL28.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 11 = CIMMERIA (decorations `CIMMERIA.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CIMMERIA (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1304 | — | — |  | 0x80 | 63 |
| 1 | 1217 | 1 | 4 |  | 0x07 | 255 |
| 2 | 1230 | 2 | 5 |  | 0x07 | 255 |
| 3 | 48 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 16 | 3 | 4 |  | 0xaf | 13 |
| 23 | 4 | 4 | 4 |  | 0x84 | 25 |
| 24 | 4 | 5 | 4 |  | 0x84 | 26 |
| 27 | 20 | — | 15 |  | 0x80 | 10 |
| 29 | 2 | 1 | 20 | 2 lever (to on) | 0x07 | 207 |
| 31 | 4 | 2 | 6 | 6 niche | 0x87 | 14 |
| 32 | 4 | 2 | 11 | 1 clickable wall | 0x07 | 210 |
| 36 | 20 | — | 48 |  | 0x07 | 63 |
| 38 | 6 | 2 | 41 | 2 lever (to on) | 0x07 | 207 |
| 40 | 2 | 2 | 18 | 2 lever (to on) | 0x07 | 207 |
| 42 | 8 | — | 17 |  | 0x80 | 11 |
| 43 | 5 | 2 | 45 | 1 clickable wall | 0x07 | 207 |
| 44 | 64 | 1 | 37 |  | 0x07 | 255 |
| 45 | 8 | 1 | 75 | 1 clickable wall | 0x07 | 255 |
| 47 | 1 | 1 | 87 | 1 clickable wall | 0x07 | 255 |
| 48 | 5 | 1 | 93 | 1 clickable wall | 0x07 | 255 |
| 50 | 1 | 1 | 105 | 1 clickable wall | 0x07 | 255 |
| 51 | 1 | 2 | 22 | 2 lever (to on) | 0x07 | 207 |
| 53 | 2 | 1 | 24 | 2 lever (to on) | 0x07 | 207 |
| 55 | 2 | 1 | 26 | 2 lever (to on) | 0x07 | 207 |
| 57 | 1 | 2 | 34 | 2 lever (to on) | 0x07 | 207 |
| 59 | 1 | 2 | 30 | 2 lever (to on) | 0x07 | 207 |
| 61 | 1 | 2 | 32 | 2 lever (to on) | 0x07 | 207 |
| 63 | 9 | 1 | 16 | 1 clickable wall | 0x07 | 255 |
| 67 | 20 | 6 | 54 | 1 clickable wall | 0x07 | 255 |
| 68 | 20 | — | 55 | 1 clickable wall | 0x80 | 255 |
| 69 | 12 | — | 56 | 1 clickable wall | 0x84 | 255 |
| 70 | 3 | 2 | 50 | 1 clickable wall | 0x07 | 255 |
| 71 | 5 | 2 | 51 | 1 clickable wall | 0x07 | 255 |
| 72 | 3 | 2 | 52 | 1 clickable wall | 0x07 | 255 |
| 73 | 4 | — | 60 | 1 clickable wall | 0x06 | 255 |
| 75 | 3 | 2 | 53 | 1 clickable wall | 0x07 | 255 |
| 76 | 35 | 1 | 61 | 1 clickable wall | 0x07 | 255 |
| 77 | 1 | 1 | 62 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 8 (x 8, y 0) | south | 67 | clickable wall |
| 12 (x 12, y 0) | south | 63 | clickable wall |
| 34 (x 2, y 1) | south | 45 | clickable wall |
| 35 (x 3, y 1) | south | 67 | clickable wall |
| 36 (x 4, y 1) | south | 47 | clickable wall |
| 42 (x 10, y 1) | west | 45 | clickable wall |
| 45 (x 13, y 1) | west | 57 | lever (to on) |
| 47 (x 15, y 1) | south | 76 | clickable wall |
| 65 (x 1, y 2) | east | 67 | clickable wall |
| 69 (x 5, y 2) | west | 48 | clickable wall |
| 70 (x 6, y 2) | east | 76 | clickable wall |
| 72 (x 8, y 2) | north | 68 | clickable wall |
| 72 (x 8, y 2) | east | 68 | clickable wall |
| 72 (x 8, y 2) | south | 68 | clickable wall |
| 72 (x 8, y 2) | west | 68 | clickable wall |
| 74 (x 10, y 2) | west | 71 | clickable wall |
| 78 (x 14, y 2) | east | 53 | lever (to on) |
| 97 (x 1, y 3) | east | 45 | clickable wall |
| 99 (x 3, y 3) | north | 68 | clickable wall |
| 99 (x 3, y 3) | east | 68 | clickable wall |
| 99 (x 3, y 3) | south | 68 | clickable wall |
| 99 (x 3, y 3) | west | 68 | clickable wall |
| 101 (x 5, y 3) | west | 75 | clickable wall |
| 106 (x 10, y 3) | west | 67 | clickable wall |
| 129 (x 1, y 4) | east | 67 | clickable wall |
| 133 (x 5, y 4) | west | 50 | clickable wall |
| 135 (x 7, y 4) | north | 3 | door / door switch |
| 135 (x 7, y 4) | south | 3 | door / door switch |
| 137 (x 9, y 4) | south | 76 | clickable wall |
| 140 (x 12, y 4) | north | 63 | clickable wall |
| 143 (x 15, y 4) | north | 3 | door / door switch |
| 143 (x 15, y 4) | south | 3 | door / door switch |
| 161 (x 1, y 5) | east | 70 | clickable wall |
| 165 (x 5, y 5) | east | 3 | door / door switch |
| 165 (x 5, y 5) | west | 3 | door / door switch |
| 172 (x 12, y 5) | west | 76 | clickable wall |
| 173 (x 13, y 5) | east | 45 | clickable wall |
| 180 (x 20, y 5) | east | 63 | clickable wall |
| 188 (x 28, y 5) | west | 63 | clickable wall |
| 193 (x 1, y 6) | east | 67 | clickable wall |
| 200 (x 8, y 6) | south | 76 | clickable wall |
| 202 (x 10, y 6) | north | 38 | lever (to on) |
| 205 (x 13, y 6) | south | 76 | clickable wall |
| 207 (x 15, y 6) | north | 3 | door / door switch |
| 207 (x 15, y 6) | south | 3 | door / door switch |
| 210 (x 18, y 6) | north | 76 | clickable wall |
| 214 (x 22, y 6) | north | 38 | lever (to on) |
| 217 (x 25, y 6) | east | 43 | clickable wall |
| 229 (x 5, y 7) | north | 68 | clickable wall |
| 229 (x 5, y 7) | east | 68 | clickable wall |
| 229 (x 5, y 7) | south | 68 | clickable wall |
| 229 (x 5, y 7) | west | 68 | clickable wall |
| 244 (x 20, y 7) | east | 72 | clickable wall |
| 246 (x 22, y 7) | east | 32 | clickable wall |
| 260 (x 4, y 8) | east | 76 | clickable wall |
| 265 (x 9, y 8) | north | 76 | clickable wall |
| 275 (x 19, y 8) | south | 76 | clickable wall |
| 278 (x 22, y 8) | south | 43 | clickable wall |
| 283 (x 27, y 8) | west | 76 | clickable wall |
| 292 (x 4, y 9) | south | 76 | clickable wall |
| 300 (x 12, y 9) | south | 76 | clickable wall |
| 301 (x 13, y 9) | north | 76 | clickable wall |
| 303 (x 15, y 9) | north | 3 | door / door switch |
| 303 (x 15, y 9) | south | 3 | door / door switch |
| 322 (x 2, y 10) | south | 75 | clickable wall |
| 325 (x 5, y 10) | south | 76 | clickable wall |
| 329 (x 9, y 10) | east | 63 | clickable wall |
| 339 (x 19, y 10) | north | 38 | lever (to on) |
| 341 (x 21, y 10) | west | 38 | lever (to on) |
| 343 (x 23, y 10) | north | 38 | lever (to on) |
| 344 (x 24, y 10) | north | 3 | door / door switch |
| 344 (x 24, y 10) | south | 3 | door / door switch |
| 352 (x 0, y 11) | east | 63 | clickable wall |
| 360 (x 8, y 11) | west | 76 | clickable wall |
| 362 (x 10, y 11) | north | 3 | door / door switch |
| 362 (x 10, y 11) | south | 3 | door / door switch |
| 365 (x 13, y 11) | north | 3 | door / door switch |
| 365 (x 13, y 11) | south | 3 | door / door switch |
| 375 (x 23, y 11) | west | 61 | lever (to on) |
| 399 (x 15, y 12) | west | 71 | clickable wall |
| 410 (x 26, y 12) | west | 76 | clickable wall |
| 416 (x 0, y 13) | east | 71 | clickable wall |
| 423 (x 7, y 13) | east | 67 | clickable wall |
| 427 (x 11, y 13) | north | 69 | clickable wall |
| 427 (x 11, y 13) | east | 69 | clickable wall |
| 427 (x 11, y 13) | south | 69 | clickable wall |
| 427 (x 11, y 13) | west | 69 | clickable wall |
| 431 (x 15, y 13) | west | 67 | clickable wall |
| 433 (x 17, y 13) | north | 3 | door / door switch |
| 433 (x 17, y 13) | south | 3 | door / door switch |
| 437 (x 21, y 13) | north | 3 | door / door switch |
| 437 (x 21, y 13) | south | 3 | door / door switch |
| 439 (x 23, y 13) | north | 3 | door / door switch |
| 439 (x 23, y 13) | south | 3 | door / door switch |
| 451 (x 3, y 14) | north | 69 | clickable wall |
| 451 (x 3, y 14) | east | 69 | clickable wall |
| 451 (x 3, y 14) | south | 69 | clickable wall |
| 451 (x 3, y 14) | west | 69 | clickable wall |
| 458 (x 10, y 14) | north | 45 | clickable wall |
| 460 (x 12, y 14) | north | 76 | clickable wall |
| 461 (x 13, y 14) | north | 67 | clickable wall |
| 484 (x 4, y 15) | north | 63 | clickable wall |
| 486 (x 6, y 15) | west | 45 | clickable wall |
| 487 (x 7, y 15) | south | 43 | clickable wall |
| 505 (x 25, y 15) | south | 76 | clickable wall |
| 507 (x 27, y 15) | south | 75 | clickable wall |
| 516 (x 4, y 16) | east | 29 | lever (to on) |
| 521 (x 9, y 16) | north | 73 | clickable wall |
| 521 (x 9, y 16) | east | 73 | clickable wall |
| 521 (x 9, y 16) | south | 73 | clickable wall |
| 521 (x 9, y 16) | west | 73 | clickable wall |
| 526 (x 14, y 16) | south | 76 | clickable wall |
| 531 (x 19, y 16) | east | 76 | clickable wall |
| 545 (x 1, y 17) | east | 76 | clickable wall |
| 549 (x 5, y 17) | north | 55 | lever (to on) |
| 550 (x 6, y 17) | east | 51 | lever (to on) |
| 552 (x 8, y 17) | west | 40 | lever (to on) |
| 557 (x 13, y 17) | east | 3 | door / door switch |
| 557 (x 13, y 17) | west | 3 | door / door switch |
| 563 (x 19, y 17) | west | 70 | clickable wall |
| 587 (x 11, y 18) | south | 76 | clickable wall |
| 592 (x 16, y 18) | north | 45 | clickable wall |
| 595 (x 19, y 18) | south | 76 | clickable wall |
| 602 (x 26, y 18) | north | 69 | clickable wall |
| 602 (x 26, y 18) | east | 69 | clickable wall |
| 602 (x 26, y 18) | south | 69 | clickable wall |
| 602 (x 26, y 18) | west | 69 | clickable wall |
| 616 (x 8, y 19) | east | 3 | door / door switch |
| 616 (x 8, y 19) | west | 3 | door / door switch |
| 620 (x 12, y 19) | west | 40 | lever (to on) |
| 622 (x 14, y 19) | north | 3 | door / door switch |
| 622 (x 14, y 19) | south | 3 | door / door switch |
| 625 (x 17, y 19) | north | 3 | door / door switch |
| 625 (x 17, y 19) | south | 3 | door / door switch |
| 626 (x 18, y 19) | east | 67 | clickable wall |
| 642 (x 2, y 20) | south | 31 | niche |
| 644 (x 4, y 20) | north | 3 | door / door switch |
| 644 (x 4, y 20) | south | 3 | door / door switch |
| 647 (x 7, y 20) | north | 63 | clickable wall |
| 650 (x 10, y 20) | east | 31 | niche |
| 661 (x 21, y 20) | east | 3 | door / door switch |
| 661 (x 21, y 20) | west | 3 | door / door switch |
| 668 (x 28, y 20) | east | 77 | clickable wall |
| 685 (x 13, y 21) | south | 76 | clickable wall |
| 686 (x 14, y 21) | north | 45 | clickable wall |
| 690 (x 18, y 21) | east | 67 | clickable wall |
| 702 (x 30, y 21) | west | 43 | clickable wall |
| 705 (x 1, y 22) | east | 72 | clickable wall |
| 709 (x 5, y 22) | west | 67 | clickable wall |
| 711 (x 7, y 22) | south | 76 | clickable wall |
| 712 (x 8, y 22) | south | 31 | niche |
| 719 (x 15, y 22) | west | 67 | clickable wall |
| 725 (x 21, y 22) | south | 67 | clickable wall |
| 729 (x 25, y 22) | north | 3 | door / door switch |
| 729 (x 25, y 22) | south | 3 | door / door switch |
| 738 (x 2, y 23) | north | 67 | clickable wall |
| 739 (x 3, y 23) | north | 76 | clickable wall |
| 748 (x 12, y 23) | east | 3 | door / door switch |
| 748 (x 12, y 23) | west | 3 | door / door switch |
| 754 (x 18, y 23) | west | 32 | clickable wall |
| 773 (x 5, y 24) | east | 67 | clickable wall |
| 777 (x 9, y 24) | east | 3 | door / door switch |
| 777 (x 9, y 24) | west | 3 | door / door switch |
| 782 (x 14, y 24) | north | 68 | clickable wall |
| 782 (x 14, y 24) | east | 68 | clickable wall |
| 782 (x 14, y 24) | south | 68 | clickable wall |
| 782 (x 14, y 24) | west | 68 | clickable wall |
| 787 (x 19, y 24) | east | 67 | clickable wall |
| 791 (x 23, y 24) | west | 76 | clickable wall |
| 795 (x 27, y 24) | east | 48 | clickable wall |
| 799 (x 31, y 24) | west | 48 | clickable wall |
| 806 (x 6, y 25) | north | 72 | clickable wall |
| 811 (x 11, y 25) | north | 3 | door / door switch |
| 811 (x 11, y 25) | south | 3 | door / door switch |
| 813 (x 13, y 25) | north | 67 | clickable wall |
| 814 (x 14, y 25) | south | 76 | clickable wall |
| 816 (x 16, y 25) | south | 55 | lever (to on) |
| 818 (x 18, y 25) | south | 76 | clickable wall |
| 820 (x 20, y 25) | north | 31 | niche |
| 822 (x 22, y 25) | south | 43 | clickable wall |
| 824 (x 24, y 25) | south | 76 | clickable wall |
| 827 (x 27, y 25) | south | 67 | clickable wall |
| 829 (x 29, y 25) | north | 59 | lever (to on) |
| 859 (x 27, y 26) | north | 68 | clickable wall |
| 859 (x 27, y 26) | east | 68 | clickable wall |
| 859 (x 27, y 26) | south | 68 | clickable wall |
| 859 (x 27, y 26) | west | 68 | clickable wall |
| 861 (x 29, y 26) | west | 48 | clickable wall |
| 868 (x 4, y 27) | south | 53 | lever (to on) |
| 879 (x 15, y 27) | west | 71 | clickable wall |
| 883 (x 19, y 27) | west | 70 | clickable wall |
| 884 (x 20, y 27) | south | 76 | clickable wall |
| 894 (x 30, y 27) | west | 76 | clickable wall |
| 922 (x 26, y 28) | east | 3 | door / door switch |
| 922 (x 26, y 28) | west | 3 | door / door switch |
| 925 (x 29, y 28) | west | 67 | clickable wall |
| 933 (x 5, y 29) | east | 76 | clickable wall |
| 938 (x 10, y 29) | north | 3 | door / door switch |
| 938 (x 10, y 29) | south | 3 | door / door switch |
| 950 (x 22, y 29) | south | 29 | lever (to on) |
| 953 (x 25, y 29) | north | 3 | door / door switch |
| 953 (x 25, y 29) | south | 3 | door / door switch |
| 956 (x 28, y 29) | north | 48 | clickable wall |
| 963 (x 3, y 30) | east | 63 | clickable wall |
| 973 (x 13, y 30) | west | 32 | clickable wall |
| 977 (x 17, y 30) | north | 71 | clickable wall |
| 988 (x 28, y 30) | west | 32 | clickable wall |
| 999 (x 7, y 31) | north | 38 | lever (to on) |
| 1013 (x 21, y 31) | north | 76 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL28.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CIMMERIA; loads monster sprites MANTHA.SHP into slot 0; loads monster sprites DETHDISK.SHP into slot 1; defines monster type 1; defines monster type 2; set global var |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 902; places a monster (slot 1) on block 974; places a monster (slot 2) on block 248; places a monster (slot 2) on block 245; places a monster (slot 2) on block 235; places a monster (slot 1) on block 590; places a monster (slot 2) on block 654; places a monster (slot 2) on block 529 … |

### LEVEL28.INF

| Entry | Events | What it does |
|---|---|---|
| block 12 (x 12, y 0) | wall clicked | a character speaks |
| block 44 (x 12, y 1) | party arrives (second path) | make item; play environmental sfx; launches a projectile; checks a wall of block 75 |
| block 45 (x 13, y 1) | wall clicked | toggles the east wall of block 107 between types 31 and 1; plays a sound |
| block 74 (x 10, y 2) | wall clicked | a character speaks |
| block 75 (x 11, y 2) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 75 to type 28; checks a wall of block 75; plays a sound |
| block 77 (x 13, y 2) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 78 (x 14, y 2) | wall clicked | sets the west wall of block 78 to type 0; plays a sound |
| block 108 (x 12, y 3) | party arrives (second path) | make item; play environmental sfx; launches a projectile; checks a wall of block 107 |
| block 140 (x 12, y 4) | wall clicked | a character speaks |
| block 143 (x 15, y 4) | wall clicked | operates the door at block 207; block door |
| block 169 (x 9, y 5) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 27, block 169; sets game flag 46; moves objects from block 169 to block 169; checks a wall of block 169 |
| block 171 (x 11, y 5) | party arrives (second path) | sets the west wall of block 169 to type 0; sets the west wall of block 169 to type 42; drops the party through a pit; deals damage; moves the party to level 27, block 169; moves objects from block 169 to block 169; sets game flag 46; checks a wall of block 169 … |
| block 180 (x 20, y 5) | wall clicked | a character speaks |
| block 181 (x 21, y 5) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 181 to type 28; make item; play environmental sfx; launches a projectile; checks a wall of block 181; plays a sound; checks a wall of block 186 |
| block 186 (x 26, y 5) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 186 to type 28; make item; play environmental sfx; launches a projectile; checks a wall of block 186; plays a sound; checks a wall of block 181 |
| block 188 (x 28, y 5) | wall clicked | a character speaks |
| block 202 (x 10, y 6) | wall clicked | sets the west wall of block 169 to type 0; sets the west wall of block 169 to type 42; drops the party through a pit; deals damage; moves the party to level 27, block 169; moves objects from block 169 to block 169; sets game flag 46; checks a wall of block 169 … |
| block 207 (x 15, y 6) | wall clicked | operates the door at block 143; block door |
| block 214 (x 22, y 6) | wall clicked | sets the west wall of block 180 to type 0; plays a sound |
| block 217 (x 25, y 6) | wall clicked | a character speaks |
| block 246 (x 22, y 7) | wall clicked | gives item 123 (Westwood stick); gives item 144 (Aegis great helm); gives item 217 (Aloe); sets game flag 436; checks a wall of block 96; tests game flag 436 |
| block 247 (x 23, y 7) | bits 0x400 (no engine caller found) | sets game flag 436; checks a wall of block 96; tests game flag 436 |
| block 278 (x 22, y 8) | wall clicked | a character speaks; sets game flag 438 |
| block 329 (x 9, y 10) | wall clicked | starts cut-scene ?.TIM; sets the south wall of block 258 to type ?; sets the south wall of block 258 to type 0; sets the south wall of block 258 to type 1; sets the south wall of block 258 to type 2; sets the south wall of block 258 to type 3; sets the south wall of block 258 to type 4; a character speaks … |
| block 335 (x 15, y 10) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 339 (x 19, y 10) | wall clicked | operates the door at block 338; plays a sound |
| block 341 (x 21, y 10) | wall clicked | operates the door at block 372; plays a sound |
| block 343 (x 23, y 10) | wall clicked | operates the door at block 342; tests game flag 438; plays a sound |
| block 352 (x 0, y 11) | wall clicked | a character speaks |
| block 359 (x 7, y 11) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 374 (x 22, y 11) | party steps in, party arrives (second path), item put down | checks a wall of block 374 |
| block 375 (x 23, y 11) | wall clicked | sets the west wall of block 374 to type 0; sets the west wall of block 374 to type 37; moves objects from block 374 to block 556; checks a wall of block 374; plays a sound; set global var |
| block 388 (x 4, y 12) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 427 (x 11, y 13) | party arrives (second path), wall clicked | deals damage; move party |
| block 451 (x 3, y 14) | party arrives (second path), wall clicked | deals damage; move party |
| block 484 (x 4, y 15) | wall clicked | a character speaks |
| block 487 (x 7, y 15) | wall clicked | a character speaks |
| block 491 (x 11, y 15) | wall clicked | sets the south wall of block 258 to type 0; sets the north wall of block 257 to type 9; sets the south wall of block 258 to type 9; sets the ? wall of block 525 to type 1; sets the north wall of block 257 to type ?; sets the north wall of block 257 to type 14; sets the south wall of block 258 to type 14; a character speaks … |
| block 516 (x 4, y 16) | wall clicked | sets the west wall of block 518 to type 0; plays a sound |
| block 517 (x 5, y 16) | party arrives (second path), item put down | drops the party through a pit; deals damage; sets the west wall of block 517 to type 0; moves the party to level 26, block 517; sets game flag 46; moves objects from block 517 to block 517; checks a wall of block 517 |
| block 519 (x 7, y 16) | party arrives (second path) | make item; play environmental sfx; launches a projectile; tests game flag 439 |
| block 521 (x 9, y 16) | party steps in | sets the north wall of block 257 to type 1; sets the west wall of block 492 to type 0; sets the west wall of block 525 to type 0; sets the south wall of block 258 to type 0; sets game flag 453; sets game flag 584; a character speaks; starts a dialogue … |
| block 522 (x 10, y 16) | wall clicked | sets the south wall of block 258 to type 9; sets the south wall of block 258 to type 14; sets the ? wall of block 492 to type ?; sets the north wall of block 257 to type 8; sets the north wall of block 257 to type 7; sets the north wall of block 257 to type 6; sets the north wall of block 257 to type 5; sets the north wall of block 257 to type 4 … |
| block 523 (x 11, y 16) | wall clicked | sets game flag 592; a character speaks; set global var; plays a sound; tests game flag 592 |
| block 549 (x 5, y 17) | wall clicked | sets the west wall of block 517 to type 0; sets the west wall of block 517 to type 42; drops the party through a pit; deals damage; moves the party to level 26, block 517; moves objects from block 517 to block 517; sets game flag 46; checks a wall of block 517 … |
| block 550 (x 6, y 17) | wall clicked | sets game flag 439 |
| block 552 (x 8, y 17) | wall clicked | toggles the west wall of block 583 between types 0 and 1; plays a sound |
| block 555 (x 11, y 17) | wall clicked | sets the north wall of block 257 to type 17; sets the north wall of block 257 to type 15; sets the south wall of block 258 to type 0; sets the south wall of block 258 to type 9; sets the north wall of block 257 to type 16; places item 281 (Shard of truth) on block 520; gives item 281 (Shard of truth); delete hand item … |
| block 602 (x 26, y 18) | party arrives (second path), wall clicked | deals damage; move party |
| block 618 (x 10, y 19) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 27, block 618; sets game flag 46; moves objects from block 618 to block 618; checks a wall of block 618 |
| block 620 (x 12, y 19) | wall clicked, thrown item hits | sets the west wall of block 681 to type 0; sets the west wall of block 681 to type 37; moves objects from block 681 to block 681; checks a wall of block 681; plays a sound; set global var |
| block 644 (x 4, y 20) | wall clicked | block door |
| block 647 (x 7, y 20) | wall clicked | a character speaks |
| block 650 (x 10, y 20) | item put down, item taken | sets the west wall of block 618 to type 0; sets the west wall of block 618 to type 42; drops the party through a pit; deals damage; moves the party to level 27, block 618; moves objects from block 618 to block 618; sets game flag 46; checks a wall of block 618 … |
| block 652 (x 12, y 20) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 652 to type 28; sets the west wall of block 649 to type 0; sets the west wall of block 649 to type 42; drops the party through a pit; deals damage; moves the party to level 27, block 649; moves objects from block 649 to block 649; sets game flag 46 … |
| block 657 (x 17, y 20) | party steps in, party arrives (second path), item put down | moves objects from block 657 to block 721 |
| block 681 (x 9, y 21) | party steps in, party arrives (second path), item put down | checks a wall of block 681 |
| block 702 (x 30, y 21) | wall clicked | a character speaks |
| block 712 (x 8, y 22) | item put down | sets the south wall of block 712 to type 1; moves objects from block 712 to block 28; plays a sound |
| block 753 (x 17, y 23) | bits 0x400 (no engine caller found) | sets game flag 434; checks a wall of block 32; tests game flag 434 |
| block 754 (x 18, y 23) | wall clicked | gives item 229 (Cloud ring); gives item 69 (Great bow "Darkness"); sets game flag 434; checks a wall of block 32; tests game flag 434 |
| block 816 (x 16, y 25) | wall clicked | sets the west wall of block 816 to type 1; plays a sound |
| block 822 (x 22, y 25) | wall clicked | a character speaks |
| block 829 (x 29, y 25) | wall clicked | toggles the north wall of block 828 between types 31 and 2; plays a sound |
| block 836 (x 4, y 26) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 838 (x 6, y 26) | party arrives (second path), party leaves (second path) | toggles the west wall of block 839 between types 0 and 1; plays a sound |
| block 868 (x 4, y 27) | wall clicked | operates the door at block 932 |
| block 904 (x 8, y 28) | party steps in, party arrives (second path), item put down | moves objects from block 904 to block 904 |
| block 950 (x 22, y 29) | wall clicked | toggles the north wall of block 1014 between types 31 and 1; plays a sound |
| block 963 (x 3, y 30) | wall clicked | a character speaks |
| block 972 (x 12, y 30) | bits 0x400 (no engine caller found) | sets game flag 433; checks a wall of block 0; tests game flag 433 |
| block 973 (x 13, y 30) | wall clicked | gives item 109 (Staff "Gustavus"); gives item 45 (Dagger "Riposte"); sets game flag 433; checks a wall of block 0; tests game flag 433 |
| block 987 (x 27, y 30) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 988 (x 28, y 30) | wall clicked | gives item 279 (Bracers of Defense); gives item 270 (Ace of Infinity); gives item 272 (Ace of Oblivion); gives 500 crown(s) |
| block 999 (x 7, y 31) | wall clicked | operates the door at block 932; plays a sound |
| `0x400` level loaded | — | starts script timer 0; starts script timer 1; starts script timer 2 |
| `0x401` script timer 0 | — | make item; play environmental sfx; launches a projectile |
| `0x402` script timer 1 | — | places a monster (slot 1) on block 930; places a monster (slot 2) on block 916; places a monster (slot 1) on block 282; places a monster (slot 1) on block 515; checks a wall of block 932 |
| `0x403` script timer 2 | — | update block animations2; starts script timer 2; tests game flag 474; checks a wall of block 301; checks a wall of block 260; checks a wall of block 739; checks a wall of block 545; checks a wall of block 933 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 127 | Trident "Plague" | 28 | 1014 |
| INI entry 1 (runs when the level loads) | 23 | Unicorn figurine | 28 | 828 |
| INI entry 1 (runs when the level loads) | 208 | Adder key | 28 | 107 |
| INI entry 1 (runs when the level loads) | 203 | Noir key | 28 | 642 |
| INI entry 1 (runs when the level loads) | 206 | Carrion key | 28 | 650 |
| block 555 (x 11, y 17) | 281 | Shard of truth | 28 | 520 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 902 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 974 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 248 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 245 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 235 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 590 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 654 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 529 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 593 | 0 | 1 | 3 |
| `0x402` script timer 1 | 930 | 0 | 1 | 4 |
| `0x402` script timer 1 | 916 | 2 | 2 | 4 |
| `0x402` script timer 1 | 282 | 0 | 1 | 4 |
| `0x402` script timer 1 | 515 | 3 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 9, y 16 | 4 | x 8, y 16 | 0x4205 | KING RICHARD |

## Text shown by the scripts (ids only)

- Level text file `LEVEL28.<lang>`: 42 ids: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 23, 24, 26, 28, 30, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL28.ENG --index N`.
