# Level 11

Made by `tools/level_report.py` from `LEVEL11.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 4 = SWAMP (decorations `SWAMP.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: SWAMP (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 948 | — | — |  | 0x80 | 63 |
| 1 | 80 | 1 | — |  | 0x07 | 255 |
| 2 | 80 | 2 | — |  | 0x07 | 255 |
| 25 | 12 | — | — |  | 0x84 | 63 |
| 27 | 10 | 2 | 19 | 1 clickable wall | 0x07 | 255 |
| 53 | 915 | 1 | — |  | 0x07 | 255 |
| 54 | 878 | 2 | — |  | 0x07 | 255 |
| 55 | 1052 | 3 | — |  | 0x07 | 255 |
| 56 | 2 | 2 | 2 | 1 clickable wall | 0x07 | 210 |
| 59 | 4 | — | 5 |  | 0x04 | 63 |
| 60 | 4 | — | 6 |  | 0x04 | 63 |
| 61 | 68 | — | 1 | 1 clickable wall | 0x84 | 11 |
| 67 | 4 | — | 12 |  | 0x06 | 63 |
| 68 | 4 | — | 13 |  | 0x06 | 63 |
| 69 | 4 | — | 14 |  | 0x06 | 255 |
| 70 | 4 | — | 15 |  | 0x06 | 255 |
| 71 | 7 | 1 | 16 | 1 clickable wall | 0x07 | 255 |
| 72 | 7 | 2 | 17 | 1 clickable wall | 0x07 | 255 |
| 73 | 8 | 3 | 18 | 1 clickable wall | 0x07 | 255 |
| 75 | 5 | 1 | 32 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 42 (x 10, y 1) | south | 72 | clickable wall |
| 106 (x 10, y 3) | west | 27 | clickable wall |
| 117 (x 21, y 3) | north | 61 | clickable wall |
| 117 (x 21, y 3) | east | 61 | clickable wall |
| 117 (x 21, y 3) | south | 61 | clickable wall |
| 117 (x 21, y 3) | west | 61 | clickable wall |
| 121 (x 25, y 3) | south | 71 | clickable wall |
| 122 (x 26, y 3) | south | 73 | clickable wall |
| 131 (x 3, y 4) | north | 61 | clickable wall |
| 131 (x 3, y 4) | east | 61 | clickable wall |
| 131 (x 3, y 4) | south | 61 | clickable wall |
| 131 (x 3, y 4) | west | 61 | clickable wall |
| 132 (x 4, y 4) | west | 72 | clickable wall |
| 139 (x 11, y 4) | north | 27 | clickable wall |
| 168 (x 8, y 5) | south | 27 | clickable wall |
| 248 (x 24, y 7) | north | 61 | clickable wall |
| 248 (x 24, y 7) | east | 61 | clickable wall |
| 248 (x 24, y 7) | south | 61 | clickable wall |
| 248 (x 24, y 7) | west | 61 | clickable wall |
| 270 (x 14, y 8) | south | 71 | clickable wall |
| 274 (x 18, y 8) | north | 61 | clickable wall |
| 274 (x 18, y 8) | east | 61 | clickable wall |
| 274 (x 18, y 8) | south | 61 | clickable wall |
| 274 (x 18, y 8) | west | 61 | clickable wall |
| 275 (x 19, y 8) | east | 72 | clickable wall |
| 281 (x 25, y 8) | east | 75 | clickable wall |
| 282 (x 26, y 8) | north | 61 | clickable wall |
| 282 (x 26, y 8) | east | 61 | clickable wall |
| 282 (x 26, y 8) | south | 61 | clickable wall |
| 282 (x 26, y 8) | west | 61 | clickable wall |
| 288 (x 0, y 9) | east | 73 | clickable wall |
| 305 (x 17, y 9) | west | 72 | clickable wall |
| 321 (x 1, y 10) | south | 56 | clickable wall |
| 337 (x 17, y 10) | east | 73 | clickable wall |
| 358 (x 6, y 11) | south | 72 | clickable wall |
| 369 (x 17, y 11) | north | 61 | clickable wall |
| 369 (x 17, y 11) | east | 61 | clickable wall |
| 369 (x 17, y 11) | south | 61 | clickable wall |
| 369 (x 17, y 11) | west | 61 | clickable wall |
| 380 (x 28, y 11) | north | 61 | clickable wall |
| 380 (x 28, y 11) | east | 61 | clickable wall |
| 380 (x 28, y 11) | south | 61 | clickable wall |
| 380 (x 28, y 11) | west | 61 | clickable wall |
| 409 (x 25, y 12) | north | 71 | clickable wall |
| 415 (x 31, y 12) | west | 71 | clickable wall |
| 418 (x 2, y 13) | north | 73 | clickable wall |
| 426 (x 10, y 13) | south | 27 | clickable wall |
| 434 (x 18, y 13) | north | 61 | clickable wall |
| 434 (x 18, y 13) | east | 61 | clickable wall |
| 434 (x 18, y 13) | south | 61 | clickable wall |
| 434 (x 18, y 13) | west | 61 | clickable wall |
| 448 (x 0, y 14) | east | 73 | clickable wall |
| 451 (x 3, y 14) | north | 71 | clickable wall |
| 452 (x 4, y 14) | north | 61 | clickable wall |
| 452 (x 4, y 14) | east | 61 | clickable wall |
| 452 (x 4, y 14) | south | 61 | clickable wall |
| 452 (x 4, y 14) | west | 61 | clickable wall |
| 463 (x 15, y 14) | west | 27 | clickable wall |
| 490 (x 10, y 15) | north | 27 | clickable wall |
| 497 (x 17, y 15) | north | 61 | clickable wall |
| 497 (x 17, y 15) | east | 61 | clickable wall |
| 497 (x 17, y 15) | south | 61 | clickable wall |
| 497 (x 17, y 15) | west | 61 | clickable wall |
| 498 (x 18, y 15) | north | 61 | clickable wall |
| 498 (x 18, y 15) | east | 61 | clickable wall |
| 498 (x 18, y 15) | south | 61 | clickable wall |
| 498 (x 18, y 15) | west | 61 | clickable wall |
| 500 (x 20, y 15) | south | 27 | clickable wall |
| 503 (x 23, y 15) | north | 61 | clickable wall |
| 503 (x 23, y 15) | east | 61 | clickable wall |
| 503 (x 23, y 15) | south | 61 | clickable wall |
| 503 (x 23, y 15) | west | 61 | clickable wall |
| 530 (x 18, y 16) | north | 61 | clickable wall |
| 530 (x 18, y 16) | east | 61 | clickable wall |
| 530 (x 18, y 16) | south | 61 | clickable wall |
| 530 (x 18, y 16) | west | 61 | clickable wall |
| 533 (x 21, y 16) | west | 27 | clickable wall |
| 553 (x 9, y 17) | south | 27 | clickable wall |
| 560 (x 16, y 17) | north | 61 | clickable wall |
| 560 (x 16, y 17) | east | 61 | clickable wall |
| 560 (x 16, y 17) | south | 61 | clickable wall |
| 560 (x 16, y 17) | west | 61 | clickable wall |
| 563 (x 19, y 17) | east | 73 | clickable wall |
| 577 (x 1, y 18) | north | 56 | clickable wall |
| 581 (x 5, y 18) | north | 71 | clickable wall |
| 604 (x 28, y 18) | north | 61 | clickable wall |
| 604 (x 28, y 18) | east | 61 | clickable wall |
| 604 (x 28, y 18) | south | 61 | clickable wall |
| 604 (x 28, y 18) | west | 61 | clickable wall |
| 612 (x 4, y 19) | north | 61 | clickable wall |
| 612 (x 4, y 19) | east | 61 | clickable wall |
| 612 (x 4, y 19) | south | 61 | clickable wall |
| 612 (x 4, y 19) | west | 61 | clickable wall |
| 613 (x 5, y 19) | west | 72 | clickable wall |
| 617 (x 9, y 19) | north | 27 | clickable wall |
| 621 (x 13, y 19) | north | 61 | clickable wall |
| 621 (x 13, y 19) | east | 61 | clickable wall |
| 621 (x 13, y 19) | south | 61 | clickable wall |
| 621 (x 13, y 19) | west | 61 | clickable wall |
| 653 (x 13, y 20) | north | 75 | clickable wall |
| 653 (x 13, y 20) | east | 75 | clickable wall |
| 653 (x 13, y 20) | south | 75 | clickable wall |
| 653 (x 13, y 20) | west | 75 | clickable wall |
| 689 (x 17, y 21) | north | 73 | clickable wall |
| 868 (x 4, y 27) | south | 71 | clickable wall |
| 870 (x 6, y 27) | south | 72 | clickable wall |
| 872 (x 8, y 27) | south | 73 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL11.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles SWAMP; loads monster sprites SWAMPMON.SHP into slot 0; loads monster sprites HURZELL.SHP into slot 0; loads monster sprites SWAMPCIT.SHP into slot 1; defines monster type 1; defines monster type 2; sets game flag 77; tests game flag 86 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 135; places a monster (slot 2) on block 515; places a monster (slot 2) on block 668; places a monster (slot 1) on block 545; places a monster (slot 1) on block 449; places a monster (slot 1) on block 521; places a monster (slot 1) on block 357; places a monster (slot 1) on block 268 … |

### LEVEL11.INF

| Entry | Events | What it does |
|---|---|---|
| block 42 (x 10, y 1) | wall clicked | a character speaks |
| block 45 (x 13, y 1) | wall clicked | places a monster (slot 1) on block 659; sets the north wall of block 992 to type 0; moves the party to level 11, block 109; places a monster (slot 2) on block 109; gives item 220 (Ruby of Truth); places item 125 (Trident "Mantis") on block 109; gives item 125 (Trident "Mantis"); sets game flag 83 … |
| block 77 (x 13, y 2) | party steps in, wall clicked | shows a message; a character speaks; set global var; tests game flag 284; tests game flag 84; tests game flag 81 |
| block 104 (x 8, y 3) | party arrives (second path) | tests game flag 84 |
| block 106 (x 10, y 3) | wall clicked | a character speaks |
| block 108 (x 12, y 3) | party steps in | sets the north wall of block 992 to type 0; checks a wall of block 992 |
| block 109 (x 13, y 3) | party steps in, bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; sets the north wall of block 992 to type 0; checks a wall of block 992 |
| block 113 (x 17, y 3) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 114 (x 18, y 3) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 117 (x 21, y 3) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 121 (x 25, y 3) | wall clicked | a character speaks |
| block 122 (x 26, y 3) | wall clicked | a character speaks |
| block 131 (x 3, y 4) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 135 (x 7, y 4) | party arrives (second path) | tests game flag 84 |
| block 139 (x 11, y 4) | wall clicked | a character speaks |
| block 163 (x 3, y 5) | wall clicked | a character speaks |
| block 165 (x 5, y 5) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 167 (x 7, y 5) | party arrives (second path), bits 0x10 (no engine caller found) | check equipped item script flags; a character speaks; starts a dialogue; sets game flag 270; move monster; sets game flag 271; tests game flag 271 |
| block 168 (x 8, y 5) | wall clicked | a character speaks |
| block 193 (x 1, y 6) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 197 (x 5, y 6) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 208 (x 16, y 6) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 209 (x 17, y 6) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 225 (x 1, y 7) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 248 (x 24, y 7) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 264 (x 8, y 8) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 265 (x 9, y 8) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 270 (x 14, y 8) | wall clicked | a character speaks |
| block 272 (x 16, y 8) | wall clicked | a character speaks |
| block 274 (x 18, y 8) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 275 (x 19, y 8) | wall clicked | a character speaks |
| block 277 (x 21, y 8) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 281 (x 25, y 8) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 282 (x 26, y 8) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 284 (x 28, y 8) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 290 (x 2, y 9) | wall clicked | a character speaks |
| block 309 (x 21, y 9) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 316 (x 28, y 9) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 321 (x 1, y 10) | wall clicked | deals damage; checks a wall of block 993 |
| block 334 (x 14, y 10) | wall clicked | sets the north wall of block 0 to type 83; sets the north wall of block 0 to type 0; gives ? crown(s); gives item 39 (Crossbow); gives item 35 (Bow); gives item 66 (Great bow); get item price; clears game flag ? … |
| block 337 (x 17, y 10) | wall clicked | a character speaks |
| block 353 (x 1, y 11) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 993 |
| block 358 (x 6, y 11) | wall clicked | places a monster (slot 2) on block 109; a character speaks; suspend monster; make item; give item to monster; changes a monster; sets game flag 84; tests game flag 84 … |
| block 366 (x 14, y 11) | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; set global var; tests game flag 275; tests game flag 274; tests game flag 276; plays a sound; tests game flag 84; tests game flag 81 |
| block 369 (x 17, y 11) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 380 (x 28, y 11) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 409 (x 25, y 12) | wall clicked | a character speaks |
| block 415 (x 31, y 12) | wall clicked | a character speaks |
| block 418 (x 2, y 13) | wall clicked | a character speaks |
| block 426 (x 10, y 13) | wall clicked | a character speaks |
| block 432 (x 16, y 13) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 433 (x 17, y 13) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 434 (x 18, y 13) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 448 (x 0, y 14) | wall clicked | a character speaks |
| block 451 (x 3, y 14) | wall clicked | a character speaks |
| block 452 (x 4, y 14) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 453 (x 5, y 14) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 454 (x 6, y 14) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 455 (x 7, y 14) | party arrives (second path) | tests game flag 84 |
| block 463 (x 15, y 14) | wall clicked | a character speaks |
| block 473 (x 25, y 14) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 474 (x 26, y 14) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 475 (x 27, y 14) | party arrives (second path) | tests game flag 84 |
| block 487 (x 7, y 15) | wall clicked | gives ? crown(s); sets the north wall of block 0 to type 87; sets the north wall of block 0 to type 0; takes 300 crown(s); gives item 232 (Wand of Fireballs); sets game flag 314; sets game flag 313; sets game flag 316 … |
| block 490 (x 10, y 15) | wall clicked | a character speaks |
| block 497 (x 17, y 15) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 498 (x 18, y 15) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 500 (x 20, y 15) | wall clicked | a character speaks |
| block 503 (x 23, y 15) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 515 (x 3, y 16) | party arrives (second path) | tests game flag 84 |
| block 519 (x 7, y 16) | party steps in, wall clicked | shows a message; starts a dialogue; set global var; tests game flag 84 |
| block 523 (x 11, y 16) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 530 (x 18, y 16) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 531 (x 19, y 16) | wall clicked | a character speaks |
| block 545 (x 1, y 17) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 992 |
| block 547 (x 3, y 17) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; starts a dialogue; move monster; sets game flag 269; tests game flag 269 |
| block 551 (x 7, y 17) | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; sets the north wall of block 992 to type 0; set global var; checks a wall of block 992 |
| block 553 (x 9, y 17) | wall clicked | a character speaks |
| block 555 (x 11, y 17) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 560 (x 16, y 17) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 561 (x 17, y 17) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 577 (x 1, y 18) | wall clicked | deals damage; checks a wall of block 992 |
| block 583 (x 7, y 18) | party steps in | sets the north wall of block 992 to type 0; checks a wall of block 992 |
| block 593 (x 17, y 18) | party arrives (second path) | deals damage; paralyze poison character; shows a message |
| block 595 (x 19, y 18) | wall clicked | a character speaks |
| block 604 (x 28, y 18) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 611 (x 3, y 19) | party arrives (second path) | sets game flag 255; a character speaks; tests game flag 255 |
| block 612 (x 4, y 19) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 613 (x 5, y 19) | wall clicked | a character speaks |
| block 617 (x 9, y 19) | wall clicked | a character speaks |
| block 621 (x 13, y 19) | party arrives (second path), wall clicked, item put down, fireball passes | gives item 212 (Swamp Vial); delete hand item; plays a sound |
| block 628 (x 20, y 19) | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; sets game flag 82; a character speaks; set global var; tests game flag 277; tests game flag 278; tests game flag 279; tests game flag 280 … |
| block 653 (x 13, y 20) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 660 (x 20, y 20) | wall clicked | sets the north wall of block 0 to type 71; sets the north wall of block 0 to type 0; gives ? crown(s); gives item 70 (Great sword); gives item 52 (Great axe); gives item 124 (Trident); gives item 149 (Kite shield); get item price … |
| block 668 (x 28, y 20) | party arrives (second path) | tests game flag 84 |
| block 673 (x 1, y 21) | party steps in, party arrives (second path), item put down | moves objects from block 673 to block 161 |
| block 689 (x 17, y 21) | wall clicked | a character speaks |
| block 700 (x 28, y 21) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; starts a dialogue; move monster; sets game flag 269; tests game flag 269 |
| block 734 (x 30, y 22) | party arrives (second path) | a character speaks; sets game flag 590; tests game flag 590 |
| block 735 (x 31, y 22) | party steps in, party arrives (second path), item put down | moves objects from block 735 to block 705 |
| `0x400` level loaded | — | sets the north wall of block 992 to type 0; starts script timer 0; starts script timer 1; starts script timer 2 |
| `0x401` script timer 0 | — | check equipped item script flags; move monster; sets game flag 271; tests game flag 270; tests game flag 271 |
| `0x402` script timer 1 | — | places a monster (slot 2) on block 361; places a monster (slot 2) on block 475; places a monster (slot 2) on block 455; tests game flag 284; tests game flag 84 |
| `0x403` script timer 2 | — | update block animations2; tests game flag 418; checks a wall of block 131; plays a sound; checks a wall of block 533; checks a wall of block 553; checks a wall of block 617; checks a wall of block 463 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 80 | Bronze horseshoe | 11 | 623 |
| INI entry 1 (runs when the level loads) | 110 | Staff "Beater" | 11 | 450 |
| INI entry 1 (runs when the level loads) | 164 | Glint mail | 11 | 379 |
| INI entry 1 (runs when the level loads) | 133 | Dwarvish buckler | 11 | 249 |
| INI entry 1 (runs when the level loads) | 37 | Bow "Scout" | 11 | 620 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 11 | 565 |
| block 45 (x 13, y 1) | 125 | Trident "Mantis" | 11 | 109 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 135 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 135 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 515 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 515 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 668 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 668 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 545 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 449 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 521 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 357 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 268 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 271 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 525 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 387 | 0 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 419 | 0 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 385 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 227 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 170 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 142 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 80 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 84 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 276 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 411 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 382 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 312 | 1 | 1 | 3 |
| block 45 (x 13, y 1) | 659 | 0 | 1 | 4 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 45 (x 13, y 1) | 109 | 3 | 2 | 7 |
| block 358 (x 6, y 11) | 109 | 3 | 2 | 7 |
| block 358 (x 6, y 11) | 109 | 3 | 2 | 7 |
| block 358 (x 6, y 11) | 109 | 3 | 2 | 7 |
| `0x402` script timer 1 | 361 | 0 | 2 | 4 |
| `0x402` script timer 1 | 361 | 0 | 2 | 4 |
| `0x402` script timer 1 | 475 | 0 | 2 | 4 |
| `0x402` script timer 1 | 475 | 0 | 2 | 4 |
| `0x402` script timer 1 | 455 | 1 | 2 | 4 |
| `0x402` script timer 1 | 455 | 1 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 1, y 22 | 0 | x 1, y 20 | 0x41de | FOREST |
| x 31, y 22 | 9 | x 29, y 22 | 0x41de | FOREST |
| x 14, y 11 | 4 | x 14, y 12 | 0x41e5 | FLETCHER |
| x 13, y 1 | 3 | x 13, y 2 | 0x41e6 | GORKHA CHIEFTAIN |
| x 7, y 16 | 5 | x 7, y 16 | 0x41e7 | WITCH DOCTOR |
| x 20, y 19 | 8 | x 20, y 19 | 0x41e8 | BLACKSMITH |

## Text shown by the scripts (ids only)

- Level text file `LEVEL11.<lang>`: 16 ids: 0, 1, 2, 3, 32, 33, 47, 52, 75, 76, 77, 89, 90, 91, 98, 99.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL11.ENG --index N`.
