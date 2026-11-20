# Level 9

Made by `tools/level_report.py` from `LEVEL9.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 9](../PROGRESSION.md#level-9) and [item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 3 = CAVE1 (decorations `CAVE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 344 | — | — |  | 0x80 | 63 |
| 1 | 1854 | 1 | — |  | 0x07 | 255 |
| 2 | 1850 | 2 | — |  | 0x07 | 255 |
| 23 | 8 | 4 | — |  | 0x04 | 25 |
| 27 | 1 | 1 | 49 | 2 lever (to on) | 0x07 | 207 |
| 29 | 1 | 2 | 51 | 1 clickable wall | 0x07 | 207 |
| 35 | 12 | — | 20 |  | 0x80 | 10 |
| 42 | 1 | 1 | 68 | 1 clickable wall | 0x07 | 207 |
| 53 | 2 | 1 | 26 | 1 clickable wall | 0x07 | 210 |
| 61 | 4 | 2 | 63 | 1 clickable wall | 0x07 | 255 |
| 62 | 4 | 1 | 39 | 1 clickable wall | 0x07 | 255 |
| 65 | 8 | 1 | 9 | 1 clickable wall | 0x07 | 255 |
| 77 | 3 | 1 | 59 | 1 clickable wall | 0x07 | 255 |
| 78 | 4 | 2 | 60 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 83 (x 19, y 2) | south | 65 | clickable wall |
| 86 (x 22, y 2) | south | 78 | clickable wall |
| 91 (x 27, y 2) | south | 77 | clickable wall |
| 158 (x 30, y 4) | west | 65 | clickable wall |
| 178 (x 18, y 5) | east | 78 | clickable wall |
| 181 (x 21, y 5) | east | 77 | clickable wall |
| 185 (x 25, y 5) | west | 78 | clickable wall |
| 219 (x 27, y 6) | east | 29 | clickable wall |
| 242 (x 18, y 7) | east | 65 | clickable wall |
| 248 (x 24, y 7) | north | 78 | clickable wall |
| 248 (x 24, y 7) | south | 61 | clickable wall |
| 252 (x 28, y 7) | south | 65 | clickable wall |
| 278 (x 22, y 8) | north | 62 | clickable wall |
| 278 (x 22, y 8) | south | 62 | clickable wall |
| 285 (x 29, y 8) | north | 65 | clickable wall |
| 308 (x 20, y 9) | south | 65 | clickable wall |
| 373 (x 21, y 11) | east | 53 | clickable wall |
| 373 (x 21, y 11) | south | 27 | lever (to on) |
| 382 (x 30, y 11) | west | 61 | clickable wall |
| 403 (x 19, y 12) | east | 77 | clickable wall |
| 434 (x 18, y 13) | east | 61 | clickable wall |
| 440 (x 24, y 13) | east | 61 | clickable wall |
| 468 (x 20, y 14) | north | 62 | clickable wall |
| 468 (x 20, y 14) | south | 62 | clickable wall |
| 498 (x 18, y 15) | east | 65 | clickable wall |
| 503 (x 23, y 15) | east | 42 | clickable wall |
| 531 (x 19, y 16) | north | 53 | clickable wall |
| 538 (x 26, y 16) | north | 65 | clickable wall |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL9.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0000` | — | loads wall tiles CAVE1; loads monster sprites MORIBUND.SHP into slot 0; loads monster sprites FLSPIDER.SHP into slot 1; defines monster type 2; defines monster type 1 |
| INI entry 1 (runs when the level loads) | `0x00B5` | — | places a monster of type slot 1 on block 379 in mode 3; places a monster of type slot 1 on block 435 in mode 3; places a monster of type slot 1 on block 441 in mode 3; places item 99 (Rock) on block 309; places item 99 (Rock) on block 436; places item 243 (Coin Purse) on block 219; sets the west wall of block 992 to type -1; sets the east wall of block 992 to type 0 … |

### LEVEL9.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 152 (x 24, y 4) | `0x065B` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 152 to type 36; creates item type 9 and returns its handle; launches a projectile from block 157 in direction 3; checks the south wall of block 152; plays a sound (ID 80); plays a sound (ID 69) at block 157 |
| block 157 (x 29, y 4) | `0x0684` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 157 to type 36; creates item type 9 and returns its handle; launches a projectile from block 253 in direction 0; checks the south wall of block 157; plays a sound (ID 80); plays a sound (ID 69) at block 253 |
| block 179 (x 19, y 5) | `0x051A` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 179 to type 36; creates item type 9 and returns its handle; launches a projectile from block 115 in direction 2; sets game flag 42; sets script timer 1 to 120 ticks; checks the south wall of block 179; plays a sound (ID 80); plays a sound (ID 69) at block 115 |
| block 218 (x 26, y 6) | `0x06AD` | party steps in, party arrives (second path), item put down | moves items from block 218 to level 8, block 219 |
| block 219 (x 27, y 6) | `0x06BA` | wall clicked | sets the east wall of block 219 to type 45; checks the east wall of block 219 |
| block 246 (x 22, y 7) | `0x054B` | party arrives (second path), party leaves (second path), item put down, item taken, bits 0x400 (no engine caller found) | sets the north wall of block 278 to type 63; sets all four walls of block 246 to type 36; creates item type 9 and returns its handle; launches a projectile from block 243 in direction 1; checks the north wall of block 278; plays a sound (ID 135); checks the south wall of block 246; plays a sound (ID 80) … |
| block 247 (x 23, y 7) | `0x05BE` | fireball passes | no action summarized |
| block 248 (x 24, y 7) | `0x06D8` | wall clicked | plays chat/dialogue text ID 0x0009 |
| block 310 (x 22, y 9) | `0x059A` | bits 0x400 (no engine caller found) | sets the south wall of block 278 to type 63; checks the south wall of block 278; plays a sound (ID 135) |
| block 373 (x 21, y 11) | `0x04F3` | wall clicked | plays chat/dialogue text ID 0x0002; clears game flag 43; checks the south wall of block 993; checks the west wall of block 440; plays a sound (ID 79); checks the south wall of block 373 |
| block 374 (x 22, y 11) | `0x050E` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x0002; checks the south wall of block 993; checks the west wall of block 440 |
| block 378 (x 26, y 11) | `0x044F` | party arrives (second path) | creates item type 9 and returns its handle; launches a projectile from block 284 in direction 2; plays a sound (ID 69) at block 284 |
| block 382 (x 30, y 11) | `0x06DE` | wall clicked | plays chat/dialogue text ID 0x0009 |
| block 404 (x 20, y 12) | `0x05C0` | party arrives (second path), party leaves (second path), item put down, item taken | creates item type 9 and returns its handle; launches a projectile from block 340 in direction 2; sets game flag 43; sets script timer 1 to 120 ticks; checks the south wall of block 373; plays a sound (ID 69) at block 340 |
| block 412 (x 28, y 12) | `0x046D` | party arrives (second path), party leaves (second path), item put down, item taken | sets all four walls of block 412 to type 36; creates item type 9 and returns its handle; launches a projectile from block 506 in direction 0; checks the south wall of block 412; plays a sound (ID 80); plays a sound (ID 69) at block 506 |
| block 434 (x 18, y 13) | `0x06D2` | wall clicked | plays chat/dialogue text ID 0x0009 |
| block 436 (x 20, y 13) | `0x05F2` | party arrives (second path), bits 0x400 (no engine caller found) | sets the north wall of block 468 to type 63; plays chat/dialogue text ID 0x0005; checks the north wall of block 468; plays a sound (ID 135) |
| block 440 (x 24, y 13) | `0x06CC` | wall clicked | plays chat/dialogue text ID 0x0009 |
| block 499 (x 19, y 15) | `0x0516` | bits 0x400 (no engine caller found) | plays chat/dialogue text ID 0x0004; checks the south wall of block 992; checks the north wall of block 531 |
| block 500 (x 20, y 15) | `0x0632` | bits 0x400 (no engine caller found) | sets the south wall of block 468 to type 63; checks the south wall of block 468; plays a sound (ID 135) |
| block 503 (x 23, y 15) | `0x04C9` | party arrives (second path), wall clicked | sets all four walls of block 503 to type 0; creates item type 9 and returns its handle; launches a projectile from block 499 in direction 1; plays a sound (ID 69) at block 499 |
| block 504 (x 24, y 15) | `0x0496` | party arrives (second path) | sets game flag 159; plays chat/dialogue text ID 0x0000; plays chat/dialogue text ID 0x0001; checks the east wall of block 503; tests game flag 159 |
| block 509 (x 29, y 15) | `0x0442` | party steps in, party arrives (second path), item put down | moves items from block 509 to level 8, block 541 |
| block 531 (x 19, y 16) | `0x0512` | wall clicked | plays chat/dialogue text ID 0x0004; checks the south wall of block 992; checks the north wall of block 531 |
| `0x400` level loaded | `0x03AF` | — | sets script timer 0 to 3600 ticks; sets music theme 273; sets script timer 1 to 120 ticks |
| `0x401` script timer 0 | `0x03C1` | — | places a monster of type slot 2 on block 280 in mode 4 |
| `0x402` script timer 1 | `0x03EA` | — | creates item type 9 and returns its handle; launches a projectile from block 115 in direction 2; launches a projectile from block 340 in direction 2; disables script timer 1; tests game flag 42; plays a sound (ID 69) at block 115; tests game flag 43; checks the south wall of block 373 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 99 | Rock | 9 | 309 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 9 | 436 |
| INI entry 1 (runs when the level loads) | 243 | Coin Purse | 9 | 219 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 379 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 435 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 441 | 1 | 1 | 3 |
| `0x401` script timer 0 | 280 | 2 | 2 | 4 |
| `0x401` script timer 0 | 280 | 2 | 2 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 1, y 7 | 9 | x 13, y 14 | 0xffff |  |

## Text shown by the scripts (ids only)

- Level text file `LEVEL09.<lang>`: 6 ids: 0, 1, 2, 4, 5, 9.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL09.ENG --index N`.
