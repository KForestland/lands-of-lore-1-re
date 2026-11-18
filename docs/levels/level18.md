# Level 18

Made by `tools/level_report.py` from `LEVEL18.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 7 = TOWER1 (decorations `TOWER1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: TOWER1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 586 | — | — |  | 0x80 | 63 |
| 1 | 1596 | 1 | — |  | 0x07 | 255 |
| 2 | 1594 | 2 | — |  | 0x07 | 255 |
| 3 | 20 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 16 | 3 | — |  | 0xaf | 13 |
| 18 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 8 | 4 | — |  | 0x04 | 25 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 25 | 38 | 2 | 22 |  | 0x07 | 255 |
| 26 | 1 | 2 | 5 | 2 lever (to on) | 0x07 | 207 |
| 30 | 2 | 2 | 21 | 6 niche | 0x87 | 14 |
| 31 | 2 | 1 | 28 | 1 clickable wall | 0x07 | 210 |
| 37 | 4 | — | — |  | 0x07 | 255 |
| 42 | 1 | 2 | 32 | 1 clickable wall | 0x07 | 255 |
| 44 | 4 | — | 25 |  | 0x07 | 255 |
| 45 | 4 | 3 | 26 |  | 0x84 | 63 |
| 46 | 1 | 1 | 7 | 2 lever (to on) | 0x07 | 207 |
| 48 | 20 | 1 | 42 | 1 clickable wall | 0x07 | 255 |
| 49 | 21 | 1 | 43 | 1 clickable wall | 0x07 | 255 |
| 50 | 1 | 1 | 11 | 2 lever (to on) | 0x07 | 207 |
| 54 | 1 | 2 | 15 | 1 clickable wall | 0x07 | 207 |
| 56 | 1 | 2 | 65 | 1 clickable wall | 0x07 | 255 |
| 57 | 1 | 2 | 37 | 1 clickable wall | 0x07 | 207 |
| 58 | 1 | 2 | 19 | 2 lever (to on) | 0x07 | 207 |
| 60 | 2 | 2 | 24 | 1 clickable wall | 0x07 | 207 |
| 61 | 4 | 1 | 57 | 1 clickable wall | 0x07 | 207 |
| 71 | 2 | 1 | 41 | 2 lever (to on) | 0x07 | 255 |
| 73 | 26 | 1 | 44 |  | 0x07 | 255 |
| 74 | 19 | 1 | 45 |  | 0x07 | 255 |
| 75 | 20 | 1 | 46 |  | 0x07 | 255 |
| 76 | 27 | 2 | 51 |  | 0x07 | 255 |
| 77 | 21 | 2 | 52 |  | 0x07 | 255 |
| 78 | 23 | 2 | 53 |  | 0x07 | 255 |
| 79 | 23 | 2 | 50 |  | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 37 (x 5, y 1) | south | 49 | clickable wall |
| 42 (x 10, y 1) | south | 58 | lever (to on) |
| 43 (x 11, y 1) | south | 49 | clickable wall |
| 45 (x 13, y 1) | south | 48 | clickable wall |
| 71 (x 7, y 2) | west | 48 | clickable wall |
| 73 (x 9, y 2) | east | 56 | clickable wall |
| 76 (x 12, y 2) | east | 61 | clickable wall |
| 137 (x 9, y 4) | south | 61 | clickable wall |
| 140 (x 12, y 4) | east | 54 | clickable wall |
| 140 (x 12, y 4) | south | 48 | clickable wall |
| 142 (x 14, y 4) | north | 49 | clickable wall |
| 161 (x 1, y 5) | south | 48 | clickable wall |
| 165 (x 5, y 5) | north | 3 | door / door switch |
| 165 (x 5, y 5) | south | 3 | door / door switch |
| 174 (x 14, y 5) | east | 49 | clickable wall |
| 177 (x 17, y 5) | south | 71 | lever (to on) |
| 195 (x 3, y 6) | east | 3 | door / door switch |
| 195 (x 3, y 6) | west | 3 | door / door switch |
| 201 (x 9, y 6) | east | 48 | clickable wall |
| 201 (x 9, y 6) | south | 31 | clickable wall |
| 201 (x 9, y 6) | west | 49 | clickable wall |
| 206 (x 14, y 6) | south | 61 | clickable wall |
| 207 (x 15, y 6) | north | 3 | door / door switch |
| 207 (x 15, y 6) | south | 3 | door / door switch |
| 208 (x 16, y 6) | north | 49 | clickable wall |
| 208 (x 16, y 6) | south | 48 | clickable wall |
| 225 (x 1, y 7) | north | 49 | clickable wall |
| 229 (x 5, y 7) | north | 49 | clickable wall |
| 232 (x 8, y 7) | west | 48 | clickable wall |
| 234 (x 10, y 7) | east | 49 | clickable wall |
| 236 (x 12, y 7) | south | 42 | clickable wall |
| 242 (x 18, y 7) | west | 49 | clickable wall |
| 259 (x 3, y 8) | east | 3 | door / door switch |
| 259 (x 3, y 8) | west | 3 | door / door switch |
| 264 (x 8, y 8) | east | 3 | door / door switch |
| 264 (x 8, y 8) | west | 3 | door / door switch |
| 273 (x 17, y 8) | north | 3 | door / door switch |
| 273 (x 17, y 8) | south | 3 | door / door switch |
| 288 (x 0, y 9) | east | 49 | clickable wall |
| 296 (x 8, y 9) | west | 48 | clickable wall |
| 297 (x 9, y 9) | north | 48 | clickable wall |
| 306 (x 18, y 9) | west | 48 | clickable wall |
| 322 (x 2, y 10) | south | 49 | clickable wall |
| 325 (x 5, y 10) | west | 49 | clickable wall |
| 331 (x 11, y 10) | east | 3 | door / door switch |
| 331 (x 11, y 10) | west | 3 | door / door switch |
| 333 (x 13, y 10) | east | 3 | door / door switch |
| 333 (x 13, y 10) | west | 3 | door / door switch |
| 336 (x 16, y 10) | north | 49 | clickable wall |
| 336 (x 16, y 10) | south | 46 | lever (to on) |
| 386 (x 2, y 12) | north | 60 | clickable wall |
| 389 (x 5, y 12) | east | 60 | clickable wall |
| 393 (x 9, y 12) | south | 30 | niche |
| 397 (x 13, y 12) | east | 57 | clickable wall |
| 397 (x 13, y 12) | west | 26 | lever (to on) |
| 400 (x 16, y 12) | north | 48 | clickable wall |
| 418 (x 2, y 13) | east | 48 | clickable wall |
| 424 (x 8, y 13) | east | 48 | clickable wall |
| 450 (x 2, y 14) | south | 48 | clickable wall |
| 453 (x 5, y 14) | east | 48 | clickable wall |
| 459 (x 11, y 14) | east | 49 | clickable wall |
| 463 (x 15, y 14) | west | 49 | clickable wall |
| 489 (x 9, y 15) | west | 71 | lever (to on) |
| 491 (x 11, y 15) | south | 30 | niche |
| 492 (x 12, y 15) | north | 3 | door / door switch |
| 492 (x 12, y 15) | south | 3 | door / door switch |
| 493 (x 13, y 15) | south | 49 | clickable wall |
| 494 (x 14, y 15) | north | 31 | clickable wall |
| 494 (x 14, y 15) | east | 48 | clickable wall |
| 514 (x 2, y 16) | north | 49 | clickable wall |
| 518 (x 6, y 16) | north | 61 | clickable wall |
| 518 (x 6, y 16) | south | 49 | clickable wall |
| 521 (x 9, y 16) | east | 48 | clickable wall |
| 528 (x 16, y 16) | north | 48 | clickable wall |
| 553 (x 9, y 17) | east | 3 | door / door switch |
| 553 (x 9, y 17) | west | 3 | door / door switch |
| 555 (x 11, y 17) | west | 49 | clickable wall |
| 559 (x 15, y 17) | north | 50 | lever (to on) |
| 581 (x 5, y 18) | east | 48 | clickable wall |
| 619 (x 11, y 19) | north | 49 | clickable wall |
| 621 (x 13, y 19) | north | 48 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL18.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles TOWER1; loads monster sprites AMAZON.SHP into slot 0; loads monster sprites ARCHRSLG.SHP into slot 1; defines monster type 1; defines monster type 2; defines monster type 3 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 550; places a monster (slot 1) on block 176; places a monster (slot 1) on block 172; places a monster (slot 1) on block 77; places a monster (slot 1) on block 110; places a monster (slot 1) on block 70; places a monster (slot 1) on block 162; places a monster (slot 1) on block 290 … |

