# Level sheets

One page per level, written by `tools/level_report.py` from the level's own files (CD edition): map, wall table, automap legend and scripts. No game text is copied except the short names of items and automap places.

## How to read a sheet

- **Wall types used**: every wall type number in the map, how many block sides carry it, and its entry in the level's WLL table ([wll.md](../formats/wll.md)): VMP page (how it is drawn; — = nothing), decoration shape, special type, flags, automap symbol.
- **Clickable walls**: block sides whose wall type has a WLL *special* type: 1 clickable wall, 2 lever (to on), 3 lever (to off), 4 click runs the script only, 5 door or door switch (clicking it plays the door sound and runs the script), 6 niche (ScummVM `gui/gui_lol.cpp:1413-1440`). Clicking one runs the block's script with event 0x40.
- **Script entry points**: the level's scripts are entered by block number (0-1023) or by a special number: 0x400 level loaded, 0x401-0x403 script timers, 0x404 a monster died (`engines/kyra/script/script_lol.cpp:64-92`, `engines/kyra/engine/timer_lol.cpp:148`, `engines/kyra/engine/sprites_lol.cpp:203`). The description is built from the game functions the entry's code calls ([emc2_scripts.md](../emc2_scripts.md)), with constant arguments; `?` means the value is computed while the game runs.
- **Items and monsters placed**: calls of `createLevelItem` (0x11) and `initMonster` (0x38) with their arguments. Item names come from `ONETIME.INF` and `LANDS.ENG`.
- **Text ids**: the ids the scripts pass to message and dialogue functions; ids with bit 0x4000 are in `LANDS.<lang>`, others in the level's own text file.

## Events

| Bit | Event | Engine caller (ScummVM upstream) |
|-----|-------|----------------------------------|
| 0x0001 | party steps in | `engines/kyra/engine/scene_lol.cpp:665` |
| 0x0002 | party arrives (second movement path; also the `setNextFunc` script function) | `scene_lol.cpp:695`, `engines/kyra/engine/lol.cpp:947` |
| 0x0004 | party leaves | `scene_lol.cpp:664` |
| 0x0008 | party leaves (second path) | `scene_lol.cpp:694` |
| 0x0020 | a fireball ends in the block | `lol.cpp:2708` |
| 0x0040 | wall clicked | `engines/kyra/engine/scene_rpg.cpp:580`, `scene_lol.cpp:783`, `engines/kyra/gui/gui_lol.cpp:1446` |
| 0x0080 | item put down | `engines/kyra/engine/items_lol.cpp:374` |
| 0x0100 | item taken | `items_lol.cpp:382` |
| 0x0200 | a fireball passes | `lol.cpp:2577` |
| 0x0800 | a monster leaves the block | `engines/kyra/engine/sprites_lol.cpp:289` |
| 0x8000 | a thrown item hits | `items_lol.cpp:493` |

The difference between bits 1 and 2 (and 4 and 8) is the movement path that raises them; which player actions take which path is UNCONFIRMED.

## Levels

| Level | Script entries | Items placed | Monsters placed | Text ids |
|---|---|---|---|---|
| [1](level01.md) | 47 | 0 | 4 | 107 |
| [2](level02.md) | 38 | 15 | 11 | 44 |
| [3](level03.md) | 22 | 6 | 15 | 62 |
| [4](level04.md) | 46 | 8 | 13 | 33 |
| [5](level05.md) | 14 | 11 | 6 | 1 |
| [6](level06.md) | 35 | 8 | 12 | 23 |
| [7](level07.md) | 53 | 15 | 19 | 24 |
| [8](level08.md) | 43 | 13 | 13 | 22 |
| [9](level09.md) | 29 | 3 | 5 | 6 |
| [10](level10.md) | 64 | 4 | 16 | 31 |
| [11](level11.md) | 106 | 7 | 44 | 17 |
| [12](level12.md) | 64 | 4 | 5 | 42 |
| [13](level13.md) | 27 | 9 | 16 | 7 |
| [14](level14.md) | 60 | 6 | 8 | 7 |
| [15](level15.md) | 39 | 7 | 18 | 21 |
| [16](level16.md) | 38 | 11 | 4 | 16 |
| [17](level17.md) | 46 | 10 | 27 | 8 |
| [18](level18.md) | 31 | 22 | 32 | 14 |
| [19](level19.md) | 28 | 5 | 4 | 5 |
| [20](level20.md) | 64 | 7 | 4 | 10 |
| [21](level21.md) | 36 | 6 | 32 | 4 |
| [22](level22.md) | 45 | 29 | 25 | 44 |
| [23](level23.md) | 125 | 3 | 43 | 13 |
| [24](level24.md) | 46 | 1 | 30 | 19 |
| [25](level25.md) | 6 | 0 | 28 | 0 |
| [26](level26.md) | 51 | 16 | 34 | 16 |
| [27](level27.md) | 91 | 4 | 26 | 10 |
| [28](level28.md) | 81 | 6 | 13 | 42 |
| [29](level29.md) | 100 | 5 | 15 | 11 |
