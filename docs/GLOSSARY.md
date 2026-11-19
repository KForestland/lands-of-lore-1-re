# Glossary

Words used across these pages, in plain terms. Format names link to their page.

## Shared words

These words mean the same thing in the notes for all three Lands of Lore games.

| Term | Meaning |
|------|---------|
| Original | The released game's own files and program. Every fact in this repository is about the original game. |
| CONFIRMED / UNCONFIRMED | CONFIRMED: proved from the program code or the files. UNCONFIRMED: a reading not yet proved. |
| Answered / Mostly answered / Partly answered | The state words of [open questions](OPEN_QUESTIONS.md). *Answered*: nothing is left to settle from the files or the program. *Mostly answered*: the main question is settled; named details remain. *Partly answered*: part is settled; the main point is open. A row that says 'answered for' a setup (one renderer, one device) counts as answered for that setup only. |
| Native | In or from the original game program, as opposed to a reimplementation. |
| Open question | A numbered question on the [open-questions page](OPEN_QUESTIONS.md). |
| Archive | A file that holds many pieces of game data. |
| Entry | One piece of data stored inside an archive. |
| Level | One place the player walks through, stored as its own set of files. |
| Level sheet | One page per level, written by a tool from that level's files. |
| Schematic | A top-down line drawing of a level from its map data, with no game pixels. |
| Script | Commands the game runs for a level, an item, or a cut-scene. |
| Opcode | The number that begins one script command and selects what it does. |
| Event | A script that runs when something happens, such as a click, a step, or a timer. |
| Item | An object the player can carry, or that a level places in the world. |
| Creature | A living opponent or other character placed in a level. Monster means the same on these pages. |
| Placement | One recorded place where a level puts an item, a creature, or another object. |
| Save slot | One file the original game wrote for a game in progress. Tools may read it; this repository does not store it. |
| Probe | One check that needs the original game running. |
| Rating | The four counted lines near the top of the README, written by `tools/rating.py`. |
| Files read | A file whose every byte a tool here assigns to a known header, directory, entry or other named part; what is inside an entry may still be only partly understood. Files the game writes into the data folder while it runs are added to the total and count as read only if a reader walks them. Which folder is counted: [how we rate](HOW_WE_RATE.md). |
| History page | A page marked **History** at its top: an older note kept as a record. The rating does not count it; where it differs, the current pages are right. |
| File offset | The position of a byte in a file on disk. |
| Spell | A magic effect the player casts. Its cost is stored in the game's tables. |
| Dialogue | Lines a character says, or that the game prints. |
| Music | The game's songs. A music tool can list or convert them. The tools do not play sound. |
| Combat | How an attack is resolved: whether it hits, and what the hit changes. |
| Hash | A number computed from other bytes. A file hash identifies a whole file. A name hash stands in for a file name. |
| LCW, format 80 | Westwood's byte-oriented compression, also called format 80. |

## Editions and sources

