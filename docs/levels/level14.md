# Level 14

Made by `tools/level_report.py` from `LEVEL14.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 6 = MINE1 (decorations `MINE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MINE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 607 | — | — |  | 0x80 | 63 |
| 1 | 1231 | 1 | — |  | 0x07 | 255 |
| 2 | 1227 | 2 | — |  | 0x07 | 255 |
| 3 | 2 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 6 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 27 | 4 | 1 | 7 | 2 lever (to on) | 0x07 | 207 |
| 30 | 8 | — | 29 |  | 0x80 | 63 |
| 31 | 3 | 2 | 14 | 2 lever (to on) | 0x07 | 207 |
| 35 | 40 | — | 25 |  | 0x80 | 10 |
| 37 | 16 | — | 23 |  | 0x80 | 63 |
| 38 | 4 | — | 4 |  | 0x84 | 11 |
| 40 | 1 | 2 | 60 | 1 clickable wall | 0x07 | 207 |
| 41 | 8 | 1 | 3 |  | 0x07 | 255 |
| 42 | 6 | 1 | 16 | 2 lever (to on) | 0x07 | 207 |
| 45 | 2 | 1 | 24 | 6 niche | 0x87 | 14 |
| 46 | 16 | 2 | — |  | 0x00 | 214 |
| 47 | 1 | 6 | 59 | 1 clickable wall | 0x07 | 207 |
| 51 | 1 | 2 | 71 | 1 clickable wall | 0x07 | 207 |
| 53 | 267 | 1 | — |  | 0x07 | 255 |
| 54 | 317 | 2 | — |  | 0x07 | 255 |
| 55 | 308 | 6 | — |  | 0x07 | 255 |
| 56 | 3 | 1 | 9 | 1 clickable wall | 0x07 | 210 |
| 63 | 3 | 2 | 65 | 1 clickable wall | 0x07 | 255 |
| 65 | 1 | 5 | 64 | 1 clickable wall | 0x07 | 26 |
| 66 | 2 | 2 | 37 | 1 clickable wall | 0x07 | 255 |
| 67 | 8 | — | 27 |  | 0x80 | 11 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 6 (x 6, y 0) | south | 27 | lever (to on) |
| 10 (x 10, y 0) | south | 51 | clickable wall |
| 16 (x 16, y 0) | south | 66 | clickable wall |
| 37 (x 5, y 1) | west | 3 | door / door switch |
| 49 (x 17, y 1) | west | 27 | lever (to on) |
| 131 (x 3, y 4) | south | 31 | lever (to on) |
| 144 (x 16, y 4) | north | 56 | clickable wall |
| 149 (x 21, y 4) | south | 27 | lever (to on) |
| 162 (x 2, y 5) | east | 31 | lever (to on) |
| 164 (x 4, y 5) | west | 31 | lever (to on) |
| 227 (x 3, y 7) | north | 66 | clickable wall |
| 235 (x 11, y 7) | south | 42 | lever (to on) |
| 236 (x 12, y 7) | south | 63 | clickable wall |
| 237 (x 13, y 7) | south | 42 | lever (to on) |
| 246 (x 22, y 7) | west | 3 | door / door switch |
| 263 (x 7, y 8) | north | 56 | clickable wall |
| 272 (x 16, y 8) | north | 56 | clickable wall |
| 292 (x 4, y 9) | north | 40 | clickable wall |
| 303 (x 15, y 9) | west | 42 | lever (to on) |
| 329 (x 9, y 10) | east | 47 | clickable wall |
| 335 (x 15, y 10) | west | 63 | clickable wall |
| 359 (x 7, y 11) | east | 65 | clickable wall |
| 367 (x 15, y 11) | west | 42 | lever (to on) |
| 379 (x 27, y 11) | south | 27 | lever (to on) |
| 427 (x 11, y 13) | north | 42 | lever (to on) |
| 428 (x 12, y 13) | north | 63 | clickable wall |
| 429 (x 13, y 13) | north | 42 | lever (to on) |
| 445 (x 29, y 13) | south | 45 | niche |
| 468 (x 20, y 14) | north | 45 | niche |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL14.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles MINE1; loads monster sprites MULTIPD.SHP into slot 0; loads monster sprites MAGICMIR.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 443; places item 84 (Long sword "Flayer") on block 485; places item 250 (Humanoid bone) on block 497; places item 242 (Note) on block 497; places item 176 (Mine key 4) on block 486; places item 177 (Mine key 5) on block 468; places item 232 (Wand of Fireballs) on block 445; sets the west wall of block 992 to type -1 … |

