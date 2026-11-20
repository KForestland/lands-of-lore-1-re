# Level 17

Made by `tools/level_report.py` from `LEVEL17.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 17](../PROGRESSION.md#level-17) and [item, spell and creature numbers](../NUMBERS.md).

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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL17.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0084` | — | loads wall tiles FOREST1; loads monster sprites HORNET.SHP into slot 0; loads monster sprites MOLDER.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x012E` | — | places a monster of type slot 2 on block 581 in mode 3; places a monster of type slot 2 on block 420 in mode 3; places a monster of type slot 2 on block 392 in mode 3; places a monster of type slot 2 on block 519 in mode 3; places a monster of type slot 2 on block 135 in mode 3; places a monster of type slot 2 on block 501 in mode 3; places a monster of type slot 2 on block 567 in mode 3; places a monster of type slot 2 on block 186 in mode 3 … |

### LEVEL17.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 78 (x 14, y 2) | `0x0592` | party steps in, party arrives (second path), item put down | moves items from block 78 to level 24, block 910 |
| block 133 (x 5, y 4) | `0x0836` | wall clicked | tests game flag 506 |
| block 187 (x 27, y 5) | `0x0646` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); loads cut-scene ?.TIM into slot ?; sets the west wall of block 240 to type ?; sets the south wall of block 240 to type 0; loads cut-scene UNBAR1.TIM into slot 1; loads cut-scene UNBAR2.TIM into slot 2; sets the south wall of block 240 to type 47; sets all four walls of block 240 to type 0 … |
| block 188 (x 28, y 5) | `0x0642` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 995 |
| block 201 (x 9, y 6) | `0x08FD` | wall clicked | tests game flag 534 |
| block 228 (x 4, y 7) | `0x0878` | wall clicked | tests game flag 512 |
| block 240 (x 16, y 7) | `0x071C` | party steps in, wall clicked | requests engine global change, selector 10, operands 0, 0; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 272; checks the south wall of block 240; tests game flag 325 |
| block 256 (x 0, y 8) | `0x090F` | wall clicked | tests game flag 535 |
| block 260 (x 4, y 8) | `0x0945` | wall clicked | tests game flag 538 |
| block 272 (x 16, y 8) | `0x0744` | party arrives (second path), bits 0x410 (no engine caller found) | loads cut-scene HAG_S.TIM into slot 0; loads cut-scene BARRIER.TIM into slot 0; sets the south wall of block 240 to type 47; sets the west wall of block 240 to type 0; sets game flag 325; plays music track 287; starts a dialogue sequence in mode 0; plays music track 286 … |
| block 282 (x 26, y 8) | `0x084C` | wall clicked | tests game flag 508 |
| block 298 (x 10, y 9) | `0x08EB` | wall clicked | tests game flag 533 |
| block 319 (x 31, y 9) | `0x0895` | wall clicked | tests game flag 514 |
| block 326 (x 6, y 10) | `0x062A` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 346 (x 26, y 10) | `0x08A0` | wall clicked | tests game flag 515 |
| block 356 (x 4, y 11) | `0x0841` | wall clicked | tests game flag 507 |
| block 358 (x 6, y 11) | `0x062E` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 372 (x 20, y 11) | `0x086D` | wall clicked | tests game flag 511 |
| block 412 (x 28, y 12) | `0x0992` | wall clicked | deletes the held item; puts item 213 (Honey) on an empty cursor; plays chat/dialogue text ID 0x0015; plays chat/dialogue text ID 0x0014 |
| block 444 (x 28, y 13) | `0x0981` | fireball passes | sets the south wall of block 412 to type 79 |
| block 462 (x 14, y 14) | `0x0968` | wall clicked | deletes the held item; puts item 213 (Honey) on an empty cursor; plays chat/dialogue text ID 0x0015; plays chat/dialogue text ID 0x0014 |
| block 463 (x 15, y 14) | `0x0957` | fireball passes | sets the west wall of block 462 to type 79 |
| block 480 (x 0, y 15) | `0x0933` | wall clicked | tests game flag 537 |
| block 482 (x 2, y 15) | `0x08CB` | wall clicked | tests game flag 518 |
| block 517 (x 5, y 16) | `0x0632` | wall clicked | sets the south wall of block 993 to type 0; checks the south wall of block 993 |
| block 549 (x 5, y 17) | `0x0636` | bits 0x400 (no engine caller found) | sets the south wall of block 993 to type 0; checks the south wall of block 993 |
| block 557 (x 13, y 17) | `0x0921` | wall clicked | tests game flag 536 |
| block 568 (x 24, y 17) | `0x063E` | bits 0x400 (no engine caller found) | no action summarized |
| block 569 (x 25, y 17) | `0x063A` | wall clicked | no action summarized |
| block 586 (x 10, y 18) | `0x097D` | wall clicked | deletes the held item; puts item 213 (Honey) on an empty cursor; plays chat/dialogue text ID 0x0015; plays chat/dialogue text ID 0x0014 |
| block 587 (x 11, y 18) | `0x096C` | fireball passes | sets the east wall of block 586 to type 79 |
| block 615 (x 7, y 19) | `0x08DB` | wall clicked | tests game flag 532 |
| block 627 (x 19, y 19) | `0x088A` | wall clicked | tests game flag 513 |
| block 631 (x 23, y 19) | `0x0862` | wall clicked | tests game flag 510 |
| block 679 (x 7, y 21) | `0x0857` | wall clicked | tests game flag 509 |
| block 704 (x 0, y 22) | `0x059D` | party steps in, party arrives (second path) | moves items from block 704 to level 11, block 734 |
| block 705 (x 1, y 22) | `0x0620` | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 318; plays chat/dialogue text ID 0x0000; tests game flag 318 |
| block 728 (x 24, y 22) | `0x05AA` | party steps in | no action summarized |
| block 745 (x 9, y 23) | `0x08AB` | wall clicked | tests game flag 516 |
| block 748 (x 12, y 23) | `0x08BB` | wall clicked | tests game flag 517 |
| block 760 (x 24, y 23) | `0x05AF` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; sets game flag 319; plays chat/dialogue text ID 0x0001; tests game flag 319 |
| block 792 (x 24, y 24) | `0x05EA` | party steps in, party arrives (second path), wall clicked | moves items from block ? to level 12, block 124 |
| `0x400` level loaded | `0x04EC` | — | sets music theme 329; sets script timer 0 to 3600 ticks |
| `0x401` script timer 0 | `0x04F8` | — | places a monster of type slot 1 on block 460 in mode 4; places a monster of type slot 1 on block 461 in mode 4; places a monster of type slot 1 on block 587 in mode 4; places a monster of type slot 1 on block 588 in mode 4; places a monster of type slot 1 on block 444 in mode 4; places a monster of type slot 1 on block 476 in mode 4; checks the west wall of block 462; checks the east wall of block 586 … |

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
