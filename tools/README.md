# Tools

Python tools that read the data files of *Lands of Lore: The Throne of Chaos* (DOS) from your own copy of the game. Format pages: [`../docs/formats/`](../docs/formats/README.md); terms: [glossary](../docs/GLOSSARY.md).

## Setup

- Python 3.8+ and Pillow (`pip install -r requirements.txt`) for the tools that write PNG files.
- Your own copy of the game. Point the tools at its main `DATA` folder (the one holding `GENERAL.PAK` and, on the CD, `L01.PAK`) with `--data /path/to/DATA`, or once with `export LOL1_DATA=/path/to/DATA`. A language subfolder such as the CD's `DATA/ENG` is not a complete game folder.

## Rules every tool follows

- `--help` prints usage and changes nothing.
- The game folder comes from `--data` or `$LOL1_DATA`; there are no built-in paths.
- Nothing is written unless you pass `--out FILE`, `--out-dir DIR`, `--png FILE`, `--wav FILE` or `--json FILE`, and then only there. Do not point them inside this repository: `.gitignore` blocks game file types and the example output folders, and `repo_guard.py` fails if any is committed.
- `--check` reads every file of the tool's kind and prints one `CHECK` line; exit code 0 means it passed. On the CD edition, tools that rebuild a file in `data/` also compare with it.
- `lol1lib.py` is the shared library (PAK listing, Frame4, bitmap header, palettes); it has no command line.

## Examples and expected output

Run from the repository root with `LOL1_DATA` set to the CD edition's `DATA` folder. Long lines are cut with `...`.

### `check_all.py`

Run every tool's `--check` (30 checks) and print one line each, then a summary line; exit 0 when all pass. The run below shows the first three lines and the summary.

```
$ python3 tools/check_all.py | sed -n "1,3p;31p"
CHECK pak: 111 containers, 6075 members, bad=none
CHECK pak_index: 81 PAKs, 1163 members, matches data/pak_index.json: True
CHECK tlk: 30 files, 4912 members, all VOC: 4912/4912, speech-pattern names 4853, NNNNN.VOC names 59, bad=none
ALL 30 CHECKS PASSED
```

### `pak_reader.py`

List or extract the members of a PAK archive (also the CD speech files `NN.TLK`).

```
$ python3 tools/pak_reader.py list GENERAL.PAK
      1126      9176  LORESFX.ADL
     10302      2476  LOLSYSEX.C55
     12778      3924  LORESFX.C55
     16702       768  FXPAL.COL
```

### `pak_indexer.py`

Index every PAK member (rebuilds `data/pak_index.json` with `--out`). `--survey --out f.json` is a different mode: it lists every loose file under the game folder (not only PAK members), grouped by extension, with a few header bytes per type.

```
$ python3 tools/pak_indexer.py
81 PAKs, 1163 members
```

### `tlk_verify.py`

Check the CD speech archives `NN.TLK`: PAK layout, every member a VOC, names as the game builds them.

```
$ python3 tools/tlk_verify.py
00.TLK: 349 members, directory ends 4548, VOC 349, first 00000.VOC@4548, 019A0.00@48663, 019B0.00@86850, other names []
01.TLK: 506 members, directory ends 6640, VOC 506, first 00000.VOC@6640, 000_0.01@50755, 000_1.01@92650, other names []
```

### `decode_frame4.py`

An independent port of the Frame4 (LCW) decompressor; `--check` compares it with `lol1lib`; `--out-dir` writes every CPS as PNG.

```
$ python3 tools/decode_frame4.py --check
CHECK frame4: 140 files (CPS, CMZ, VCN, VMP), both decoders agree and reach the stated size: 140/140, bad=none
```

### `cps_reader.py`

CPS full-screen pictures: header, decode, PNG.

```
$ python3 tools/cps_reader.py PARCH.CPS --png parch.png
PARCH.CPS in GENERAL.PAK: {'size_field': 12665, 'comp_type': 4, 'byte3': 0, 'uncompressed_size': 64000, 'palette_size': 768}, decoded 64000 bytes
wrote parch.png
```

### `shp_renderer.py`

