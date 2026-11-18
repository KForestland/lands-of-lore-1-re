# Level 8

Made by `tools/level_report.py` from `LEVEL8.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 598 | — | — |  | 0x80 | 63 |
| 1 | 1708 | 1 | — |  | 0x07 | 255 |
| 2 | 1708 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 12 | 4 | — |  | 0x04 | 25 |
| 24 | 12 | 5 | — |  | 0x04 | 26 |
| 29 | 1 | 2 | 66 | 2 lever (to on) | 0x07 | 207 |
| 33 | 5 | 2 | 72 | 2 lever (to on) | 0x07 | 207 |
| 35 | 4 | — | 20 |  | 0x80 | 10 |
| 37 | 12 | — | 22 |  | 0x80 | 63 |
| 39 | 8 | — | 19 |  | 0x80 | 11 |
| 41 | 2 | 1 | 45 |  | 0x07 | 255 |
| 42 | 1 | 1 | 15 | 2 lever (to on) | 0x07 | 207 |
| 45 | 1 | 1 | 50 | 6 niche | 0x87 | 14 |
| 46 | 4 | 2 | — |  | 0x00 | 214 |
| 48 | 1 | 1 | 46 | 1 clickable wall | 0x07 | 207 |
| 49 | 1 | 1 | 48 | 1 clickable wall | 0x07 | 207 |
| 53 | 3 | 1 | 26 | 1 clickable wall | 0x07 | 210 |
| 61 | 7 | 2 | 63 | 1 clickable wall | 0x07 | 255 |
| 71 | 1 | 1 | 53 | 1 clickable wall | 0x07 | 207 |
| 77 | 3 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 2 | 2 | 60 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 81 (x 17, y 2) | south | 48 | clickable wall |
| 155 (x 27, y 4) | east | 78 | clickable wall |
| 179 (x 19, y 5) | south | 61 | clickable wall |
| 189 (x 29, y 5) | east | 77 | clickable wall |
| 221 (x 29, y 6) | west | 77 | clickable wall |
| 222 (x 30, y 6) | north | 33 | lever (to on) |
| 222 (x 30, y 6) | east | 33 | lever (to on) |
| 222 (x 30, y 6) | south | 33 | lever (to on) |
| 222 (x 30, y 6) | west | 33 | lever (to on) |
| 236 (x 12, y 7) | south | 61 | clickable wall |
| 246 (x 22, y 7) | south | 61 | clickable wall |
| 251 (x 27, y 7) | east | 77 | clickable wall |
| 272 (x 16, y 8) | south | 61 | clickable wall |
| 277 (x 21, y 8) | north | 53 | clickable wall |
| 281 (x 25, y 8) | north | 33 | lever (to on) |
| 285 (x 29, y 8) | north | 78 | clickable wall |
| 335 (x 15, y 10) | south | 42 | lever (to on) |
| 342 (x 22, y 10) | west | 29 | lever (to on) |
| 411 (x 27, y 12) | north | 61 | clickable wall |
| 428 (x 12, y 13) | east | 71 | clickable wall |
| 440 (x 24, y 13) | north | 61 | clickable wall |
| 440 (x 24, y 13) | west | 53 | clickable wall |
| 501 (x 21, y 15) | north | 61 | clickable wall |
| 501 (x 21, y 15) | east | 53 | clickable wall |
| 538 (x 26, y 16) | north | 49 | clickable wall |
| 562 (x 18, y 17) | east | 45 | niche |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and marks effects inferred from ScummVM **UNCONFIRMED** for DOS where applicable.

### LEVEL8.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CAVE1; loads monster sprites SCAVNGR.SHP into slot 0; loads monster sprites FLSPIDER.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x00AA` | — | places a monster of type slot 2 on block 364 in mode 3; places a monster of type slot 2 on block 400 in mode 3; places a monster of type slot 2 on block 211 in mode 3; places a monster of type slot 2 on block 304 in mode 3; places a monster of type slot 2 on block 408 in mode 3; places a monster of type slot 2 on block 379 in mode 3; places item 44 (Dagger) on block 365; places item 29 (Axe) on block 376 … |