### LEVEL18.INF

| Entry | Events | What it does |
|---|---|---|
| block 40 (x 8, y 1) | wall clicked | sets the north wall of block 996 to type 1; sets the north wall of block 994 to type 0; sets the east wall of block 994 to type 0; sets the south wall of block 994 to type 0; sets the west wall of block 994 to type 0; sets the north wall of block 996 to type 2; sets the ? wall of block 994 to type 1; sets the north wall of block 996 to type 3 … |
| block 42 (x 10, y 1) | wall clicked | toggles the east wall of block 73 between types 30 and 56; plays a sound |
| block 72 (x 8, y 2) | party steps in, party arrives (second path), party leaves, item put down, bits 0x4000 (no engine caller found) | moves objects from block 72 to block 167; set global var; plays a sound; tests game flag 347; checks a wall of block 996 |
| block 75 (x 11, y 2) | party steps in, bits 0x4000 (no engine caller found) | gives 9 crown(s); places item 226 (Amber Ring) on block 73; places item 243 (Coin Purse) on block 74; sets the east wall of block 73 to type 30; gives item 226 (Amber Ring); gives 8 crown(s); gives 5 crown(s); sets the north wall of block 996 to type 2 … |
| block 76 (x 12, y 2) | wall clicked | sets the east wall of block 76 to type 65; a character speaks |
| block 137 (x 9, y 4) | wall clicked | sets the south wall of block 137 to type 64; a character speaks |
| block 140 (x 12, y 4) | wall clicked | sets the east wall of block 140 to type 55; operates the door at block 108; sets the east wall of block 140 to type 54; a character speaks; checks a wall of block 76; plays a sound; checks a wall of block 140 |
| block 201 (x 9, y 6) | wall clicked | sets the south wall of block 993 to type 0; checks a wall of block 992 |
| block 206 (x 14, y 6) | wall clicked | sets the south wall of block 206 to type 65; a character speaks |
| block 233 (x 9, y 7) | bits 0x400 (no engine caller found) | sets the south wall of block 993 to type 0; checks a wall of block 992 |
| block 264 (x 8, y 8) | wall clicked | toggles the west wall of block 266 between types 76 and 0; plays a sound |
| block 330 (x 10, y 10) | party steps in, party arrives (second path), item put down | moves objects from block 330 to block 329 |
| block 334 (x 14, y 10) | party steps in, party arrives (second path), item put down | moves objects from block 334 to block 335 |
| block 336 (x 16, y 10) | wall clicked | operates the door at block 337; plays a sound; checks a wall of block 336 |
| block 386 (x 2, y 12) | wall clicked | a character speaks |
| block 389 (x 5, y 12) | wall clicked | a character speaks |
| block 393 (x 9, y 12) | item taken | sets the west wall of block 424 to type 0; checks a wall of block 424; plays a sound |
| block 397 (x 13, y 12) | wall clicked | sets the east wall of block 397 to type ?; sets the east wall of block 397 to type 57; operates the door at block 429; sets the east wall of block 397 to type 28; sets the north wall of block 995 to type 28; sets the east wall of block 397 to type 29; sets the north wall of block 995 to type 29; make item … |
| block 426 (x 10, y 13) | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 350; changes a monster; tests game flag 350 |
| block 449 (x 1, y 14) | party steps in, party arrives (second path), item put down | moves objects from block 449 to block 198 |
| block 457 (x 9, y 14) | party arrives (second path), bits 0x10 (no engine caller found) | sets game flag 350; changes a monster; tests game flag 350 |
| block 462 (x 14, y 14) | bits 0x400 (no engine caller found) | deals damage; sets the south wall of block 993 to type 0; checks a wall of block 993 |
| block 491 (x 11, y 15) | item put down, item taken | sets the west wall of block 490 to type 0; sets the north wall of block 490 to type 77; sets the south wall of block 490 to type 76; plays a sound |
| block 494 (x 14, y 15) | wall clicked | deals damage; sets the south wall of block 993 to type 0; checks a wall of block 993 |
| block 518 (x 6, y 16) | wall clicked | sets the north wall of block 518 to type 62; a character speaks |
| block 559 (x 15, y 17) | wall clicked | operates the door at block 526; places item 226 (Amber Ring) on block 73; sets the east wall of block 73 to type 30; gives item 226 (Amber Ring); places item 243 (Coin Purse) on block 74; place inventory item in hand; starts a dialogue; sets/clears game flag 345 … |
| block 620 (x 12, y 19) | party steps in, party arrives (second path), item put down, fireball passes | moves objects from block 620 to block 689 |
| `0x400` level loaded | — | drops the party through a pit; clears game flag 46; starts script timer 0; tests game flag 46 |
| `0x401` script timer 0 | — | places a monster (slot 3) on block 209; places a monster (slot 3) on block 488; checks a wall of block 177; checks a wall of block 489 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 97 | Rapier "Talon" | 18 | 586 |
| INI entry 1 (runs when the level loads) | 120 | Star "Vega" | 18 | 268 |
| INI entry 1 (runs when the level loads) | 245 | Lockpicks | 18 | 110 |
| INI entry 1 (runs when the level loads) | 44 | Dagger | 18 | 110 |
| INI entry 1 (runs when the level loads) | 192 | Mystic Key | 18 | 548 |
| INI entry 1 (runs when the level loads) | 196 | Mystic Key | 18 | 393 |
| INI entry 1 (runs when the level loads) | 268 | Note | 18 | 491 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 243 | Coin Purse | 18 | 74 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 243 | Coin Purse | 18 | 74 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 243 | Coin Purse | 18 | 74 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 226 | Amber Ring | 18 | 73 |
| block 75 (x 11, y 2) | 243 | Coin Purse | 18 | 74 |
| block 559 (x 15, y 17) | 226 | Amber Ring | 18 | 73 |
| block 559 (x 15, y 17) | 226 | Amber Ring | 18 | 73 |
| block 559 (x 15, y 17) | 243 | Coin Purse | 18 | 74 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 550 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 550 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 550 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 550 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 176 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 176 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 176 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 176 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 172 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 172 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 77 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 77 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 110 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 110 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 70 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 70 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 70 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 70 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 162 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 162 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 162 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 162 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 290 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 290 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 290 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 290 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 425 | 2 | 2 | 2 |
| INI entry 1 (runs when the level loads) | 304 | 1 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 368 | 1 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 527 | 0 | 1 | 3 |
| `0x401` script timer 0 | 209 | 2 | 3 | 4 |
| `0x401` script timer 0 | 488 | 3 | 3 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 10, y 14 | 4 | x 10, y 15 | 0x41f3 | QUEEN JANA |
| x 8, y 1 | 1 | x 8, y 2 | 0x41f4 | ALTAR DE BLANCA |
| x 10, y 2 | 2 | x 10, y 2 | 0x41f5 | LYLE'S CELL |

## Text shown by the scripts (ids only)

- Level text file `LEVEL18.<lang>`: 14 ids: 1, 3, 12, 21, 25, 26, 27, 28, 40, 45, 46, 47, 48, 49.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL18.ENG --index N`.
