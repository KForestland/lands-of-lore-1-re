# Level 16

Made by `tools/level_report.py` from `LEVEL16.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 6 = MINE1 (decorations `MINE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MINE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 382 | — | — |  | 0x80 | 63 |
| 3 | 2 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 4 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 31 | 3 | 2 | 14 | 2 lever (to on) | 0x07 | 207 |
| 32 | 1 | 2 | 15 | 3 lever (to off) | 0x07 | 207 |
| 41 | 6 | 1 | 3 |  | 0x07 | 255 |
| 42 | 3 | 1 | 16 | 2 lever (to on) | 0x07 | 207 |
| 44 | 16 | — | — |  | 0x84 | 17 |
| 47 | 2 | 6 | 61 | 1 clickable wall | 0x07 | 207 |
| 53 | 299 | 1 | — |  | 0x07 | 255 |
| 54 | 1701 | 2 | — |  | 0x07 | 255 |
| 55 | 1658 | 6 | — |  | 0x07 | 255 |
| 60 | 1 | 6 | 60 | 1 clickable wall | 0x07 | 207 |
| 66 | 2 | 1 | 37 | 1 clickable wall | 0x07 | 255 |
| 68 | 8 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 79 | 4 | — | 38 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 64 (x 0, y 2) | north | 68 | clickable wall |
| 64 (x 0, y 2) | east | 68 | clickable wall |
| 64 (x 0, y 2) | south | 68 | clickable wall |
| 64 (x 0, y 2) | west | 68 | clickable wall |
| 135 (x 7, y 4) | north | 79 | clickable wall |
| 135 (x 7, y 4) | east | 79 | clickable wall |
| 135 (x 7, y 4) | south | 79 | clickable wall |
| 135 (x 7, y 4) | west | 79 | clickable wall |
| 137 (x 9, y 4) | south | 32 | lever (to off) |
| 139 (x 11, y 4) | west | 31 | lever (to on) |
| 145 (x 17, y 4) | north | 68 | clickable wall |
| 145 (x 17, y 4) | east | 68 | clickable wall |
| 145 (x 17, y 4) | south | 68 | clickable wall |
| 145 (x 17, y 4) | west | 68 | clickable wall |
| 201 (x 9, y 6) | east | 31 | lever (to on) |
| 203 (x 11, y 6) | north | 31 | lever (to on) |
| 236 (x 12, y 7) | north | 47 | clickable wall |
| 260 (x 4, y 8) | south | 42 | lever (to on) |
| 261 (x 5, y 8) | east | 42 | lever (to on) |
| 266 (x 10, y 8) | west | 66 | clickable wall |
| 295 (x 7, y 9) | north | 42 | lever (to on) |
| 358 (x 6, y 11) | north | 60 | clickable wall |
| 360 (x 8, y 11) | north | 47 | clickable wall |
| 418 (x 2, y 13) | east | 66 | clickable wall |
| 451 (x 3, y 14) | north | 3 | door / door switch |
| 451 (x 3, y 14) | south | 3 | door / door switch |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL16.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles MINE1; operates the door at block 174; operates the door at block 207; operates the door at block 238; operates the door at block 141; loads monster sprites ROCKLING.SHP into slot 0; loads monster sprites TREZ.SHP into slot 1; defines monster type 1 … |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 72; places a monster (slot 2) on block 110; places a monster (slot 1) on block 226; places a monster (slot 1) on block 271; places item 248 (Oil Flask) on block 611; places item 262 (Bezel Cup) on block 611; places item 176 (Mine key 4) on block 611; places item 33 (Axe "Vixen") on block 611 … |

### LEVEL16.INF

