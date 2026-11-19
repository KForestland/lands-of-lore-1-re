# Tools

Python tools that read the data files of *Lands of Lore: The Throne of Chaos* (DOS) from your own copy of the game. Format pages: [`../docs/formats/`](../docs/formats/README.md); terms: [glossary](../docs/GLOSSARY.md).

## Setup

- Python 3.8+ and Pillow (`pip install -r requirements.txt`) for the tools that write PNG files; Capstone (in the same file) for `monster_reference_scan.py`.
- Your own copy of the game. Point the tools at its main `DATA` folder (the one holding `GENERAL.PAK` and, on the CD, `L01.PAK`) with `--data /path/to/DATA`, or once with `export LOL1_DATA=/path/to/DATA`. A language subfolder such as the CD's `DATA/ENG` is not a complete game folder.

## Rules every tool follows

- `--help` prints usage and changes nothing.
- The game folder comes from `--data` or `$LOL1_DATA`; there are no built-in paths. `monster_reference_scan.py` also takes the two `MAIN.EXE` files directly as `--cd FILE --floppy FILE`.
- Nothing is written unless you pass `--out FILE`, `--out-dir DIR`, `--png FILE`, `--walls-png FILE`, `--wav FILE`, `--json FILE` or `-o`/`--output FILE` (`emc2_decompile.py`), and then only there. Do not point them inside this repository: `.gitignore` blocks game file types and the example output folders, and `repo_guard.py` fails if any is committed.
- `--check` reads every file of the tool's kind and prints one `CHECK` line; exit code 0 means it passed. On the CD edition, tools that rebuild a file in `data/` also compare with it.
- `lol1lib.py` is the shared library (PAK listing, Frame4, bitmap header, palettes); it has no command line.

## Parity: every format and table, its reader and how to look at it

One row per documented format and per rules or tables page. The aim: with your own copy of the game you can look at what each page describes. Checked on 19 November 2026 against the English CD edition (every example below was run as written) and, for saves, against floppy `_LEVELn.TMP` files and ScummVM `lol-cd.NNN` saves.

Legend:

- **Check**: "yes" = the tool has `--check` and `check_all.py` runs it; "corpus test" = `check_all.py` runs `tests/test_emc2_corpus.py` instead; "not in check_all" = the tool has a check that `check_all.py` does not run.
- **Look at it**: the command that shows you the content. "picture" = it writes PNG files you can open; "text" = it prints the content; "listen" = WAV or MIDI.
- **Unit test**: a test in `tests/` (`test_readers.py`, `test_formats.py`, `test_gap_tools.py`) that needs no game files (`python3 -m unittest discover -s tests`).
- **Example**: a section below with the command and its expected output.
- **gap** = missing; **part** = only partly covered (the note says what is missing).

