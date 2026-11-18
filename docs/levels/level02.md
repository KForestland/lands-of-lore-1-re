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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and marks effects inferred from ScummVM **UNCONFIRMED** for DOS where applicable.

### LEVEL2.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0026` | — | loads wall tiles FOREST1; loads monster sprites BOAR.SHP into slot 0; loads monster sprites ORC.SHP into slot 1; defines monster type 3; loads monster sprites THUG.SHP into slot 1; defines monster type 1; defines monster type 4; defines monster type 2 … |
| INI entry 1 (runs when the level loads) | `0x0145` | — | places a monster of type slot 1 on block 228 in mode 2; places a monster of type slot 1 on block 165 in mode 2; places a monster of type slot 1 on block 97 in mode 2; places a monster of type slot 2 on block 69 in mode 3; places item 121 (Stick) on block 69; places item 99 (Rock) on block 172; places item 99 (Rock) on block 228; places item 43 (Weathered dagger) on block 136 … |

### LEVEL2.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 13 (x 13, y 0) | `0x08BE` | party steps in, party arrives (second path), wall clicked, item put down | moves the party to level 6, block 449, facing 0; moves items from block 13 to level 6, block 449; requests engine global change, selector 10, operands 0, 2 |
| block 45 (x 13, y 1) | `0x049E` | party arrives (second path), bits 0x10 (no engine caller found) | sets the south wall of block 13 to type 63; starts a dialogue sequence in mode 0; plays chat/dialogue text ID 0x0059; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0061; sets game flag 136; tests game flag 67 … |
| block 70 (x 6, y 2) | `0x0DCF` | wall clicked | plays chat/dialogue text ID 0x001c |
| block 71 (x 7, y 2) | `0x0DE9` | wall clicked | plays chat/dialogue text ID 0x003b; tests game flag 191 |
| block 74 (x 10, y 2) | `0x0507` | party steps in, wall clicked | requests engine global change, selector 10, operands 0, 0; plays chat/dialogue text ID 0x0055; plays chat/dialogue text ID 0x0000; plays chat/dialogue text ID 0x005f; plays chat/dialogue text ID 0x005e; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 106; tests game flag 41 … |
| block 76 (x 12, y 2) | `0x0DAC` | wall clicked | plays chat/dialogue text ID 0x0039 |
| block 77 (x 13, y 2) | `0x0414` | item taken | no action summarized |
| block 96 (x 0, y 3) | `0x0D5D` | party steps in, party arrives (second path), wall clicked, item put down | moves the party to level 5, block 260, facing 3; moves items from block 96 to level 5, block 260; requests engine global change, selector 0, operands 0, 97; shows text ID 0x403f; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 10, operands 0, 2 |
| block 98 (x 2, y 3) | `0x0D3D` | party steps in | requests engine global change, selector 0, operands 0, 99; requests engine global change, selector 10, operands 0, 0; shows text ID 0x403f; tests game flag 35 |
| block 99 (x 3, y 3) | `0x0BF3` | party steps in, bits 0x4000 (no engine caller found) | moves the party to level 5, block 260, facing 3; places a monster of type slot 1 on block 97 in mode 7; requests engine global change, selector 10, operands 0, 0; plays chat/dialogue text ID 0x0038; sets up 3 dialogue choices; reads the dialogue result; requests engine global change, selector 1, operands 0, 2; sets game flag 35 … |
| block 104 (x 8, y 3) | `0x0DC8` | wall clicked | plays chat/dialogue text ID 0x0028 |
| block 106 (x 10, y 3) | `0x0560` | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; plays chat/dialogue text ID 0x002c; plays chat/dialogue text ID 0x0053; requests engine global change, selector 10, operands 0, 0; tests game flag 67; tests game flag 41 |
| block 109 (x 13, y 3) | `0x0418` | item taken | no action summarized |
| block 132 (x 4, y 4) | `0x0DD6` | wall clicked | plays chat/dialogue text ID 0x0029 |
| block 136 (x 8, y 4) | `0x083E` | item taken | clears game flag 187; tests game flag 187 |
| block 138 (x 10, y 4) | `0x041C` | party arrives (second path) | starts a dialogue sequence in mode 0; plays chat/dialogue text ID 0x0055; sets up 1 dialogue choices; reads the dialogue result; plays chat/dialogue text ID 0x0065; plays chat/dialogue text ID 0x0057; sets game flag 134; tests game flag 67 … |
| block 141 (x 13, y 4) | `0x0DF5` | party arrives (second path) | loads cut-scene TIM1.TIM into slot 0; sets game flag 14; sets game flag 35; sets game flag 38; suspend monster; sets game flag 70; plays music track 270; starts a dialogue sequence in mode 0 … |
| block 166 (x 6, y 5) | `0x0834` | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; sets monster 1 facing to 1; plays music track 265; starts a dialogue sequence in mode 0; plays music track ?; tests game flag 14 |
| block 170 (x 10, y 5) | `0x0468` | party arrives (second path) | starts a dialogue sequence in mode 0; plays chat/dialogue text ID 0x0058; sets up 1 dialogue choices; reads the dialogue result; sets game flag 135; tests game flag 67; tests game flag 41; tests game flag 135 |
| block 176 (x 16, y 5) | `0x0DB3` | wall clicked | plays chat/dialogue text ID 0x0039 |
| block 193 (x 1, y 6) | `0x0DBA` | wall clicked | plays chat/dialogue text ID 0x0039 |
| block 227 (x 3, y 7) | `0x05E4` | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; sets monster 0 facing to 3; plays music track 265; starts a dialogue sequence in mode 0; plays music track ?; tests game flag 14 |
| block 232 (x 8, y 7) | `0x0870` | party arrives (second path), bits 0x10 (no engine caller found) | loads cut-scene SCOTIA1.TIM into slot 0; sets game flag 15; plays music track 263; plays music track ?; tests game flag 15; tests game flag 67 |
| block 239 (x 15, y 7) | `0x0DDD` | wall clicked | plays chat/dialogue text ID 0x003b; tests game flag 190 |
| block 260 (x 4, y 8) | `0x05DA` | party arrives (second path), bits 0x10 (no engine caller found) | suspend monster; sets game flag 14; sets monster 0 facing to 2; plays music track 265; starts a dialogue sequence in mode 0; plays music track ?; tests game flag 14 |
| block 261 (x 5, y 8) | `0x0854` | wall clicked | gives 3 crown(s); plays chat/dialogue text ID 0x001d; clears game flag 188; plays chat/dialogue text ID 0x001c; tests game flag 188 |
| block 264 (x 8, y 8) | `0x08A4` | party arrives (second path) | requests engine global change, selector 0, operands 0, 232; shows text ID 0x403f; tests game flag 15 |
| block 268 (x 12, y 8) | `0x08EC` | party arrives (second path) | loads cut-scene VICTOR7.TIM into slot 0; loads cut-scene VICTOR6.TIM into slot 0; loads cut-scene VICTOR5.TIM into slot 0; places item 81 (Long sword) on block 301; gives item 81 (Long sword) if inventory placement succeeds; puts item 81 (Long sword) on an empty cursor; places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713, facing 0 … |
| block 270 (x 14, y 8) | `0x0DC1` | wall clicked | plays chat/dialogue text ID 0x0028 |
| block 300 (x 12, y 9) | `0x0AD9` | party steps in, party arrives (second path), party leaves, wall clicked, bits 0x4000 (no engine caller found) | loads cut-scene VICTOR6.TIM into slot 0; loads cut-scene VICTOR7.TIM into slot 0; loads cut-scene VICTOR5.TIM into slot 0; places item 81 (Long sword) on block 301; gives item 81 (Long sword) if inventory placement succeeds; puts item 81 (Long sword) on an empty cursor; places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713, facing 0 … |
| block 301 (x 13, y 9) | `0x0BA9` | party steps in, wall clicked | loads cut-scene VICTOR5.TIM into slot 0; places item 81 (Long sword) on block 301; gives item 81 (Long sword) if inventory placement succeeds; puts item 81 (Long sword) on an empty cursor; places item 241 (Riddle Scroll) on block 301; moves the party to level 10, block 713, facing 0; loads cut-scene VICTOR7.TIM into slot 0; loads cut-scene VICTOR6.TIM into slot 0 … |
| block 328 (x 8, y 10) | `0x05EE` | party steps in, party arrives (second path), party leaves, bits 0x4000 (no engine caller found) | requests engine global change, selector 10, operands 0, 2; requests engine global change, selector 10, operands 0, 0; tests game flag 67 |
| block 360 (x 8, y 11) | `0x063B` | party steps in, wall clicked | loads cut-scene LYNN1.TIM into slot 0; loads cut-scene LYNN2.TIM into slot 0; loads cut-scene LYNN3.TIM into slot 1; plays chat/dialogue text ID 0x005c; shows text ID 0x403f; requests engine global change, selector 0, operands 0, 328; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 360 … |
| block 392 (x 8, y 12) | `0x06A4` | wall clicked | deletes the held item; loads cut-scene BOAT.TIM into slot 0; moves the party to level 3, block 526, facing 2; sets game flag 25; plays chat/dialogue text ID 0x0012; plays music track 257; plays chat/dialogue text ID 0x0015; plays chat/dialogue text ID 0x0014 … |
| `0x400` level loaded | `0x037D` | — | places a monster of type slot 3 on block 109 in mode 3; suspend monster; creates item type ? and returns its handle; give item to monster; creates item type 216 and returns its handle; creates item type 243 and returns its handle; sets game flag 44; sets script timer 0 to 14400 ticks … |
| `0x401` script timer 0 | `0x03FD` | — | places a monster of type slot 2 on block 136 in mode 7 |

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
