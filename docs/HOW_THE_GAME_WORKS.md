# How Lands of Lore works

This guide follows the original DOS game from loading its files to saving
your progress. The linked pages give the original offsets and distinguish
native evidence from readings based on ScummVM. [Glossary](GLOSSARY.md)

## The program and its data

The game runs from `MAIN.EXE`. On CD the DOS executable is in
`WESTWOOD.001` and also appears loose under `DATA/HARDRIVE`. The floppy
edition has a loose `MAIN.EXE`. It holds the code and tables for spells,
character defaults, experience and difficulty. [Executable tables](executable_tables.md#locating-the-executables)

PAK archives hold level files, graphics, audio and text. The CD edition
also uses TLK archives for speech. [PAK directory](formats/pak.md) ·
[CD speech archives](formats/tlk.md)

## Starting the game

The original `ONETIME.INF` (CD `STARTUP.PAK`, floppy `GENERAL.PAK`) allocates 285 item types and supplies one
definition for each. A definition has a name ID, a shape, combat values
and an item-script entry. The separate `ITEM.INF` holds the event code
for items. [Item definitions and script loader](executable_tables.md#item-types-and-item-properties)

## Entering a level

Level scripts load the map and the art used to draw it. For example,
the first level's scripts load the KEEP wall tiles and define a monster
type. The map uses a 32 × 32 grid. Each block has four wall type bytes,
one per direction. A wall type selects a WLL record, which can refer to
a VMP tile layout and the tile pixels in the VCN file.
[Level 1 sheet](levels/level01.md) · [Monster definitions](executable_tables.md#monster-properties) ·
[Map blocks](formats/cmz.md) · [Wall types](formats/wll.md) · [Tile selection](formats/vcn_vmp.md)

## While you play

`LEVELn.INF` holds handlers for events such as entering a block,
clicking a wall or taking an item. An event runs an entry when its flag
shares a bit with the entry's mask. A handler can change walls, set
flags, give items and play sounds. In level 22 a click under the right
conditions loads the YVEL2 tile set and sets flag 357. The level loader
uses that flag when it loads the level again.
[EMC2 format](formats/emc2.md) · [EMC2 dispatch](emc2_scripts.md) · [Wall click tutorial](tutorial-one-event.md) ·
[YVEL2 event](unknowns/04_yvel2.md)

TIM commands can play animation frames, show text and choices, and
request speech. WSA files store changes between frames. The CD edition
carries speech clips in TLK archives. [TIM commands](formats/tim.md) ·
[WSA frames](formats/wsa.md) · [TLK speech](formats/tlk.md)

## Combat

The native hit test rolls once. A roll at or above the critical
threshold gives a critical hit. Below that, the defender's evade
threshold separates misses from ordinary hits. The game calculates
damage across eight categories. For a positive total `S`, the
standard item damage routine rolls two dice with `S` sides. Armour can
reduce a nonzero ordinary hit, with a minimum of two in that branch.
[Hit test, version differences and damage formulas](game_rules.md#combat)

## Experience and magic

The native experience thresholds start at 0, 500, 1,500 and 5,000 in
both editions. The HP and MP gains at each new level are **CONFIRMED** in both
native executables: Fighter `4d6` HP, Rogue `2d6` HP, Mage `1d6` HP
plus MP. They match ScummVM.
[Experience and skills](game_rules.md#experience-and-skills)

The program has tables for spell costs and separate routines for the
effects. For example, Fireball checks up to three blocks starting at
the party's block. It sends an event along the path and stops when the
wall or occupancy tests succeed. [Native spell effects](unknowns/07_native_rules.md#casting)

## Monsters, light and time

A monster's current mode selects what it does during an update. The
original code can change that mode before running its handler. For
example, a recent hit or successful visibility check can put a monster
into mode 7 (attack) when the corresponding mode flag allows it.
[Monster updates](unknowns/07_native_rules.md#monster-transitions)

The timer table schedules lamp oil use every 360 enabled ticks and
passive regeneration every 1,200. Both DOS editions run the game clock at
60 ticks per second, so 360 ticks is about 6 seconds and 1,200 about 20. The game can pause the gameplay timer while its separate
delay clock continues. [Lamp and regeneration](unknowns/07_native_rules.md#lamp-regeneration-and-the-clock) ·
[Native clock](unknowns/07_native_rules.md#native-tick-duration-and-pause)

## Saving

The original DOS save writer stores four character records, global
state, 400 item slots and 30 level snapshot slots of 2,500 bytes each.
A mask tells the loader which snapshots are populated. The layout comes
from the save code in both DOS executables and four level files
(`_LEVELn.TMP`) written by the original floppy program. No complete
original save file has been examined yet, so the end of the file and a
few skipped bytes are still **UNCONFIRMED**. One save written by either DOS
program, read against this layout, would settle them.
[Save layout](savegame_format.md) · [Unresolved save bytes](unknowns/17_native_save_fields.md#isolated-bytes)
