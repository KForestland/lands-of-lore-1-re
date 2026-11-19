# Q14 — Callers for three alternative VGA palettes

**CONFIRMED** All three names identify 768-byte palette members. Each floppy member is byte-identical to its CD counterpart. The CD copies sit in the relevant tileset PAK. floppy puts the three in `GENERAL.PAK`.

| Name | CD member | floppy member | floppy `MAIN.EXE` name and resource row |
| --- | --- | --- | --- |
| `CAV_PLT2.PAL` | `CAVE1.PAK+0x1D72C` | `GENERAL.PAK+0x5B2` | name `0x3A525`, on-disk row 227 at `0x2E21C` |
| `CAV_PLT4.PAL` | `CAVE1.PAK+0x1DD2C` | `GENERAL.PAK+0xBB2` | name `0x3A53F`, on-disk row 229 at `0x2E244` |
| `ALTPAL3.PAL` | `FOREST1.PAK+0x1B8B5` | `GENERAL.PAK+0x14B2` | name `0x3A564`, on-disk row 232 at `0x2E280` |

**CONFIRMED** The floppy `MAIN.EXE` names are registered resources. The 20-byte row begins with a relocated far pointer, followed by a four-byte length of `0x300`. A word at +0x12 contains `0x1000`. The native file lookup searches names in this table, then the generic open routine uses the returned row in the `0x1000` branch. floppy `MAIN.EXE+0x236D3–0x2383E` (name comparison and row lookup), `+0xB480–0xB4E9` (open routine), table base `+0x2D060`. This accounts for the relocations without a direct instruction pushing any of the three filename addresses. The table is a catalog of 1081 rows, ending at an all-zero row (byte +0x10 is the archive index, and the counts per index match each floppy PAK's member count; the 0x177 pushed at `+0x23768` is the offset half of the far pointer `0x1ECE:0x0177` to the sort comparator, not a row count): the VOC files sit in rows 11-225, and the palettes that are used (rows 228, 230, 231) have rows of exactly the same form. A row is therefore a registration, not evidence of a load.

**CONFIRMED** The CD keeps the same 20-byte rows in `FILEDATA.FDT`: rows 204, 206 and 122 (file offsets `0xFF0`, `0x1018`, `0x988`) give size `0x300`, the member offset inside the archive at +0x0C (`0x1D72C`, `0x1DD2C`, `0x1B8B5`) and flags `0x1000` at +0x12.

**CONFIRMED** On-disk row 227 starts `C5 2C 06 33 00 03 00 00`. The MZ header is `0x4800` bytes, so this pointer resolves to `0x4800 + 0x3306 × 16 + 0x2CC5 = 0x3A525`, the string `CAV_PLT2.PAL`. The `0x300` length matches the PAK member at `GENERAL.PAK+0x5B2`. The floppy `FINALE.EXE` contains the same three names at `0x235F9`, `0x23613` and `0x23638`.

## Palette loads observed

**CONFIRMED** Syscall `0x09` resolves argument 5 as a filename. The tileset loader reads 384 bytes from that file over the VCN's RGB palette region (CD `MAIN.EXE+0x474C3–0x475D2, +0x465EC–0x46622`; floppy `MAIN.EXE+0x50CA6–0x50DB5, +0x4FDAD–0x4FDE3`; upstream `engines/kyra/script/script_lol.cpp:208–212`, `engines/kyra/engine/scene_lol.cpp:358–367`). The following script TEXT names provide positive controls in both editions.

| Script | Palette | CD TEXT location | floppy TEXT location |
| --- | --- | --- | --- |
| `LEVEL2.INI` | `ALTPAL2.PAL` | `L02.PAK+0x10DB5` | `CHAPTER1.PAK+0x61CA1` |
| `LEVEL3.INI` | `ALTPAL1.PAL` | `L03.PAK+0x5458` | `CHAPTER1.PAK+0x621E7` |
| `LEVEL24.INI` | `ALTPAL1.PAL` | `L24.PAK+0xD86C` | `CHAPTER6.PAK+0x6F32B` |
| `LEVEL25.INI` | `CAV_PLT3.PAL` | `L25.PAK+0xB86` | `CHAPTER6.PAK+0x6F6A5` |

**CONFIRMED** The first 384 bytes of each of the three questioned palettes differ from the embedded CAVE1 or FOREST1 VCN palette and the sibling PAL files. For example, the first half of `ALTPAL3.PAL` shares 372 of 384 bytes with the FOREST1 VCN palette and differs from the first halves of `ALTPAL1.PAL` and `ALTPAL2.PAL`. The three ALTPAL files have identical second halves (CD `FOREST1.PAK+0x1B2B5, +0x1B5B5, +0x1B8B5`; floppy `GENERAL.PAK+0xEB2, +0x11B2, +0x14B2`).

## Remaining question

**CONFIRMED** No multiply-by-20 site loads the three row numbers as a constant. The site form searched is `BA 14 00 F7 EA` (a word multiplied by `0x14`). On the CD the row numbers are 122, 204 and 206 of `FILEDATA.FDT` (`ALTPAL3.PAL`, `CAV_PLT2.PAL`, `CAV_PLT4.PAL`); on the floppy they are on-disk rows 227, 229 and 232. None of those words sits in the six bytes before such a multiply, in `HARDRIVE/MAIN.EXE` or in floppy `MAIN.EXE`. `lol1_mode_paths.py --check` re-reads the three `FILEDATA.FDT` rows and the three on-disk rows, and that absence. This rules out only a literal index in that one form: an index can be computed, the floppy lookup sorts its table at run time (`0x2377E`, below), so an on-disk row number need not be the index used, and the generic name lookup can reach a row when a caller supplies the name. It is not evidence that no code reaches the rows.

**UNCONFIRMED** No specific gameplay caller of the three resource rows was identified. The check searched exact and prefix names in the 60 EMC2 scripts of each edition and the 139 CD and 147 floppy TIM members. It found the four EMC2 controls above and no occurrence of the three names in question. The CD executables checked have no corresponding name strings. The check also read `INSTALL.EXE` (134819 bytes, beside `DATA`), `DATA/HARDRIVE/SETUP.EXE` (103188 bytes), `LOLCD.EXE`, `MAINW.EXE`, and the English, French and German `LANDS.EXE` and `FINALE.EXE`: none contains the three names. Archive payloads do not contain them either. The names that do occur in script text, `ALTPAL1.PAL`, `ALTPAL2.PAL` and `CAV_PLT3.PAL`, are the four controls in the table above. In floppy the direct near-address search returned only the relocated descriptor pointers for the three names and an incidental byte match for the ALTPAL3 offset. The generic lookup and open paths above take a filename at runtime. A computed filename could reach them. The lookup prepares and searches a runtime table, including a sort step at `0x2377E`, so the file row positions serve as byte anchors. A trace of floppy's open routine at `0xB442` should filter by the incoming filename and capture the caller address and requested read length. The tool's search uses the exact upper-case names in raw archive payloads, the programs under `DATA` and `INSTALL.EXE` (CD edition). A wider review search (case variants, stems and fragments, UTF-16, Frame4-decompressed members, the installer bundle `WESTWOOD.001`, the demo programs and every other loose file) found nothing more. `lol1_name_callers.py --check` re-reads the catalog strings, the empty program and installer search, and the three script controls.

## Close-out

**What was measured.** The member-offset dwords of the three palettes are `2C D7 01 00`, `2C DD 01 00` and `B5 B8 01 00`, read at `FILEDATA.FDT` `+0xFFC`, `+0x1024` and `+0x994`. Each of those three sequences occurs once in `FILEDATA.FDT` and zero times in `HARDRIVE/MAIN.EXE`, `MAINW.EXE`, `LOLCD.EXE`, `SETUP.EXE`, the English, French and German `LANDS.EXE` and `FINALE.EXE`, and `INSTALL.EXE`.

**What was tried.** The scan searched those four-byte archive offsets in the programs and the installer. The page already searched the palette names in scripts, TIM members, those programs and `INSTALL.EXE`.

**What would settle it.** A running-game trace that logs the incoming filename at the floppy open routine `+0xB442` and stops on the three names gives the caller and the requested read length; on the CD, break on the DOS open and seek calls as the probe describes. The running-game test is not yet run ([probes not yet run](../NEEDS_A_RUNNING_GAME.md#probes-not-yet-run)).