| Page | Reader | Check | Look at it | Unit test | Example |
|------|--------|-------|-----------|-----------|---------|
| [pak](../docs/formats/pak.md) | `pak_reader.py`, `pak_indexer.py` | yes | text: `pak_reader.py list GENERAL.PAK`; `extract … -o DIR` copies a member out | part: PAK directory parsing, but through `emc2_decompile.py`'s own reader, not `lol1lib`'s | yes |
| [tlk](../docs/formats/tlk.md) | `tlk_verify.py`, `voc_reader.py` | yes | text: `tlk_verify.py`; listen: `voc_reader.py 01.TLK:000_0.01 --wav out.wav` | gap | yes |
| [lcw](../docs/formats/lcw.md) | `lol1lib.py`, `decode_frame4.py` | yes | picture: `decode_frame4.py --out-dir DIR` (every CPS screen) | yes | yes |
| [cps](../docs/formats/cps.md) | `cps_reader.py` | yes | picture: `cps_reader.py PARCH.CPS --png parch.png`; its palette: `palette_reader.py PARCH.CPS` | yes (header and palette) | yes |
| [shp](../docs/formats/shp.md) | `shp_renderer.py` | yes | picture: one PNG per shape; monsters, items and wall decorations need `--level N`, interface shapes `--pal-from` a CPS (`GAMESHP.SHP --pal-from PLAYFLD.CPS`) | part: the `--help` example only | yes |
| [wsa](../docs/formats/wsa.md) | `wsa_extract.py`, `wsa_all_frames_extract.py` | yes (`wsa_all_frames_extract.py --check` repeats the same check, not in check_all) | picture: frame 0, or every frame with `--all` | gap | yes |
| [voc](../docs/formats/voc.md) | `voc_reader.py` | yes | listen: `--wav` | yes (header and sound block) | yes |
| [music](../docs/formats/music.md) | `extract_music.py`, `xmi_to_midi.py`, `adl_to_midi.py` | yes | listen: `xmi_to_midi.py` (XMI, C55, PCS) and `adl_to_midi.py` (ADL) write MIDI files | gap | yes |
| [text](../docs/formats/text.md) | `extract_dialogue.py`, `decode_dialogue.py` | yes | text: `decode_dialogue.py LEVEL01.ENG` | gap | yes |
| [cmz](../docs/formats/cmz.md) | `cmz_analyzer.py`, `level_renderer.py` | yes | picture: `level_renderer.py --level N` (one flat colour per wall type, taken from the wall face the game draws) or `--schematic`; text: wall-type counts | part: the map drawing (`level_renderer.draw_map`), not the CMZ reader | yes |
| [wll](../docs/formats/wll.md) | `wll_parser.py` | yes | text: counts per level; every record with its fields: `wll_parser.py --level N` | yes | yes |
| [vcn_vmp](../docs/formats/vcn_vmp.md) | `vcn_vmp_reader.py`, `tileset_mapper.py` | yes | picture: `vcn_vmp_reader.py KEEP --walls-png walls.png` (every wall page assembled from the VMP, its nine pieces as drawn on screen, and the floor/ceiling); `--png tiles.png` the 8×8 tiles in file order | yes: tile colours, mirroring, transparent words, piece offsets | yes |
| [xxx](../docs/formats/xxx.md) | `xxx_reader.py` | yes | text: every legend record with its name | yes | yes |
| [dat](../docs/formats/dat.md) | `dat_reader.py` | yes | text: one record per `--index` | gap | yes |
| [tlc](../docs/formats/tlc.md) | `tlc_reader.py` | yes | text: first 16 bytes of each used row; table1 and all 20 rows in full with `--full` | yes | yes |
| [palette](../docs/formats/palette.md) | `palette_reader.py`, `cps_reader.py --pal-from` | yes | text: `palette_reader.py ALTPAL1.PAL` (256 colours, 6-bit and 8-bit); picture: `--out-dir DIR` writes a 16 × 16 swatch; applied to a CPS: `cps_reader.py PARCH.CPS --png p.png --pal-from FXPAL.COL` | yes | yes |
| [fnt](../docs/formats/fnt.md) | `fnt_reader.py` | yes | picture: glyph atlas | yes (header and glyph tables) | yes |
| [emc2](../docs/formats/emc2.md) | `emc2_decompile.py` | corpus test (the tool has no `--check`) | text: script listing (stops quietly when the reader closes the pipe, e.g. `\| head`) | yes | yes |
| [tim](../docs/formats/tim.md) | `parse_tim.py`, `lol1_tim_words.py` | yes (also re-counts the command table of Q6) | text: `parse_tim.py --list NAME.TIM`, command by command with the command names | yes (framing, walk, listing) | yes |
| [drivers](../docs/formats/drivers.md) | `decode_dialogue.py` (`TRIG.TBL` only) | yes | text: `decode_dialogue.py TRIG.TBL`; the `.ADV`/`.DRV` drivers have no reader (they are program code) | gap | gap (no `TRIG.TBL` example) |
| [loose](../docs/formats/loose.md) | `lol1_loose.py` | yes | gap: only the one `CHECK` line, no per-file dump | gap | yes |
| [game_rules](../docs/game_rules.md) | `exe_tables.py` for the tables the rules use (experience thresholds, difficulty rows, spell costs, character modifier rows, movement step words); the formulas themselves are program code | part: the tables | part: `exe_tables.py --table difficulty` (text); the formulas have no reader | yes (tables) | yes |
| [executable_tables](../docs/executable_tables.md) | `exe_tables.py` for the tables inside `MAIN.EXE` and `MAINW.EXE` (character defaults, modifier rows, equipment layout, spell properties, experience thresholds, difficulty and price tables); item types and monster properties are script calls | yes, and the corpus test | text: `exe_tables.py` (every table, both editions); `emc2_decompile.py STARTUP.PAK --entry ONETIME.INF` lists the item-type calls, `Lnn.PAK --entry LEVELn.INI` the monster calls | yes | yes |
| [savegame_format](../docs/savegame_format.md) | `save_reader.py` | yes | text; every field with `--json` | yes (original save layout) | yes |
| [emc2_scripts](../docs/emc2_scripts.md) | `emc2_decompile.py`, `tests/test_emc2_corpus.py` | corpus test | text: script listing | yes | yes |
| [levels/](../docs/levels/README.md) | `level_report.py` | yes | text: `level_report.py --level N` (same sheet as the page) | gap | yes |
| [level_tileset_map](../docs/level_tileset_map.md) | `tileset_mapper.py` | yes | text | gap | yes |
| [Q5 TRIG.TBL](../docs/unknowns/05_adv_drv_tbl.md) | `decode_dialogue.py` | yes | text: `decode_dialogue.py TRIG.TBL` | gap | gap |
| [Q6 TIM opcodes](../docs/unknowns/06_tim_opcodes.md) | `lol1_tim_words.py`, `parse_tim.py`, `exe_tables.py` | yes (`parse_tim.py --check` re-counts the command uses) | text: `exe_tables.py --table tim_commands` and `--table tim_nested` (native command tables); `parse_tim.py --list NAME.TIM` | yes | yes |
| [Q7 native rules](../docs/unknowns/07_native_rules.md) | `exe_tables.py` for its tables (timer array, monster mode flags, spell-effect and wall-click pointers); the traced code has no reader | part: the tables | part: `exe_tables.py --table timers` (text) | yes (tables) | yes |
| [Q13 decoration positions](../docs/unknowns/13_decoration_positions.md) | none for the cell table in `MAIN.EXE`; `dat_reader.py` for the records | gap | part: DAT records only | gap | gap |
| [Q16 VCN colour banks](../docs/unknowns/16_vcn_colour_banks.md) | `vcn_vmp_reader.py` | yes | text: shift values; picture: tile atlas, assembled walls | yes: bank ORed into the colour index | yes |
| [Q17 native save fields](../docs/unknowns/17_native_save_fields.md) | `save_reader.py` | yes | text, `--json` | part | yes |
| [Q18 native records](../docs/unknowns/18_native_records.md) | `monster_reference_scan.py` (needs Capstone, in `requirements.txt`) | yes (the edition of `--data`) | text: one `CHECK` line per edition | part: folder handling and `--help`, not the census | yes |

