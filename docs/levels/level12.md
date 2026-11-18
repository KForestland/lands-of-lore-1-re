# Level 12

Made by `tools/level_report.py` from `LEVEL12.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 5 = URBISH (decorations `URBISH.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: URBISH (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 518 | — | — |  | 0x80 | 63 |
| 1 | 512 | 1 | — |  | 0x07 | 255 |
| 2 | 512 | 2 | — |  | 0x07 | 255 |
| 3 | 32 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 8 | 5 | — |  | 0x04 | 26 |
| 27 | 4 | 2 | 57 | 1 clickable wall | 0x07 | 255 |
| 28 | 3 | 2 | 25 | 1 clickable wall | 0x07 | 255 |
| 29 | 6 | 6 | 26 | 1 clickable wall | 0x07 | 255 |
| 30 | 4 | 2 | 27 | 1 clickable wall | 0x07 | 255 |
| 31 | 3 | 1 | 28 | 1 clickable wall | 0x07 | 255 |
| 32 | 1 | 2 | 29 | 6 niche | 0x87 | 14 |
| 33 | 1 | 1 | 30 | 1 clickable wall | 0x07 | 255 |
| 34 | 2 | 2 | 31 | 1 clickable wall | 0x07 | 255 |
| 36 | 8 | 1 | 34 | 1 clickable wall | 0x07 | 255 |
| 37 | 4 | 6 | 43 | 1 clickable wall | 0x07 | 255 |
| 38 | 1 | 6 | 46 | 1 clickable wall | 0x07 | 255 |
| 39 | 1 | 2 | 44 | 1 clickable wall | 0x07 | 255 |
| 40 | 1 | 2 | 47 | 1 clickable wall | 0x07 | 255 |
| 41 | 34 | 2 | 33 |  | 0x07 | 255 |
| 42 | 1 | 1 | 3 | 2 lever (to on) | 0x07 | 207 |
| 44 | 2 | 1 | 49 | 1 clickable wall | 0x07 | 255 |
| 45 | 3 | 2 | 50 | 1 clickable wall | 0x07 | 255 |
| 46 | 11 | — | 60 | 1 clickable wall | 0x07 | 255 |
| 47 | 1 | 2 | 11 | 1 clickable wall | 0x07 | 207 |
| 50 | 9 | 2 | 20 |  | 0x07 | 255 |
| 52 | 8 | — | 59 | 1 clickable wall | 0x07 | 255 |
| 53 | 770 | 1 | — |  | 0x07 | 255 |
| 54 | 786 | 2 | — |  | 0x07 | 255 |
| 55 | 802 | 6 | — |  | 0x07 | 255 |
| 56 | 1 | 1 | 38 | 1 clickable wall | 0x07 | 210 |
| 60 | 1 | 1 | 35 | 1 clickable wall | 0x07 | 255 |
| 61 | 3 | 1 | 36 | 1 clickable wall | 0x07 | 255 |
| 62 | 3 | — | — | 1 clickable wall | 0x06 | 255 |
| 63 | 8 | 3 | 42 |  | 0x06 | 63 |
| 64 | 4 | — | 37 | 1 clickable wall | 0x07 | 255 |
| 65 | 3 | 1 | 61 | 1 clickable wall | 0x07 | 255 |
| 67 | 1 | 1 | 62 | 1 clickable wall | 0x07 | 255 |
| 68 | 2 | 1 | 64 | 1 clickable wall | 0x07 | 255 |
| 73 | 1 | 6 | 12 | 1 clickable wall | 0x07 | 255 |
| 76 | 3 | 2 | 15 | 1 clickable wall | 0x07 | 255 |
| 77 | 4 | 1 | 16 | 1 clickable wall | 0x07 | 255 |
| 78 | 3 | 1 | 23 | 1 clickable wall | 0x07 | 255 |
| 79 | 5 | 6 | 24 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 13 (x 13, y 0) | east | 31 | clickable wall |
| 36 (x 4, y 1) | south | 40 | clickable wall |
| 37 (x 5, y 1) | south | 33 | clickable wall |
| 38 (x 6, y 1) | south | 37 | clickable wall |
| 40 (x 8, y 1) | south | 45 | clickable wall |
| 41 (x 9, y 1) | south | 27 | clickable wall |
| 45 (x 13, y 1) | south | 79 | clickable wall |
| 49 (x 17, y 1) | south | 73 | clickable wall |
| 51 (x 19, y 1) | south | 38 | clickable wall |
| 52 (x 20, y 1) | south | 27 | clickable wall |
| 66 (x 2, y 2) | east | 65 | clickable wall |
| 74 (x 10, y 2) | west | 42 | lever (to on) |
| 78 (x 14, y 2) | east | 3 | door / door switch |
| 78 (x 14, y 2) | west | 3 | door / door switch |
| 82 (x 18, y 2) | west | 27 | clickable wall |
| 85 (x 21, y 2) | east | 37 | clickable wall |
| 87 (x 23, y 2) | west | 65 | clickable wall |
| 106 (x 10, y 3) | west | 30 | clickable wall |
| 108 (x 12, y 3) | south | 34 | clickable wall |
| 111 (x 15, y 3) | north | 65 | clickable wall |
| 112 (x 16, y 3) | north | 64 | clickable wall |
| 112 (x 16, y 3) | east | 64 | clickable wall |
| 112 (x 16, y 3) | south | 64 | clickable wall |
| 112 (x 16, y 3) | west | 64 | clickable wall |
| 113 (x 17, y 3) | north | 79 | clickable wall |
| 117 (x 21, y 3) | west | 39 | clickable wall |
| 131 (x 3, y 4) | north | 37 | clickable wall |
| 132 (x 4, y 4) | north | 3 | door / door switch |
| 132 (x 4, y 4) | south | 3 | door / door switch |
| 134 (x 6, y 4) | south | 29 | clickable wall |
| 136 (x 8, y 4) | north | 3 | door / door switch |
| 136 (x 8, y 4) | south | 3 | door / door switch |
| 138 (x 10, y 4) | east | 45 | clickable wall |
| 144 (x 16, y 4) | north | 45 | clickable wall |
| 147 (x 19, y 4) | north | 3 | door / door switch |
| 147 (x 19, y 4) | south | 3 | door / door switch |
| 150 (x 22, y 4) | north | 3 | door / door switch |
| 150 (x 22, y 4) | south | 3 | door / door switch |
| 158 (x 30, y 4) | west | 76 | clickable wall |
| 162 (x 2, y 5) | east | 30 | clickable wall |
| 171 (x 11, y 5) | north | 31 | clickable wall |
| 172 (x 12, y 5) | south | 78 | clickable wall |
| 173 (x 13, y 5) | north | 3 | door / door switch |
| 173 (x 13, y 5) | south | 3 | door / door switch |
| 176 (x 16, y 5) | east | 30 | clickable wall |
| 188 (x 28, y 5) | north | 52 | clickable wall |
| 188 (x 28, y 5) | east | 52 | clickable wall |
| 188 (x 28, y 5) | south | 52 | clickable wall |
| 188 (x 28, y 5) | west | 52 | clickable wall |
| 195 (x 3, y 6) | south | 32 | niche |
| 196 (x 4, y 6) | north | 79 | clickable wall |
| 203 (x 11, y 6) | south | 78 | clickable wall |
| 207 (x 15, y 6) | north | 3 | door / door switch |
| 207 (x 15, y 6) | south | 3 | door / door switch |
| 208 (x 16, y 6) | south | 61 | clickable wall |
| 219 (x 27, y 6) | east | 77 | clickable wall |
| 226 (x 2, y 7) | east | 37 | clickable wall |
| 229 (x 5, y 7) | west | 67 | clickable wall |
| 230 (x 6, y 7) | east | 79 | clickable wall |
| 243 (x 19, y 7) | east | 29 | clickable wall |
| 243 (x 19, y 7) | west | 60 | clickable wall |
| 245 (x 21, y 7) | east | 3 | door / door switch |
| 245 (x 21, y 7) | west | 3 | door / door switch |
| 250 (x 26, y 7) | east | 3 | door / door switch |
| 250 (x 26, y 7) | west | 3 | door / door switch |
| 258 (x 2, y 8) | east | 27 | clickable wall |
| 261 (x 5, y 8) | east | 3 | door / door switch |
| 261 (x 5, y 8) | west | 3 | door / door switch |
| 265 (x 9, y 8) | north | 29 | clickable wall |
| 266 (x 10, y 8) | east | 77 | clickable wall |
| 286 (x 30, y 8) | west | 77 | clickable wall |
| 290 (x 2, y 9) | east | 44 | clickable wall |
| 296 (x 8, y 9) | north | 47 | clickable wall |
| 300 (x 12, y 9) | north | 3 | door / door switch |
| 300 (x 12, y 9) | south | 3 | door / door switch |
| 302 (x 14, y 9) | north | 79 | clickable wall |
| 303 (x 15, y 9) | north | 3 | door / door switch |
| 303 (x 15, y 9) | south | 3 | door / door switch |
| 305 (x 17, y 9) | north | 77 | clickable wall |
| 306 (x 18, y 9) | south | 56 | clickable wall |
| 309 (x 21, y 9) | east | 3 | door / door switch |
| 309 (x 21, y 9) | west | 3 | door / door switch |
| 311 (x 23, y 9) | west | 28 | clickable wall |
| 316 (x 28, y 9) | east | 29 | clickable wall |
| 324 (x 4, y 10) | north | 3 | door / door switch |
| 324 (x 4, y 10) | south | 3 | door / door switch |
| 328 (x 8, y 10) | north | 62 | clickable wall |
| 328 (x 8, y 10) | south | 62 | clickable wall |
| 328 (x 8, y 10) | west | 62 | clickable wall |
| 329 (x 9, y 10) | north | 46 | clickable wall |
| 329 (x 9, y 10) | east | 46 | clickable wall |
| 329 (x 9, y 10) | south | 46 | clickable wall |
| 331 (x 11, y 10) | north | 46 | clickable wall |
| 331 (x 11, y 10) | east | 46 | clickable wall |
| 331 (x 11, y 10) | south | 46 | clickable wall |
| 331 (x 11, y 10) | west | 46 | clickable wall |
| 333 (x 13, y 10) | east | 61 | clickable wall |
| 337 (x 17, y 10) | west | 61 | clickable wall |
| 340 (x 20, y 10) | north | 3 | door / door switch |
| 340 (x 20, y 10) | south | 3 | door / door switch |
| 343 (x 23, y 10) | west | 44 | clickable wall |
| 348 (x 28, y 10) | east | 76 | clickable wall |
| 350 (x 30, y 10) | north | 52 | clickable wall |
| 350 (x 30, y 10) | east | 52 | clickable wall |
| 350 (x 30, y 10) | south | 52 | clickable wall |
| 350 (x 30, y 10) | west | 52 | clickable wall |
| 355 (x 3, y 11) | east | 28 | clickable wall |
| 358 (x 6, y 11) | west | 68 | clickable wall |
| 361 (x 9, y 11) | east | 28 | clickable wall |
| 367 (x 15, y 11) | north | 46 | clickable wall |
| 367 (x 15, y 11) | east | 46 | clickable wall |
| 367 (x 15, y 11) | south | 46 | clickable wall |
| 367 (x 15, y 11) | west | 46 | clickable wall |
| 369 (x 17, y 11) | east | 31 | clickable wall |
| 371 (x 19, y 11) | east | 3 | door / door switch |
| 371 (x 19, y 11) | west | 3 | door / door switch |
| 375 (x 23, y 11) | west | 68 | clickable wall |
| 380 (x 28, y 11) | south | 30 | clickable wall |
| 389 (x 5, y 12) | north | 34 | clickable wall |
| 395 (x 11, y 12) | north | 36 | clickable wall |
| 395 (x 11, y 12) | east | 36 | clickable wall |
| 395 (x 11, y 12) | south | 36 | clickable wall |
| 395 (x 11, y 12) | west | 36 | clickable wall |
| 396 (x 12, y 12) | north | 78 | clickable wall |
| 398 (x 14, y 12) | north | 36 | clickable wall |
| 398 (x 14, y 12) | east | 36 | clickable wall |
| 398 (x 14, y 12) | south | 36 | clickable wall |
| 398 (x 14, y 12) | west | 36 | clickable wall |
| 404 (x 20, y 12) | north | 76 | clickable wall |
| 406 (x 22, y 12) | north | 29 | clickable wall |
| 445 (x 29, y 13) | north | 29 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL12.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles URBISH; loads monster sprites TREZ.SHP into slot 0; loads monster sprites LARKHON.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 2) on block 249; places a monster (slot 1) on block 357; places a monster (slot 1) on block 356; places a monster (slot 1) on block 86; places item 243 (Coin Purse) on block 368; places item 145 (Helm) on block 105; places item 245 (Lockpicks) on block 140; places item 60 (Great maul) on block 195 … |

