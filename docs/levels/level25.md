# Level 25

Made by `tools/level_report.py` from `LEVEL25.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).

## Size, area and graphics

- Map: 32 x 32 blocks, 4 bytes per block in the CMZ.
- Area (WLL header): 9 = CATWALK (decorations `CATWALK.SHP` / `.DAT`).
- Wall tiles loaded by the scripts: CAVE1 with palette CAV_PLT3.PAL (INI).

## Wall types used

| Type | Count | VMP page | Shape | Special | Flags | Automap |
|---|---|---|---|---|---|---|
| 0 | 134 | — | — |  | 0x80 | 63 |
| 1 | 1970 | 1 | — |  | 0x07 | 255 |
| 2 | 1970 | 2 | — |  | 0x07 | 255 |
| 8 | 2 | 3 | — |  | 0xaf | 13 |
| 23 | 4 | 4 | — |  | 0x84 | 25 |
| 40 | 4 | — | — |  | 0x84 | 17 |
| 44 | 2 | 1 | 52 | 2 lever (to on) | 0x07 | 207 |
| 46 | 8 | — | 37 |  | 0x80 | 63 |
| 49 | 2 | 1 | 59 |  | 0x07 | 255 |

## Clickable walls

| Block | Side | Wall type | What it is |
|---|---|---|---|
| 832 (x 0, y 26) | north | 44 | lever (to on) |
| 834 (x 2, y 26) | south | 44 | lever (to on) |

## Script entry points

Each row is one entry of the level's scripts. Events: when the engine runs it ([README](README.md#events)). The description lists the game actions the entry's code calls, actions that change the game first, then checks (constant arguments only; `?` = computed at run time; `…` = more than eight).

### LEVEL25.INI

| Entry | Events | What it does |
|---|---|---|
| INI entry 0 (runs when the level loads) | — | loads wall tiles CAVE1; loads monster sprites CABAL.SHP into slot 0; loads monster sprites NECROSAP.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | — | places a monster (slot 1) on block 943; places a monster (slot 1) on block 946; places a monster (slot 1) on block 843; places a monster (slot 1) on block 846; places a monster (slot 1) on block 819; places a monster (slot 1) on block 866; places a monster (slot 1) on block 898; places a monster (slot 2) on block 673 … |

### LEVEL25.INF

| Entry | Events | What it does |
|---|---|---|
| block 325 (x 5, y 10) | party steps in, party arrives (second path), item put down | moves objects from block 325 to block 293 |
| block 771 (x 3, y 24) | party steps in, party arrives (second path), item put down | moves objects from block 771 to block 801; plays a sound |
| `0x400` level loaded | — | drops the party through a pit; clears game flag 46; starts script timer 0; tests game flag 46 |
| `0x401` script timer 0 | — | places a monster (slot 1) on block 896; places a monster (slot 1) on block 672; places a monster (slot 1) on block 196 |

## Items placed by the scripts

None by constant script calls.

## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 943 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 943 | 1 | 1 | 4 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 946 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 843 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 843 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 846 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 846 | 1 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 819 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 819 | 2 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 866 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 898 | 3 | 1 | 3 |
| INI entry 1 (runs when the level loads) | 673 | 1 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 545 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 546 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 240 | 3 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 241 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 242 | 2 | 2 | 4 |
| INI entry 1 (runs when the level loads) | 774 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 774 | 2 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 680 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 680 | 3 | 2 | 3 |
| INI entry 1 (runs when the level loads) | 728 | 3 | 1 | 4 |
| `0x401` script timer 0 | 896 | 0 | 1 | 4 |
| `0x401` script timer 0 | 672 | 2 | 1 | 4 |
| `0x401` script timer 0 | 196 | 2 | 1 | 4 |

## Automap legend

| Symbol at | Symbol | Shown after exploring | Text id | Name |
|---|---|---|---|---|
| x 0, y 1 | 6 | x 0, y 1 | 0xffff |  |

## Text shown by the scripts (ids only)

- Level text file `LEVEL25.<lang>`: 0 ids: none.
- Global text `LANDS.<lang>`: 0 ids: none.

Read any of them with `tools/decode_dialogue.py LEVEL25.ENG --index N`.
