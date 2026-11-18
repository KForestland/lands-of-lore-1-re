# Level 3

Made by `tools/level_report.py` from `LEVEL3.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 1 = FOREST1 (decorations `FOREST1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: FOREST1 with palette ALTPAL1.PAL (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 560 | — | — |  | 0x80 | 63 |
| 1 | 1725 | 1 | 8 |  | 0x07 | 255 |
| 2 | 1724 | 2 | 9 |  | 0x07 | 255 |
| 26 | 8 | — | — |  | 0x84 | 63 |
| 46 | 3 | 1 | 12 | 1 clickable wall | 0x07 | 255 |
| 50 | 2 | 2 | 26 | 1 clickable wall | 0x07 | 255 |
| 51 | 2 | 1 | 27 | 1 clickable wall | 0x07 | 255 |
| 52 | 1 | 2 | 28 | 1 clickable wall | 0x07 | 255 |
| 53 | 4 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 54 | 3 | 2 | 41 | 1 clickable wall | 0x07 | 255 |
| 55 | 4 | 2 | 42 | 1 clickable wall | 0x07 | 255 |
| 56 | 4 | — | 1 |  | 0x06 | 63 |
| 57 | 4 | — | 2 |  | 0x06 | 63 |
| 58 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 59 | 4 | — | 4 |  | 0x06 | 63 |
| 60 | 4 | — | 5 |  | 0x06 | 63 |
| 61 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 62 | 3 | 1 | 25 | 1 clickable wall | 0x07 | 255 |
| 63 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 64 | 3 | 1 | 14 | 1 clickable wall | 0x07 | 255 |
| 65 | 2 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 66 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 67 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 68 | 16 | — | 24 | 1 clickable wall | 0x80 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 70 (x 6, y 2) | north | 68 | clickable wall |
| 70 (x 6, y 2) | east | 68 | clickable wall |
| 70 (x 6, y 2) | south | 68 | clickable wall |
| 70 (x 6, y 2) | west | 68 | clickable wall |
| 71 (x 7, y 2) | south | 62 | clickable wall |
| 76 (x 12, y 2) | east | 51 | clickable wall |
| 104 (x 8, y 3) | west | 64 | clickable wall |
| 132 (x 4, y 4) | south | 65 | clickable wall |
| 176 (x 16, y 5) | west | 51 | clickable wall |
| 193 (x 1, y 6) | east | 52 | clickable wall |
| 239 (x 15, y 7) | west | 50 | clickable wall |
| 261 (x 5, y 8) | north | 68 | clickable wall |
| 261 (x 5, y 8) | east | 68 | clickable wall |
| 261 (x 5, y 8) | south | 68 | clickable wall |
| 261 (x 5, y 8) | west | 68 | clickable wall |
| 270 (x 14, y 8) | north | 64 | clickable wall |
| 300 (x 12, y 9) | north | 68 | clickable wall |
| 300 (x 12, y 9) | east | 68 | clickable wall |
| 300 (x 12, y 9) | south | 68 | clickable wall |
| 300 (x 12, y 9) | west | 68 | clickable wall |
| 513 (x 1, y 16) | south | 62 | clickable wall |
| 520 (x 8, y 16) | south | 54 | clickable wall |
| 586 (x 10, y 18) | north | 46 | clickable wall |
| 591 (x 15, y 18) | north | 68 | clickable wall |
| 591 (x 15, y 18) | east | 68 | clickable wall |
| 591 (x 15, y 18) | south | 68 | clickable wall |
| 591 (x 15, y 18) | west | 68 | clickable wall |
| 611 (x 3, y 19) | west | 64 | clickable wall |
| 641 (x 1, y 20) | north | 55 | clickable wall |
| 642 (x 2, y 20) | south | 54 | clickable wall |
| 645 (x 5, y 20) | east | 50 | clickable wall |
| 648 (x 8, y 20) | north | 46 | clickable wall |
| 683 (x 11, y 21) | north | 65 | clickable wall |
| 713 (x 9, y 22) | east | 55 | clickable wall |
| 718 (x 14, y 22) | west | 54 | clickable wall |
| 741 (x 5, y 23) | north | 53 | clickable wall |
| 748 (x 12, y 23) | east | 53 | clickable wall |
| 771 (x 3, y 24) | west | 46 | clickable wall |
| 801 (x 1, y 25) | east | 62 | clickable wall |
| 810 (x 10, y 25) | north | 55 | clickable wall |
| 839 (x 7, y 26) | north | 53 | clickable wall |
| 849 (x 17, y 26) | north | 55 | clickable wall |
| 867 (x 3, y 27) | north | 53 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL3.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles FOREST1; loads monster sprites ORC.SHP into slot 0; loads monster sprites LIZARD.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 752; places a monster (slot 2) on block 817; places a monster (slot 2) on block 581; places a monster (slot 1) on block 544; places a monster (slot 1) on block 610; places a monster (slot 1) on block 676; places a monster (slot 1) on block 770; places item 99 (Rock) on block 551 … |

### LEVEL3.INF

| Entry | Events | What it does |
|---|---|---|
| block 462 (x 14, y 14) | wall clicked | a character speaks; sets game flag 193; starts a dialogue; set global var; tests game flag 193 |
| block 494 (x 14, y 15) | party steps in, wall clicked | starts cut-scene THOMGOG3.TIM; gives ? crown(s); starts cut-scene BOAT.TIM; moves the party to level 2, block 328; a character speaks; shows a message; set global var; tests game flag 27 … |
| block 513 (x 1, y 16) | wall clicked | tests game flag 481 |
| block 520 (x 8, y 16) | wall clicked | tests game flag 480 |
| block 526 (x 14, y 16) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | set global var |
| block 586 (x 10, y 18) | wall clicked | tests game flag 477 |
| block 642 (x 2, y 20) | wall clicked | tests game flag 478 |
| block 648 (x 8, y 20) | wall clicked | tests game flag 476 |
| block 688 (x 16, y 21) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | set global var |
| block 689 (x 17, y 21) | party steps in, wall clicked | sets game flag 192; a character speaks; shows a message; set global var; tests game flag 16 |
| block 690 (x 18, y 21) | wall clicked | starts cut-scene COMPASSE.TIM; starts cut-scene COMPASSF.TIM; starts cut-scene COMPASSG.TIM; a character joins the party; starts cut-scene INN1.TIM; starts cut-scene TYRUS1.TIM; starts cut-scene TYRUS2.TIM; starts cut-scene INN3.TIM … |
| block 712 (x 8, y 22) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | clears game flag 7; sets game flag 7; set global var; tests game flag 7 |
| block 718 (x 14, y 22) | wall clicked | tests game flag 479 |
| block 744 (x 8, y 23) | party steps in, wall clicked | sets game flag 27; a character speaks; shows a message; plays a sound; set global var; tests game flag 27 |
| block 771 (x 3, y 24) | wall clicked | tests game flag 475 |
| block 772 (x 4, y 24) | party steps in, wall clicked | moves the party to level 4, block 167; a character speaks; clears game flag 7; shows a message; set global var |
| block 776 (x 8, y 24) | wall clicked | starts cut-scene BUCK12.TIM; starts cut-scene BUCKBUY.TIM; gives ? crown(s); starts cut-scene BUCK15.TIM; starts cut-scene BUCK02.TIM; takes 20 crown(s); gives item 216 (Salve); takes 100 crown(s) … |
| block 804 (x 4, y 25) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | clears game flag 7; sets game flag 7; a character speaks; sets game flag 37; set global var; tests game flag 7; tests game flag 37; tests game flag 16 |
| `0x400` level loaded | — | starts script timer 0 |
| `0x401` script timer 0 | — | no game action (only stack and screen bookkeeping) |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 3 | 551 |
| INI entry 1 (runs when the level loads) | 79 | Horseshoe | 3 | 817 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 3 | 752 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 3 | 544 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 3 | 752 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 3 | 747 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 752 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 817 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 581 | 3 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 544 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 544 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 610 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 610 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 610 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 676 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 676 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 676 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 676 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 770 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 770 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 770 | 0 | 1 | 3 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 4, y 24 | 4 | x 4, y 24 | 0x41da | ROLAND'S MANOR |
| x 17, y 21 | 8 | x 16, y 21 | 0x41db | GREY EAGLE INN |
| x 14, y 15 | 1 | x 14, y 16 | 0x41d7 | MARINA |
| x 8, y 23 | 0 | x 8, y 22 | 0x41dc | BUCK'S SKINS |

## Text shown by the scripts (ids only)

- Level text file `LEVEL03.<lang>`: 61 ids: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 40, 41, 42, 43, 44, 48, 50, 51, 53, 54, 55, 56, 58, 60, 61, 63, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 84.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL03.ENG --index N`.
