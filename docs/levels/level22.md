# Level 22

Made by `tools/level_report.py` from `LEVEL22.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 8 = YVEL1 (decorations `YVEL1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: YVEL1 (INI); YVEL2 (INI); YVEL1 (INI); YVEL2 (INF); YVEL1 (INF); YVEL1 (INF); YVEL2 (INF).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1580 | — | — |  | 0x80 | 63 |
| 1 | 797 | 1 | — |  | 0x07 | 255 |
| 2 | 764 | 2 | — |  | 0x07 | 255 |
| 22 | 1 | 3 | — |  | 0x98 | 13 |
| 23 | 3 | 2 | — |  | 0x84 | 25 |
| 24 | 4 | 3 | — |  | 0x84 | 26 |
| 27 | 7 | 1 | 18 |  | 0x07 | 255 |
| 28 | 4 | 2 | 19 |  | 0x07 | 255 |
| 29 | 3 | 2 | 20 |  | 0x07 | 255 |
| 31 | 2 | 2 | 24 | 1 clickable wall | 0x07 | 210 |
| 35 | 1 | 1 | 21 | 2 lever (to on) | 0x07 | 207 |
| 37 | 13 | 1 | 1 | 1 clickable wall | 0x06 | 13 |
| 38 | 3 | 2 | 2 | 1 clickable wall | 0x06 | 13 |
| 39 | 8 | 1 | 3 |  | 0x07 | 255 |
| 40 | 8 | 2 | 4 |  | 0x07 | 255 |
| 41 | 7 | 4 | 5 |  | 0x07 | 255 |
| 42 | 12 | 1 | 14 | 1 clickable wall | 0x07 | 255 |
| 43 | 12 | 2 | 29 | 1 clickable wall | 0x07 | 255 |
| 44 | 1 | 3 | 13 | 1 clickable wall | 0x06 | 13 |
| 47 | 3 | 1 | 12 | 1 clickable wall | 0x07 | 207 |
| 48 | 29 | 1 | 6 |  | 0x07 | 255 |
| 49 | 36 | 1 | 7 |  | 0x07 | 255 |
| 50 | 32 | 1 | 8 |  | 0x07 | 255 |
| 51 | 25 | 2 | 6 |  | 0x07 | 255 |
| 52 | 39 | 2 | 7 |  | 0x07 | 255 |
| 53 | 75 | 2 | 8 |  | 0x07 | 255 |
| 54 | 399 | 4 | 31 |  | 0x07 | 255 |
| 55 | 85 | 1 | — |  | 0x07 | 255 |
| 56 | 84 | 2 | — |  | 0x07 | 255 |
| 57 | 5 | 4 | 6 |  | 0x07 | 255 |
| 58 | 19 | 4 | 7 |  | 0x07 | 255 |
| 59 | 12 | 4 | 8 |  | 0x07 | 255 |
| 60 | 14 | 1 | 16 | 1 clickable wall | 0x06 | 255 |
| 61 | 6 | 1 | 17 | 1 clickable wall | 0x06 | 255 |
| 63 | 3 | 2 | 2 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 59 (x 27, y 1) | south | 35 | lever (to on) |
| 131 (x 3, y 4) | north | 60 | clickable wall |
| 131 (x 3, y 4) | south | 37 | clickable wall |
| 135 (x 7, y 4) | east | 63 | clickable wall |
| 135 (x 7, y 4) | west | 61 | clickable wall |
| 137 (x 9, y 4) | east | 60 | clickable wall |
| 137 (x 9, y 4) | west | 37 | clickable wall |
| 142 (x 14, y 4) | north | 60 | clickable wall |
| 142 (x 14, y 4) | south | 37 | clickable wall |
| 145 (x 17, y 4) | north | 60 | clickable wall |
| 145 (x 17, y 4) | south | 37 | clickable wall |
| 151 (x 23, y 4) | east | 60 | clickable wall |
| 151 (x 23, y 4) | west | 37 | clickable wall |
| 167 (x 7, y 5) | east | 47 | clickable wall |
| 232 (x 8, y 7) | north | 47 | clickable wall |
| 233 (x 9, y 7) | north | 63 | clickable wall |
| 233 (x 9, y 7) | south | 61 | clickable wall |
| 241 (x 17, y 7) | north | 37 | clickable wall |
| 241 (x 17, y 7) | south | 60 | clickable wall |
| 243 (x 19, y 7) | north | 43 | clickable wall |
| 246 (x 22, y 7) | north | 42 | clickable wall |
| 248 (x 24, y 7) | north | 43 | clickable wall |
| 259 (x 3, y 8) | east | 37 | clickable wall |
| 259 (x 3, y 8) | west | 60 | clickable wall |
| 303 (x 15, y 9) | north | 61 | clickable wall |
| 303 (x 15, y 9) | south | 38 | clickable wall |
| 355 (x 3, y 11) | north | 37 | clickable wall |
| 355 (x 3, y 11) | south | 60 | clickable wall |
| 396 (x 12, y 12) | south | 31 | clickable wall |
| 403 (x 19, y 12) | south | 43 | clickable wall |
| 406 (x 22, y 12) | south | 42 | clickable wall |
| 408 (x 24, y 12) | north | 60 | clickable wall |
| 408 (x 24, y 12) | south | 37 | clickable wall |
| 516 (x 4, y 16) | east | 47 | clickable wall |
| 532 (x 20, y 16) | east | 43 | clickable wall |
| 548 (x 4, y 17) | east | 63 | clickable wall |
| 548 (x 4, y 17) | west | 61 | clickable wall |
| 554 (x 10, y 17) | north | 60 | clickable wall |
| 554 (x 10, y 17) | south | 37 | clickable wall |
| 556 (x 12, y 17) | north | 31 | clickable wall |
| 568 (x 24, y 17) | east | 61 | clickable wall |
| 568 (x 24, y 17) | west | 38 | clickable wall |
| 643 (x 3, y 20) | north | 38 | clickable wall |
| 643 (x 3, y 20) | south | 61 | clickable wall |
| 657 (x 17, y 20) | east | 60 | clickable wall |
| 657 (x 17, y 20) | west | 37 | clickable wall |
| 662 (x 22, y 20) | east | 42 | clickable wall |
| 679 (x 7, y 21) | east | 43 | clickable wall |
| 686 (x 14, y 21) | east | 42 | clickable wall |
| 697 (x 25, y 21) | east | 60 | clickable wall |
| 697 (x 25, y 21) | west | 42 | clickable wall |
| 713 (x 9, y 22) | west | 42 | clickable wall |
| 721 (x 17, y 22) | west | 42 | clickable wall |
| 749 (x 13, y 23) | east | 43 | clickable wall |
| 758 (x 22, y 23) | east | 43 | clickable wall |
| 774 (x 6, y 24) | east | 42 | clickable wall |
| 785 (x 17, y 24) | west | 43 | clickable wall |
| 793 (x 25, y 24) | east | 60 | clickable wall |
| 793 (x 25, y 24) | west | 37 | clickable wall |
| 808 (x 8, y 25) | west | 43 | clickable wall |
| 813 (x 13, y 25) | east | 42 | clickable wall |
| 822 (x 22, y 25) | east | 42 | clickable wall |
| 836 (x 4, y 26) | east | 43 | clickable wall |
| 841 (x 9, y 26) | south | 43 | clickable wall |
| 913 (x 17, y 28) | north | 37 | clickable wall |
| 913 (x 17, y 28) | south | 60 | clickable wall |
| 917 (x 21, y 28) | north | 42 | clickable wall |
| 921 (x 25, y 28) | west | 42 | clickable wall |
| 951 (x 23, y 29) | north | 43 | clickable wall |
| 1003 (x 11, y 31) | north | 44 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL22.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles YVEL1; loads wall tiles YVEL2; loads monster sprites GRTORC.SHP into slot 0; loads monster sprites CABAL.SHP into slot 1; defines monster type 1; defines monster type 2; tests game flag 357 |
| INI entry 1 (runs when the level loads) | — | places item 154 (Hale leather jerkin) on block 378; places item 76 (Halberd "Sever") on block 133; places item 77 (Halberd "Widow") on block 166; places item 190 (Speckled Key) on block 730; places item 237 (Hand of Fate scroll) on block 730; places item 191 (Jade Key) on block 297; places item 156 (Plate mail) on block 264; places item 140 (Great helm) on block 298 … |

