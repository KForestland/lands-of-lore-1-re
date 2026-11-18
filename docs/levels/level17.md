# Level 17

Made by `tools/level_report.py` from `LEVEL17.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 1 = FOREST1 (decorations `FOREST1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: FOREST1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1066 | — | — |  | 0x80 | 63 |
| 1 | 1485 | 1 | 8 |  | 0x07 | 255 |
| 2 | 1484 | 2 | 9 |  | 0x07 | 255 |
| 46 | 6 | 1 | 12 | 1 clickable wall | 0x07 | 255 |
| 50 | 3 | 2 | 26 | 1 clickable wall | 0x07 | 255 |
| 51 | 1 | 1 | 27 | 1 clickable wall | 0x07 | 255 |
| 52 | 3 | 2 | 28 | 1 clickable wall | 0x07 | 255 |
| 53 | 4 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 54 | 6 | 2 | 41 | 1 clickable wall | 0x07 | 255 |
| 55 | 9 | 2 | 42 | 1 clickable wall | 0x07 | 255 |
| 62 | 3 | 1 | 25 | 1 clickable wall | 0x07 | 255 |
| 63 | 4 | 1 | 7 |  | 0x84 | 63 |
| 64 | 2 | 1 | 14 | 1 clickable wall | 0x07 | 255 |
| 65 | 1 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 68 | 4 | — | 24 | 1 clickable wall | 0x80 | 63 |
| 69 | 4 | 1 | 16 | 1 clickable wall | 0x07 | 210 |
| 73 | 4 | — | 30 |  | 0x84 | 63 |
| 74 | 4 | — | 32 |  | 0x84 | 63 |
| 78 | 3 | 1 | 34 | 1 clickable wall | 0x07 | 14 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 133 (x 5, y 4) | south | 46 | clickable wall |
| 143 (x 15, y 4) | west | 53 | clickable wall |
| 188 (x 28, y 5) | west | 69 | clickable wall |
| 190 (x 30, y 5) | west | 64 | clickable wall |
| 201 (x 9, y 6) | west | 52 | clickable wall |
| 214 (x 22, y 6) | east | 53 | clickable wall |
| 228 (x 4, y 7) | north | 54 | clickable wall |
| 256 (x 0, y 8) | east | 62 | clickable wall |
| 260 (x 4, y 8) | south | 50 | clickable wall |
| 282 (x 26, y 8) | north | 46 | clickable wall |
| 298 (x 10, y 9) | south | 62 | clickable wall |
| 319 (x 31, y 9) | west | 54 | clickable wall |
| 326 (x 6, y 10) | south | 69 | clickable wall |
| 346 (x 26, y 10) | south | 54 | clickable wall |
| 356 (x 4, y 11) | west | 46 | clickable wall |
| 368 (x 16, y 11) | south | 53 | clickable wall |
| 372 (x 20, y 11) | north | 54 | clickable wall |
| 405 (x 21, y 12) | east | 55 | clickable wall |
| 412 (x 28, y 12) | south | 78 | clickable wall |
| 462 (x 14, y 14) | west | 78 | clickable wall |
| 474 (x 26, y 14) | south | 55 | clickable wall |
| 480 (x 0, y 15) | east | 50 | clickable wall |
| 482 (x 2, y 15) | east | 52 | clickable wall |
| 509 (x 29, y 15) | east | 53 | clickable wall |
| 517 (x 5, y 16) | east | 69 | clickable wall |
| 523 (x 11, y 16) | north | 55 | clickable wall |
| 528 (x 16, y 16) | east | 46 | clickable wall |
| 532 (x 20, y 16) | west | 55 | clickable wall |
| 557 (x 13, y 17) | south | 50 | clickable wall |
| 560 (x 16, y 17) | south | 64 | clickable wall |
| 569 (x 25, y 17) | west | 69 | clickable wall |
| 586 (x 10, y 18) | east | 78 | clickable wall |
| 594 (x 18, y 18) | west | 55 | clickable wall |
| 607 (x 31, y 18) | west | 55 | clickable wall |
| 615 (x 7, y 19) | north | 62 | clickable wall |
| 627 (x 19, y 19) | south | 54 | clickable wall |
| 631 (x 23, y 19) | east | 46 | clickable wall |
| 631 (x 23, y 19) | west | 54 | clickable wall |
| 679 (x 7, y 21) | north | 46 | clickable wall |
| 683 (x 11, y 21) | south | 55 | clickable wall |
| 688 (x 16, y 21) | north | 55 | clickable wall |
| 706 (x 2, y 22) | north | 68 | clickable wall |
| 706 (x 2, y 22) | east | 68 | clickable wall |
| 706 (x 2, y 22) | south | 68 | clickable wall |
| 706 (x 2, y 22) | west | 68 | clickable wall |
| 725 (x 21, y 22) | north | 55 | clickable wall |
| 745 (x 9, y 23) | north | 51 | clickable wall |
| 748 (x 12, y 23) | north | 52 | clickable wall |
| 763 (x 27, y 23) | north | 65 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL17.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles FOREST1; loads monster sprites HORNET.SHP into slot 0; loads monster sprites MOLDER.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 581; places a monster (slot 2) on block 420; places a monster (slot 2) on block 392; places a monster (slot 2) on block 519; places a monster (slot 2) on block 135; places a monster (slot 2) on block 501; places a monster (slot 2) on block 567; places a monster (slot 2) on block 186 … |

