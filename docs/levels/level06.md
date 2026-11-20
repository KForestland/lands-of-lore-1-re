# Level 6

Made by `tools/level_report.py` from `LEVEL6.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 6](../PROGRESSION.md#level-6) and [item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 382 | — | — |  | 0x80 | 63 |
| 1 | 1832 | 1 | — |  | 0x07 | 255 |
| 2 | 1836 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 24 | 4 | 5 | — |  | 0x04 | 26 |
| 35 | 8 | — | 20 |  | 0x80 | 10 |
| 38 | 12 | — | 19 |  | 0x84 | 11 |
| 41 | 2 | 1 | 45 |  | 0x07 | 255 |
| 42 | 1 | 2 | 70 | 2 lever (to on) | 0x07 | 207 |
| 54 | 1 | 1 | 29 | 2 lever (to on) | 0x07 | 207 |
| 56 | 1 | 1 | 31 | 2 lever (to on) | 0x07 | 207 |
| 58 | 1 | 1 | 27 | 2 lever (to on) | 0x07 | 207 |
| 63 | 2 | 1 | 40 | 1 clickable wall | 0x07 | 255 |
| 65 | 1 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 74 | 4 | — | 55 |  | 0x84 | 63 |
| 75 | 2 | 1 | 61 | 2 lever (to on) | 0x07 | 207 |
| 77 | 2 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 1 | 1 | 60 | 1 clickable wall | 0x07 | 255 |
| 79 | 2 | 2 | 64 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 108 (x 12, y 3) | west | 65 | clickable wall |
| 141 (x 13, y 4) | south | 75 | lever (to on) |
| 145 (x 17, y 4) | south | 78 | clickable wall |
| 200 (x 8, y 6) | west | 79 | clickable wall |
| 206 (x 14, y 6) | north | 77 | clickable wall |
| 212 (x 20, y 6) | north | 77 | clickable wall |
| 256 (x 0, y 8) | east | 58 | lever (to on) |
| 258 (x 2, y 8) | west | 56 | lever (to on) |
| 261 (x 5, y 8) | north | 79 | clickable wall |
| 264 (x 8, y 8) | north | 63 | clickable wall |
| 289 (x 1, y 9) | north | 54 | lever (to on) |
| 453 (x 5, y 14) | west | 75 | lever (to on) |
| 458 (x 10, y 14) | south | 42 | lever (to on) |
| 459 (x 11, y 14) | north | 63 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL6.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CAVE1; loads monster sprites BANDIT.SHP into slot 0; loads monster sprites RATMAN.SHP into slot 1; defines monster type 1; defines monster type 3 |
| INI entry 1 (runs when the level loads) | `0x00A6` | — | places a monster of type slot 1 on block 229 in mode 3; places a monster of type slot 1 on block 198 in mode 3; places a monster of type slot 3 on block 235 in mode 3; places a monster of type slot 3 on block 267 in mode 3; places a monster of type slot 3 on block 233 in mode 3; places a monster of type slot 3 on block 425 in mode 3; places a monster of type slot 3 on block 427 in mode 3; places a monster of type slot 3 on block 426 in mode 3 … |

### LEVEL6.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 103 (x 7, y 3) | `0x04E9` | party arrives (second path) | sets game flag 124; plays chat/dialogue text ID 0x000a; tests game flag 124 |
| block 104 (x 8, y 3) | `0x050B` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 104 to type 36; creates item type 5 and returns its handle; launches a projectile from block 107 in direction 3; checks the south wall of block 104; plays a sound (ID 80); plays a sound (ID 133) |
| block 108 (x 12, y 3) | `0x054E` | wall clicked | plays chat/dialogue text ID 0x0015 |
| block 118 (x 22, y 3) | `0x0633` | party steps in, party arrives (second path), item put down | moves items from block 118 to level 7, block 86 |
| block 129 (x 1, y 4) | `0x045D` | party arrives (second path) | clears game flag 64 |
| block 132 (x 4, y 4) | `0x04BF` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 132 to type 36; operates the door switch at block 165 with action 1; operates the door switch at block 165 with action -1; plays chat/dialogue text ID 0x0008; sets game flag 128; checks the south wall of block 132; plays a sound (ID 80); tests game flag 128 |
| block 133 (x 5, y 4) | `0x0427` | party arrives (second path), bits 0x10 (no engine caller found) | sets all four walls of block 132 to type 36; sets monster 0 mode to 7; sets monster 1 mode to 7; sets game flag 129; plays chat/dialogue text ID 0x0009; tests game flag 129; checks the south wall of block 132; plays a sound (ID 80) |
| block 141 (x 13, y 4) | `0x0604` | wall clicked | sets all four walls of block 203 to type 1; sets all four walls of block 170 to type 2; sets all four walls of block 172 to type 0; sets all four walls of block 162 to type 0; sets all four walls of block 163 to type 0; sets all four walls of block 194 to type 0; sets all four walls of block 195 to type 0; plays a sound (ID 38) |
| block 161 (x 1, y 5) | `0x0463` | party arrives (second path) | sets all four walls of block 194 to type 0; sets all four walls of block 194 to type 38; removes monsters from block 194; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 194, facing ?; sets all four walls of block 162 to type 0; sets all four walls of block 162 to type 38 … |
| block 162 (x 2, y 5) | `0x03FF` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 162, facing ?; removes monsters from block 162; sets game flag 46; moves items from block 162 to level 7, block 162; checks the north wall of block 162 |
| block 163 (x 3, y 5) | `0x0413` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 163, facing ?; removes monsters from block 163; sets game flag 46; moves items from block 163 to level 7, block 163; checks the north wall of block 163 |
| block 194 (x 2, y 6) | `0x0409` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 194, facing ?; removes monsters from block 194; sets game flag 46; moves items from block 194 to level 7, block 194; checks the north wall of block 194 |
| block 195 (x 3, y 6) | `0x041D` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 195, facing ?; removes monsters from block 195; sets game flag 46; moves items from block 195 to level 7, block 195; checks the north wall of block 195 |
| block 200 (x 8, y 6) | `0x0670` | wall clicked | plays chat/dialogue text ID 0x001d |
| block 225 (x 1, y 7) | `0x03F5` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 225, facing ?; removes monsters from block 225; sets game flag 46; moves items from block 225 to level 7, block 225; checks the north wall of block 225 |
| block 232 (x 8, y 7) | `0x0561` | party arrives (second path), bits 0x410 (no engine caller found) | sets the north wall of block 264 to type 64; plays chat/dialogue text ID 0x000c; plays chat/dialogue text ID 0x000d; sets script global 13 to ?; plays chat/dialogue text ID 0x000b; sets game flag 121; checks the north wall of block 264; plays a sound (ID 135) … |
| block 256 (x 0, y 8) | `0x0388` | wall clicked | sets all four walls of block 194 to type 0; sets all four walls of block 194 to type 38; removes monsters from block 194; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 194, facing ?; sets all four walls of block 225 to type 0; sets all four walls of block 225 to type 38 … |
| block 258 (x 2, y 8) | `0x03BA` | party steps in, party arrives (second path), wall clicked, item put down | sets all four walls of block 163 to type 0; sets all four walls of block 163 to type 38; removes monsters from block 163; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 163, facing ?; sets all four walls of block 195 to type 0; sets all four walls of block 195 to type 38 … |
| block 259 (x 3, y 8) | `0x0457` | party arrives (second path) | sets game flag 64 |
| block 261 (x 5, y 8) | `0x0669` | wall clicked | plays chat/dialogue text ID 0x001d |
| block 289 (x 1, y 9) | `0x03A1` | wall clicked | sets all four walls of block 162 to type 0; sets all four walls of block 162 to type 38; removes monsters from block 162; drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 162, facing ?; sets all four walls of block 194 to type 0; sets all four walls of block 194 to type 38 … |
| block 290 (x 2, y 9) | `0x063E` | party arrives (second path) | sets game flag 164; plays chat/dialogue text ID 0x0002; tests game flag 125; tests game flag 164 |
| block 390 (x 6, y 12) | `0x036E` | party arrives (second path) | shows text ID 0x403f; requests engine global change, selector 0, operands 0, 422; tests game flag 127 |
| block 422 (x 6, y 13) | `0x0350` | party arrives (second path), bits 0x10 (no engine caller found) | plays chat/dialogue text ID 0x0006; sets monster 10 mode to 7; sets game flag 127; tests game flag 127 |
| block 427 (x 11, y 13) | `0x059B` | party arrives (second path), bits 0x410 (no engine caller found) | sets the north wall of block 459 to type 63; sets the north wall of block 459 to type 64; plays chat/dialogue text ID 0x000f; plays chat/dialogue text ID 0x0010; plays chat/dialogue text ID 0x0011; sets script global 14 to ?; plays chat/dialogue text ID 0x000e; sets game flag 122 … |
| block 449 (x 1, y 14) | `0x029B` | party arrives (second path) | plays chat/dialogue text ID 0x0000; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0001; sets game flag 120; tests game flag 120 |
| block 452 (x 4, y 14) | `0x0317` | party arrives (second path), bits 0x10 (no engine caller found) | plays chat/dialogue text ID 0x0004; sets game flag 137; tests game flag 137 |
| block 453 (x 5, y 14) | `0x0332` | wall clicked | toggles all four walls of block 422 between types 0 and 2; plays chat/dialogue text ID 0x0003; sets game flag 126; tests game flag 126; plays a sound (ID 38) |
| block 455 (x 7, y 14) | `0x05FA` | party arrives (second path), item put down | drops the party through a pit; deals damage to the party (amount ?); moves the party to level 7, block 455, facing ?; removes monsters from block 455; sets game flag 46; moves items from block 455 to level 7, block 455; checks the north wall of block 455 |
| block 458 (x 10, y 14) | `0x05D5` | wall clicked | toggles all four walls of block 487 between types 0 and 1; toggles all four walls of block 486 between types 0 and 1; plays chat/dialogue text ID 0x0012; sets game flag 123; plays a sound (ID 38); tests game flag 123 |
| block 481 (x 1, y 15) | `0x02C9` | party steps in, party arrives (second path), item put down | moves the party to level 2, block 45, facing 2; moves items from block 481 to level 2, block 45; requests engine global change, selector 10, operands 0, 0; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 449; requests engine global change, selector 10, operands 0, 2 |
| `0x400` level loaded | `0x0267` | — | sets the south wall of block 258 to type 70; sets script timer 0 to 3600 ticks; sets music theme 272; tests game flag 125 |
| `0x401` script timer 0 | `0x027F` | — | places a monster of type slot 3 on block 262 in mode 4 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 247 | Broken glass | 6 | 167 |
| INI entry 1 (runs when the level loads) | 245 | Lockpicks | 6 | 168 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 6 | 168 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 168 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 6 | 296 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 296 |
| INI entry 1 (runs when the level loads) | 218 | Ginseng | 6 | 296 |
| INI entry 1 (runs when the level loads) | 249 | Lantern | 6 | 483 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 229 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 229 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 198 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 198 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 235 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 267 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 233 | 1 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 425 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 427 | 3 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 426 | 0 | 3 | 3 |
| INI entry 1 (runs when the level loads) | 358 | 2 | 3 | 3 |
| `0x401` script timer 0 | 262 | 2 | 3 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 1, y 15 | 0 | x 1, y 14 | 0x41de | FOREST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL06.<lang>`: 22 ids: 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 29.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL06.ENG --index N`.