SHP sprites: list the shapes, write one PNG per shape (`--out-dir`), inventory (`--out`). Monster and item shapes need the scene palette of the level that loads them: `--level N`. Interface shapes take a CPS palette with `--pal-from`.

```
$ python3 tools/shp_renderer.py GUARD.SHP --level 1 --out-dir guard
  0 56x96 flags=0x0005 frame_size=2846 exact=True
  1 56x96 flags=0x0005 frame_size=2867 exact=True
  2 56x96 flags=0x0005 frame_size=2948 exact=True
```

### `wsa_extract.py`

WSA animations: header and frame table; frame 0 (or every frame with `--all`) as PNG. A WSA without its own palette needs the one it is shown over: `--pal-from` the backdrop CPS the script loads with it (for `KNOWLTK1.WSA`, `KNOWLTK.CPS`).

```
$ python3 tools/wsa_extract.py ESCAPE.WSA --out-dir escape
ESCAPE.WSA O27A.PAK {'frames': 51, 'x_add': 4, 'y_add': 0, 'width': 136, 'height': 104, 'delta_buffer': 1859, 'flags': 1, 'has_first_frame': True, ...
wrote PNGs to escape
```

### `wsa_all_frames_extract.py`

Every frame of every WSA, or of the named ones.

```
$ python3 tools/wsa_all_frames_extract.py --out-dir frames CHANDELR.WSA
wrote 3 frames of 1 WSA files to frames
```

### `fnt_reader.py`

Fonts: header and a glyph atlas PNG.

```
$ python3 tools/fnt_reader.py FONT9P.FNT --png font.png
FONT9P.FNT STARTUP.PAK {'size_field': 3881, 'signature': '0x500', 'glyphs': 226, 'height': 9, 'width': 8}
wrote font.png
```

### `cmz_analyzer.py`

Wall-type statistics of every level map (rebuilds `data/wall_type_analysis.json`).

```
$ python3 tools/cmz_analyzer.py
  Level  1: len=4 blocks=1024 wall_types=26 size=OK decomp=4102
  Level  2: len=4 blocks=1024 wall_types=24 size=OK decomp=4102
  Level  3: len=4 blocks=1024 wall_types=24 size=OK decomp=4102
  Level  4: len=4 blocks=1024 wall_types=30 size=OK decomp=4102
```

### `wll_parser.py`

Wall-type tables of every level (rebuilds `data/wll_parsed.json`).

```
$ python3 tools/wll_parser.py
  Level  1: shape_idx=0 records=52 with_vmp=47 without=5
  Level  2: shape_idx=1 records=41 with_vmp=32 without=7
```

### `vcn_vmp_reader.py`

An area's wall tiles (VCN) and tile layouts (VMP); tile atlas PNG.

```
$ python3 tools/vcn_vmp_reader.py KEEP --png keep_tiles.png
KEEP (KEEP.PAK): VCN {'tiles': 1282, 'decoded': 42820, 'expected': 42820}, shift values [0, 16, 32, 48, 64, 80, 96, 112]; VMP 2916 words = 330 floo...
wrote keep_tiles.png
```

### `tileset_mapper.py`

Which area, tile set and override palette each level uses (rebuilds `data/tileset_mapping.json`).

```
$ python3 tools/tileset_mapper.py
L01  WLL area  0 KEEP      graphics: INI:KEEP
L02  WLL area  1 FOREST1   graphics: INI:FOREST1+ALTPAL2.PAL
L03  WLL area  1 FOREST1   graphics: INI:FOREST1+ALTPAL1.PAL
```

### `level_renderer.py`

Top-down map PNG of a level, with the game's tiles or as a plain drawing (`--schematic`).

```
$ python3 tools/level_renderer.py --level 1 --out-dir maps --schematic
wrote maps/level01_schematic.png
```

### `xxx_reader.py`

Automap legend records of a level, with the legend text (`--lang ENG|FRE|GER`).

