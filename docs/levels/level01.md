# Level 1

Made by `tools/level_report.py` from `LEVEL1.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 0 = KEEP (decorations `KEEP.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: KEEP (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 188 | — | — |  | 0x80 | 63 |
| 1 | 1922 | 1 | — |  | 0x07 | 255 |
| 2 | 1926 | 2 | — |  | 0x07 | 255 |
| 3 | 8 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 53 | 1 | 1 | 7 | 1 clickable wall | 0x07 | 255 |
| 54 | 2 | 1 | 8 | 1 clickable wall | 0x07 | 255 |
| 55 | 2 | 1 | 4 | 1 clickable wall | 0x07 | 255 |
| 57 | 1 | 4 | — | 4 click runs script | 0x07 | 255 |
| 59 | 3 | 6 | — | 4 click runs script | 0x06 | 13 |
| 60 | 2 | 6 | 3 | 4 click runs script | 0x06 | 13 |
| 61 | 3 | 1 | 5 | 1 clickable wall | 0x07 | 255 |
| 62 | 2 | 1 | 6 | 1 clickable wall | 0x07 | 255 |
| 63 | 1 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 64 | 1 | 1 | 10 | 1 clickable wall | 0x07 | 255 |
| 65 | 1 | 1 | 11 | 1 clickable wall | 0x07 | 255 |
| 68 | 4 | — | 12 | 1 clickable wall | 0x07 | 63 |
| 71 | 4 | 5 | 15 | 1 clickable wall | 0x07 | 14 |
| 72 | 12 | 1 | 16 |  | 0x07 | 255 |
| 73 | 1 | 1 | 17 | 1 clickable wall | 0x07 | 207 |
| 74 | 1 | 6 | 19 | 1 clickable wall | 0x06 | 13 |
| 75 | 2 | 1 | 21 | 1 clickable wall | 0x07 | 255 |
| 76 | 2 | 1 | 22 | 1 clickable wall | 0x07 | 255 |
| 77 | 1 | 1 | 23 | 1 clickable wall | 0x07 | 255 |
| 78 | 2 | 1 | 24 | 1 clickable wall | 0x07 | 255 |
| 79 | 2 | 1 | 25 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 201 (x 9, y 6) | south | 79 | clickable wall |
| 202 (x 10, y 6) | south | 65 | clickable wall |
| 237 (x 13, y 7) | south | 78 | clickable wall |
| 238 (x 14, y 7) | south | 54 | clickable wall |
| 264 (x 8, y 8) | east | 76 | clickable wall |
| 273 (x 17, y 8) | west | 74 | clickable wall |
| 298 (x 10, y 9) | north | 3 | door / door switch |
| 298 (x 10, y 9) | south | 3 | door / door switch |
| 300 (x 12, y 9) | south | 63 | clickable wall |
| 302 (x 14, y 9) | north | 54 | clickable wall |
| 327 (x 7, y 10) | south | 79 | clickable wall |
| 328 (x 8, y 10) | south | 71 | clickable wall |
| 329 (x 9, y 10) | east | 64 | clickable wall |
| 331 (x 11, y 10) | east | 3 | door / door switch |
| 331 (x 11, y 10) | west | 3 | door / door switch |
| 334 (x 14, y 10) | west | 75 | clickable wall |
| 358 (x 6, y 11) | east | 71 | clickable wall |
| 364 (x 12, y 11) | north | 3 | door / door switch |
| 364 (x 12, y 11) | south | 3 | door / door switch |
| 367 (x 15, y 11) | south | 61 | clickable wall |
| 390 (x 6, y 12) | east | 78 | clickable wall |
| 393 (x 9, y 12) | west | 71 | clickable wall |
| 394 (x 10, y 12) | north | 73 | clickable wall |
| 395 (x 11, y 12) | south | 61 | clickable wall |
| 397 (x 13, y 12) | east | 55 | clickable wall |
| 397 (x 13, y 12) | south | 55 | clickable wall |
| 400 (x 16, y 12) | west | 59 | click runs script |
| 423 (x 7, y 13) | north | 71 | clickable wall |
| 424 (x 8, y 13) | north | 77 | clickable wall |
| 426 (x 10, y 13) | east | 59 | click runs script |
| 429 (x 13, y 13) | north | 68 | clickable wall |
| 429 (x 13, y 13) | east | 68 | clickable wall |
| 429 (x 13, y 13) | south | 68 | clickable wall |
| 429 (x 13, y 13) | west | 68 | clickable wall |
| 431 (x 15, y 13) | west | 53 | clickable wall |
| 459 (x 11, y 14) | east | 57 | click runs script |
| 464 (x 16, y 14) | west | 59 | click runs script |
| 492 (x 12, y 15) | south | 62 | clickable wall |
| 493 (x 13, y 15) | north | 3 | door / door switch |
| 493 (x 13, y 15) | south | 3 | door / door switch |
| 494 (x 14, y 15) | south | 62 | clickable wall |
| 495 (x 15, y 15) | north | 61 | clickable wall |
| 527 (x 15, y 16) | west | 75 | clickable wall |
| 555 (x 11, y 17) | east | 76 | clickable wall |
| 621 (x 13, y 19) | north | 60 | click runs script |
| 621 (x 13, y 19) | south | 60 | click runs script |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL1.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles KEEP; loads monster sprites GUARD.SHP into slot 0; defines monster type 1; tests game flag 39 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 589; places a monster (slot 1) on block 525; places a monster (slot 1) on block 271; make item; give item to monster; clears game flag 108; sets game flag 108; set global var … |

### LEVEL1.INF

| Entry | Events | What it does |
|---|---|---|
| block 201 (x 9, y 6) | wall clicked | a character speaks; sets game flag 90; clears game flag 90; tests game flag 39; tests game flag 90 |
| block 202 (x 10, y 6) | wall clicked | a character speaks; sets game flag 104; clears game flag 104; tests game flag 39; tests game flag 104 |
| block 237 (x 13, y 7) | wall clicked | a character speaks; sets game flag 92; clears game flag 92; tests game flag 39; tests game flag 92 |
| block 238 (x 14, y 7) | wall clicked | a character speaks; sets game flag 99; clears game flag 99; tests game flag 39; tests game flag 99 |
| block 264 (x 8, y 8) | wall clicked | a character speaks; sets game flag 91; clears game flag 91; tests game flag 39; tests game flag 91 |
| block 269 (x 13, y 8) | party arrives (second path) | clears game flag 23; move monster; tests game flag 23 |
| block 270 (x 14, y 8) | party arrives (second path), bits 0x10 (no engine caller found) | starts cut-scene GUARD1.TIM; starts cut-scene GUARD2.TIM; starts cut-scene GUARD6.TIM; sets game flag 23; move monster; a character speaks; starts a dialogue; tests game flag 23 … |
| block 272 (x 16, y 8) | party arrives (second path) | sets game flag 23; move monster; tests game flag 23 |
| block 273 (x 17, y 8) | party steps in, wall clicked | starts cut-scene KING1.TIM; starts cut-scene CONFRONT.TIM; starts cut-scene TALAMSCA.TIM; a character speaks; shows a message; sets game flag 4; starts a dialogue; set global var … |
| block 274 (x 18, y 8) | wall clicked | starts cut-scene DAWN1.TIM; starts cut-scene WILL1.TIM; a character leaves the party; a character joins the party; starts cut-scene SPELLBKE.TIM; starts cut-scene SPELLBKF.TIM; starts cut-scene SPELLBKG.TIM; starts cut-scene NATE4.TIM … |
| block 300 (x 12, y 9) | wall clicked | a character speaks; sets game flag 101; clears game flag 101; tests game flag 39; tests game flag 101 |
| block 302 (x 14, y 9) | wall clicked | a character speaks; sets game flag 100; clears game flag 100; tests game flag 39; tests game flag 100 |
| block 327 (x 7, y 10) | wall clicked | a character speaks; sets game flag 94; clears game flag 94; tests game flag 39; tests game flag 94 |
| block 328 (x 8, y 10) | wall clicked | starts a dialogue; a character speaks; plays a sound; set global script var |
| block 329 (x 9, y 10) | wall clicked | a character speaks; sets game flag 103; clears game flag 103; tests game flag 39; tests game flag 103 |
| block 334 (x 14, y 10) | wall clicked | a character speaks; sets game flag 93; clears game flag 93; tests game flag 39; tests game flag 93 |
| block 358 (x 6, y 11) | wall clicked | starts a dialogue; a character speaks; plays a sound; set global script var |
| block 367 (x 15, y 11) | wall clicked | a character speaks; tests game flag 39 |
| block 390 (x 6, y 12) | wall clicked | a character speaks; sets game flag 95; clears game flag 95; tests game flag 39; tests game flag 95 |
| block 393 (x 9, y 12) | wall clicked | sets the west wall of block 393 to type 58; starts cut-scene AUTOMAP.TIM; sets game flag 252; a character speaks; starts a dialogue; checks a wall of block 393; set global script var |
| block 394 (x 10, y 12) | wall clicked | a character speaks |
| block 395 (x 11, y 12) | wall clicked | a character speaks; tests game flag 39 |
| block 397 (x 13, y 12) | wall clicked | deals damage; a character speaks; sets game flag 107; tests game flag 107 |
| block 400 (x 16, y 12) | party steps in, wall clicked | starts cut-scene DRVICTOR.TIM; starts cut-scene VICTOR1.TIM; starts cut-scene VICTOR2.TIM; starts cut-scene VICTOR3.TIM; a character speaks; shows a message; sets game flag 12; starts a dialogue … |
| block 401 (x 17, y 12) | wall clicked | gives ? crown(s); takes 125 crown(s); gives item 81 (Long sword); takes 40 crown(s); gives item 90 (Mace); takes 60 crown(s); gives item 93 (Rapier); takes 10 crown(s) … |
| block 423 (x 7, y 13) | wall clicked | starts a dialogue; a character speaks; plays a sound; set global script var |
| block 424 (x 8, y 13) | wall clicked | a character speaks; sets game flag 96; clears game flag 96; tests game flag 39; tests game flag 96 |
| block 425 (x 9, y 13) | wall clicked | a character speaks; sets game flag 11; starts a dialogue; tests game flag 11; set global var; tests game flag 41 |
| block 426 (x 10, y 13) | party steps in, wall clicked | starts cut-scene DRGERIM.TIM; starts cut-scene GERIM1.TIM; starts cut-scene GERIM2.TIM; starts cut-scene GERIM3.TIM; shows a message; a character speaks; move monster; starts a dialogue … |
| block 429 (x 13, y 13) | wall clicked | gives 1 crown(s); a character speaks; sets game flag 109; clears game flag 109; clears game flag 108; clears game flag 88; sets game flag 88; tests game flag 39 … |
| block 431 (x 15, y 13) | wall clicked | a character speaks; sets game flag 105; clears game flag 105; tests game flag 39; tests game flag 105 |
| block 459 (x 11, y 14) | wall clicked | a character speaks; sets game flag 102; clears game flag 102; tests game flag 39; tests game flag 102 |
| block 464 (x 16, y 14) | party steps in, wall clicked | starts cut-scene DRNATHAN.TIM; starts cut-scene NATE1.TIM; starts cut-scene NATE2.TIM; starts cut-scene NATE3.TIM; a character speaks; shows a message; sets game flag 13; starts a dialogue … |
| block 465 (x 17, y 14) | wall clicked | takes 20 crown(s); gives item 216 (Salve); takes 10 crown(s); gives item 218 (Ginseng); takes 5 crown(s); gives item 217 (Aloe); a character speaks; starts a dialogue … |
| block 492 (x 12, y 15) | wall clicked | a character speaks; sets game flag 88; clears game flag 88; tests game flag 39; tests game flag 88 |
| block 494 (x 14, y 15) | wall clicked | a character speaks; sets game flag 89; clears game flag 89; tests game flag 39; tests game flag 89 |
| block 495 (x 15, y 15) | wall clicked | a character speaks; tests game flag 39 |
| block 526 (x 14, y 16) | party arrives (second path) | no game action (only stack and screen bookkeeping) |
| block 527 (x 15, y 16) | wall clicked | a character speaks; sets game flag 98; clears game flag 98; tests game flag 39; tests game flag 98 |
| block 555 (x 11, y 17) | wall clicked | a character speaks; sets game flag 97; clears game flag 97; tests game flag 39; tests game flag 97 |
| block 557 (x 13, y 17) | party arrives (second path), bits 0x10 (no engine caller found) | starts cut-scene GUARD6.TIM; a character speaks; move monster; sets game flag 110; tests game flag 110; tests game flag 11; tests game flag 4 |
| block 621 (x 13, y 19) | party steps in, wall clicked | moves the party to level 2, block 106; a character speaks; shows a message; set global var; plays a sound |
| `0x400` level loaded | — | changes a monster; move monster; starts script timer 0; starts script timer 1; tests game flag 1; set global script var; tests game flag 39; tests game flag 40 … |
| `0x401` script timer 0 | — | toggles the west wall of block 429 between types 68 and 69 |
| `0x402` script timer 1 | — | no game action (only stack and screen bookkeeping) |

## Items placed by the scripts

None by constant script calls.

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 589 | 0 | 1 | 1 |
| INI entry 1 (runs when the level loads) | 525 | 2 | 1 | 1 |
| INI entry 1 (runs when the level loads) | 271 | 3 | 1 | 1 |
| INI entry 1 (runs when the level loads) | 271 | 3 | 1 | 1 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 13, y 13 | 1 | x 13, y 14 | 0x41d0 | FOUNTAIN |
| x 18, y 8 | 4 | x 16, y 8 | 0x41d1 | THRONE ROOM |
| x 9, y 13 | 2 | x 10, y 13 | 0x41d2 | GERON'S OFFICE |
| x 17, y 12 | 8 | x 16, y 12 | 0x41d3 | VICTOR'S ARMS |
| x 17, y 14 | 0 | x 16, y 14 | 0x41d4 | NATHANIEL'S HERBS |
| x 13, y 20 | 7 | x 13, y 18 | 0x41de | FOREST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL01.<lang>`: 106 ids: 0, 1, 16, 17, 18, 24, 25, 26, 27, 28, 29, 30, 31, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86, 89, 90, 91, 92, 93, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 141, 142, 143, 144, 145, 146.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL01.ENG --index N`.
