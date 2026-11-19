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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL26.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x002C` | — | loads wall tiles RUIN; sets all four walls of block 834 to type 37; sets all four walls of block 414 to type 37; loads monster sprites KNOWLES.SHP into slot 0; defines monster type 1; loads monster sprites XEOB.SHP into slot 1; defines monster type 2; loads monster sprites XEOB.SHP into slot 0 … |
| INI entry 1 (runs when the level loads) | `0x017F` | — | places a monster of type slot 1 on block 122 in mode 3; places a monster of type slot 1 on block 346 in mode 3; places a monster of type slot 1 on block 371 in mode 3; places a monster of type slot 1 on block 823 in mode 3; places a monster of type slot 1 on block 815 in mode 3; places a monster of type slot 1 on block 868 in mode 3; places a monster of type slot 1 on block 630 in mode 3; places a monster of type slot 1 on block 726 in mode 3 … |

### LEVEL26.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 46 (x 14, y 1) | `0x10CE` | wall clicked | toggles all four walls of block 77 between types 0 and 1; plays a sound (ID 38) |
| block 58 (x 26, y 1) | `0x0B11` | bits 0x400 (no engine caller found) | sets game flag 414; checks the south wall of block 224; tests game flag 414 |
| block 59 (x 27, y 1) | `0x0AD2` | wall clicked | puts item 130 (Dwarvish boots) on an empty cursor; puts item 157 (Galenian plate mail) on an empty cursor; sets game flag 414; checks the south wall of block 224; tests game flag 414 |
| block 109 (x 13, y 3) | `0x078C` | wall clicked | puts item 278 (Steel Bracers) on an empty cursor; puts item 271 (Ace of Dominion) on an empty cursor; puts item 269 (Guardian) on an empty cursor |
| block 131 (x 3, y 4) | `0x0785` | wall clicked | plays chat/dialogue text ID 0x0021 |
| block 134 (x 6, y 4) | `0x0A31` | party arrives (second path) | creates item type 11 and returns its handle; launches a projectile from block 132 in direction 1; plays a sound (ID 69) at block 132 |
| block 141 (x 13, y 4) | `0x07C9` | bits 0x400 (no engine caller found) | no action summarized |
| block 251 (x 27, y 7) | `0x06B7` | party arrives (second path) | sets all four walls of block 252 to type 1; sets the east wall of block 252 to type 40; checks the east wall of block 252; plays a sound (ID 38) |
| block 252 (x 28, y 7) | `0x06AC` | wall clicked | sets all four walls of block 252 to type 0; plays a sound (ID 38) |
| block 253 (x 29, y 7) | `0x10A6` | party arrives (second path) | places item 180 (Xeob Key) on block 835; places item 181 (Knowle Key) on block 380; sets game flag 415; tests game flag 415 |
| block 254 (x 30, y 7) | `0x069E` | party steps in, party arrives (second path), item put down | moves items from block 254 to level 24, block 395 |
| block 265 (x 9, y 8) | `0x10D9` | party arrives (second path) | creates item type 11 and returns its handle; launches a projectile from block 329 in direction 0; plays a sound (ID 18) at block 329 |
| block 334 (x 14, y 10) | `0x06D2` | wall clicked | puts item 126 (Trident "Mandible") on an empty cursor; gives 50 crown(s); puts item 158 (Dwarvish plate mail) on an empty cursor; puts item 215 (Bannon's reserve) on an empty cursor; sets game flag 409; checks the south wall of block 32; tests game flag 409 |
| block 335 (x 15, y 10) | `0x072D` | bits 0x400 (no engine caller found) | sets game flag 409; checks the south wall of block 32; tests game flag 409 |
| block 382 (x 30, y 11) | `0x0FC1` | party arrives (second path), wall clicked | plays chat/dialogue text ID 0x0015; sets game flag 423; requests engine global change, selector 0, operands 0, 446; requests engine global change, selector 1, operands 0, 2; plays music track 306; plays chat/dialogue text ID 0x000f; plays chat/dialogue text ID 0x0011; plays chat/dialogue text ID 0x0012 … |
| block 414 (x 30, y 12) | `0x0DEF` | party arrives (second path), bits 0x4000 (no engine caller found) | places a monster of type slot 2 on block 382 in mode 7; places a monster of type slot 2 on block 381 in mode 7; places a monster of type slot 2 on block 413 in mode 7; sets all four walls of block 414 to type 0; places item 264 (Vaelan's Cube) on block 414; places item 181 (Knowle Key) on block 414; places item 114 (Death Stick) on block 414; heals character 0 with amount or spell level ? … |
| block 469 (x 21, y 14) | `0x09F3` | party steps in, party arrives (second path), item put down | moves items from block 469 to level 27, block 437 |
| block 479 (x 31, y 14) | `0x0A5D` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 525 (x 13, y 16) | `0x0816` | bits 0x400 (no engine caller found) | sets game flag 410; checks the south wall of block 96; tests game flag 410 |
| block 526 (x 14, y 16) | `0x07D8` | wall clicked | puts item 216 (Salve) on an empty cursor; puts item 221 (Diamond) on an empty cursor; sets game flag 410; checks the south wall of block 96; tests game flag 410 |
| block 566 (x 22, y 17) | `0x09CB` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 591 (x 15, y 18) | `0x083C` | wall clicked | plays a sound (ID 29) |
| block 592 (x 16, y 18) | `0x0841` | party arrives (second path) | sets all four walls of block 623 to type 1; checks the north wall of block 623; plays a sound (ID 38) |
| block 599 (x 23, y 18) | `0x0A01` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 615 (x 7, y 19) | `0x094F` | wall clicked | plays chat/dialogue text ID 0x0021 |
| block 619 (x 11, y 19) | `0x0924` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 619 to type 28; creates item type 9 and returns its handle; launches a projectile from block 616 in direction 1; checks the south wall of block 619; plays a sound (ID 80); plays a sound (ID 69) at block 615 |
| block 622 (x 14, y 19) | `0x08E9` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 622 to type 28; sets all four walls of block 623 to type 0; creates item type 9 and returns its handle; launches a projectile from block 616 in direction 1; checks the south wall of block 622; plays a sound (ID 80); checks the north wall of block 623; plays a sound (ID 69) at block 615 |
| block 624 (x 16, y 19) | `0x08C1` | bits 0x400 (no engine caller found) | sets game flag 411; checks the south wall of block 128; tests game flag 411 |
| block 625 (x 17, y 19) | `0x0856` | wall clicked | sets all four walls of block 623 to type 0; operates the door switch at block 592 with action 0; checks the north wall of block 623; checks the north wall of block 592; checks the north wall of block 591; plays a sound (ID 38) |
| block 626 (x 18, y 19) | `0x099C` | bits 0x400 (no engine caller found) | removes monsters from block 626; sets game flag 412; moves items from block 626 to level 26, block 503; checks the south wall of block 160; tests game flag 412; plays a sound (ID 73) |
| block 628 (x 20, y 19) | `0x1135` | party steps in, party arrives (second path), item put down | removes monsters from block 628; moves items from block 628 to level 26, block 535; plays a sound (ID 73) |
| block 656 (x 16, y 20) | `0x0882` | wall clicked | puts item 34 (Axe "Butcher") on an empty cursor; puts item 248 (Oil Flask) on an empty cursor; sets game flag 411; checks the south wall of block 128; tests game flag 411 |
| block 658 (x 18, y 20) | `0x0956` | wall clicked | removes monsters from block 658; puts item 42 (Crossbow "Elayna") on an empty cursor; puts item 142 (Great helm "Nestor") on an empty cursor; sets game flag 412; moves items from block 658 to level 26, block 503; checks the south wall of block 160; tests game flag 412; plays a sound (ID 73) |
| block 691 (x 19, y 21) | `0x0A1B` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 696 (x 24, y 21) | `0x0A0E` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 734 (x 30, y 22) | `0x1117` | party arrives (second path), item put down | moves the party to level 23, block 857, facing ?; moves items from block 734 to level 23, block 857; plays a sound (ID 73) |
| block 754 (x 18, y 23) | `0x0A28` | party steps in, party arrives (second path), item put down | removes monsters from block 754; moves items from block 754 to level 26, block 565; plays a sound (ID 73) |
| block 773 (x 5, y 24) | `0x10F8` | party arrives (second path) | creates item type 10 and returns its handle; launches a projectile from block 901 in direction 0; plays a sound (ID 18) at block 901 |
| block 786 (x 18, y 24) | `0x0753` | wall clicked | toggles all four walls of block 817 between types 0 and 1; toggles the north wall of block 850 between types 31 and 1; plays a sound (ID 38) |
| block 812 (x 12, y 25) | `0x0775` | wall clicked | toggles the west wall of block 814 between types 31 and 1 |
| block 834 (x 2, y 26) | `0x0B4F` | party arrives (second path), bits 0x4000 (no engine caller found) | sets all four walls of block 834 to type 0; places a monster of type slot 2 on block 835 in mode 7; places a monster of type slot 2 on block 834 in mode 7; places item 264 (Vaelan's Cube) on block 834; places item 180 (Xeob Key) on block 834; places item 74 (Great sword "Justice") on block 834; heals character 0 with amount or spell level ?; heals character 1 with amount or spell level ? … |
| block 835 (x 3, y 26) | `0x0D04` | party steps in, wall clicked | shows text ID 0x403f; requests engine global change, selector 0, operands 0, 834; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 1, operands 0, 2; plays music track 306; plays chat/dialogue text ID 0x0004; plays chat/dialogue text ID 0x0006; plays chat/dialogue text ID 0x0007 … |
| block 850 (x 18, y 26) | `0x0766` | item put down | moves items from block 850 to level 28, block 820; plays a sound (ID 73) |
| block 867 (x 3, y 27) | `0x0A50` | wall clicked | plays chat/dialogue text ID 0x0019 |
| block 896 (x 0, y 28) | `0x0A6A` | wall clicked | puts item 150 (George's kite shield) on an empty cursor; puts item 136 (Chain mail "Protector") on an empty cursor; sets game flag 413; checks the south wall of block 192; tests game flag 413 |
| block 897 (x 1, y 28) | `0x0AAA` | bits 0x400 (no engine caller found) | sets game flag 413; checks the south wall of block 192; tests game flag 413 |
| block 933 (x 5, y 29) | `0x077E` | wall clicked | plays chat/dialogue text ID 0x0021 |
| `0x400` level loaded | `0x061D` | — | drops the party through a pit; clears game flag 46; sets music theme 306; sets script timer 0 to 7200 ticks; tests game flag 46 |
| `0x401` script timer 0 | `0x0638` | — | places a monster of type slot 1 on block 984 in mode 7; places a monster of type slot 1 on block 82 in mode 7; sets the north wall of block 0 to type ?; checks the north wall of block 0 |

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
