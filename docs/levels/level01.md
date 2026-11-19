# Level 1

Made by `tools/level_report.py` from `LEVEL1.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

[Item, spell and creature numbers](../NUMBERS.md).

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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL1.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x001B` | — | loads wall tiles KEEP; loads monster sprites GUARD.SHP into slot 0; defines monster type 1; tests game flag 39 |
| INI entry 1 (runs when the level loads) | `0x009F` | — | places a monster of type slot 1 on block 589 in mode 1; places a monster of type slot 1 on block 525 in mode 1; places a monster of type slot 1 on block 271 in mode 1; creates item type 75 and returns its handle; give item to monster; requests engine global change, selector 0, operands 0, 557; requests engine global change, selector 1, operands 0, 0; sets script global 5 to ? … |

### LEVEL1.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 201 (x 9, y 6) | `0x1146` | wall clicked | plays chat/dialogue text ID 0x0031; sets game flag 90; plays chat/dialogue text ID 0x0032; clears game flag 90; tests game flag 39; tests game flag 90 |
| block 202 (x 10, y 6) | `0x11C4` | wall clicked | plays chat/dialogue text ID 0x003f; sets game flag 104; plays chat/dialogue text ID 0x0040; clears game flag 104; tests game flag 39; tests game flag 104 |
| block 237 (x 13, y 7) | `0x1158` | wall clicked | plays chat/dialogue text ID 0x0031; sets game flag 92; plays chat/dialogue text ID 0x0032; clears game flag 92; tests game flag 39; tests game flag 92 |
| block 238 (x 14, y 7) | `0x1197` | wall clicked | plays chat/dialogue text ID 0x003b; sets game flag 99; plays chat/dialogue text ID 0x003c; clears game flag 99; tests game flag 39; tests game flag 99 |
| block 264 (x 8, y 8) | `0x114F` | wall clicked | plays chat/dialogue text ID 0x0033; sets game flag 91; plays chat/dialogue text ID 0x0034; clears game flag 91; tests game flag 39; tests game flag 91 |
| block 269 (x 13, y 8) | `0x0491` | party arrives (second path) | clears game flag 23; move monster; tests game flag 23 |
| block 270 (x 14, y 8) | `0x04B0` | party arrives (second path), bits 0x10 (no engine caller found) | loads cut-scene GUARD1.TIM into slot 0; loads cut-scene GUARD2.TIM into slot 0; loads cut-scene GUARD6.TIM into slot 1; sets game flag 23; move monster; plays chat/dialogue text ID 0x008b; plays chat/dialogue text ID 0x008c; sets up 1 dialogue choices … |
| block 272 (x 16, y 8) | `0x05A4` | party arrives (second path) | sets game flag 23; move monster; tests game flag 23 |
| block 273 (x 17, y 8) | `0x05C4` | party steps in, wall clicked | loads cut-scene KING1.TIM into slot 0; loads cut-scene CONFRONT.TIM into slot 0; loads cut-scene TALAMSCA.TIM into slot 0; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 272; plays chat/dialogue text ID 0x0050; shows text ID 0x403f; sets game flag 4 … |
| block 274 (x 18, y 8) | `0x068B` | wall clicked | loads cut-scene DAWN1.TIM into slot 1; loads cut-scene WILL1.TIM into slot 1; a character leaves the party; a character joins the party; loads cut-scene SPELLBKE.TIM into slot 0; loads cut-scene SPELLBKF.TIM into slot 0; loads cut-scene SPELLBKG.TIM into slot 0; loads cut-scene NATE4.TIM into slot 1 … |
| block 300 (x 12, y 9) | `0x11A9` | wall clicked | plays chat/dialogue text ID 0x0039; sets game flag 101; plays chat/dialogue text ID 0x003a; clears game flag 101; tests game flag 39; tests game flag 101 |
| block 302 (x 14, y 9) | `0x11A0` | wall clicked | plays chat/dialogue text ID 0x003b; sets game flag 100; plays chat/dialogue text ID 0x003c; clears game flag 100; tests game flag 39; tests game flag 100 |
| block 327 (x 7, y 10) | `0x116A` | wall clicked | plays chat/dialogue text ID 0x0031; sets game flag 94; plays chat/dialogue text ID 0x0032; clears game flag 94; tests game flag 39; tests game flag 94 |
| block 328 (x 8, y 10) | `0x12A8` | wall clicked | starts a dialogue sequence in mode 0; plays chat/dialogue text ID ?; sets up 1 dialogue choices; sets script global 6 to ?; plays a sound (ID 105) |
| block 329 (x 9, y 10) | `0x11BB` | wall clicked | plays chat/dialogue text ID 0x003d; sets game flag 103; plays chat/dialogue text ID 0x003e; clears game flag 103; tests game flag 39; tests game flag 103 |
| block 334 (x 14, y 10) | `0x1161` | wall clicked | plays chat/dialogue text ID 0x0033; sets game flag 93; plays chat/dialogue text ID 0x0034; clears game flag 93; tests game flag 39; tests game flag 93 |
| block 358 (x 6, y 11) | `0x12B6` | wall clicked | starts a dialogue sequence in mode 0; plays chat/dialogue text ID ?; sets up 1 dialogue choices; sets script global 7 to ?; plays a sound (ID 105) |
| block 367 (x 15, y 11) | `0x11EF` | wall clicked | plays chat/dialogue text ID 0x0044; tests game flag 39 |
| block 390 (x 6, y 12) | `0x1173` | wall clicked | plays chat/dialogue text ID 0x0033; sets game flag 95; plays chat/dialogue text ID 0x0034; clears game flag 95; tests game flag 39; tests game flag 95 |
| block 393 (x 9, y 12) | `0x1231` | wall clicked | sets the west wall of block 393 to type 58; loads cut-scene AUTOMAP.TIM into slot 1; sets game flag 252; plays chat/dialogue text ID 0x004a; plays chat/dialogue text ID 0x0051; starts a dialogue sequence in mode 0; plays chat/dialogue text ID ?; sets up 1 dialogue choices … |
| block 394 (x 10, y 12) | `0x1227` | wall clicked | plays chat/dialogue text ID 0x004d |
| block 395 (x 11, y 12) | `0x11E8` | wall clicked | plays chat/dialogue text ID 0x0045; tests game flag 39 |
| block 397 (x 13, y 12) | `0x11FD` | wall clicked | deals damage to target 0 (amount 1); plays chat/dialogue text ID 0x002f; sets game flag 107; plays chat/dialogue text ID 0x0030; tests game flag 107 |
| block 400 (x 16, y 12) | `0x0B40` | party steps in, wall clicked | loads cut-scene DRVICTOR.TIM into slot 0; loads cut-scene VICTOR1.TIM into slot 0; loads cut-scene VICTOR2.TIM into slot 0; loads cut-scene VICTOR3.TIM into slot 1; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 399; plays chat/dialogue text ID 0x0050; requests engine global change, selector 0, operands 1, 399 … |
| block 401 (x 17, y 12) | `0x0C48` | wall clicked | gives ? crown(s); deletes the held item; takes 125 crown(s); puts item 81 (Long sword) on an empty cursor; takes 40 crown(s); puts item 90 (Mace) on an empty cursor; takes 60 crown(s); puts item 93 (Rapier) on an empty cursor … |
| block 423 (x 7, y 13) | `0x12C4` | wall clicked | starts a dialogue sequence in mode 0; plays chat/dialogue text ID ?; sets up 1 dialogue choices; sets script global 8 to ?; plays a sound (ID 105) |
| block 424 (x 8, y 13) | `0x117C` | wall clicked | plays chat/dialogue text ID 0x0031; sets game flag 96; plays chat/dialogue text ID 0x0032; clears game flag 96; tests game flag 39; tests game flag 96 |
| block 425 (x 9, y 13) | `0x0A79` | wall clicked | plays chat/dialogue text ID 0x0089; plays chat/dialogue text ID 0x0012; sets game flag 11; sets up 1 dialogue choices; requests engine global change, selector 0, operands 0, 427; plays music track 254; plays music track 250; plays chat/dialogue text ID 0x0054 … |
| block 426 (x 10, y 13) | `0x093E` | party steps in, wall clicked | loads cut-scene DRGERIM.TIM into slot 0; loads cut-scene GERIM1.TIM into slot 0; loads cut-scene GERIM2.TIM into slot 0; loads cut-scene GERIM3.TIM into slot 1; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 427; shows text ID 0x403f; plays chat/dialogue text ID 0x0050 … |
| block 429 (x 13, y 13) | `0x111D` | wall clicked | gives 1 crown(s); plays chat/dialogue text ID 0x002c; sets game flag 109; plays chat/dialogue text ID 0x002d; clears game flag 109; plays chat/dialogue text ID 0x002e; clears game flag 108; plays chat/dialogue text ID 0x0080 … |
| block 431 (x 15, y 13) | `0x11CD` | wall clicked | plays chat/dialogue text ID 0x0041; sets game flag 105; plays chat/dialogue text ID 0x0042; clears game flag 105; tests game flag 39; tests game flag 105 |
| block 459 (x 11, y 14) | `0x11B2` | wall clicked | plays chat/dialogue text ID 0x0035; sets game flag 102; plays chat/dialogue text ID 0x0036; clears game flag 102; tests game flag 39; tests game flag 102 |
| block 464 (x 16, y 14) | `0x0E95` | party steps in, wall clicked | loads cut-scene DRNATHAN.TIM into slot 0; loads cut-scene NATE1.TIM into slot 0; loads cut-scene NATE2.TIM into slot 0; loads cut-scene NATE3.TIM into slot 1; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 463; plays chat/dialogue text ID 0x0050; requests engine global change, selector 0, operands 1, 463 … |
| block 465 (x 17, y 14) | `0x0F84` | wall clicked | takes 20 crown(s); puts item 216 (Salve) on an empty cursor; takes 10 crown(s); puts item 218 (Ginseng) on an empty cursor; takes 5 crown(s); puts item 217 (Aloe) on an empty cursor; plays chat/dialogue text ID 0x001f; sets up 1 dialogue choices … |
| block 492 (x 12, y 15) | `0x11D6` | wall clicked | plays chat/dialogue text ID 0x0052; sets game flag 88; plays chat/dialogue text ID 0x0053; clears game flag 88; tests game flag 39; tests game flag 88 |
| block 494 (x 14, y 15) | `0x11DF` | wall clicked | plays chat/dialogue text ID 0x0052; sets game flag 89; plays chat/dialogue text ID 0x0053; clears game flag 89; tests game flag 39; tests game flag 89 |
| block 495 (x 15, y 15) | `0x11F6` | wall clicked | plays chat/dialogue text ID 0x0043; tests game flag 39 |
| block 526 (x 14, y 16) | `0x048F` | party arrives (second path) | no action summarized |
| block 527 (x 15, y 16) | `0x118E` | wall clicked | plays chat/dialogue text ID 0x0031; sets game flag 98; plays chat/dialogue text ID 0x0032; clears game flag 98; tests game flag 39; tests game flag 98 |
| block 555 (x 11, y 17) | `0x1185` | wall clicked | plays chat/dialogue text ID 0x0033; sets game flag 97; plays chat/dialogue text ID 0x0034; clears game flag 97; tests game flag 39; tests game flag 97 |
| block 557 (x 13, y 17) | `0x040B` | party arrives (second path), bits 0x10 (no engine caller found) | loads cut-scene GUARD6.TIM into slot 1; plays chat/dialogue text ID 0x0000; move monster; sets game flag 110; plays chat/dialogue text ID 0x0001; plays chat/dialogue text ID 0x004b; tests game flag 110; tests game flag 11 … |
| block 621 (x 13, y 19) | `0x12D2` | party steps in, wall clicked | moves the party to level 2, block 106, facing 2; requests engine global change, selector 10, operands 0, 0; requests engine global change, selector 0, operands 0, 589; plays chat/dialogue text ID 0x0050; shows text ID 0x403f; plays a sound (ID 109) |
| `0x400` level loaded | `0x03AD` | — | sets script global 0 to 0; sets script global 2 to 0; sets script global 1 to 0; sets monster 0 block to 557; sets monster 0 facing to 2; move monster; sets script timer 0 to 15 ticks; sets script timer 1 to 60 ticks … |
| `0x401` script timer 0 | `0x0400` | — | toggles all four walls of block 429 between types 68 and 69 |
| `0x402` script timer 1 | `0x0409` | — | no action summarized |

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
