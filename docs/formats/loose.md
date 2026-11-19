# Loose files in the CD DATA folder

**Edition read:** the CD `DATA` folder. On a floppy install (no `L01.PAK`) the check returns without comparing, and `tools/rating.py` does not credit loose files there.

Thirty-seven files under `DATA` are not a PAK archive and not a `NN.TLK` speech archive. `tools/lol1_loose.py` walks twenty-five of them to the last byte: every byte belongs to a header, a directory or an entry. Twelve stay open. The insides of a program image are not disassembled. The walk stops once every byte belongs to the declared image.

## Fonts

**CONFIRMED.** `ENG/NEW6P.FNT`, `FRE/NEW6P.FNT` and `GER/NEW6P.FNT` are one file three times: 3213 bytes, signature `0x0500` at byte 2, 226 glyphs, height 8. The size field at byte 0 equals the file length and every glyph fits the font height. The parts tile the file with no gap and no overlap, in this order: header 0..14 (seven words), descriptor 14..20, bitmap-offset table 20..472 (two bytes per glyph), width table 472..698 (one byte per glyph), glyph bitmaps 698..2761, height table 2761..3213 (two bytes per glyph). The ranges come from the header words at +4, +6, +8 and +12 and the glyph count. Glyphs may share a bitmap offset (54 glyphs have offset 0, so no bitmap); the 86 distinct bitmaps tile 698..2761 on their own. That is the DOS font layout in [fnt.md](fnt.md). The name `NEW6P.FNT` sits at `ENG/LANDS.EXE+0x20279`, `ENG/FINALE.EXE+0x1D9C8`, `FRE/FINALE.EXE+0x1E07A` and `GER/FINALE.EXE+0x1E0C4`.

## String tables

**CONFIRMED.** `HARDRIVE/ENG.LM`, `FRE.LM`, `GER.LM`, `SETUPENG.DIP`, `SETUPFRE.DIP` and `SETUPGER.DIP` are a uint16 offset table followed by NUL-terminated strings. The first word is both the length of the table and the offset of the first string. Each later offset begins at the previous string's NUL, and the last NUL is the last byte of the file.

`ENG.LM` is 1794 bytes and its first word is `0x0058` (44 strings). `SETUPENG.DIP` is 3881 bytes and its first word is `0x00D6` (107 strings). String 1 is `File Write Error`.

`HARDRIVE/MAIN.EXE+0x33C44` and `HARDRIVE/MAINW.EXE+0x336E8` name `FILEDATA.FDT`, `ENG.LM`, `FRE.LM` and `GER.LM` in that order. `HARDRIVE/SETUP.EXE+0x17518` contains `SETUP%s.DIP`. `INSTALL.EXE` (134819 bytes, beside `DATA`) contains `SETUPENG.DIP` at `+0x7D69`.

These are plain strings. The `.DIP` members inside the language PAKs use the [text](text.md) layout. This walk does not read those members.

## Archive inventory

**CONFIRMED.** `FILEDATA.FDT` is 1275 records of 20 bytes and then a name pool. Record 0's first uint32 is `0x639C`, which is 1275 times 20, so the pool starts where the records end. Records 0 through 1273 each hold the next name in the pool. The names are non-empty ASCII, they follow one another with no gap, and the last name's NUL is the last byte (`YVIC.TIM`). Record 1274 is 20 zero bytes.

`HARDRIVE/MAIN.EXE+0x334DC` and `HARDRIVE/MAINW.EXE+0x32F82` contain `FILEDATA.FDT`.

The three palette rows already measured in [Q14](../unknowns/14_palette_callers.md) are re-read here. Row 122 is `ALTPAL3.PAL` with size `0x300`, member offset `0x1B8B5` at +0x0C and flags `0x1000` at +0x12. Row 204 is `CAV_PLT2.PAL`, member `0x1D72C`. Row 206 is `CAV_PLT4.PAL`, member `0x1DD2C`. Same size and flags.

## Icons

**CONFIRMED.** `HARDRIVE/LANDS.ICO` and `HARDRIVE/SETUP.ICO` are 766 bytes. The directory says reserved 0, type 1, count 1. The one entry is 32 by 32, 16 colours, image size 744, image offset 22. The image is a 40-byte bitmap header (width 32, height 64, one plane, 4 bits), a 64-byte palette, a 512-byte XOR mask and a 128-byte AND mask. `INSTALL.EXE+0xFEB5` is `LANDS.ICO` and `+0xFF05` is `SETUP.ICO`.

## Program information files

