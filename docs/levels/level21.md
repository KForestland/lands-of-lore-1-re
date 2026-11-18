# Level 21

Made by `tools/level_report.py` from `LEVEL21.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 7 = TOWER1 (decorations `TOWER1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: TOWER1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 539 | — | — |  | 0x80 | 63 |
| 1 | 1614 | 1 | — |  | 0x07 | 255 |
| 2 | 1615 | 2 | — |  | 0x07 | 255 |
| 3 | 16 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 10 | 3 | — |  | 0xaf | 13 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 25 | 25 | 2 | 22 |  | 0x07 | 255 |
| 26 | 1 | 2 | 5 | 1 clickable wall | 0x07 | 207 |
| 30 | 1 | 2 | 21 | 6 niche | 0x87 | 14 |
| 31 | 7 | 1 | 28 | 1 clickable wall | 0x07 | 210 |
| 35 | 8 | — | 2 |  | 0x80 | 10 |
| 38 | 4 | — | 1 |  | 0x84 | 11 |
| 40 | 8 | 2 | — |  | 0x80 | 214 |
| 41 | 4 | 2 | — |  | 0x84 | 214 |
| 42 | 2 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 46 | 1 | 1 | 7 | 2 lever (to on) | 0x07 | 207 |
| 48 | 1 | — | 9 | 2 lever (to on) | 0x80 | 207 |
| 52 | 1 | 1 | 13 | 2 lever (to on) | 0x07 | 207 |
| 57 | 2 | 2 | 37 | 1 clickable wall | 0x07 | 207 |
| 60 | 1 | 2 | 24 | 1 clickable wall | 0x07 | 207 |
| 61 | 2 | 1 | 57 | 1 clickable wall | 0x07 | 207 |
| 71 | 21 | 1 | 42 |  | 0x07 | 255 |
| 72 | 27 | 1 | 43 |  | 0x07 | 255 |
| 73 | 24 | 1 | 44 |  | 0x07 | 255 |
| 74 | 23 | 1 | 45 |  | 0x07 | 255 |
| 75 | 18 | 1 | 46 |  | 0x07 | 255 |
| 76 | 18 | 2 | 51 |  | 0x07 | 255 |
| 77 | 35 | 2 | 52 |  | 0x07 | 255 |
| 78 | 34 | 2 | 53 |  | 0x07 | 255 |
| 79 | 30 | 2 | 50 |  | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 37 (x 5, y 1) | south | 30 | niche |
| 103 (x 7, y 3) | north | 61 | clickable wall |
| 105 (x 9, y 3) | north | 3 | door / door switch |
| 105 (x 9, y 3) | south | 3 | door / door switch |
| 107 (x 11, y 3) | north | 60 | clickable wall |
| 110 (x 14, y 3) | north | 3 | door / door switch |
| 110 (x 14, y 3) | south | 3 | door / door switch |
| 144 (x 16, y 4) | south | 31 | clickable wall |
| 197 (x 5, y 6) | east | 26 | clickable wall |
| 201 (x 9, y 6) | west | 46 | lever (to on) |
| 210 (x 18, y 6) | west | 31 | clickable wall |
| 239 (x 15, y 7) | north | 3 | door / door switch |
| 239 (x 15, y 7) | south | 3 | door / door switch |
| 263 (x 7, y 8) | south | 57 | clickable wall |
| 291 (x 3, y 9) | north | 31 | clickable wall |
| 356 (x 4, y 11) | east | 52 | lever (to on) |
| 360 (x 8, y 11) | east | 3 | door / door switch |
| 360 (x 8, y 11) | west | 3 | door / door switch |
| 363 (x 11, y 11) | north | 3 | door / door switch |
| 363 (x 11, y 11) | south | 3 | door / door switch |
| 396 (x 12, y 12) | east | 31 | clickable wall |
| 449 (x 1, y 14) | north | 31 | clickable wall |
| 455 (x 7, y 14) | north | 57 | clickable wall |
| 459 (x 11, y 14) | north | 31 | clickable wall |
| 484 (x 4, y 15) | north | 3 | door / door switch |
| 484 (x 4, y 15) | south | 3 | door / door switch |
| 485 (x 5, y 15) | east | 31 | clickable wall |
| 489 (x 9, y 15) | east | 3 | door / door switch |
| 489 (x 9, y 15) | west | 3 | door / door switch |
| 524 (x 12, y 16) | south | 61 | clickable wall |
| 589 (x 13, y 18) | east | 3 | door / door switch |
| 589 (x 13, y 18) | west | 3 | door / door switch |
| 590 (x 14, y 18) | west | 48 | lever (to on) |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL21.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles TOWER1; loads monster sprites APARITIN.SHP into slot 0; loads monster sprites WRAITH.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 487; places a monster (slot 1) on block 583; places a monster (slot 2) on block 361; places a monster (slot 2) on block 425; places a monster (slot 1) on block 297; places a monster (slot 2) on block 395; places a monster (slot 2) on block 208; places a monster (slot 2) on block 385 … |

### LEVEL21.INF

