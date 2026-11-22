# Start here, by goal

<!-- suite-counts:begin -->
- **Original game files.** 54 checks with the required files and dependencies. Quick mode selects 52.
- **Synthetic data.** 130 unit tests.
<!-- suite-counts:end -->

[Format quick reference](QUICK_REFERENCE.md) pairs each documented game format with a command and its evidence.

Use Python 3.10 or later and your own copy of *Lands of Lore: The Throne of Chaos* for DOS. Install Pillow and Capstone before running the full check. Point the tools at the folder holding `GENERAL.PAK` (on the CD the `DATA` folder, on the floppy the install folder). Six checks skip comparison with the CD tables when reading the floppy edition.

```bash
export LOL1_DATA=/path/to/your/LOL1/DATA
python3 tools/check_all.py
```

Words you do not know are in the [glossary](GLOSSARY.md). Short worked commands, with the first lines they print, are in the [cookbook](COOKBOOK.md). Run the examples from the clone after `mkdir -p ../lol1-out`; they write there, outside the clone, so nothing from your game ends up in the repository. To contribute, see [CONTRIBUTING](../CONTRIBUTING.md).

## I want to read the level maps

0. Start with the level's sheet in [levels/](levels/README.md): how the level is put together, block by block (made by `python3 tools/level_report.py --level N`).
1. Read [formats/cmz.md](formats/cmz.md) (the 32 x 32 grid of wall types) and [formats/wll.md](formats/wll.md) (what each wall type is).
2. Draw a map: `python3 tools/level_renderer.py --level 1 --out ../lol1-out --schematic` (a plain drawing) or without `--schematic` (with the game's wall tiles).
3. See which tile set, decorations and palette each level uses: `python3 tools/tileset_mapper.py`.
4. Named places on the automap: [formats/xxx.md](formats/xxx.md), `python3 tools/xxx_reader.py LEVEL1.XXX` (prints each place's name, e.g. FOUNTAIN).

## I want to look at pictures, sprites and animations

- Full-screen pictures: [formats/cps.md](formats/cps.md), `python3 tools/cps_reader.py PARCH.CPS --out ../lol1-out/parch.png`.
- Sprites: [formats/shp.md](formats/shp.md), `python3 tools/shp_renderer.py GUARD.SHP --level 1 --out ../lol1-out/guard` (`--level` picks the palette of a level that uses the sprite).
- Animations: [formats/wsa.md](formats/wsa.md), `python3 tools/wsa_extract.py ESCAPE.WSA --out ../lol1-out/escape --all`.
- Wall tiles: [formats/vcn_vmp.md](formats/vcn_vmp.md), `python3 tools/vcn_vmp_reader.py KEEP --out ../lol1-out/keep_tiles.png`.
- Fonts: [formats/fnt.md](formats/fnt.md), `python3 tools/fnt_reader.py FONT9P.FNT --out ../lol1-out/font.png`.

## I want to listen to sound and speech

- [formats/voc.md](formats/voc.md): `python3 tools/voc_reader.py VOC.PAK:1BOLTC.VOC --out ../lol1-out/bolt.wav`.
- CD speech is in `NN.TLK` files ([formats/tlk.md](formats/tlk.md)): `python3 tools/pak_reader.py list 01.TLK`, then `python3 tools/voc_reader.py 01.TLK:000_0.01 --out ../lol1-out/line.wav`.
- Music: [formats/music.md](formats/music.md), `python3 tools/xmi_to_midi.py LORE01A.XMI --out ../lol1-out/midi` (standard MIDI files you can play).

## I want to read the game's text

- [formats/text.md](formats/text.md): `python3 tools/decode_dialogue.py LEVEL01.ENG` (also `.FRE`, `.GER`).

## I want to understand the scripts

1. [formats/emc2.md](formats/emc2.md), then [emc2_scripts.md](emc2_scripts.md) (every opcode and all 192 script functions).
2. Disassemble a level script: `python3 tools/emc2_decompile.py L01.PAK --entry LEVEL1.INI` (CD; on the floppy use `CHAPTER1.PAK`) (bare PAK names are looked up in `$LOL1_DATA`). Disassemble all 60 scripts as a test: `python3 tests/test_emc2_corpus.py`.
3. [Follow one wall click](tutorial-one-event.md) through its original EMC2 entry.
4. Cut-scene scripts: [formats/tim.md](formats/tim.md) and [unknowns/06_tim_opcodes.md](unknowns/06_tim_opcodes.md).

## I want to understand the game rules

[HOW_THE_GAME_WORKS.md](HOW_THE_GAME_WORKS.md) is the overview; [game_rules.md](game_rules.md) has the formulas (combat, magic, experience, monsters, light, time) and [executable_tables.md](executable_tables.md) the tables inside `MAIN.EXE` (spells, characters, experience levels).

## I want to read or change a save game

[savegame_format.md](savegame_format.md) lays out the original `_SAVEnnn.DAT` files and ScummVM's saves field by field. Read one with `python3 tools/save_reader.py FILE` (original `_SAVEnnn.DAT`, `_LEVELn.TMP`, or a ScummVM save; `--json` writes every field). To change a copy of a save, use `tools/save_edit.py` (see the README); the offsets in the page are what one would need. [Edited saves](EDITED_SAVES.md) lists the runs where the original game loaded a hand-edited copy, each with a link to its byte table.

## I want to know which edition I have

[edition_comparison.md](edition_comparison.md) compares the CD and floppy editions and shows the file hash ScummVM uses to recognise each.

## I want to help

Pick an open question in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). See [STATUS.md](STATUS.md) for what is done and how it was checked. [CORRECTIONS.md](CORRECTIONS.md) lists what these pages got wrong and how it was caught.
