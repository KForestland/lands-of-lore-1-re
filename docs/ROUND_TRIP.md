# Round-trip proof for LoL1

Five writers read the original files, build a replacement in memory and compare it with the original. Their checks write nothing to disk. "Byte-identical" means the rebuilt file equals the original file. "Decode-identical" means the rebuilt file reads back through the existing readers to the same pixels and palettes, while its compressed bytes differ.

The CD counts cover the `DATA` folder with its `ENG`, `FRE` and `GER` subfolders (CD1.02). The floppy counts are an English floppy installation.

| Writer | What is rebuilt | Comparison | CD | Floppy |
|---|---|---|---:|---:|
| `lol1_pak_writer.py` | PAK archives and PAK-layout TLK speech files, from their ordered members | Byte-identical | 132 PAKs and 30 TLKs, 7,209 members | 15 PAKs, 1,213 members |
| `lol1_compression_writer.py` | CPS, CMZ, VCN and VMP bitmaps, re-encoded with a new Frame4 encoder | Decode-identical: palette and expanded pixels | 320 files | 167 files |
| same | WSA animations: XOR deltas and Frame4 re-encoded, frame offsets regenerated | Decode-identical: every frame through the reader | 529 files, 12,785 deltas | 254 files, 5,420 deltas |
| same | SHP shapes: scanlines and Frame4 re-encoded, shape offsets and sizes regenerated | Decode-identical: flags, dimensions and pixels of every shape (colour tables copied) | 236 files, 7,299 shapes | 95 files, 3,601 shapes |
| `lol1_script_writer.py` | EMC2 level and item scripts (INF/INI) and TIM cut-scene scripts, assembled from their lossless listings | Byte-identical | 60 EMC2 and 157 TIM scripts (139 in `DATA`, 6 each in `ENG`, `FRE`, `GER`) | 60 EMC2 and 147 TIM scripts |
| `lol1_level_writer.py` | CMZ mazes (Frame4 packets kept), WLL wall tables, decoration DATs and ENG/FRE/GER string tables, from their parsed fields and strings | Byte-identical | 29 CMZ, 29 WLL, 12 DAT, 30 each of ENG, FRE and GER | 29 CMZ, 29 WLL, 13 DAT (`CIMMERIA.DAT` is in two PAKs), 30 ENG |
| `lol1_xmi_writer.py` | XMI, C55 and PCS XMIDI scores: IFF chunk sizes and order, the INFO sequence count and every EVNT event, from their parsed fields | Byte-identical | 51 files (18 XMI, 17 C55, 16 PCS), 620 sequences, 71,966 events | 57 files (20 XMI, 19 C55, 18 PCS), 808 sequences, 88,438 events |

On both editions none of the 1,085 (CD) and 516 (floppy) re-encoded files is byte-identical to its original. All Frame4 streams in them (20,354 on the CD, 9,075 on the floppy) decode to the same bytes through both Frame4 readers.

## PAK and speech archives

