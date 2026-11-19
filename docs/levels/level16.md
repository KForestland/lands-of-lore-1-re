# Level 16

Made by `tools/level_report.py` from `LEVEL16.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

[Item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 6 = MINE1 (decorations `MINE1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MINE1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 382 | — | — |  | 0x80 | 63 |
| 3 | 2 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 8 | 4 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 31 | 3 | 2 | 14 | 2 lever (to on) | 0x07 | 207 |
| 32 | 1 | 2 | 15 | 3 lever (to off) | 0x07 | 207 |
| 41 | 6 | 1 | 3 |  | 0x07 | 255 |
| 42 | 3 | 1 | 16 | 2 lever (to on) | 0x07 | 207 |
| 44 | 16 | — | — |  | 0x84 | 17 |
| 47 | 2 | 6 | 61 | 1 clickable wall | 0x07 | 207 |
| 53 | 299 | 1 | — |  | 0x07 | 255 |
| 54 | 1701 | 2 | — |  | 0x07 | 255 |
| 55 | 1658 | 6 | — |  | 0x07 | 255 |
| 60 | 1 | 6 | 60 | 1 clickable wall | 0x07 | 207 |
| 66 | 2 | 1 | 37 | 1 clickable wall | 0x07 | 255 |
| 68 | 8 | 1 | 13 | 1 clickable wall | 0x07 | 255 |
| 79 | 4 | — | 38 | 1 clickable wall | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 64 (x 0, y 2) | north | 68 | clickable wall |
| 64 (x 0, y 2) | east | 68 | clickable wall |
| 64 (x 0, y 2) | south | 68 | clickable wall |
| 64 (x 0, y 2) | west | 68 | clickable wall |
| 135 (x 7, y 4) | north | 79 | clickable wall |
| 135 (x 7, y 4) | east | 79 | clickable wall |
| 135 (x 7, y 4) | south | 79 | clickable wall |
| 135 (x 7, y 4) | west | 79 | clickable wall |
| 137 (x 9, y 4) | south | 32 | lever (to off) |
| 139 (x 11, y 4) | west | 31 | lever (to on) |
| 145 (x 17, y 4) | north | 68 | clickable wall |
| 145 (x 17, y 4) | east | 68 | clickable wall |
| 145 (x 17, y 4) | south | 68 | clickable wall |
| 145 (x 17, y 4) | west | 68 | clickable wall |
| 201 (x 9, y 6) | east | 31 | lever (to on) |
| 203 (x 11, y 6) | north | 31 | lever (to on) |
| 236 (x 12, y 7) | north | 47 | clickable wall |
| 260 (x 4, y 8) | south | 42 | lever (to on) |
| 261 (x 5, y 8) | east | 42 | lever (to on) |
| 266 (x 10, y 8) | west | 66 | clickable wall |
| 295 (x 7, y 9) | north | 42 | lever (to on) |
| 358 (x 6, y 11) | north | 60 | clickable wall |
| 360 (x 8, y 11) | north | 47 | clickable wall |
| 418 (x 2, y 13) | east | 66 | clickable wall |
| 451 (x 3, y 14) | north | 3 | door / door switch |
| 451 (x 3, y 14) | south | 3 | door / door switch |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL16.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x002B` | — | loads wall tiles MINE1; loads monster sprites ROCKLING.SHP into slot 0; loads monster sprites TREZ.SHP into slot 1; defines monster type 1; defines monster type 2; sets door state bit 0x20 on block 174; sets door state bit 0x20 on block 207; sets door state bit 0x20 on block 238 … |
| INI entry 1 (runs when the level loads) | `0x0101` | — | places a monster of type slot 2 on block 72 in mode 3; places a monster of type slot 2 on block 110 in mode 3; places a monster of type slot 1 on block 226 in mode 3; places a monster of type slot 1 on block 271 in mode 3; places item 248 (Oil Flask) on block 611; places item 262 (Bezel Cup) on block 611; places item 176 (Mine key 4) on block 611; places item 33 (Axe "Vixen") on block 611 … |

### LEVEL16.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 64 (x 0, y 2) | `0x0474` | wall clicked | puts item 210 (Rusty key) on an empty cursor; sets game flag 226; plays music track 316; plays music track 317; plays music track 273; sets game flag 227; plays chat/dialogue text ID 0x0001; tests game flag 226 … |
| block 135 (x 7, y 4) | `0x040A` | wall clicked | plays chat/dialogue text ID 0x0012 |
| block 136 (x 8, y 4) | `0x0411` | bits 0x400 (no engine caller found) | places or moves item handle ? to level 16, block 136; sets the east wall of block 0 to type ?; sets all four walls of block 135 to type 0; creates item type 99 and returns its handle; checks the north wall of block 135; plays a sound (ID 135); checks the east wall of block 0; plays a sound (ID 134) |
| block 137 (x 9, y 4) | `0x0380` | wall clicked | no action summarized |
| block 139 (x 11, y 4) | `0x0382` | wall clicked | no action summarized |
| block 141 (x 13, y 4) | `0x0586` | party steps in, party arrives (second path), item put down | removes monsters from block 141; moves items from block 141 to level 16, block 292; plays a sound (ID 73) |
| block 145 (x 17, y 4) | `0x04F9` | wall clicked | puts item 258 (Note) on an empty cursor; puts item 253 (Gear) on an empty cursor; sets game flag 224; sets game flag 225; plays chat/dialogue text ID 0x0002; tests game flag 224; tests game flag 225 |
| block 170 (x 10, y 5) | `0x0319` | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 0 to type 1; sets the west wall of block 0 to type 0; character surprise feedback; move party; checks the west wall of block 0; checks the east wall of block 201; checks the south wall of block 137; checks the west wall of block 139 … |
| block 174 (x 14, y 5) | `0x0592` | party steps in, party arrives (second path), item put down | removes monsters from block 174; moves items from block 174 to level 12, block 246; plays a sound (ID 73) |
| block 196 (x 4, y 6) | `0x03A0` | wall clicked | plays chat/dialogue text ID 0x0012 |
| block 197 (x 5, y 6) | `0x03A7` | bits 0x400 (no engine caller found) | places or moves item handle ? to level 16, block 197; sets the south wall of block 0 to type ?; sets all four walls of block 196 to type 0; creates item type 99 and returns its handle; checks the north wall of block 196; plays a sound (ID 135); checks the south wall of block 0; plays a sound (ID 134) |
| block 198 (x 6, y 6) | `0x0386` | party arrives (second path) | sets all four walls of block 196 to type 79; sets game flag 228; tests game flag 228; plays a sound (ID 134) |
| block 201 (x 9, y 6) | `0x0317` | wall clicked | no action summarized |
| block 203 (x 11, y 6) | `0x0384` | wall clicked | no action summarized |
| block 207 (x 15, y 6) | `0x057A` | party steps in, party arrives (second path), item put down | removes monsters from block 207; moves items from block 207 to level 16, block 206; plays a sound (ID 73) |
| block 236 (x 12, y 7) | `0x0530` | wall clicked | deletes the held item; operates the door switch at block 205 with action 1; plays chat/dialogue text ID 0x0013; plays chat/dialogue text ID 0x4065; plays chat/dialogue text ID 0x0014; checks the west wall of block 205; plays a sound (ID 41); plays a sound (ID 40) |
| block 238 (x 14, y 7) | `0x059D` | party steps in, party arrives (second path), item put down | removes monsters from block 238; moves items from block 238 to level 14, block 332; plays a sound (ID 73) |
| block 259 (x 3, y 8) | `0x02E6` | party steps in, party arrives (second path), item put down | removes monsters from block 259; moves items from block 259 to level 16, block 262; checks the north wall of block 259; plays a sound (ID 73) |
| block 260 (x 4, y 8) | `0x02C3` | wall clicked | sets all four walls of block 259 to type 0; sets all four walls of block 259 to type 44; clears door state bit 0x20 on block 259; sets door state bit 0x20 on block 259; checks the north wall of block 259 |
| block 261 (x 5, y 8) | `0x02FB` | wall clicked | sets/clears game flag 219; tests game flag 219 |
| block 263 (x 7, y 8) | `0x0308` | party arrives (second path) | sets the north wall of block 0 to type ?; creates item type 9 and returns its handle; creates item type 10 and returns its handle; creates item type 1 and returns its handle; launches a projectile from block 265 in direction 3; tests game flag 219; checks the north wall of block 0; plays a sound (ID 69) at block 265 … |
| block 264 (x 8, y 8) | `0x030C` | party arrives (second path) | sets the north wall of block 0 to type ?; creates item type 9 and returns its handle; creates item type 10 and returns its handle; creates item type 1 and returns its handle; launches a projectile from block 265 in direction 3; tests game flag 219; checks the north wall of block 0; plays a sound (ID 69) at block 265 … |
| block 266 (x 10, y 8) | `0x0310` | wall clicked | plays chat/dialogue text ID 0x0015 |
| block 293 (x 5, y 9) | `0x02B6` | party steps in, party arrives (second path), item put down | moves items from block 293 to level 15, block 329 |
| block 295 (x 7, y 9) | `0x05A9` | wall clicked | sets all four walls of block 295 to type 0; plays a sound (ID 38) |
| block 358 (x 6, y 11) | `0x05B4` | wall clicked | deletes the held item; operates the door switch at block 359 with action 1; plays chat/dialogue text ID 0x0013; plays chat/dialogue text ID 0x4065; sets game flag 220; plays chat/dialogue text ID 0x000d; plays chat/dialogue text ID 0x000e; plays chat/dialogue text ID 0x0014 … |
| block 360 (x 8, y 11) | `0x05FD` | wall clicked | deletes the held item; operates the door switch at block 359 with action 1; plays chat/dialogue text ID 0x0013; plays chat/dialogue text ID 0x4065; sets game flag 221; plays chat/dialogue text ID 0x000d; plays chat/dialogue text ID 0x000e; plays chat/dialogue text ID 0x0014 … |
| block 418 (x 2, y 13) | `0x08A7` | wall clicked | plays chat/dialogue text ID 0x0015 |
| block 419 (x 3, y 13) | `0x08AE` | party arrives (second path), bits 0x10 (no engine caller found) | sets the west wall of block 0 to type 1; sets the west wall of block 0 to type 0; character surprise feedback; move party; checks the west wall of block 0 |
| block 422 (x 6, y 13) | `0x0897` | party arrives (second path) | sets game flag 223; tests game flag 223 |
| block 517 (x 5, y 16) | `0x0726` | wall clicked | places item 264 (Vaelan's Cube) on block 611; a character joins the party; puts item 200 (Paulson's Key) on an empty cursor; sets game flag 230; plays chat/dialogue text ID 0x000a; requests engine global change, selector 0, operands 0, 549; requests engine global change, selector 1, operands 0, 3; plays chat/dialogue text ID 0x0007 … |
| block 547 (x 3, y 17) | `0x08CB` | party arrives (second path), bits 0x10 (no engine caller found) | sets the north wall of block 579 to type 42; starts a dialogue sequence in mode 0; plays chat/dialogue text ID 0x0016; sets up 1 dialogue choices; reads the dialogue result; sets game flag 551; plays chat/dialogue text ID 0x0017; checks the north wall of block 579 … |
| block 549 (x 5, y 17) | `0x065B` | party steps in, bits 0x4000 (no engine caller found) | plays chat/dialogue text ID 0x0004; tests game flag 230; plays a sound (ID 128); tests game flag 231 |
| block 579 (x 3, y 18) | `0x092D` | wall clicked | sets all four walls of block 579 to type 0; plays a sound (ID 38) |
| `0x400` level loaded | `0x027D` | — | sets the west wall of block 0 to type 0; sets music theme 273; sets script timer 0 to 300 ticks |
| `0x401` script timer 0 | `0x028E` | — | creates item type 9 and returns its handle; launches a projectile from block 419 in direction 1; tests game flag 223; plays a sound (ID 69) at block 419 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 16 | 611 |
| INI entry 1 (runs when the level loads) | 262 | Bezel Cup | 16 | 611 |
| INI entry 1 (runs when the level loads) | 176 | Mine key 4 | 16 | 611 |
| INI entry 1 (runs when the level loads) | 33 | Axe "Vixen" | 16 | 611 |
| INI entry 1 (runs when the level loads) | 149 | Kite shield | 16 | 611 |
| INI entry 1 (runs when the level loads) | 130 | Dwarvish boots | 16 | 611 |
| INI entry 1 (runs when the level loads) | 140 | Great helm | 16 | 611 |
| INI entry 1 (runs when the level loads) | 134 | Chain mail | 16 | 611 |
| block 517 (x 5, y 16) | 264 | Vaelan's Cube | 16 | 611 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 72 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 110 | 0 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 226 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 271 | 2 | 1 | 3 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 5, y 16 | 3 | x 5, y 16 | 0x41ee | HIDEOUT |
| x 1, y 2 | 4 | x 1, y 2 | 0x41ef | ORIN'S GHOST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL16.<lang>`: 15 ids: 1, 2, 4, 7, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 23.
- Global text `LANDS.<lang>`: 1 ids: 0x4065.

Read any of them with `tools/decode_dialogue.py LEVEL16.ENG --index N`.