| Entry | Events | What it does |
|---|---|---|
| block 64 (x 0, y 2) | wall clicked | gives item 210 (Rusty key); sets game flag 226; sets game flag 227; a character speaks; tests game flag 226; tests game flag 227 |
| block 135 (x 7, y 4) | wall clicked | a character speaks |
| block 136 (x 8, y 4) | bits 0x400 (no engine caller found) | sets the east wall of block 0 to type ?; sets the west wall of block 135 to type 0; make item; place move level item; checks a wall of block 135; plays a sound; checks a wall of block 0 |
| block 137 (x 9, y 4) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 139 (x 11, y 4) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 141 (x 13, y 4) | party steps in, party arrives (second path), item put down | moves objects from block 141 to block 292; plays a sound |
| block 145 (x 17, y 4) | wall clicked | gives item 258 (Note); gives item 253 (Gear); sets game flag 224; sets game flag 225; a character speaks; tests game flag 224; tests game flag 225 |
| block 170 (x 10, y 5) | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 0 to type 1; sets the west wall of block 0 to type 0; character surprise feedback; move party; checks a wall of block 0; checks a wall of block 201; checks a wall of block 137; checks a wall of block 139 … |
| block 174 (x 14, y 5) | party steps in, party arrives (second path), item put down | moves objects from block 174 to block 246; plays a sound |
| block 196 (x 4, y 6) | wall clicked | a character speaks |
| block 197 (x 5, y 6) | bits 0x400 (no engine caller found) | sets the south wall of block 0 to type ?; sets the west wall of block 196 to type 0; make item; place move level item; checks a wall of block 196; plays a sound; checks a wall of block 0 |
| block 198 (x 6, y 6) | party arrives (second path) | sets the west wall of block 196 to type 79; sets game flag 228; tests game flag 228; plays a sound |
| block 201 (x 9, y 6) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 203 (x 11, y 6) | wall clicked | no game action (only stack and screen bookkeeping) |
| block 207 (x 15, y 6) | party steps in, party arrives (second path), item put down | moves objects from block 207 to block 206; plays a sound |
| block 236 (x 12, y 7) | wall clicked | operates the door at block 205; a character speaks; delete hand item; checks a wall of block 205; plays a sound |
| block 238 (x 14, y 7) | party steps in, party arrives (second path), item put down | moves objects from block 238 to block 332; plays a sound |
| block 259 (x 3, y 8) | party steps in, party arrives (second path), item put down | moves objects from block 259 to block 262; checks a wall of block 259; plays a sound |
| block 260 (x 4, y 8) | wall clicked | operates the door at block 259; sets the west wall of block 259 to type 0; sets the west wall of block 259 to type 44; checks a wall of block 259 |
| block 261 (x 5, y 8) | wall clicked | sets/clears game flag 219; tests game flag 219 |
| block 263 (x 7, y 8) | party arrives (second path) | sets the north wall of block 0 to type ?; make item; play environmental sfx; launches a projectile; tests game flag 219; checks a wall of block 0 |
| block 264 (x 8, y 8) | party arrives (second path) | sets the north wall of block 0 to type ?; make item; play environmental sfx; launches a projectile; tests game flag 219; checks a wall of block 0 |
| block 266 (x 10, y 8) | wall clicked | a character speaks |
| block 293 (x 5, y 9) | party steps in, party arrives (second path), item put down | moves objects from block 293 to block 329 |
| block 295 (x 7, y 9) | wall clicked | sets the west wall of block 295 to type 0; plays a sound |
| block 358 (x 6, y 11) | wall clicked | operates the door at block 359; a character speaks; delete hand item; sets game flag 220; tests game flag 220; plays a sound; tests game flag 221 |
| block 360 (x 8, y 11) | wall clicked | operates the door at block 359; a character speaks; delete hand item; sets game flag 221; tests game flag 221; plays a sound; tests game flag 220; tests game flag 231 |
| block 418 (x 2, y 13) | wall clicked | a character speaks |
| block 419 (x 3, y 13) | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 0 to type 1; sets the west wall of block 0 to type 0; character surprise feedback; move party; checks a wall of block 0 |
| block 422 (x 6, y 13) | party arrives (second path) | sets game flag 223; tests game flag 223 |
| block 517 (x 5, y 16) | wall clicked | places item 264 (Vaelan's Cube) on block 611; a character joins the party; gives item 200 (Paulson's Key); sets game flag 230; a character speaks; sets game flag 315; sets game flag 231; tests game flag 230 … |
| block 547 (x 3, y 17) | party arrives (second path), bits 0x10 (no engine caller found) | sets the north wall of block 579 to type 42; starts a dialogue; a character speaks; sets game flag 551; checks a wall of block 579; tests game flag 551 |
| block 549 (x 5, y 17) | party steps in, bits 0x4000 (no engine caller found) | a character speaks; tests game flag 230; plays a sound; tests game flag 231 |
| block 579 (x 3, y 18) | wall clicked | sets the west wall of block 579 to type 0; plays a sound |
| `0x400` level loaded | — | sets the west wall of block 0 to type 0; starts script timer 0 |
| `0x401` script timer 0 | — | make item; play environmental sfx; launches a projectile; tests game flag 223 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 262 | Bezel Cup | 16 | 611 |
| INI entry 1 (runs when the level loads) | 176 | Mine key 4 | 16 | 611 |
| INI entry 1 (runs when the level loads) | 33 | Axe "Vixen" | 16 | 611 |
| INI entry 1 (runs when the level loads) | 149 | Kite shield | 16 | 611 |
| INI entry 1 (runs when the level loads) | 130 | Dwarvish boots | 16 | 611 |
| INI entry 1 (runs when the level loads) | 140 | Great helm | 16 | 611 |
| INI entry 1 (runs when the level loads) | 134 | Chain mail | 16 | 611 |
| block 517 (x 5, y 16) | 264 | Vaelan's Cube | 16 | 611 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 72 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 110 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 226 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 271 | 2 | 1 | 3 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 5, y 16 | 3 | x 5, y 16 | 0x41ee | HIDEOUT |
| x 1, y 2 | 4 | x 1, y 2 | 0x41ef | ORIN'S GHOST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL16.<lang>`: 15 ids: 1, 2, 4, 7, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 23.
- Global text `LANDS.<lang>`: 1 ids: 0x4065.

Read any of them with `tools/decode_dialogue.py LEVEL16.ENG --index N`.
