# Level 20

Made by `tools/level_report.py` from `LEVEL20.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

[Item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 7 = TOWER1 (decorations `TOWER1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: TOWER1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 542 | — | — |  | 0x80 | 63 |
| 1 | 123 | 1 | — |  | 0x07 | 255 |
| 2 | 120 | 2 | — |  | 0x07 | 255 |
| 3 | 12 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 6 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 8 | 5 | — |  | 0x04 | 26 |
| 25 | 18 | 2 | 22 |  | 0x07 | 255 |
| 30 | 2 | 2 | 21 | 6 niche | 0x87 | 14 |
| 35 | 36 | — | 2 |  | 0x80 | 10 |
| 38 | 28 | — | 1 |  | 0x84 | 11 |
| 39 | 32 | — | 1 |  | 0x80 | 11 |
| 40 | 4 | 2 | — |  | 0x84 | 214 |
| 41 | 8 | 1 | 23 | 1 clickable wall | 0x07 | 255 |
| 42 | 5 | 2 | 32 | 1 clickable wall | 0x07 | 255 |
| 43 | 1 | 2 | 4 | 1 clickable wall | 0x07 | 255 |
| 46 | 1 | 1 | 7 | 2 lever (to on) | 0x07 | 207 |
| 50 | 1 | 1 | 11 | 2 lever (to on) | 0x07 | 207 |
| 52 | 1 | 1 | 13 | 2 lever (to on) | 0x07 | 207 |
| 54 | 1 | 2 | 15 | 2 lever (to on) | 0x07 | 207 |
| 56 | 2 | 1 | 17 | 2 lever (to on) | 0x07 | 207 |
| 58 | 1 | 2 | 19 | 2 lever (to on) | 0x07 | 207 |
| 60 | 1 | 2 | 24 | 1 clickable wall | 0x07 | 207 |
| 61 | 3 | 1 | 57 | 1 clickable wall | 0x07 | 207 |
| 69 | 1 | 1 | 33 | 1 clickable wall | 0x07 | 207 |
| 71 | 26 | 1 | 42 |  | 0x07 | 255 |
| 72 | 755 | 1 | 43 |  | 0x07 | 255 |
| 73 | 750 | 1 | 44 |  | 0x07 | 255 |
| 74 | 751 | 1 | 45 |  | 0x07 | 255 |
| 75 | 745 | 1 | 46 |  | 0x07 | 255 |
| 76 | 21 | 2 | 51 |  | 0x07 | 255 |
| 77 | 31 | 2 | 52 |  | 0x07 | 255 |
| 78 | 29 | 2 | 53 |  | 0x07 | 255 |
| 79 | 27 | 2 | 50 |  | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 135 (x 7, y 4) | west | 41 | clickable wall |
| 166 (x 6, y 5) | south | 69 | clickable wall |
| 192 (x 0, y 6) | east | 42 | clickable wall |
| 231 (x 7, y 7) | south | 56 | lever (to on) |
| 233 (x 9, y 7) | south | 52 | lever (to on) |
| 235 (x 11, y 7) | south | 50 | lever (to on) |
| 237 (x 13, y 7) | south | 46 | lever (to on) |
| 260 (x 4, y 8) | east | 42 | clickable wall |
| 271 (x 15, y 8) | east | 3 | door / door switch |
| 271 (x 15, y 8) | west | 3 | door / door switch |
| 321 (x 1, y 10) | south | 30 | niche |
| 322 (x 2, y 10) | south | 41 | clickable wall |
| 323 (x 3, y 10) | south | 42 | clickable wall |
| 331 (x 11, y 10) | east | 56 | lever (to on) |
| 333 (x 13, y 10) | west | 43 | clickable wall |
| 352 (x 0, y 11) | east | 41 | clickable wall |
| 356 (x 4, y 11) | west | 41 | clickable wall |
| 357 (x 5, y 11) | north | 3 | door / door switch |
| 357 (x 5, y 11) | south | 3 | door / door switch |
| 364 (x 12, y 11) | north | 3 | door / door switch |
| 364 (x 12, y 11) | south | 3 | door / door switch |
| 384 (x 0, y 12) | east | 42 | clickable wall |
| 388 (x 4, y 12) | east | 3 | door / door switch |
| 388 (x 4, y 12) | west | 3 | door / door switch |
| 391 (x 7, y 12) | east | 61 | clickable wall |
| 397 (x 13, y 12) | east | 54 | lever (to on) |
| 416 (x 0, y 13) | east | 41 | clickable wall |
| 420 (x 4, y 13) | west | 41 | clickable wall |
| 450 (x 2, y 14) | north | 41 | clickable wall |
| 450 (x 2, y 14) | west | 30 | niche |
| 451 (x 3, y 14) | north | 42 | clickable wall |
| 461 (x 13, y 14) | west | 60 | clickable wall |
| 481 (x 1, y 15) | north | 41 | clickable wall |
| 526 (x 14, y 16) | north | 61 | clickable wall |
| 550 (x 6, y 17) | west | 61 | clickable wall |
| 559 (x 15, y 17) | north | 58 | lever (to on) |
| 586 (x 10, y 18) | east | 3 | door / door switch |
| 586 (x 10, y 18) | west | 3 | door / door switch |
| 588 (x 12, y 18) | east | 3 | door / door switch |
| 588 (x 12, y 18) | west | 3 | door / door switch |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL20.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles TOWER1; loads monster sprites STARK.SHP into slot 0; loads monster sprites MINOTAUR.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x00B8` | — | places a monster of type slot 2 on block 105 in mode 2; places item 195 (Mystic Key) on block 335; places item 97 (Rapier "Talon") on block 209; places item 147 (Helm "Prentis") on block 77; places item 196 (Mystic Key) on block 398; places item 197 (Mystic Key) on block 300; places item 197 (Mystic Key) on block 321; places item 236 (Fireball scroll) on block 450 … |

### LEVEL20.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 100 (x 4, y 3) | `0x0707` | party arrives (second path) | sets all four walls of block 132 to type 35; plays chat/dialogue text ID 0x0006; checks the north wall of block 132 |
| block 131 (x 3, y 4) | `0x06C3` | party arrives (second path) | sets all four walls of block 132 to type 35; plays chat/dialogue text ID 0x0008; checks the north wall of block 132 |
| block 132 (x 4, y 4) | `0x0668` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 132 to type 36; creates item type 9 and returns its handle; launches a projectile from block 134 in direction 3; checks the north wall of block 132; plays a sound (ID 69) at block 134; checks the south wall of block 132; plays a sound (ID 80) |
| block 133 (x 5, y 4) | `0x06E5` | party arrives (second path) | sets all four walls of block 132 to type 35; plays chat/dialogue text ID 0x0007; checks the north wall of block 132 |
| block 135 (x 7, y 4) | `0x0729` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 137 (x 9, y 4) | `0x0772` | party arrives (second path), bits 0x10 (no engine caller found) | plays chat/dialogue text ID 0x0000; sets monster ? facing to 1; sets monster ? facing to 2; sets monster ? mode to 7 |
| block 165 (x 5, y 5) | `0x0745` | party arrives (second path) | sets all four walls of block 197 to type 77; checks the north wall of block 197; plays a sound (ID 38) |
| block 166 (x 6, y 5) | `0x075A` | wall clicked | sets the south wall of block 166 to type 70; plays chat/dialogue text ID 0x0003 |
| block 192 (x 0, y 6) | `0x0661` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 194 (x 2, y 6) | `0x061D` | party arrives (second path) | sets all four walls of block 226 to type 35; plays chat/dialogue text ID 0x0006; checks the north wall of block 226 |
| block 196 (x 4, y 6) | `0x0730` | party arrives (second path) | sets all four walls of block 197 to type 77; checks the north wall of block 197; plays a sound (ID 38) |
| block 226 (x 2, y 7) | `0x05C7` | party arrives (second path), party leaves (second path) | sets all four walls of block 226 to type 36; creates item type 9 and returns its handle; launches a projectile from block 193 in direction 1; checks the north wall of block 226; plays a sound (ID 69) at block 193; checks the south wall of block 226; plays a sound (ID 80) |
| block 231 (x 7, y 7) | `0x0588` | wall clicked | plays a sound (ID 79) |
| block 233 (x 9, y 7) | `0x0550` | wall clicked | plays a sound (ID 79) |
| block 235 (x 11, y 7) | `0x0518` | wall clicked | plays a sound (ID 79) |
| block 237 (x 13, y 7) | `0x04E0` | wall clicked | plays a sound (ID 79) |
| block 258 (x 2, y 8) | `0x063F` | party arrives (second path) | sets all four walls of block 226 to type 35; plays chat/dialogue text ID 0x0005; checks the north wall of block 226 |
| block 260 (x 4, y 8) | `0x05C0` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 262 (x 6, y 8) | `0x058D` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 262 to type 36; creates item type 9 and returns its handle; launches a projectile from block 261 in direction 1; checks the south wall of block 262; plays a sound (ID 80); checks the south wall of block 231; plays a sound (ID 69) at block 261 |
| block 264 (x 8, y 8) | `0x0555` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 264 to type 36; creates item type 9 and returns its handle; launches a projectile from block 261 in direction 1; checks the south wall of block 264; plays a sound (ID 80); checks the south wall of block 233; plays a sound (ID 69) at block 261 |
| block 266 (x 10, y 8) | `0x051D` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 266 to type 36; creates item type 9 and returns its handle; launches a projectile from block 261 in direction 1; checks the south wall of block 266; plays a sound (ID 80); checks the south wall of block 235; plays a sound (ID 69) at block 261 |
| block 268 (x 12, y 8) | `0x04E5` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 268 to type 36; creates item type 9 and returns its handle; launches a projectile from block 261 in direction 1; checks the south wall of block 268; plays a sound (ID 80); checks the south wall of block 237; plays a sound (ID 69) at block 261 |
| block 322 (x 2, y 10) | `0x03B6` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 323 (x 3, y 10) | `0x0385` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 330 (x 10, y 10) | `0x0241` | party steps in, party arrives (second path), item put down | moves items from block 330 to level 18, block 331 |
| block 331 (x 11, y 10) | `0x028B` | wall clicked | toggles the south wall of block 300 between types 30 and 77; sets the east wall of block 331 to type 56; sets the east wall of block 331 to type 57; plays chat/dialogue text ID 0x000d; checks the north wall of block 364; plays a sound (ID 38); checks the east wall of block 331 |
| block 333 (x 13, y 10) | `0x0234` | wall clicked | plays chat/dialogue text ID 0x000c |
| block 334 (x 14, y 10) | `0x024E` | party steps in, party arrives (second path), item put down | moves items from block 334 to level 18, block 333 |
| block 352 (x 0, y 11) | `0x03FD` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 353 (x 1, y 11) | `0x03BD` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 353 to type 36; creates item type 9 and returns its handle; launches a projectile from block 449 in direction 0; launches a projectile from block 355 in direction 3; launches a projectile from block 418 in direction 0; checks the south wall of block 353; plays a sound (ID 80); tests game flag 339 … |
| block 354 (x 2, y 11) | `0x0393` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 354 to type 36; creates item type 9 and returns its handle; launches a projectile from block 418 in direction 0; launches a projectile from block 353 in direction 1; launches a projectile from block 355 in direction 3; checks the south wall of block 354; plays a sound (ID 80); plays a sound (ID 69) at block 418 … |
| block 355 (x 3, y 11) | `0x0368` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 355 to type 36; creates item type 9 and returns its handle; launches a projectile from block 353 in direction 1; launches a projectile from block 419 in direction 0; checks the south wall of block 355; plays a sound (ID 80); plays a sound (ID 69) at block 353; plays a sound (ID 69) at block 419 |
| block 356 (x 4, y 11) | `0x038C` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 369 (x 17, y 11) | `0x033E` | party arrives (second path) | plays chat/dialogue text ID 0x000b |
| block 384 (x 0, y 12) | `0x041B` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 385 (x 1, y 12) | `0x0404` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 385 to type 36; creates item type 9 and returns its handle; launches a projectile from block 449 in direction 0; checks the south wall of block 385; plays a sound (ID 80); plays a sound (ID 69) at block 449 |
| block 386 (x 2, y 12) | `0x04B6` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 386 to type 36; creates item type 9 and returns its handle; launches a projectile from block 354 in direction 2; launches a projectile from block 385 in direction 1; launches a projectile from block 418 in direction 0; checks the south wall of block 386; plays a sound (ID 80); plays a sound (ID 69) at block 354 … |
| block 387 (x 3, y 12) | `0x0345` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 387 to type 36; creates item type 9 and returns its handle; launches a projectile from block 385 in direction 1; launches a projectile from block 355 in direction 2; launches a projectile from block 419 in direction 0; checks the south wall of block 387; plays a sound (ID 80); plays a sound (ID 69) at block 385 … |
| block 391 (x 7, y 12) | `0x025B` | wall clicked | sets the east wall of block 391 to type 68; plays chat/dialogue text ID 0x0003 |
| block 397 (x 13, y 12) | `0x0331` | wall clicked | sets all four walls of block 495 to type 0; sets all four walls of block 495 to type 38; removes monsters from block 495; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 495, facing ?; moves items from block 495 to level 18, block 495; sets game flag 46 … |
| block 401 (x 17, y 12) | `0x0327` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 401, facing ?; removes monsters from block 401; sets game flag 46; moves items from block 401 to level 18, block 401; checks the north wall of block 401 |
| block 416 (x 0, y 13) | `0x043F` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 417 (x 1, y 13) | `0x0422` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 417 to type 36; creates item type 9 and returns its handle; launches a projectile from block 449 in direction 0; launches a projectile from block 419 in direction 3; checks the south wall of block 417; plays a sound (ID 80); plays a sound (ID 69) at block 449; plays a sound (ID 69) at block 419 |
| block 418 (x 2, y 13) | `0x044D` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 418 to type 36; creates item type 9 and returns its handle; launches a projectile from block 354 in direction 2; launches a projectile from block 417 in direction 1; launches a projectile from block 419 in direction 3; checks the south wall of block 418; plays a sound (ID 80); plays a sound (ID 69) at block 354 … |
| block 419 (x 3, y 13) | `0x0492` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x10 (no engine caller found) | sets all four walls of block 419 to type 36; creates item type 9 and returns its handle; launches a projectile from block 417 in direction 1; launches a projectile from block 355 in direction 2; checks the south wall of block 419; plays a sound (ID 80); plays a sound (ID 69) at block 417; plays a sound (ID 69) at block 355 |
| block 420 (x 4, y 13) | `0x04D9` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 430 (x 14, y 13) | `0x031D` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 430, facing ?; removes monsters from block 430; sets game flag 46; moves items from block 430 to level 18, block 430; checks the north wall of block 430 |
| block 431 (x 15, y 13) | `0x0313` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 431, facing ?; removes monsters from block 431; sets game flag 46; moves items from block 431 to level 18, block 431; checks the north wall of block 431 |
| block 433 (x 17, y 13) | `0x0309` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 433, facing ?; removes monsters from block 433; sets game flag 46; moves items from block 433 to level 18, block 433; checks the north wall of block 433 |
| block 450 (x 2, y 14) | `0x0470` | wall clicked, item taken | plays chat/dialogue text ID 0x0004; sets game flag 339 |
| block 451 (x 3, y 14) | `0x04AF` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 461 (x 13, y 14) | `0x02BE` | wall clicked | plays chat/dialogue text ID 0x0003 |
| block 465 (x 17, y 14) | `0x02FF` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 465, facing ?; removes monsters from block 465; sets game flag 46; moves items from block 465 to level 18, block 465; checks the north wall of block 465 |
| block 481 (x 1, y 15) | `0x0446` | wall clicked | plays chat/dialogue text ID 0x0004 |
| block 494 (x 14, y 15) | `0x07C9` | party arrives (second path) | operates the door switch at block 493 with action -1; checks the north wall of block 526 |
| block 495 (x 15, y 15) | `0x02E2` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 495, facing ?; removes monsters from block 495; sets game flag 46; moves items from block 495 to level 18, block 495; checks the north wall of block 495 |
| block 526 (x 14, y 16) | `0x02CA` | wall clicked | sets the north wall of block 526 to type 67; plays chat/dialogue text ID 0x0003 |
| block 550 (x 6, y 17) | `0x0273` | wall clicked | sets the west wall of block 550 to type 64; plays chat/dialogue text ID 0x0003 |
| block 559 (x 15, y 17) | `0x02EC` | wall clicked | sets all four walls of block 401 to type 0; sets all four walls of block 401 to type 38; removes monsters from block 401; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 18, block 401, facing ?; moves items from block 401 to level 18, block 401; sets game flag 46 … |
| block 584 (x 8, y 18) | `0x07B8` | party steps in, party arrives (second path), item put down | moves items from block 584 to level 21, block 586; plays a sound (ID 137) |
| `0x400` level loaded | `0x01F8` | — | drops the party through a pit; clears game flag 46; sets music theme 291; sets script timer 0 to 3600 ticks; tests game flag 46 |
| `0x401` script timer 0 | `0x0213` | — | places a monster of type slot 1 on block 515 in mode 4; places a monster of type slot 1 on block 173 in mode 4 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 195 | Mystic Key | 20 | 335 |
| INI entry 1 (runs when the level loads) | 97 | Rapier "Talon" | 20 | 209 |
| INI entry 1 (runs when the level loads) | 147 | Helm "Prentis" | 20 | 77 |
| INI entry 1 (runs when the level loads) | 196 | Mystic Key | 20 | 398 |
| INI entry 1 (runs when the level loads) | 197 | Mystic Key | 20 | 300 |
| INI entry 1 (runs when the level loads) | 197 | Mystic Key | 20 | 321 |
| INI entry 1 (runs when the level loads) | 236 | Fireball scroll | 20 | 450 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 105 | 0 | 2 | 2 |
| `0x401` script timer 0 | 515 | 0 | 1 | 4 |
| `0x401` script timer 0 | 173 | 0 | 1 | 4 |
| `0x401` script timer 0 | 173 | 0 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 25, y 0 | 0 | x 25, y 0 | 0x41eb | INVALID LOCATION |

## Text shown by the scripts (ids only)

- Level text file `LEVEL20.<lang>`: 10 ids: 0, 3, 4, 5, 6, 7, 8, 11, 12, 13.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL20.ENG --index N`.
