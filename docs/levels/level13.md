# Level 13

Made by `tools/level_report.py` from `LEVEL13.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 6 = MINE1 (decorations `MINE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MINE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 800 | — | — |  | 0x80 | 63 |
| 1 | 400 | 1 | — |  | 0x07 | 255 |
| 2 | 400 | 2 | — |  | 0x07 | 255 |
| 8 | 4 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 27 | 1 | 1 | 7 | 2 lever (to on) | 0x07 | 207 |
| 31 | 3 | 2 | 14 | 2 lever (to on) | 0x07 | 207 |
| 32 | 2 | 2 | 15 | 3 lever (to off) | 0x07 | 207 |
| 38 | 8 | — | 4 |  | 0x84 | 11 |
| 41 | 4 | 1 | 3 |  | 0x07 | 255 |
| 45 | 2 | 1 | 24 | 6 niche | 0x87 | 14 |
| 46 | 21 | 1 | — |  | 0x84 | 214 |
| 47 | 3 | 1 | 59 | 1 clickable wall | 0x07 | 207 |
| 53 | 829 | 1 | — |  | 0x07 | 255 |
| 54 | 761 | 2 | — |  | 0x07 | 255 |
| 55 | 847 | 6 | — |  | 0x07 | 255 |
| 56 | 1 | 1 | 9 | 1 clickable wall | 0x07 | 210 |
| 60 | 1 | 1 | 6 | 1 clickable wall | 0x07 | 255 |
| 69 | 1 | 1 | 65 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 21 (x 21, y 0) | south | 32 | lever (to off) |
| 81 (x 17, y 2) | west | 47 | clickable wall |
| 83 (x 19, y 2) | east | 27 | lever (to on) |
| 85 (x 21, y 2) | north | 32 | lever (to off) |
| 294 (x 6, y 9) | west | 60 | clickable wall |
| 313 (x 25, y 9) | north | 31 | lever (to on) |
| 324 (x 4, y 10) | north | 47 | clickable wall |
| 343 (x 23, y 10) | east | 47 | clickable wall |
| 349 (x 29, y 10) | west | 31 | lever (to on) |
| 356 (x 4, y 11) | west | 31 | lever (to on) |
| 378 (x 26, y 11) | north | 45 | niche |
| 379 (x 27, y 11) | east | 45 | niche |
| 400 (x 16, y 12) | south | 69 | clickable wall |
| 560 (x 16, y 17) | north | 56 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL13.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0030` | — | loads wall tiles MINE1; loads monster sprites GIMLET.SHP into slot 0; loads monster sprites IRONGRZR.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x00E5` | — | places a monster of type slot 2 on block 147 in mode 4; places a monster of type slot 2 on block 107 in mode 4; places a monster of type slot 2 on block 485 in mode 3; places a monster of type slot 2 on block 456 in mode 3; places a monster of type slot 2 on block 493 in mode 3; places a monster of type slot 1 on block 497 in mode 4; places item 99 (Rock) on block 293; places item 92 (Mace "Puma") on block 369 … |

