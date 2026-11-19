# Loose files in the CD DATA folder

**Edition read:** the CD `DATA` folder. On a floppy install (no `L01.PAK`) the check returns without comparing.

Thirty-seven files under `DATA` are not a PAK archive and not a `NN.TLK` speech archive. `tools/lol1_loose.py` walks twenty-five of them to the last byte: every byte belongs to a header, a directory or an entry. Twelve stay open. The insides of a program image are not disassembled. The walk stops once every byte belongs to the declared image.

## Fonts

**CONFIRMED.** `ENG/NEW6P.FNT`, `FRE/NEW6P.FNT` and `GER/NEW6P.FNT` are one file three times: 3213 bytes, signature `0x0500` at byte 2, 226 glyphs, height 8. The size field at byte 0 equals the file length, and every glyph bitmap falls inside the file and inside the font height. That is the DOS font layout in [fnt.md](fnt.md). The name `NEW6P.FNT` sits at `ENG/LANDS.EXE+0x20279`, `ENG/FINALE.EXE+0x1D9C8`, `FRE/FINALE.EXE+0x1E07A` and `GER/FINALE.EXE+0x1E0C4`.

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

**CONFIRMED.** For these seven files the uint16 at +2 (bytes used in the last page) and the uint16 at +4 (page count of 512) declare a size equal to the file. The header length, paragraph count at +8 times 16, sits inside the file.

| File | Bytes | Header |
|------|------:|-------:|
| `ENG/FINALE.EXE` | 132328 | 8704 |
| `FRE/FINALE.EXE` | 134122 | 8704 |
| `GER/FINALE.EXE` | 134212 | 8704 |
| `HARDRIVE/LOLCD.EXE` | 19356 | 1024 |
| `HARDRIVE/SETUP.EXE` | 103188 | 7168 |
| `HARDRIVE/VDSPD.386` | 10936 | 64 |
| `HARDRIVE/VWWSD.386` | 5371 | 64 |

`VDSPD.386` and `VWWSD.386` are MZ images. Both carry the stub text `This program cannot be run in DOS mode.` `INSTALL.EXE+0xFDCA` is `vdspd.386` and `+0xFDFD` is `VWWSD.386`. `ENG/FINALE.EXE+0x1DB04` is the name inside the sentence `Digitized samples unavailable -- VWWSD.386 not found`. The check does not disassemble the image.

## MAIN.EXE and MAINW.EXE

**CONFIRMED.** Both are an MZ image followed by an FBOV overlay. The signature `FBOV` stands at the first byte after the MZ image. The uint32 at `FBOV+4` is the body length, and the 16-byte header plus that body is the rest of the file. The uint32 at `FBOV+8` falls inside the MZ image, after the DOS header. On `MAIN.EXE` that field is `0x2FC50`, the directory offset already used by the [native reference scan](../unknowns/18_native_records.md).

| File | MZ image ends | Body length | `FBOV+8` | File length |
|------|-------------:|------------:|---------:|------------:|
| `HARDRIVE/MAIN.EXE` | 248896 (`0x3CC40`) | `0x1A5F0` | `0x2FC50` | 356928 |
| `HARDRIVE/MAINW.EXE` | 247328 (`0x3C620`) | `0x19B60` | `0x2F710` | 352656 |

**UNCONFIRMED.** The third uint32 of the FBOV header is `0x127` in both files. The check records the value and does not read a use of it. Settling test: the instruction in the overlay loader that reads `FBOV+12`.

## COM program

**CONFIRMED.** `HARDRIVE/VISBIOS.COM` is 30976 bytes. Byte 0 is `E9 1D 00`, a near jump to file offset `0x20`. Bytes 4 through 25 are `Revision 1.01 02/12/93` and byte 26 is NUL. A COM file has no length field, so the file length is the image. The bytes after the revision string are that program. The check does not disassemble them. `INSTALL.EXE+0xFD78` is `VISBIOS.COM`.

## Editor text

**CONFIRMED.** `FRE/STATE.RST` is 187 bytes. Every byte is a carriage return, a line feed or a printable ASCII character, and the file ends with a line feed. It starts `[edit-]`. The French folder is the only copy under `DATA`.

## Still open

**UNCONFIRMED.** `BLEND.TAB` and `BLEND2.TAB` in `ENG`, `FRE` and `GER` are 65536 bytes each. The three copies of each name are byte-identical, and the two names are different bytes. The strings `BLEND`, `.TAB` and `STATE.RST` do not occur in `MAIN.EXE`, `MAINW.EXE`, `SETUP.EXE`, `LOLCD.EXE`, the three `LANDS.EXE` files, the three `FINALE.EXE` files, `DRIVERS.PAK` or `INSTALL.EXE`. Settling test: the open that reads 65536 bytes from `BLEND.TAB` or `BLEND2.TAB`.

**UNCONFIRMED.** `ENG/FINALE.TDS` (210583 bytes), `FRE/FINALE.TDS` and `GER/FINALE.TDS` (210724 bytes each) start `FB 52 10 03` (uint16 `0x52FB`, uint16 `0x0310`). The same four bytes start the tail of each `LANDS.EXE` after its MZ image. The English file is 357509 bytes with an image of 146176 (tail 211333). The French file is 359338 bytes with an image of 147952 (tail 211386). The German file is 359418 bytes with an image of 148032 (tail 211386). Each LANDS header is 10240 bytes. None of the first 16 uint32 values in the block equals the block length. The English symbol file and the English LANDS tail both end with `FILECHNG`, `new_size` and `.\FILECHNG.C`. Settling test: a record-length walk that consumes the block through its last byte.

## Tool

`python3 tools/lol1_loose.py --check`

```
CHECK loose: 25 files reach the last byte (3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 7 mz, 2 overlay, 1 text, 1 com); 12 open (6 blend tables, 3 symbol files, 3 LANDS tails)
```
