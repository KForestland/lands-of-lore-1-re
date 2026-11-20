# Level 28

Made by `tools/level_report.py` from `LEVEL28.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 28](../PROGRESSION.md#level-28) and [item, spell and creature numbers](../NUMBERS.md).

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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL28.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CIMMERIA; loads monster sprites MANTHA.SHP into slot 0; loads monster sprites DETHDISK.SHP into slot 1; defines monster type 1; defines monster type 2; requests engine global change, selector 11, operands 0, 0 |
| INI entry 1 (runs when the level loads) | `0x00BA` | — | places a monster of type slot 2 on block 902 in mode 3; places a monster of type slot 1 on block 974 in mode 3; places a monster of type slot 2 on block 248 in mode 3; places a monster of type slot 2 on block 245 in mode 3; places a monster of type slot 2 on block 235 in mode 3; places a monster of type slot 1 on block 590 in mode 3; places a monster of type slot 2 on block 654 in mode 3; places a monster of type slot 2 on block 529 in mode 3 … |

### LEVEL28.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 12 (x 12, y 0) | `0x09D7` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 44 (x 12, y 1) | `0x09A6` | party arrives (second path) | creates item type 11 and returns its handle; launches a projectile from block 12 in direction 2; checks the north wall of block 75; plays a sound (ID 18) at block 74 |
| block 45 (x 13, y 1) | `0x09CC` | wall clicked | toggles the east wall of block 107 between types 31 and 1; plays a sound (ID 38) |
| block 74 (x 10, y 2) | `0x099F` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 75 (x 11, y 2) | `0x0998` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 75 to type 28; checks the south wall of block 75; plays a sound (ID 80) |
| block 77 (x 13, y 2) | `0x097B` | party arrives (second path) | creates item type 10 and returns its handle; launches a projectile from block 75 in direction 1; plays a sound (ID 18) at block 74 |
| block 78 (x 14, y 2) | `0x0971` | wall clicked | sets all four walls of block 78 to type 0; plays a sound (ID 38) |
| block 108 (x 12, y 3) | `0x09DE` | party arrives (second path) | creates item type 14 and returns its handle; launches a projectile from block 108 in direction 0; checks the east wall of block 107; plays a sound (ID 18) at block 140 |
| block 140 (x 12, y 4) | `0x0A05` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 143 (x 15, y 4) | `0x095D` | wall clicked | operates the door switch at block 207 with action 0; block door |
| block 169 (x 9, y 5) | `0x0A2B` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 169, facing ?; removes monsters from block 169; sets game flag 46; moves items from block 169 to level 27, block 169; checks the north wall of block 169 |
| block 171 (x 11, y 5) | `0x0A4A` | party arrives (second path) | sets all four walls of block 169 to type 0; sets all four walls of block 169 to type 42; removes monsters from block 169; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 169, facing ?; moves items from block 169 to level 27, block 169; sets game flag 46 … |
| block 180 (x 20, y 5) | `0x094B` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 181 (x 21, y 5) | `0x0901` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 181 to type 28; creates item type 11 and returns its handle; launches a projectile from block 181 in direction 1; launches a projectile from block 187 in direction 3; checks the south wall of block 181; plays a sound (ID 80); checks the north wall of block 186; plays a sound (ID 18) at block 180 … |
| block 186 (x 26, y 5) | `0x08B0` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 186 to type 28; creates item type 11 and returns its handle; launches a projectile from block 181 in direction 1; launches a projectile from block 187 in direction 3; checks the south wall of block 186; plays a sound (ID 80); checks the north wall of block 181; plays a sound (ID 18) at block 180 … |
| block 188 (x 28, y 5) | `0x08FA` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 202 (x 10, y 6) | `0x0A35` | wall clicked | sets all four walls of block 169 to type 0; sets all four walls of block 169 to type 42; removes monsters from block 169; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 169, facing ?; moves items from block 169 to level 27, block 169; sets game flag 46 … |
| block 207 (x 15, y 6) | `0x0967` | wall clicked | operates the door switch at block 143 with action 0; block door |
| block 214 (x 22, y 6) | `0x0952` | wall clicked | sets all four walls of block 180 to type 0; plays a sound (ID 38) |
| block 217 (x 25, y 6) | `0x0833` | wall clicked | plays chat/dialogue text ID 0x002a |
| block 246 (x 22, y 7) | `0x0842` | wall clicked | puts item 123 (Westwood stick) on an empty cursor; puts item 144 (Aegis great helm) on an empty cursor; puts item 217 (Aloe) on an empty cursor; sets game flag 436; checks the south wall of block 96; tests game flag 436 |
| block 247 (x 23, y 7) | `0x088A` | bits 0x400 (no engine caller found) | sets game flag 436; checks the south wall of block 96; tests game flag 436 |
| block 278 (x 22, y 8) | `0x07ED` | wall clicked | plays chat/dialogue text ID 0x002a; sets game flag 438 |
| block 329 (x 9, y 10) | `0x0BB3` | wall clicked | loads cut-scene ?.TIM into slot ?; loads cut-scene ?.TIM into slot 0; sets the south wall of block 258 to type ?; sets the south wall of block 258 to type 0; sets the south wall of block 258 to type 1; sets the south wall of block 258 to type 2; sets the south wall of block 258 to type 3; sets the south wall of block 258 to type 4 … |
| block 335 (x 15, y 10) | `0x0A0C` | party arrives (second path) | creates item type 11 and returns its handle; launches a projectile from block 330 in direction 1; plays a sound (ID 18) at block 329 |
| block 339 (x 19, y 10) | `0x0829` | wall clicked | operates the door switch at block 338 with action 0; plays a sound (ID 30) |
| block 341 (x 21, y 10) | `0x081F` | wall clicked | operates the door switch at block 372 with action 0; plays a sound (ID 30) |
| block 343 (x 23, y 10) | `0x07DA` | wall clicked | operates the door switch at block 342 with action 0; tests game flag 438; plays a sound (ID 30) |
| block 352 (x 0, y 11) | `0x0A9D` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 359 (x 7, y 11) | `0x0A5F` | party arrives (second path) | creates item type 10 and returns its handle; launches a projectile from block 353 in direction 1; plays a sound (ID 18) at block 329 |
| block 374 (x 22, y 11) | `0x0805` | party steps in, party arrives (second path), item put down | checks the north wall of block 374 |
| block 375 (x 23, y 11) | `0x0812` | wall clicked | sets all four walls of block 374 to type 0; sets all four walls of block 374 to type 37; removes monsters from block 374; moves items from block 374 to level 28, block 556; requests engine global change, selector 1, operands 0, ?; requests engine global change, selector 0, operands 0, 556; checks the north wall of block 374; plays a sound (ID 73) |
| block 388 (x 4, y 12) | `0x0A7E` | party arrives (second path) | creates item type 9 and returns its handle; launches a projectile from block 452 in direction 0; plays a sound (ID 69) at block 484 |
| block 427 (x 11, y 13) | `0x1C50` | party arrives (second path), wall clicked | deals damage to the party (amount ?); move party |
| block 451 (x 3, y 14) | `0x1C57` | party arrives (second path), wall clicked | deals damage to the party (amount ?); move party |
| block 484 (x 4, y 15) | `0x0AA4` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 487 (x 7, y 15) | `0x0B25` | wall clicked | plays chat/dialogue text ID 0x002a |
| block 491 (x 11, y 15) | `0x1591` | wall clicked | sets the south wall of block 258 to type 0; sets the north wall of block 257 to type 9; sets the south wall of block 258 to type 9; sets the north wall of block 257 to type ?; deletes the held item; sets the north wall of block 257 to type 14; sets the south wall of block 258 to type 14; requests engine global change, selector 0, operands 0, 521 … |
| block 516 (x 4, y 16) | `0x0AD8` | wall clicked | sets all four walls of block 518 to type 0; plays a sound (ID 38) |
| block 517 (x 5, y 16) | `0x0AB9` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); sets all four walls of block 517 to type 0; moves the party to level 26, block 517, facing ?; removes monsters from block 517; sets game flag 46; moves items from block 517 to level 26, block 517; checks the north wall of block 517 |
| block 519 (x 7, y 16) | `0x0AE3` | party arrives (second path) | creates item type 11 and returns its handle; launches a projectile from block 615 in direction 0; tests game flag 439; plays a sound (ID 18) at block 647 |
| block 521 (x 9, y 16) | `0x11F2` | party steps in | sets the north wall of block 257 to type 1; sets all four walls of block 492 to type 0; sets all four walls of block 525 to type 0; sets the south wall of block 258 to type 0; sets game flag 453; requests engine global change, selector 0, operands 0, 521; requests engine global change, selector 1, operands 0, 1; plays music track 274 … |
| block 522 (x 10, y 16) | `0x13CB` | wall clicked | sets the south wall of block 258 to type 9; sets the south wall of block 258 to type 14; sets the north wall of block 257 to type 8; sets the north wall of block 257 to type 7; sets the north wall of block 257 to type 6; sets the north wall of block 257 to type 5; sets the north wall of block 257 to type 4; sets the north wall of block 257 to type 3 … |
| block 523 (x 11, y 16) | `0x1968` | wall clicked | requests engine global change, selector 0, operands 0, 520; requests engine global change, selector 1, operands 0, 1; plays music track 306; sets game flag 592; plays chat/dialogue text ID 0x0014; plays a sound (ID 30); tests game flag 592 |
| block 549 (x 5, y 17) | `0x0AC3` | wall clicked | sets all four walls of block 517 to type 0; sets all four walls of block 517 to type 42; removes monsters from block 517; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 26, block 517, facing ?; moves items from block 517 to level 26, block 517; sets game flag 46 … |
| block 550 (x 6, y 17) | `0x0B12` | wall clicked | sets game flag 439 |
| block 552 (x 8, y 17) | `0x0B19` | wall clicked | toggles all four walls of block 583 between types 0 and 1; plays a sound (ID 38) |
| block 555 (x 11, y 17) | `0x19D4` | wall clicked | sets the north wall of block 257 to type 17; deletes the held item; sets the north wall of block 257 to type 15; sets the south wall of block 258 to type 0; sets the south wall of block 258 to type 9; sets the north wall of block 257 to type 16; places item 281 (Shard of truth) on block 520; gives item 281 (Shard of truth) if inventory placement succeeds … |
| block 602 (x 26, y 18) | `0x1C5E` | party arrives (second path), wall clicked | deals damage to the party (amount ?); move party |
| block 618 (x 10, y 19) | `0x0B41` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 618, facing ?; removes monsters from block 618; sets game flag 46; moves items from block 618 to level 27, block 618; checks the north wall of block 618 |
| block 620 (x 12, y 19) | `0x0B4B` | wall clicked, thrown item hits | sets all four walls of block 681 to type 0; sets all four walls of block 681 to type 37; removes monsters from block 681; moves items from block 681 to level 28, block 681; requests engine global change, selector 1, operands 0, ?; requests engine global change, selector 0, operands 0, 681; checks the north wall of block 681; plays a sound (ID 73) |
| block 644 (x 4, y 20) | `0x0AAB` | wall clicked | block door |
| block 647 (x 7, y 20) | `0x0B0B` | wall clicked | plays chat/dialogue text ID 0x002c |
| block 650 (x 10, y 20) | `0x0B58` | item put down, item taken | sets all four walls of block 618 to type 0; sets all four walls of block 618 to type 42; removes monsters from block 618; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 618, facing ?; moves items from block 618 to level 27, block 618; sets game flag 46 … |
| block 652 (x 12, y 20) | `0x0B8A` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 652 to type 28; sets all four walls of block 649 to type 0; sets all four walls of block 649 to type 42; removes monsters from block 649; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 27, block 649, facing ?; moves items from block 649 to level 27, block 649 … |
| block 657 (x 17, y 20) | `0x0BA6` | party steps in, party arrives (second path), item put down | moves items from block 657 to level 29, block 721 |
| block 681 (x 9, y 21) | `0x0B34` | party steps in, party arrives (second path), item put down | checks the north wall of block 681 |
| block 702 (x 30, y 21) | `0x07C0` | wall clicked | plays chat/dialogue text ID 0x002a |
| block 712 (x 8, y 22) | `0x0675` | item put down | sets the south wall of block 712 to type 1; moves items from block 712 to level 642, block 28; plays a sound (ID 38) |
| block 753 (x 17, y 23) | `0x0734` | bits 0x400 (no engine caller found) | sets game flag 434; checks the south wall of block 32; tests game flag 434 |
| block 754 (x 18, y 23) | `0x06F7` | wall clicked | puts item 229 (Cloud ring) on an empty cursor; puts item 69 (Great bow "Darkness") on an empty cursor; sets game flag 434; checks the south wall of block 32; tests game flag 434 |
| block 816 (x 16, y 25) | `0x06EC` | wall clicked | sets all four walls of block 816 to type 1; plays a sound (ID 38) |
| block 822 (x 22, y 25) | `0x07B2` | wall clicked | plays chat/dialogue text ID 0x002a |
| block 829 (x 29, y 25) | `0x07CE` | wall clicked | toggles the north wall of block 828 between types 31 and 2; plays a sound (ID 38) |
| block 836 (x 4, y 26) | `0x0667` | party arrives (second path) | no action summarized |
| block 838 (x 6, y 26) | `0x0669` | party arrives (second path), party leaves (second path) | toggles all four walls of block 839 between types 0 and 1; plays a sound (ID 38) |
| block 868 (x 4, y 27) | `0x0660` | wall clicked | operates the door switch at block 932 with action 0 |
| block 904 (x 8, y 28) | `0x0642` | party steps in, party arrives (second path), item put down | moves items from block 904 to level 27, block 904 |
| block 950 (x 22, y 29) | `0x075A` | wall clicked | toggles the north wall of block 1014 between types 31 and 1; plays a sound (ID 38) |
| block 963 (x 3, y 30) | `0x0659` | wall clicked | plays chat/dialogue text ID 0x002b |
| block 972 (x 12, y 30) | `0x06C6` | bits 0x400 (no engine caller found) | sets game flag 433; checks the south wall of block 0; tests game flag 433 |
| block 973 (x 13, y 30) | `0x068A` | wall clicked | puts item 109 (Staff "Gustavus") on an empty cursor; puts item 45 (Dagger "Riposte") on an empty cursor; sets game flag 433; checks the south wall of block 0; tests game flag 433 |
| block 987 (x 27, y 30) | `0x07A2` | bits 0x400 (no engine caller found) | no action summarized |
| block 988 (x 28, y 30) | `0x0766` | wall clicked | puts item 279 (Bracers of Defense) on an empty cursor; puts item 270 (Ace of Infinity) on an empty cursor; puts item 272 (Ace of Oblivion) on an empty cursor; gives 500 crown(s) |
| block 999 (x 7, y 31) | `0x064F` | wall clicked | operates the door switch at block 932 with action 0; plays a sound (ID 30) |
| `0x400` level loaded | `0x04CA` | — | sets music theme 306; sets script timer 0 to 120 ticks; sets script timer 1 to 3600 ticks; sets script timer 2 to 10 ticks |
| `0x401` script timer 0 | `0x04E0` | — | creates item type 9 and returns its handle; launches a projectile from block 964 in direction 1; plays a sound (ID 69) at block 964 |
| `0x402` script timer 1 | `0x0509` | — | places a monster of type slot 1 on block 930 in mode 4; places a monster of type slot 2 on block 916 in mode 4; places a monster of type slot 1 on block 282 in mode 4; places a monster of type slot 1 on block 515 in mode 4; checks the north wall of block 932 |
| `0x403` script timer 2 | `0x0551` | — | update block animations2; sets script timer 2 to ? ticks; tests game flag 474; checks the north wall of block 301; checks the east wall of block 260; checks the north wall of block 739; checks the east wall of block 545; checks the east wall of block 933 … |

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
