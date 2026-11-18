# Level 7

Made by `tools/level_report.py` from `LEVEL7.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 618 | — | — |  | 0x80 | 63 |
| 1 | 1693 | 1 | — |  | 0x07 | 255 |
| 2 | 1686 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 24 | 12 | 5 | — |  | 0x04 | 26 |
| 26 | 4 | — | — |  | 0x84 | 63 |
| 27 | 3 | 1 | 49 | 2 lever (to on) | 0x07 | 207 |
| 29 | 1 | 2 | 70 | 2 lever (to on) | 0x07 | 207 |
| 31 | 3 | 1 | 61 | 2 lever (to on) | 0x07 | 207 |
| 33 | 1 | 1 | 53 | 1 clickable wall | 0x07 | 207 |
| 37 | 20 | — | 22 |  | 0x80 | 63 |
| 38 | 8 | — | 19 |  | 0x84 | 11 |
| 41 | 2 | 1 | 45 |  | 0x07 | 255 |
| 42 | 1 | 1 | 68 | 2 lever (to on) | 0x07 | 207 |
| 45 | 5 | 1 | 50 | 6 niche | 0x87 | 14 |
| 46 | 4 | 2 | — |  | 0x00 | 214 |
| 48 | 1 | 2 | 46 | 1 clickable wall | 0x07 | 207 |
| 49 | 1 | 2 | 72 | 1 clickable wall | 0x07 | 207 |
| 53 | 4 | 1 | 26 | 1 clickable wall | 0x07 | 210 |
| 54 | 2 | 1 | 66 | 2 lever (to on) | 0x07 | 207 |
| 60 | 4 | 5 | — |  | 0x06 | 63 |
| 61 | 2 | 2 | 63 | 1 clickable wall | 0x07 | 255 |
| 65 | 2 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 66 | 2 | 1 | 38 | 1 clickable wall | 0x07 | 255 |
| 69 | 4 | 1 | 36 |  | 0x06 | 25 |
| 77 | 2 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 1 | 2 | 60 | 1 clickable wall | 0x07 | 255 |
| 79 | 4 | 2 | 64 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 23 (x 23, y 0) | south | 77 | clickable wall |
| 27 (x 27, y 0) | south | 77 | clickable wall |
| 89 (x 25, y 2) | north | 78 | clickable wall |
| 130 (x 2, y 4) | south | 49 | clickable wall |
| 161 (x 1, y 5) | south | 79 | clickable wall |
| 171 (x 11, y 5) | south | 79 | clickable wall |
| 227 (x 3, y 7) | west | 54 | lever (to on) |
| 237 (x 13, y 7) | south | 54 | lever (to on) |
| 242 (x 18, y 7) | south | 65 | clickable wall |
| 261 (x 5, y 8) | west | 27 | lever (to on) |
| 262 (x 6, y 8) | south | 66 | clickable wall |
| 265 (x 9, y 8) | north | 53 | clickable wall |
| 265 (x 9, y 8) | east | 53 | clickable wall |
| 268 (x 12, y 8) | east | 45 | niche |
| 270 (x 14, y 8) | east | 61 | clickable wall |
| 275 (x 19, y 8) | west | 53 | clickable wall |
| 289 (x 1, y 9) | south | 79 | clickable wall |
| 295 (x 7, y 9) | west | 66 | clickable wall |
| 335 (x 15, y 10) | south | 45 | niche |
| 361 (x 9, y 11) | south | 61 | clickable wall |
| 361 (x 9, y 11) | west | 53 | clickable wall |
| 366 (x 14, y 11) | east | 27 | lever (to on) |
| 371 (x 19, y 11) | west | 31 | lever (to on) |
| 392 (x 8, y 12) | south | 29 | lever (to on) |
| 400 (x 16, y 12) | south | 45 | niche |
| 433 (x 17, y 13) | west | 27 | lever (to on) |
| 482 (x 2, y 15) | east | 79 | clickable wall |
| 489 (x 9, y 15) | east | 65 | clickable wall |
| 513 (x 1, y 16) | south | 33 | clickable wall |
| 522 (x 10, y 16) | north | 42 | lever (to on) |
| 524 (x 12, y 16) | north | 31 | lever (to on) |
| 998 (x 6, y 31) | north | 45 | niche |
| 998 (x 6, y 31) | east | 48 | clickable wall |
| 998 (x 6, y 31) | south | 31 | lever (to on) |
| 998 (x 6, y 31) | west | 45 | niche |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and marks effects inferred from ScummVM **UNCONFIRMED** for DOS where applicable.

### LEVEL7.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CAVE1; places a monster of type slot 1 on block 194 in mode 7; loads monster sprites SCAVNGR.SHP into slot 0; loads monster sprites RATMAN.SHP into slot 0; loads monster sprites CAVEDWLR.SHP into slot 1; defines monster type 1; defines monster type 2; defines monster type 3 … |
| INI entry 1 (runs when the level loads) | `0x011F` | — | places a monster of type slot 2 on block 488 in mode 3; places a monster of type slot 2 on block 484 in mode 3; places a monster of type slot 2 on block 616 in mode 3; places a monster of type slot 2 on block 580 in mode 3; places item 99 (Rock) on block 229; places item 99 (Rock) on block 429; places item 99 (Rock) on block 369; places item 153 (Leather jerkin) on block 103 … |

### LEVEL7.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 58 (x 26, y 1) | `0x0CD5` | party arrives (second path) | sets the north wall of block 999 to type 1; plays chat/dialogue text ID 0x0015; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0016; checks the north wall of block 999 |
| block 66 (x 2, y 2) | `0x0B7B` | wall clicked | a character joins the party; loads cut-scene POD1.TIM into slot 0; loads cut-scene POD2.TIM into slot 0; requests engine global change, selector 0, operands 0, 130; requests engine global change, selector 1, operands 0, 2; plays music track 273; plays chat/dialogue text ID 0x0013; sets game flag 56 … |
| block 98 (x 2, y 3) | `0x0AED` | party steps in, party arrives (second path) | requests engine global change, selector 10, operands 0, 0; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 130; requests engine global change, selector 10, operands 0, 2; plays music track 279; sets game flag 59; plays chat/dialogue text ID 0x0007; tests game flag 58 … |
| block 109 (x 13, y 3) | `0x08B0` | party arrives (second path) | sets all four walls of block 295 to type 1 |
| block 118 (x 22, y 3) | `0x0A07` | party steps in, party arrives (second path), item put down | moves items from block 118 to level 6, block 150 |
| block 124 (x 28, y 3) | `0x0A12` | party steps in, party arrives (second path), item put down | moves items from block 124 to level 8, block 156 |
| block 130 (x 2, y 4) | `0x0AD6` | wall clicked | sets all four walls of block 98 to type 1; sets all four walls of block 130 to type 0; tests game flag 588; plays a sound (ID 38) |
| block 161 (x 1, y 5) | `0x0D11` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 162 (x 2, y 5) | `0x0D2F` | party arrives (second path) | sets all four walls of block 98 to type 1; sets game flag 548; plays chat/dialogue text ID 0x0028; tests game flag 548; tests game flag 588 |
| block 169 (x 9, y 5) | `0x086D` | party arrives (second path) | places a monster of type slot 3 on block 139 in mode 4; places a monster of type slot 3 on block 107 in mode 4; character surprise feedback; move party |
| block 171 (x 11, y 5) | `0x0D23` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 207 (x 15, y 6) | `0x09FA` | party steps in, party arrives (second path), item put down | moves items from block 207 to level 8, block 208 |
| block 227 (x 3, y 7) | `0x0A9B` | wall clicked | toggles all four walls of block 258 between types 0 and 1; plays a sound (ID 38) |
| block 233 (x 9, y 7) | `0x08A5` | bits 0x400 (no engine caller found) | puts item 243 (Coin Purse) on an empty cursor |
| block 237 (x 13, y 7) | `0x063A` | wall clicked | places or moves item handle ? to level 7, block 992; places or moves item handle ? to level 7, block 993; places or moves item handle ? to level 7, block 268; sets the east wall of block 268 to type 45; sets the east wall of block 268 to type 31; sets the east wall of block 268 to type 47; sets all four walls of block 268 to type 0; remove level item … |
| block 242 (x 18, y 7) | `0x0D50` | wall clicked | plays chat/dialogue text ID 0x0029 |
| block 261 (x 5, y 8) | `0x084A` | wall clicked | operates the door switch at block 293 with action 0 |
| block 262 (x 6, y 8) | `0x0851` | wall clicked | plays chat/dialogue text ID 0x0002; plays chat/dialogue text ID 0x0004; sets game flag 141; plays chat/dialogue text ID 0x001a; checks the south wall of block 262; tests game flag 141 |
| block 265 (x 9, y 8) | `0x0898` | wall clicked | puts item 243 (Coin Purse) on an empty cursor; deals damage to the party (amount ?); checks the south wall of block 994 |
| block 266 (x 10, y 8) | `0x08B8` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 994 |
| block 268 (x 12, y 8) | `0x06DD` | wall clicked, item put down | places or moves item handle ? to level 9, block 219; sets the east wall of block 268 to type 1; remove level item; sets game flag ?; plays chat/dialogue text ID 0x0021; plays chat/dialogue text ID 0x4084; plays chat/dialogue text ID 0x0022; moves items from block 268 to level 9, block 219 … |
| block 270 (x 14, y 8) | `0x0D29` | wall clicked | plays chat/dialogue text ID 0x0025 |
| block 274 (x 18, y 8) | `0x0A1D` | bits 0x400 (no engine caller found) | deals damage to the party (amount ?); checks the south wall of block 995 |
| block 275 (x 19, y 8) | `0x0A21` | wall clicked | deals damage to the party (amount ?); checks the south wall of block 995 |
| block 289 (x 1, y 9) | `0x0D17` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 290 (x 2, y 9) | `0x0AA7` | party steps in, party arrives (second path), item put down | plays chat/dialogue text ID 0x0014; sets game flag 125; moves items from block 290 to level 6, block 322; tests game flag 125; checks speech playback |
| block 295 (x 7, y 9) | `0x085F` | wall clicked | plays chat/dialogue text ID 0x0002; plays chat/dialogue text ID 0x0004; sets game flag 140; plays chat/dialogue text ID 0x001a; checks the west wall of block 295; tests game flag 140 |
| block 296 (x 8, y 9) | `0x08A9` | party arrives (second path) | sets all four walls of block 108 to type 1 |
| block 360 (x 8, y 11) | `0x0846` | bits 0x400 (no engine caller found) | puts item 247 (Broken glass) on an empty cursor; puts item 248 (Oil Flask) on an empty cursor; sets the west wall of block 992 to type 0; checks the west wall of block 992 |
| block 361 (x 9, y 11) | `0x0838` | wall clicked | puts item 247 (Broken glass) on an empty cursor; puts item 248 (Oil Flask) on an empty cursor; sets the west wall of block 992 to type 0; plays chat/dialogue text ID 0x0025; checks the west wall of block 992 |
| block 366 (x 14, y 11) | `0x0A4B` | wall clicked, thrown item hits | sets all four walls of block 367 to type 38; removes monsters from block 367; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 8, block 367, facing ?; sets all four walls of block 367 to type 0; moves items from block 367 to level 8, block 367; sets game flag 46 … |
| block 367 (x 15, y 11) | `0x0A73` | party arrives (second path), item put down | removes monsters from block 367; moves items from block 367 to level 8, block 367; checks the north wall of block 367 |
| block 371 (x 19, y 11) | `0x0A25` | wall clicked | creates item type 9 and returns its handle; launches a projectile from block 274 in direction 2; checks the west wall of block 371; plays a sound (ID 69) |
| block 392 (x 8, y 12) | `0x0958` | wall clicked | sets the east wall of block 423 to type 45; places item 218 (Ginseng) on block 423; checks the east wall of block 423; plays a sound (ID 38) |
| block 420 (x 4, y 13) | `0x0807` | party arrives (second path) | places a monster of type slot 2 on block 321 in mode 4; plays chat/dialogue text ID 0x0001; character surprise feedback; move party |
| block 425 (x 9, y 13) | `0x0954` | party arrives (second path) | character surprise feedback; move party |
| block 426 (x 10, y 13) | `0x09D8` | party arrives (second path) | sets all four walls of block 427 to type 46; checks the north wall of block 427; plays a sound (ID 38) |
| block 430 (x 14, y 13) | `0x0A7D` | party arrives (second path), item put down | removes monsters from block 430; moves items from block 430 to level 8, block 430; checks the north wall of block 430 |
| block 431 (x 15, y 13) | `0x0A87` | party arrives (second path), item put down | removes monsters from block 431; moves items from block 431 to level 8, block 431; checks the north wall of block 431 |
| block 432 (x 16, y 13) | `0x0A91` | party arrives (second path), item put down | removes monsters from block 432; moves items from block 432 to level 8, block 432; checks the north wall of block 432 |
| block 433 (x 17, y 13) | `0x097B` | wall clicked, thrown item hits | toggles the west wall of block 433 between types 27 and 28; sets all four walls of block 430 to type 0; sets all four walls of block 431 to type 38; removes monsters from block 431; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 8, block 431, facing ?; sets all four walls of block 431 to type 0 … |
| block 455 (x 7, y 14) | `0x062B` | party arrives (second path) | sets game flag 138; tests game flag 138 |
| block 482 (x 2, y 15) | `0x0D1D` | wall clicked | plays chat/dialogue text ID 0x0024 |
| block 489 (x 9, y 15) | `0x0D0A` | wall clicked | plays chat/dialogue text ID 0x001a |
| block 495 (x 15, y 15) | `0x09ED` | party steps in, party arrives (second path), item put down | moves items from block 495 to level 8, block 527 |
| block 513 (x 1, y 16) | `0x093F` | wall clicked | sets all four walls of block 513 to type 0; checks the north wall of block 513; plays a sound (ID 38) |
| block 522 (x 10, y 16) | `0x08E4` | wall clicked | sets all four walls of block 522 to type 0; checks the north wall of block 522; plays a sound (ID 38) |
| block 524 (x 12, y 16) | `0x08BC` | wall clicked | creates item type 9 and returns its handle; launches a projectile from block 490 in direction 1; checks the north wall of block 524; plays a sound (ID 69) at block 490 |
| block 554 (x 10, y 17) | `0x08F9` | party arrives (second path) | sets all four walls of block 522 to type 1; places a monster of type slot 2 on block 616 in mode 7; places a monster of type slot 2 on block 580 in mode 7; checks the north wall of block 522; plays a sound (ID 38) |
| `0x400` level loaded | `0x059A` | — | drops the party through a pit; clears game flag 46; sets script timer 0 to 3600 ticks; sets music theme 273; tests game flag 46 |
| `0x401` script timer 0 | `0x05B5` | — | places a monster of type slot 2 on block 203 in mode 4; places a monster of type slot 2 on block 271 in mode 4; places a monster of type slot 3 on block 302 in mode 4; clears game flag 130; sets game flag 130; tests game flag 130 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 229 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 429 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 7 | 369 |
| INI entry 1 (runs when the level loads) | 153 | Leather jerkin | 7 | 103 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 7 | 463 |
| INI entry 1 (runs when the level loads) | 59 | Sledge | 7 | 196 |
| INI entry 1 (runs when the level loads) | 46 | Dagger "Stiletto" | 7 | 463 |
| INI entry 1 (runs when the level loads) | 116 | Star "Shining" | 7 | 555 |
| INI entry 1 (runs when the level loads) | 169 | Worn key | 7 | 335 |
| INI entry 1 (runs when the level loads) | 275 | Note | 7 | 268 |
| INI entry 1 (runs when the level loads) | 250 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 251 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 252 | Humanoid bone | 7 | 130 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 7 | 423 |
| block 392 (x 8, y 12) | 218 | Ginseng | 7 | 423 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 0 (runs when the level loads) | 194 | 0 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 488 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 484 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 484 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 616 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 616 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 580 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 580 | 3 | 2 | 3 |
| block 169 (x 9, y 5) | 139 | 0 | 3 | 4 |
| block 169 (x 9, y 5) | 107 | 1 | 3 | 4 |
| block 420 (x 4, y 13) | 321 | 2 | 2 | 4 |
| block 420 (x 4, y 13) | 321 | 2 | 2 | 4 |
| block 554 (x 10, y 17) | 616 | 0 | 2 | 7 |
| block 554 (x 10, y 17) | 580 | 0 | 2 | 7 |
| `0x401` script timer 0 | 203 | 2 | 2 | 4 |
| `0x401` script timer 0 | 203 | 2 | 2 | 4 |
| `0x401` script timer 0 | 271 | 1 | 2 | 4 |
| `0x401` script timer 0 | 271 | 1 | 2 | 4 |
| `0x401` script timer 0 | 302 | 1 | 3 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 2, y 2 | 6 | x 2, y 3 | 0x41df | POD ROOM |

## Text shown by the scripts (ids only)

- Level text file `LEVEL07.<lang>`: 22 ids: 1, 2, 4, 7, 8, 9, 10, 19, 20, 21, 22, 26, 28, 30, 31, 32, 33, 34, 36, 37, 40, 41.
- Global text `LANDS.<lang>`: 2 ids: 0x403f, 0x4084.

Read any of them with `tools/decode_dialogue.py LEVEL07.ENG --index N`.
