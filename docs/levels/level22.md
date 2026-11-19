# Level 22

Made by `tools/level_report.py` from `LEVEL22.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

[Item, spell and creature numbers](../NUMBERS.md).

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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL22.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x003E` | — | loads wall tiles YVEL1; loads wall tiles YVEL2; loads monster sprites GRTORC.SHP into slot 0; loads monster sprites CABAL.SHP into slot 1; defines monster type 1; defines monster type 2; tests game flag 357 |
| INI entry 1 (runs when the level loads) | `0x0108` | — | places item 154 (Hale leather jerkin) on block 378; places item 76 (Halberd "Sever") on block 133; places item 77 (Halberd "Widow") on block 166; places item 190 (Speckled Key) on block 730; places item 237 (Hand of Fate scroll) on block 730; places item 191 (Jade Key) on block 297; places item 156 (Plate mail) on block 264; places item 140 (Great helm) on block 298 … |

### LEVEL22.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 27 (x 27, y 0) | `0x1B3F` | party steps in, party arrives (second path), item put down | places item 139 (Whisper Cloak) on block 150; gives item 139 (Whisper Cloak) if inventory placement succeeds; puts item 139 (Whisper Cloak) on an empty cursor; takes 1000 crown(s); sets the east wall of block 151 to type 1; moves items from block 27 to level 23, block 977; sets game flag 378; plays chat/dialogue text ID 0x0080 … |
| block 59 (x 27, y 1) | `0x1B35` | wall clicked | sets all four walls of block 59 to type 0; plays a sound (ID 38) |
| block 113 (x 17, y 3) | `0x188C` | wall clicked | requests engine global change, selector 0, operands 0, 177; clears game flag 358; clears game flag 357; plays music track ?; sets game flag 316; place inventory item in hand; plays chat/dialogue text ID 0x004f; checks the north wall of block 145 … |
| block 122 (x 26, y 3) | `0x20EB` | party steps in, party arrives (second path) | loads wall tiles YVEL1; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 123; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 10, operands 0, 2; requests engine global change, selector 0, operands 0, 151; requests engine global change, selector 1, operands 0, 1; clears game flag 357 … |
| block 131 (x 3, y 4) | `0x1AC2` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 135 (x 7, y 4) | `0x1B0D` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 137 (x 9, y 4) | `0x1ABA` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 142 (x 14, y 4) | `0x1B1D` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 145 (x 17, y 4) | `0x15BB` | party steps in, wall clicked | sets the north wall of block 145 to type 1; sets the north wall of block 145 to type 2; sets the north wall of block 145 to type 3; sets the north wall of block 145 to type 4; sets the north wall of block 145 to type 5; sets the north wall of block 43 to type 0; sets the north wall of block 145 to type 6; places a monster of type slot 1 on block 92 in mode 3 … |
| block 151 (x 23, y 4) | `0x208A` | party steps in, wall clicked | sets the east wall of block 151 to type 0; sets the east wall of block 151 to type 1; requests engine global change, selector 0, operands 0, 151; plays music track 327; plays music track 299; sets game flag 379; plays a sound (ID 104); checks the north wall of block 145 … |
| block 152 (x 24, y 4) | `0x213F` | wall clicked | loads wall tiles YVEL2; sets the east wall of block 151 to type 1; requests engine global change, selector 0, operands 0, 150; clears game flag 358; clears game flag 357; plays music track ?; requests engine global change, selector 0, operands 0, 123; sets game flag 357 … |
| block 167 (x 7, y 5) | `0x1AF0` | wall clicked | plays chat/dialogue text ID 0x0093; plays chat/dialogue text ID 0x0091; checks the east wall of block 135 |
| block 232 (x 8, y 7) | `0x1A94` | wall clicked | plays chat/dialogue text ID 0x0093; plays chat/dialogue text ID 0x0091; checks the north wall of block 233 |
| block 233 (x 9, y 7) | `0x1AB2` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 241 (x 17, y 7) | `0x1B25` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 259 (x 3, y 8) | `0x1A8C` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 303 (x 15, y 9) | `0x117F` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 355 (x 3, y 11) | `0x123A` | party steps in, wall clicked | requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 355; plays chat/dialogue text ID 0x0094; plays music track 283; sets game flag 367; plays chat/dialogue text ID 0x0023; plays chat/dialogue text ID 0x0025; tests game flag 352 … |
| block 376 (x 24, y 11) | `0x0C0C` | wall clicked | places item 214 (Earth Vial) on block 440; gives item 214 (Earth Vial) if inventory placement succeeds; puts item 214 (Earth Vial) on an empty cursor; sets the north wall of block 416 to type 83; sets the north wall of block 416 to type 0; takes 500 crown(s); takes 50 crown(s); takes 20 crown(s) … |
| block 387 (x 3, y 12) | `0x12C3` | wall clicked | sets the north wall of block 416 to type 80; sets the north wall of block 416 to type 0; deletes the held item; gives ? crown(s); sets the south wall of block 387 to type ?; takes 225 crown(s); gives item 68 (Peregrin great bow) if inventory placement succeeds; puts item 68 (Peregrin great bow) on an empty cursor … |
| block 396 (x 12, y 12) | `0x10FB` | wall clicked | puts item 161 (Silent sandals) on an empty cursor; puts item 262 (Bezel Cup) on an empty cursor |
| block 408 (x 24, y 12) | `0x0AF3` | party steps in, wall clicked | requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 408; plays chat/dialogue text ID 0x0094; plays music track 298; sets game flag 363; plays chat/dialogue text ID 0x0001; plays chat/dialogue text ID 0x0003; plays chat/dialogue text ID 0x000b … |
| block 425 (x 9, y 13) | `0x10F7` | party steps in, wall clicked | no action summarized |
| block 428 (x 12, y 13) | `0x1123` | bits 0x400 (no engine caller found) | no action summarized |
| block 459 (x 11, y 14) | `0x10F9` | party steps in, wall clicked | no action summarized |
| block 516 (x 4, y 16) | `0x1ACA` | wall clicked | plays chat/dialogue text ID 0x0093; plays chat/dialogue text ID 0x0091; checks the east wall of block 548 |
| block 521 (x 9, y 16) | `0x10F5` | party steps in, wall clicked | no action summarized |
| block 524 (x 12, y 16) | `0x116D` | bits 0x400 (no engine caller found) | no action summarized |
| block 548 (x 4, y 17) | `0x1AE8` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 554 (x 10, y 17) | `0x10ED` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 556 (x 12, y 17) | `0x1133` | wall clicked | puts item 248 (Oil Flask) on an empty cursor; gives 10 crown(s); puts item 100 (Granite rock) on an empty cursor; puts item 277 (Bracers) on an empty cursor |
| block 568 (x 24, y 17) | `0x096C` | party steps in, wall clicked | takes 100 crown(s); gives ? crown(s); heals character ? with amount or spell level ?; takes 50 crown(s); sets the north wall of block 416 to type 83; sets the north wall of block 416 to type 0; heals character 0 with amount or spell level ?; heals character 1 with amount or spell level ? … |
| block 643 (x 3, y 20) | `0x1B15` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 657 (x 17, y 20) | `0x0E90` | party steps in, wall clicked | requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 657; plays chat/dialogue text ID 0x0094; plays music track 255; sets game flag 366; plays chat/dialogue text ID 0x0018; tests game flag 352; checks the north wall of block 145 … |
| block 658 (x 18, y 20) | `0x0F5D` | wall clicked | sets the north wall of block 416 to type 86; sets the north wall of block 416 to type 0; deletes the held item; gives ? crown(s); takes 325 crown(s); gives item 57 (Great axe "Brimstone") if inventory placement succeeds; puts item 57 (Great axe "Brimstone") on an empty cursor; takes 550 crown(s) … |
| block 697 (x 25, y 21) | `0x1187` | party steps in, wall clicked | sets the west wall of block 697 to type 37; plays chat/dialogue text ID 0x001f; sets game flag 354; plays chat/dialogue text ID 0x0020; sets game flag 355; sets game flag 585; plays chat/dialogue text ID 0x0021; tests game flag 354 … |
| block 793 (x 25, y 24) | `0x1B2D` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 907 (x 11, y 28) | `0x0962` | party steps in, wall clicked | no action summarized |
| block 913 (x 17, y 28) | `0x0964` | party steps in, wall clicked | sets game flag 585; tests game flag 357 |
| block 1003 (x 11, y 31) | `0x0927` | party steps in, wall clicked | moves the party to level 24, block 674, facing 2; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 971; requests engine global change, selector 10, operands 0, 0; plays a sound (ID 109) |
| `0x400` level loaded | `0x0719` | — | sets script timer 0 to 1800 ticks; sets music theme ?; tests game flag 352 |
| `0x401` script timer 0 | `0x0923` | — | tests game flag 352 |
| `0x404` a monster died | `0x0737` | — | sets the north wall of block 43 to type ?; sets the south wall of block 145 to type 46; sets the north wall of block 145 to type 7; places a monster of type slot ? on block ? in mode ?; places a monster of type slot 1 on block 76 in mode 4; places a monster of type slot 2 on block 52 in mode 4; places a monster of type slot 1 on block 217 in mode 4; places a monster of type slot 2 on block 474 in mode 4 … |

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