| Entry | Events | What it does |
|---|---|---|
| block 103 (x 7, y 3) | wall clicked | sets the north wall of block 103 to type 67; a character speaks |
| block 107 (x 11, y 3) | wall clicked | a character speaks |
| block 144 (x 16, y 4) | wall clicked | checks a wall of block 144 |
| block 176 (x 16, y 5) | bits 0x400 (no engine caller found) | checks a wall of block 144 |
| block 197 (x 5, y 6) | wall clicked, thrown item hits | toggles the east wall of block 197 between types 27 and 26; sets the west wall of block 199 to type 0; sets the west wall of block 199 to type 38; moves objects from block 199 to block 199; plays a sound; checks a wall of block 197; checks a wall of block 201; checks a wall of block 199 |
| block 199 (x 7, y 6) | party arrives (second path), item put down | drops the party through a pit; deals damage; moves the party to level 20, block 199; sets game flag 46; moves objects from block 199 to block 199; checks a wall of block 199 |
| block 201 (x 9, y 6) | wall clicked | sets the west wall of block 199 to type 0; sets the west wall of block 199 to type 38; moves objects from block 199 to block 199; plays a sound; checks a wall of block 197; checks a wall of block 201; checks a wall of block 199 |
| block 209 (x 17, y 6) | bits 0x400 (no engine caller found) | checks a wall of block 210 |
| block 210 (x 18, y 6) | wall clicked | checks a wall of block 210 |
| block 239 (x 15, y 7) | wall clicked | sets game flag 361; block door; tests game flag 361; plays a sound |
| block 259 (x 3, y 8) | bits 0x400 (no engine caller found) | gives 8 crown(s); a character speaks |
| block 263 (x 7, y 8) | wall clicked | sets the south wall of block 263 to type ?; checks a wall of block 263; plays a sound; checks a wall of block 1000 |
| block 291 (x 3, y 9) | wall clicked | gives 8 crown(s); a character speaks |
| block 298 (x 10, y 9) | party arrives (second path) | sets the west wall of block 298 to type 40 |
| block 301 (x 13, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 301 to type 36; checks a wall of block 301; plays a sound; checks a wall of block 304 |
| block 304 (x 16, y 9) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 304 to type 36; checks a wall of block 304; plays a sound; checks a wall of block 301 |
| block 321 (x 1, y 10) | party arrives (second path) | changes a monster; sets game flag 335; tests game flag 335 |
| block 356 (x 4, y 11) | wall clicked | toggles the west wall of block 358 between types 0 and 75; plays a sound |
| block 385 (x 1, y 12) | item put down | changes a monster; sets game flag 335; tests game flag 335 |
| block 396 (x 12, y 12) | wall clicked | gives item 233 (Wand of Lightning) |
| block 397 (x 13, y 12) | bits 0x400 (no engine caller found) | gives item 233 (Wand of Lightning) |
| block 417 (x 1, y 13) | bits 0x400 (no engine caller found) | sets the south wall of block 995 to type 0; checks a wall of block 995 |
| block 427 (x 11, y 13) | bits 0x400 (no engine caller found) | gives item 83 (Long sword "Protector") |
| block 449 (x 1, y 14) | wall clicked | sets the south wall of block 995 to type 0; checks a wall of block 995 |
| block 455 (x 7, y 14) | wall clicked | sets the north wall of block 455 to type ?; checks a wall of block 455; plays a sound; checks a wall of block 999 |
| block 459 (x 11, y 14) | wall clicked | gives item 83 (Long sword "Protector") |
| block 485 (x 5, y 15) | wall clicked | gives item 48 (Dagger "Fang") |
| block 486 (x 6, y 15) | bits 0x400 (no engine caller found) | gives item 48 (Dagger "Fang") |
| block 524 (x 12, y 16) | wall clicked | sets the south wall of block 524 to type 68; a character speaks |
| block 585 (x 9, y 18) | party steps in, party arrives (second path), item put down | moves objects from block 585 to block 992 |
| block 590 (x 14, y 18) | wall clicked | toggles the west wall of block 591 between types 30 and 76; plays a sound |
| `0x400` level loaded | — | a character speaks; sets game flag 360; clears game flag 343; starts script timer 0; starts script timer 1; tests game flag 360 |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 100; places a monster (slot 1) on block 273; places a monster (slot 1) on block 324; clears game flag 130; sets game flag 130; tests game flag 130 |
| `0x402` script timer 1 | — | places a monster (slot 2) on block 261 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 18 | Saber "Cougar" | 21 | 525 |
| INI entry 1 (runs when the level loads) | 36 | Bow "Gemini" | 21 | 399 |
| INI entry 1 (runs when the level loads) | 195 | Mystic Key | 21 | 591 |
| INI entry 1 (runs when the level loads) | 184 | Ivory Key | 21 | 37 |
| INI entry 1 (runs when the level loads) | 216 | Salve | 21 | 525 |
| INI entry 1 (runs when the level loads) | 215 | Bannon's reserve | 21 | 525 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 487 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 487 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 583 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 583 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 361 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 361 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 425 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 425 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 297 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 297 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 395 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 395 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 208 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 208 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 208 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 208 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 385 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 385 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 385 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 73 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 73 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 462 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 462 | 0 | 1 | 3 |
| `0x401` script timer 0 | 100 | 2 | 2 | 4 |
| `0x401` script timer 0 | 100 | 2 | 2 | 4 |
| `0x401` script timer 0 | 273 | 3 | 1 | 4 |
| `0x401` script timer 0 | 273 | 3 | 1 | 4 |
| `0x401` script timer 0 | 273 | 3 | 1 | 4 |
| `0x401` script timer 0 | 324 | 3 | 1 | 4 |
| `0x401` script timer 0 | 324 | 1 | 1 | 4 |
| `0x402` script timer 1 | 261 | 0 | 2 | 4 |
| `0x402` script timer 1 | 261 | 0 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 10, y 18 | 0 | x 10, y 18 | 0x41f7 | WARNING SPIRIT |

## Text shown by the scripts (ids only)

- Level text file `LEVEL21.<lang>`: 4 ids: 1, 2, 13, 15.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL21.ENG --index N`.
