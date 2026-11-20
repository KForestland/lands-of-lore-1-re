# Lands of Lore I: file formats and game rules

**New here?** Start with the [first ten minutes](docs/FIRST_TEN_MINUTES.md): download, one command, a level picture on your screen.

[Identify your edition](docs/EDITIONS.md) by the sizes and checksums of your own files. [See unused content and development leftovers](docs/UNUSED.md).

*Lands of Lore: The Throne of Chaos* is a first-person role-playing game for DOS by Westwood Studios (1993; CD-ROM edition with speech later). This repository explains how its data files and its rules work, and gives you Python tools that read every file type from your own copy of the game.

It contains documentation, tools and small tables of numbers. It contains no game files and no dumps of game pictures, sounds or text; the only game-derived images are five small ones: three examples in `examples/` and two level schematics in `docs/images/`.

## At a glance

- **What this is:** documentation of every type of data file and the main rules of the original 1993 DOS game (CD and floppy editions), checked against the game files and the original program.
- **What you can do today:** read every file type with a tool (pictures, sprites, animations, sound, speech, music, fonts, text, maps, scripts, saves), draw any level, disassemble every level script, and look up how combat, magic and monsters work.
- **Using git?** The [quick start with git](#quick-start-with-git-for-people-who-use-git) below, then [Start here, by goal](docs/START_HERE.md), [How the game works](docs/HOW_THE_GAME_WORKS.md) or the [worked example](docs/tutorial-one-event.md).
- **Recipes:** [cookbook](docs/COOKBOOK.md), short recipes with the command and the first lines it prints.
- **Change the game, safely:** [change a number in your own copy](#change-a-number-in-your-own-copy) with the mod kit, share it as a small [patch](docs/formats/patch.md) that can be undone, or change a field in a copy of a save; your game folder is only read.
- **Patches:** [original faults and the item-name spelling patch](patches/README.md).
- **What is still unknown:** a few details, listed in [open questions](docs/OPEN_QUESTIONS.md) and counted in the [rating](#rating). Some questions need a test in the running original game (a *probe*); [NEEDS_A_RUNNING_GAME](docs/NEEDS_A_RUNNING_GAME.md) lists them and which are answered. Some probes were also tried on [edited saves](docs/EDITED_SAVES.md), copies of a game-written save with a few bytes changed.
- **What changed lately:** [what's new](docs/WHATS_NEW.md), newest first.
- **What we got wrong:** [corrections](docs/CORRECTIONS.md), each with how it was caught and the commit that fixed it.
- **The three games:** [LoL1](https://github.com/KForestland/lands-of-lore-1-re) · [LoL2](https://github.com/KForestland/lands-of-lore-2-re) · [LoL3](https://github.com/KForestland/Lands-of-lore-3-re) ([what they share](docs/series-formats.md), [how the engine changed](docs/engine-evolution.md), [how they gate progress and scale numbers](docs/series-progress-and-numbers.md)).

![Level 12 drawn by tools/level_renderer.py --schematic](docs/images/level12_schematic.png)

*Level 12 drawn from its map file alone (`tools/level_renderer.py --level 12 --schematic`): open squares light, walls dark, doors and switches orange, decorated walls marked red.*

## Rating

These are counts of work done, not a percentage of how complete the project is. They are produced by `tools/rating.py` on the English CD copy; [how we rate](docs/HOW_WE_RATE.md) explains each line and what it does not claim.

<!-- rating:begin -->
- **Files read:** 199 of 199 files in the CD `DATA` folder (289.0 of 289.0 MiB) have their whole layout read by a tool here: every byte belongs to a known header, directory or entry (what is inside an entry may still be only partly understood).
- **Rules traced:** the pages mark 563 statements CONFIRMED (proved from the program code or the files) and 98 UNCONFIRMED (a reading not yet proved), on 106 current pages; old notes kept as history are not counted.
- **Seen in the running game:** 1 of 6 probes that need the original game running are answered (a question can have more than one probe); 0 of them rest on edited saves only.
- **Open questions:** 18 numbered questions: 12 answered, 4 mostly answered, 2 partly answered.
<!-- rating:end -->

## Quick start with git (for people who use git)

Use Python 3.10 or later and your own copy of the DOS game (CD or floppy edition). Install Pillow for the image tools and Capstone for the executable reference scan. The full check uses both packages.

```bash
git clone https://github.com/KForestland/lands-of-lore-1-re.git
cd lands-of-lore-1-re
python3 -m venv .venv && . .venv/bin/activate
python3 -m pip install -r requirements.txt
export LOL1_DATA="/path/to/your/LOL1/DATA"      # the folder holding GENERAL.PAK (CD: DATA inside the install folder, which also holds INSTALL.EXE and README.ENG that two checks read; floppy: the install folder)
python3 tools/check_all.py --quick              # lists the checks it skips
python3 tools/check_all.py                      # full suite of 52 checks
python3 -m unittest discover -s tests
python3 tools/level_renderer.py --level 1 --out ../maps/ --schematic
python3 tools/decode_dialogue.py LEVEL01.ENG --index 0
python3 tools/full_report.py --out "../lol1-out/report"
```

On the reference CD installation, the full suite took about 102 seconds and `--quick` about 16; on the floppy edition, about 59 and 19. Quick mode skips the Frame4, WSA and SHP re-encoding check and the progression walk, and prints each skip. Each run prints the time per check and the total. [Check audit](docs/CHECK_AUDIT.md)

The dialogue command prints `[0] Welcome to Gladstone Keep.  King Richard awaits you in the throne room.` The report command writes an inventory, level sheets and text counts to the named folder. On Windows, use `py -3 -m venv .venv` and `.\.venv\Scripts\python.exe` in place of `python3`. Set `$env:LOL1_DATA = 'D:\Games\LoL1\DATA'` in PowerShell, or pass `--data` with a quoted folder path to each tool.

## Tools at a glance

[Edit walls and items on a level plan](docs/LEVEL_EDITOR.md). The editor builds a checked copy from your own game files.

[How a level is put together](docs/HOW_A_LEVEL_IS_PUT_TOGETHER.md) · [Numbers at a glance](docs/NUMBERS.md)

What you can look at with your own copy of the game. Run from the clone with `export LOL1_DATA=/path/to/your/LOL1/DATA` (CD) or the floppy install folder; pictures and files go only where you point them (here `../lol1-out`, outside the clone; make it first with `mkdir -p ../lol1-out`). Every tool and option is in [`tools/README.md`](tools/README.md), with a table of every format and how to look at it.

| To see | Command |
|---|---|
| A level as a map | `python3 tools/level_renderer.py --level level01 --schematic --out ../lol1-out/schematic` |
| A level's walls in their colours | `python3 tools/level_renderer.py --level level01 --out ../lol1-out/wall-map` |
| A level sheet (scripts, items, monsters) | `python3 tools/level_report.py --level 1 --out ../lol1-out` |
| A monster in its colours | `python3 tools/shp_renderer.py GUARD.SHP --level 1 --out ../lol1-out/guard` |
| An area's walls as the game draws them | `python3 tools/vcn_vmp_reader.py KEEP --walls-png ../lol1-out/keep_walls.png` |
| A full-screen picture | `python3 tools/cps_reader.py PARCH.CPS --out ../lol1-out/parch.png` |
| An animation | `python3 tools/wsa_extract.py KNOWLTK1.WSA --pal-from KNOWLTK.CPS --out ../lol1-out/knowltk1` |
| A palette and its swatch | `python3 tools/palette_reader.py PARCH.CPS --out ../lol1-out` |
| A line of game text | `python3 tools/decode_dialogue.py LEVEL01.ENG --index 0` |
| A level script | `python3 tools/emc2_decompile.py L01.PAK --entry LEVEL1.INI` |
| A cut-scene script, command by command | `python3 tools/parse_tim.py --list AUTOMAP.TIM` |
| The tables inside the game program | `python3 tools/exe_tables.py --table difficulty --image cd` |
| A sound effect as WAV | `python3 tools/voc_reader.py VOC.PAK:1BOLTC.VOC --out ../lol1-out/bolt.wav` |
| Music as standard MIDI | `python3 tools/xmi_to_midi.py LORE01A.XMI --out ../lol1-out/midi` |
| A saved game you made | `python3 tools/save_reader.py /path/to/your/save` |

## Change a number in your own copy

The [mod kit](tools/README.md#modkitpy) turns the game's tables into files you can edit, and the [patch tool](docs/formats/patch.md) turns your change into a small patch file that can be applied and undone. The tools only read your game folder; everything they write goes into new folders you name, outside the game and this repository. Try changes on a **copy** of the game, never on the folder you play from. Patches must not remove or bypass copy protection.

Type these in this repository's folder. Put quotes around paths with spaces. On Windows type `py -3` instead of `python3`, and `\` instead of `/` inside paths if you like; copy folders with Explorer. Each command ends with one summary line, or one sentence saying what is wrong.

1. Unpack: `python3 tools/modkit.py unpack "/path/to/LoL1/DATA" "my mod work"`. Give the folder holding the PAK archives: the CD's `DATA` folder, or the floppy game folder.
2. Change one number: the item definitions are in the start-up script. Open the file in `my mod work/edits/` whose name ends in `_STARTUP.PAK_ONETIME.INF.json` (floppy: ends in `_GENERAL.PAK_ONETIME.INF.json`; the number in front may differ on your copy) in a text editor and search for `"might"`. The second match is in a row that reads `"argument": 8`; change the 8 to 9 (an item's might, [numbers](docs/NUMBERS.md)). Change nothing else.
3. Build and check: `python3 tools/modkit.py build "/path/to/LoL1/DATA" "my mod work" "my mod output"`, then the same with `verify`. Both end with `62 archives or loose tables, 1 changed (STARTUP.PAK)` (floppy: `11 ..., 1 changed (GENERAL.PAK)`).
4. Make the patch: `python3 tools/patch.py make --data "/path/to/LoL1/DATA" "my mod output" --title "Stronger item" --out "stronger item.json"` prints `make: data patch with 1 change in 1 file (STARTUP.PAK) ...`.
5. Copy your whole game folder to a new folder, for example `LoL1 test copy`.
6. Apply the patch to the copy: `python3 tools/patch.py apply --data "/path/to/LoL1 test copy/DATA" "stronger item.json" --out "patched files"`. Copy everything in `patched files` except `undo.json` into the copy's `DATA` folder (floppy: the copy itself), replacing the files there.
7. Read it back: `python3 tools/modkit.py unpack "/path/to/LoL1 test copy/DATA" "check work"`; the same file in `check work/edits` now says 9. Play the copy to try it.
8. Undo: `python3 tools/patch.py apply --data "/path/to/LoL1 test copy/DATA" "patched files/undo.json" --out "restored files"`, then copy the files in `restored files` (except `undo.json`) into the copy in the same way. The copy is then byte for byte the original again.

A saved game can be changed in a copy too: `python3 tools/save_edit.py set "/path/to/your/_SAVE001.DAT" money 5000 --out "my edited save.DAT"` prints the old and the new value. More in the [cookbook](docs/COOKBOOK.md#share-a-change-as-a-patch).

## What you get

[Walk through one level from its map to its exit](docs/TOUR.md). Search the [JSON documentation index](docs/index.json) by page, question or tool. What each format writer proves, byte-identical or decode-identical, is on one page: [round trip](docs/ROUND_TRIP.md).

- **One page per file format** in [`docs/formats/`](docs/formats/README.md): layout, a worked example with real bytes, which part of the game reads it, and how it was checked.
- **How the game works**: [`docs/HOW_THE_GAME_WORKS.md`](docs/HOW_THE_GAME_WORKS.md), with the details in [scripts](docs/emc2_scripts.md), [rules](docs/game_rules.md), [tables in the program](docs/executable_tables.md) and [save files](docs/savegame_format.md).
- **Tools** in [`tools/`](tools/README.md): a reader for every format, map and sprite renderers, a script disassembler, text and sound extractors. Each has `--help`, writes only where you tell it, and the readers have a `--check` that tests it against every file of its kind (the script disassembler is tested by `tests/test_emc2_corpus.py` instead).
- **[Level sheets](docs/levels/README.md)**: one page per level, made from its files: graphics, wall types, clickable walls, every script entry with a one-line description, items and monsters placed, automap legend.
- **[Start here, by goal](docs/START_HERE.md)** and a **[glossary](docs/GLOSSARY.md)**.

## Status

Full table with evidence: [`docs/STATUS.md`](docs/STATUS.md). "Q7" and the like are numbered questions in [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md); format names (CMZ, WLL, EMC2, TIM and so on) are explained in the [glossary](docs/GLOSSARY.md).

| Area | State |
|------|-------|
| Archives, compression, pictures, sprites, animations, sound, fonts, text | Documented, readers, checked on every file of both editions read |
| Level maps (CMZ, WLL, VCN/VMP, decorations, automap legend) | Documented, readers and renderer, checked on every file; Q3 and Q11 answered; level 24 has extra bytes whose purpose cannot be found in the files |
| Level and item scripts (EMC2), cut-scene scripts (TIM) | Documented with full opcode and function tables; all 60 scripts of both editions and the 139 TIM files of the CD checked |
| Tables inside the program, save files | Documented and checked in both executables and on save files |
| Game rules (combat, magic, experience, monsters, light, time) | Traced in both original executables: combat, spells, timers, regeneration, lamp oil, monster modes; clock CONFIRMED at 60 ticks per second; WLL bit 0x40 and a few monster details open (Q7) |
| Music | XMIDI (XMI, C55, PCS) converts to standard MIDI; the AdLib (ADL) layout is documented field by field (Q15) and `adl_to_midi.py` turns ADL tracks into a MIDI file of notes |

Two editions were read: the CD-ROM edition with speech (version CD1.02) and an English floppy edition. See [`docs/edition_comparison.md`](docs/edition_comparison.md).

## Repository layout

- [`docs/`](docs): format pages, how the game works, status, open questions, glossary
- [`docs/levels/`](docs/levels/README.md): one sheet per level
- [`docs/unknowns/`](docs/unknowns): detailed notes on the numbered questions (answered and open)
- [`tools/`](tools/README.md): readers, renderers and extractors
- [`tests/`](tests): synthetic reader tests (`python3 -m unittest`, no game files) and the script disassembler's corpus test (needs game data)
- [`data/`](data): tables produced by the tools (inventories, wall tables, counts)
- [`examples/`](examples): three small example outputs, checked against today's tools by `example_images.py`

[`docs/closure_memo.md`](docs/closure_memo.md), [`docs/repo_scope.md`](docs/repo_scope.md) and [`docs/level_tileset_map.md`](docs/level_tileset_map.md) are older notes kept as history; where they disagree with the format pages, the format pages are right.

## Asset policy

No game files and no dumps of extracted game media are included. Short quotations of game text and short byte excerpts appear in the documentation as examples. `tools/check_all.py` includes `repo_guard.py`, which fails if a game file, converted media or a stray image is ever committed. To run the tools you need your own copy of the game.

## Sources and thanks

Formats were checked against the game files themselves and against the source code of [ScummVM](https://www.scummvm.org/)'s Kyra engine, which runs Lands of Lore; ScummVM line references point at upstream commit `3b4db303`. This is independent documentation, not a ScummVM product.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to help.
