# Level 15

Made by `tools/level_report.py` from `LEVEL15.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 15](../PROGRESSION.md#level-15) and [item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 6 = MINE1 (decorations `MINE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MINE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1086 | — | — |  | 0x80 | 63 |
| 8 | 10 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 25 | 8 | — | — |  | 0x84 | 63 |
| 35 | 4 | — | 25 |  | 0x80 | 10 |
| 37 | 12 | — | 23 |  | 0x80 | 63 |
| 40 | 1 | 6 | 59 | 1 clickable wall | 0x07 | 207 |
| 41 | 10 | 1 | 3 |  | 0x07 | 255 |
| 42 | 5 | 1 | 16 | 2 lever (to on) | 0x07 | 207 |
| 44 | 4 | — | — |  | 0x84 | 17 |
| 45 | 1 | 1 | 24 | 6 niche | 0x87 | 14 |
| 46 | 4 | 2 | — |  | 0x00 | 214 |
| 47 | 1 | 6 | 61 | 1 clickable wall | 0x07 | 207 |
| 48 | 1 | 2 | 70 | 1 clickable wall | 0x07 | 207 |
| 49 | 1 | 2 | 72 | 1 clickable wall | 0x07 | 207 |
| 50 | 1 | 2 | 73 | 1 clickable wall | 0x07 | 207 |
| 51 | 2 | 2 | 71 | 1 clickable wall | 0x07 | 207 |
| 53 | 912 | 1 | — |  | 0x07 | 255 |
| 54 | 873 | 2 | — |  | 0x07 | 255 |
| 55 | 922 | 6 | — |  | 0x07 | 255 |
| 56 | 1 | 1 | 9 | 1 clickable wall | 0x07 | 210 |
| 60 | 128 | — | 20 |  | 0x06 | 63 |
| 61 | 36 | — | 21 |  | 0x06 | 63 |
| 62 | 36 | — | 80 |  | 0x06 | 63 |
| 66 | 1 | 1 | 37 | 1 clickable wall | 0x07 | 255 |
| 70 | 2 | 1 | 34 | 1 clickable wall | 0x07 | 255 |
| 72 | 16 | — | 22 | 1 clickable wall | 0x06 | 255 |
| 73 | 5 | 1 | 18 | 1 clickable wall | 0x07 | 255 |
| 75 | 1 | 2 | 35 | 1 clickable wall | 0x07 | 255 |
| 78 | 4 | — | 81 |  | 0x06 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 0 (x 0, y 0) | north | 48 | clickable wall |
| 0 (x 0, y 0) | east | 49 | clickable wall |
| 0 (x 0, y 0) | south | 50 | clickable wall |
| 0 (x 0, y 0) | west | 51 | clickable wall |
| 38 (x 6, y 1) | west | 70 | clickable wall |
| 55 (x 23, y 1) | west | 45 | niche |
| 91 (x 27, y 2) | east | 73 | clickable wall |
| 109 (x 13, y 3) | east | 73 | clickable wall |
| 115 (x 19, y 3) | south | 42 | lever (to on) |
| 117 (x 21, y 3) | north | 40 | clickable wall |
| 124 (x 28, y 3) | north | 73 | clickable wall |
| 131 (x 3, y 4) | south | 66 | clickable wall |
| 260 (x 4, y 8) | east | 42 | lever (to on) |
| 291 (x 3, y 9) | south | 42 | lever (to on) |
| 366 (x 14, y 11) | north | 51 | clickable wall |
| 368 (x 16, y 11) | north | 75 | clickable wall |
| 390 (x 6, y 12) | west | 73 | clickable wall |
| 399 (x 15, y 12) | north | 72 | clickable wall |
| 399 (x 15, y 12) | east | 72 | clickable wall |
| 399 (x 15, y 12) | south | 72 | clickable wall |
| 399 (x 15, y 12) | west | 72 | clickable wall |
| 421 (x 5, y 13) | north | 73 | clickable wall |
| 424 (x 8, y 13) | south | 47 | clickable wall |
| 429 (x 13, y 13) | north | 56 | clickable wall |
| 517 (x 5, y 16) | north | 72 | clickable wall |
| 517 (x 5, y 16) | east | 72 | clickable wall |
| 517 (x 5, y 16) | south | 72 | clickable wall |
| 517 (x 5, y 16) | west | 72 | clickable wall |
| 536 (x 24, y 16) | north | 72 | clickable wall |
| 536 (x 24, y 16) | east | 72 | clickable wall |
| 536 (x 24, y 16) | south | 72 | clickable wall |
| 536 (x 24, y 16) | west | 72 | clickable wall |
| 879 (x 15, y 27) | north | 72 | clickable wall |
| 879 (x 15, y 27) | east | 72 | clickable wall |
| 879 (x 15, y 27) | south | 72 | clickable wall |
| 879 (x 15, y 27) | west | 72 | clickable wall |
| 914 (x 18, y 28) | south | 42 | lever (to on) |
| 944 (x 16, y 29) | west | 42 | lever (to on) |
| 980 (x 20, y 30) | north | 70 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL15.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0032` | — | loads wall tiles MINE1; loads monster sprites ROCKLING.SHP into slot 0; loads monster sprites AVIANWRM.SHP into slot 1; defines monster type 1; defines monster type 2; sets door state bit 0x20 on block 52 |
| INI entry 1 (runs when the level loads) | `0x00F2` | — | places a monster of type slot 2 on block 389 in mode 4; places a monster of type slot 1 on block 100 in mode 3; places a monster of type slot 1 on block 214 in mode 3; places a monster of type slot 1 on block 365 in mode 3; places a monster of type slot 1 on block 302 in mode 3; places a monster of type slot 1 on block 391 in mode 3; places a monster of type slot 1 on block 330 in mode 3; places a monster of type slot 1 on block 395 in mode 3 … |

### LEVEL15.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 37 (x 5, y 1) | `0x0622` | party arrives (second path), bits 0x400 (no engine caller found) | sets all four walls of block 38 to type 0; plays chat/dialogue text ID 0x0000; plays chat/dialogue text ID 0x0017; checks the west wall of block 38; plays a sound (ID 134) |
| block 52 (x 20, y 1) | `0x06D2` | party steps in, party arrives (second path), item put down | removes monsters from block 52; moves items from block 52 to level 12, block 246; plays a sound (ID 73) |
| block 91 (x 27, y 2) | `0x076F` | wall clicked | plays chat/dialogue text ID 0x0012; plays chat/dialogue text ID 0x0013; tests game flag 215 |
| block 92 (x 28, y 2) | `0x0729` | fireball passes | sets the north wall of block 124 to type 74; sets the east wall of block 91 to type 74; sets game flag 215; tests game flag 215 |
| block 109 (x 13, y 3) | `0x06B1` | wall clicked | plays chat/dialogue text ID 0x0012; plays chat/dialogue text ID 0x0013; tests game flag 214 |
| block 110 (x 14, y 3) | `0x0686` | fireball passes | sets the east wall of block 109 to type 74; sets game flag 214; tests game flag 214 |
| block 115 (x 19, y 3) | `0x06C7` | wall clicked | toggles all four walls of block 116 between types 0 and 1; plays a sound (ID 38) |
| block 117 (x 21, y 3) | `0x06DD` | wall clicked | deletes the held item; sets all four walls of block 118 to type 0; plays chat/dialogue text ID 0x0009; plays chat/dialogue text ID 0x4065; plays chat/dialogue text ID 0x000a; checks the north wall of block 118; plays a sound (ID 41); plays a sound (ID 40) … |
| block 124 (x 28, y 3) | `0x0759` | wall clicked | plays chat/dialogue text ID 0x0012; plays chat/dialogue text ID 0x0013; tests game flag 215 |
| block 131 (x 3, y 4) | `0x061B` | wall clicked | plays chat/dialogue text ID 0x0008 |
| block 227 (x 3, y 7) | `0x05F1` | party arrives (second path) | sets all four walls of block 227 to type 36; creates item type 10 and returns its handle; launches a projectile from block 163 in direction 2; checks the south wall of block 227; plays a sound (ID 80); plays a sound (ID 69) at block 163 |
| block 260 (x 4, y 8) | `0x0A59` | wall clicked | toggles the south wall of block 229 between types 45 and 1; plays a sound (ID 79) |
| block 261 (x 5, y 8) | `0x0A3A` | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 217; character surprise feedback; move party; clears game flag 217; tests game flag 217 |
| block 263 (x 7, y 8) | `0x0A2D` | party steps in, party arrives (second path), item put down | moves items from block 263 to level 14, block 360 |
| block 291 (x 3, y 9) | `0x05E6` | wall clicked | sets all four walls of block 291 to type 0; plays a sound (ID 38) |
| block 328 (x 8, y 10) | `0x0A20` | party steps in, party arrives (second path), item put down | moves items from block 328 to level 16, block 292 |
| block 330 (x 10, y 10) | `0x0A03` | party arrives (second path) | operates the door switch at block 425 with action 1; sets game flag 549; sets game flag 550; tests game flag 550; plays a sound (ID 80) |
| block 366 (x 14, y 11) | `0x0785` | wall clicked | sets the north wall of block 366 to type ?; checks the north wall of block 366; checks wall side ? of block 0; plays a sound (ID 30) |
| block 368 (x 16, y 11) | `0x07C0` | wall clicked | puts item 224 (Gold Jewel) on an empty cursor; operates the door switch at block 367 with action -1; sets the north wall of block 368 to type 75; deletes the held item; sets the north wall of block 368 to type 76; operates the door switch at block 367 with action 1; plays chat/dialogue text ID 0x000b; plays chat/dialogue text ID 0x0001 … |
| block 389 (x 5, y 12) | `0x058D` | fireball passes | sets the west wall of block 390 to type 74; sets the north wall of block 421 to type 74; sets game flag 213; tests game flag 213 |
| block 390 (x 6, y 12) | `0x05D0` | wall clicked | plays chat/dialogue text ID 0x0012; plays chat/dialogue text ID 0x0013; tests game flag 213 |
| block 393 (x 9, y 12) | `0x09EB` | party arrives (second path) | operates the door switch at block 425 with action -1; sets game flag 549; tests game flag 549; plays a sound (ID 80) |
| block 397 (x 13, y 12) | `0x099A` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x000d; checks the north wall of block 429 |
| block 399 (x 15, y 12) | `0x0821` | wall clicked | shows text ID 0x403f; requests engine global change, selector 0, operands 0, 367; tests game flag 217 |
| block 421 (x 5, y 13) | `0x05BA` | wall clicked | plays chat/dialogue text ID 0x0012; plays chat/dialogue text ID 0x0013; tests game flag 213 |
| block 424 (x 8, y 13) | `0x09A2` | wall clicked | operates the door switch at block 425 with action 1; plays chat/dialogue text ID 0x0009; shows text ID 0x4054; plays chat/dialogue text ID 0x000a; checks the north wall of block 425; plays a sound (ID 40); plays a sound (ID 41) |
| block 429 (x 13, y 13) | `0x099E` | wall clicked | plays chat/dialogue text ID 0x000d; checks the north wall of block 429 |
| block 431 (x 15, y 13) | `0x0847` | party steps in | sets all four walls of block 536 to type 60; sets all four walls of block 536 to type 72; operates the door switch at block 535 with action 1; sets all four walls of block 517 to type 60; sets all four walls of block 517 to type 72; operates the door switch at block 518 with action 1; sets all four walls of block 879 to type 60; sets all four walls of block 879 to type 72 … |
| block 516 (x 4, y 16) | `0x08B8` | party steps in | sets all four walls of block 399 to type 60; sets all four walls of block 399 to type 72; operates the door switch at block 367 with action 1; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 517; sets game flag 217; plays chat/dialogue text ID 0x000c; clears game flag 217 … |
| block 537 (x 25, y 16) | `0x095A` | party steps in | sets all four walls of block 399 to type 60; sets all four walls of block 399 to type 72; operates the door switch at block 367 with action 1; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 536; sets game flag 217; plays chat/dialogue text ID 0x000c; clears game flag 217 … |
| block 847 (x 15, y 26) | `0x0909` | party steps in | sets all four walls of block 399 to type 60; sets all four walls of block 399 to type 72; operates the door switch at block 367 with action 1; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 879; sets game flag 217; plays chat/dialogue text ID 0x000c; clears game flag 217 … |
| block 914 (x 18, y 28) | `0x0A70` | wall clicked | sets all four walls of block 914 to type 0; plays a sound (ID 38) |
| block 944 (x 16, y 29) | `0x0A65` | wall clicked | sets all four walls of block 944 to type 0; plays a sound (ID 38) |
| block 948 (x 20, y 29) | `0x0A7B` | party arrives (second path), bits 0x410 (no engine caller found) | places a monster of type slot 1 on block 819 in mode 7; sets the north wall of block 64 to type ?; places or moves item handle ? to level 15, block 948; sets game flag 218; plays chat/dialogue text ID 0x0007; creates item type 98 and returns its handle; plays chat/dialogue text ID 0x0016; tests game flag 218 … |
| block 980 (x 20, y 30) | `0x0AF5` | wall clicked | plays chat/dialogue text ID 0x0015; plays chat/dialogue text ID 0x0014; checks the north wall of block 64 |
| `0x400` level loaded | `0x051B` | — | drops the party through a pit; clears game flag 46; sets music theme 272; sets script timer 0 to 3600 ticks; sets game flag 216; tests game flag 46 |
| `0x401` script timer 0 | `0x053B` | — | places a monster of type slot 2 on block 389 in mode 4; places a monster of type slot 2 on block 110 in mode 4; places a monster of type slot 2 on block 124 in mode 4; tests game flag 213; tests game flag 214; tests game flag 215 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 173 | Silver key | 15 | 55 |
| INI entry 1 (runs when the level loads) | 257 | Note | 15 | 156 |
| INI entry 1 (runs when the level loads) | 209 | Shiney key | 15 | 229 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 15 | 168 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 15 | 50 |
| INI entry 1 (runs when the level loads) | 28 | Pick | 15 | 35 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 15 | 35 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 389 | 0 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 389 | 0 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 389 | 0 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 389 | 0 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 100 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 214 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 365 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 302 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 391 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 330 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 395 | 3 | 1 | 3 |
| block 948 (x 20, y 29) | 819 | 2 | 1 | 7 |
| `0x401` script timer 0 | 389 | 0 | 2 | 4 |
| `0x401` script timer 0 | 389 | 0 | 2 | 4 |
| `0x401` script timer 0 | 110 | 1 | 2 | 4 |
| `0x401` script timer 0 | 110 | 1 | 2 | 4 |
| `0x401` script timer 0 | 124 | 1 | 2 | 4 |
| `0x401` script timer 0 | 124 | 1 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 15, y 12 | 8 | x 15, y 12 | 0x41ed | MINE CAR |

## Text shown by the scripts (ids only)

- Level text file `LEVEL15.<lang>`: 18 ids: 0, 1, 2, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23.
- Global text `LANDS.<lang>`: 3 ids: 0x403f, 0x4054, 0x4065.

Read any of them with `tools/decode_dialogue.py LEVEL15.ENG --index N`.
