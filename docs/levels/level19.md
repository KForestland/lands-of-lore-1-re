# Level 19

Made by `tools/level_report.py` from `LEVEL19.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

Related references: [Progression rows for level 19](../PROGRESSION.md#level-19) and [item, spell and creature numbers](../NUMBERS.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 7 = TOWER1 (decorations `TOWER1.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: TOWER1 (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 141 | — | — |  | 0x80 | 63 |
| 1 | 1939 | 1 | — |  | 0x07 | 255 |
| 2 | 1939 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x04 | 25 |
| 25 | 2 | 2 | 22 |  | 0x07 | 255 |
| 30 | 5 | 2 | 21 | 6 niche | 0x87 | 14 |
| 43 | 1 | 2 | 4 | 1 clickable wall | 0x07 | 255 |
| 44 | 4 | — | 3 |  | 0x80 | 17 |
| 56 | 1 | 1 | 17 | 1 clickable wall | 0x07 | 207 |
| 61 | 1 | 2 | 57 | 1 clickable wall | 0x07 | 207 |
| 71 | 6 | 1 | 42 |  | 0x07 | 255 |
| 72 | 8 | 1 | 43 |  | 0x07 | 255 |
| 73 | 6 | 1 | 44 |  | 0x07 | 255 |
| 74 | 6 | 1 | 45 |  | 0x07 | 255 |
| 75 | 6 | 1 | 46 |  | 0x07 | 255 |
| 76 | 6 | 2 | 51 |  | 0x07 | 255 |
| 77 | 8 | 2 | 52 |  | 0x07 | 255 |
| 78 | 6 | 2 | 53 |  | 0x07 | 255 |
| 79 | 5 | 2 | 50 |  | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 6 (x 6, y 0) | south | 30 | niche |
| 68 (x 4, y 2) | east | 30 | niche |
| 68 (x 4, y 2) | south | 43 | clickable wall |
| 70 (x 6, y 2) | east | 30 | niche |
| 117 (x 21, y 3) | west | 56 | clickable wall |
| 134 (x 6, y 4) | north | 30 | niche |
| 137 (x 9, y 4) | north | 61 | clickable wall |
| 165 (x 5, y 5) | west | 30 | niche |

## Script entry points

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL19.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x0087` | — | loads wall tiles TOWER1; loads monster sprites APARITIN.SHP into slot 0; loads monster sprites WRAITH.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x0141` | — | places a monster of type slot 2 on block 116 in mode 3; places a monster of type slot 1 on block 147 in mode 3; sets the north wall of block ? to type 37; sets the east wall of block ? to type 192; sets the south wall of block ? to type 64; sets the north wall of block ? to type 38; sets the east wall of block ? to type 64; sets the north wall of block ? to type 39 … |

### LEVEL19.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 6 (x 6, y 0) | `0x04DA` | item put down, item taken | sets the north wall of block 134 to type 76; sets the east wall of block 68 to type 77; sets the south wall of block 6 to type 78; sets the east wall of block 70 to type 79; sets game flag 329; sets game flag 330 |
| block 37 (x 5, y 1) | `0x04CE` | party leaves (second path), item taken | no action summarized |
| block 38 (x 6, y 1) | `0x04DE` | party leaves (second path), item taken, bits 0x10 (no engine caller found) | no action summarized |
| block 39 (x 7, y 1) | `0x04EE` | party leaves (second path), item taken | no action summarized |
| block 68 (x 4, y 2) | `0x04FA` | wall clicked, item put down, item taken | sets the north wall of block 134 to type 76; sets the east wall of block 68 to type 77; sets the south wall of block 6 to type 78; sets the east wall of block 70 to type 79; plays chat/dialogue text ID 0x0002; sets game flag 329; sets game flag 330 |
| block 69 (x 5, y 2) | `0x04D2` | party leaves (second path), item taken, bits 0x10 (no engine caller found) | no action summarized |
| block 70 (x 6, y 2) | `0x04E2` | item put down, item taken | sets the north wall of block 134 to type 76; sets the east wall of block 68 to type 77; sets the south wall of block 6 to type 78; sets the east wall of block 70 to type 79; sets game flag 329; sets game flag 330 |
| block 71 (x 7, y 2) | `0x04F6` | party leaves (second path), item taken, bits 0x10 (no engine caller found) | no action summarized |
| block 73 (x 9, y 2) | `0x04BB` | party steps in, party arrives (second path), item put down | removes monsters from block 73; moves items from block 73 to level 19, block 115; tests game flag 329; plays a sound (ID 73) |
| block 101 (x 5, y 3) | `0x04D6` | party leaves (second path), item taken | no action summarized |
| block 102 (x 6, y 3) | `0x04E6` | party leaves (second path), item taken, bits 0x10 (no engine caller found) | no action summarized |
| block 103 (x 7, y 3) | `0x04F2` | party leaves (second path), item taken | no action summarized |
| block 117 (x 21, y 3) | `0x0485` | wall clicked | sets the west wall of block 117 to type 0; plays a sound (ID 37) |
| block 118 (x 22, y 3) | `0x048F` | party steps in, party arrives (second path), item put down | sets the west wall of block 117 to type 56; removes monsters from block 118; suspend monster; moves items from block 118 to level 19, block 198; plays chat/dialogue text ID 0x0008; sets game flag 332; plays a sound (ID 73); tests game flag 332 … |
| block 134 (x 6, y 4) | `0x04EA` | item put down, item taken | sets the north wall of block 134 to type 76; sets the east wall of block 68 to type 77; sets the south wall of block 6 to type 78; sets the east wall of block 70 to type 79; sets game flag 329; sets game flag 330 |
| block 137 (x 9, y 4) | `0x038E` | wall clicked | sets the north wall of block 137 to type 66; puts item 260 (Crucible of Faith) on an empty cursor; plays chat/dialogue text ID 0x0005; plays music track -1; plays music track 290; plays chat/dialogue text ID 0x0009; plays chat/dialogue text ID 0x0001; sets game flag 359 … |
| block 140 (x 12, y 4) | `0x046A` | wall clicked | puts item 260 (Crucible of Faith) on an empty cursor; plays music track 290; sets game flag 359 |
| block 166 (x 6, y 5) | `0x0381` | party steps in, party arrives (second path), item put down | moves items from block 166 to level 18, block 417 |
| block 170 (x 10, y 5) | `0x0450` | party arrives (second path), party leaves, bits 0x4010 (no engine caller found) | plays music track -1; plays music track 290; tests game flag 359; plays a sound (ID 128); plays a sound (ID 94) |
| block 172 (x 12, y 5) | `0x0464` | party arrives (second path), party leaves, bits 0x4010 (no engine caller found) | plays music track -1; plays music track 290; tests game flag 359; plays a sound (ID 128); plays a sound (ID 94) |
| block 202 (x 10, y 6) | `0x0456` | wall clicked | puts item 260 (Crucible of Faith) on an empty cursor; plays music track 290; sets game flag 359 |
| block 204 (x 12, y 6) | `0x045A` | party arrives (second path), party leaves, bits 0x4010 (no engine caller found) | plays music track -1; plays music track 290; tests game flag 359; plays a sound (ID 128); plays a sound (ID 94) |
| block 205 (x 13, y 6) | `0x0460` | wall clicked | puts item 260 (Crucible of Faith) on an empty cursor; plays music track 290; sets game flag 359 |
| block 229 (x 5, y 7) | `0x046E` | party arrives (second path) | sets game flag 328; tests game flag 328; plays a sound (ID 179) |
| `0x400` level loaded | `0x036E` | — | sets music theme 290; sets script timer 0 to 70 ticks |
| `0x401` script timer 0 | `0x0378` | — | sets game flag 331; moves items from block 38 to level 19, block 37; moves items from block 39 to level 19, block 38; moves items from block 71 to level 19, block 39; moves items from block 103 to level 19, block 71; moves items from block 102 to level 19, block 103; moves items from block 101 to level 19, block 102; moves items from block 69 to level 19, block 101 … |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | ? | ? | 19 | ? |
| INI entry 1 (runs when the level loads) | 16 | Dwarvish horseshoe | 19 | 38 |
| INI entry 1 (runs when the level loads) | 17 | Dwarvish helm | 19 | 69 |
| INI entry 1 (runs when the level loads) | 18 | Saber "Cougar" | 19 | 102 |
| INI entry 1 (runs when the level loads) | 19 | Wand of Death | 19 | 71 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 116 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 116 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 147 | 0 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 147 | 0 | 1 | 3 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 10, y 5 | 1 | x 10, y 5 | 0x41f6 | OLD WOMAN |

## Text shown by the scripts (ids only)

- Level text file `LEVEL19.<lang>`: 5 ids: 1, 2, 5, 8, 9.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL19.ENG --index N`.