**CONFIRMED.** `HARDRIVE/LANDS.PIF` and `HARDRIVE/DOSETUP.PIF` are 545 bytes. At `0x171` the section name is `MICROSOFT PIFEX`. Its data field is offset 0 and size 369, which is the basic record. At `0x187` the name is `WINDOWS 386 3.0`, data at `0x19D` for 104 bytes. At `0x205` the name is `WINDOWS 286 3.0`, data at `0x21B` for 6 bytes, and the next-section word is `0xFFFF`. Data offsets in the section header are absolute. Those spans meet, do not overlap, and end on byte 545. The program name at file `0x24` is `LOLCD.EXE` in `LANDS.PIF` and `SETUP.EXE` in `DOSETUP.PIF`. `INSTALL.EXE+0xFEEA` is `LANDS.PIF` and `+0xFF1A` is `DOSETUP.PIF`.

## Programs whose MZ image is the whole file

**CONFIRMED.** For these seven files the uint16 at +2 (bytes used in the last page) and the uint16 at +4 (page count of 512) declare a size equal to the file. The header length, paragraph count at +8 times 16, sits inside the file, and the relocation table (offset at +0x18, count at +6, four bytes per entry) fits inside the header.

| File | Bytes | Header |
|------|------:|-------:|
| `ENG/FINALE.EXE` | 132328 | 8704 |
| `FRE/FINALE.EXE` | 134122 | 8704 |
| `GER/FINALE.EXE` | 134212 | 8704 |
| `HARDRIVE/LOLCD.EXE` | 19356 | 1024 |
| `HARDRIVE/SETUP.EXE` | 103188 | 7168 |
| `HARDRIVE/VDSPD.386` | 10936 | 64 |
| `HARDRIVE/VWWSD.386` | 5371 | 64 |

`VDSPD.386` and `VWWSD.386` are an MZ stub plus an LE (Windows VxD) program. Both stubs carry the text `This program cannot be run in DOS mode.` The uint32 at MZ `+0x3C` is `0x80`, where `LE` stands with byte and word order 0. The LE loader and fixup sections end before the data pages and the gap up to them is zero bytes. The data pages, (page count - 1) times 4096 plus the last-page byte count, end where the non-resident name table starts, and that table ends on the last byte:

| File | Data pages at | Pages | Last page | Non-resident names | Total |
|------|-------------:|------:|----------:|-------------------:|------:|
| `VDSPD.386` | `0x800` | 3 | 641 | 55 bytes at `0x2A81` | 2048 + 2 x 4096 + 641 + 55 = 10936 |
| `VWWSD.386` | `0x400` | 2 | 201 | 50 bytes at `0x14C9` | 1024 + 4096 + 201 + 50 = 5371 |

The non-resident name tables name the modules: `MMSys Win386 VDSPD Device (Version 3.x)` and `Win386 VWWSD Device  (Version 0.1)`. `INSTALL.EXE+0xFDCA` is `vdspd.386` and `+0xFDFD` is `VWWSD.386`. `ENG/FINALE.EXE+0x1DB04` is the name inside the sentence `Digitized samples unavailable -- VWWSD.386 not found`. The check does not disassemble the image.

## MAIN.EXE and MAINW.EXE

**CONFIRMED.** Both are an MZ image followed by an FBOV overlay. The signature `FBOV` stands at the first byte after the MZ image. The uint32 at `FBOV+4` is the body length, and the 16-byte header plus that body is the rest of the file. The uint32 at `FBOV+8` falls inside the MZ image, after the DOS header. On `MAIN.EXE` that field is `0x2FC50`, the directory offset already used by the [native reference scan](../unknowns/18_native_records.md).

| File | MZ image ends | Body length | `FBOV+8` | File length |
|------|-------------:|------------:|---------:|------------:|
| `HARDRIVE/MAIN.EXE` | 248896 (`0x3CC40`) | `0x1A5F0` | `0x2FC50` | 356928 |
| `HARDRIVE/MAINW.EXE` | 247328 (`0x3C620`) | `0x19B60` | `0x2F710` | 352656 |

**CONFIRMED.** The third uint32 of the FBOV header, `0x127` in both files, is the row count of the directory that `FBOV+8` points at. The directory rows are 8 bytes (four uint16: segment, size, kind, adjust). Walking from `MAIN.EXE+0x2FC50` (`MAINW.EXE+0x2F710`), the segment word never decreases and points inside the MZ image for 295 (`0x127`) rows. The last row, at `MAIN.EXE+0x30580`, is segment `0x393C` with size 128: header 14336 + `0x393C` x 16 + 128 = 248896, the end of the MZ image (`MAINW.EXE+0x30040`: segment `0x38DA`, 14336 + `0x38DA` x 16 + 128 = 247328). The next 8 bytes are not a row: they start the text `main.exe` (`mainw.exe`), whose first word as a segment (`0x616D`) lies past the image. The loader instruction that reads `FBOV+12` was not traced.

## COM program

**CONFIRMED.** `HARDRIVE/VISBIOS.COM` is 30976 bytes. Byte 0 is `E9 1D 00`, a near jump to file offset `0x20`. Bytes 4 through 25 are `Revision 1.01 02/12/93` and byte 26 is NUL. A COM file has no length field, so the file length is the image. The bytes after the revision string are that program. The check does not disassemble them. `INSTALL.EXE+0xFD78` is `VISBIOS.COM`.

