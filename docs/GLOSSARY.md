# Glossary

Words used across these pages, in plain terms. Format names link to their page.

## Editions and sources

| Term | Meaning |
|------|---------|
| CD edition | The CD-ROM release with spoken dialogue (version CD1.02). Read from its `DATA/` folder. ScummVM calls it the "talkie" version. |
| Floppy edition, LANDSoL | The English floppy release, without speech, data split into `CHAPTER1.PAK` … `CHAPTER8.PAK`. "LANDSoL" is the name of the folder the copy was read from. |
| ScummVM | Open-source program that runs many classic games, including this one, by reimplementing their engines. Its *Kyra* engine (named after Westwood's *Legend of Kyrandia*) runs Lands of Lore. Its source code is the main written reference used here; citations point at upstream commit `3b4db303`. |
| Closure memo | `docs/closure_memo.md`, a March 2026 summary written when this work was first called finished. Kept as history; the format pages correct it. |
| Native | In or from the original DOS program (`MAIN.EXE`), as opposed to ScummVM's reimplementation. "Checked natively" means the instructions in the original program were read (disassembled). |
| Checked independently | A second program, written separately, gave the same result on the same files. |
| CONFIRMED / UNCONFIRMED | CONFIRMED: checked on the game files (or in the original program code). UNCONFIRMED: taken from ScummVM or reasoning, not yet checked. |
| Q1 … Q18 | Numbered open questions, see [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). |

## Files and containers

| Term | Meaning |
|------|---------|
| [PAK](formats/pak.md) | Archive holding many files. Almost all game data lives in PAKs. |
| [TLK](formats/tlk.md) | CD speech archive, one per level (`01.TLK` …); a PAK of VOC sound files. |
| Member | One file inside a PAK. |
| [Frame4 / LCW](formats/lcw.md) | The compression used by Westwood games of the time ("format 80"). |
| Bitmap container | The 10-byte header plus optional palette used by CPS files and also by CMZ, VCN, VMP and most SHP files ([cps.md](formats/cps.md)). |
| IFF, FORM, chunk | A general file layout: a `FORM` header, a type (`EMC2`, `AVFS`, `XDIR`), then named chunks. Used by scripts, TIM files and music. |
| MZ executable | A DOS program file (`MAIN.EXE`). Tables of game numbers sit inside it ([executable_tables.md](executable_tables.md)). |
| Far pointer | A DOS memory address of two 16-bit words (offset, segment). |

## Pictures and sound

| Term | Meaning |
|------|---------|
| [CPS](formats/cps.md) | A full-screen 320 x 200 picture. |
| [SHP](formats/shp.md) | A set of sprites (monsters, items, wall decorations, portraits). Each one is a *shape*. |
| [WSA](formats/wsa.md) | An animation: a first picture and then the differences (*deltas*) to each next frame. |
| [VOC](formats/voc.md) | A sound sample (Creative Voice File). |
| [XMI, C55, ADL, PCS](formats/music.md) | Music for different sound devices: XMI for MIDI/MT-32, ADL for AdLib, PCS for the PC speaker; what C55 stands for is open (Q15). |
| [PAL, COL](formats/palette.md) | A palette: 256 colours, 3 bytes each, on the VGA 0-63 scale. |
| [FNT](formats/fnt.md) | A bitmap font. |
| [TLC](formats/tlc.md) | CD-only tables for drawing see-through colours. |

## Levels and the 3D view

| Term | Meaning |
|------|---------|
| Level | One map, numbered 1-29. Its files sit in `Lnn.PAK`: `LEVELn.CMZ`, `.WLL`, `.INF`, `.INI`, `.XXX`, `LEVELnn.TLC`, text. |
| Block, square | One cell of a level's 32 x 32 grid. Block number = x + y x 32. |
| [CMZ](formats/cmz.md) | A level's map: for every block, four *wall types* (north, east, south, west). |
| Wall type | A number 0-255 meaning "what is on this side of this block": nothing, plain wall, door, switch, decoration … Its meaning is set per level by the WLL file. |
| [WLL](formats/wll.md) | A level's table of wall types: how each is drawn, its flags, its automap symbol. |
| Area | The tile and decoration set a level uses (KEEP, FOREST1, CAVE1, …). |
| [VCN](formats/vcn_vmp.md) | An area's small 8 x 8 picture tiles. |
| [VMP](formats/vcn_vmp.md) | How those tiles are arranged into the floor/ceiling and into each *wall page*. |
| Wall page | One set of tile layouts for a kind of wall seen at every distance and angle. |
| [DAT](formats/dat.md) | An area's decoration table: which shapes to draw where for each decoration. |
| [XXX](formats/xxx.md) | A level's automap legend (named places and symbols on the map screen). |

## Scripts and rules

| Term | Meaning |
|------|---------|
| [INF, INI, EMC2](formats/emc2.md) | Level scripts in Westwood's EMC2 bytecode. `LEVELn.INI` runs when the level loads; `LEVELn.INF` holds its event handlers; `ONETIME.INF` defines all items; `ITEM.INF` holds item events. Details: [emc2_scripts.md](emc2_scripts.md). |
| Script function, sysCall | A numbered game action a script can call (192 of them, e.g. 0x09 load level graphics). |
| Game flag | A numbered on/off value scripts set and test (e.g. flag 357 on level 22). |
| [TIM](formats/tim.md) | A small script that plays a cut-scene or conversation: animations, text, speech. Its code chunk is `AVTL`. |
| TIM command, nested function | A TIM instruction (0x00-0x1E); command 0x19 calls a second list of game functions. |
| Hit code | Result of an attack roll: 0 miss, 1 hit, 2 critical ([game_rules.md](game_rules.md)). |
| Fixed point x/256 | Many game factors are stored so that 256 means 1.0 (e.g. 384 = 1.5). |
| Monster mode | A monster's current behaviour state (0-16): waiting, chasing, fleeing, dying … ([game_rules.md](game_rules.md)). |
| Save file | `_SAVEnnn.DAT` in the original game; layout in [savegame_format.md](savegame_format.md). |
