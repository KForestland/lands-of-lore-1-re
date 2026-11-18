# Level 5

Made by `tools/level_report.py` from `LEVEL5.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 92 | — | — |  | 0x80 | 63 |
| 1 | 1992 | 1 | — |  | 0x07 | 255 |
| 2 | 1992 | 2 | — |  | 0x07 | 255 |
| 29 | 1 | 2 | 51 | 1 clickable wall | 0x07 | 207 |
| 31 | 1 | 1 | 23 | 2 lever (to on) | 0x07 | 207 |
| 35 | 8 | — | 20 |  | 0x80 | 10 |
| 36 | 4 | — | 21 |  | 0x80 | 10 |
| 42 | 1 | 1 | 15 | 1 clickable wall | 0x07 | 207 |
| 53 | 1 | 2 | 26 | 1 clickable wall | 0x07 | 210 |
| 74 | 4 | — | 55 |  | 0x84 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 32 (x 0, y 1) | east | 53 | clickable wall |
| 67 (x 3, y 2) | north | 42 | clickable wall |
| 132 (x 4, y 4) | east | 29 | clickable wall |
| 162 (x 2, y 5) | south | 31 | lever (to on) |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL5.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; loads monster sprites THUG.SHP into slot 0; defines monster type 1 |
| INI entry 1 (runs when the level loads) | — | places item 99 (Rock) on block 195; places item 99 (Rock) on block 102; places item 243 (Coin Purse) on block 193; places item 243 (Coin Purse) on block 136; places item 43 (Weathered dagger) on block 131; places item 137 (Torn shirt) on block 131; places item 247 (Broken glass) on block 39; places item 247 (Broken glass) on block 135 … |

### LEVEL5.INF

| Entry | Events | What it does |
|---|---|---|
| block 3 (x 3, y 0) | wall clicked | sets the south wall of block 3 to type 43; sets the east wall of block 34 to type 33; sets the south wall of block 3 to type 42; sets the east wall of block 34 to type 2; tests game flag 47; checks a wall of block 3; plays a sound |
| block 32 (x 0, y 1) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 33 (x 1, y 1) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 34 (x 2, y 1) | wall clicked | sets the west wall of block 34 to type 0; sets game flag 47; plays a sound |
| block 36 (x 4, y 1) | party arrives (second path), party leaves (second path) | sets the north wall of block 993 to type ?; sets the west wall of block 34 to type 0; sets the east wall of block 34 to type ?; tests game flag 47; plays a sound; checks a wall of block 34; checks a wall of block 993 |
| block 67 (x 3, y 2) | wall clicked | sets the north wall of block 67 to type 43; sets the south wall of block 3 to type 42; sets the north wall of block 67 to type 42; sets the south wall of block 3 to type 1; sets the east wall of block 34 to type 2; tests game flag 47; checks a wall of block 67; plays a sound |
| block 100 (x 4, y 3) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 69 to type 0; places a monster (slot 1) on block 259; places a monster (slot 1) on block 260; sets the west wall of block 69 to type 1; sets game flag 119; checks a wall of block 69; plays a sound; tests game flag 38 … |
| block 102 (x 6, y 3) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 69 to type 0; places a monster (slot 1) on block 259; places a monster (slot 1) on block 260; sets the west wall of block 69 to type 1; sets game flag 119; checks a wall of block 69; plays a sound; tests game flag 38 … |
| block 132 (x 4, y 4) | wall clicked | sets the north wall of block 165 to type 1; sets the east wall of block 132 to type 29; sets the north wall of block 165 to type 45; sets the east wall of block 132 to type 30; checks a wall of block 132; plays a sound |
| block 162 (x 2, y 5) | wall clicked | sets the west wall of block 161 to type 0; sets the west wall of block 161 to type 2; plays a sound; checks a wall of block 162 |
| block 261 (x 5, y 8) | party steps in, party arrives (second path), item put down | moves the party to level 2, block 97; shows a message; moves objects from block 261 to block 97; set global var |
| `0x400` level loaded | — | no game action (only stack and screen bookkeeping) |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 5 | 195 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 5 | 102 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 5 | 193 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 5 | 136 |
| INI entry 1 (runs when the level loads) | 43 | Weathered dagger | 5 | 131 |
| INI entry 1 (runs when the level loads) | 137 | Torn shirt | 5 | 131 |
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 5 | 39 |
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 5 | 135 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 5 | 39 |
| INI entry 1 (runs when the level loads) | 167 | Thug's key | 5 | 165 |
| INI entry 1 (runs when the level loads) | 249 | Lantern | 5 | 97 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| block 100 (x 4, y 3) | 259 | 0 | 1 | 4 |
| block 100 (x 4, y 3) | 259 | 0 | 1 | 4 |
| block 100 (x 4, y 3) | 260 | 3 | 1 | 4 |
| block 102 (x 6, y 3) | 259 | 0 | 1 | 4 |
| block 102 (x 6, y 3) | 259 | 0 | 1 | 4 |
| block 102 (x 6, y 3) | 260 | 3 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 5, y 8 | 0 | x 4, y 8 | 0x41de | FOREST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL05.<lang>`: 0 ids: none.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL05.ENG --index N`.
