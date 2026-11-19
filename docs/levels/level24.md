# Level 24

Made by `tools/level_report.py` from `LEVEL24.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 9 bytes per block in the CMZ.
- Area (WLL header): 1 = FOREST1 (decorations `FOREST1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: FOREST1 with palette ALTPAL1.PAL (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 925 | — | — |  | 0x80 | 63 |
| 1 | 1561 | 1 | 8 |  | 0x07 | 255 |
| 2 | 1556 | 2 | 9 |  | 0x07 | 255 |
| 46 | 4 | 1 | 12 | 1 clickable wall | 0x07 | 255 |
| 47 | 4 | — | 33 | 1 clickable wall | 0x07 | 63 |
| 51 | 1 | 1 | 27 | 1 clickable wall | 0x07 | 255 |
| 53 | 4 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 54 | 5 | 2 | 41 | 1 clickable wall | 0x07 | 255 |
| 55 | 9 | 2 | 42 | 1 clickable wall | 0x07 | 255 |
| 56 | 4 | — | 39 |  | 0x86 | 63 |
| 57 | 8 | — | 38 |  | 0x84 | 63 |
| 58 | 4 | — | — | 1 clickable wall | 0x06 | 63 |
| 63 | 4 | 1 | 7 |  | 0x84 | 192 |
| 65 | 2 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 69 | 1 | 1 | 16 | 1 clickable wall | 0x07 | 210 |
| 77 | 4 | — | 31 |  | 0x86 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 176 (x 16, y 5) | east | 54 | clickable wall |
| 232 (x 8, y 7) | east | 54 | clickable wall |
| 284 (x 28, y 8) | north | 46 | clickable wall |
| 302 (x 14, y 9) | east | 46 | clickable wall |
| 331 (x 11, y 10) | east | 55 | clickable wall |
| 337 (x 17, y 10) | east | 46 | clickable wall |
| 395 (x 11, y 12) | north | 51 | clickable wall |
| 427 (x 11, y 13) | north | 58 | clickable wall |
| 427 (x 11, y 13) | east | 58 | clickable wall |
| 427 (x 11, y 13) | south | 58 | clickable wall |
| 427 (x 11, y 13) | west | 58 | clickable wall |
| 443 (x 27, y 13) | west | 53 | clickable wall |
| 462 (x 14, y 14) | north | 55 | clickable wall |
| 511 (x 31, y 15) | west | 54 | clickable wall |
| 538 (x 26, y 16) | east | 46 | clickable wall |
| 566 (x 22, y 17) | south | 55 | clickable wall |
| 575 (x 31, y 17) | west | 54 | clickable wall |
| 659 (x 19, y 20) | east | 54 | clickable wall |
| 666 (x 26, y 20) | west | 55 | clickable wall |
| 685 (x 13, y 21) | west | 55 | clickable wall |
| 715 (x 11, y 22) | north | 69 | clickable wall |
| 724 (x 20, y 22) | east | 53 | clickable wall |
| 730 (x 26, y 22) | south | 55 | clickable wall |
| 739 (x 3, y 23) | north | 53 | clickable wall |
| 746 (x 10, y 23) | north | 47 | clickable wall |
| 746 (x 10, y 23) | east | 47 | clickable wall |
| 746 (x 10, y 23) | south | 47 | clickable wall |
| 746 (x 10, y 23) | west | 47 | clickable wall |
| 780 (x 12, y 24) | south | 55 | clickable wall |
| 824 (x 24, y 25) | north | 55 | clickable wall |
| 828 (x 28, y 25) | north | 55 | clickable wall |
| 847 (x 15, y 26) | south | 65 | clickable wall |
| 873 (x 9, y 27) | east | 65 | clickable wall |
| 877 (x 13, y 27) | east | 53 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL24.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles FOREST1; loads monster sprites GRTORC.SHP into slot 0; loads monster sprites LIZARD.SHP into slot 1; defines monster type 3; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x00F8` | — | places a monster of type slot 2 on block 210 in mode 3; places a monster of type slot 2 on block 338 in mode 3; places a monster of type slot 2 on block 340 in mode 3; creates item type 264 and returns its handle; give item to monster |

### LEVEL24.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 141 (x 13, y 4) | `0x0A35` | wall clicked | tests game flag 529 |
| block 176 (x 16, y 5) | `0x09F0` | wall clicked | tests game flag 523 |
| block 185 (x 25, y 5) | `0x0A47` | wall clicked | tests game flag 530 |
| block 189 (x 29, y 5) | `0x0A59` | wall clicked | loads cut-scene ?.TIM into slot ?; sets the west wall of block 746 to type ?; sets the south wall of block 746 to type 0; loads cut-scene UNBAR1.TIM into slot 1; loads cut-scene UNBAR2.TIM into slot 2; sets the south wall of block 746 to type 47; sets all four walls of block 746 to type 0; deletes the held item … |
| block 232 (x 8, y 7) | `0x0A06` | wall clicked | tests game flag 525 |
| block 272 (x 16, y 8) | `0x08AA` | party steps in, party arrives (second path), wall clicked | sets the north wall of block 32 to type 4; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 273; starts a dialogue sequence in mode 0; plays chat/dialogue text ID 0x0014; shows text ID 0x403f; plays chat/dialogue text ID 0x0001; plays chat/dialogue text ID 0x0002 … |
| block 273 (x 17, y 8) | `0x078C` | party steps in, party arrives (second path), party leaves, wall clicked, bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; plays music track 294; sets game flag 421; plays chat/dialogue text ID 0x0000; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 273; shows text ID 0x403f; plays music track 329 … |
| block 274 (x 18, y 8) | `0x06B7` | party arrives (second path) | sets the north wall of block 32 to type 2; find inventory item; sets monster ? facing to 0; sets monster ? mode to 7; sets monster ? facing to 2; tests game flag 421 |
| block 276 (x 20, y 8) | `0x069C` | party arrives (second path) | find inventory item; sets script timer 1 to 3600 ticks; sets monster ? facing to 2; sets monster ? mode to 7; sets monster ? facing to 0 |
| block 284 (x 28, y 8) | `0x09E5` | wall clicked | tests game flag 522 |
| block 302 (x 14, y 9) | `0x09DA` | wall clicked | tests game flag 521 |
| block 328 (x 8, y 10) | `0x0A23` | wall clicked | tests game flag 528 |
| block 337 (x 17, y 10) | `0x09C4` | wall clicked | tests game flag 519 |
| block 395 (x 11, y 12) | `0x06E1` | item put down | sets all four walls of block 395 to type 0; delete level item |
| block 427 (x 11, y 13) | `0x0704` | party arrives (second path), wall clicked, item put down, fireball passes, thrown item hits | moves the party to level 26, block 427, facing 2; places or moves item handle ? to level 26, block 427; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 395; plays a sound (ID 137) |
| block 443 (x 27, y 13) | `0x0D55` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 538 (x 26, y 16) | `0x09CF` | wall clicked | tests game flag 520 |
| block 566 (x 22, y 17) | `0x0CAD` | wall clicked | plays chat/dialogue text ID 0x0025 |
| block 575 (x 31, y 17) | `0x09FB` | wall clicked | tests game flag 524 |
| block 610 (x 2, y 19) | `0x064D` | item put down | moves items from block 610 to level 22, block 971 |
| block 642 (x 2, y 20) | `0x0659` | party steps in, party arrives (second path), item put down | moves the party to level 22, block 971, facing 0; moves items from block 610 to level 22, block 971; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 674; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 10, operands 0, 2 |
| block 657 (x 17, y 20) | `0x05D1` | party steps in, party arrives (second path), wall clicked | plays chat/dialogue text ID 0x0010; plays chat/dialogue text ID 0x0011; moves items from block ? to level 18, block 588 |
| block 659 (x 19, y 20) | `0x0D3D` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 683 (x 11, y 21) | `0x0765` | bits 0x400 (no engine caller found) | puts item 132 (Shield of Stealth) on an empty cursor; puts item 25 (Arbalest "Equalizer") on an empty cursor |
| block 689 (x 17, y 21) | `0x059F` | party steps in, party arrives (second path), bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; sets game flag 320; plays chat/dialogue text ID 0x000f; tests game flag 320 |
| block 695 (x 23, y 21) | `0x0A11` | wall clicked | tests game flag 527 |
| block 715 (x 11, y 22) | `0x073E` | wall clicked | puts item 132 (Shield of Stealth) on an empty cursor; puts item 25 (Arbalest "Equalizer") on an empty cursor |
| block 721 (x 17, y 22) | `0x059A` | party steps in | no action summarized |
| block 724 (x 20, y 22) | `0x0D25` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 730 (x 26, y 22) | `0x0CF5` | wall clicked | plays chat/dialogue text ID 0x0025 |
| block 739 (x 3, y 23) | `0x0D6D` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 778 (x 10, y 24) | `0x0B3D` | party arrives (second path), bits 0x410 (no engine caller found) | sets the south wall of block 746 to type 47; sets the west wall of block 746 to type 0; sets the east wall of block 746 to type 0; sets game flag 581; checks the south wall of block 746; tests game flag 581 |
| block 824 (x 24, y 25) | `0x0CC5` | wall clicked | plays chat/dialogue text ID 0x0025 |
| block 828 (x 28, y 25) | `0x0CDD` | wall clicked | plays chat/dialogue text ID 0x0025 |
| block 846 (x 14, y 26) | `0x0B68` | party arrives (second path), bits 0x10 (no engine caller found) | places item 198 (Dawn's Key) on block 1021; loads cut-scene DAWN_LIZ.TIM into slot 0; places a monster of type slot 3 on block 878 in mode 7; sets game flag 312; plays music track 313; plays chat/dialogue text ID 0x001a; plays chat/dialogue text ID 0x001c; remove inventory item … |
| block 847 (x 15, y 26) | `0x0D9D` | wall clicked | plays chat/dialogue text ID 0x0023 |
| block 873 (x 9, y 27) | `0x0D85` | wall clicked | plays chat/dialogue text ID 0x0023 |
| block 877 (x 13, y 27) | `0x0D0D` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 878 (x 14, y 27) | `0x0C7B` | party steps in | requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 846; shows text ID 0x403f; tests game flag 586; tests game flag 312 |
| block 942 (x 14, y 29) | `0x0641` | party steps in, party arrives (second path), item put down | moves items from block 942 to level 17, block 110 |
| `0x400` level loaded | `0x03AB` | — | sets music theme 329; sets script timer 0 to 14400 ticks; sets script timer 1 to 14400 ticks |
| `0x401` script timer 0 | `0x03BF` | — | places a monster of type slot 1 on block 905 in mode 4; places a monster of type slot 1 on block 753 in mode 4; places a monster of type slot 1 on block 734 in mode 4; places a monster of type slot 1 on block 473 in mode 4; places a monster of type slot 1 on block 414 in mode 4; places a monster of type slot 1 on block 221 in mode 4; places a monster of type slot 1 on block 213 in mode 4; places a monster of type slot 1 on block 329 in mode 4 … |
| `0x402` script timer 1 | `0x0543` | — | places a monster of type slot 1 on block 373 in mode 4; places a monster of type slot 1 on block 209 in mode 4; tests game flag 356 |
| `0x404` a monster died | `0x0394` | — | loads cut-scene LIZ_BIRD.TIM into slot 0; sets monster ? flag bits 0x0; suspend monster |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| block 846 (x 14, y 26) | 198 | Dawn's Key | 29 | 1021 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 210 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 210 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 338 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 338 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 340 | 2 | 2 | 3 |
| block 846 (x 14, y 26) | 878 | 0 | 3 | 7 |
| `0x401` script timer 0 | 905 | 1 | 1 | 4 |
| `0x401` script timer 0 | 905 | 1 | 1 | 4 |
| `0x401` script timer 0 | 753 | 1 | 1 | 4 |
| `0x401` script timer 0 | 753 | 1 | 1 | 4 |
| `0x401` script timer 0 | 734 | 3 | 1 | 4 |
| `0x401` script timer 0 | 734 | 3 | 1 | 4 |
| `0x401` script timer 0 | 473 | 1 | 1 | 4 |
| `0x401` script timer 0 | 473 | 1 | 1 | 4 |
| `0x401` script timer 0 | 414 | 3 | 1 | 4 |
| `0x401` script timer 0 | 414 | 3 | 1 | 4 |
| `0x401` script timer 0 | 221 | 2 | 1 | 4 |
| `0x401` script timer 0 | 221 | 2 | 1 | 4 |
| `0x401` script timer 0 | 213 | 2 | 1 | 4 |
| `0x401` script timer 0 | 213 | 2 | 1 | 4 |
| `0x401` script timer 0 | 329 | 1 | 1 | 4 |
| `0x401` script timer 0 | 329 | 1 | 1 | 4 |
| `0x401` script timer 0 | 430 | 0 | 1 | 4 |
| `0x401` script timer 0 | 430 | 0 | 1 | 4 |
| `0x401` script timer 0 | 336 | 3 | 1 | 4 |
| `0x401` script timer 0 | 336 | 3 | 1 | 4 |
| `0x402` script timer 1 | 373 | 3 | 1 | 4 |
| `0x402` script timer 1 | 373 | 3 | 1 | 4 |
| `0x402` script timer 1 | 209 | 0 | 1 | 4 |
| `0x402` script timer 1 | 209 | 0 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 14, y 29 | 0 | x 14, y 28 | 0x41de | FOREST |
| x 2, y 20 | 2 | x 2, y 21 | 0x41ff | YVEL |
| x 16, y 8 | 1 | x 17, y 8 | 0x4200 | VULTURE'S CHASM |
| x 11, y 14 | 8 | x 11, y 13 | 0x4201 | CASTLE CIMMERIA |
| x 17, y 21 | 5 | x 17, y 22 | 0x41f1 | WHITE TOWER |
| x 10, y 24 | 4 | x 10, y 24 | 0x41f0 | SCOTIA'S BARRIER |

## Text shown by the scripts (ids only)

- Level text file `LEVEL24.<lang>`: 18 ids: 0, 1, 2, 3, 15, 16, 17, 18, 19, 20, 21, 26, 28, 31, 32, 35, 36, 37.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL24.ENG --index N`.
