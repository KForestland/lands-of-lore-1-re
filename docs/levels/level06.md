# Level 6

Made by `tools/level_report.py` from `LEVEL6.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 382 | — | — |  | 0x80 | 63 |
| 1 | 1832 | 1 | — |  | 0x07 | 255 |
| 2 | 1836 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 35 | 8 | — | 20 |  | 0x80 | 10 |
| 38 | 12 | — | 19 |  | 0x84 | 11 |
| 41 | 2 | 1 | 45 |  | 0x07 | 255 |
| 42 | 1 | 2 | 70 | 2 lever (to on) | 0x07 | 207 |
| 54 | 1 | 1 | 29 | 2 lever (to on) | 0x07 | 207 |
| 56 | 1 | 1 | 31 | 2 lever (to on) | 0x07 | 207 |
| 58 | 1 | 1 | 27 | 2 lever (to on) | 0x07 | 207 |
| 63 | 2 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 65 | 1 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 74 | 4 | — | 55 |  | 0x84 | 63 |
| 75 | 2 | 1 | 61 | 2 lever (to on) | 0x07 | 207 |
| 77 | 2 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 1 | 1 | 60 | 1 clickable wall | 0x07 | 255 |
| 79 | 2 | 2 | 64 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 108 (x 12, y 3) | west | 65 | clickable wall |
| 141 (x 13, y 4) | south | 75 | lever (to on) |
| 145 (x 17, y 4) | south | 78 | clickable wall |
| 200 (x 8, y 6) | west | 79 | clickable wall |
| 206 (x 14, y 6) | north | 77 | clickable wall |
| 212 (x 20, y 6) | north | 77 | clickable wall |
| 256 (x 0, y 8) | east | 58 | lever (to on) |
| 258 (x 2, y 8) | west | 56 | lever (to on) |
| 261 (x 5, y 8) | north | 79 | clickable wall |
| 264 (x 8, y 8) | north | 63 | clickable wall |
| 289 (x 1, y 9) | north | 54 | lever (to on) |
| 453 (x 5, y 14) | west | 75 | lever (to on) |
| 458 (x 10, y 14) | south | 42 | lever (to on) |
| 459 (x 11, y 14) | north | 63 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL6.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; loads monster sprites BANDIT.SHP into slot 0; loads monster sprites RATMAN.SHP into slot 1; defines monster type 1; defines monster type 3 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 229; places a monster (slot 1) on block 198; places a monster (slot 3) on block 235; places a monster (slot 3) on block 267; places a monster (slot 3) on block 233; places a monster (slot 3) on block 425; places a monster (slot 3) on block 427; places a monster (slot 3) on block 426 … |

### LEVEL6.INF

| Entry | Events | What it does |
|---|---|---|
| block 103 (x 7, y 3) | party arrives (second path) | sets game flag 124; a character speaks; tests game flag 124 |
| block 104 (x 8, y 3) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 104 to type 36; make item; launches a projectile; checks a wall of block 104; plays a sound |
| block 108 (x 12, y 3) | wall clicked | a character speaks |
| block 118 (x 22, y 3) | party steps in, party arrives (second path), item put down | moves objects from block 118 to block 86 |
| block 129 (x 1, y 4) | party arrives (second path) | clears game flag 64 |
| block 132 (x 4, y 4) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 132 to type 36; operates the door at block 165; a character speaks; sets game flag 128; checks a wall of block 132; plays a sound; tests game flag 128 |
| block 133 (x 5, y 4) | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 132 to type 36; changes a monster; sets game flag 129; a character speaks; tests game flag 129; checks a wall of block 132; plays a sound |
| block 141 (x 13, y 4) | wall clicked | sets the west wall of block 203 to type 1; sets the west wall of block 170 to type 2; sets the west wall of block 172 to type 0; sets the west wall of block 162 to type 0; sets the west wall of block 163 to type 0; sets the west wall of block 194 to type 0; sets the west wall of block 195 to type 0; plays a sound |
| block 161 (x 1, y 5) | party arrives (second path) | sets the west wall of block 194 to type 0; sets the west wall of block 194 to type 38; drops the party through a pit; deals damage; moves the party to level 7, block 194; sets the west wall of block 162 to type 0; sets the west wall of block 162 to type 38; moves the party to level 7, block 162 … |
| block 162 (x 2, y 5) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 162; sets game flag 46; moves objects from block 162 to block 162; checks a wall of block 162 |
| block 163 (x 3, y 5) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 163; sets game flag 46; moves objects from block 163 to block 163; checks a wall of block 163 |
| block 194 (x 2, y 6) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 194; sets game flag 46; moves objects from block 194 to block 194; checks a wall of block 194 |
| block 195 (x 3, y 6) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 195; sets game flag 46; moves objects from block 195 to block 195; checks a wall of block 195 |
| block 200 (x 8, y 6) | wall clicked | a character speaks |
| block 225 (x 1, y 7) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 225; sets game flag 46; moves objects from block 225 to block 225; checks a wall of block 225 |
| block 232 (x 8, y 7) | party arrives (second path), bits 0x410 (no engine caller found) | sets the north wall of block 264 to type 64; a character speaks; sets game flag 121; checks a wall of block 264; plays a sound; set global script var; tests game flag 121 |
| block 256 (x 0, y 8) | wall clicked | sets the west wall of block 194 to type 0; sets the west wall of block 194 to type 38; drops the party through a pit; deals damage; moves the party to level 7, block 194; sets the west wall of block 225 to type 0; sets the west wall of block 225 to type 38; moves the party to level 7, block 225 … |
| block 258 (x 2, y 8) | party steps in, party arrives (second path), wall clicked, item put down | sets the west wall of block 163 to type 0; sets the west wall of block 163 to type 38; drops the party through a pit; deals damage; moves the party to level 7, block 163; sets the west wall of block 195 to type 0; sets the west wall of block 195 to type 38; moves the party to level 7, block 195 … |
| block 259 (x 3, y 8) | party arrives (second path) | sets game flag 64 |
| block 261 (x 5, y 8) | wall clicked | a character speaks |
| block 289 (x 1, y 9) | wall clicked | sets the west wall of block 162 to type 0; sets the west wall of block 162 to type 38; drops the party through a pit; deals damage; moves the party to level 7, block 162; sets the west wall of block 194 to type 0; sets the west wall of block 194 to type 38; moves the party to level 7, block 194 … |
| block 290 (x 2, y 9) | party arrives (second path) | sets game flag 164; a character speaks; tests game flag 125; tests game flag 164 |
| block 390 (x 6, y 12) | party arrives (second path) | shows a message; tests game flag 127; set global var |
| block 422 (x 6, y 13) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; changes a monster; sets game flag 127; tests game flag 127 |
| block 427 (x 11, y 13) | party arrives (second path), bits 0x410 (no engine caller found) | sets the north wall of block 459 to type 63; sets the north wall of block 459 to type 64; a character speaks; sets game flag 122; checks a wall of block 459; plays a sound; set global script var; tests game flag 122 |
| block 449 (x 1, y 14) | party arrives (second path) | a character speaks; starts a dialogue; sets game flag 120; tests game flag 120 |
| block 452 (x 4, y 14) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; sets game flag 137; tests game flag 137 |
| block 453 (x 5, y 14) | wall clicked | toggles the west wall of block 422 between types 0 and 2; a character speaks; sets game flag 126; tests game flag 126; plays a sound |
| block 455 (x 7, y 14) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 7, block 455; sets game flag 46; moves objects from block 455 to block 455; checks a wall of block 455 |
| block 458 (x 10, y 14) | wall clicked | toggles the west wall of block 487 between types 0 and 1; toggles the west wall of block 486 between types 0 and 1; a character speaks; sets game flag 123; plays a sound; tests game flag 123 |
| block 481 (x 1, y 15) | party steps in, party arrives (second path), item put down | moves the party to level 2, block 45; moves objects from block 481 to block 45; shows a message; set global var |
| `0x400` level loaded | — | sets the south wall of block 258 to type 70; starts script timer 0; tests game flag 125 |
| `0x401` script timer 0 | — | places a monster (slot 3) on block 262 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 6 | 167 |
| INI entry 1 (runs when the level loads) | 245 | Lockpicks | 6 | 168 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 6 | 168 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 168 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 6 | 296 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 296 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 296 |
| INI entry 1 (runs when the level loads) | 249 | Lantern | 6 | 483 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 229 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 229 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 198 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 198 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 235 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 267 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 233 | 1 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 425 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 427 | 3 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 426 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 358 | 2 | 3 | 3 |
| `0x401` script timer 0 | 262 | 2 | 3 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 1, y 15 | 0 | x 1, y 14 | 0x41de | FOREST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL06.<lang>`: 22 ids: 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 29.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL06.ENG --index N`.
