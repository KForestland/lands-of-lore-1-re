# Level 26

Made by `tools/level_report.py` from `LEVEL26.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 10 = RUIN (decorations `RUIN.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: RUIN (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 1504 | — | — |  | 0x80 | 63 |
| 1 | 1186 | 1 | — |  | 0x07 | 255 |
| 2 | 1186 | 2 | — |  | 0x07 | 255 |
| 3 | 18 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 4 | 3 | — |  | 0xaf | 13 |
| 13 | 15 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 18 | 3 | 3 | — |  | 0xaf | 13 |
| 23 | 8 | 4 | — |  | 0x84 | 25 |
| 27 | 12 | — | 9 |  | 0x80 | 10 |
| 30 | 1 | 1 | 13 | 3 lever (to off) | 0x07 | 207 |
| 31 | 1 | 1 | 5 | 6 niche | 0x87 | 14 |
| 32 | 4 | 1 | 20 | 1 clickable wall | 0x07 | 210 |
| 36 | 12 | 2 | — |  | 0x84 | 22 |
| 37 | 12 | — | — |  | 0x84 | 17 |
| 38 | 1 | 2 | 10 | 2 lever (to on) | 0x07 | 207 |
| 40 | 2 | 1 | 6 | 2 lever (to on) | 0x07 | 207 |
| 42 | 72 | — | 1 |  | 0x80 | 63 |
| 43 | 3 | 1 | 4 | 1 clickable wall | 0x07 | 207 |
| 44 | 1 | 2 | 29 | 1 clickable wall | 0x07 | 207 |
| 45 | 1 | 1 | 30 | 1 clickable wall | 0x07 | 207 |
| 46 | 40 | 1 | 32 |  | 0x07 | 255 |
| 47 | 3 | 2 | 24 | 1 clickable wall | 0x07 | 255 |
| 53 | 1 | 2 | 16 | 2 lever (to on) | 0x07 | 207 |
| 55 | 1 | 2 | 18 | 2 lever (to on) | 0x07 | 207 |
| 57 | 4 | 2 | 8 | 1 clickable wall | 0x07 | 255 |
| 58 | 1 | 2 | 28 | 1 clickable wall | 0x07 | 207 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 46 (x 14, y 1) | south | 30 | lever (to off) |
| 59 (x 27, y 1) | west | 32 | clickable wall |
| 75 (x 11, y 2) | east | 31 | niche |
| 109 (x 13, y 3) | south | 32 | clickable wall |
| 131 (x 3, y 4) | east | 57 | clickable wall |
| 252 (x 28, y 7) | east | 40 | lever (to on) |
| 265 (x 9, y 8) | north | 3 | door / door switch |
| 265 (x 9, y 8) | south | 3 | door / door switch |
| 276 (x 20, y 8) | north | 3 | door / door switch |
| 276 (x 20, y 8) | south | 3 | door / door switch |
| 334 (x 14, y 10) | east | 32 | clickable wall |
| 337 (x 17, y 10) | east | 13 | door / door switch |
| 337 (x 17, y 10) | west | 13 | door / door switch |
| 361 (x 9, y 11) | north | 57 | clickable wall |
| 401 (x 17, y 12) | east | 3 | door / door switch |
| 401 (x 17, y 12) | west | 3 | door / door switch |
| 446 (x 30, y 13) | north | 13 | door / door switch |
| 479 (x 31, y 14) | west | 45 | clickable wall |
| 489 (x 9, y 15) | north | 3 | door / door switch |
| 489 (x 9, y 15) | south | 3 | door / door switch |
| 491 (x 11, y 15) | north | 13 | door / door switch |
| 491 (x 11, y 15) | south | 13 | door / door switch |
| 526 (x 14, y 16) | west | 32 | clickable wall |
| 529 (x 17, y 16) | north | 3 | door / door switch |
| 529 (x 17, y 16) | south | 3 | door / door switch |
| 531 (x 19, y 16) | north | 13 | door / door switch |
| 531 (x 19, y 16) | south | 13 | door / door switch |
| 566 (x 22, y 17) | west | 58 | clickable wall |
| 568 (x 24, y 17) | north | 13 | door / door switch |
| 591 (x 15, y 18) | north | 38 | lever (to on) |
| 592 (x 16, y 18) | north | 13 | door / door switch |
| 592 (x 16, y 18) | south | 13 | door / door switch |
| 594 (x 18, y 18) | north | 3 | door / door switch |
| 594 (x 18, y 18) | south | 3 | door / door switch |
| 596 (x 20, y 18) | north | 13 | door / door switch |
| 596 (x 20, y 18) | south | 13 | door / door switch |
| 599 (x 23, y 18) | east | 43 | clickable wall |
| 615 (x 7, y 19) | east | 57 | clickable wall |
| 625 (x 17, y 19) | west | 40 | lever (to on) |
| 648 (x 8, y 20) | north | 3 | door / door switch |
| 648 (x 8, y 20) | south | 3 | door / door switch |
| 651 (x 11, y 20) | north | 13 | door / door switch |
| 651 (x 11, y 20) | south | 13 | door / door switch |
| 654 (x 14, y 20) | north | 3 | door / door switch |
| 654 (x 14, y 20) | south | 3 | door / door switch |
| 656 (x 16, y 20) | north | 47 | clickable wall |
| 658 (x 18, y 20) | north | 47 | clickable wall |
| 663 (x 23, y 20) | north | 3 | door / door switch |
| 691 (x 19, y 21) | east | 43 | clickable wall |
| 696 (x 24, y 21) | west | 43 | clickable wall |
| 723 (x 19, y 22) | west | 13 | door / door switch |
| 786 (x 18, y 24) | south | 55 | lever (to on) |
| 812 (x 12, y 25) | east | 53 | lever (to on) |
| 866 (x 2, y 27) | north | 3 | door / door switch |
| 867 (x 3, y 27) | south | 44 | clickable wall |
| 896 (x 0, y 28) | east | 47 | clickable wall |
| 933 (x 5, y 29) | north | 57 | clickable wall |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL26.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles RUIN; sets the west wall of block 834 to type 37; sets the west wall of block 414 to type 37; loads monster sprites KNOWLES.SHP into slot 0; defines monster type 1; loads monster sprites XEOB.SHP into slot 1; defines monster type 2; loads monster sprites XEOB.SHP into slot 0 … |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 122; places a monster (slot 1) on block 346; places a monster (slot 1) on block 371; places a monster (slot 1) on block 823; places a monster (slot 1) on block 815; places a monster (slot 1) on block 868; places a monster (slot 1) on block 630; places a monster (slot 1) on block 726 … |

### LEVEL26.INF

| Entry | Events | What it does |
|---|---|---|
| block 46 (x 14, y 1) | wall clicked | toggles the west wall of block 77 between types 0 and 1; plays a sound |
| block 58 (x 26, y 1) | bits 0x400 (no engine caller found) | sets game flag 414; checks a wall of block 224; tests game flag 414 |
| block 59 (x 27, y 1) | wall clicked | gives item 130 (Dwarvish boots); gives item 157 (Galenian plate mail); sets game flag 414; checks a wall of block 224; tests game flag 414 |
| block 109 (x 13, y 3) | wall clicked | gives item 278 (Steel Bracers); gives item 271 (Ace of Dominion); gives item 269 (Guardian) |
| block 131 (x 3, y 4) | wall clicked | a character speaks |
| block 134 (x 6, y 4) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 141 (x 13, y 4) | bits 0x400 (no engine caller found) | no game action (only stack and screen bookkeeping) |
| block 251 (x 27, y 7) | party arrives (second path) | sets the west wall of block 252 to type 1; sets the east wall of block 252 to type 40; checks a wall of block 252; plays a sound |
| block 252 (x 28, y 7) | wall clicked | sets the west wall of block 252 to type 0; plays a sound |
| block 253 (x 29, y 7) | party arrives (second path) | places item 180 (Xeob Key) on block 835; places item 181 (Knowle Key) on block 380; sets game flag 415; tests game flag 415 |
| block 254 (x 30, y 7) | party steps in, party arrives (second path), item put down | moves objects from block 254 to block 395 |
| block 265 (x 9, y 8) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 334 (x 14, y 10) | wall clicked | gives item 126 (Trident "Mandible"); gives 50 crown(s); gives item 158 (Dwarvish plate mail); gives item 215 (Bannon's reserve); sets game flag 409; checks a wall of block 32; tests game flag 409 |
| block 335 (x 15, y 10) | bits 0x400 (no engine caller found) | sets game flag 409; checks a wall of block 32; tests game flag 409 |
| block 382 (x 30, y 11) | party arrives (second path), wall clicked | a character speaks; sets game flag 423; tests game flag 582; plays a sound; tests game flag 417; tests game flag 423; set global var |
| block 414 (x 30, y 12) | party arrives (second path), bits 0x4000 (no engine caller found) | places a monster (slot 2) on block 382; places a monster (slot 2) on block 381; places a monster (slot 2) on block 413; sets the west wall of block 414 to type 0; places item 264 (Vaelan's Cube) on block 414; places item 181 (Knowle Key) on block 414; places item 114 (Death Stick) on block 414; heals … |
| block 469 (x 21, y 14) | party steps in, party arrives (second path), item put down | moves objects from block 469 to block 437 |
| block 479 (x 31, y 14) | wall clicked | a character speaks |
| block 525 (x 13, y 16) | bits 0x400 (no engine caller found) | sets game flag 410; checks a wall of block 96; tests game flag 410 |
| block 526 (x 14, y 16) | wall clicked | gives item 216 (Salve); gives item 221 (Diamond); sets game flag 410; checks a wall of block 96; tests game flag 410 |
| block 566 (x 22, y 17) | wall clicked | a character speaks |
| block 591 (x 15, y 18) | wall clicked | plays a sound |
| block 592 (x 16, y 18) | party arrives (second path) | sets the west wall of block 623 to type 1; checks a wall of block 623; plays a sound |
| block 599 (x 23, y 18) | wall clicked | a character speaks |
| block 615 (x 7, y 19) | wall clicked | a character speaks |
| block 619 (x 11, y 19) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 619 to type 28; make item; play environmental sfx; launches a projectile; checks a wall of block 619; plays a sound |
| block 622 (x 14, y 19) | party arrives (second path), party leaves (second path), item put down, item taken | sets the west wall of block 622 to type 28; sets the west wall of block 623 to type 0; make item; play environmental sfx; launches a projectile; checks a wall of block 622; plays a sound; checks a wall of block 623 |
| block 624 (x 16, y 19) | bits 0x400 (no engine caller found) | sets game flag 411; checks a wall of block 128; tests game flag 411 |
| block 625 (x 17, y 19) | wall clicked | sets the west wall of block 623 to type 0; operates the door at block 592; checks a wall of block 623; checks a wall of block 592; checks a wall of block 591; plays a sound |
| block 626 (x 18, y 19) | bits 0x400 (no engine caller found) | sets game flag 412; moves objects from block 626 to block 503; checks a wall of block 160; tests game flag 412; plays a sound |
| block 628 (x 20, y 19) | party steps in, party arrives (second path), item put down | moves objects from block 628 to block 535; plays a sound |
| block 656 (x 16, y 20) | wall clicked | gives item 34 (Axe "Butcher"); gives item 248 (Oil Flask); sets game flag 411; checks a wall of block 128; tests game flag 411 |
| block 658 (x 18, y 20) | wall clicked | gives item 42 (Crossbow "Elayna"); gives item 142 (Great helm "Nestor"); sets game flag 412; moves objects from block 658 to block 503; checks a wall of block 160; tests game flag 412; plays a sound |
| block 691 (x 19, y 21) | wall clicked | a character speaks |
| block 696 (x 24, y 21) | wall clicked | a character speaks |
| block 734 (x 30, y 22) | party arrives (second path), item put down | moves the party to level 23, block 857; moves objects from block 734 to block 857; plays a sound |
| block 754 (x 18, y 23) | party steps in, party arrives (second path), item put down | moves objects from block 754 to block 565; plays a sound |
| block 773 (x 5, y 24) | party arrives (second path) | make item; play environmental sfx; launches a projectile |
| block 786 (x 18, y 24) | wall clicked | toggles the west wall of block 817 between types 0 and 1; toggles the north wall of block 850 between types 31 and 1; plays a sound |
| block 812 (x 12, y 25) | wall clicked | toggles the west wall of block 814 between types 31 and 1 |
| block 834 (x 2, y 26) | party arrives (second path), bits 0x4000 (no engine caller found) | sets the west wall of block 834 to type 0; places a monster (slot 2) on block 835; places a monster (slot 2) on block 834; places item 264 (Vaelan's Cube) on block 834; places item 180 (Xeob Key) on block 834; places item 74 (Great sword "Justice") on block 834; heals; a character speaks … |
| block 835 (x 3, y 26) | party steps in, wall clicked | shows a message; a character speaks; tests game flag 583; plays a sound; tests game flag 415; tests game flag 416; set global var |
| block 850 (x 18, y 26) | item put down | moves objects from block 850 to block 820; plays a sound |
| block 867 (x 3, y 27) | wall clicked | a character speaks |
| block 896 (x 0, y 28) | wall clicked | gives item 150 (George's kite shield); gives item 136 (Chain mail "Protector"); sets game flag 413; checks a wall of block 192; tests game flag 413 |
| block 897 (x 1, y 28) | bits 0x400 (no engine caller found) | sets game flag 413; checks a wall of block 192; tests game flag 413 |
| block 933 (x 5, y 29) | wall clicked | a character speaks |
| `0x400` level loaded | — | drops the party through a pit; clears game flag 46; starts script timer 0; tests game flag 46 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 984; places a monster (slot 1) on block 82; sets the north wall of block 0 to type ?; checks a wall of block 0 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 179 | Gold Key | 26 | 270 |
| INI entry 1 (runs when the level loads) | 183 | Copper Key | 26 | 779 |
| INI entry 1 (runs when the level loads) | 262 | Bezel Cup | 26 | 814 |
| INI entry 1 (runs when the level loads) | 199 | Nathanial's Key | 26 | 75 |
| INI entry 1 (runs when the level loads) | 269 | Guardian | 26 | 712 |
| INI entry 1 (runs when the level loads) | 272 | Ace of Oblivion | 26 | 380 |
| INI entry 1 (runs when the level loads) | 215 | Bannon's reserve | 26 | 380 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 26 | 380 |
| block 253 (x 29, y 7) | 180 | Xeob Key | 26 | 835 |
| block 253 (x 29, y 7) | 181 | Knowle Key | 26 | 380 |
| block 414 (x 30, y 12) | 264 | Vaelan's Cube | 26 | 414 |
| block 414 (x 30, y 12) | 181 | Knowle Key | 26 | 414 |
| block 414 (x 30, y 12) | 114 | Death Stick | 26 | 414 |
| block 834 (x 2, y 26) | 264 | Vaelan's Cube | 26 | 834 |
| block 834 (x 2, y 26) | 180 | Xeob Key | 26 | 834 |
| block 834 (x 2, y 26) | 74 | Great sword "Justice" | 26 | 834 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 122 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 122 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 346 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 346 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 371 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 371 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 823 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 823 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 815 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 815 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 868 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 868 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 630 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 630 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 726 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 726 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 899 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 899 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 478 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 478 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 53 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 53 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 87 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 87 | 3 | 1 | 3 |
| block 414 (x 30, y 12) | 382 | 2 | 2 | 7 |
| block 414 (x 30, y 12) | 381 | 2 | 2 | 7 |
| block 414 (x 30, y 12) | 413 | 1 | 2 | 7 |
| block 834 (x 2, y 26) | 835 | 3 | 2 | 7 |
| block 834 (x 2, y 26) | 835 | 3 | 2 | 7 |
| block 834 (x 2, y 26) | 834 | 2 | 2 | 7 |
| `0x401` script timer 0 | 984 | 0 | 1 | 7 |
| `0x401` script timer 0 | 984 | 0 | 1 | 7 |
| `0x401` script timer 0 | 82 | 3 | 1 | 7 |
| `0x401` script timer 0 | 82 | 3 | 1 | 7 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 31, y 7 | 0 | x 30, y 7 | 0x41f2 | YVEL CAVE |

## Text shown by the scripts (ids only)

- Level text file `LEVEL26.<lang>`: 15 ids: 2, 4, 6, 7, 8, 9, 11, 15, 17, 18, 19, 21, 22, 25, 33.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL26.ENG --index N`.