Its own strings say what it is: a resident Tandy driver for the VIS (Tandy Sensation) video and synthesizer. `+0x5151` `VIS BIOS Extensions for Sensation`, `+0x519F` `Tandy Corporation`, `+0x1C4` `VIS video emulation`, `+0x215` `VIS synthesizer`, `+0x513F` `Installed OK.` The check pins these five strings.

## Editor text

**CONFIRMED.** `FRE/STATE.RST` is 187 bytes. Every byte is a carriage return, a line feed or a printable ASCII character, and the file ends with a line feed. It starts `[edit-]`. The French folder is the only copy under `DATA`.

It is a developer's text-editor state file left on the disc, not game data. Its sections are `[edit-]`, `[brief]` and `[shared-]`, with screen size, search and replace fields, and the last file edited, `r:\intro\td.bat`. The game does not read it: the name `state.rst` occurs, in any letter case, in none of `MAIN.EXE`, `MAINW.EXE`, `SETUP.EXE`, `LOLCD.EXE`, the three `LANDS.EXE`, the three `FINALE.EXE`, `DRIVERS.PAK` or `INSTALL.EXE` (the check scans them).

## Still open

**UNCONFIRMED.** `BLEND.TAB` and `BLEND2.TAB` in `ENG`, `FRE` and `GER` are 65536 bytes each. The three copies of each name are byte-identical, and the two names are different bytes. Their layout is not read here.

Who reads them, CONFIRMED in the bytes: the finale script. `LOLFINAL.TIM` in `ENG/FINALE2.PAK` (member at `+0xC9D0D`) has `BLEND.TAB` as TEXT string 3 (`+0xCAF7B`) and `BLEND2.TAB` as string 30 (`+0xCB08F`), among the WSA, CPS and VOC names. The nested-`0x19` function-6 instructions at `+0xC9D49` (`05 00 00 00 19 01 06 00 03 00`) and `+0xCA45B` (index `0x1E`) pass them in the same list of file names as `DEATH.WSA`, `RETURN.CPS` and the rest; functions 5 and 7 name them too. On the floppy `FINALE.EXE`, nested functions 6 and 7 forward a TEXT string to a resource routine ([Q6](../unknowns/06_tim_opcodes.md)). The CD `FINALE.EXE` routine that opens a 65536-byte table has not been traced.

Who writes them is open. `INSTALL.EXE` has the string-table entries 1049 `Creating intro blend tables...` (`+0x12AC0`) and 1050 `Creating finale blend tables...` (`+0x12ADF`), so the installer was written to report building blend tables. The CD installer loads its strings as a language base (`DS:0730`, 1000, 2000 or 3000) plus an index, through the routine at `INSTALL.EXE+0xAC00` (`+0xAC78`-`0xAC8A`). The index 45 (`WARNING!`) is pushed as an immediate at eight places (first `+0xC59C`); 46 to 50 are not pushed as immediates anywhere in the code segments, and 47 to 50 are not words in the data segment. No caller of entries 1049 and 1050 is found, and the CD ships the tables ready-made in `DATA`. The file names `blend.tab`, `blend2.tab`, `.tab` and `state.rst` occur, in any letter case, in none of `MAIN.EXE`, `MAINW.EXE`, `SETUP.EXE`, `LOLCD.EXE`, the three `LANDS.EXE`, the three `FINALE.EXE`, `DRIVERS.PAK` or `INSTALL.EXE`. Settling test: trace the CD `FINALE.EXE` handler of nested TIM `0x19` function 5/6 to the open of `BLEND.TAB` and its 65536-byte read, or regenerate both tables from a finale palette and compare them byte for byte.

**UNCONFIRMED.** `ENG/FINALE.TDS` (210583 bytes), `FRE/FINALE.TDS` and `GER/FINALE.TDS` (210724 bytes each) start `FB 52 10 03` (uint16 `0x52FB`, uint16 `0x0310`). The same four bytes start the tail of each `LANDS.EXE` after its MZ image. The English file is 357509 bytes with an image of 146176 (tail 211333). The French file is 359338 bytes with an image of 147952 (tail 211386). The German file is 359418 bytes with an image of 148032 (tail 211386). Each LANDS header is 10240 bytes. None of the first 16 uint32 values in the block equals the block length. The English symbol file and the English LANDS tail both end with `FILECHNG`, `new_size` and `.\FILECHNG.C`. Settling test: a record-length walk that consumes the block through its last byte.

## Tool

`python3 tools/lol1_loose.py --check`

```
CHECK loose: 25 files reach the last byte (3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 5 mz, 2 le, 2 overlay, 1 text, 1 com); 12 open (6 blend tables, 3 symbol files, 3 LANDS tails)
```