```
$ python3 tools/xxx_reader.py LEVEL1.XXX
0 symbol_x=13 symbol_y=13 symbol=0x0001 reveal_x=13 reveal_y=14 string_id=0x41d0  "FOUNTAIN"
1 symbol_x=18 symbol_y=8 symbol=0x0004 reveal_x=16 reveal_y=8 string_id=0x41d1  "THRONE ROOM"
2 symbol_x=9 symbol_y=13 symbol=0x0002 reveal_x=10 reveal_y=13 string_id=0x41d2  "GERON'S OFFICE"
```

### `dat_reader.py`

Decoration records of an area.

```
$ python3 tools/dat_reader.py KEEP.DAT --index 1
KEEP.DAT in KEEP.PAK: 26 records
1 {'shapeIndex': [65535, 17, 20, 21, 65535, 65535, 65535, 65535, 65535, 65535], 'scaleFlag': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'shapeX': [0, 99, 65, ...
```

### `level_report.py`

A sheet per level made from its files: graphics loaded, wall types used, clickable walls, every script entry with a one-line description, items and monsters placed, automap legend, text ids. `--out-dir docs/levels` writes all 29 and an index.

```
$ python3 tools/level_report.py --level 1 | grep -E "^- Area|^\| block 621 "
- Area (WLL header): 0 = KEEP (decorations `KEEP.SHP` / `.DAT`).
| block 621 (x 13, y 19) | party steps in, wall clicked | moves the party to level 2, block 106; a character speaks; shows a message; set global var; plays a sound |
```

### `tlc_reader.py`

CD transparency tables of a level.

```
$ python3 tools/tlc_reader.py LEVEL01.TLC
LEVEL01.TLC in L01.PAK: 5376 bytes; effect colours -> slot: {0: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 1...
slot 0: first 16 of row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

### `extract_dialogue.py`

Raw strings of every text file (`--out-dir` writes one JSON per file).

```
$ python3 tools/extract_dialogue.py
90 files, 6495 strings, {'ENG': 2165, 'FRE': 2165, 'GER': 2165}
```

### `decode_dialogue.py`

Readable text straight from the game files (any language file; also `TRIG.TBL`).

```
$ python3 tools/decode_dialogue.py LEVEL01.ENG --index 0
[0] Welcome to Gladstone Keep.  King Richard awaits you in the throne room.
```

### `voc_reader.py`

Sound samples: blocks and rate; WAV output.

```
$ python3 tools/voc_reader.py VOC.PAK:1BOLTC.VOC --wav bolt.wav
{'header_size': 26, 'version': '0x10a', 'check_ok': True, 'blocks': [(1, 21320)], 'rate': 11025, 'samples': 21318}
wrote bolt.wav
```

### `extract_music.py`

Music file inventory (rebuilds `data/music_inventory.json`); `--out-dir` writes the raw files.

```
$ python3 tools/extract_music.py
67 files {'C55': 17, 'ADL': 16, 'PCS': 16, 'XMI': 18}
```

### `xmi_to_midi.py`

XMIDI music (`.XMI`, and the XMIDI-container `.C55` and `.PCS` files) to standard MIDI files, one per sequence (`--out-dir`). `--check` converts every sequence of every file and re-reads each result as MIDI.

```
$ python3 tools/xmi_to_midi.py LORE01A.XMI --out-dir midi | head -3
LORE01A #00: 0 notes, 0 controller, 0 program, 4 meta, 0 sysex events; 0.0 s; end-of-track: True
LORE01A #01: 0 notes, 0 controller, 0 program, 4 meta, 0 sysex events; 0.0 s; end-of-track: True
LORE01A #02: 8 notes, 8 controller, 3 program, 7 meta, 0 sysex events; 35.7 s; end-of-track: True
```

### `adl_to_midi.py`

Project an original AdLib music track to a Standard MIDI File with notes and timing. Output carries default MIDI instrument sounds. Repeat and jump handling, corpus coverage and remaining OPL effects are described in [Q15](../docs/unknowns/15_adl_and_c55.md#midi-note-projection). Choose an output path outside the checkout and the original game folder.

```sh
python3 tools/adl_to_midi.py --data DATA LORE01B.ADL --track 2 --seconds 30 --out ../lore01b.mid
python3 tools/adl_to_midi.py --data DATA --check
```

### `parse_tim.py`

TIM cut-scene scripts: chunk structure and statistics (rebuilds `data/tim_analysis.json`).

```
$ python3 tools/parse_tim.py
Parsed 139/139 TIM files
```

### `emc2_decompile.py`

Disassemble a level or item script (EMC2) to a readable listing. Takes a loose `.INF`/`.INI` file, or a PAK with `--entry`; a bare PAK name is looked up in `--data`/`$LOL1_DATA`. The run below picks a few lines of the listing.

```
$ python3 tools/emc2_decompile.py L01.PAK --entry LEVEL1.INI | grep -E "^; L01|TEXT\[0\]|loadLevelGraphics|loadBlockProperties"
; L01.PAK/LEVEL1.INI (PAK+0xF225) | 260 DATA words | 10 TEXT strings
; TEXT[0] +0x0014 "KEEP"
  0026  sysCall          0x09 loadLevelGraphics [arg0=TEXT[0] "KEEP"]
  0033  sysCall          0x0A loadBlockProperties [arg0=TEXT[3] "LEVEL1.CMZ"]