Tools in `check_all.py` with no section below: `rating.py`. No unit test needs game data; tests cover PAK directories, Frame4, EMC2 (with the closed-pipe case), the original save layout (`tests/test_readers.py`), PAL/CPS palettes, WLL, TLC, XXX, FNT, VOC headers, TIM framing and the executable tables (`tests/test_formats.py`), and wall assembly (VCN/VMP), the level map drawing, `shp_renderer.py --help` and `monster_reference_scan.py`'s folder handling (`tests/test_gap_tools.py`).

## Examples and expected output

Run with `LOL1_DATA` set to the CD edition's `DATA` folder. If you run from another folder, use the path to the tool in place of `tools/...`. Keep generated output outside the repository and the game tree. Long lines are cut with `...`.

### `check_all.py`

Run every tool's `--check` (36 checks) and print one line each, then a summary line; exit 0 when all pass. The run below shows the first three lines and the summary.

```
$ python3 tools/check_all.py | sed -n "1,3p;37p"
CHECK pak: 111 containers, 6075 members, bad=none
CHECK pak_index: 81 PAKs, 1163 members, matches data/pak_index.json: True
CHECK tlk: 30 files, 4912 members, all VOC: 4912/4912, speech-pattern names 4853, NNNNN.VOC names 59, bad=none
ALL 36 CHECKS PASSED
```

### `doc_links.py`

Checks links and anchors only (it runs no command shown in the pages): every relative link, image link, `<a href>` and `#anchor` in `README.md`, `tools/README.md`, `CONTRIBUTING.md`, `docs/`, and `examples/` and `evidence/` when present. Anchors follow GitHub's heading ids. A link or heading inside a fenced example is skipped. Part of `check_all.py`.

```
$ python3 tools/doc_links.py --check
CHECK links: every relative link and anchor in the README files and docs resolves
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

SHP sprites: list the shapes, write one PNG per shape (`--out-dir`), inventory (`--out`). Monster, item and wall-decoration shapes (`KEEP.SHP`, `KEEPDOOR.SHP`, …) need the scene palette of a level that loads them: `--level N`. Interface shapes take a CPS palette with `--pal-from`: `GAMESHP.SHP` (buttons, arrows, spell icons) is drawn over the game screen, so `--pal-from PLAYFLD.CPS`; its shape 6, a splash, comes out magenta because `PLAYFLD.CPS` holds 63,0,63 at that index; what colour the game uses there is not checked.

```
$ python3 tools/shp_renderer.py GUARD.SHP --level 1 --out-dir guard
  0 56x96 flags=0x0005 frame_size=2846 exact=True
  1 56x96 flags=0x0005 frame_size=2867 exact=True
  2 56x96 flags=0x0005 frame_size=2948 exact=True