### LEVEL8.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 81 (x 17, y 2) | `0x0806` | wall clicked | deletes the held item; sets all four walls of block 114 to type 0; plays chat/dialogue text ID 0x0025; shows text ID 0x4054; plays chat/dialogue text ID 0x0027; plays a sound (ID 40); plays a sound (ID 38); plays a sound (ID 41) |
| block 115 (x 19, y 3) | `0x08C3` | party arrives (second path), bits 0x10 (no engine caller found) | sets all four walls of block 114 to type 1; plays chat/dialogue text ID 0x0002; sets game flag 153; sets game flag 154; plays chat/dialogue text ID 0x0003; tests game flag 153 |
| block 116 (x 20, y 3) | `0x0905` | party arrives (second path) | sets game flag 154; plays chat/dialogue text ID 0x0004; tests game flag 153; tests game flag 154 |
| block 124 (x 28, y 3) | `0x0AFF` | party steps in, party arrives (second path), item put down | moves items from block 124 to level 7, block 92 |
| block 179 (x 19, y 5) | `0x0C72` | wall clicked | plays chat/dialogue text ID 0x002f |
| block 207 (x 15, y 6) | `0x07F9` | party steps in, party arrives (second path), item put down | moves items from block 207 to level 7, block 206 |
| block 209 (x 17, y 6) | `0x07EB` | party arrives (second path) | sets the south wall of block 32 to type 1 |
| block 218 (x 26, y 6) | `0x0AF2` | party steps in, party arrives (second path), item put down | moves items from block 218 to level 9, block 217 |
| block 223 (x 31, y 6) | `0x0BE9` | wall clicked | deletes the held item; requests engine global change, selector 0, operands 0, 254; requests engine global change, selector 1, operands 0, 1; plays chat/dialogue text ID 0x0012; sets game flag 60; plays chat/dialogue text ID 0x0013; plays a sound (ID 118) |
| block 236 (x 12, y 7) | `0x0C6C` | wall clicked | plays chat/dialogue text ID 0x002f |
| block 245 (x 21, y 7) | `0x0922` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x0005; checks the north wall of block 277 |
| block 246 (x 22, y 7) | `0x0C7E` | wall clicked | plays chat/dialogue text ID 0x002f |
| block 254 (x 30, y 7) | `0x0B0A` | party steps in, party arrives (second path), wall clicked, item put down | loads cut-scene DRARCLE4.TIM into slot 0; moves items from block 254 to level 8, block 253; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 253; requests engine global change, selector 10, operands 0, 0; sets game flag 588; requests engine global change, selector 10, operands 0, 2; clears game flag 62 … |
| block 255 (x 31, y 7) | `0x0B5F` | party arrives (second path), wall clicked | loads cut-scene DRARCLE3.TIM into slot 0; sets game flag 309; requests engine global change, selector 0, operands 0, 156; requests engine global change, selector 1, operands 0, 1; requests engine global change, selector 0, operands 0, 253; plays music track 272; sets game flag 62; requests engine global change, selector 1, operands 0, 0 … |
| block 272 (x 16, y 8) | `0x0C78` | wall clicked | plays chat/dialogue text ID 0x002f |
| block 277 (x 21, y 8) | `0x0926` | wall clicked | plays chat/dialogue text ID 0x0005; checks the north wall of block 277 |
| block 281 (x 25, y 8) | `0x092A` | wall clicked | sets all four walls of block 280 to type 0 |
| block 311 (x 23, y 9) | `0x09A8` | party arrives (second path) | sets game flag 157 |
| block 312 (x 24, y 9) | `0x09AF` | party arrives (second path) | plays chat/dialogue text ID 0x0009; sets game flag 157; plays chat/dialogue text ID 0x000a; tests game flag 157 |
| block 335 (x 15, y 10) | `0x0860` | wall clicked | sets the west wall of block 368 to type 45; places item 234 (Freeze scroll) on block 368; checks the west wall of block 368; plays a sound (ID 38) |
| block 342 (x 22, y 10) | `0x099F` | wall clicked | toggles all four walls of block 311 between types 0 and 1 |
| block 366 (x 14, y 11) | `0x085C` | party arrives (second path) | character surprise feedback; move party |
| block 367 (x 15, y 11) | `0x0882` | party arrives (second path) | plays chat/dialogue text ID 0x0000; sets game flag 152; plays chat/dialogue text ID 0x0001; checks the south wall of block 335; tests game flag 152 |
| block 411 (x 27, y 12) | `0x0C84` | wall clicked | plays chat/dialogue text ID 0x002f |
| block 428 (x 12, y 13) | `0x096D` | wall clicked | sets the south wall of block 397 to type 45; places item 49 (Dagger "Razor") on block 397; places item 217 (Aloe) on block 397; sets game flag 49; tests game flag 49; plays a sound (ID 38) |
| block 437 (x 21, y 13) | `0x093F` | party arrives (second path), bits 0x10 (no engine caller found) | no action summarized |
| block 438 (x 22, y 13) | `0x0941` | party arrives (second path) | sets game flag 155; sets game flag 156; plays chat/dialogue text ID 0x002b; tests game flag 156 |
| block 439 (x 23, y 13) | `0x0969` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x0008; checks the west wall of block 440 |
| block 440 (x 24, y 13) | `0x095B` | wall clicked | plays chat/dialogue text ID 0x0008; plays chat/dialogue text ID 0x002f; checks the west wall of block 440 |
| block 442 (x 26, y 13) | `0x09E7` | party arrives (second path) | character surprise feedback; move party |
| block 495 (x 15, y 15) | `0x0932` | party steps in, party arrives (second path), item put down | moves items from block 495 to level 7, block 463 |
| block 501 (x 21, y 15) | `0x09EB` | wall clicked | plays chat/dialogue text ID 0x002f; plays chat/dialogue text ID 0x000b; checks the east wall of block 501 |
| block 502 (x 22, y 15) | `0x09FA` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x000b; checks the east wall of block 501 |
| block 509 (x 29, y 15) | `0x0AE5` | party steps in, party arrives (second path), item put down | moves items from block 509 to level 9, block 477 |
| block 538 (x 26, y 16) | `0x09FE` | wall clicked | sets all four walls of block 537 to type 0; deletes the held item; plays chat/dialogue text ID 0x002d; sets game flag 66; shows text ID 0x4054; plays chat/dialogue text ID 0x0026; plays chat/dialogue text ID 0x0027; tests game flag 66 … |
| block 562 (x 18, y 17) | `0x0A86` | item put down | places item 47 (Dagger "Back Biter") on block 562; sets game flag 65; delete level item; tests game flag 65 |
| block 563 (x 19, y 17) | `0x0AB8` | party arrives (second path), party leaves (second path), bits 0x10 (no engine caller found) | sets game flag 158; plays chat/dialogue text ID 0x000c; tests game flag 158 |
| block 566 (x 22, y 17) | `0x0A6F` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 566 to type 36; toggles the east wall of block 562 between types 45 and 1; checks the south wall of block 566; plays a sound (ID 80); plays a sound (ID 38) |
| block 592 (x 16, y 18) | `0x07F2` | party arrives (second path) | sets the south wall of block 32 to type 2 |
| `0x400` level loaded | `0x0735` | — | drops the party through a pit; clears game flag 46; sets script timer 0 to 3600 ticks; sets music theme 272; tests game flag 46 |
| `0x401` script timer 0 | `0x0750` | — | places a monster of type slot 2 on block 268 in mode 4; places a monster of type slot 1 on block 119 in mode 4; places a monster of type slot 1 on block 278 in mode 4; places a monster of type slot 1 on block 472 in mode 4; clears game flag 130; tests game flag 130 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 44 | Dagger | 8 | 365 |
| INI entry 1 (runs when the level loads) | 29 | Axe | 8 | 376 |
| INI entry 1 (runs when the level loads) | 116 | Star "Shining" | 8 | 154 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 8 | 271 |
| INI entry 1 (runs when the level loads) | 103 | Sabre "Cutter" | 8 | 349 |
| INI entry 1 (runs when the level loads) | 211 | Empty flask | 8 | 117 |
| INI entry 1 (runs when the level loads) | 211 | Empty flask | 8 | 469 |
| INI entry 1 (runs when the level loads) | 171 | Iron key | 8 | 304 |
| INI entry 1 (runs when the level loads) | 171 | Iron key | 8 | 120 |
| block 335 (x 15, y 10) | 234 | Freeze scroll | 8 | 368 |
| block 428 (x 12, y 13) | 49 | Dagger "Razor" | 8 | 397 |
| block 428 (x 12, y 13) | 217 | Aloe | 8 | 397 |
| block 562 (x 18, y 17) | 47 | Dagger "Back Biter" | 8 | 562 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 364 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 400 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 211 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 304 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 408 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 379 | 0 | 2 | 3 |
| `0x401` script timer 0 | 268 | 2 | 2 | 4 |
| `0x401` script timer 0 | 119 | 1 | 1 | 4 |
| `0x401` script timer 0 | 119 | 1 | 1 | 4 |
| `0x401` script timer 0 | 278 | 2 | 1 | 4 |
| `0x401` script timer 0 | 278 | 2 | 1 | 4 |
| `0x401` script timer 0 | 472 | 2 | 1 | 4 |
| `0x401` script timer 0 | 472 | 2 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 30, y 7 | 4 | x 30, y 7 | 0x41e0 | DRARACLE'S LAIR |

## Text shown by the scripts (ids only)

- Level text file `LEVEL08.<lang>`: 20 ids: 0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 17, 18, 19, 37, 38, 39, 43, 45, 47.
- Global text `LANDS.<lang>`: 2 ids: 0x403f, 0x4054.

Read any of them with `tools/decode_dialogue.py LEVEL08.ENG --index N`.