### LEVEL22.INF

| Entry | Events | What it does |
|---|---|---|
| block 27 (x 27, y 0) | party steps in, party arrives (second path), item put down | places item 139 (Whisper Cloak) on block 150; gives item 139 (Whisper Cloak); takes 1000 crown(s); sets the east wall of block 151 to type 1; moves objects from block 27 to block 977; sets game flag 378; a character speaks; place inventory item in hand … |
| block 59 (x 27, y 1) | wall clicked | sets the west wall of block 59 to type 0; plays a sound |
| block 113 (x 17, y 3) | wall clicked | clears game flag 358; clears game flag 357; sets game flag 316; place inventory item in hand; a character speaks; checks a wall of block 145; tests game flag 352; set global var … |
| block 122 (x 26, y 3) | party steps in, party arrives (second path) | loads wall tiles YVEL1; shows a message; clears game flag 357; set global var |
| block 131 (x 3, y 4) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 135 (x 7, y 4) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 137 (x 9, y 4) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 142 (x 14, y 4) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 145 (x 17, y 4) | party steps in, wall clicked | sets the north wall of block 145 to type 1; sets the north wall of block 145 to type 2; sets the north wall of block 145 to type 3; sets the north wall of block 145 to type 4; sets the north wall of block 145 to type 5; sets the north wall of block 43 to type 0; sets the north wall of block 145 to type 6; places a monster (slot 1) on block 92 … |
| block 151 (x 23, y 4) | party steps in, wall clicked | sets the east wall of block 151 to type 0; sets the east wall of block 151 to type 1; sets game flag 379; plays a sound; set global var; checks a wall of block 145; tests game flag 377; tests game flag 379 … |
| block 152 (x 24, y 4) | wall clicked | loads wall tiles YVEL2; sets the east wall of block 151 to type 1; clears game flag 358; clears game flag 357; sets game flag 357; tests game flag 352; set global var; checks a wall of block 145 … |
| block 167 (x 7, y 5) | wall clicked | a character speaks; checks a wall of block 135 |
| block 232 (x 8, y 7) | wall clicked | a character speaks; checks a wall of block 233 |
| block 233 (x 9, y 7) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 241 (x 17, y 7) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 259 (x 3, y 8) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 303 (x 15, y 9) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 355 (x 3, y 11) | party steps in, wall clicked | a character speaks; sets game flag 367; tests game flag 352; set global var; plays a sound; tests game flag 372; tests game flag 373; tests game flag 374 … |
| block 376 (x 24, y 11) | wall clicked | places item 214 (Earth Vial) on block 440; gives item 214 (Earth Vial); sets the north wall of block 416 to type 83; sets the north wall of block 416 to type 0; takes 500 crown(s); takes 50 crown(s); takes 20 crown(s); gives item 216 (Salve) … |
| block 387 (x 3, y 12) | wall clicked | sets the north wall of block 416 to type 80; sets the north wall of block 416 to type 0; gives ? crown(s); sets the south wall of block 387 to type ?; takes 225 crown(s); gives item 68 (Peregrin great bow); takes 300 crown(s); gives item 41 (Crossbow "Swift") … |
| block 396 (x 12, y 12) | wall clicked | gives item 161 (Silent sandals); gives item 262 (Bezel Cup) |
| block 408 (x 24, y 12) | party steps in, wall clicked | a character speaks; sets game flag 363; clears game flag 358; tests game flag 352; set global var; plays a sound; tests game flag 364; tests game flag 365 … |
| block 425 (x 9, y 13) | party steps in, wall clicked | no game action (only stack and screen bookkeeping) |
| block 428 (x 12, y 13) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 459 (x 11, y 14) | party steps in, wall clicked | no game action (only stack and screen bookkeeping) |
| block 516 (x 4, y 16) | wall clicked | a character speaks; checks a wall of block 548 |
| block 521 (x 9, y 16) | party steps in, wall clicked | no game action (only stack and screen bookkeeping) |
| block 524 (x 12, y 16) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 548 (x 4, y 17) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 554 (x 10, y 17) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 556 (x 12, y 17) | wall clicked | gives item 248 (Oil Flask); gives 10 crown(s); gives item 100 (Granite rock); gives item 277 (Bracers) |
| block 568 (x 24, y 17) | party steps in, wall clicked | takes 100 crown(s); gives ? crown(s); heals; takes 50 crown(s); sets the north wall of block 416 to type 83; sets the north wall of block 416 to type 0; sets game flag 585; remove character effects … |
| block 643 (x 3, y 20) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 657 (x 17, y 20) | party steps in, wall clicked | a character speaks; sets game flag 366; tests game flag 352; checks a wall of block 145; set global var; plays a sound; tests game flag 368; tests game flag 369 … |
| block 658 (x 18, y 20) | wall clicked | sets the north wall of block 416 to type 86; sets the north wall of block 416 to type 0; gives ? crown(s); takes 325 crown(s); gives item 57 (Great axe "Brimstone"); takes 550 crown(s); gives item 74 (Great sword "Justice"); takes 150 crown(s) … |
| block 697 (x 25, y 21) | party steps in, wall clicked | sets the west wall of block 697 to type 37; a character speaks; sets game flag 354; sets game flag 355; sets game flag 585; tests game flag 354; plays a sound; tests game flag 355 … |
| block 793 (x 25, y 24) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 907 (x 11, y 28) | party steps in, wall clicked | no game action (only stack and screen bookkeeping) |
| block 913 (x 17, y 28) | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 1003 (x 11, y 31) | party steps in, wall clicked | moves the party to level 24, block 674; shows a message; plays a sound; set global var |
| `0x400` level loaded | — | starts script timer 0; tests game flag 352 |
| `0x401` script timer 0 | — | tests game flag 352 |
| `0x404` a monster died | — | sets the north wall of block 43 to type ?; sets the south wall of block 145 to type 46; sets the north wall of block 145 to type 7; places a monster (slot ?) on block ?; places a monster (slot 1) on block 76; places a monster (slot 2) on block 52; places a monster (slot 1) on block 217; places a monster (slot 2) on block 474 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 154 | Hale leather jerkin | 22 | 378 |
| INI entry 1 (runs when the level loads) | 76 | Halberd "Sever" | 22 | 133 |
| INI entry 1 (runs when the level loads) | 77 | Halberd "Widow" | 22 | 166 |
| INI entry 1 (runs when the level loads) | 190 | Speckled Key | 22 | 730 |
| INI entry 1 (runs when the level loads) | 237 | Hand of Fate scroll | 22 | 730 |
| INI entry 1 (runs when the level loads) | 191 | Jade Key | 22 | 297 |
| INI entry 1 (runs when the level loads) | 156 | Plate mail | 22 | 264 |
| INI entry 1 (runs when the level loads) | 140 | Great helm | 22 | 298 |
| INI entry 1 (runs when the level loads) | 149 | Kite shield | 22 | 264 |
| INI entry 1 (runs when the level loads) | 137 | Torn shirt | 22 | 941 |
| INI entry 1 (runs when the level loads) | 271 | Ace of Dominion | 22 | 943 |
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 22 | 794 |
| INI entry 1 (runs when the level loads) | 162 | Sandals | 22 | 270 |
| INI entry 1 (runs when the level loads) | 138 | Shirt | 22 | 673 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 22 | 771 |
| INI entry 1 (runs when the level loads) | 272 | Ace of Oblivion | 22 | 771 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 22 | 455 |
| INI entry 1 (runs when the level loads) | 137 | Torn shirt | 22 | 520 |
| INI entry 1 (runs when the level loads) | 26 | Arbalest "Redemption" | 22 | 271 |
| INI entry 1 (runs when the level loads) | 148 | Aegis helm | 22 | 226 |
| INI entry 1 (runs when the level loads) | 148 | Aegis helm | 22 | 98 |
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 22 | 98 |
| INI entry 1 (runs when the level loads) | 137 | Torn shirt | 22 | 3 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 22 | 305 |
| INI entry 1 (runs when the level loads) | 158 | Dwarvish plate mail | 22 | 538 |
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 22 | 106 |
| INI entry 1 (runs when the level loads) | 270 | Ace of Infinity | 22 | 110 |
| block 27 (x 27, y 0) | 139 | Whisper Cloak | 22 | 150 |
| block 376 (x 24, y 11) | 214 | Earth Vial | 22 | 440 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| block 145 (x 17, y 4) | 92 | 0 | 1 | 3 |
| block 145 (x 17, y 4) | 92 | 0 | 1 | 3 |
| block 145 (x 17, y 4) | 91 | 0 | 1 | 3 |
| block 145 (x 17, y 4) | 124 | 0 | 1 | 3 |
| `0x404` a monster died | ? | ? | ? | ? |
| `0x404` a monster died | 76 | 0 | 1 | 4 |
| `0x404` a monster died | 76 | 0 | 1 | 4 |
| `0x404` a monster died | 52 | 0 | 2 | 4 |
| `0x404` a monster died | 52 | 0 | 2 | 4 |
| `0x404` a monster died | 217 | 0 | 1 | 4 |
| `0x404` a monster died | 217 | 0 | 1 | 4 |
| `0x404` a monster died | 474 | 0 | 2 | 4 |
| `0x404` a monster died | 474 | 0 | 2 | 4 |
| `0x404` a monster died | 635 | 0 | 1 | 4 |
| `0x404` a monster died | 635 | 0 | 1 | 4 |
| `0x404` a monster died | 859 | 0 | 2 | 4 |
| `0x404` a monster died | 859 | 0 | 2 | 4 |
| `0x404` a monster died | 947 | 0 | 2 | 4 |
| `0x404` a monster died | 947 | 0 | 2 | 4 |
| `0x404` a monster died | 971 | 0 | 1 | 4 |
| `0x404` a monster died | 971 | 0 | 1 | 4 |
| `0x404` a monster died | 609 | 0 | 2 | 4 |
| `0x404` a monster died | 609 | 0 | 2 | 4 |
| `0x404` a monster died | 161 | 0 | 2 | 4 |
| `0x404` a monster died | 161 | 0 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 11, y 31 | 0 | x 11, y 31 | 0x42d1 | FOREST |
| x 24, y 11 | 6 | x 24, y 11 | 0x41f8 | SADIE'S SHOP |
| x 18, y 20 | 8 | x 18, y 20 | 0x41d3 | VICTOR'S ARMS |
| x 3, y 12 | 4 | x 3, y 12 | 0x41e5 | FLETCHER |
| x 17, y 3 | 1 | x 17, y 3 | 0x41f9 | YVEL'S COUNCIL |
| x 24, y 4 | 7 | x 24, y 4 | 0x41fa | BRUNO'S LODGE |

## Text shown by the scripts (ids only)

- Level text file `LEVEL22.<lang>`: 43 ids: 1, 3, 5, 8, 11, 12, 13, 24, 31, 32, 33, 35, 37, 47, 49, 50, 62, 73, 75, 77, 79, 88, 90, 100, 101, 102, 114, 125, 128, 130, 133, 136, 139, 140, 145, 147, 148, 149, 150, 152, 174, 175, 178.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL22.ENG --index N`.
