# Tools

To write the inventory, level sheets and text counts together, use `full_report.py`. [Cookbook](../docs/COOKBOOK.md#write-a-full-report)

Python tools that read the data files of *Lands of Lore: The Throne of Chaos* (DOS) from your own copy of the game. Format pages: [`../docs/formats/`](../docs/formats/README.md); terms: [glossary](../docs/GLOSSARY.md).

The numeric tables can be regenerated with `python3 tools/lol1_numbers.py`. On the CD edition, `--check` prints `CHECK numbers: CD tables match docs/NUMBERS.md`. [Numbers at a glance](../docs/NUMBERS.md)

[Translation guide](../docs/TRANSLATION.md) covers `translate.py` , the FNT reader `translate_fonts.py`, and its game-specific `translate_data.py`.

The `lol.py` job menu opens with `python tools/lol.py`. Add `JOB --help`
to see the job's options. `level_viewer.py` writes an offline HTML plan with clickable details using `level_html.py`.
Use `level_viewer.py --check` to write and read back one plan in a temporary folder. [Level editor](../docs/LEVEL_EDITOR.md) documents `level_edit.py` and its patch and undo output.

[First ten minutes](../docs/FIRST_TEN_MINUTES.md) ·
[Interactive plans](../docs/COOKBOOK.md#open-an-interactive-level-plan)

`edition.py` reads names, file sizes and SHA-256 to identify a measured game copy. `--check` verifies the full fingerprint in `check_all.py`. [Edition fingerprints](../docs/EDITIONS.md)

## Setup

- Python 3.10 or later and Pillow (`pip install -r requirements.txt`) for the tools that write PNG files; Capstone (in the same file) for `monster_reference_scan.py`.
- Your own copy of the game. Point the tools at its main `DATA` folder (the one holding `GENERAL.PAK` and, on the CD, `L01.PAK`) with `--data /path/to/DATA`, or once with `export LOL1_DATA=/path/to/DATA`. A language subfolder such as the CD's `DATA/ENG` is not a complete game folder.

## Rules every tool follows

- `--help` prints usage and changes nothing.
- The game folder comes from `--data` or `$LOL1_DATA`; there are no built-in paths. `monster_reference_scan.py` also takes the two `MAIN.EXE` files directly as `--cd FILE --floppy FILE`.
- Write output by giving `--out` and a path outside the repository. The tools reference below notes the few secondary outputs.
- `--check` reads every file of the tool's kind and prints one `CHECK` line; exit code 0 means it passed. On the CD edition, tools that rebuild a file in `data/` also compare with it.
- `lol1lib.py` is the shared library (PAK listing, Frame4, bitmap header, palettes); it has no command line.

## Parity: every format and table, its reader and how to look at it

One row per documented format and per rules or tables page. The aim: with your own copy of the game you can look at what each page describes. Every example below was run as written against the English CD edition; saves were also checked against floppy `_LEVELn.TMP` files and ScummVM `lol-cd.NNN` saves.

Legend:

- **Check**: "yes" = the tool has `--check` and `check_all.py` runs it; "corpus test" = `check_all.py` runs `tests/test_emc2_corpus.py` instead; "not in check_all" = the tool has a check that `check_all.py` does not run.
- **Look at it**: the command that shows you the content. "picture" = it writes PNG files you can open; "text" = it prints the content; "listen" = WAV or MIDI.
- **Unit test**: a test in `tests/` (`test_readers.py`, `test_formats.py`, `test_gap_tools.py`, `test_round_trip.py`) that needs no game files (`python3 -m unittest discover -s tests`).
- **Example**: a section below with the command and its expected output.
- **gap** = missing; **part** = only partly covered (the note says what is missing).

| Page | Reader | Check | Look at it | Unit test | Example |
|------|--------|-------|-----------|-----------|---------|
| [pak](../docs/formats/pak.md) | `pak_reader.py`, `pak_indexer.py`, `lol1_pak_writer.py` | yes | text: `pak_reader.py list GENERAL.PAK`; `extract … -o DIR` copies a member out | yes: `tests/test_round_trip.py` writes synthetic PAKs and reads them back with `lol1lib` | yes |
| [tlk](../docs/formats/tlk.md) | `tlk_verify.py`, `voc_reader.py` | yes | text: `tlk_verify.py`; listen: `voc_reader.py 01.TLK:000_0.01 --out out.wav` | gap | yes |
| [lcw](../docs/formats/lcw.md) | `lol1lib.py`, `decode_frame4.py`, `lol1_compression_writer.py` | yes | picture: `decode_frame4.py --out DIR` (every CPS screen) | yes | yes |
| [cps](../docs/formats/cps.md) | `cps_reader.py` | yes | picture: `cps_reader.py PARCH.CPS --out parch.png`; its palette: `palette_reader.py PARCH.CPS` | yes (header and palette) | yes |
| [shp](../docs/formats/shp.md) | `shp_renderer.py` | yes | picture: one PNG per shape; monsters, items and wall decorations need `--level N`, interface shapes `--pal-from` a CPS (`GAMESHP.SHP --pal-from PLAYFLD.CPS`) | part: the `--help` example only | yes |
| [wsa](../docs/formats/wsa.md) | `wsa_extract.py`, `wsa_all_frames_extract.py` | yes (`wsa_all_frames_extract.py --check` repeats the same check, not in check_all) | picture: frame 0, or every frame with `--all` | gap | yes |
| [voc](../docs/formats/voc.md) | `voc_reader.py` | yes | listen: `--out` | yes (header and sound block) | yes |
| [music](../docs/formats/music.md) | `extract_music.py`, `xmi_to_midi.py`, `adl_to_midi.py` | yes | listen: `xmi_to_midi.py` (XMI, C55, PCS) and `adl_to_midi.py` (ADL) write MIDI files | gap | yes |
| [text](../docs/formats/text.md) | `extract_dialogue.py`, `decode_dialogue.py` | yes | text: `decode_dialogue.py LEVEL01.ENG` | gap | yes |
| [cmz](../docs/formats/cmz.md) | `cmz_analyzer.py`, `level_renderer.py` | yes | picture: `level_renderer.py --level N` (one flat colour per wall type, taken from the wall face the game draws) or `--schematic`; text: wall-type counts | part: the map drawing (`level_renderer.draw_map`), not the CMZ reader | yes |
| [wll](../docs/formats/wll.md) | `wll_parser.py` | yes | text: counts per level; every record with its fields: `wll_parser.py --level N` | yes | yes |
| [vcn_vmp](../docs/formats/vcn_vmp.md) | `vcn_vmp_reader.py`, `tileset_mapper.py` | yes | picture: `vcn_vmp_reader.py KEEP --walls-png walls.png` (every wall page assembled from the VMP, its nine pieces as drawn on screen, and the floor/ceiling); `--out tiles.png` the 8×8 tiles in file order | yes: tile colours, mirroring, transparent words, piece offsets | yes |
| [xxx](../docs/formats/xxx.md) | `xxx_reader.py` | yes | text: every legend record with its name | yes | yes |
| [dat](../docs/formats/dat.md) | `dat_reader.py` | yes | text: one record per `--index` | gap | yes |
| [tlc](../docs/formats/tlc.md) | `tlc_reader.py` | yes | text: first 16 bytes of each used row; table1 and all 20 rows in full with `--full` | yes | yes |
| [palette](../docs/formats/palette.md) | `palette_reader.py`, `cps_reader.py --pal-from` | yes | text: `palette_reader.py ALTPAL1.PAL` (256 colours, 6-bit and 8-bit); picture: `--out DIR` writes a 16 × 16 swatch; applied to a CPS: `cps_reader.py PARCH.CPS --out p.png --pal-from FXPAL.COL` | yes | yes |
| [fnt](../docs/formats/fnt.md) | `fnt_reader.py` | yes | picture: glyph atlas | yes (header and glyph tables) | yes |
| [emc2](../docs/formats/emc2.md) | `emc2_decompile.py` | corpus test (the tool has no `--check`) | text: script listing (stops quietly when the reader closes the pipe, e.g. `\| head`) | yes | yes |
| [tim](../docs/formats/tim.md) | `parse_tim.py`, `lol1_tim_words.py` | yes (also re-counts the command table of Q6) | text: `parse_tim.py --list NAME.TIM`, command by command with the command names | yes (framing, walk, listing) | yes |
| [drivers](../docs/formats/drivers.md) | `decode_dialogue.py` (`TRIG.TBL`), `lol1_driver_tables.py` (driver entry tables) | yes | text: `decode_dialogue.py TRIG.TBL`; `lol1_driver_tables.py` lists each `.ADV` entry ID and the `ALFX.DRV` selectors; the routine bodies have no reader (they are program code) | part: `tests/test_gap_tools.py` (synthetic driver tables; none for `TRIG.TBL`) | part (driver tables only; no `TRIG.TBL` example) |
| [loose](../docs/formats/loose.md) | `lol1_loose.py` | yes | gap: only the one `CHECK` line, no per-file dump | gap | yes |
| [game_rules](../docs/game_rules.md) | `exe_tables.py` for the tables the rules use (experience thresholds, difficulty rows, spell costs, character modifier rows, movement step words); `lol1_attack_types.py` for the ten attack arms and six defense arms | part: the tables and the type arms | part: `exe_tables.py --table difficulty` (text); `lol1_attack_types.py --check` | yes (tables) | yes |
| [executable_tables](../docs/executable_tables.md) | `exe_tables.py` for the tables inside `MAIN.EXE` and `MAINW.EXE` (character defaults, modifier rows, equipment layout, spell properties, experience thresholds, difficulty and price tables); item types and monster properties are script calls | yes, and the corpus test | text: `exe_tables.py` (every table, both editions); `emc2_decompile.py STARTUP.PAK --entry ONETIME.INF` lists the item-type calls, `Lnn.PAK --entry LEVELn.INI` the monster calls | yes | yes |
| [savegame_format](../docs/savegame_format.md) | `save_reader.py` | yes | text; every field with `--json` | yes (original save layout) | yes |
| [emc2_scripts](../docs/emc2_scripts.md) | `emc2_decompile.py`, `tests/test_emc2_corpus.py`, `exe_tables.py --table emc2` | corpus and executable table checks | text: script listing or original entry and body offsets | yes | yes |
| [levels/](../docs/levels/README.md) | `level_report.py` | yes | text: `level_report.py --level N` (same sheet as the page) | gap | yes |
| [level_tileset_map](../docs/level_tileset_map.md) | `tileset_mapper.py` | yes | text | gap | yes |
| [Q5 TRIG.TBL](../docs/unknowns/05_adv_drv_tbl.md) | `decode_dialogue.py` | yes | text: `decode_dialogue.py TRIG.TBL` | gap | gap |
| [Q6 TIM opcodes](../docs/unknowns/06_tim_opcodes.md) | `lol1_tim_words.py`, `parse_tim.py`, `exe_tables.py` | yes (`parse_tim.py --check` re-counts the command uses) | text: `exe_tables.py --table tim_commands` and `--table tim_nested` (native command tables); `parse_tim.py --list NAME.TIM` | yes | yes |
| [Q7 native rules](../docs/unknowns/07_native_rules.md) | `exe_tables.py` for its tables (timer array, monster mode flags, spell-effect and wall-click pointers); `lol1_mode_paths.py` for the direct instance mode stores, the finale catalog index sites and the three palette row numbers | yes | text: one `CHECK` line per edition; `exe_tables.py --table timers` for the timer array | part: the tables, not the mode stores | yes |
| [Q13 decoration positions](../docs/unknowns/13_decoration_positions.md) | none for the cell table in `MAIN.EXE`; `dat_reader.py` for the records | gap | part: DAT records only | gap | gap |
| [Q16 VCN colour banks](../docs/unknowns/16_vcn_colour_banks.md) | `vcn_vmp_reader.py` | yes | text: shift values; picture: tile atlas, assembled walls | yes: bank ORed into the colour index | yes |
| [Q17 native save fields](../docs/unknowns/17_native_save_fields.md) | `save_reader.py` | yes | text, `--json` | part | yes |
| [Q18 native records](../docs/unknowns/18_native_records.md) | `monster_reference_scan.py` (needs Capstone, in `requirements.txt`) | yes (the edition of `--data`) | text: one `CHECK` line per edition | part: folder handling and `--help`, not the census | yes |

Tools in `check_all.py` with no section below: `rating.py`. No unit test needs game data; tests cover PAK directories, Frame4, EMC2 (with the closed-pipe case), the original save layout (`tests/test_readers.py`), PAL/CPS palettes, WLL, TLC, XXX, FNT, VOC headers, TIM framing and the executable tables (`tests/test_formats.py`), and wall assembly (VCN/VMP), the level map drawing, `shp_renderer.py --help` and `monster_reference_scan.py`'s folder handling (`tests/test_gap_tools.py`), and the PAK writer: order, duplicate names, the end-offset and five zero bytes, and refused inputs (`tests/test_round_trip.py`), and the mod kit on synthetic PAK files: text compression, edit, byte-identical rebuild, refused folders and one-line errors (`tests/test_modkit.py`), the patch tool: make, apply, undo, file names from the DATA folder or the folder above, program patches and size limits (`tests/test_patch.py`), and the save editor on synthetic slots (`tests/test_save_edit.py`).

## Examples and expected output

Run with `LOL1_DATA` set to the CD edition's `DATA` folder. If you run from another folder, use the path to the tool in place of `tools/...`. Keep generated output outside the repository and the game tree. Long lines are cut with `...`.

### `check_all.py`

Run every tool's `--check` (53 checks) and print one line each, then the total time and a result line. The exit code is 0 when all attempted checks pass. The run below shows the first three lines and the summary.

```
$ python3 tools/check_all.py | sed -n '1,3p;$p'
CHECK pak: 111 containers, 6075 members, bad=none
CHECK pak write: 132 PAK and 30 PAK-layout TLK files, 7209 ordered members; byte-identical
CHECK pak_index: 81 PAKs, 1163 members, matches data/pak_index.json: True
ALL 53 CHECKS PASSED
```

### `modkit.py`

The mod kit changes game text and numbers in copies; your game folder is only read. Run it from any folder and put quotes around paths with spaces:

```bash
python3 tools/modkit.py unpack "/path/to/LoL1/DATA" "my mod work"
# change the files in "my mod work/edits", then:
python3 tools/modkit.py build "/path/to/LoL1/DATA" "my mod work" "my mod output"
python3 tools/modkit.py verify "/path/to/LoL1/DATA" "my mod work" "my mod output"
```

- `modkit.py` names the LoL1 tables; `modkit_core.py`, the same file in the three repositories, does the unpack, build, verify and folder checks.
- The game folder is the CD `DATA` folder or the floppy game folder (the one holding `GENERAL.PAK`). Language subfolders such as the CD's `DATA/ENG` are not read; give one as the game folder to edit its scripts.
- `unpack` creates the work folder with `manifest.json`, a `README.txt` and one JSON file per table in `edits/`: every `.ENG`, `.FRE` and `.GER` text table as plain text (the game's bigram compression is undone; accented letters use code page 437, as the game's font does) and every EMC2 (`.INF`, `.INI`) and AVFS (`.TIM`) script as an editable listing, in which the item and monster definition calls name their fields (`definition_field`). Change only `"value"`; keep the number of rows, the field names and codes such as `\r` or `\u0002`.
- `build` creates the output folder and writes every unpacked file into it, changed or not (about 8 MB on the CD), and names the changed files. `verify` reads the output back with the archive and table readers and checks it against the work folder. Copy the changed files over a backup copy of your game to try them.
- Refused, with one line saying why: a work or output folder that already exists, lies inside the game folder, inside a folder holding PAK or TLK, or inside this repository, and an output inside the work folder.
- An unchanged work folder rebuilds byte for byte: CD: 62 PAK files from 289 entries; floppy: 11 PAK files from 237 entries. `--check` does unpack, build and verify in a temporary folder (`--data` or `$LOL1_DATA`) and is part of `check_all.py`:

```
$ python3 tools/modkit.py --check
CHECK modkit: 62 archives or loose tables rebuilt byte-identically from 289 unpacked entries; outputs in the game, work, archive and repository folders refused
```

### `patch.py`

Makes, applies and undoes small patches for your own copy of the game ([format, rules and limits](../docs/formats/patch.md)). `patch.py` is the same file in the three repositories. Your game folder is only read. Run it from any folder and put quotes around paths with spaces:

```bash
python3 tools/patch.py make --data "/path/to/LoL1/DATA" "my mod output" --title "Stronger item" --out "stronger item.json"
python3 tools/patch.py apply --data "/path/to/LoL1 test copy/DATA" "stronger item.json" --out "patched files"
python3 tools/patch.py apply --data "/path/to/LoL1 test copy/DATA" "patched files/undo.json" --out "restored files"
```

- `--data` is the folder holding the PAK archives (the CD `DATA` folder or the floppy game folder); given the folder above `DATA`, the tool reads `DATA` (default: `$LOL1_DATA`). It may also be given as the first path, as `modkit.py` takes it.
- `make` writes a new patch file from the differences between the game folder and a folder of changed files, such as the output of `modkit.py build`. `--title` is required; `--description` is optional; `--kind data` or `--kind program` is found from the changed files when left out.
- `apply` checks each replaced span's SHA-256, the program's whole-file SHA-256 for a program patch and the undo before it writes anything, then writes the patched files and `undo.json` into the new `--out` folder. Copy the files except `undo.json`, with their folders, into a copy of the game. Applying `undo.json` to that copy gives the original bytes back. Keep the undo file private because it holds those bytes.
- Refused, with one sentence saying why: a missing or unchanged changed folder, a patch for another game, edition or version, a patch already applied, a patch over the size limits (data: 256 bytes per change and 4,096 per patch; program: 16 and 256), an output that already exists, whose folder does not exist, or that lies inside the game folder, a folder holding game archives or this repository.
- Tests on synthetic files: `tests/test_patch.py` (the same file in the three repositories).

```
$ python3 tools/patch.py make --data "/path/to/LoL1/DATA" "my mod output" --title "Stronger item" --out "stronger item.json"
make: data patch with 1 change in 1 file (STARTUP.PAK) written to /path/to/stronger item.json
Data patches are for the original program under DOSBox; ScummVM also reads the changed data when it still recognizes the release.
```

### `save_edit.py`

`save_page.py` renders the offline page produced by `lol.py save page`. See [the save guide](../docs/EDITED_SAVES.md#see-the-fields-in-an-offline-page).

Writes a copy of an original save with one field changed; the save itself is only read. Each run prints the old and the new value and one line saying whether the game has been shown to load such an edit (CONFIRMED) or not yet (UNCONFIRMED). Fields and their status: [cookbook](../docs/COOKBOOK.md#change-a-saved-game-a-copy).

```
$ python3 tools/save_edit.py set "/path/to/your/_SAVE001.DAT" money 5000 --out "my edited save.DAT"
set: money OLD -> 5000; copy written to /path/to/my edited save.DAT; the original save was only read
UNCONFIRMED: no edited copy of this field has been loaded by the game yet; keep a backup of your saves
```

- Fields: `name` (the slot description), `block` (0–1023), `facing` (0–3), `money` (0–65535, the field `save_reader.py` prints as money) and `lamp-oil` (0–100), for CD 1.02 slots and floppy `.13` slots. Numbers can be decimal or start with `0x`.
- Refused, with one sentence saying why: a missing or damaged save, a value out of range, a name that is not plain ASCII, a donor save from another level or version, and an output that already exists, lies in the save's own folder, in the game folder or in this repository. Tests on synthetic slots: `tests/test_save_edit.py`.

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

### `lol1_pak_writer.py`

Rebuild every PAK and PAK-layout TLK under the data folder (subfolders included) from its parsed members, in memory, and compare every byte with the original. It writes no file; `--check` is its only mode. The library function `write_pak(members)` builds an archive from ordered `(name, bytes)` pairs.

```
$ python3 tools/lol1_pak_writer.py --check
CHECK pak write: 132 PAK and 30 PAK-layout TLK files, 7209 ordered members; byte-identical
```

The floppy edition gives `15 PAK and 0 PAK-layout TLK files, 1213 ordered members`.

### `lol1_compression_writer.py`

Re-encode every CPS, CMZ, VCN, VMP, WSA and SHP file under the data folder (loose files and PAK members), in memory, and read each rebuilt file back through the existing readers (`lol1lib.load_bitmap` and `decode_frame4`, `decode_frame4.py`, `wsa_extract.py`, `shp_renderer.py`); the decoded pixels must equal the original's. It writes no file; `--check` is its only mode. The encoders are new and simple (Frame4 literals and fills, back-references only when a 16-bit size field needs them; WSA XOR deltas with skips and literals; SHP scanlines with zero runs). They are not the original encoder: no rebuilt file matches its original byte for byte, and on the CD the rebuilt files are larger (WSA 1.5 times, CPS 1.8 times, SHP 1.4 times, VCN 1.2 times, VMP 1.1 times, CMZ 5.8 times the original bytes). The check proves that every original picture survives encoding and reading back, not that the original compressed bytes can be recreated.

```
$ python3 tools/lol1_compression_writer.py --check
CHECK compression write: 1085 files (29 .cmz, 265 .cps, 236 .shp, 13 .vcn, 13 .vmp, 529 .wsa); 20354 source Frame4 streams, 12785 WSA deltas and 7299 SHP shapes read back identically; 0 files byte-identical
```

The floppy edition gives `516 files (29 .cmz, 112 .cps, 95 .shp, 13 .vcn, 13 .vmp, 254 .wsa); 9075 source Frame4 streams, 5420 WSA deltas and 3601 SHP shapes`. The CD check takes about a minute, the floppy about 15 seconds.

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

An independent port of the Frame4 (LCW) decompressor; `--check` compares it with `lol1lib`; `--out` writes every CPS as PNG.

```
$ python3 tools/decode_frame4.py --check
CHECK frame4: 140 files (CPS, CMZ, VCN, VMP), both decoders agree and reach the stated size: 140/140, bad=none
```

### `cps_reader.py`

CPS full-screen pictures: header, decode, PNG.

```
$ python3 tools/cps_reader.py PARCH.CPS --out parch.png
PARCH.CPS in GENERAL.PAK: {'size_field': 12665, 'comp_type': 4, 'byte3': 0, 'uncompressed_size': 64000, 'palette_size': 768}, decoded 64000 bytes
wrote parch.png
```

### `shp_renderer.py`

SHP sprites: give a member and `--out DIR` for individual PNGs, or omit the member and use `--out FILE` for the inventory. Monster, item and wall-decoration shapes (`KEEP.SHP`, `KEEPDOOR.SHP`, …) need the scene palette of a level that loads them: `--level N`. Interface shapes take a CPS palette with `--pal-from`: `GAMESHP.SHP` (buttons, arrows, spell icons) is drawn over the game screen, so `--pal-from PLAYFLD.CPS`; its shape 6, a splash, comes out magenta because `PLAYFLD.CPS` holds 63,0,63 at that index; what colour the game uses there is not checked.

```
$ python3 tools/shp_renderer.py GUARD.SHP --level 1 --out guard
  0 56x96 flags=0x0005 frame_size=2846 exact=True
  1 56x96 flags=0x0005 frame_size=2867 exact=True
  2 56x96 flags=0x0005 frame_size=2948 exact=True
$ python3 tools/shp_renderer.py GAMESHP.SHP --out gameshp --pal-from PLAYFLD.CPS | head -3
  0 13x19 flags=0x0001 frame_size=247 exact=True
  1 18x19 flags=0x0001 frame_size=259 exact=True
  2 12x19 flags=0x0001 frame_size=185 exact=True
```

### `wsa_extract.py`

WSA animations: header and frame table; frame 0 (or every frame with `--all`) as PNG. A WSA without its own palette needs the one it is shown over: `--pal-from` the backdrop CPS the script loads with it (for `KNOWLTK1.WSA`, `KNOWLTK.CPS`).

```
$ python3 tools/wsa_extract.py ESCAPE.WSA --out escape
ESCAPE.WSA O27A.PAK {'frames': 51, 'x_add': 4, 'y_add': 0, 'width': 136, 'height': 104, 'delta_buffer': 1859, 'flags': 1, 'has_first_frame': True, ...
wrote PNGs to escape
```

### `wsa_all_frames_extract.py`

Every frame of every WSA, or of the named ones.

```
$ python3 tools/wsa_all_frames_extract.py --out frames CHANDELR.WSA
wrote 3 frames of 1 WSA files to frames
```

### `fnt_reader.py`

Fonts: header and a glyph atlas PNG.

```
$ python3 tools/fnt_reader.py FONT9P.FNT --out font.png
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

An area's wall tiles (VCN) and tile layouts (VMP). `--out` writes the 8×8 tiles in file order; `--walls-png` assembles the blocks as they appear on screen: the first row is the 22×15-tile floor/ceiling layout, then one row per wall page with its nine pieces (side walls at three depths, the wall two squares ahead, the 128×96 wall one square ahead, the near side wall), drawn at 2× size. For KEEP the six rows after the floor are plain wall, the window wall, an open archway, the bird relief, the fountain niche and the double door.

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
$ python3 tools/level_renderer.py --level 1 --out maps
Wrote map for level01 to maps/level01_keep.png.
$ python3 tools/level_renderer.py --level 1 --out schematic --schematic
Wrote schematic for level01 to schematic/level01_schematic.png.
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

A sheet per level made from its files: graphics loaded, wall types used, clickable walls, every script entry with a one-line description, items and monsters placed, automap legend, text ids. `--out docs/levels` writes all 29 and an index.

```
$ python3 tools/level_report.py --level 1 | grep -E "^- Area|^\| block 621 "
- Area (WLL header): 0 = KEEP (decorations `KEEP.SHP` / `.DAT`).
| block 621 (x 13, y 19) | `0x12D2` | party steps in, wall clicked | moves the party to level 2, block 106, facing 2; ...
```

### `lol1_progression.py`

The level-to-level table and the door calls, one row per static call with the entries that reach it and the tests that guard it. `--check` on the CD edition requires `docs/PROGRESSION.md` to equal the text it prints, every level in the table to have a sheet in `docs/levels/` and every sheet to have rows, and each sheet to link its anchored rows (`PROGRESSION.md#level-N`) and `NUMBERS.md`. On the floppy edition it still reads every level script and does not compare that page.

```
$ python3 tools/lol1_progression.py --check
CHECK progression: 71 level changes, 136 door calls; docs/PROGRESSION.md matches; 29 linked level sheets
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

A palette's colours: a `.PAL` or `.COL` file, or the palette inside a CPS. One row per colour with the 6-bit VGA values and the 8-bit RGB; `--out DIR` also writes `DIR/NAME_EXT_swatch.png`, 16 × 16 squares with colour 0 top left. A file longer than 768 bytes (floppy `MONSTERS.PAL`) shows its first 256 colours unless you pass `--all`.

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

Raw strings of every text file (`--out` writes one JSON per file).

```
$ python3 tools/extract_dialogue.py
90 files, 6495 strings, {'ENG': 2165, 'FRE': 2165, 'GER': 2165}
```

### `decode_dialogue.py`

Readable text straight from the game files (any language file; also `TRIG.TBL`).

### `list_likely_spellings.py`

Prints English words in the text tables that are one small edit from a system-dictionary word, for a person to judge. French and German are checked only for a broken string table. It writes no patch. It reads the English word list at `/usr/share/dict/words` (Linux and macOS); on Windows, or for another list, give one with `--words FILE`. `--check` exits nonzero when a table or a bigram is out of range.

```
$ python3 tools/list_likely_spellings.py --data DATA --check
```

```
$ python3 tools/decode_dialogue.py LEVEL01.ENG --index 0
[0] Welcome to Gladstone Keep.  King Richard awaits you in the throne room.
```

### `voc_reader.py`

Sound samples: blocks and rate; WAV output.

```
$ python3 tools/voc_reader.py VOC.PAK:1BOLTC.VOC --out bolt.wav
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

XMIDI music (`.XMI`, and the XMIDI-container `.C55` and `.PCS` files) to standard MIDI files, one per sequence (`--out`). `--check` converts every sequence of every file and re-reads each result as MIDI.

```
$ python3 tools/xmi_to_midi.py LORE01A.XMI --out midi | head -3
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
$ python3 tools/save_reader.py /path/to/cd/_LEVEL1.TMP   # a level file the CD game wrote during play (game-written, not shipped)
level file; ends at 1529 as the layout predicts: True
  difficulty 1, 0 changed wall bytes, 4 monster slots in use, 0 flying objects
$ python3 tools/save_reader.py /path/to/scummvm/saves/lol-cd.NNN
ScummVM save, CD, version 21: "<save name>"; ends at <size> as the layout predicts: True
  <one line per character: name, HP, MP, skills, XP>
  level <n>, block <b> (x, y), facing <f>, money <m>, <k> game flags set, levels stored [...], <i> items in use
```

The counts and end offset depend on the save you pass.

### `example_images.py`

Regenerates each image in `examples/` and the two level schematics in `docs/images/` with its listed command and compares pixels; part of `check_all.py`. `--out` writes today's versions.

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

### `lol1_driver_tables.py`

Reads the entry table of each `.ADV` member in `DRIVERS.PAK` (ID, routine offset, `55 8B EC` prologue) and the `ALFX.DRV` selector dispatch. On the CD it also reads the `ENG`, `FRE` and `GER` copies of `DRIVERS.PAK` and requires them to be identical. See the [driver page](../docs/formats/drivers.md#sound-drivers-driverspak).

```
$ python3 tools/lol1_driver_tables.py --check
CHECK drivers: 6 ADV tables per archive; CD 150 entries, ALFX +0x1A8E 24 wrappers; CD language 146 entries, ALFX +0x1A8E 24 wrappers; 3 identical language copies
```

### `lol1_attack_types.py`

Re-reads the creature attack switch (types 1 to 10) and defense switch (types 1 to 6) in `MAIN.EXE` of either edition: the bound test, the jump table, the first bytes of each arm and the arm addresses printed on the [rules page](../docs/game_rules.md#monster-attack-and-defense-types). Types 5 and 7, and any type outside the range, go straight to the routine's epilogue. The whole file, overlay bodies included, holds one same-segment call to the attack routine and one far call to the defense routine, the latter behind the test of attacker bit `0x8000`. Pass `--floppy FOLDER` to check the floppy edition in the same run. It adds no spell table: spell effects by rank are on the [casting table](../docs/unknowns/07_native_rules.md#casting).

```
$ python3 tools/lol1_attack_types.py --check
CHECK attack_types: 10 attack arms and 6 defense arms at the page addresses; types 5 and 7 and out-of-range types go to the epilogue; one same-segment attack call and one far defense call, no other reference
```

### `lol1_mode_paths.py`

Re-reads the direct instance mode-byte stores in both editions (ten CD, eight floppy), the CD setter's call immediates, the script modes, finale catalog row 40 with its index sites and the startup sort, and the absence of the three palette row numbers as constant stride-20 indexes. Needs Capstone (`requirements.txt`). On a floppy folder the finale catalog is not present, so that half of the line is the floppy store and palette sentence. The absence checks rule out literal constants only; a computed index is not excluded.

```
$ python3 tools/lol1_mode_paths.py --check
CHECK mode_paths: 10 CD mode-byte stores, none stores 10, no resolved caller or script passes 10, 3 LEVEL23 calls pass 11; finale row 40 is one of 93 catalog rows, no index site loads the constant 40, startup sorts rows 4-92; no stride-20 site loads palette rows 122, 204 or 206 as a constant
```

### `lol1_name_callers.py`

On the CD, re-reads the `00000.VOC` catalog row in `ENG/FINALE.EXE` and checks that the three unused palette names occur in `FILEDATA.FDT` and in no program, archive payload, or `INSTALL.EXE` beside `DATA`. On a floppy folder it reports that the CD finale is not there.

```
$ python3 tools/lol1_name_callers.py --check
CHECK name_callers: FINALE.EXE+0x1D1D0 is the 00000.VOC catalog row (44115 bytes); no other reference to the name's offset; the three palettes are catalog names only, installer included
```

### `lol1_loose.py`

Walks the loose CD `DATA` files. Thirty-seven reach their last byte, including fonts, string tables, executable images, symbol tables and the six finale blend tables (one 256 × 256 grid each). The check reproduces bytes 0–65531 of both distinct finale blend tables and pins the four-byte trailer. It runs the `lol1_blend_indices.py` census. It also re-reads `README.ENG` beside `DATA` at file +0x72, the eight bytes `LANDS OF`. See the loose-file page for the palette pairings and the bytes whose writer is open. [Loose-file formats](../docs/formats/loose.md)

```
$ python3 tools/lol1_loose.py --check
CHECK loose: 37 files reach the last byte (3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 5 mz, 2 le, 2 overlay, 1 text, 1 com, 3 symbol, 3 mz plus symbol tail, 6 blend table); 0 open; palette self-blend 22/42 matches BLEND.TAB 65532 of 65536 from RETURN.CPS, BLEND2.TAB 65532 of 65536 from FACE.CPS; last four bytes E4 D5 02 00 are row FF, never indexed, writer open
```

### `lol1_blend_indices.py`

Pins the finale blend reader in the three CD `FINALE.EXE` files and the floppy one: slot 5, the 65536-byte read, the page-4 source and page-2 destination, the shared page-4/5 buffer, the three passes and the `table[source*256+destination]` lookup. It decodes the four source pictures and checks the source rows each table can be indexed with (199 and 190, none above `EF`). On the CD it also models the destination pages and pins the cells met. `--indices` lists the ranges. [Finale blend table inputs](../docs/formats/finale-blend-indices.md)

```
$ python3 tools/lol1_blend_indices.py --check
CHECK finale blend: 3 languages, 4 calls, 3 passes each; source rows BLEND.TAB 199, BLEND2.TAB 190 (highest EF); modelled cells BLEND.TAB 7696, BLEND2.TAB 7876; no source 255
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
CHECK exe_tables: CD MAIN.EXE, CD MAINW.EXE: character rows 0,0,0,1,0,0,1,2,4, spells, experience, difficulty rows, prices, timers, mode flags, spell/wall/TIM/EMC2 pointers as the pages give, bad=none
```

### `repo_guard.py`

Asset-policy guard, run by `check_all.py`: fails if git tracks any game file type (`.PAK`, `.CPS`, `.SHP`, `.XMI`, …), converted media (`.MID`, `.WAV`, …), a PNG outside `examples/` and `docs/images/`, a file over 300 KB (except the tables it lists by name), a machine path, or a word from an optional local word list (`.git/info/private_words`, never tracked). `--release` also checks every commit's author and committer address. Needs no game data. `N` is the number of tracked files; with a local word list the line ends `private word list: K words` instead.

```
$ python3 tools/repo_guard.py --check
CHECK repo_guard: N tracked files; game files, converted media, stray PNGs, files over 300 KB, machine paths, words from the local list, or commit identities and messages: none (0); private word list: not present, skipped
```

### `tests/test_emc2_corpus.py`

Disassembles every level and item script (60 per edition) and fails on any unknown opcode, function or branch target. `check_all.py` runs it as its last check.

```
$ python3 tests/test_emc2_corpus.py
/path/to/DATA: PASS 60/60 scripts, 124298 DATA words, 109845 instructions, 756 TEXT strings, 0 unknown opcodes/functions
```

## Command-line conventions

Set `LOL1_DATA` or pass `--data` for the original game's DATA or floppy folder. Run `--help` for the tool's inputs and modes. Use `--check` for the available read-only validation and `--out` to write a result to a path you choose. Read-only listings print to stdout. `check_all.py` runs the whole suite by default. `doc_links.py` and `repo_guard.py` use repository files and need no game data.

| Difference | Why it remains |
|---|---|
| `LOL1_DATA`, where LoL2 and LoL3 use `LOL2_DAT` and `LOL3_DAT` | Each name follows the game's own folder: LoL1 keeps its files in `DATA`, LoL2 and LoL3 in `DAT`. Shells and scripts already set these names. |
| `--pak` and `--game-dir` | The CD and floppy group resources differently. `--pak` restricts a member search. The loose-file survey can select the install root separately. |
| A positional script, archive or save | `emc2_decompile.py`, `pak_reader.py` and `save_reader.py` can inspect one named file. The folder option helps resolve a bare resource name or run corpus checks. |
| Output path can be a file or folder | A single result, such as a WAV or a JSON save, takes a file. Frame and map batches take a folder. For `shp_renderer.py`, a named member selects a folder of PNGs and no member selects an inventory file. |
| `--walls-png` and `extract_music.py --out-dir` | These request a second output alongside the ordinary `--out` product, assembled wall pages or raw music files. |
| `lol1_pak_writer.py` has no `--out` | It rebuilds archives in memory only, to compare them with the originals, so it cannot write into the game folder or the repository. `--check` is its only mode. |
| `lol1_compression_writer.py` has no `--out` | It re-encodes pictures in memory only, to read them back through the existing readers, so it cannot write into the game folder or the repository. `--check` is its only mode. |
| Older output flags | The original `--out-dir`, `--png`, `--wav`, `--json` and `--output` spellings are kept as aliases and shown in `--help`, where they previously requested the same output. |

## Documentation index

`doc_index.py` reads the repository's Markdown pages and generates [docs/index.json](../docs/index.json).
Its `pages` records include the title, original path, question IDs and cited tool source paths.
`answers` uses the Page or Where column of [Open questions](../docs/OPEN_QUESTIONS.md).
`question_references` records other references to the same IDs. The top-level `questions`
object preserves the published state and lists each question's answer pages. Tool citations
include command examples. The index covers the Markdown files shipped in the repository,
including the root pages, example and evidence notes, and issue templates. In a git checkout
it reads only tracked pages, so local untracked notes do not change the check.

```bash
python3 tools/doc_index.py --out docs/index.json
python3 tools/doc_index.py --check
```

The check also runs in `check_all.py` and GitHub Actions. It needs no game data.

`lol1_script_writer.py` assembles the lossless listings of `emc2_decompile.py --assembly` and `parse_tim.py --list NAME --assembly` back into scripts. `--check --data DATA` rebuilds every EMC2 and TIM script in memory and compares it byte for byte; `LISTING --out NEW` writes one new file, never over an existing one, inside the repository, `--data` or a folder holding PAK or TLK archives. See [round trip](../docs/ROUND_TRIP.md#scripts-emc2-and-tim).

`lol1_level_writer.py` rebuilds every CMZ maze, WLL wall table, decoration DAT and ENG/FRE/GER string table in the PAKs of `--data` and compares it byte for byte (`--check`; no output option). CMZ files are byte-identical because the parsed Frame4 packet choices of the original are kept; level 24's five extra bytes per block are kept verbatim without a parse. See [round trip](../docs/ROUND_TRIP.md#levels-and-text).

`lol1_xmi_writer.py` rebuilds every XMI, C55 and PCS score (in the PAKs of `--data` and loose in it) from its IFF chunks and parsed EVNT events and compares it byte for byte (`--check`; no output option). Delays, statuses, note durations and the stored variable-length widths are written from the parsed fields; TIMB/RBRN payloads, padding and the bytes after each end-of-track are kept verbatim. For standard MIDI use `xmi_to_midi.py`. See [round trip](../docs/ROUND_TRIP.md#music-xmidi).

`doc_format_offsets.py` checks six format-page offsets against the readers that decode those fields, using small synthetic files. It runs in `check_all.py` and needs no game data. [Check audit](../docs/CHECK_AUDIT.md)

`check_all.py --quick` skips the Frame4, WSA and SHP re-encoding check and the progression walk. It lists each skip and reports the total elapsed time for the checks it ran.
