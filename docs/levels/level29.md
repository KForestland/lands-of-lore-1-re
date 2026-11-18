# Level 29

Made by `tools/level_report.py` from `LEVEL29.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 11 = CIMMERIA (decorations `CIMMERIA.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CIMMERIA (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1928 | — | — |  | 0x80 | 63 |
| 1 | 979 | 1 | 4 |  | 0x07 | 255 |
| 2 | 1008 | 2 | 5 |  | 0x07 | 255 |
| 3 | 12 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 1 | 3 | 4 |  | 0xaf | 13 |
| 24 | 4 | 5 | 4 |  | 0x84 | 26 |
| 27 | 8 | — | 15 |  | 0x80 | 10 |
| 29 | 7 | 1 | 20 | 2 lever (to on) | 0x07 | 207 |
| 32 | 4 | 2 | 11 | 1 clickable wall | 0x07 | 210 |
| 36 | 4 | 2 | 5 |  | 0x84 | 214 |
| 38 | 1 | 2 | 41 | 2 lever (to on) | 0x07 | 207 |
| 40 | 1 | 2 | 18 | 2 lever (to on) | 0x07 | 207 |
| 42 | 12 | — | 17 |  | 0x80 | 11 |
| 43 | 2 | 2 | 45 | 1 clickable wall | 0x07 | 207 |
| 44 | 14 | 1 | 37 |  | 0x07 | 255 |
| 45 | 38 | 1 | 75 | 1 clickable wall | 0x07 | 255 |
| 51 | 1 | 2 | 22 | 2 lever (to on) | 0x07 | 207 |
| 52 | 1 | 2 | 23 | 3 lever (to off) | 0x07 | 207 |
| 53 | 1 | 1 | 24 | 2 lever (to on) | 0x07 | 207 |
| 55 | 3 | 1 | 26 | 2 lever (to on) | 0x07 | 207 |
| 59 | 1 | 2 | 30 | 2 lever (to on) | 0x07 | 207 |
| 61 | 1 | 2 | 32 | 2 lever (to on) | 0x07 | 207 |
| 63 | 8 | 1 | 16 | 1 clickable wall | 0x07 | 255 |
| 67 | 2 | 6 | 54 | 1 clickable wall | 0x07 | 255 |
| 68 | 8 | — | 55 | 1 clickable wall | 0x80 | 255 |
| 69 | 12 | — | 56 | 1 clickable wall | 0x84 | 255 |
| 70 | 6 | 2 | 50 | 1 clickable wall | 0x07 | 255 |
| 71 | 4 | 2 | 51 | 1 clickable wall | 0x07 | 255 |
| 72 | 5 | 2 | 57 | 1 clickable wall | 0x07 | 255 |
| 75 | 20 | — | 67 | 1 clickable wall | 0x80 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 15 (x 15, y 0) | south | 45 | clickable wall |
| 23 (x 23, y 0) | south | 45 | clickable wall |
| 49 (x 17, y 1) | south | 71 | clickable wall |
| 97 (x 1, y 3) | east | 45 | clickable wall |
| 103 (x 7, y 3) | north | 75 | clickable wall |
| 103 (x 7, y 3) | east | 75 | clickable wall |
| 103 (x 7, y 3) | south | 75 | clickable wall |
| 103 (x 7, y 3) | west | 75 | clickable wall |
| 110 (x 14, y 3) | south | 45 | clickable wall |
| 133 (x 5, y 4) | east | 70 | clickable wall |
| 146 (x 18, y 4) | north | 45 | clickable wall |
| 151 (x 23, y 4) | east | 70 | clickable wall |
| 154 (x 26, y 4) | east | 45 | clickable wall |
| 168 (x 8, y 5) | south | 67 | clickable wall |
| 169 (x 9, y 5) | north | 45 | clickable wall |
| 191 (x 31, y 5) | west | 71 | clickable wall |
| 202 (x 10, y 6) | west | 67 | clickable wall |
| 204 (x 12, y 6) | north | 32 | clickable wall |
| 215 (x 23, y 6) | south | 45 | clickable wall |
| 231 (x 7, y 7) | east | 3 | door / door switch |
| 231 (x 7, y 7) | west | 3 | door / door switch |
| 233 (x 9, y 7) | north | 68 | clickable wall |
| 233 (x 9, y 7) | east | 68 | clickable wall |
| 233 (x 9, y 7) | south | 68 | clickable wall |
| 233 (x 9, y 7) | west | 68 | clickable wall |
| 241 (x 17, y 7) | east | 45 | clickable wall |
| 249 (x 25, y 7) | north | 32 | clickable wall |
| 250 (x 26, y 7) | east | 59 | lever (to on) |
| 259 (x 3, y 8) | north | 75 | clickable wall |
| 259 (x 3, y 8) | east | 75 | clickable wall |
| 259 (x 3, y 8) | south | 75 | clickable wall |
| 259 (x 3, y 8) | west | 75 | clickable wall |
| 261 (x 5, y 8) | west | 45 | clickable wall |
| 272 (x 16, y 8) | south | 70 | clickable wall |
| 276 (x 20, y 8) | north | 45 | clickable wall |
| 284 (x 28, y 8) | east | 45 | clickable wall |
| 294 (x 6, y 9) | north | 68 | clickable wall |
| 294 (x 6, y 9) | east | 68 | clickable wall |
| 294 (x 6, y 9) | south | 68 | clickable wall |
| 294 (x 6, y 9) | west | 68 | clickable wall |
| 299 (x 11, y 9) | east | 29 | lever (to on) |
| 309 (x 21, y 9) | south | 38 | lever (to on) |
| 314 (x 26, y 9) | south | 45 | clickable wall |
| 332 (x 12, y 10) | north | 53 | lever (to on) |
| 333 (x 13, y 10) | south | 45 | clickable wall |
| 334 (x 14, y 10) | north | 45 | clickable wall |
| 342 (x 22, y 10) | north | 75 | clickable wall |
| 342 (x 22, y 10) | east | 75 | clickable wall |
| 342 (x 22, y 10) | south | 75 | clickable wall |
| 342 (x 22, y 10) | west | 75 | clickable wall |
| 376 (x 24, y 11) | west | 45 | clickable wall |
| 394 (x 10, y 12) | north | 45 | clickable wall |
| 397 (x 13, y 12) | south | 45 | clickable wall |
| 398 (x 14, y 12) | south | 61 | lever (to on) |
| 402 (x 18, y 12) | east | 45 | clickable wall |
| 445 (x 29, y 13) | south | 32 | clickable wall |
| 446 (x 30, y 13) | north | 3 | door / door switch |
| 446 (x 30, y 13) | south | 3 | door / door switch |
| 450 (x 2, y 14) | north | 45 | clickable wall |
| 458 (x 10, y 14) | east | 45 | clickable wall |
| 472 (x 24, y 14) | north | 69 | clickable wall |
| 472 (x 24, y 14) | east | 69 | clickable wall |
| 472 (x 24, y 14) | south | 69 | clickable wall |
| 472 (x 24, y 14) | west | 69 | clickable wall |
| 490 (x 10, y 15) | east | 3 | door / door switch |
| 490 (x 10, y 15) | west | 3 | door / door switch |
| 503 (x 23, y 15) | north | 45 | clickable wall |
| 516 (x 4, y 16) | north | 45 | clickable wall |
| 517 (x 5, y 16) | south | 63 | clickable wall |
| 522 (x 10, y 16) | east | 45 | clickable wall |
| 537 (x 25, y 16) | north | 71 | clickable wall |
| 542 (x 30, y 16) | north | 45 | clickable wall |
| 568 (x 24, y 17) | south | 45 | clickable wall |
| 588 (x 12, y 18) | north | 45 | clickable wall |
| 590 (x 14, y 18) | north | 45 | clickable wall |
| 590 (x 14, y 18) | south | 43 | clickable wall |
| 591 (x 15, y 18) | south | 55 | lever (to on) |
| 592 (x 16, y 18) | south | 43 | clickable wall |
| 617 (x 9, y 19) | east | 32 | clickable wall |
| 628 (x 20, y 19) | north | 69 | clickable wall |
| 628 (x 20, y 19) | east | 69 | clickable wall |
| 628 (x 20, y 19) | south | 69 | clickable wall |
| 628 (x 20, y 19) | west | 69 | clickable wall |
| 632 (x 24, y 19) | north | 75 | clickable wall |
| 632 (x 24, y 19) | east | 75 | clickable wall |
| 632 (x 24, y 19) | south | 75 | clickable wall |
| 632 (x 24, y 19) | west | 75 | clickable wall |
| 640 (x 0, y 20) | east | 45 | clickable wall |
| 648 (x 8, y 20) | west | 63 | clickable wall |
| 665 (x 25, y 20) | north | 69 | clickable wall |
| 665 (x 25, y 20) | east | 69 | clickable wall |
| 665 (x 25, y 20) | south | 69 | clickable wall |
| 665 (x 25, y 20) | west | 69 | clickable wall |
| 675 (x 3, y 21) | north | 45 | clickable wall |
| 678 (x 6, y 21) | east | 70 | clickable wall |
| 687 (x 15, y 21) | north | 3 | door / door switch |
| 687 (x 15, y 21) | south | 3 | door / door switch |
| 728 (x 24, y 22) | east | 29 | lever (to on) |
| 728 (x 24, y 22) | south | 29 | lever (to on) |
| 728 (x 24, y 22) | west | 29 | lever (to on) |
| 737 (x 1, y 23) | north | 63 | clickable wall |
| 744 (x 8, y 23) | north | 29 | lever (to on) |
| 744 (x 8, y 23) | south | 29 | lever (to on) |
| 747 (x 11, y 23) | south | 71 | clickable wall |
| 750 (x 14, y 23) | south | 45 | clickable wall |
| 766 (x 30, y 23) | north | 75 | clickable wall |
| 766 (x 30, y 23) | east | 75 | clickable wall |
| 766 (x 30, y 23) | south | 75 | clickable wall |
| 766 (x 30, y 23) | west | 75 | clickable wall |
| 770 (x 2, y 24) | east | 45 | clickable wall |
| 803 (x 3, y 25) | north | 3 | door / door switch |
| 803 (x 3, y 25) | south | 3 | door / door switch |
| 807 (x 7, y 25) | east | 63 | clickable wall |
| 815 (x 15, y 25) | east | 63 | clickable wall |
| 833 (x 1, y 26) | east | 72 | clickable wall |
| 837 (x 5, y 26) | west | 72 | clickable wall |
| 843 (x 11, y 26) | west | 45 | clickable wall |
| 851 (x 19, y 26) | south | 55 | lever (to on) |
| 859 (x 27, y 26) | west | 45 | clickable wall |
| 861 (x 29, y 26) | east | 3 | door / door switch |
| 861 (x 29, y 26) | west | 3 | door / door switch |
| 871 (x 7, y 27) | east | 45 | clickable wall |
| 876 (x 12, y 27) | east | 55 | lever (to on) |
| 888 (x 24, y 27) | east | 40 | lever (to on) |
| 888 (x 24, y 27) | west | 63 | clickable wall |
| 891 (x 27, y 27) | east | 45 | clickable wall |
| 897 (x 1, y 28) | east | 72 | clickable wall |
| 901 (x 5, y 28) | west | 72 | clickable wall |
| 916 (x 20, y 28) | south | 70 | clickable wall |
| 921 (x 25, y 28) | east | 52 | lever (to off) |
| 926 (x 30, y 28) | west | 72 | clickable wall |
| 933 (x 5, y 29) | east | 45 | clickable wall |
| 935 (x 7, y 29) | east | 63 | clickable wall |
| 943 (x 15, y 29) | east | 63 | clickable wall |
| 987 (x 27, y 30) | east | 51 | lever (to on) |
| 991 (x 31, y 30) | west | 29 | lever (to on) |
| 1000 (x 8, y 31) | north | 70 | clickable wall |
| 1009 (x 17, y 31) | north | 45 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL29.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CIMMERIA; loads monster sprites TOAD.SHP into slot 0; defines monster type 1; loads monster sprites SCO_TOAD.SHP into slot 0; loads monster sprites TOAD.SHP into slot 1; defines monster type 2; loads monster sprites TOADSERP.SHP into slot 0; loads monster sprites VIPER.SHP into slot 1 … |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 2; places a monster (slot 1) on block 247; places a monster (slot 1) on block 257; places a monster (slot 1) on block 78; places a monster (slot 1) on block 123; places a monster (slot 1) on block 94; places a monster (slot 1) on block 4; places item 202 (Death Key) on block 211 … |

### LEVEL29.INF

| Entry | Events | What it does |
|---|---|---|
| block 76 (x 12, y 2) | party arrives (second path) | changes a monster |
| block 80 (x 16, y 2) | party arrives (second path) | changes a monster |
| block 89 (x 25, y 2) | party arrives (second path) | changes a monster |
| block 152 (x 24, y 4) | party arrives (second path) | changes a monster |
| block 172 (x 12, y 5) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 187 (x 27, y 5) | party arrives (second path) | changes a monster |
| block 190 (x 30, y 5) | party arrives (second path) | changes a monster |
| block 195 (x 3, y 6) | party arrives (second path) | changes a monster |
| block 204 (x 12, y 6) | wall clicked | gives item 182 (Silver Key); gives item 216 (Salve); gives 25 crown(s); sets game flag 470; checks a wall of block 64; tests game flag 470 |
| block 217 (x 25, y 6) | bits 0x400 (no engine caller found) | sets game flag 469; checks a wall of block 32; tests game flag 469 |
| block 229 (x 5, y 7) | party arrives (second path) | changes a monster |
| block 245 (x 21, y 7) | party arrives (second path) | changes a monster |
| block 249 (x 25, y 7) | wall clicked | gives item 78 (Halberd "Death's Hand"); gives item 160 (Aegis plate mail); gives 200 crown(s); sets game flag 469; checks a wall of block 32; tests game flag 469 |
| block 250 (x 26, y 7) | wall clicked | sets the west wall of block 252 to type 0; checks a wall of block 252; plays a sound |
| block 299 (x 11, y 9) | wall clicked | sets the west wall of block 268 to type 0; checks a wall of block 268; plays a sound |
| block 300 (x 12, y 9) | party arrives (second path) | sets the west wall of block 268 to type 1; sets the west wall of block 301 to type 1; plays a sound |
| block 309 (x 21, y 9) | wall clicked | toggles the west wall of block 373 between types 0 and 1; play environmental sfx |
| block 311 (x 23, y 9) | party arrives (second path) | changes a monster |
| block 322 (x 2, y 10) | party arrives (second path) | changes a monster |
| block 332 (x 12, y 10) | wall clicked | sets the west wall of block 301 to type 0; checks a wall of block 301; plays a sound |
| block 398 (x 14, y 12) | wall clicked | sets the west wall of block 398 to type 0; plays a sound |
| block 445 (x 29, y 13) | wall clicked | gives item 218 (Ginseng); gives item 146 (Helm "Talamar"); gives 100 crown(s); sets game flag 471; checks a wall of block 96; tests game flag 471 |
| block 472 (x 24, y 14) | party arrives (second path), wall clicked | deals damage; move party |
| block 477 (x 29, y 14) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 490 (x 10, y 15) | party arrives (second path) | places a monster (slot 1) on block 489; sets game flag 454; a character speaks; loads monster sprites SCO_TOAD.SHP into slot 0; loads monster sprites TOAD.SHP into slot 1; defines monster type 1; defines monster type 2; sets game flag 576 … |
| block 496 (x 16, y 15) | monster leaves | sets the west wall of block 497 to type 0; plays a sound |
| block 517 (x 5, y 16) | wall clicked | a character speaks |
| block 534 (x 22, y 16) | party arrives (second path), party leaves (second path) | sets the west wall of block 534 to type 28; sets the west wall of block 566 to type 2; checks a wall of block 534; plays a sound; checks a wall of block 566 |
| block 559 (x 15, y 17) | party arrives (second path) | operates the door at block 591; clears game flag 463; clears game flag 464; checks a wall of block 591 |
| block 590 (x 14, y 18) | wall clicked | a character speaks; sets game flag 472 |
| block 591 (x 15, y 18) | wall clicked | sets the north wall of block 591 to type 8; sets the south wall of block 591 to type 3; sets the east wall of block 591 to type 0; sets the west wall of block 591 to type 0; block door; checks a wall of block 591; plays a sound; tests game flag 472 … |
| block 592 (x 16, y 18) | wall clicked | a character speaks; sets game flag 473 |
| block 598 (x 22, y 18) | party arrives (second path) | character surprise feedback; move party |
| block 609 (x 1, y 19) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 617 (x 9, y 19) | wall clicked | gives item 27 (Arbalest "Eternity"); gives item 159 (Bastion plate mail); gives 500 crown(s); sets game flag 468; checks a wall of block 0; tests game flag 468 |
| block 618 (x 10, y 19) | bits 0x400 (no engine caller found) | sets game flag 468; checks a wall of block 0; tests game flag 468 |
| block 628 (x 20, y 19) | party arrives (second path), wall clicked | deals damage; move party |
| block 645 (x 5, y 20) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 648 (x 8, y 20) | wall clicked | a character speaks |
| block 665 (x 25, y 20) | party arrives (second path), wall clicked | deals damage; move party |
| block 689 (x 17, y 21) | party steps in, party arrives (second path), item put down | moves objects from block 680 to block 625 |
| block 709 (x 5, y 22) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 728 (x 24, y 22) | wall clicked | sets the west wall of block 728 to type 0; places a monster (slot 1) on block 728; suspend monster |
| block 737 (x 1, y 23) | wall clicked | a character speaks |
| block 744 (x 8, y 23) | wall clicked | sets the west wall of block 744 to type 0; places a monster (slot 1) on block 744; suspend monster |
| block 753 (x 17, y 23) | party arrives (second path) | sets the west wall of block 721 to type 1; starts a dialogue; a character speaks; checks a wall of block 721; plays a sound |
| block 807 (x 7, y 25) | wall clicked | a character speaks |
| block 815 (x 15, y 25) | wall clicked | a character speaks |
| block 833 (x 1, y 26) | wall clicked | a character speaks |
| block 834 (x 2, y 26) | item put down, item taken | sets the north wall of block 995 to type 31; sets the north wall of block 995 to type 1; clears game flag 460; sets game flag 460; play environmental sfx; tests game flag 459; tests game flag 460; tests game flag 462 … |
| block 836 (x 4, y 26) | item put down, item taken | sets the north wall of block 995 to type 31; sets the north wall of block 995 to type 1; clears game flag 459; sets game flag 459; play environmental sfx; tests game flag 459; tests game flag 460; tests game flag 462 … |
| block 837 (x 5, y 26) | wall clicked | a character speaks |
| block 840 (x 8, y 26) | party arrives (second path) | sets game flag 464 |
| block 841 (x 9, y 26) | party arrives (second path) | sets game flag 464 |
| block 842 (x 10, y 26) | party arrives (second path) | sets game flag 464 |
| block 844 (x 12, y 26) | party arrives (second path) | sets game flag 464 |
| block 845 (x 13, y 26) | party arrives (second path) | sets game flag 464 |
| block 846 (x 14, y 26) | party arrives (second path) | sets game flag 464 |
| block 848 (x 16, y 26) | party arrives (second path) | sets game flag 463 |
| block 849 (x 17, y 26) | party arrives (second path) | sets game flag 463 |
| block 851 (x 19, y 26) | wall clicked | toggles the north wall of block 915 between types 31 and 1; plays a sound |
| block 853 (x 21, y 26) | party arrives (second path) | sets game flag 463 |
| block 854 (x 22, y 26) | party arrives (second path) | sets game flag 463 |
| block 867 (x 3, y 27) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 867 to type 28; operates the door at block 803; checks a wall of block 867; plays a sound |
| block 871 (x 7, y 27) | wall clicked | toggles the west wall of block 874 between types 31 and 1; sets game flag 466; checks a wall of block 874; plays a sound |
| block 873 (x 9, y 27) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 28, block 873; sets game flag 46; moves objects from block 873 to block 873; checks a wall of block 873 |
| block 876 (x 12, y 27) | wall clicked | toggles the west wall of block 879 between types 31 and 1; sets game flag 467; checks a wall of block 879; plays a sound |
| block 878 (x 14, y 27) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 28, block 878; sets game flag 46; moves objects from block 878 to block 878; checks a wall of block 878 |
| block 888 (x 24, y 27) | wall clicked, thrown item hits | toggles the east wall of block 888 between types 40 and 41; sets/clears game flag 465; tests game flag 465 |
| block 889 (x 25, y 27) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 28, block 889; sets game flag 46; moves objects from block 889 to block 889; checks a wall of block 889 |
| block 897 (x 1, y 28) | wall clicked | a character speaks |
| block 898 (x 2, y 28) | item put down, item taken | sets the north wall of block 995 to type 31; sets the north wall of block 995 to type 1; clears game flag 461; sets game flag 461; play environmental sfx; tests game flag 459; tests game flag 460; tests game flag 462 … |
| block 900 (x 4, y 28) | item put down, item taken | sets the north wall of block 995 to type 31; sets the north wall of block 995 to type 1; clears game flag 462; sets game flag 462; play environmental sfx; tests game flag 459; tests game flag 460; tests game flag 462 … |
| block 901 (x 5, y 28) | wall clicked | a character speaks |
| block 904 (x 8, y 28) | party arrives (second path) | sets game flag 464 |
| block 905 (x 9, y 28) | party arrives (second path) | sets game flag 464 |
| block 906 (x 10, y 28) | party arrives (second path) | sets game flag 464 |
| block 908 (x 12, y 28) | party arrives (second path) | sets game flag 464 |
| block 909 (x 13, y 28) | party arrives (second path) | sets game flag 464 |
| block 910 (x 14, y 28) | party arrives (second path) | sets game flag 464 |
| block 912 (x 16, y 28) | party arrives (second path) | sets game flag 463 |
| block 913 (x 17, y 28) | party arrives (second path) | sets game flag 463 |
| block 917 (x 21, y 28) | party arrives (second path) | sets game flag 463 |
| block 918 (x 22, y 28) | party arrives (second path) | sets game flag 463 |
| block 920 (x 24, y 28) | wall clicked | sets the west wall of block 920 to type 0; sets the west wall of block 919 to type 1; sets the west wall of block 957 to type 0; plays a sound |
| block 921 (x 25, y 28) | wall clicked | sets the west wall of block 921 to type 0; sets the west wall of block 920 to type 1; sets the east wall of block 920 to type 53; plays a sound |
| block 926 (x 30, y 28) | wall clicked | a character speaks |
| block 935 (x 7, y 29) | wall clicked | a character speaks |
| block 943 (x 15, y 29) | wall clicked | a character speaks |
| block 987 (x 27, y 30) | wall clicked | sets the north wall of block 1021 to type 31; checks a wall of block 987; plays a sound |
| block 989 (x 29, y 30) | party arrives (second path) | sets the west wall of block 957 to type 1; sets the west wall of block 957 to type 0; checks a wall of block 1021; checks a wall of block 957; plays a sound |
| block 991 (x 31, y 30) | wall clicked | sets the north wall of block 1021 to type 1; checks a wall of block 1021; plays a sound |
| block 995 (x 3, y 31) | item taken | operates the door at block 803 |
| `0x400` level loaded | — | starts script timer 0; starts script timer 1; starts script timer 2 |
| `0x401` script timer 0 | — | deals damage; make item; play environmental sfx; launches a projectile; tests game flag 464; tests game flag 466; tests game flag 467; tests game flag 463 … |
| `0x402` script timer 1 | — | update block animations2; set global script var; plays a sound |
| `0x403` script timer 2 | — | update block animations2; starts script timer 2; checks a wall of block 588; checks a wall of block 590; checks a wall of block 458; checks a wall of block 397; checks a wall of block 522; checks a wall of block 376 … |
| `0x404` a monster died | — | places a monster (slot 2) on block ?; places a monster (slot 1) on block ?; a character speaks; play end sequence; suspend monster; release monster shapes; loads monster sprites TOADSERP.SHP into slot 0; loads monster sprites VIPER.SHP into slot 1 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 202 | Death Key | 29 | 211 |
| INI entry 1 (runs when the level loads) | 205 | Oily key | 29 | 200 |
| INI entry 1 (runs when the level loads) | 22 | Humanoid figurine | 29 | 1021 |
| INI entry 1 (runs when the level loads) | 179 | Gold Key | 29 | 915 |
| INI entry 1 (runs when the level loads) | 204 | Dull key | 29 | 995 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 2 | 2 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 247 | 3 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 257 | 1 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 78 | 0 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 123 | 2 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 94 | 2 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 4 | 2 | 1 | 7 |
| block 490 (x 10, y 15) | 489 | 1 | 1 | 12 |
| block 728 (x 24, y 22) | 728 | 2 | 1 | 7 |
| block 744 (x 8, y 23) | 744 | 2 | 1 | 7 |
| `0x404` a monster died | ? | ? | 2 | 7 |
| `0x404` a monster died | ? | ? | 1 | 12 |
| `0x404` a monster died | ? | ? | 2 | 7 |
| `0x404` a monster died | ? | ? | 1 | 12 |
| `0x404` a monster died | ? | ? | 2 | 7 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 9, y 15 | 8 | x 10, y 15 | 0x4206 | SCOTIA |

## Text shown by the scripts (ids only)

- Level text file `LEVEL29.<lang>`: 11 ids: 0, 1, 2, 3, 4, 6, 11, 18, 19, 20, 21.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL29.ENG --index N`.
