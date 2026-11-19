# Level 10

Made by `tools/level_report.py` from `LEVEL10.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 1 = FOREST1 (decorations `FOREST1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: FOREST1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 960 | — | — |  | 0x80 | 63 |
| 1 | 1514 | 1 | 8 |  | 0x07 | 255 |
| 2 | 1516 | 2 | 9 |  | 0x07 | 255 |
| 25 | 16 | — | — |  | 0x84 | 63 |
| 26 | 4 | — | — |  | 0x84 | 63 |
| 46 | 7 | 1 | 12 | 1 clickable wall | 0x07 | 255 |
| 48 | 1 | — | 36 |  | 0x86 | 63 |
| 49 | 4 | — | 37 |  | 0x86 | 63 |
| 50 | 2 | 2 | 26 | 1 clickable wall | 0x07 | 255 |
| 51 | 3 | 1 | 27 | 1 clickable wall | 0x07 | 255 |
| 52 | 1 | 2 | 28 | 1 clickable wall | 0x07 | 255 |
| 53 | 4 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 54 | 8 | 2 | 41 | 1 clickable wall | 0x07 | 255 |
| 55 | 8 | 2 | 42 | 1 clickable wall | 0x07 | 255 |
| 62 | 3 | 1 | 25 | 1 clickable wall | 0x07 | 255 |
| 64 | 3 | 1 | 14 | 1 clickable wall | 0x07 | 255 |
| 65 | 4 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 68 | 8 | — | 24 | 1 clickable wall | 0x80 | 63 |
| 69 | 2 | 1 | 16 | 1 clickable wall | 0x07 | 210 |
| 73 | 4 | — | 30 |  | 0x04 | 63 |
| 74 | 4 | — | 32 |  | 0x06 | 63 |
| 75 | 4 | — | 29 |  | 0x86 | 63 |
| 76 | 16 | 1 | 8 | 4 click runs script | 0x84 | 214 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 108 (x 12, y 3) | south | 51 | clickable wall |
| 117 (x 21, y 3) | south | 55 | clickable wall |
| 133 (x 5, y 4) | south | 64 | clickable wall |
| 158 (x 30, y 4) | west | 69 | clickable wall |
| 167 (x 7, y 5) | west | 69 | clickable wall |
| 184 (x 24, y 5) | south | 62 | clickable wall |
| 187 (x 27, y 5) | west | 50 | clickable wall |
| 193 (x 1, y 6) | north | 68 | clickable wall |
| 193 (x 1, y 6) | east | 68 | clickable wall |
| 193 (x 1, y 6) | south | 68 | clickable wall |
| 193 (x 1, y 6) | west | 68 | clickable wall |
| 199 (x 7, y 6) | east | 54 | clickable wall |
| 236 (x 12, y 7) | west | 46 | clickable wall |
| 242 (x 18, y 7) | west | 64 | clickable wall |
| 247 (x 23, y 7) | north | 51 | clickable wall |
| 265 (x 9, y 8) | south | 46 | clickable wall |
| 267 (x 11, y 8) | south | 53 | clickable wall |
| 277 (x 21, y 8) | east | 50 | clickable wall |
| 293 (x 5, y 9) | east | 51 | clickable wall |
| 302 (x 14, y 9) | west | 46 | clickable wall |
| 312 (x 24, y 9) | south | 46 | clickable wall |
| 314 (x 26, y 9) | east | 55 | clickable wall |
| 317 (x 29, y 9) | east | 46 | clickable wall |
| 322 (x 2, y 10) | east | 46 | clickable wall |
| 332 (x 12, y 10) | east | 53 | clickable wall |
| 339 (x 19, y 10) | east | 55 | clickable wall |
| 368 (x 16, y 11) | west | 64 | clickable wall |
| 370 (x 18, y 11) | south | 53 | clickable wall |
| 383 (x 31, y 11) | west | 55 | clickable wall |
| 405 (x 21, y 12) | east | 55 | clickable wall |
| 410 (x 26, y 12) | west | 55 | clickable wall |
| 427 (x 11, y 13) | north | 62 | clickable wall |
| 433 (x 17, y 13) | south | 55 | clickable wall |
| 456 (x 8, y 14) | east | 62 | clickable wall |
| 482 (x 2, y 15) | north | 54 | clickable wall |
| 486 (x 6, y 15) | east | 52 | clickable wall |
| 505 (x 25, y 15) | south | 54 | clickable wall |
| 520 (x 8, y 16) | north | 76 | click runs script |
| 520 (x 8, y 16) | east | 76 | click runs script |
| 520 (x 8, y 16) | south | 76 | click runs script |
| 520 (x 8, y 16) | west | 76 | click runs script |
| 534 (x 22, y 16) | north | 76 | click runs script |
| 534 (x 22, y 16) | east | 76 | click runs script |
| 534 (x 22, y 16) | south | 76 | click runs script |
| 534 (x 22, y 16) | west | 76 | click runs script |
| 542 (x 30, y 16) | west | 54 | clickable wall |
| 569 (x 25, y 17) | east | 65 | clickable wall |
| 580 (x 4, y 18) | east | 53 | clickable wall |
| 584 (x 8, y 18) | south | 55 | clickable wall |
| 587 (x 11, y 18) | south | 46 | clickable wall |
| 598 (x 22, y 18) | west | 54 | clickable wall |
| 625 (x 17, y 19) | north | 76 | click runs script |
| 625 (x 17, y 19) | east | 76 | click runs script |
| 625 (x 17, y 19) | south | 76 | click runs script |
| 625 (x 17, y 19) | west | 76 | click runs script |
| 627 (x 19, y 19) | north | 76 | click runs script |
| 627 (x 19, y 19) | east | 76 | click runs script |
| 627 (x 19, y 19) | south | 76 | click runs script |
| 627 (x 19, y 19) | west | 76 | click runs script |
| 637 (x 29, y 19) | north | 65 | clickable wall |
| 643 (x 3, y 20) | north | 54 | clickable wall |
| 649 (x 9, y 20) | north | 68 | clickable wall |
| 649 (x 9, y 20) | east | 68 | clickable wall |
| 649 (x 9, y 20) | south | 68 | clickable wall |
| 649 (x 9, y 20) | west | 68 | clickable wall |
| 666 (x 26, y 20) | east | 65 | clickable wall |
| 693 (x 21, y 21) | west | 54 | clickable wall |
| 717 (x 13, y 22) | north | 54 | clickable wall |
| 732 (x 28, y 22) | north | 65 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL10.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x008B` | — | loads wall tiles FOREST1; loads monster sprites ORC.SHP into slot 0; loads monster sprites PENTROG.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x0137` | — | places a monster of type slot 1 on block 619 in mode 3; places a monster of type slot 1 on block 613 in mode 3; places a monster of type slot 2 on block 418 in mode 3; places a monster of type slot 2 on block 421 in mode 3; places a monster of type slot 2 on block 165 in mode 3; places a monster of type slot 2 on block 536 in mode 3; places a monster of type slot 2 on block 156 in mode 3; places item 116 (Star "Shining") on block 321 … |