| Term | Meaning |
|------|---------|
| CD edition | The CD-ROM release with spoken dialogue (version CD1.02). Read from its `DATA/` folder. ScummVM calls it the "talkie" version. |
| Floppy edition, LANDSoL | The English floppy release, without speech, data split into `CHAPTER1.PAK` … `CHAPTER8.PAK`. "LANDSoL" is the name of the folder the copy was read from. |
| ScummVM | Open-source program that runs many classic games, including this one, by reimplementing their engines. Its *Kyra* engine (named after Westwood's *Legend of Kyrandia*) runs Lands of Lore. Its source code is the main written reference used here; citations point at upstream commit `3b4db303`. |
| Closure memo | `docs/closure_memo.md`, an older summary kept as history; the format pages correct it. |
| Checked independently | A second program, written separately, gave the same result on the same files. |
| DATA folder | The directory of this game's data files, which the tools read. Set `LOL1_DATA` to it. A DAT file, below, is an area's decoration table, not this folder. |

## Files and containers

| Term | Meaning |
|------|---------|
| [PAK](formats/pak.md) | This game's archive. Almost all game data lives in PAKs. |
| [TLK](formats/tlk.md) | CD speech archive: 30 files, `00.TLK` … `29.TLK`; a PAK of VOC sound files. |
| Member | These pages' word for an entry: one file inside a PAK. |
| [Frame4](formats/lcw.md) | ScummVM's name (`decodeFrame4`) for LCW compression, used here for picture and map files. |
| Bitmap container | The 10-byte header plus optional palette used by CPS files and also by CMZ, VCN, VMP and most SHP files ([cps.md](formats/cps.md)). |
| Chunk, IFF, FORM | A named block inside a larger file. This game uses an IFF layout: a `FORM` header, a type (`EMC2`, `AVFS`, `XDIR`), then those chunks. Used by scripts, TIM files and music. |
| MZ executable | A DOS program file (`MAIN.EXE`). Tables of game numbers sit inside it ([executable_tables.md](executable_tables.md)). |
| LE (Linear Executable) | A 32-bit program format; here, Windows drivers placed after an MZ stub. |
| FBOV overlay | Westwood's block of overlay code stored after the MZ image of a program; the game loads it into memory while running, so its code has no fixed address. |
| Far pointer | A DOS memory address of two 16-bit words (offset, segment). |
| [ENG, FRE, GER](formats/text.md) | Text files, one set per language. Each is a string table. `LANDS.<lang>` holds the global strings and `LEVELnn.<lang>` one level's strings. The CD has 30 files per language; the floppy has only the ENG files. |
| [Loose files](formats/loose.md) | Files in the CD `DATA` folder that are neither a PAK nor a `NN.TLK` archive. `tools/lol1_loose.py` walks 25 of the 37 to the last byte; 12 stay open. |

## Pictures and sound

| Term | Meaning |
|------|---------|
| [CPS](formats/cps.md) | A full-screen 320 x 200 picture. |
| [SHP](formats/shp.md) | A set of sprites (monsters, items, wall decorations, portraits). Each sprite is one picture, called a shape. |
| [WSA](formats/wsa.md) | An animation: a first picture, then the differences (deltas) to each next frame. |
| [VOC](formats/voc.md) | A sound sample (Creative Voice File). |
| WAV | A standard sound file (`.wav`). `tools/voc_reader.py --wav` writes one from a VOC; the tools do not play it. |
| MIDI | A standard music file (`.mid`). The music tools can write one; they do not play it. |
| [XMI, C55, ADL, PCS](formats/music.md) | Music for different sound devices: XMI for a MIDI device such as the MT-32, C55 the XMIDI set for General MIDI or Roland GS, ADL for AdLib, PCS for the PC speaker. What C55 stands for is open (an [open question](OPEN_QUESTIONS.md)). |
| [PAL, COL](formats/palette.md) | A table of colours the pictures use. In this game, 256 colours, 3 bytes each, on the VGA 0-63 scale. |
| [FNT](formats/fnt.md) | A bitmap font. |
| [TLC](formats/tlc.md) | CD-only tables for drawing see-through colours. |

## Levels and the 3D view

| Term | Meaning |
|------|---------|
| Level files | This game numbers levels 1-29. Files sit in `Lnn.PAK` on the CD (`CHAPTERn.PAK` on the floppy): `LEVELn.CMZ`, `.WLL`, `.INF`, `.INI`, `.XXX`, `LEVELnn.TLC`, text. |
| Block, square | One cell of a level's 32 x 32 grid. Block number = x + y x 32. |
| [CMZ](formats/cmz.md) | A level's map: for every block, four *wall types* (north, east, south, west). |
| Wall type | A number 0-255 meaning what is on this side of this block: nothing, plain wall, door, switch, decoration. Its meaning is set per level by the WLL file. |
| Switch | A wall the player clicks to run a script, often to move a door. |
| Door | A wall that can open. |
| Light | The brightness of the view. This game tracks it with lamp oil and a timer. |
| [WLL](formats/wll.md) | A level's table of wall types: how each is drawn, its flags, its automap symbol. |
| Area | The tile and decoration set a level uses (KEEP, FOREST1, CAVE1, …). |
| [VCN](formats/vcn_vmp.md) | An area's small 8 x 8 picture tiles. |
| [VMP](formats/vcn_vmp.md) | How those tiles are arranged into the floor/ceiling and into each *wall page*. |
| Wall page | One set of tile layouts for a kind of wall seen at every distance and angle. |
| [DAT](formats/dat.md) | An area's decoration table: which shapes to draw where for each decoration. |
| [XXX](formats/xxx.md) | A level's automap legend (named places and symbols on the map screen). |
| Automap | The game's map screen. Each wall type has an automap symbol in the WLL file, and the XXX file adds the level's named places. |

## Scripts and rules

| Term | Meaning |
|------|---------|
| [INF, INI, EMC2](formats/emc2.md) | Level scripts in Westwood's EMC2 bytecode. `LEVELn.INI` runs when the level loads; `LEVELn.INF` holds its event handlers; `ONETIME.INF` defines all items; `ITEM.INF` holds item events. Details: [emc2_scripts.md](emc2_scripts.md). |
| Script function, sysCall | A numbered game action a script can call (192 of them, e.g. 0x09 load level graphics). |
| Game flag | A numbered on/off value scripts set and test (e.g. flag 357 on level 22). |
| [TIM](formats/tim.md) | A small script that plays a cut-scene or conversation: animations, text, speech. Its code chunk is `AVTL`. |
| TIM command, nested function | A TIM instruction (0x00-0x1E); command 0x19 calls a second list of game functions. |
| Script entry | A starting point in a level's script. An INF entry is named by its block number or by a special number (`0x400` level loaded, `0x401`-`0x403` timers, `0x404` a monster died). "INI entry 1" is entry 1 of the `LEVELn.INI` script, which runs when the level loads. |
| Type slot | The monster type a placement uses. The level's INI script first defines the type (function 0x3F); function 0x38 `initMonster` then places a monster of that type ([emc2_scripts.md](emc2_scripts.md)). |
| Facing | The direction the party or a creature faces, stored as a number. Scripts pass it to `initMonster` and `loadNewLevel`; a save stores the party's. |
| Hit code | Result of an attack roll: 0 miss, 1 hit, 2 critical ([game_rules.md](game_rules.md)). |
| Fixed point x/256 | Many game factors are stored so that 256 means 1.0 (e.g. 384 = 1.5). |
| Monster mode | A monster's current behaviour state (0-16): waiting, chasing, fleeing, dying … ([game_rules.md](game_rules.md)). |
| Save file | The original name of a save slot is `_SAVEnnn.DAT`. Layout: [savegame_format.md](savegame_format.md). |
| `_LEVELn.TMP` | A snapshot of one level that the original program writes while it runs: map changes, monsters and flying objects. It is not shipped. A save slot holds a copy of it. The four studied here came from the floppy edition ([savegame_format.md](savegame_format.md)). |