### LEVEL17.INF

| Entry | Events | What it does |
|---|---|---|
| block 78 (x 14, y 2) | party steps in, party arrives (second path), item put down | moves objects from block 78 to block 910 |
| block 133 (x 5, y 4) | wall clicked | tests game flag 506 |
| block 187 (x 27, y 5) | bits 0x400 (no engine caller found) | deals damage; starts cut-scene ?.TIM; sets the west wall of block 240 to type ?; sets the south wall of block 240 to type 0; starts cut-scene UNBAR1.TIM; starts cut-scene UNBAR2.TIM; sets the south wall of block 240 to type 47; sets the west wall of block 240 to type 0 … |
| block 188 (x 28, y 5) | wall clicked | deals damage; checks a wall of block 995 |
| block 201 (x 9, y 6) | wall clicked | tests game flag 534 |
| block 228 (x 4, y 7) | wall clicked | tests game flag 512 |
| block 240 (x 16, y 7) | party steps in, wall clicked | shows a message; checks a wall of block 240; tests game flag 325; set global var |
| block 256 (x 0, y 8) | wall clicked | tests game flag 535 |
| block 260 (x 4, y 8) | wall clicked | tests game flag 538 |
| block 272 (x 16, y 8) | party arrives (second path), bits 0x410 (no engine caller found) | starts cut-scene HAG_S.TIM; starts cut-scene BARRIER.TIM; sets the south wall of block 240 to type 47; sets the west wall of block 240 to type 0; sets game flag 325; starts a dialogue; a character speaks; checks a wall of block 240 … |
| block 282 (x 26, y 8) | wall clicked | tests game flag 508 |
| block 298 (x 10, y 9) | wall clicked | tests game flag 533 |
| block 319 (x 31, y 9) | wall clicked | tests game flag 514 |
| block 326 (x 6, y 10) | wall clicked | deals damage; checks a wall of block 992 |
| block 346 (x 26, y 10) | wall clicked | tests game flag 515 |
| block 356 (x 4, y 11) | wall clicked | tests game flag 507 |
| block 358 (x 6, y 11) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 992 |
| block 372 (x 20, y 11) | wall clicked | tests game flag 511 |
| block 412 (x 28, y 12) | wall clicked | gives item 213 (Honey); delete hand item; a character speaks |
| block 444 (x 28, y 13) | fireball passes | sets the south wall of block 412 to type 79 |
| block 462 (x 14, y 14) | wall clicked | gives item 213 (Honey); delete hand item; a character speaks |
| block 463 (x 15, y 14) | fireball passes | sets the west wall of block 462 to type 79 |
| block 480 (x 0, y 15) | wall clicked | tests game flag 537 |
| block 482 (x 2, y 15) | wall clicked | tests game flag 518 |
| block 517 (x 5, y 16) | wall clicked | sets the south wall of block 993 to type 0; checks a wall of block 993 |
| block 549 (x 5, y 17) | bits 0x400 (no engine caller found) | sets the south wall of block 993 to type 0; checks a wall of block 993 |
| block 557 (x 13, y 17) | wall clicked | tests game flag 536 |
| block 568 (x 24, y 17) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 569 (x 25, y 17) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 586 (x 10, y 18) | wall clicked | gives item 213 (Honey); delete hand item; a character speaks |
| block 587 (x 11, y 18) | fireball passes | sets the east wall of block 586 to type 79 |
| block 615 (x 7, y 19) | wall clicked | tests game flag 532 |
| block 627 (x 19, y 19) | wall clicked | tests game flag 513 |
| block 631 (x 23, y 19) | wall clicked | tests game flag 510 |
| block 679 (x 7, y 21) | wall clicked | tests game flag 509 |
| block 704 (x 0, y 22) | party steps in, party arrives (second path) | moves objects from block 704 to block 734 |
| block 705 (x 1, y 22) | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 318; a character speaks; tests game flag 318 |
| block 728 (x 24, y 22) | party steps in | no game action (only stack and screen bookkeeping) |
| block 745 (x 9, y 23) | wall clicked | tests game flag 516 |
| block 748 (x 12, y 23) | wall clicked | tests game flag 517 |
| block 760 (x 24, y 23) | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets game flag 319; a character speaks; set global var; tests game flag 319 |
| block 792 (x 24, y 24) | party steps in, party arrives (second path), wall clicked | moves objects from block ? to block 124 |
| `0x400` level loaded | — | starts script timer 0 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 460; places a monster (slot 1) on block 461; places a monster (slot 1) on block 587; places a monster (slot 1) on block 588; places a monster (slot 1) on block 444; places a monster (slot 1) on block 476; checks a wall of block 462; checks a wall of block 586 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 17 | 715 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 17 | 606 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 17 | 292 |
| INI entry 1 (runs when the level loads) | 121 | Stick | 17 | 458 |
| INI entry 1 (runs when the level loads) | 121 | Stick | 17 | 609 |
| INI entry 1 (runs when the level loads) | 121 | Stick | 17 | 376 |
| INI entry 1 (runs when the level loads) | 50 | Dagger "Assassin" | 17 | 596 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 17 | 461 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 17 | 587 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 17 | 444 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 581 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 581 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 420 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 420 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 392 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 392 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 519 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 519 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 135 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 501 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 501 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 567 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 186 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 186 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 187 | 3 | 2 | 3 |
| `0x401` script timer 0 | 460 | 3 | 1 | 4 |
| `0x401` script timer 0 | 460 | 3 | 1 | 4 |
| `0x401` script timer 0 | 461 | 3 | 1 | 4 |
| `0x401` script timer 0 | 461 | 3 | 1 | 4 |
| `0x401` script timer 0 | 587 | 1 | 1 | 4 |
| `0x401` script timer 0 | 587 | 1 | 1 | 4 |
| `0x401` script timer 0 | 588 | 1 | 1 | 4 |
| `0x401` script timer 0 | 588 | 1 | 1 | 4 |
| `0x401` script timer 0 | 444 | 2 | 1 | 4 |
| `0x401` script timer 0 | 444 | 2 | 1 | 4 |
| `0x401` script timer 0 | 476 | 2 | 1 | 4 |
| `0x401` script timer 0 | 476 | 2 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 0, y 22 | 7 | x 1, y 22 | 0x41e1 | SWAMP |
| x 24, y 23 | 8 | x 24, y 22 | 0x41e4 | URBISH MINES |
| x 16, y 8 | 4 | x 16, y 7 | 0x41f0 | SCOTIA'S BARRIER |
| x 14, y 2 | 0 | x 14, y 2 | 0x41f2 | YVEL CAVE |

## Text shown by the scripts (ids only)

- Level text file `LEVEL17.<lang>`: 7 ids: 0, 1, 4, 5, 6, 20, 21.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL17.ENG --index N`.
