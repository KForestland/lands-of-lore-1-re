# Level 2

Made by `tools/level_report.py` from `LEVEL2.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 1 = FOREST1 (decorations `FOREST1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: FOREST1 with palette ALTPAL2.PAL (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 556 | — | — |  | 0x80 | 63 |
| 1 | 1727 | 1 | 8 |  | 0x07 | 255 |
| 2 | 1726 | 2 | 9 |  | 0x07 | 255 |
| 26 | 8 | — | — |  | 0x84 | 63 |
| 46 | 3 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 50 | 2 | 2 | 26 | 1 clickable wall | 0x07 | 255 |
| 51 | 2 | 1 | 27 | 1 clickable wall | 0x07 | 255 |
| 52 | 1 | 2 | 28 | 1 clickable wall | 0x07 | 255 |
| 53 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 54 | 3 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 55 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 56 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 57 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 58 | 4 | — | 3 |  | 0x06 | 63 |
| 59 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 60 | 4 | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |
| 61 | 4 | — | 6 |  | 0x06 | 63 |
| 62 | 3 | 1 | 25 | 1 clickable wall | 0x07 | 255 |
| 63 | 4 | 1 | 7 |  | 0x84 | 63 |
| 64 | 3 | 1 | 14 | 1 clickable wall | 0x07 | 255 |
| 65 | 2 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 66 | 4 | 1 | 23 | 1 clickable wall | 0x07 | 63 |
| 67 | 4 | — | 3 |  | 0x06 | 63 |
| 68 | 16 | — | 24 | 1 clickable wall | 0x80 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 13 (x 13, y 0) | north | 66 | clickable wall |
| 13 (x 13, y 0) | east | 66 | clickable wall |
| 13 (x 13, y 0) | south | 66 | clickable wall |
| 13 (x 13, y 0) | west | 66 | clickable wall |
| 70 (x 6, y 2) | north | 68 | clickable wall |
| 70 (x 6, y 2) | east | 68 | clickable wall |
| 70 (x 6, y 2) | south | 68 | clickable wall |
| 70 (x 6, y 2) | west | 68 | clickable wall |
| 71 (x 7, y 2) | south | 62 | clickable wall |
| 76 (x 12, y 2) | east | 51 | clickable wall |
| 104 (x 8, y 3) | west | 64 | clickable wall |
| 132 (x 4, y 4) | south | 65 | clickable wall |
| 176 (x 16, y 5) | west | 51 | clickable wall |
| 193 (x 1, y 6) | east | 52 | clickable wall |
| 239 (x 15, y 7) | west | 50 | clickable wall |
| 261 (x 5, y 8) | north | 68 | clickable wall |
| 261 (x 5, y 8) | east | 68 | clickable wall |
| 261 (x 5, y 8) | south | 68 | clickable wall |
| 261 (x 5, y 8) | west | 68 | clickable wall |
| 270 (x 14, y 8) | north | 64 | clickable wall |
| 300 (x 12, y 9) | north | 68 | clickable wall |
| 300 (x 12, y 9) | east | 68 | clickable wall |
| 300 (x 12, y 9) | south | 68 | clickable wall |
| 300 (x 12, y 9) | west | 68 | clickable wall |
| 513 (x 1, y 16) | south | 62 | clickable wall |
| 591 (x 15, y 18) | north | 68 | clickable wall |
| 591 (x 15, y 18) | east | 68 | clickable wall |
| 591 (x 15, y 18) | south | 68 | clickable wall |
| 591 (x 15, y 18) | west | 68 | clickable wall |
| 611 (x 3, y 19) | west | 64 | clickable wall |
| 645 (x 5, y 20) | east | 50 | clickable wall |
| 683 (x 11, y 21) | north | 65 | clickable wall |
| 801 (x 1, y 25) | east | 62 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL2.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles FOREST1; loads monster sprites BOAR.SHP into slot 0; loads monster sprites ORC.SHP into slot 1; defines monster type 3; loads monster sprites THUG.SHP into slot 1; defines monster type 1; defines monster type 4; defines monster type 2 … |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 228; places a monster (slot 1) on block 165; places a monster (slot 1) on block 97; places a monster (slot 2) on block 69; places item 121 (Stick) on block 69; places item 99 (Rock) on block 172; places item 99 (Rock) on block 228; places item 43 (Weathered dagger) on block 136 … |

### LEVEL2.INF

| Entry | Events | What it does |
|---|---|---|
| block 13 (x 13, y 0) | party steps in, party arrives (second path), wall clicked, item put down | moves the party to level 6, block 449; moves objects from block 13 to block 449; set global var |
| block 45 (x 13, y 1) | party arrives (second path), bits 0x10 (no engine caller found) | sets the south wall of block 13 to type 63; starts a dialogue; a character speaks; sets game flag 136; tests game flag 67; tests game flag 41; tests game flag 136; plays a sound |
| block 70 (x 6, y 2) | wall clicked | a character speaks |
| block 71 (x 7, y 2) | wall clicked | a character speaks; tests game flag 191 |
| block 74 (x 10, y 2) | party steps in, wall clicked | a character speaks; shows a message; set global var; tests game flag 41; tests game flag 67 |
| block 76 (x 12, y 2) | wall clicked | a character speaks |
| block 77 (x 13, y 2) | item taken | no game action (only stack and screen bookkeeping) |
| block 96 (x 0, y 3) | party steps in, party arrives (second path), wall clicked, item put down | moves the party to level 5, block 260; moves objects from block 96 to block 260; shows a message; set global var |
| block 98 (x 2, y 3) | party steps in | shows a message; tests game flag 35; set global var |
| block 99 (x 3, y 3) | party steps in, bits 0x4000 (no engine caller found) | moves the party to level 5, block 260; places a monster (slot 1) on block 97; a character speaks; starts a dialogue; sets game flag 35; sets game flag 38; suspend monster; changes a monster … |
| block 104 (x 8, y 3) | wall clicked | a character speaks |
| block 106 (x 10, y 3) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | a character speaks; set global var; tests game flag 67; tests game flag 41 |
| block 109 (x 13, y 3) | item taken | no game action (only stack and screen bookkeeping) |
| block 132 (x 4, y 4) | wall clicked | a character speaks |
| block 136 (x 8, y 4) | item taken | clears game flag 187; tests game flag 187 |
| block 138 (x 10, y 4) | party arrives (second path) | starts a dialogue; a character speaks; sets game flag 134; tests game flag 67; tests game flag 41; tests game flag 134 |
| block 141 (x 13, y 4) | party arrives (second path) | starts cut-scene TIM1.TIM; sets game flag 14; sets game flag 35; sets game flag 38; suspend monster; sets game flag 70; starts a dialogue; a character speaks … |
| block 166 (x 6, y 5) | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; changes a monster; starts a dialogue; tests game flag 14 |
| block 170 (x 10, y 5) | party arrives (second path) | starts a dialogue; a character speaks; sets game flag 135; tests game flag 67; tests game flag 41; tests game flag 135 |
| block 176 (x 16, y 5) | wall clicked | a character speaks |
| block 193 (x 1, y 6) | wall clicked | a character speaks |
| block 227 (x 3, y 7) | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; changes a monster; starts a dialogue; tests game flag 14 |
| block 232 (x 8, y 7) | party arrives (second path), bits 0x10 (no engine caller found) | starts cut-scene SCOTIA1.TIM; sets game flag 15; tests game flag 15; tests game flag 67 |
| block 239 (x 15, y 7) | wall clicked | a character speaks; tests game flag 190 |
| block 260 (x 4, y 8) | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; changes a monster; starts a dialogue; tests game flag 14 |
| block 261 (x 5, y 8) | wall clicked | gives 3 crown(s); a character speaks; clears game flag 188; tests game flag 188 |
| block 264 (x 8, y 8) | party arrives (second path) | shows a message; tests game flag 15; set global var |
| block 268 (x 12, y 8) | party arrives (second path) | starts cut-scene VICTOR7.TIM; starts cut-scene VICTOR6.TIM; starts cut-scene VICTOR5.TIM; places item 81 (Long sword) on block 301; gives item 81 (Long sword); places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713; starts a dialogue … |
| block 270 (x 14, y 8) | wall clicked | a character speaks |
| block 300 (x 12, y 9) | party steps in, party arrives (second path), party leaves, wall clicked, bits 0x4000 (no engine caller found) | starts cut-scene VICTOR6.TIM; starts cut-scene VICTOR7.TIM; starts cut-scene VICTOR5.TIM; places item 81 (Long sword) on block 301; gives item 81 (Long sword); places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713; starts a dialogue … |
| block 301 (x 13, y 9) | party steps in, wall clicked | starts cut-scene VICTOR5.TIM; places item 81 (Long sword) on block 301; gives item 81 (Long sword); places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713; starts cut-scene VICTOR7.TIM; starts cut-scene VICTOR6.TIM; moves objects from block 301 to block 713 … |
| block 328 (x 8, y 10) | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | set global var; tests game flag 67 |
| block 360 (x 8, y 11) | party steps in, wall clicked | starts cut-scene LYNN1.TIM; starts cut-scene LYNN2.TIM; starts cut-scene LYNN3.TIM; a character speaks; shows a message; sets game flag 24; tests game flag 67; set global var … |
| block 392 (x 8, y 12) | wall clicked | starts cut-scene BOAT.TIM; moves the party to level 3, block 526; sets game flag 25; delete hand item; a character speaks; starts a dialogue; tests game flag 41; tests game flag 67 … |
| `0x400` level loaded | — | places a monster (slot 3) on block 109; suspend monster; make item; give item to monster; sets game flag 44; starts script timer 0; tests game flag 67; tests game flag 44 |
| `0x401` script timer 0 | — | places a monster (slot 2) on block 136 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 121 | Stick | 2 | 69 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 2 | 172 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 2 | 228 |
| INI entry 1 (runs when the level loads) | 43 | Weathered dagger | 2 | 136 |
| INI entry 1 (runs when the level loads) | 43 | Weathered dagger | 2 | 175 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 2 | 175 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 2 | 69 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 2 | 194 |
| INI entry 1 (runs when the level loads) | 267 | Swarm | 2 | 175 |
| block 268 (x 12, y 8) | 81 | Long sword | 2 | 301 |
| block 268 (x 12, y 8) | 241 | Riddle Scroll | 2 | 301 |
| block 300 (x 12, y 9) | 81 | Long sword | 2 | 301 |
| block 300 (x 12, y 9) | 241 | Riddle Scroll | 2 | 301 |
| block 301 (x 13, y 9) | 81 | Long sword | 2 | 301 |
| block 301 (x 13, y 9) | 241 | Riddle Scroll | 2 | 301 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 228 | 0 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 165 | 1 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 97 | 1 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 97 | 1 | 1 | 2 |
| INI entry 1 (runs when the level loads) | 69 | 1 | 2 | 3 |
| block 99 (x 3, y 3) | 97 | 1 | 1 | 7 |
| `0x400` level loaded | 109 | 0 | 3 | 3 |
| `0x400` level loaded | 109 | 0 | 3 | 3 |
| `0x400` level loaded | 109 | 0 | 3 | 3 |
| `0x400` level loaded | 109 | 0 | 3 | 3 |
| `0x401` script timer 0 | 136 | 2 | 2 | 7 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 10, y 2 | 4 | x 10, y 3 | 0x41d5 | GLADSTONE KEEP |
| x 0, y 3 | 8 | x 1, y 3 | 0x41d6 | THUG'S CAVE |
| x 8, y 11 | 1 | x 8, y 10 | 0x41d7 | MARINA |
| x 13, y 0 | 3 | x 13, y 0 | 0x41d8 | DRARACLE'S CAVE |
| x 13, y 9 | 5 | x 12, y 9 | 0x41d9 | LAKE DREAD |

## Text shown by the scripts (ids only)

- Level text file `LEVEL02.<lang>`: 43 ids: 0, 13, 18, 20, 21, 22, 23, 24, 25, 26, 28, 29, 35, 36, 38, 40, 41, 44, 49, 50, 53, 54, 55, 56, 57, 59, 70, 71, 72, 73, 74, 75, 83, 85, 87, 88, 89, 91, 92, 94, 95, 97, 101.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL02.ENG --index N`.
