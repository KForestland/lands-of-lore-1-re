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

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL13.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles MINE1; loads monster sprites GIMLET.SHP into slot 0; loads monster sprites IRONGRZR.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 147; places a monster (slot 2) on block 107; places a monster (slot 2) on block 485; places a monster (slot 2) on block 456; places a monster (slot 2) on block 493; places a monster (slot 1) on block 497; places item 99 (Rock) on block 293; places item 92 (Mace "Puma") on block 369 … |

### LEVEL13.INF

| Entry | Events | What it does |
|---|---|---|
| block 52 (x 20, y 1) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 14, block 180; moves objects from block 52 to block 14; sets game flag 46; checks a wall of block 52 |
| block 53 (x 21, y 1) | party arrives (second path) | sets the west wall of block 52 to type 0 |
| block 81 (x 17, y 2) | wall clicked | a character speaks |
| block 83 (x 19, y 2) | wall clicked | sets the west wall of block 52 to type 38; sets the west wall of block 116 to type 0; operates the door at block 116; places a monster (slot 1) on block 116; sets the west wall of block 116 to type 44; places a monster (slot 2) on block 116; sets the west wall of block 52 to type 0; moves objects from block 52 to block 52 … |
| block 116 (x 20, y 3) | party steps in, party arrives (second path), item put down | moves objects from block 116 to block 246; move party; moves objects from block 116 to block 332; checks a wall of block 116; checks a wall of block 21; checks a wall of block 85; plays a sound |
| block 143 (x 15, y 4) | party steps in, party arrives (second path), item put down | moves objects from block 143 to block 207 |
| block 227 (x 3, y 7) | party steps in, party arrives (second path), item put down | moves objects from block 227 to block 323 |
| block 282 (x 26, y 8) | item put down | sets the west wall of block 314 to type 0; sets the west wall of block 316 to type 0; checks a wall of block 314; plays a sound |
| block 293 (x 5, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 340 to type 0; sets the west wall of block 372 to type 1; sets the west wall of block 340 to type 1; sets the west wall of block 372 to type 0; checks a wall of block 372; plays a sound |
| block 294 (x 6, y 9) | wall clicked | a character speaks |
| block 313 (x 25, y 9) | wall clicked | sets the west wall of block 314 to type 0; sets the west wall of block 314 to type 38; drops the party through a pit; deals damage; moves the party to level 14, block 442; moves objects from block 314 to block 442; sets game flag 46; plays a sound … |
| block 314 (x 26, y 9) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 14, block 442; moves objects from block 314 to block 14; sets game flag 46; checks a wall of block 314 |
| block 316 (x 28, y 9) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 14, block 444; moves objects from block 316 to block 14; sets game flag 46; checks a wall of block 316 |
| block 324 (x 4, y 10) | wall clicked | a character speaks |
| block 343 (x 23, y 10) | wall clicked | sets the west wall of block 375 to type 0; a character speaks; delete hand item; checks a wall of block 375; plays a sound |
| block 349 (x 29, y 10) | wall clicked | sets the west wall of block 316 to type 0; sets the west wall of block 316 to type 38; drops the party through a pit; deals damage; moves the party to level 14, block 444; sets the west wall of block 349 to type 32; moves objects from block 316 to block 444; sets game flag 46 … |
| block 355 (x 3, y 11) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 14, block 483; moves objects from block 355 to block 14; sets game flag 46; checks a wall of block 355 |
| block 356 (x 4, y 11) | wall clicked | sets the west wall of block 355 to type 0; sets the west wall of block 355 to type 38; drops the party through a pit; deals damage; moves the party to level 14, block 483; moves objects from block 355 to block 483; sets game flag 46; plays a sound … |
| block 378 (x 26, y 11) | item taken | sets the west wall of block 314 to type 38; moves objects from block 314 to block 14; checks a wall of block 314; plays a sound |
| block 400 (x 16, y 12) | wall clicked | a character speaks |
| block 528 (x 16, y 16) | bits 0x400 (no engine caller found) | gives item 154 (Hale leather jerkin) |
| block 560 (x 16, y 17) | wall clicked | gives item 154 (Hale leather jerkin) |
| `0x400` level loaded | — | starts script timer 0; starts script timer 1 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 101; places a monster (slot 1) on block 246 |
| `0x402` script timer 1 | — | places a monster (slot 2) on block 338; checks a wall of block 372 |

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
