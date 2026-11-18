# How the game works

A short tour for a reader who has the game and wants to know how it runs: which files it reads, what drives each level, and how the rules are computed. Each section links to the detailed page with the evidence. Terms: [glossary](GLOSSARY.md).

## The program and its data

The game program is `MAIN.EXE`. On the CD it sits inside the install archive `WESTWOOD.001` and again in `DATA/HARDRIVE`; on the floppy edition it is a loose file ([executable_tables.md](executable_tables.md)). It holds the code and a few fixed tables: the 17 spells, the 9 playable characters' starting values, the experience needed for each level, and difficulty factors.

Everything else is data in PAK archives ([formats/pak.md](formats/pak.md)): pictures, sprites, animations, sounds, music, text in three languages, and one set of files per level.

## Starting the game

At start-up the program runs the script `ONETIME.INF`. It calls one script function 285 times, once per item type, to define every item in the game: name, picture, type, might, protection and so on ([executable_tables.md](executable_tables.md#item-types-and-item-properties)). Item behaviour (what happens when one is used) lives in `ITEM.INF`.

## Entering a level

Each of the 29 levels has its own scripts. When a level loads, its `LEVELn.INI` script runs ([formats/emc2.md](formats/emc2.md)). For level 1 it:

- loads the wall tiles (`KEEP.VCN`/`.VMP`, [formats/vcn_vmp.md](formats/vcn_vmp.md)) and the map (`LEVEL1.CMZ`, [formats/cmz.md](formats/cmz.md));
- loads door and decoration graphics (`KEEPDOOR.SHP`, `KEEP.SHP` with `KEEP.DAT`, [formats/dat.md](formats/dat.md));
- loads the monsters' sprites and defines their statistics (79 such definitions across the game);
- loads the level's text file and sounds.

The map is a 32 x 32 grid. Each square stores four *wall types* (north, east, south, west); the level's `LEVELn.WLL` file says what each wall type is: plain wall, door, switch, decorated wall, nothing ([formats/wll.md](formats/wll.md)). The 3D view is drawn from those wall types: each one picks a page of tile layouts in the VMP file, whose tiles come from the VCN file.

## While you play

`LEVELn.INF` holds the level's event handlers. The engine calls them when you step on a square, click a wall, use an item and so on. Handlers call script functions to change walls (open a door), set and test game flags, start conversations, give items, move monsters and play sounds. All 192 functions are listed in [emc2_scripts.md](emc2_scripts.md).

Example: on level 22, a click while a certain wall is showing switches the walls to a second tile set (`YVEL2`) and sets game flag 357, so the switch survives a reload ([unknowns/04_yvel2.md](unknowns/04_yvel2.md)).

Conversations and cut-ins are TIM scripts: they play WSA animations frame by frame, show text and choices, and play speech ([formats/tim.md](formats/tim.md)). On the CD, speech comes from the level's `NN.TLK` archive ([formats/tlk.md](formats/tlk.md)).

## Combat

([game_rules.md](game_rules.md#combat); the parts below were checked in the original program code)

- Dice: "n d s" rolls n dice of s sides. Each die is 1 + (a 15-bit random number x s / 32768).
- To hit: roll 1d100. A roll at or above `100 − (skill level + modifier)` is a critical (hit code 2). Otherwise a roll below the defender's evade threshold misses (0), anything else hits (1).
- Damage: each of eight damage categories (item might x attacker factor x target factor, as fractions of 256) is summed; the attack then rolls 2 dice of that sum.
- Armour: unless the hit is critical, the target's protection reduces damage by up to 217/256 (`256 − min(217, protection x 128 / damage)`, then x/256), never below 2.

## Experience and magic

Experience levels start at 0, 500, 1500, 5000, 25000, 50000, 80000, 120000, 180000 and 270000 points, the same in both editions ([executable_tables.md](executable_tables.md)). On each new level a character gains hit points, and magic points for the mage skill; the amounts are so far taken from ScummVM ([game_rules.md](game_rules.md#experience-and-skills)).

Spells cost magic points per rank (for example Spark 5 / 10 / 15 / 25) and do fixed damage inputs per rank, stored in the program (Spark 7 / 15 / 25 / 60, Fireball 20 / 40 / 80 / 100) ([game_rules.md](game_rules.md#magic)). What each spell does beyond those numbers is so far taken from ScummVM.

## Monsters

Each monster has a *mode*: waiting, walking to a place, watching, chasing, recovering after an attack, fleeing, dying … ([game_rules.md](game_rules.md#monster-behavior)). A table in the program says which checks run in each mode; the transitions between modes are so far taken from ScummVM.

## Light and time

The lamp burns oil every 360 ticks of 1/60 second, and the screen darkens in steps as the oil runs low; characters regenerate every 1200 ticks ([game_rules.md](game_rules.md#light-and-time)). These timings are ScummVM's and still need a check in the original program ([Q7](OPEN_QUESTIONS.md)).

## Saving

An original save (`_SAVEnnn.DAT`) holds the four party members, the game state (position, inventory, game flags, money, spells), 400 item records and a 2500-byte snapshot for each of 30 levels ([savegame_format.md](savegame_format.md)).