### LEVEL13.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 52 (x 20, y 1) | `0x03C6` | party arrives (second path), item put down | removes monsters from block 52; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 180, facing ?; moves items from block 52 to level 180, block 14; sets game flag 46; checks the north wall of block 52 |
| block 53 (x 21, y 1) | `0x0443` | party arrives (second path) | sets all four walls of block 52 to type 0 |
| block 81 (x 17, y 2) | `0x03BC` | wall clicked | plays chat/dialogue text ID -0x001 |
| block 83 (x 19, y 2) | `0x03CF` | wall clicked | sets all four walls of block 52 to type 38; removes monsters from block 52; sets all four walls of block 116 to type 0; places a monster of type slot 1 on block 116 in mode 4; sets all four walls of block 116 to type 44; places a monster of type slot 2 on block 116 in mode 4; sets all four walls of block 52 to type 0; moves items from block 52 to level 13, block 52 … |
| block 116 (x 20, y 3) | `0x044A` | party steps in, party arrives (second path), item put down | removes monsters from block 116; moves items from block 116 to level 12, block 246; move party; moves items from block 116 to level 14, block 332; checks the north wall of block 116; checks the south wall of block 21; checks the north wall of block 85; plays a sound (ID 73) |
| block 143 (x 15, y 4) | `0x03B0` | party steps in, party arrives (second path), item put down | moves items from block 143 to level 12, block 207 |
| block 227 (x 3, y 7) | `0x049D` | party steps in, party arrives (second path), item put down | moves items from block 227 to level 14, block 323 |
| block 282 (x 26, y 8) | `0x05A3` | item put down | sets all four walls of block 314 to type 0; sets all four walls of block 316 to type 0; checks the north wall of block 314; plays a sound (ID 37) |
| block 293 (x 5, y 9) | `0x04C9` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 340 to type 0; sets all four walls of block 372 to type 1; sets all four walls of block 340 to type 1; sets all four walls of block 372 to type 0; checks the north wall of block 372; plays a sound (ID 38) |
| block 294 (x 6, y 9) | `0x05F6` | wall clicked | plays chat/dialogue text ID 0x0002 |
| block 313 (x 25, y 9) | `0x0566` | wall clicked | sets all four walls of block 314 to type 0; sets all four walls of block 314 to type 38; removes monsters from block 314; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 442, facing ?; moves items from block 314 to level 14, block 442; sets game flag 46 … |
| block 314 (x 26, y 9) | `0x0570` | party arrives (second path), item put down | removes monsters from block 314; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 442, facing ?; moves items from block 314 to level 442, block 14; sets game flag 46; checks the north wall of block 314 |
| block 316 (x 28, y 9) | `0x05C8` | party arrives (second path), item put down | removes monsters from block 316; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 444, facing ?; moves items from block 316 to level 444, block 14; sets game flag 46; checks the north wall of block 316 |
| block 324 (x 4, y 10) | `0x04AA` | wall clicked | plays chat/dialogue text ID -0x001 |
| block 343 (x 23, y 10) | `0x0517` | wall clicked | sets all four walls of block 375 to type 0; deletes the held item; plays chat/dialogue text ID 0x0005; plays chat/dialogue text ID 0x0006; plays chat/dialogue text ID 0x4065; plays chat/dialogue text ID 0x0007; checks the east wall of block 375; plays a sound (ID 38) … |
| block 349 (x 29, y 10) | `0x05D2` | wall clicked | sets all four walls of block 316 to type 0; sets all four walls of block 316 to type 38; removes monsters from block 316; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 444, facing ?; sets the west wall of block 349 to type 32; moves items from block 316 to level 14, block 444 … |
| block 355 (x 3, y 11) | `0x04B5` | party arrives (second path), item put down | removes monsters from block 355; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 483, facing ?; moves items from block 355 to level 483, block 14; sets game flag 46; checks the north wall of block 355 |
| block 356 (x 4, y 11) | `0x04BF` | wall clicked | sets all four walls of block 355 to type 0; sets all four walls of block 355 to type 38; removes monsters from block 355; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 14, block 483, facing ?; moves items from block 355 to level 14, block 483; sets game flag 46 … |
| block 378 (x 26, y 11) | `0x057A` | item taken | sets all four walls of block 314 to type 38; moves items from block 314 to level 442, block 14; checks the north wall of block 314; plays a sound (ID 37) |
| block 400 (x 16, y 12) | `0x0510` | wall clicked | plays chat/dialogue text ID 0x0001 |
| block 528 (x 16, y 16) | `0x0601` | bits 0x400 (no engine caller found) | puts item 154 (Hale leather jerkin) on an empty cursor |
| block 560 (x 16, y 17) | `0x05FD` | wall clicked | puts item 154 (Hale leather jerkin) on an empty cursor |
| `0x400` level loaded | `0x035B` | — | sets music theme 288; sets script timer 0 to 3600 ticks; sets script timer 1 to 5400 ticks |
| `0x401` script timer 0 | `0x0371` | — | places a monster of type slot 1 on block 101 in mode 4; places a monster of type slot 1 on block 246 in mode 4 |
| `0x402` script timer 1 | `0x039B` | — | places a monster of type slot 2 on block 338 in mode 4; checks the north wall of block 372 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 13 | 293 |
| INI entry 1 (runs when the level loads) | 92 | Mace "Puma" | 13 | 369 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 13 | 246 |
| INI entry 1 (runs when the level loads) | 174 | Mine key 2 | 13 | 246 |
| INI entry 1 (runs when the level loads) | 274 | Emerald blade | 13 | 246 |
| INI entry 1 (runs when the level loads) | 105 | Saber "Wolf" | 13 | 369 |
| INI entry 1 (runs when the level loads) | 256 | Note | 13 | 162 |
| INI entry 1 (runs when the level loads) | 174 | Mine key 2 | 13 | 378 |
| INI entry 1 (runs when the level loads) | 175 | Mine key 3 | 13 | 379 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 147 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 107 | 1 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 485 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 456 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 493 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 497 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 497 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 497 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 497 | 1 | 1 | 4 |
| block 83 (x 19, y 2) | 116 | 3 | 1 | 4 |
| block 83 (x 19, y 2) | 116 | 3 | 2 | 4 |
| `0x401` script timer 0 | 101 | 0 | 1 | 4 |
| `0x401` script timer 0 | 101 | 0 | 1 | 4 |
| `0x401` script timer 0 | 246 | 0 | 1 | 4 |
| `0x401` script timer 0 | 246 | 0 | 1 | 4 |
| `0x402` script timer 1 | 338 | 2 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 27, y 21 | 0 | x 27, y 21 | 0x41eb | INVALID LOCATION |

## Text shown by the scripts (ids only)

- Level text file `LEVEL13.<lang>`: 6 ids: 1, 2, 5, 6, 7, 8.
- Global text `LANDS.<lang>`: 1 ids: 0x4065.

Read any of them with `tools/decode_dialogue.py LEVEL13.ENG --index N`.
