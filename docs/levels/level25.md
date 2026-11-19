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

**CONFIRMED.** The DATA word is the ORDR target in the named original script. Its event mask identifies when the engine can run it ([event sources](README.md#events)).

Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. `?` marks an argument the walk could not recover. `…` marks additional actions. The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets and the evidence label of each effect (effects known only from ScummVM are labelled there).

### LEVEL25.INI

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| INI entry 0 (runs when the level loads) | `0x003E` | — | loads wall tiles CAVE1; loads monster sprites CABAL.SHP into slot 0; loads monster sprites NECROSAP.SHP into slot 1; defines monster type 1; defines monster type 2 |
| INI entry 1 (runs when the level loads) | `0x00EA` | — | places a monster of type slot 1 on block 943 in mode 4; places a monster of type slot 1 on block 946 in mode 3; places a monster of type slot 1 on block 843 in mode 3; places a monster of type slot 1 on block 846 in mode 3; places a monster of type slot 1 on block 819 in mode 3; places a monster of type slot 1 on block 866 in mode 3; places a monster of type slot 1 on block 898 in mode 3; places a monster of type slot 2 on block 673 in mode 3 … |

### LEVEL25.INF

| Entry | DATA word | Events | What it can do |
|---|---:|---|---|
| block 325 (x 5, y 10) | `0x00C9` | party steps in, party arrives (second path), item put down | moves items from block 325 to level 23, block 293 |
| block 771 (x 3, y 24) | `0x00D7` | party steps in, party arrives (second path), item put down | removes monsters from block 771; moves items from block 771 to level 23, block 801; plays a sound (ID 73) |
| `0x400` level loaded | `0x0071` | — | drops the party through a pit; clears game flag 46; sets music theme 268; sets script timer 0 to 10800 ticks; tests game flag 46 |
| `0x401` script timer 0 | `0x008D` | — | places a monster of type slot 1 on block 896 in mode 4; places a monster of type slot 1 on block 672 in mode 4; places a monster of type slot 1 on block 196 in mode 4 |

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