**CONFIRMED.** A PAK directory is a list of u32 member offsets, each followed by the member's NUL-terminated name, starting at +0; members carry no length. In every original archive of both editions the last name is followed by one more u32 equal to the file size and then five zero bytes, after which member 0 starts. The writer emits that directory from the members' names and lengths, then the members in order, and every archive comes out byte for byte equal to the file. Example: the first offset in CD `GENERAL.PAK` is `0x466`. [PAK layout and the end of the directory](formats/pak.md#end-of-the-directory-in-the-original-files)

## Bitmaps, WSA and SHP

**CONFIRMED.** For a bitmap the writer keeps the compression and palette fields and re-encodes the pixels. It recalculates the size word at +0x00 and writes the expanded size at +0x04. For example, the original CD `PARCH.CPS+0x00` holds 12,665 and its re-encoded copy holds 61,471. The palette starts at +0x0A in both. For a WSA it re-encodes each stored XOR delta, including the closing one, and regenerates the frame offsets at +0x0E and the delta buffer size at +0x0A. For a SHP it regenerates the shape offsets, each 10-byte shape header's sizes and the scanlines with their transparent runs; shapes stored in a bitmap wrapper are then wrapped again. Each rebuilt file must read back through the existing readers with the same pictures. [Frame4 commands](formats/lcw.md) · [Bitmap header](formats/cps.md#layout) · [WSA layout](formats/wsa.md#layout) · [SHP shape layout](formats/shp.md#shape-layout)

This proves that the formats can be written, not that the original compressor is reproduced. The new encoder chooses a different mix of literal, fill and copy commands, and the WSA and SHP writers choose different XOR and transparent runs, so the rebuilt files are larger than the originals (see [tools/README](../tools/README.md#lol1_compression_writerpy)).

## Scripts (EMC2 and TIM)

**CONFIRMED.** `emc2_decompile.py --assembly` and `parse_tim.py --list NAME --assembly` write a lossless listing (JSON): the FORM length convention, each chunk's tag and alignment byte, the EMC2 entry table, one row per EMC2 instruction (opcode, mnemonic, argument and encoding mode, plus the spare low byte where the encoding keeps one), one row per TIM command (delay, opcode, operands) and the TEXT string table with its offsets. No chunk of a shipped script falls back to raw hex and no TIM word is left outside a command row. `lol1_script_writer.py` assembles a listing back into the script and refuses a listing that does not read back to itself. Changing one instruction's argument in a listing changes only that word, and the rebuilt script disassembles to the changed instruction. [EMC2 scripts](formats/emc2.md) · [TIM opcodes](unknowns/06_tim_opcodes.md)

The assembler writes only a new file given with `--out`, and refuses an existing file, a path inside the repository or `--data`, and any folder at or below one holding a PAK or TLK archive.

The [native EMC2 function table](emc2_native_handlers.md) compares all 192 CD slots starting at `MAIN.EXE+0x33F64` with the documentation. The byte comparison above covers the script operands and encoding. Each native-handler verdict records how far the original body explains its effect.

## Levels and text

**CONFIRMED.** `lol1_level_writer.py --check` rebuilds every CMZ, WLL, decoration DAT and ENG/FRE/GER string table in the PAKs of `--data` and compares it with the original; each WLL, DAT and string table must also read back through `wll_parser.py`, `dat_reader.py` and `decode_dialogue.py` to the same records and strings. WLL and DAT files are rebuilt from their parsed records. String tables are rebuilt from the parsed offset directory and strings, not copied; the offsets are kept as parsed because some tables point two entries at the same string. [Maze format](formats/cmz.md)

A CMZ is a Frame4-compressed bitmap. Its maze fields (the 32 by 32 grid, the per-block length word and each block's four wall bytes) are parsed, and the writer also parses the original Frame4 stream into its packets (literal, fill, relative, absolute and long copies, end) and writes those same packets again. The CMZ files are byte-identical because the original packet choices are kept: the decode-identical encoder of `lol1_compression_writer.py` reproduces none of the 29 CMZ files on either edition. If an edited field no longer matches the kept packets, the maze is compressed afresh with that encoder (decode-identical, not the original bytes) and the size word is recomputed.

`LEVEL24.CMZ` stores 9 bytes per block instead of 4. The five bytes after the walls are kept verbatim per block without a parse: both `MAIN.EXE` files copy only the four wall bytes and their meaning is open ([Q3](unknowns/03_level24_cmz.md)). No original CMZ has bytes after its Frame4 end command; the writer would keep such bytes verbatim too.

Changing one wall byte, one WLL record field, one decoration offset or one string (with the later offsets moved by `replace_string`) gives a different file that reads back through the existing readers with only that change. The checks write nothing; the writer has no output option.

## Music (XMIDI)

**CONFIRMED.** `lol1_xmi_writer.py --check` rebuilds every XMI, C55 and PCS file in the PAKs of `--data` (and any loose in it) and compares it byte for byte. Chunk sizes, the `INFO` sequence count and each `EVNT` stream are written from the parsed fields: each event's delay bytes, its status byte (XMIDI has no running status), its data bytes, a note's duration and the stored width of every variable-length number. Kept verbatim are the payloads of the other chunks (`TIMB`, `RBRN`), the `FORM`/`CAT` type tags, the pad bytes and the bytes after each end-of-track (368 on the CD, 476 on the floppy). The file and sequence counts equal those of `xmi_to_midi.py --check`. The floppy has six more files than the CD: `LOREINTR` and `LOREFINL` in their XMI, C55 and PCS forms (intro and finale scores, in `INTROVOC.PAK` and `FINALE2.PAK`); the CD `DATA` folder holds neither. ADL files are not XMIDI and are not covered. [Music formats](formats/music.md#writing-the-original-scores)

Changing one note's key gives a file that differs in that one byte and converts through `xmi_to_midi.py` to the same MIDI except for that note's on and off events. The check writes nothing; the writer has no output option. Standard MIDI files still come from `xmi_to_midi.py`, unchanged.

## Run the checks

```bash
python3 tools/lol1_pak_writer.py --data "$LOL1_DATA" --check
python3 tools/lol1_compression_writer.py --data "$LOL1_DATA" --check
python3 tools/lol1_script_writer.py --data "$LOL1_DATA" --check
python3 tools/lol1_level_writer.py --data "$LOL1_DATA" --check
python3 tools/lol1_xmi_writer.py --data "$LOL1_DATA" --check
python3 -m unittest tests.test_round_trip tests.test_structures_write tests.test_xmi_write
```

All five checks run in `tools/check_all.py`. The PAK, compression, level and music writers have no output option; the script assembler writes one new file only when given a listing and `--out`. The unit tests use synthetic archives and pictures and need no game files: member order, duplicate names and the end of the directory; refused names and a final empty member; Frame4 literals, fills, back-references and the end command; a WSA skip and closing delta; a SHP colour table and a long transparent run. `tests.test_structures_write` covers a duplicate EMC2 mnemonic, a TIM tail and alignment byte, the refused output folders, a 9-byte maze block with kept Frame4 packets, an edited maze wall, WLL high bytes and duplicate or moved string offsets. `tests.test_xmi_write` covers a two-byte delay, a note duration, a byte after the end-of-track and a padded opaque chunk.