```

### `save_reader.py`

Save files field by field: original `_SAVEnnn.DAT`, the original game's level files `_LEVELn.TMP`, and ScummVM's LoL saves. `--json out.json` writes every field. `--check` reads every such file in the game folder (and its parent) and, when you pass `--saves DIR`, in that ScummVM save folder, and checks each ends where the layout predicts; it also runs the original-save layout on blank files of the documented sizes, since no original `_SAVEnnn.DAT` has been available.

```
$ python3 tools/save_reader.py /path/to/floppy/_LEVEL1.TMP     # a file the game wrote while you played
level file; ends at 1621 as the layout predicts: True
  difficulty 1, 15 changed wall bytes, 4 monster slots in use, 0 flying objects
$ python3 tools/save_reader.py /path/to/scummvm/saves/lol-cd.NNN
ScummVM save, CD, version 21: "<save name>"; ends at <size> as the layout predicts: True
  <one line per character: name, HP, MP, skills, XP>
  level <n>, block <b> (x, y), facing <f>, money <m>, <k> game flags set, levels stored [...], <i> items in use
```

### `example_images.py`

Regenerates each image in `examples/` with the command listed in `examples/README.md` and compares pixels; part of `check_all.py`. `--out-dir` writes today's versions.

```
$ python3 tools/example_images.py --check
CHECK example_images: 3 example images equal today's tool output pixel for pixel
```

### `lol1_name_callers.py`

On the CD, re-reads the `00000.VOC` catalog row in `ENG/FINALE.EXE` and checks that the three unused palette names occur in `FILEDATA.FDT` and in no program, archive payload, or `INSTALL.EXE` beside `DATA`. On a floppy folder it reports that the CD finale is not there.

```
$ python3 tools/lol1_name_callers.py --check
CHECK name_callers: FINALE.EXE+0x1D1D0 is the 00000.VOC catalog row (44115 bytes); no other reference to the name's offset; the three palettes are catalog names only, installer included
```

### `repo_guard.py`

Asset-policy guard, run by `check_all.py`: fails if git tracks any game file type (`.PAK`, `.CPS`, `.SHP`, `.XMI`, …), converted media (`.MID`, `.WAV`, …), a PNG outside `examples/` and `docs/images/`, a file over 300 KB (except the tables it lists by name), a machine path, or a word from an optional local word list (`.git/info/private_words`, never tracked). `--release` also checks every commit's author and committer address. Needs no game data.

```
$ python3 tools/repo_guard.py --check
CHECK repo_guard: N tracked files; game files, converted media, stray PNGs, files over 300 KB, machine paths, words from the local list, or commit identities: none (0); private word list: not present, skipped
```

### `tests/test_emc2_corpus.py`

Disassembles every level and item script (60 per edition) and fails on any unknown opcode, function or branch target. `check_all.py` runs it as its 26th check.

```
$ python3 tests/test_emc2_corpus.py
/path/to/DATA: PASS 60/60 scripts, 124298 DATA words, 109845 instructions, 756 TEXT strings, 0 unknown opcodes/functions
```
