# Level 7

Made by `tools/level_report.py` from `LEVEL7.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 618 | — | — |  | 0x80 | 63 |
| 1 | 1693 | 1 | — |  | 0x07 | 255 |
| 2 | 1686 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 12 | 5 | — |  | 0x04 | 26 |
| 26 | 4 | — | — |  | 0x84 | 63 |
| 27 | 3 | 1 | 49 | 2 lever (to on) | 0x07 | 207 |
| 29 | 1 | 2 | 70 | 2 lever (to on) | 0x07 | 207 |
| 31 | 3 | 1 | 61 | 2 lever (to on) | 0x07 | 207 |
| 33 | 1 | 1 | 53 | 1 clickable wall | 0x07 | 207 |
| 37 | 20 | — | 22 |  | 0x80 | 63 |
| 38 | 8 | — | 19 |  | 0x84 | 11 |
| 41 | 2 | 1 | 45 |  | 0x07 | 255 |
| 42 | 1 | 1 | 68 | 2 lever (to on) | 0x07 | 207 |
| 45 | 5 | 1 | 50 | 6 niche | 0x87 | 14 |
| 46 | 4 | 2 | — |  | 0x00 | 214 |
| 48 | 1 | 2 | 46 | 1 clickable wall | 0x07 | 207 |
| 49 | 1 | 2 | 72 | 1 clickable wall | 0x07 | 207 |
| 53 | 4 | 1 | 26 | 1 clickable wall | 0x07 | 210 |
| 54 | 2 | 1 | 66 | 2 lever (to on) | 0x07 | 207 |
| 60 | 4 | 5 | — |  | 0x06 | 63 |
| 61 | 2 | 2 | 63 | 1 clickable wall | 0x07 | 255 |
| 65 | 2 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 66 | 2 | 1 | 38 | 1 clickable wall | 0x07 | 255 |
| 69 | 4 | 1 | 36 |  | 0x06 | 25 |
| 77 | 2 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 1 | 2 | 60 | 1 clickable wall | 0x07 | 255 |
| 79 | 4 | 2 | 64 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 23 (x 23, y 0) | south | 77 | clickable wall |
| 27 (x 27, y 0) | south | 77 | clickable wall |
| 89 (x 25, y 2) | north | 78 | clickable wall |
| 130 (x 2, y 4) | south | 49 | clickable wall |
| 161 (x 1, y 5) | south | 79 | clickable wall |
| 171 (x 11, y 5) | south | 79 | clickable wall |
| 227 (x 3, y 7) | west | 54 | lever (to on) |
| 237 (x 13, y 7) | south | 54 | lever (to on) |
| 242 (x 18, y 7) | south | 65 | clickable wall |
| 261 (x 5, y 8) | west | 27 | lever (to on) |
| 262 (x 6, y 8) | south | 66 | clickable wall |
| 265 (x 9, y 8) | north | 53 | clickable wall |
| 265 (x 9, y 8) | east | 53 | clickable wall |
| 268 (x 12, y 8) | east | 45 | niche |
| 270 (x 14, y 8) | east | 61 | clickable wall |
| 275 (x 19, y 8) | west | 53 | clickable wall |
| 289 (x 1, y 9) | south | 79 | clickable wall |
| 295 (x 7, y 9) | west | 66 | clickable wall |
| 335 (x 15, y 10) | south | 45 | niche |
| 361 (x 9, y 11) | south | 61 | clickable wall |
| 361 (x 9, y 11) | west | 53 | clickable wall |
| 366 (x 14, y 11) | east | 27 | lever (to on) |
| 371 (x 19, y 11) | west | 31 | lever (to on) |
| 392 (x 8, y 12) | south | 29 | lever (to on) |
| 400 (x 16, y 12) | south | 45 | niche |
| 433 (x 17, y 13) | west | 27 | lever (to on) |
| 482 (x 2, y 15) | east | 79 | clickable wall |
| 489 (x 9, y 15) | east | 65 | clickable wall |
| 513 (x 1, y 16) | south | 33 | clickable wall |
| 522 (x 10, y 16) | north | 42 | lever (to on) |
| 524 (x 12, y 16) | north | 31 | lever (to on) |
| 998 (x 6, y 31) | north | 45 | niche |
| 998 (x 6, y 31) | east | 48 | clickable wall |
| 998 (x 6, y 31) | south | 31 | lever (to on) |
| 998 (x 6, y 31) | west | 45 | niche |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL7.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; places a monster (slot 1) on block 194; loads monster sprites SCAVNGR.SHP into slot 0; loads monster sprites RATMAN.SHP into slot 0; loads monster sprites CAVEDWLR.SHP into slot 1; defines monster type 1; defines monster type 2; defines monster type 3 … |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 488; places a monster (slot 2) on block 484; places a monster (slot 2) on block 616; places a monster (slot 2) on block 580; places item 99 (Rock) on block 229; places item 99 (Rock) on block 429; places item 99 (Rock) on block 369; places item 153 (Leather jerkin) on block 103 … |

### LEVEL7.INF

| Entry | Events | What it does |
|---|---|---|
| block 58 (x 26, y 1) | party arrives (second path) | sets the north wall of block 999 to type 1; a character speaks; starts a dialogue; checks a wall of block 999 |
| block 66 (x 2, y 2) | wall clicked | a character joins the party; starts cut-scene POD1.TIM; starts cut-scene POD2.TIM; a character speaks; sets game flag 56; sets game flag 57; sets game flag 139; sets game flag 58 … |
| block 98 (x 2, y 3) | party steps in, party arrives (second path) | shows a message; sets game flag 59; a character speaks; set global var; tests game flag 58; tests game flag 56; tests game flag 57; tests game flag 59 |
| block 109 (x 13, y 3) | party arrives (second path) | sets the west wall of block 295 to type 1 |
| block 118 (x 22, y 3) | party steps in, party arrives (second path), item put down | moves objects from block 118 to block 150 |
| block 124 (x 28, y 3) | party steps in, party arrives (second path), item put down | moves objects from block 124 to block 156 |
| block 130 (x 2, y 4) | wall clicked | sets the west wall of block 98 to type 1; sets the west wall of block 130 to type 0; tests game flag 588; plays a sound |
| block 161 (x 1, y 5) | wall clicked | a character speaks |
| block 162 (x 2, y 5) | party arrives (second path) | sets the west wall of block 98 to type 1; sets game flag 548; a character speaks; tests game flag 548; tests game flag 588 |
| block 169 (x 9, y 5) | party arrives (second path) | places a monster (slot 3) on block 139; places a monster (slot 3) on block 107; character surprise feedback; move party |
| block 171 (x 11, y 5) | wall clicked | a character speaks |
| block 207 (x 15, y 6) | party steps in, party arrives (second path), item put down | moves objects from block 207 to block 208 |
| block 227 (x 3, y 7) | wall clicked | toggles the west wall of block 258 between types 0 and 1; plays a sound |
| block 233 (x 9, y 7) | bits 0x400 (no engine caller found) | gives item 243 (Coin Purse) |
| block 237 (x 13, y 7) | wall clicked | sets the east wall of block 268 to type 45; sets the east wall of block 268 to type 31; sets the east wall of block 268 to type 47; sets the west wall of block 268 to type 0; remove level item; place move level item; checks a wall of block 268; tests game flag ? … |
| block 242 (x 18, y 7) | wall clicked | a character speaks |
| block 261 (x 5, y 8) | wall clicked | operates the door at block 293 |
| block 262 (x 6, y 8) | wall clicked | a character speaks; sets game flag 141; checks a wall of block 262; tests game flag 141 |
| block 265 (x 9, y 8) | wall clicked | gives item 243 (Coin Purse); deals damage; checks a wall of block 994 |
| block 266 (x 10, y 8) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 994 |
| block 268 (x 12, y 8) | wall clicked, item put down | sets the east wall of block 268 to type 1; remove level item; place move level item; sets game flag ?; a character speaks; moves objects from block 268 to block 219; checks a wall of block 268; plays a sound |
| block 270 (x 14, y 8) | wall clicked | a character speaks |
| block 274 (x 18, y 8) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 995 |
| block 275 (x 19, y 8) | wall clicked | deals damage; checks a wall of block 995 |
| block 289 (x 1, y 9) | wall clicked | a character speaks |
| block 290 (x 2, y 9) | party steps in, party arrives (second path), item put down | a character speaks; sets game flag 125; moves objects from block 290 to block 322; tests game flag 125 |
| block 295 (x 7, y 9) | wall clicked | a character speaks; sets game flag 140; checks a wall of block 295; tests game flag 140 |
| block 296 (x 8, y 9) | party arrives (second path) | sets the west wall of block 108 to type 1 |
| block 360 (x 8, y 11) | bits 0x400 (no engine caller found) | gives item 247 (Broken glass); gives item 248 (Oil Flask); sets the west wall of block 992 to type 0; checks a wall of block 992 |
| block 361 (x 9, y 11) | wall clicked | gives item 247 (Broken glass); gives item 248 (Oil Flask); sets the west wall of block 992 to type 0; a character speaks; checks a wall of block 992 |
| block 366 (x 14, y 11) | wall clicked, thrown item hits | sets the west wall of block 367 to type 38; drops the party through a pit; deals damage; moves the party to level 8, block 367; sets the west wall of block 367 to type 0; moves objects from block 367 to block 367; sets game flag 46; checks a wall of block 367 … |
| block 367 (x 15, y 11) | party arrives (second path), item put down | moves objects from block 367 to block 367; checks a wall of block 367 |
| block 371 (x 19, y 11) | wall clicked | make item; launches a projectile; checks a wall of block 371; plays a sound |
| block 392 (x 8, y 12) | wall clicked | sets the east wall of block 423 to type 45; places item 218 (Ginseng) on block 423; checks a wall of block 423; plays a sound |
| block 420 (x 4, y 13) | party arrives (second path) | places a monster (slot 2) on block 321; a character speaks; character surprise feedback; move party |
| block 425 (x 9, y 13) | party arrives (second path) | character surprise feedback; move party |
| block 426 (x 10, y 13) | party arrives (second path) | sets the west wall of block 427 to type 46; checks a wall of block 427; plays a sound |
| block 430 (x 14, y 13) | party arrives (second path), item put down | moves objects from block 430 to block 430; checks a wall of block 430 |
| block 431 (x 15, y 13) | party arrives (second path), item put down | moves objects from block 431 to block 431; checks a wall of block 431 |
| block 432 (x 16, y 13) | party arrives (second path), item put down | moves objects from block 432 to block 432; checks a wall of block 432 |
| block 433 (x 17, y 13) | wall clicked, thrown item hits | toggles the west wall of block 433 between types 27 and 28; sets the west wall of block 430 to type 0; sets the west wall of block 431 to type 38; drops the party through a pit; deals damage; moves the party to level 8, block 431; sets the west wall of block 431 to type 0; sets the west wall of block 432 to type 38 … |
| block 455 (x 7, y 14) | party arrives (second path) | sets game flag 138; tests game flag 138 |
| block 482 (x 2, y 15) | wall clicked | a character speaks |
| block 489 (x 9, y 15) | wall clicked | a character speaks |
| block 495 (x 15, y 15) | party steps in, party arrives (second path), item put down | moves objects from block 495 to block 527 |
| block 513 (x 1, y 16) | wall clicked | sets the west wall of block 513 to type 0; checks a wall of block 513; plays a sound |
| block 522 (x 10, y 16) | wall clicked | sets the west wall of block 522 to type 0; checks a wall of block 522; plays a sound |
| block 524 (x 12, y 16) | wall clicked | make item; play environmental sfx; launches a projectile; checks a wall of block 524 |
| block 554 (x 10, y 17) | party arrives (second path) | sets the west wall of block 522 to type 1; places a monster (slot 2) on block 616; places a monster (slot 2) on block 580; checks a wall of block 522; plays a sound |
| `0x400` level loaded | — | drops the party through a pit; clears game flag 46; starts script timer 0; tests game flag 46 |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 203; places a monster (slot 2) on block 271; places a monster (slot 3) on block 302; clears game flag 130; sets game flag 130; tests game flag 130 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 229 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 429 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 369 |
| INI entry 1 (runs when the level loads) | 153 | Leather jerkin | 7 | 103 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 7 | 463 |
| INI entry 1 (runs when the level loads) | 59 | Sledge | 7 | 196 |
| INI entry 1 (runs when the level loads) | 46 | Dagger "Stiletto" | 7 | 463 |
| INI entry 1 (runs when the level loads) | 116 | Star "Shining" | 7 | 555 |
| INI entry 1 (runs when the level loads) | 169 | Worn key | 7 | 335 |
| INI entry 1 (runs when the level loads) | 275 | Note | 7 | 268 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 251 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 252 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 7 | 423 |
| block 392 (x 8, y 12) | 218 | Ginseng | 7 | 423 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 0 (runs when the level loads) | 194 | 0 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 488 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 484 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 484 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 616 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 616 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 580 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 580 | 3 | 2 | 3 |
| block 169 (x 9, y 5) | 139 | 0 | 3 | 4 |
| block 169 (x 9, y 5) | 107 | 1 | 3 | 4 |
| block 420 (x 4, y 13) | 321 | 2 | 2 | 4 |
| block 420 (x 4, y 13) | 321 | 2 | 2 | 4 |
| block 554 (x 10, y 17) | 616 | 0 | 2 | 7 |
| block 554 (x 10, y 17) | 580 | 0 | 2 | 7 |
| `0x401` script timer 0 | 203 | 2 | 2 | 4 |
| `0x401` script timer 0 | 203 | 2 | 2 | 4 |
| `0x401` script timer 0 | 271 | 1 | 2 | 4 |
| `0x401` script timer 0 | 271 | 1 | 2 | 4 |
| `0x401` script timer 0 | 302 | 1 | 3 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 2, y 2 | 6 | x 2, y 3 | 0x41df | POD ROOM |

## Text shown by the scripts (ids only)

- Level text file `LEVEL07.<lang>`: 22 ids: 1, 2, 4, 7, 8, 9, 10, 19, 20, 21, 22, 26, 28, 30, 31, 32, 33, 34, 36, 37, 40, 41.
- Global text `LANDS.<lang>`: 2 ids: 0x403f, 0x4084.

Read any of them with `tools/decode_dialogue.py LEVEL07.ENG --index N`.
