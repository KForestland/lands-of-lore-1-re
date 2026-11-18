# Level 9

Made by `tools/level_report.py` from `LEVEL9.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 344 | — | — |  | 0x80 | 63 |
| 1 | 1854 | 1 | — |  | 0x07 | 255 |
| 2 | 1850 | 2 | — |  | 0x07 | 255 |
| 23 | 8 | 4 | — |  | 0x04 | 25 |
| 27 | 1 | 1 | 49 | 2 lever (to on) | 0x07 | 207 |
| 29 | 1 | 2 | 51 | 1 clickable wall | 0x07 | 207 |
| 35 | 12 | — | 20 |  | 0x80 | 10 |
| 42 | 1 | 1 | 68 | 1 clickable wall | 0x07 | 207 |
| 53 | 2 | 1 | 26 | 1 clickable wall | 0x07 | 210 |
| 61 | 4 | 2 | 63 | 1 clickable wall | 0x07 | 255 |
| 62 | 4 | 1 | 39 | 1 clickable wall | 0x07 | 255 |
| 65 | 8 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 77 | 3 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 4 | 2 | 60 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 83 (x 19, y 2) | south | 65 | clickable wall |
| 86 (x 22, y 2) | south | 78 | clickable wall |
| 91 (x 27, y 2) | south | 77 | clickable wall |
| 158 (x 30, y 4) | west | 65 | clickable wall |
| 178 (x 18, y 5) | east | 78 | clickable wall |
| 181 (x 21, y 5) | east | 77 | clickable wall |
| 185 (x 25, y 5) | west | 78 | clickable wall |
| 219 (x 27, y 6) | east | 29 | clickable wall |
| 242 (x 18, y 7) | east | 65 | clickable wall |
| 248 (x 24, y 7) | north | 78 | clickable wall |
| 248 (x 24, y 7) | south | 61 | clickable wall |
| 252 (x 28, y 7) | south | 65 | clickable wall |
| 278 (x 22, y 8) | north | 62 | clickable wall |
| 278 (x 22, y 8) | south | 62 | clickable wall |
| 285 (x 29, y 8) | north | 65 | clickable wall |
| 308 (x 20, y 9) | south | 65 | clickable wall |
| 373 (x 21, y 11) | east | 53 | clickable wall |
| 373 (x 21, y 11) | south | 27 | lever (to on) |
| 382 (x 30, y 11) | west | 61 | clickable wall |
| 403 (x 19, y 12) | east | 77 | clickable wall |
| 434 (x 18, y 13) | east | 61 | clickable wall |
| 440 (x 24, y 13) | east | 61 | clickable wall |
| 468 (x 20, y 14) | north | 62 | clickable wall |
| 468 (x 20, y 14) | south | 62 | clickable wall |
| 498 (x 18, y 15) | east | 65 | clickable wall |
| 503 (x 23, y 15) | east | 42 | clickable wall |
| 531 (x 19, y 16) | north | 53 | clickable wall |
| 538 (x 26, y 16) | north | 65 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL9.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; loads monster sprites MORIBUND.SHP into slot 0; loads monster sprites FLSPIDER.SHP into slot 1; defines monster type 2; defines monster type 1 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 379; places a monster (slot 1) on block 435; places a monster (slot 1) on block 441; places item 99 (Rock) on block 309; places item 99 (Rock) on block 436; places item 243 (Coin Purse) on block 219; sets the west wall of block 992 to type -1; sets the east wall of block 992 to type 0 … |

### LEVEL9.INF

| Entry | Events | What it does |
|---|---|---|
| block 152 (x 24, y 4) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 152 to type 36; make item; play environmental sfx; launches a projectile; checks a wall of block 152; plays a sound |
| block 157 (x 29, y 4) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 157 to type 36; make item; play environmental sfx; launches a projectile; checks a wall of block 157; plays a sound |
| block 179 (x 19, y 5) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 179 to type 36; make item; play environmental sfx; launches a projectile; sets game flag 42; starts script timer 1; checks a wall of block 179; plays a sound |
| block 218 (x 26, y 6) | party steps in, party arrives (second path), item put down | moves objects from block 218 to block 219 |
| block 219 (x 27, y 6) | wall clicked | sets the east wall of block 219 to type 45; checks a wall of block 219 |
| block 246 (x 22, y 7) | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x400 (no engine caller found) | sets the north wall of block 278 to type 63; sets the west wall of block 246 to type 36; make item; play environmental sfx; launches a projectile; checks a wall of block 278; plays a sound; checks a wall of block 246 |
| block 247 (x 23, y 7) | fireball passes | no game action (only stack and screen bookkeeping) |
| block 248 (x 24, y 7) | wall clicked | a character speaks |
| block 310 (x 22, y 9) | bits 0x400 (no engine caller found) | sets the south wall of block 278 to type 63; checks a wall of block 278; plays a sound |
| block 373 (x 21, y 11) | wall clicked | a character speaks; clears game flag 43; checks a wall of block 993; checks a wall of block 440; plays a sound; checks a wall of block 373 |
| block 374 (x 22, y 11) | bits 0x400 (no engine caller found) | a character speaks; checks a wall of block 993; checks a wall of block 440 |
| block 378 (x 26, y 11) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 382 (x 30, y 11) | wall clicked | a character speaks |
| block 404 (x 20, y 12) | party arrives (second path), party leaves (second path), item put down, item taken | make item; play environmental sfx; launches a projectile; sets game flag 43; starts script timer 1; checks a wall of block 373 |
| block 412 (x 28, y 12) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 412 to type 36; make item; play environmental sfx; launches a projectile; checks a wall of block 412; plays a sound |
| block 434 (x 18, y 13) | wall clicked | a character speaks |
| block 436 (x 20, y 13) | party arrives (second path), bits 0x400 (no engine caller found) | sets the north wall of block 468 to type 63; a character speaks; checks a wall of block 468; plays a sound |
| block 440 (x 24, y 13) | wall clicked | a character speaks |
| block 499 (x 19, y 15) | bits 0x400 (no engine caller found) | a character speaks; checks a wall of block 992; checks a wall of block 531 |
| block 500 (x 20, y 15) | bits 0x400 (no engine caller found) | sets the south wall of block 468 to type 63; checks a wall of block 468; plays a sound |
| block 503 (x 23, y 15) | party arrives (second path), wall clicked | sets the west wall of block 503 to type 0; make item; play environmental sfx; launches a projectile |
| block 504 (x 24, y 15) | party arrives (second path) | sets game flag 159; a character speaks; checks a wall of block 503; tests game flag 159 |
| block 509 (x 29, y 15) | party steps in, party arrives (second path), item put down | moves objects from block 509 to block 541 |
| block 531 (x 19, y 16) | wall clicked | a character speaks; checks a wall of block 992; checks a wall of block 531 |
| `0x400` level loaded | — | starts script timer 0; starts script timer 1 |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 280 |
| `0x402` script timer 1 | — | make item; play environmental sfx; launches a projectile; starts script timer 1; tests game flag 42; tests game flag 43; checks a wall of block 373 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 9 | 309 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 9 | 436 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 9 | 219 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 379 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 435 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 441 | 1 | 1 | 3 |
| `0x401` script timer 0 | 280 | 2 | 2 | 4 |
| `0x401` script timer 0 | 280 | 2 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 1, y 7 | 9 | x 13, y 14 | 0xffff |  |

## Text shown by the scripts (ids only)

- Level text file `LEVEL09.<lang>`: 6 ids: 0, 1, 2, 4, 5, 9.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL09.ENG --index N`.