### LEVEL10.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 108 (x 12, y 3) | `0x0ED6` | wall clicked | tests game flag 503 |
| block 117 (x 21, y 3) | `0x0F4E` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 129 (x 1, y 4) | `0x0614` | party steps in, party arrives (second path), item put down | moves items from block 129 to level 11, block 641 |
| block 133 (x 5, y 4) | `0x0F06` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 157 (x 29, y 4) | `0x0610` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 993 |
| block 158 (x 30, y 4) | `0x060C` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 993 |
| block 161 (x 1, y 5) | `0x05FA` | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 308; plays chat/dialogue text ID 0x0006; tests game flag 308 |
| block 166 (x 6, y 5) | `0x0608` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 167 (x 7, y 5) | `0x0604` | party arrives (second path), wall clicked | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 184 (x 24, y 5) | `0x0E81` | wall clicked | tests game flag 497 |
| block 187 (x 27, y 5) | `0x0EB4` | wall clicked | tests game flag 501 |
| block 199 (x 7, y 6) | `0x0E16` | wall clicked | tests game flag 495 |
| block 236 (x 12, y 7) | `0x0DB8` | wall clicked | tests game flag 487 |
| block 242 (x 18, y 7) | `0x0F66` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 247 (x 23, y 7) | `0x0EC6` | wall clicked | tests game flag 502 |
| block 265 (x 9, y 8) | `0x0D81` | wall clicked | tests game flag 482 |
| block 267 (x 11, y 8) | `0x0FDE` | wall clicked | plays chat/dialogue text ID 0x0052 |
| block 277 (x 21, y 8) | `0x0EA2` | wall clicked | tests game flag 500 |
| block 293 (x 5, y 9) | `0x0EE6` | wall clicked | tests game flag 504 |
| block 302 (x 14, y 9) | `0x0D8C` | wall clicked | tests game flag 483 |
| block 312 (x 24, y 9) | `0x0DAD` | wall clicked | tests game flag 486 |
| block 314 (x 26, y 9) | `0x0F1E` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 317 (x 29, y 9) | `0x0D97` | wall clicked | tests game flag 484 |
| block 322 (x 2, y 10) | `0x0DA2` | wall clicked | tests game flag 485 |
| block 330 (x 10, y 10) | `0x06B3` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 330 to type 0; sets the north wall of block 992 to type 1; sets the north wall of block 0 to type 0; sets the north wall of block 0 to type 4; takes 5 crown(s); sets the north wall of block 0 to type 3; requests engine global change, selector 10, operands 0, 2; plays music track 309 … |
| block 332 (x 12, y 10) | `0x0FF6` | wall clicked | plays chat/dialogue text ID 0x0052 |
| block 339 (x 19, y 10) | `0x0F36` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 362 (x 10, y 11) | `0x07A2` | wall clicked | gives 1 crown(s); sets the north wall of block 0 to type 1; sets the north wall of block 0 to type 5; places or moves item handle ? to level 10, block 556; gives item ? (?) if inventory placement succeeds; puts item ? (?) on an empty cursor; places or moves item handle 198 to level 10, block 556; gives item 198 (Dawn's Key) if inventory placement succeeds … |
| block 368 (x 16, y 11) | `0x0F7E` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 370 (x 18, y 11) | `0x1026` | wall clicked | plays chat/dialogue text ID 0x0052 |
| block 405 (x 21, y 12) | `0x0F96` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 410 (x 26, y 12) | `0x0FAE` | wall clicked | plays chat/dialogue text ID 0x0051 |
| block 427 (x 11, y 13) | `0x0E8C` | wall clicked | tests game flag 498 |
| block 456 (x 8, y 14) | `0x0E97` | wall clicked | tests game flag 499 |
| block 482 (x 2, y 15) | `0x0E0B` | wall clicked | tests game flag 494 |
| block 485 (x 5, y 15) | `0x05F8` | party arrives (second path), party leaves, bits 0x10 (no engine caller found) | no action summarized |
| block 486 (x 6, y 15) | `0x0EF6` | wall clicked | tests game flag 505 |
| block 505 (x 25, y 15) | `0x0DE4` | wall clicked | tests game flag 491 |
| block 542 (x 30, y 16) | `0x0E01` | wall clicked | tests game flag 493 |
| block 543 (x 31, y 16) | `0x100E` | wall clicked | plays chat/dialogue text ID 0x0052 |
| block 556 (x 12, y 17) | `0x09E2` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; requests engine global change, selector 10, operands 0, 2; plays music track 282; sets game flag 73; plays chat/dialogue text ID 0x0018; plays chat/dialogue text ID 0x001a; plays chat/dialogue text ID 0x0025; requests engine global change, selector 1, operands 0, 1 … |
| block 557 (x 13, y 17) | `0x0CDA` | wall clicked | places or moves item handle 211 to level 10, block 556; gives item 211 (Empty flask) if inventory placement succeeds; puts item 211 (Empty flask) on an empty cursor; places or moves item handle 264 to level 10, block 556; gives item 264 (Vaelan's Cube) if inventory placement succeeds; puts item 264 (Vaelan's Cube) on an empty cursor; creates item type 211 and returns its handle; place inventory item in hand … |
| block 569 (x 25, y 17) | `0x103E` | wall clicked | plays chat/dialogue text ID 0x0053 |
| block 580 (x 4, y 18) | `0x0FC6` | wall clicked | plays chat/dialogue text ID 0x0052 |
| block 587 (x 11, y 18) | `0x0DC3` | wall clicked | tests game flag 488 |
| block 588 (x 12, y 18) | `0x0BB0` | wall clicked | requests engine global change, selector 0, operands 0, 556; requests engine global change, selector 1, operands 0, 0; plays music track 261; plays chat/dialogue text ID 0x001c; plays chat/dialogue text ID 0x003f; plays chat/dialogue text ID 0x0041; plays chat/dialogue text ID 0x0040; tests game flag 311 … |
| block 598 (x 22, y 18) | `0x0DEF` | wall clicked | tests game flag 492 |
| block 625 (x 17, y 19) | `0x0698` | wall clicked | sets game flag 302; plays chat/dialogue text ID 0x0007; tests game flag 302 |
| block 637 (x 29, y 19) | `0x1056` | wall clicked | plays chat/dialogue text ID 0x0053 |
| block 643 (x 3, y 20) | `0x0DCE` | wall clicked | tests game flag 489 |
| block 666 (x 26, y 20) | `0x1086` | wall clicked | plays chat/dialogue text ID 0x0053 |
| block 681 (x 9, y 21) | `0x05EE` | party arrives (second path) | sets game flag 306; plays chat/dialogue text ID 0x0003; tests game flag 306 |
| block 693 (x 21, y 21) | `0x0DD9` | wall clicked | tests game flag 490 |
| block 701 (x 29, y 21) | `0x0621` | party steps in | sets the north wall of block 992 to type 0 |
| block 702 (x 30, y 21) | `0x0626` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 0; sets the north wall of block 992 to type 1; requests engine global change, selector 10, operands 0, 2; sets game flag 303; plays chat/dialogue text ID 0x0042; tests game flag 303 |
| block 703 (x 31, y 21) | `0x0661` | party steps in, party arrives (second path), wall clicked | moves items from block ? to level 12, block 412 |
| block 713 (x 9, y 22) | `0x0589` | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; requests engine global change, selector 10, operands 0, 0 |
| block 717 (x 13, y 22) | `0x0E28` | wall clicked | deals damage to target ? (amount 2); sets game flag 496; plays chat/dialogue text ID 0x0050; paralyze poison character; tests game flag 496 |
| block 732 (x 28, y 22) | `0x106E` | wall clicked | plays chat/dialogue text ID 0x0053 |
| block 745 (x 9, y 23) | `0x05C3` | party steps in, wall clicked | shows text ID 0x403f; requests engine global change, selector 0, operands 0, 713; requests engine global change, selector 10, operands 0, 0; plays chat/dialogue text ID ? |
| `0x400` level loaded | `0x0514` | — | sets music theme 261; sets script timer 0 to 3600 ticks |
| `0x401` script timer 0 | `0x0524` | — | places a monster of type slot 2 on block 518 in mode 4; places a monster of type slot 1 on block 590 in mode 4; places a monster of type slot 1 on block 675 in mode 4; places a monster of type slot 2 on block 472 in mode 4; places a monster of type slot 2 on block 394 in mode 4; creates item type 0 and returns its handle; give item to monster; clears game flag 130 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 116 | Star "Shining" | 10 | 321 |
| INI entry 1 (runs when the level loads) | 101 | Smooth rock | 10 | 549 |
| INI entry 1 (runs when the level loads) | 84 | Long sword "Flayer" | 10 | 472 |
| INI entry 1 (runs when the level loads) | 62 | Great maul "Pillage" | 10 | 732 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 619 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 619 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 613 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 613 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 418 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 421 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 165 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 536 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 156 | 3 | 2 | 3 |
| `0x401` script timer 0 | 518 | 1 | 2 | 4 |
| `0x401` script timer 0 | 590 | 2 | 1 | 4 |
| `0x401` script timer 0 | 590 | 2 | 1 | 4 |
| `0x401` script timer 0 | 675 | 1 | 1 | 4 |
| `0x401` script timer 0 | 675 | 1 | 1 | 4 |
| `0x401` script timer 0 | 472 | 1 | 2 | 4 |
| `0x401` script timer 0 | 394 | 1 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 9, y 23 | 1 | x 9, y 21 | 0x41d9 | LAKE DREAD |
| x 1, y 4 | 7 | x 1, y 5 | 0x41e1 | SWAMP |
| x 10, y 10 | 5 | x 10, y 10 | 0x41e2 | BEGGAR |
| x 12, y 17 | 3 | x 12, y 17 | 0x41e3 | DROEK'S WAGON |
| x 31, y 21 | 8 | x 30, y 21 | 0x41e4 | URBISH MINES |

## Text shown by the scripts (ids only)

- Level text file `LEVEL10.<lang>`: 30 ids: 3, 6, 7, 9, 10, 11, 14, 15, 20, 23, 24, 26, 28, 35, 37, 40, 41, 44, 46, 49, 58, 61, 63, 64, 65, 66, 80, 81, 82, 83.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL10.ENG --index N`.
