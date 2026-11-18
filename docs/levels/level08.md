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

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL8.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; loads monster sprites SCAVNGR.SHP into slot 0; loads monster sprites FLSPIDER.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 364; places a monster (slot 2) on block 400; places a monster (slot 2) on block 211; places a monster (slot 2) on block 304; places a monster (slot 2) on block 408; places a monster (slot 2) on block 379; places item 44 (Dagger) on block 365; places item 29 (Axe) on block 376 … |

### LEVEL8.INF

| Entry | Events | What it does |
|---|---|---|
| block 81 (x 17, y 2) | wall clicked | sets the west wall of block 114 to type 0; a character speaks; shows a message; delete hand item; plays a sound |
| block 115 (x 19, y 3) | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 114 to type 1; a character speaks; sets game flag 153; sets game flag 154; tests game flag 153 |
| block 116 (x 20, y 3) | party arrives (second path) | sets game flag 154; a character speaks; tests game flag 153; tests game flag 154 |
| block 124 (x 28, y 3) | party steps in, party arrives (second path), item put down | moves objects from block 124 to block 92 |
| block 179 (x 19, y 5) | wall clicked | a character speaks |
| block 207 (x 15, y 6) | party steps in, party arrives (second path), item put down | moves objects from block 207 to block 206 |
| block 209 (x 17, y 6) | party arrives (second path) | sets the south wall of block 32 to type 1 |
| block 218 (x 26, y 6) | party steps in, party arrives (second path), item put down | moves objects from block 218 to block 217 |
| block 223 (x 31, y 6) | wall clicked | delete hand item; a character speaks; sets game flag 60; set global var; plays a sound |
| block 236 (x 12, y 7) | wall clicked | a character speaks |
| block 245 (x 21, y 7) | bits 0x400 (no engine caller found) | a character speaks; checks a wall of block 277 |
| block 246 (x 22, y 7) | wall clicked | a character speaks |
| block 254 (x 30, y 7) | party steps in, party arrives (second path), wall clicked, item put down | starts cut-scene DRARCLE4.TIM; moves objects from block 254 to block 253; shows a message; sets game flag 588; clears game flag 62; clears game flag 63; set global var; tests game flag 60 … |
| block 255 (x 31, y 7) | party arrives (second path), wall clicked | starts cut-scene DRARCLE3.TIM; sets game flag 309; sets game flag 62; a character speaks; sets game flag 63; tests game flag 67; set global var; tests game flag 60 … |
| block 272 (x 16, y 8) | wall clicked | a character speaks |
| block 277 (x 21, y 8) | wall clicked | a character speaks; checks a wall of block 277 |
| block 281 (x 25, y 8) | wall clicked | sets the west wall of block 280 to type 0 |
| block 311 (x 23, y 9) | party arrives (second path) | sets game flag 157 |
| block 312 (x 24, y 9) | party arrives (second path) | a character speaks; sets game flag 157; tests game flag 157 |
| block 335 (x 15, y 10) | wall clicked | sets the west wall of block 368 to type 45; places item 234 (Freeze scroll) on block 368; checks a wall of block 368; plays a sound |
| block 342 (x 22, y 10) | wall clicked | toggles the west wall of block 311 between types 0 and 1 |
| block 366 (x 14, y 11) | party arrives (second path) | character surprise feedback; move party |
| block 367 (x 15, y 11) | party arrives (second path) | a character speaks; sets game flag 152; checks a wall of block 335; tests game flag 152 |
| block 411 (x 27, y 12) | wall clicked | a character speaks |
| block 428 (x 12, y 13) | wall clicked | sets the south wall of block 397 to type 45; places item 49 (Dagger "Razor") on block 397; places item 217 (Aloe) on block 397; sets game flag 49; tests game flag 49; plays a sound |
| block 437 (x 21, y 13) | party arrives (second path), bits 0x10 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 438 (x 22, y 13) | party arrives (second path) | sets game flag 155; sets game flag 156; a character speaks; tests game flag 156 |
| block 439 (x 23, y 13) | bits 0x400 (no engine caller found) | a character speaks; checks a wall of block 440 |
| block 440 (x 24, y 13) | wall clicked | a character speaks; checks a wall of block 440 |
| block 442 (x 26, y 13) | party arrives (second path) | character surprise feedback; move party |
| block 495 (x 15, y 15) | party steps in, party arrives (second path), item put down | moves objects from block 495 to block 463 |
| block 501 (x 21, y 15) | wall clicked | a character speaks; checks a wall of block 501 |
| block 502 (x 22, y 15) | bits 0x400 (no engine caller found) | a character speaks; checks a wall of block 501 |
| block 509 (x 29, y 15) | party steps in, party arrives (second path), item put down | moves objects from block 509 to block 477 |
| block 538 (x 26, y 16) | wall clicked | sets the west wall of block 537 to type 0; a character speaks; sets game flag 66; delete hand item; shows a message; tests game flag 66; plays a sound; checks a wall of block 537 |
| block 562 (x 18, y 17) | item put down | places item 47 (Dagger "Back Biter") on block 562; sets game flag 65; delete level item; tests game flag 65 |
| block 563 (x 19, y 17) | party arrives (second path), party leaves (second path), bits 0x10 (no engine caller found) | sets game flag 158; a character speaks; tests game flag 158 |
| block 566 (x 22, y 17) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 566 to type 36; toggles the east wall of block 562 between types 45 and 1; checks a wall of block 566; plays a sound |
| block 592 (x 16, y 18) | party arrives (second path) | sets the south wall of block 32 to type 2 |
| `0x400` level loaded | — | drops the party through a pit; clears game flag 46; starts script timer 0; tests game flag 46 |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 268; places a monster (slot 1) on block 119; places a monster (slot 1) on block 278; places a monster (slot 1) on block 472; clears game flag 130; tests game flag 130 |

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
