# Format quick reference

Run the commands from the repository root with `LOL1_DATA` set to the
folder containing your original `GENERAL.PAK`. The samples use the CD
edition. On the floppy, level members are in `CHAPTERn.PAK` (for example `python3 tools/pak_reader.py list CHAPTER1.PAK`), and the TLK and TLC rows are CD only.
Set `LOL1_MAIN` to the CD's `DATA/HARDRIVE/MAIN.EXE` or the floppy `MAIN.EXE`, and `LOL1_SLOT` to a `_SAVEnnn.DAT` or `_LEVELn.TMP` the game wrote while you played (none are shipped).

| File or entry | What it contains | Format and evidence | Tool | Command |
|---|---|---|---|---|
| `.PAK`, `FILEDATA.FDT` | Named resource archive and the separate archive inventory | [PAK](formats/pak.md), [archive inventory](unknowns/09_pak_order.md) | Archive indexer | `python3 tools/pak_indexer.py --check` |
| `NN.TLK` | CD speech archive with named VOC entries | [TLK](formats/tlk.md) | TLK verifier | `python3 tools/tlk_verify.py --check` |
| `.VOC` | Creative Voice audio blocks | [VOC](formats/voc.md) | VOC reader | `python3 tools/voc_reader.py --check` |
| Frame4 / LCW blocks | Compressed bytes inside bitmaps, map and animation resources | [LCW](formats/lcw.md) | LCW checker | `python3 tools/decode_frame4.py --check` |
| `.CPS` | Bitmap with an optional VGA palette | [CPS](formats/cps.md) | CPS reader | `python3 tools/cps_reader.py PARCH.CPS` |
| `.SHP` | Indexed shapes or sprite frames | [SHP](formats/shp.md) | Shape reader | `python3 tools/shp_renderer.py --check` |
| `.WSA` | Animation deltas | [WSA](formats/wsa.md) | WSA reader | `python3 tools/wsa_extract.py --check` |
| `.FNT` | Bitmap glyphs and dimensions | [FNT](formats/fnt.md) | Font reader | `python3 tools/fnt_reader.py --check` |
| `.PAL`, `.COL` | Raw VGA colour triplets | [Palettes](formats/palette.md) | PAK reader lists palette members | `python3 tools/pak_reader.py list L02.PAK` |
| `.CMZ` | Compressed grid of map blocks and wall IDs | [CMZ](formats/cmz.md) | CMZ analyzer | `python3 tools/cmz_analyzer.py --check` |
| `.WLL` | Wall properties such as art, special type and flags | [WLL](formats/wll.md) | WLL parser | `python3 tools/wll_parser.py --check` |
| `.VCN`, `.VMP` | Wall tiles and tile layouts | [VCN and VMP](formats/vcn_vmp.md) | Tileset reader | `python3 tools/vcn_vmp_reader.py --check` |
| `.XXX` | Level automap legend | [XXX](formats/xxx.md) | Legend reader | `python3 tools/xxx_reader.py LEVEL1.XXX` |
| `AREA.DAT` | Decoration definitions for an area | [Decoration DAT](formats/dat.md) | DAT reader | `python3 tools/dat_reader.py KEEP.DAT --index 1` |
| `.TLC` | CD transparency lookup tables | [TLC](formats/tlc.md) | TLC reader | `python3 tools/tlc_reader.py LEVEL01.TLC` |
| `.INF`, `.INI` | EMC2 events and initialization scripts | [EMC2](formats/emc2.md) | EMC2 disassembler | `python3 tools/emc2_decompile.py L01.PAK --entry LEVEL1.INI` |
| `.TIM` | Timed animation and dialogue commands | [TIM](formats/tim.md) | TIM parser | `python3 tools/parse_tim.py --check` |
| `.ENG`, `.FRE`, `.GER` | Indexed global and level text strings | [Text](formats/text.md) | Text decoder | `python3 tools/decode_dialogue.py LEVEL01.ENG --index 0` |
| `.TXT`, `.DIP` | Intro, history and finale text: each `.DIP` is an indexed string file in the [text](formats/text.md) layout; `CREDITS.TXT` is the end credits. Named only by the intro (`LANDS.EXE`) and finale (`FINALE.EXE`) programs. **CONFIRMED** layout and names | [Archive inventory](formats/README.md) | Text decoder | `python3 tools/decode_dialogue.py LOLINTRO.DIP --pak STARTUP.PAK --index 1` |
| `.XMI`, `.C55`, `.PCS` | XMIDI sequences for the selected sound setup | [Music](formats/music.md) | Music inventory | `python3 tools/extract_music.py --check` |
| `.ADL` | AdLib sequence and program data | [Music](formats/music.md) | ADL reader and MIDI projector | `python3 tools/adl_to_midi.py --check` |
| `.ADV`, `.DRV` | Native sound drivers | [Drivers](formats/drivers.md) | PAK reader lists driver members | `python3 tools/pak_reader.py list DRIVERS.PAK` |
| `TRIG.TBL` | Indexed manual-prompt text | [TBL](formats/drivers.md#worked-example-trigtbl-copy-protection-text) | Text decoder | `python3 tools/decode_dialogue.py TRIG.TBL --pak GENERAL.PAK --index 0` |
| `WESTWOOD.001`, `.EXE` | CD installer archive and DOS executable images | [Executable locations](executable_tables.md#locating-the-executables) | Python reads the MZ tag | `python3 -c 'import sys; print(open(sys.argv[1], "rb").read(2))' "$LOL1_MAIN"` |
| `_SAVEnnn.DAT`, `_LEVELn.TMP` | Original DOS save and level sidecar layouts | [Saves](savegame_format.md) | Save reader | `python3 tools/save_reader.py "$LOL1_SLOT"` |