### LEVEL14.INF

| Entry | Events | What it does |
|---|---|---|
| block 6 (x 6, y 0) | wall clicked | operates the door at block 37; sets game flag 295; checks a wall of block 6; checks a wall of block 42 |
| block 10 (x 10, y 0) | wall clicked | sets the north wall of block 995 to type ?; sets the south wall of block 10 to type ?; checks a wall of block 10; plays a sound; tests game flag 295 |
| block 41 (x 9, y 1) | party arrives (second path) | clears game flag 294; tests game flag 294 |
| block 42 (x 10, y 1) | party steps in, party arrives (second path), party leaves (second path), item put down, item taken, bits 0x4000 (no engine caller found) | clears game flag 294; tests game flag 294; tests game flag 295 |
| block 43 (x 11, y 1) | party arrives (second path) | clears game flag 294; tests game flag 294 |
| block 47 (x 15, y 1) | party leaves (second path) | operates the door at block 47; checks a wall of block 49; checks a wall of block 995 |
| block 48 (x 16, y 1) | party arrives (second path) | sets game flag 296; make item; play environmental sfx; launches a projectile; starts script timer 2; sets game flag 297; tests game flag 297; checks a wall of block 47 |
| block 49 (x 17, y 1) | wall clicked, thrown item hits | operates the door at block 47; sets the west wall of block 49 to type 28; sets the west wall of block 49 to type 27; make item; play environmental sfx; launches a projectile; starts script timer 2; sets game flag 297 … |
| block 112 (x 16, y 3) | bits 0x400 (no engine caller found) | gives item 247 (Broken glass); gives item 262 (Bezel Cup); sets the west wall of block 994 to type 0; checks a wall of block 994 |
| block 131 (x 3, y 4) | wall clicked | sets the east wall of block 162 to type 31; sets the south wall of block 131 to type 31; sets the west wall of block 164 to type 31; sets the west wall of block 131 to type 0; make item; play environmental sfx; launches a projectile; plays a sound … |
| block 144 (x 16, y 4) | wall clicked | gives item 247 (Broken glass); gives item 262 (Bezel Cup); sets the west wall of block 994 to type 0; checks a wall of block 994 |
| block 149 (x 21, y 4) | wall clicked | sets the west wall of block 181 to type 38; drops the party through a pit; deals damage; moves the party to level 15, block 53; sets game flag 46; moves objects from block 181 to block 53; checks a wall of block 181 |
| block 162 (x 2, y 5) | wall clicked | sets the east wall of block 162 to type 31; sets the south wall of block 131 to type 31; sets the west wall of block 164 to type 31; make item; play environmental sfx; launches a projectile; plays a sound; checks a wall of block 131 … |
| block 164 (x 4, y 5) | wall clicked | sets the east wall of block 162 to type 31; sets the south wall of block 131 to type 31; sets the west wall of block 164 to type 31; make item; play environmental sfx; launches a projectile; plays a sound; checks a wall of block 131 … |
| block 181 (x 21, y 5) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 15, block 53; sets game flag 46; moves objects from block 181 to block 53; checks a wall of block 181 |
| block 182 (x 22, y 5) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 15, block 54; sets game flag 46; moves objects from block 182 to block 54; checks a wall of block 182 |
| block 231 (x 7, y 7) | bits 0x400 (no engine caller found) | gives item 247 (Broken glass); gives item 248 (Oil Flask); sets the west wall of block 992 to type 0; checks a wall of block 992 |
| block 235 (x 11, y 7) | wall clicked | sets the west wall of block 235 to type 0; plays a sound |
| block 236 (x 12, y 7) | wall clicked | a character speaks; shows a message |
| block 237 (x 13, y 7) | wall clicked | sets the west wall of block 237 to type 0; plays a sound |
| block 240 (x 16, y 7) | bits 0x400 (no engine caller found) | deals damage; checks a wall of block 993 |
| block 248 (x 24, y 7) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 248 to type 36; operates the door at block 246; sets game flag 286; checks a wall of block 248; plays a sound; tests game flag 286 |
| block 263 (x 7, y 8) | wall clicked | gives item 247 (Broken glass); gives item 248 (Oil Flask); sets the west wall of block 992 to type 0; checks a wall of block 992 |
| block 272 (x 16, y 8) | wall clicked | deals damage; checks a wall of block 993 |
| block 292 (x 4, y 9) | wall clicked | a character speaks |
| block 303 (x 15, y 9) | wall clicked | sets the west wall of block 303 to type 0; plays a sound |
| block 329 (x 9, y 10) | wall clicked | sets the west wall of block 361 to type 0; a character speaks; plays a sound |
| block 335 (x 15, y 10) | wall clicked | a character speaks; shows a message |
| block 355 (x 3, y 11) | party steps in, party arrives (second path), item put down | moves objects from block 355 to block 259 |
| block 359 (x 7, y 11) | party steps in, party arrives (second path), wall clicked, item put down | moves objects from block 359 to block 262; a character speaks; checks a wall of block 359; set global var |
| block 367 (x 15, y 11) | wall clicked | sets the west wall of block 367 to type 0; plays a sound |
| block 374 (x 22, y 11) | fireball ends here | sets the west wall of block 374 to type 0; deals damage; gas explosion; checks a wall of block 374 |
| block 376 (x 24, y 11) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 408 to type 29; sets the west wall of block 472 to type 29; sets the west wall of block 507 to type 29; sets the west wall of block 509 to type 29; clears game flag 293; sets game flag 291; clears game flag 291; clears game flag 290 … |
| block 379 (x 27, y 11) | wall clicked | sets the west wall of block 413 to type 44; operates the door at block 413; sets the west wall of block 413 to type 0; moves objects from block 413 to block 246; checks a wall of block 411; checks a wall of block 379; checks a wall of block 413; plays a sound |
| block 406 (x 22, y 12) | party arrives (second path) | a character speaks; checks a wall of block 374 |
| block 408 (x 24, y 12) | party arrives (second path), party leaves (second path) | clears game flag 290; checks a wall of block ?; plays a sound |
| block 411 (x 27, y 12) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 411 to type 36; sets the west wall of block 413 to type 44; operates the door at block 413; sets the west wall of block 413 to type 0; moves objects from block 413 to block 246; checks a wall of block 411; plays a sound; checks a wall of block 379 … |
| block 413 (x 29, y 12) | party steps in, party arrives (second path), item put down | moves objects from block 413 to block 246; checks a wall of block 413; plays a sound |
| block 419 (x 3, y 13) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 419 to type 36; sets the west wall of block 451 to type 0; sets the west wall of block 451 to type 38; drops the party through a pit; deals damage; moves the party to level 15, block 355; sets the west wall of block 420 to type 0; sets the west wall of block 420 to type 38 … |
| block 420 (x 4, y 13) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 15, block 324; sets game flag 46; moves objects from block 420 to block 324; checks a wall of block 420 |
| block 427 (x 11, y 13) | wall clicked | sets the west wall of block 427 to type 0; plays a sound |
| block 428 (x 12, y 13) | wall clicked | a character speaks; shows a message |
| block 429 (x 13, y 13) | wall clicked | sets the west wall of block 429 to type 0; plays a sound |
| block 438 (x 22, y 13) | party arrives (second path) | sets game flag 285; a character speaks; tests game flag 285 |
| block 440 (x 24, y 13) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 408 to type 29; sets the west wall of block 472 to type 29; sets the west wall of block 507 to type 29; sets the west wall of block 509 to type 29; clears game flag 293; sets game flag 291; clears game flag 291; clears game flag 290 … |
| block 445 (x 29, y 13) | item taken | operates the door at block 246 |
| block 451 (x 3, y 14) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 15, block 355; sets game flag 46; moves objects from block 451 to block 355; checks a wall of block 451 |
| block 472 (x 24, y 14) | party arrives (second path), party leaves (second path) | clears game flag 290; checks a wall of block ?; plays a sound |
| block 489 (x 9, y 15) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 489 to type 36; toggles the east wall of block 486 between types 45 and 54; checks a wall of block 489; plays a sound |
| block 504 (x 24, y 15) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 408 to type 29; sets the west wall of block 472 to type 29; sets the west wall of block 507 to type 29; sets the west wall of block 509 to type 29; clears game flag 293; sets game flag 291; clears game flag 291; clears game flag 290 … |
| block 506 (x 26, y 15) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 408 to type 29; sets the west wall of block 472 to type 29; sets the west wall of block 507 to type 29; sets the west wall of block 509 to type 29; clears game flag 293; sets game flag 291; clears game flag 291; clears game flag 290 … |
| block 507 (x 27, y 15) | party arrives (second path), party leaves (second path) | clears game flag 290; checks a wall of block ?; plays a sound |
| block 508 (x 28, y 15) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 408 to type 29; sets the west wall of block 472 to type 29; sets the west wall of block 507 to type 29; sets the west wall of block 509 to type 29; clears game flag 293; sets game flag 291; clears game flag 291; clears game flag 290 … |
| block 509 (x 29, y 15) | party arrives (second path), party leaves (second path) | clears game flag 290; checks a wall of block ?; plays a sound |
| `0x400` level loaded | — | drops the party through a pit; sets the east wall of block 359 to type 24; sets the east wall of block 359 to type 65; clears game flag 46; starts script timer 0; starts script timer 1; starts script timer 2; tests game flag 46 … |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 253; places a monster (slot 1) on block 172; places a monster (slot 1) on block 357; places a monster (slot 2) on block 370; places a monster (slot 2) on block 195; clears game flag 130; sets game flag 130; tests game flag 130 |
| `0x402` script timer 1 | — | sets the west wall of block 408 to type 30; sets the west wall of block 472 to type 30; sets the west wall of block 408 to type 67; sets the west wall of block 472 to type 67; sets the west wall of block 507 to type 30; sets the west wall of block 509 to type 30; sets the west wall of block 507 to type 67; sets the west wall of block 509 to type 67 … |
| `0x403` script timer 2 | — | deals damage; starts script timer 2; sets game flag 290; make item; play environmental sfx; launches a projectile; sets game flag 297; tests game flag 290 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 84 | Long sword "Flayer" | 14 | 485 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 14 | 497 |
| INI entry 1 (runs when the level loads) | 242 | Note | 14 | 497 |
| INI entry 1 (runs when the level loads) | 176 | Mine key 4 | 14 | 486 |
| INI entry 1 (runs when the level loads) | 177 | Mine key 5 | 14 | 468 |
| INI entry 1 (runs when the level loads) | 232 | Wand of Fireballs | 14 | 445 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 443 | 2 | 1 | 3 |
| `0x401` script timer 0 | 253 | 2 | 2 | 4 |
| `0x401` script timer 0 | 172 | 1 | 1 | 4 |
| `0x401` script timer 0 | 357 | 2 | 1 | 4 |
| `0x401` script timer 0 | 370 | 1 | 2 | 4 |
| `0x401` script timer 0 | 370 | 1 | 2 | 4 |
| `0x401` script timer 0 | 195 | 0 | 2 | 4 |
| `0x401` script timer 0 | 195 | 0 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 22, y 12 | 9 | x 22, y 12 | 0x41ec | GAS SMELL |

## Text shown by the scripts (ids only)

- Level text file `LEVEL14.<lang>`: 7 ids: 0, 2, 3, 4, 14, 19, 20.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL14.ENG --index N`.