### LEVEL12.INF

| Entry | Events | What it does |
|---|---|---|
| block 35 (x 3, y 1) | wall clicked | gives item -1 (?); sets game flag 566; checks a wall of block 35; tests game flag 566 |
| block 36 (x 4, y 1) | wall clicked | gives item 248 (Oil Flask); sets game flag 571; checks a wall of block 36; tests game flag 571 |
| block 37 (x 5, y 1) | wall clicked | a character speaks |
| block 38 (x 6, y 1) | wall clicked | gives item -1 (?); sets game flag 572; checks a wall of block 38; tests game flag 572 |
| block 41 (x 9, y 1) | wall clicked | a character speaks |
| block 49 (x 17, y 1) | wall clicked | a character speaks |
| block 51 (x 19, y 1) | wall clicked | gives item ? (?); sets game flag 569; sets game flag 553; tests game flag 553; checks a wall of block 51; tests game flag 569 |
| block 52 (x 20, y 1) | wall clicked | a character speaks |
| block 66 (x 2, y 2) | wall clicked | gives item 248 (Oil Flask); gives item 216 (Salve); sets game flag 539; sets game flag 556; checks a wall of block 66; tests game flag 539; tests game flag 556 |
| block 74 (x 10, y 2) | wall clicked | sets the west wall of block 74 to type 0; plays a sound |
| block 80 (x 16, y 2) | party steps in, bits 0x4000 (no engine caller found) | sets the north wall of block 993 to type 1; sets the north wall of block 993 to type 0; sets game flag 580; a character speaks; sets game flag 205; sets game flag 148; set global var; tests game flag 148 … |
| block 82 (x 18, y 2) | wall clicked | a character speaks |
| block 85 (x 21, y 2) | wall clicked | gives item 248 (Oil Flask); sets game flag 565; checks a wall of block 85; tests game flag 565 |
| block 87 (x 23, y 2) | wall clicked | gives item 267 (Swarm); gives item 248 (Oil Flask); sets game flag 554; sets game flag 562; checks a wall of block 87; tests game flag 554; tests game flag 562 |
| block 92 (x 28, y 2) | party steps in, party arrives (second path), item put down | moves objects from block 92 to block 760 |
| block 106 (x 10, y 3) | wall clicked | a character speaks |
| block 108 (x 12, y 3) | wall clicked | a character speaks |
| block 111 (x 15, y 3) | wall clicked | gives item 248 (Oil Flask); gives item 243 (Coin Purse); sets game flag 542; sets game flag 559; checks a wall of block 111; tests game flag 542; tests game flag 559 |
| block 112 (x 16, y 3) | wall clicked | sets the north wall of block 993 to type 0; gives item 28 (Pick); gives item 140 (Great helm); sets game flag 148; sets game flag 149; a character speaks; sets game flag 150; set global var … |
| block 117 (x 21, y 3) | wall clicked | gives item 248 (Oil Flask); sets game flag 564; checks a wall of block 117; tests game flag 564 |
| block 131 (x 3, y 4) | wall clicked | gives item 236 (Fireball scroll); sets game flag 553; checks a wall of block 131; tests game flag 553 |
| block 138 (x 10, y 4) | wall clicked | a character speaks |
| block 162 (x 2, y 5) | wall clicked | a character speaks |
| block 171 (x 11, y 5) | wall clicked | a character speaks |
| block 175 (x 15, y 5) | party steps in, party arrives (second path), item put down | moves objects from block 175 to block 111 |
| block 176 (x 16, y 5) | wall clicked | a character speaks |
| block 188 (x 28, y 5) | wall clicked | gives item 267 (Swarm); sets game flag 567; tests game flag 567 |
| block 208 (x 16, y 6) | wall clicked | a character speaks |
| block 226 (x 2, y 7) | wall clicked | gives item 216 (Salve); sets game flag 570; checks a wall of block 226; tests game flag 570 |
| block 229 (x 5, y 7) | wall clicked | gives item 243 (Coin Purse); gives item 248 (Oil Flask); sets game flag 541; sets game flag 558; checks a wall of block 229; tests game flag 541; tests game flag 558 |
| block 243 (x 19, y 7) | wall clicked | a character speaks |
| block 247 (x 23, y 7) | party steps in, party arrives (second path), item put down | changes a monster; moves objects from block 247 to block 249 |
| block 248 (x 24, y 7) | party steps in, party arrives (second path), item put down | moves objects from block 248 to block 246 |
| block 250 (x 26, y 7) | wall clicked | sets game flag 344; starts script timer 1; tests game flag 344 |
| block 258 (x 2, y 8) | wall clicked | a character speaks |
| block 290 (x 2, y 9) | wall clicked | a character speaks |
| block 296 (x 8, y 9) | wall clicked | a character speaks |
| block 306 (x 18, y 9) | wall clicked | gives item 173 (Silver key); sets the west wall of block 992 to type 0 |
| block 327 (x 7, y 10) | party steps in, party leaves, bits 0x4000 (no engine caller found) | sets the south wall of block 993 to type 0; sets the south wall of block 993 to type 1; shows a message; set global var; checks a wall of block 993; tests game flag 207; tests game flag 208; tests game flag 209 |
| block 328 (x 8, y 10) | wall clicked | deals damage; gives item 253 (Gear); a character speaks; delete hand item; sets game flag 211; sets game flag 210; tests game flag 209; tests game flag 208 … |
| block 329 (x 9, y 10) | wall clicked | a character speaks |
| block 331 (x 11, y 10) | wall clicked | a character speaks |
| block 333 (x 13, y 10) | wall clicked | a character speaks |
| block 337 (x 17, y 10) | wall clicked | a character speaks |
| block 338 (x 18, y 10) | bits 0x400 (no engine caller found) | gives item 173 (Silver key); sets the west wall of block 992 to type 0 |
| block 340 (x 20, y 10) | wall clicked | block door; checks a wall of block 371 |
| block 343 (x 23, y 10) | wall clicked | a character speaks |
| block 350 (x 30, y 10) | wall clicked | gives item 248 (Oil Flask); sets game flag 568; tests game flag 568 |
| block 358 (x 6, y 11) | wall clicked | gives item 216 (Salve); gives item 248 (Oil Flask); sets game flag 555; sets game flag 563; checks a wall of block 358; tests game flag 555; tests game flag 563 |
| block 367 (x 15, y 11) | wall clicked | a character speaks |
| block 369 (x 17, y 11) | wall clicked | a character speaks |
| block 371 (x 19, y 11) | wall clicked | block door; checks a wall of block 340 |
| block 375 (x 23, y 11) | wall clicked | gives item ? (?); gives item 216 (Salve); sets game flag 540; sets game flag 553; sets game flag 557; tests game flag 553; checks a wall of block 375; tests game flag 540 … |
| block 389 (x 5, y 12) | wall clicked | a character speaks |
| block 395 (x 11, y 12) | wall clicked | a character speaks |
| block 398 (x 14, y 12) | wall clicked | a character speaks |
| block 411 (x 27, y 12) | party steps in, party arrives (second path), item put down | moves objects from block 411 to block 702 |
| block 412 (x 28, y 12) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; sets game flag 146; tests game flag 146 |
| `0x400` level loaded | — | sets the north wall of block 993 to type 0; sets the south wall of block 993 to type 0; starts script timer 0; starts script timer 2 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 163 |
| `0x402` script timer 1 | — | a character speaks; starts script timer 1 |
| `0x403` script timer 2 | — | toggles the north wall of block 304 between types 50 and 51; toggles the south wall of block 145 between types 50 and 51; toggles the east wall of block 197 between types 50 and 51; toggles the north wall of block 266 between types 50 and 51; toggles the west wall of block 318 between types 50 and 51; toggles the north wall of block 253 between types 50 and 51; toggles the east wall of block 123 between types 50 and 51; toggles the north wall of block 391 between types 50 and 51 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 12 | 368 |
| INI entry 1 (runs when the level loads) | 145 | Helm | 12 | 105 |
| INI entry 1 (runs when the level loads) | 245 | Lockpicks | 12 | 140 |
| INI entry 1 (runs when the level loads) | 60 | Great maul | 12 | 195 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 249 | 1 | 2 | 7 |
| INI entry 1 (runs when the level loads) | 357 | 3 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 356 | 0 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 86 | 2 | 1 | 3 |
| `0x401` script timer 0 | 163 | 0 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 26, y 12 | 0 | x 27, y 12 | 0x41de | FOREST |
| x 28, y 1 | 9 | x 28, y 2 | 0x41de | FOREST |
| x 8, y 10 | 4 | x 7, y 10 | 0x41e9 | MACHINE |
| x 16, y 3 | 5 | x 16, y 2 | 0x41ea | CLERK OFFICE |

## Text shown by the scripts (ids only)

- Level text file `LEVEL12.<lang>`: 41 ids: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 28, 32, 36, 45, 46, 47, 48, 49, 50, 51, 60, 62, 63, 64, 65, 66, 67, 68.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL12.ENG --index N`.
