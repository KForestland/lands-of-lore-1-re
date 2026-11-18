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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and marks effects inferred from ScummVM **UNCONFIRMED** for DOS where applicable.

### LEVEL11.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x004A` | — | loads wall tiles SWAMP; loads monster sprites SWAMPMON.SHP into slot 0; loads monster sprites HURZELL.SHP into slot 0; loads monster sprites SWAMPCIT.SHP into slot 1; defines monster type 1; defines monster type 2; sets game flag 77; tests game flag 86 |
| INI entry 1 (runs when the level loads) | `0x0159` | — | places a monster of type slot 2 on block 135 in mode 2; places a monster of type slot 2 on block 515 in mode 2; places a monster of type slot 2 on block 668 in mode 2; places a monster of type slot 1 on block 545 in mode 3; places a monster of type slot 1 on block 449 in mode 3; places a monster of type slot 1 on block 521 in mode 3; places a monster of type slot 1 on block 357 in mode 3; places a monster of type slot 1 on block 268 in mode 3 … |

### LEVEL11.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 42 (x 10, y 1) | `0x1B49` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 45 (x 13, y 1) | `0x17B3` | wall clicked | places a monster of type slot 1 on block 659 in mode 4; sets the north wall of block 992 to type 0; moves the party to level 11, block 109, facing 3; places a monster of type slot 2 on block 109 in mode 7; gives item 220 (Ruby of Truth) if inventory placement succeeds; puts item 220 (Ruby of Truth) on an empty cursor; deletes the held item; places item 125 (Trident "Mantis") on block 109 … |
| block 77 (x 13, y 2) | `0x177A` | party steps in, wall clicked | requests engine global change, selector 0, operands 0, 109; shows text ID 0x403f; plays chat/dialogue text ID 0x005a; requests engine global change, selector 0, operands 0, 77; requests engine global change, selector 10, operands 0, 0; tests game flag 284; tests game flag 84; tests game flag 81 |
| block 104 (x 8, y 3) | `0x1CE3` | party arrives (second path) | tests game flag 84 |
| block 106 (x 10, y 3) | `0x1AE9` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 108 (x 12, y 3) | `0x1725` | party steps in | sets the north wall of block 992 to type 0; checks the north wall of block 992 |
| block 109 (x 13, y 3) | `0x1733` | party steps in, bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; sets the north wall of block 992 to type 0; checks the north wall of block 992 |
| block 113 (x 17, y 3) | `0x0E79` | party arrives (second path) | no action summarized |
| block 114 (x 18, y 3) | `0x0FB9` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 117 (x 21, y 3) | `0x0EC6` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 121 (x 25, y 3) | `0x1BA9` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 122 (x 26, y 3) | `0x1B91` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 131 (x 3, y 4) | `0x0EBF` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 135 (x 7, y 4) | `0x1CDF` | party arrives (second path) | tests game flag 84 |
| block 139 (x 11, y 4) | `0x1B01` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 163 (x 3, y 5) | `0x1BF1` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 165 (x 5, y 5) | `0x0E6F` | party arrives (second path) | no action summarized |
| block 167 (x 7, y 5) | `0x1094` | party arrives (second path), bits 0x10 (no engine caller found) | check equipped item script flags; plays chat/dialogue text ID 0x002f; sets up 1 dialogue choices; reads the dialogue result; sets game flag 270; move monster; sets game flag 271; tests game flag 271 |
| block 168 (x 8, y 5) | `0x1AD1` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 193 (x 1, y 6) | `0x0F9F` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 197 (x 5, y 6) | `0x0FAC` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 208 (x 16, y 6) | `0x0E97` | party arrives (second path) | no action summarized |
| block 209 (x 17, y 6) | `0x0F64` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 225 (x 1, y 7) | `0x0E65` | party arrives (second path) | no action summarized |
| block 248 (x 24, y 7) | `0x0ECC` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 264 (x 8, y 8) | `0x0F92` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 265 (x 9, y 8) | `0x0E5B` | party arrives (second path) | no action summarized |
| block 270 (x 14, y 8) | `0x1C81` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 272 (x 16, y 8) | `0x1C69` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 274 (x 18, y 8) | `0x0F12` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 275 (x 19, y 8) | `0x1BC1` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 277 (x 21, y 8) | `0x0EA1` | party arrives (second path) | no action summarized |
| block 281 (x 25, y 8) | `0x1A17` | wall clicked | no action summarized |
| block 282 (x 26, y 8) | `0x0F27` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 284 (x 28, y 8) | `0x0EB5` | party arrives (second path) | no action summarized |
| block 290 (x 2, y 9) | `0x1C09` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 309 (x 21, y 9) | `0x0F6F` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 316 (x 28, y 9) | `0x0FC5` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 321 (x 1, y 10) | `0x171D` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 993 |
| block 334 (x 14, y 10) | `0x1393` | wall clicked | sets the north wall of block 0 to type 83; sets the north wall of block 0 to type 0; deletes the held item; gives ? crown(s); gives item 39 (Crossbow) if inventory placement succeeds; puts item 39 (Crossbow) on an empty cursor; gives item 35 (Bow) if inventory placement succeeds; puts item 35 (Bow) on an empty cursor … |
| block 337 (x 17, y 10) | `0x1BD9` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 353 (x 1, y 11) | `0x1721` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 993 |
| block 358 (x 6, y 11) | `0x1CB1` | wall clicked | places a monster of type slot 2 on block 109 in mode 7; plays chat/dialogue text ID 0x0062; requests engine global change, selector 0, operands 0, 108; requests engine global change, selector 1, operands 0, 1; suspend monster; creates item type 220 and returns its handle; give item to monster; creates item type 125 and returns its handle … |
| block 366 (x 14, y 11) | `0x12E2` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; requests engine global change, selector 10, operands 0, 2; requests engine global change, selector 1, operands 0, 0; plays music track 283; requests engine global change, selector 0, operands 0, 398; requests engine global change, selector 1, operands 0, 2; plays music track 284; tests game flag 275 … |
| block 369 (x 17, y 11) | `0x0EE8` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 380 (x 28, y 11) | `0x0F19` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 409 (x 25, y 12) | `0x1B61` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 415 (x 31, y 12) | `0x1B79` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 418 (x 2, y 13) | `0x1C21` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 426 (x 10, y 13) | `0x1A59` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 432 (x 16, y 13) | `0x0E83` | party arrives (second path) | no action summarized |
| block 433 (x 17, y 13) | `0x0F57` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 434 (x 18, y 13) | `0x0ED3` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 448 (x 0, y 14) | `0x1B31` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 451 (x 3, y 14) | `0x1C39` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 452 (x 4, y 14) | `0x0EE1` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 453 (x 5, y 14) | `0x0E47` | party arrives (second path) | no action summarized |
| block 454 (x 6, y 14) | `0x0F3D` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 455 (x 7, y 14) | `0x1CEB` | party arrives (second path) | tests game flag 84 |
| block 463 (x 15, y 14) | `0x1A89` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 473 (x 25, y 14) | `0x0EAB` | party arrives (second path) | no action summarized |
| block 474 (x 26, y 14) | `0x0F7A` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 475 (x 27, y 14) | `0x1CEF` | party arrives (second path) | tests game flag 84 |
| block 487 (x 7, y 15) | `0x11D4` | wall clicked | gives ? crown(s); sets the north wall of block 0 to type 87; sets the north wall of block 0 to type 0; takes 300 crown(s); gives item 232 (Wand of Fireballs) if inventory placement succeeds; puts item 232 (Wand of Fireballs) on an empty cursor; requests engine global change, selector 0, operands 0, 551; requests engine global change, selector 1, operands 0, 2 … |
| block 490 (x 10, y 15) | `0x1A71` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 497 (x 17, y 15) | `0x0EEF` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 498 (x 18, y 15) | `0x0EF6` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 500 (x 20, y 15) | `0x1AA1` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 503 (x 23, y 15) | `0x0F20` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 515 (x 3, y 16) | `0x1CE7` | party arrives (second path) | tests game flag 84 |
| block 519 (x 7, y 16) | `0x1199` | party steps in, wall clicked | requests engine global change, selector 0, operands 0, 551; shows text ID 0x403f; starts a dialogue sequence in mode 0; plays music track 285; plays music track 284; requests engine global change, selector 0, operands 0, 519; requests engine global change, selector 10, operands 0, 0; tests game flag 84 |
| block 523 (x 11, y 16) | `0x0E51` | party arrives (second path) | no action summarized |
| block 530 (x 18, y 16) | `0x0EFD` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 531 (x 19, y 16) | `0x1AB9` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 545 (x 1, y 17) | `0x0F39` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 547 (x 3, y 17) | `0x0FD0` | party arrives (second path), bits 0x10 (no engine caller found) | plays chat/dialogue text ID 0x0001; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0002; plays chat/dialogue text ID 0x0003; move monster; sets game flag 269; tests game flag 269 |
| block 551 (x 7, y 17) | `0x10F3` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; sets the north wall of block 992 to type 0; requests engine global change, selector 10, operands 0, 2; checks the north wall of block 992 |
| block 553 (x 9, y 17) | `0x1A29` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 555 (x 11, y 17) | `0x0F4A` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 560 (x 16, y 17) | `0x0F04` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 561 (x 17, y 17) | `0x0E8D` | party arrives (second path) | no action summarized |
| block 577 (x 1, y 18) | `0x0F35` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 992 |
| block 583 (x 7, y 18) | `0x10E5` | party steps in | sets the north wall of block 992 to type 0; checks the north wall of block 992 |
| block 593 (x 17, y 18) | `0x0F85` | party arrives (second path) | deals damage to target ? (amount ?); paralyze poison character; shows text ID 0x005b |
| block 595 (x 19, y 18) | `0x1C51` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 604 (x 28, y 18) | `0x0F2E` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 611 (x 3, y 19) | `0x0E3E` | party arrives (second path) | sets game flag 255; plays chat/dialogue text ID 0x0000; tests game flag 255 |
| block 612 (x 4, y 19) | `0x0EDA` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 613 (x 5, y 19) | `0x1B19` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 617 (x 9, y 19) | `0x1A41` | wall clicked | plays chat/dialogue text ID 0x0063 |
| block 621 (x 13, y 19) | `0x0F0B` | party arrives (second path), wall clicked, item put down, fireball passes | deletes the held item; puts item 212 (Swamp Vial) on an empty cursor; plays a sound (ID 181) |
| block 628 (x 20, y 19) | `0x14BB` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | sets the north wall of block 992 to type 1; requests engine global change, selector 10, operands 0, 2; requests engine global change, selector 1, operands 0, 2; plays music track 283; requests engine global change, selector 0, operands 0, 660; requests engine global change, selector 0, operands 0, 596; requests engine global change, selector 1, operands 0, 0; plays music track 284 … |
| block 653 (x 13, y 20) | `0x1A20` | wall clicked | no action summarized |
| block 660 (x 20, y 20) | `0x15C7` | wall clicked | sets the north wall of block 0 to type 71; sets the north wall of block 0 to type 0; deletes the held item; gives ? crown(s); gives item 70 (Great sword) if inventory placement succeeds; puts item 70 (Great sword) on an empty cursor; gives item 52 (Great axe) if inventory placement succeeds; puts item 52 (Great axe) on an empty cursor … |
| block 668 (x 28, y 20) | `0x1CF3` | party arrives (second path) | tests game flag 84 |
| block 673 (x 1, y 21) | `0x0E31` | party steps in, party arrives (second path), item put down | moves items from block 673 to level 10, block 161 |
| block 689 (x 17, y 21) | `0x1C99` | wall clicked | plays chat/dialogue text ID 0x0062 |
| block 700 (x 28, y 21) | `0x1032` | party arrives (second path), bits 0x10 (no engine caller found) | plays chat/dialogue text ID 0x0001; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0002; plays chat/dialogue text ID 0x0003; move monster; sets game flag 269; tests game flag 269 |
| block 734 (x 30, y 22) | `0x19FF` | party arrives (second path) | plays chat/dialogue text ID 0x004b; sets game flag 590; tests game flag 590 |
| block 735 (x 31, y 22) | `0x19F2` | party steps in, party arrives (second path), item put down | moves items from block 735 to level 17, block 705 |
| `0x400` level loaded | `0x0BB7` | — | sets the north wall of block 992 to type 0; sets music theme 284; sets script timer 0 to 60 ticks; sets script timer 1 to 10800 ticks; sets script timer 2 to 8 ticks |
| `0x401` script timer 0 | `0x0BD3` | — | check equipped item script flags; move monster; sets game flag 271; tests game flag 270; tests game flag 271 |
| `0x402` script timer 1 | `0x0C05` | — | places a monster of type slot 2 on block 361 in mode 4; places a monster of type slot 2 on block 475 in mode 4; places a monster of type slot 2 on block 455 in mode 4; tests game flag 284; tests game flag 84 |
| `0x403` script timer 2 | `0x0C54` | — | update block animations2; tests game flag 418; checks the north wall of block 131; plays a sound (ID 107); checks the west wall of block 533; checks the south wall of block 553; checks the north wall of block 617; checks the west wall of block 463 … |

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
