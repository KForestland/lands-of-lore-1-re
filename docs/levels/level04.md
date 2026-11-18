# Level 4

Made by `tools/level_report.py` from `LEVEL4.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 2 = MANOR (decorations `MANOR.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: MANOR (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 329 | — | — |  | 0x80 | 63 |
| 1 | 1792 | 1 | — |  | 0x07 | 255 |
| 2 | 1801 | 2 | — |  | 0x07 | 255 |
| 3 | 14 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 13 | 4 | 3 | — | 5 door / door switch | 0xaf | 13 |
| 41 | 10 | 1 | 12 |  | 0x07 | 255 |
| 42 | 1 | 1 | 10 | 4 click runs script | 0x07 | 207 |
| 53 | 8 | 1 | 1 | 1 clickable wall | 0x07 | 255 |
| 54 | 5 | 1 | 2 | 1 clickable wall | 0x07 | 255 |
| 55 | 5 | 1 | 3 | 1 clickable wall | 0x07 | 255 |
| 56 | 5 | 1 | 4 | 1 clickable wall | 0x07 | 255 |
| 57 | 9 | 1 | 5 | 1 clickable wall | 0x07 | 255 |
| 58 | 8 | 1 | 6 | 1 clickable wall | 0x07 | 255 |
| 59 | 8 | 1 | 7 | 1 clickable wall | 0x07 | 255 |
| 60 | 4 | 1 | 14 | 1 clickable wall | 0x07 | 210 |
| 61 | 4 | 1 | — |  | 0x07 | 255 |
| 62 | 4 | 2 | — |  | 0x07 | 255 |
| 63 | 8 | 4 | — |  | 0x07 | 255 |
| 64 | 4 | 1 | 25 | 6 niche | 0x87 | 14 |
| 65 | 36 | — | 20 | 1 clickable wall | 0x80 | 63 |
| 66 | 2 | 1 | 18 | 1 clickable wall | 0x07 | 255 |
| 67 | 2 | 1 | 19 | 1 clickable wall | 0x07 | 255 |
| 68 | 5 | 1 | 17 | 1 clickable wall | 0x07 | 255 |
| 69 | 4 | 1 | 22 | 1 clickable wall | 0x07 | 255 |
| 70 | 2 | 1 | 24 | 1 clickable wall | 0x07 | 255 |
| 71 | 7 | 1 | 23 | 1 clickable wall | 0x07 | 255 |
| 72 | 5 | 1 | 15 | 1 clickable wall | 0x07 | 210 |
| 73 | 4 | 1 | 16 | 1 clickable wall | 0x07 | 210 |
| 74 | 5 | 2 | 8 | 2 lever (to on) | 0x07 | 207 |
| 77 | 1 | 3 | 26 |  | 0x84 | 63 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 1 (x 1, y 0) | south | 58 | clickable wall |
| 2 (x 2, y 0) | south | 56 | clickable wall |
| 5 (x 5, y 0) | south | 66 | clickable wall |
| 6 (x 6, y 0) | north | 53 | clickable wall |
| 6 (x 6, y 0) | east | 53 | clickable wall |
| 6 (x 6, y 0) | south | 53 | clickable wall |
| 6 (x 6, y 0) | west | 53 | clickable wall |
| 9 (x 9, y 0) | south | 72 | clickable wall |
| 11 (x 11, y 0) | south | 58 | clickable wall |
| 12 (x 12, y 0) | south | 57 | clickable wall |
| 33 (x 1, y 1) | north | 65 | clickable wall |
| 33 (x 1, y 1) | east | 65 | clickable wall |
| 33 (x 1, y 1) | south | 65 | clickable wall |
| 33 (x 1, y 1) | west | 65 | clickable wall |
| 41 (x 9, y 1) | north | 65 | clickable wall |
| 41 (x 9, y 1) | east | 65 | clickable wall |
| 41 (x 9, y 1) | south | 65 | clickable wall |
| 41 (x 9, y 1) | west | 65 | clickable wall |
| 43 (x 11, y 1) | north | 65 | clickable wall |
| 43 (x 11, y 1) | east | 65 | clickable wall |
| 43 (x 11, y 1) | south | 65 | clickable wall |
| 43 (x 11, y 1) | west | 65 | clickable wall |
| 44 (x 12, y 1) | north | 65 | clickable wall |
| 44 (x 12, y 1) | east | 65 | clickable wall |
| 44 (x 12, y 1) | south | 65 | clickable wall |
| 44 (x 12, y 1) | west | 65 | clickable wall |
| 64 (x 0, y 2) | east | 57 | clickable wall |
| 67 (x 3, y 2) | east | 71 | clickable wall |
| 67 (x 3, y 2) | west | 67 | clickable wall |
| 69 (x 5, y 2) | north | 65 | clickable wall |
| 69 (x 5, y 2) | east | 65 | clickable wall |
| 69 (x 5, y 2) | south | 65 | clickable wall |
| 69 (x 5, y 2) | west | 65 | clickable wall |
| 72 (x 8, y 2) | west | 66 | clickable wall |
| 74 (x 10, y 2) | east | 42 | click runs script |
| 97 (x 1, y 3) | north | 71 | clickable wall |
| 97 (x 1, y 3) | south | 59 | clickable wall |
| 98 (x 2, y 3) | north | 3 | door / door switch |
| 98 (x 2, y 3) | south | 3 | door / door switch |
| 101 (x 5, y 3) | north | 58 | clickable wall |
| 102 (x 6, y 3) | north | 3 | door / door switch |
| 102 (x 6, y 3) | south | 3 | door / door switch |
| 104 (x 8, y 3) | south | 59 | clickable wall |
| 108 (x 12, y 3) | north | 3 | door / door switch |
| 108 (x 12, y 3) | south | 3 | door / door switch |
| 128 (x 0, y 4) | east | 54 | clickable wall |
| 132 (x 4, y 4) | north | 65 | clickable wall |
| 132 (x 4, y 4) | east | 65 | clickable wall |
| 132 (x 4, y 4) | south | 65 | clickable wall |
| 132 (x 4, y 4) | west | 65 | clickable wall |
| 139 (x 11, y 4) | north | 65 | clickable wall |
| 139 (x 11, y 4) | east | 65 | clickable wall |
| 139 (x 11, y 4) | south | 65 | clickable wall |
| 139 (x 11, y 4) | west | 65 | clickable wall |
| 141 (x 13, y 4) | west | 57 | clickable wall |
| 162 (x 2, y 5) | west | 71 | clickable wall |
| 163 (x 3, y 5) | south | 58 | clickable wall |
| 164 (x 4, y 5) | north | 58 | clickable wall |
| 164 (x 4, y 5) | south | 59 | clickable wall |
| 165 (x 5, y 5) | north | 67 | clickable wall |
| 169 (x 9, y 5) | north | 68 | clickable wall |
| 170 (x 10, y 5) | north | 58 | clickable wall |
| 170 (x 10, y 5) | south | 59 | clickable wall |
| 171 (x 11, y 5) | north | 3 | door / door switch |
| 171 (x 11, y 5) | south | 3 | door / door switch |
| 194 (x 2, y 6) | east | 3 | door / door switch |
| 194 (x 2, y 6) | west | 3 | door / door switch |
| 195 (x 3, y 6) | north | 65 | clickable wall |
| 195 (x 3, y 6) | east | 65 | clickable wall |
| 195 (x 3, y 6) | south | 65 | clickable wall |
| 195 (x 3, y 6) | west | 65 | clickable wall |
| 197 (x 5, y 6) | west | 70 | clickable wall |
| 205 (x 13, y 6) | west | 70 | clickable wall |
| 224 (x 0, y 7) | east | 58 | clickable wall |
| 233 (x 9, y 7) | east | 55 | clickable wall |
| 237 (x 13, y 7) | west | 58 | clickable wall |
| 257 (x 1, y 8) | north | 57 | clickable wall |
| 259 (x 3, y 8) | north | 74 | lever (to on) |
| 267 (x 11, y 8) | north | 57 | clickable wall |
| 967 (x 7, y 30) | north | 3 | door / door switch |
| 967 (x 7, y 30) | east | 3 | door / door switch |
| 967 (x 7, y 30) | south | 3 | door / door switch |
| 967 (x 7, y 30) | west | 3 | door / door switch |
| 968 (x 8, y 30) | north | 13 | door / door switch |
| 968 (x 8, y 30) | east | 13 | door / door switch |
| 968 (x 8, y 30) | south | 13 | door / door switch |
| 968 (x 8, y 30) | west | 13 | door / door switch |
| 969 (x 9, y 30) | north | 53 | clickable wall |
| 969 (x 9, y 30) | east | 53 | clickable wall |
| 969 (x 9, y 30) | south | 53 | clickable wall |
| 969 (x 9, y 30) | west | 53 | clickable wall |
| 970 (x 10, y 30) | north | 54 | clickable wall |
| 970 (x 10, y 30) | east | 54 | clickable wall |
| 970 (x 10, y 30) | south | 54 | clickable wall |
| 970 (x 10, y 30) | west | 54 | clickable wall |
| 971 (x 11, y 30) | north | 55 | clickable wall |
| 971 (x 11, y 30) | east | 55 | clickable wall |
| 971 (x 11, y 30) | south | 55 | clickable wall |
| 971 (x 11, y 30) | west | 55 | clickable wall |
| 972 (x 12, y 30) | north | 56 | clickable wall |
| 972 (x 12, y 30) | east | 56 | clickable wall |
| 972 (x 12, y 30) | south | 56 | clickable wall |
| 972 (x 12, y 30) | west | 56 | clickable wall |
| 973 (x 13, y 30) | north | 57 | clickable wall |
| 973 (x 13, y 30) | east | 57 | clickable wall |
| 973 (x 13, y 30) | south | 57 | clickable wall |
| 973 (x 13, y 30) | west | 57 | clickable wall |
| 974 (x 14, y 30) | north | 59 | clickable wall |
| 974 (x 14, y 30) | east | 59 | clickable wall |
| 974 (x 14, y 30) | south | 59 | clickable wall |
| 974 (x 14, y 30) | west | 59 | clickable wall |
| 975 (x 15, y 30) | north | 60 | clickable wall |
| 975 (x 15, y 30) | east | 60 | clickable wall |
| 975 (x 15, y 30) | south | 60 | clickable wall |
| 975 (x 15, y 30) | west | 60 | clickable wall |
| 979 (x 19, y 30) | north | 64 | niche |
| 979 (x 19, y 30) | east | 64 | niche |
| 979 (x 19, y 30) | south | 64 | niche |
| 979 (x 19, y 30) | west | 64 | niche |
| 980 (x 20, y 30) | north | 65 | clickable wall |
| 980 (x 20, y 30) | east | 65 | clickable wall |
| 980 (x 20, y 30) | south | 65 | clickable wall |
| 980 (x 20, y 30) | west | 65 | clickable wall |
| 981 (x 21, y 30) | north | 68 | clickable wall |
| 981 (x 21, y 30) | east | 68 | clickable wall |
| 981 (x 21, y 30) | south | 68 | clickable wall |
| 981 (x 21, y 30) | west | 68 | clickable wall |
| 982 (x 22, y 30) | north | 69 | clickable wall |
| 982 (x 22, y 30) | east | 69 | clickable wall |
| 982 (x 22, y 30) | south | 69 | clickable wall |
| 982 (x 22, y 30) | west | 69 | clickable wall |
| 983 (x 23, y 30) | north | 71 | clickable wall |
| 983 (x 23, y 30) | east | 71 | clickable wall |
| 983 (x 23, y 30) | south | 71 | clickable wall |
| 983 (x 23, y 30) | west | 71 | clickable wall |
| 984 (x 24, y 30) | north | 72 | clickable wall |
| 984 (x 24, y 30) | east | 72 | clickable wall |
| 984 (x 24, y 30) | south | 72 | clickable wall |
| 984 (x 24, y 30) | west | 72 | clickable wall |
| 985 (x 25, y 30) | north | 73 | clickable wall |
| 985 (x 25, y 30) | east | 73 | clickable wall |
| 985 (x 25, y 30) | south | 73 | clickable wall |
| 985 (x 25, y 30) | west | 73 | clickable wall |
| 986 (x 26, y 30) | north | 74 | lever (to on) |
| 986 (x 26, y 30) | east | 74 | lever (to on) |
| 986 (x 26, y 30) | south | 74 | lever (to on) |
| 986 (x 26, y 30) | west | 74 | lever (to on) |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL4.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles MANOR; loads monster sprites ORC.SHP into slot 0; loads monster sprites ORCLDR.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 33; places a monster (slot 1) on block 196; places a monster (slot 1) on block 137; places a monster (slot 1) on block 68; places a monster (slot 1) on block 236; places a monster (slot 1) on block 34; places a monster (slot 1) on block 228; places a monster (slot 1) on block 133 … |

### LEVEL4.INF

| Entry | Events | What it does |
|---|---|---|
| block 1 (x 1, y 0) | wall clicked | a character speaks |
| block 2 (x 2, y 0) | wall clicked | a character speaks |
| block 5 (x 5, y 0) | wall clicked | a character speaks |
| block 6 (x 6, y 0) | wall clicked | gives item 240 (Burnt Scroll); a character speaks; set global script var |
| block 9 (x 9, y 0) | wall clicked | sets the north wall of block 992 to type ?; gives 200 crown(s); a character speaks; sets game flag 254; tests game flag 254 |
| block 11 (x 11, y 0) | wall clicked | a character speaks |
| block 12 (x 12, y 0) | wall clicked | a character speaks |
| block 33 (x 1, y 1) | wall clicked | a character speaks |
| block 41 (x 9, y 1) | party arrives (second path), wall clicked, bits 0x410 (no engine caller found) | sets the north wall of block 992 to type ?; gives 200 crown(s); a character speaks; sets game flag 254; shows a message; tests game flag 254; tests game flag 29; set global var |
| block 43 (x 11, y 1) | wall clicked | a character speaks |
| block 44 (x 12, y 1) | wall clicked | a character speaks |
| block 64 (x 0, y 2) | wall clicked | a character speaks |
| block 67 (x 3, y 2) | wall clicked | a character speaks |
| block 69 (x 5, y 2) | wall clicked | a character speaks |
| block 72 (x 8, y 2) | wall clicked | a character speaks |
| block 73 (x 9, y 2) | party steps in, bits 0x4000 (no engine caller found) | starts cut-scene ROLAND1.TIM; starts cut-scene ROLAND2.TIM; sets game flag 29; sets game flag 39; a character speaks; starts a dialogue; tests game flag 29; set global var |
| block 74 (x 10, y 2) | wall clicked | sets the west wall of block 74 to type 0; plays a sound |
| block 75 (x 11, y 2) | party arrives (second path), bits 0x10 (no engine caller found) | a character speaks; sets game flag 115; tests game flag 115 |
| block 76 (x 12, y 2) | party arrives (second path), party leaves, bits 0x10 (no engine caller found) | sets game flag 116; a character speaks; starts a dialogue; move party; suspend monster; changes a monster; tests game flag 116 |
| block 97 (x 1, y 3) | wall clicked | a character speaks; starts a dialogue |
| block 101 (x 5, y 3) | wall clicked | a character speaks |
| block 104 (x 8, y 3) | wall clicked | a character speaks; starts a dialogue |
| block 128 (x 0, y 4) | wall clicked | a character speaks |
| block 132 (x 4, y 4) | wall clicked | a character speaks |
| block 139 (x 11, y 4) | wall clicked | a character speaks |
| block 141 (x 13, y 4) | wall clicked | a character speaks |
| block 162 (x 2, y 5) | wall clicked | a character speaks |
| block 163 (x 3, y 5) | wall clicked | a character speaks |
| block 164 (x 4, y 5) | wall clicked | a character speaks; starts a dialogue |
| block 165 (x 5, y 5) | wall clicked | a character speaks |
| block 169 (x 9, y 5) | wall clicked | a character speaks |
| block 170 (x 10, y 5) | wall clicked | a character speaks; starts a dialogue |
| block 195 (x 3, y 6) | wall clicked | a character speaks |
| block 197 (x 5, y 6) | wall clicked | a character speaks |
| block 199 (x 7, y 6) | party steps in, party arrives (second path), item put down | moves the party to level 3, block 804; moves objects from block 199 to block 804; shows a message; set global var |
| block 205 (x 13, y 6) | wall clicked | a character speaks |
| block 224 (x 0, y 7) | wall clicked | a character speaks |
| block 233 (x 9, y 7) | wall clicked | a character speaks |
| block 237 (x 13, y 7) | wall clicked | a character speaks |
| block 257 (x 1, y 8) | wall clicked | a character speaks |
| block 259 (x 3, y 8) | wall clicked | sets the north wall of block 260 to type 64; sets the north wall of block 260 to type 61; checks a wall of block 259 |
| block 267 (x 11, y 8) | wall clicked | a character speaks |
| `0x400` level loaded | — | starts script timer 0 |
| `0x401` script timer 0 | — | toggles the south wall of block 97 between types 59 and 78; toggles the south wall of block 164 between types 59 and 78; toggles the south wall of block 104 between types 59 and 78; toggles the south wall of block 170 between types 59 and 78 |

## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 166 | Roland's key | 4 | 41 |
| INI entry 1 (runs when the level loads) | 217 | Aloe | 4 | 260 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 4 | 260 |
| INI entry 1 (runs when the level loads) | 248 | Oil Flask | 4 | 260 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 4 | 135 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 4 | 65 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 4 | 76 |
| INI entry 1 (runs when the level loads) | 99 | Rock | 4 | 68 |

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 33 | 2 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 196 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 137 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 68 | 1 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 236 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 34 | 2 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 228 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 133 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 36 | 1 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 204 | 3 | 1 | 7 |
| INI entry 1 (runs when the level loads) | 44 | 2 | 1 | 1 |
| INI entry 1 (runs when the level loads) | 44 | 2 | 1 | 1 |
| INI entry 1 (runs when the level loads) | 44 | 2 | 2 | 1 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 9, y 1 | 4 | x 9, y 2 | 0x41dd | SIR ROLAND |
| x 7, y 6 | 0 | x 7, y 5 | 0x41de | FOREST |

## Text shown by the scripts (ids only)

- Level text file `LEVEL04.<lang>`: 32 ids: 0, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 26, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 49, 50.
- Global text `LANDS.<lang>`: 1 ids: 0x403f.

Read any of them with `tools/decode_dialogue.py LEVEL04.ENG --index N`.