$ python3 tools/shp_renderer.py GAMESHP.SHP --out-dir gameshp --pal-from PLAYFLD.CPS | head -3
  0 13x19 flags=0x0001 frame_size=247 exact=True
  1 18x19 flags=0x0001 frame_size=259 exact=True
  2 12x19 flags=0x0001 frame_size=185 exact=True
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

Wall-type tables of every level (rebuilds `data/wll_parsed.json`). `--level N` prints every record of one level with the fields of the [WLL page](../docs/formats/wll.md); the high bytes the loader skips are shown raw.

```
$ python3 tools/wll_parser.py
  Level  1: shape_idx=0 records=52 with_vmp=47 without=5
  Level  2: shape_idx=1 records=41 with_vmp=32 without=7
$ python3 tools/wll_parser.py --level 1 | head -4
LEVEL1.WLL: area 0 (KEEP), 52 records of 12 bytes, (size - 2) % 12 = 0
rec  file+  wall_type  vmp  shape_map  special  flags  automap  bytes 3/7/9/11
  0  0x002          0    0          0        0  0x80   0x3F     00 00 00 00
  1  0x00E          1    1          0        0  0x07   0xFF     00 00 00 FF
```

### `vcn_vmp_reader.py`

An area's wall tiles (VCN) and tile layouts (VMP). `--png` writes the 8×8 tiles in file order; `--walls-png` assembles the blocks as they appear on screen: the first row is the 22×15-tile floor/ceiling layout, then one row per wall page with its nine pieces (side walls at three depths, the wall two squares ahead, the 128×96 wall one square ahead, the near side wall), drawn at 2× size. For KEEP the six rows after the floor are plain wall, the window wall, an open archway, the bird relief, the fountain niche and the double door.

```
$ python3 tools/vcn_vmp_reader.py KEEP --walls-png keep_walls.png
KEEP (KEEP.PAK): VCN {'tiles': 1282, 'decoded': 42820, 'expected': 42820}, shift values [0, 16, 32, 48, 64, 80, 96, 112]; VMP 2916 words = 330 floor/ceiling + 6 wall pages of 431
wrote keep_walls.png
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

Top-down map PNG of a level (10 px per square). Without `--schematic`, solid rock is the colour of the level's main wall face and floor the colour of its floor, both averaged from the game's own tiles and palette (only the brightness is adjusted, so walls stand out); doors, switches and wall faces of other types are strips on their side of the square. `--schematic` draws from the CMZ and WLL only, without game pixels. For level 1 the keep's corridors show dark blue-grey inside sand-coloured stone, with door strips across them.

```
$ python3 tools/level_renderer.py --level 1 --out-dir maps
wrote maps/level01_keep.png
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
| block 621 (x 13, y 19) | `0x12D2` | party steps in, wall clicked | moves the party to level 2, block 106, facing 2; ...
```

### `tlc_reader.py`

CD transparency tables of a level. `--full` prints table1 and all 20 rows of table2, 16 hex values per line.

```
$ python3 tools/tlc_reader.py LEVEL01.TLC
LEVEL01.TLC in L01.PAK: 5376 bytes; effect colours -> slot: {0: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 1...
slot 0: first 16 of row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
$ python3 tools/tlc_reader.py LEVEL01.TLC --full | sed -n 2,3p
table1 (colour -> slot, ff = opaque)
    0: 00 ff 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e
```

### `palette_reader.py`

A palette's colours: a `.PAL` or `.COL` file, or the palette inside a CPS. One row per colour with the 6-bit VGA values and the 8-bit RGB; `--out-dir DIR` also writes `DIR/NAME_EXT_swatch.png`, 16 × 16 squares with colour 0 top left. A file longer than 768 bytes (floppy `MONSTERS.PAL`) shows its first 256 colours unless you pass `--all`.

```
$ python3 tools/palette_reader.py ALTPAL1.PAL | head -6
ALTPAL1.PAL in FOREST1.PAK: 768 palette bytes = 256 colours
index  6-bit r  g  b   8-bit   r   g   b  hex
    0         0  0  0           0   0   0  #000000
    1         0  0  0           0   0   0  #000000
    2        63 51 52         255 206 210  #ffced2
    3        63 36 37         255 145 149  #ff9195
$ python3 tools/palette_reader.py --check
CHECK palette: 6 PAL, 5 COL, other than 768 bytes: none; 85 of 85 CPS carry a 768-byte palette; every value 0-63 and sizes a multiple of 3, bad=none
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

```
$ python3 tools/adl_to_midi.py LORE01B.ADL --track 2 --seconds 30 --out ../lore01b.mid
LORE01B.ADL slot 2: 279 notes, 2160 callbacks (time cutoff); unmapped controls: 90, 9E, AB, AE, AF, B9; stops: {}
$ python3 tools/adl_to_midi.py --check
CHECK ADL: 16 assets, 2207 entry projections (2158 with notes), 9 unavailable entry IDs, 0 documented out-of-range repeats, unexpected issues: none
```

### `parse_tim.py`

TIM cut-scene scripts: chunk structure and statistics (rebuilds `data/tim_analysis.json`). `--list NAME.TIM` prints one file command by command: word index, function, length, delay, opcode word, the command name from [Q6](../docs/unknowns/06_tim_opcodes.md), and the parameters (named where the page names them; the TEXT string of an animation or sound name; the nested function of command 0x19). `--check` also walks every file and re-counts the uses and files of each command against Q6 (CD), and the floppy intro and outro counts.

```
$ python3 tools/parse_tim.py
Parsed 139/139 TIM files
$ python3 tools/parse_tim.py --list AUTOMAP.TIM | head -6
AUTOMAP.TIM in O00A.PAK
AUTOMAP.TIM: AVTL 143 words, 1 function(s) at word(s) [1], TEXT 7 bytes, in-game table
word  fn len delay opcode command parameters
   1   0   3     0 0x0118 cmd_return(1)
   4   0   9     0 0x0102 cmd_initWSA index=0 string_id=0 "BOOK" x=288 y=32 offscreen=0 flags=40
  13   0   3     0 0x0117 cmd_resetAllRuntimes
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

### `monster_reference_scan.py`

The [Q18](../docs/unknowns/18_native_records.md) census of the code in `MAIN.EXE` that reads or writes monster definition fields. Needs Capstone. With `--data` it checks the edition of that folder (CD: `HARDRIVE/MAIN.EXE`); `--cd FILE --floppy FILE` checks both.

```
$ python3 tools/monster_reference_scan.py --check
CHECK CD monster references: 57 instance and 7 stat load candidates, 1 critical read, 2 speed controls, 5 definition stores; 13 near and 7 far mode setter encodings
```

### `save_reader.py`

Reads native `_SAVEnnn.DAT` slots, native `_LEVELn.TMP` files and ScummVM LoL saves field by field. `--json out.json` writes every field. `--check` checks the end boundary of each save in the game folder or its parent, and in a ScummVM save folder supplied with `--saves DIR`. It also checks the native layout on synthetic CD and floppy saves.

```
$ python3 tools/save_reader.py /path/to/cd/_LEVEL1.TMP
level file; ends at 1529 as the layout predicts: True
  difficulty 1, 0 changed wall bytes, 4 monster slots in use, 0 flying objects
$ python3 tools/save_reader.py /path/to/scummvm/saves/lol-cd.NNN
ScummVM save, CD, version 21: "<save name>"; ends at <size> as the layout predicts: True
  <one line per character: name, HP, MP, skills, XP>
  level <n>, block <b> (x, y), facing <f>, money <m>, <k> game flags set, levels stored [...], <i> items in use
```

The counts and end offset depend on the save you pass.

### `example_images.py`

Regenerates each image in `examples/` and the two level schematics in `docs/images/` with its listed command and compares pixels; part of `check_all.py`. `--out-dir` writes today's versions.

```
$ python3 tools/example_images.py --check
CHECK example_images: 5 shown images (examples/ and docs/images/) equal today's tool output pixel for pixel
```

### `lol1_tim_words.py`

Re-reads the extra TIM argument words. On the CD, nested 0x07 and 0x0D push the operand pointer and a start index, the formatter reads `operand[index]` per `%n`, `%s`, `%d`, `%u`, `%x` or `%X` (`%a` reads none), and the 14 extra words are 0. On a floppy folder with `MAIN.EXE`, the same pushes are checked and the four nonzero words are 20, 10, 10 and 100.

```
$ python3 tools/lol1_tim_words.py --check
CHECK tim_words: 14 CD extra words are 0; 0x07 and 0x0D pass the operand pointer and a start index; 6 level strings have one %n and 6 have none; giveItem pushes three words
```

### `lol1_name_callers.py`

On the CD, re-reads the `00000.VOC` catalog row in `ENG/FINALE.EXE` and checks that the three unused palette names occur in `FILEDATA.FDT` and in no program, archive payload, or `INSTALL.EXE` beside `DATA`. On a floppy folder it reports that the CD finale is not there.

```
$ python3 tools/lol1_name_callers.py --check
CHECK name_callers: FINALE.EXE+0x1D1D0 is the 00000.VOC catalog row (44115 bytes); no other reference to the name's offset; the three palettes are catalog names only, installer included
```

### `lol1_loose.py`

Walks the loose CD `DATA` files. Thirty-one reach their last byte, including fonts, string tables, executable images and symbol tables. The check reproduces bytes 0–65531 of both distinct finale blend tables and pins the four-byte trailer. See the loose-file page for the palette pairings and the remaining open bytes. [Loose-file formats](../docs/formats/loose.md)

```
$ python3 tools/lol1_loose.py --check
CHECK loose: 31 files reach the last byte (3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 5 mz, 2 le, 2 overlay, 1 text, 1 com, 3 symbol, 3 mz plus symbol tail); 6 open (6 blend tables; palette self-blend 22/42 matches BLEND.TAB 65532 of 65536 from RETURN.CPS, BLEND2.TAB 65532 of 65536 from FACE.CPS, last four bytes E4 D5 02 00 open)
```

### `exe_tables.py`

The static tables inside the game program, at the offsets of [executable tables](../docs/executable_tables.md), [game rules](../docs/game_rules.md), [Q6](../docs/unknowns/06_tim_opcodes.md) and [Q7](../docs/unknowns/07_native_rules.md): character defaults, character modifier rows, equipment display layout, spell properties, experience thresholds, monster difficulty rows, item price thresholds (CD), timer array, monster mode flags, movement step words (CD), and the spell-effect, wall-click and TIM command pointer tables. It finds CD `HARDRIVE/MAIN.EXE` and `MAINW.EXE` and floppy `MAIN.EXE` by size. `--list` names the tables, `--table NAME` and `--image cd|cdw|floppy` pick one. Words the pages mark UNCONFIRMED are printed raw with their record offset. `--check` re-reads the values and counts the pages give (character modifier rows 0,0,0,1,0,0,1,2,4, spell rows, thresholds, difficulty rows, the CD-only tables absent on floppy, timer periods and callbacks, the TIM routines).

```
$ python3 tools/exe_tables.py --table difficulty --image cd
# CD MAIN.EXE (356928 bytes, MZ header 0x3800)
## Monster difficulty modifiers 1-3, easy/normal/hard, 256 = 1.0 (executable_tables.md): +0x2B85C
row 1 (+0x2B85C): easy/normal/hard = [102, 256, 384]
row 2 (+0x2B862): easy/normal/hard = [256, 256, 192]
row 3 (+0x2B868): easy/normal/hard = [320, 256, 128]
$ python3 tools/exe_tables.py --check
CHECK exe_tables: CD MAIN.EXE, CD MAINW.EXE: character rows 0,0,0,1,0,0,1,2,4, spells, experience, difficulty rows, prices, timers, mode flags, spell/wall/TIM pointers as the pages give, bad=none
```

### `repo_guard.py`

Asset-policy guard, run by `check_all.py`: fails if git tracks any game file type (`.PAK`, `.CPS`, `.SHP`, `.XMI`, …), converted media (`.MID`, `.WAV`, …), a PNG outside `examples/` and `docs/images/`, a file over 300 KB (except the tables it lists by name), a machine path, or a word from an optional local word list (`.git/info/private_words`, never tracked). `--release` also checks every commit's author and committer address. Needs no game data. `N` is the number of tracked files; with a local word list the line ends `private word list: K words` instead.

```
$ python3 tools/repo_guard.py --check
CHECK repo_guard: N tracked files; game files, converted media, stray PNGs, files over 300 KB, machine paths, words from the local list, or commit identities: none (0); private word list: not present, skipped
```

### `tests/test_emc2_corpus.py`

Disassembles every level and item script (60 per edition) and fails on any unknown opcode, function or branch target. `check_all.py` runs it as its last (36th) check.

```
$ python3 tests/test_emc2_corpus.py
/path/to/DATA: PASS 60/60 scripts, 124298 DATA words, 109845 instructions, 756 TEXT strings, 0 unknown opcodes/functions
```
