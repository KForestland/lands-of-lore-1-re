# LoL1 file formats, one page each

One page per file type of *Lands of Lore: The Throne of Chaos* (Westwood, 1993, DOS). Each page says what the file is, its layout, who reads it, how it was confirmed, the tool that reads it, and what is still open.

**Conventions**

- `CONFIRMED` = checked on the game data with the named tool (the tool's `--check` output is quoted).
- `UNCONFIRMED` = taken from ScummVM's code or an earlier note, not yet checked on the data.
- ScummVM citations are `engines/kyra/<file>:<line>` (or `audio/…`, `devtools/create_kyradat/…`) in upstream ScummVM at commit `3b4db303` (github.com/scummvm/scummvm, 2026-03-26). Names like `_vcnShift` or `_wllVmpMap` are ScummVM's variable names for the data, quoted so the reader can find them in that code.
- **Editions read:**
  - **CD** = the CD-ROM edition with spoken dialogue (its executable reports version `CD1.02`; ScummVM detects it as "Lands of Lore CD", English, `engines/kyra/detection_tables.h:1349`): the top-level `DATA/` folder plus its language folders `DATA/ENG`, `DATA/FRE`, `DATA/GER`. ScummVM calls this the "talkie" version.
  - **floppy** = an English floppy-edition installation (no speech; data in `CHAPTER1.PAK`-`CHAPTER8.PAK`, `GENERAL.PAK` etc.), named after the folder it was read from. ScummVM detects it as its English floppy entry labelled "Extracted" (`detection_tables.h:1716`). It serves as the second edition wherever the two can differ. See [`../edition_comparison.md`](../edition_comparison.md).
  - Every page says which one was read.
- File names: level files are `LEVELn.<ext>` without a leading zero for CMZ, WLL, XXX, INF, INI (`LEVEL1.CMZ`) and with two digits for TLC and the level text files (`LEVEL01.TLC`, `LEVEL01.ENG`); `Lnn.PAK` holds them.
- **Closure memo** = [`../closure_memo.md`](../closure_memo.md), a summary written in March 2026 when this work was first declared finished. It is kept as history; section letters (A, B.4, D.1 …) refer to its headings. These pages correct it where the data disagrees. "March 2026" tools and data files are the versions that memo describes.
- Open points are numbered in [`../OPEN_QUESTIONS.md`](../OPEN_QUESTIONS.md).
- No game data is stored in this repository. Tools take `--data <DATA folder>` or the `$LOL1_DATA` environment variable.

| Page | Files | Reader | State |
|------|-------|--------|-------|
| [pak.md](pak.md) | `*.PAK`, CD `NN.TLK` | `tools/pak_reader.py`, `tools/pak_indexer.py` | CONFIRMED; Q9 answered |
| [tlk.md](tlk.md) | CD speech `00.TLK`-`29.TLK` | `tools/tlk_verify.py`, `tools/voc_reader.py` | CONFIRMED (closure memo corrected); Q10 mostly answered |
| [lcw.md](lcw.md) | Frame4 / LCW compression | `tools/lol1lib.py`, `tools/decode_frame4.py` | CONFIRMED |
| [cps.md](cps.md) | `*.CPS` | `tools/cps_reader.py` | CONFIRMED |
| [shp.md](shp.md) | `*.SHP` | `tools/shp_renderer.py` | CONFIRMED on CD and floppy (closure memo corrected: no 2-byte prefix); demo unread (Q1) |
| [wsa.md](wsa.md) | `*.WSA` | `tools/wsa_extract.py` | CONFIRMED |
| [voc.md](voc.md) | `*.VOC` (and TLK members) | `tools/voc_reader.py` | CONFIRMED |
| [music.md](music.md) | `*.XMI *.C55 *.ADL *.PCS` | `tools/extract_music.py` | XMIDI converts to MIDI (`xmi_to_midi.py`); ADL layout documented (Q15 answered); `adl_to_midi.py` projects ADL tracks to a MIDI note timeline |
| [text.md](text.md) | `*.ENG *.FRE *.GER` | `tools/decode_dialogue.py` | CONFIRMED |
| [cmz.md](cmz.md) | `LEVELn.CMZ` | `tools/cmz_analyzer.py`, `tools/level_renderer.py` | CONFIRMED (Q2 answered); Q3 settled, Q11 answered |
| [wll.md](wll.md) | `LEVELn.WLL` | `tools/wll_parser.py` | CONFIRMED layout; meaning of flags Q7 |
| [vcn_vmp.md](vcn_vmp.md) | `AREA.VCN`, `AREA.VMP` | `tools/vcn_vmp_reader.py`, `tools/tileset_mapper.py` | CONFIRMED (Q4, Q16 answered) |
| [xxx.md](xxx.md) | `LEVELn.XXX` | `tools/xxx_reader.py` | CONFIRMED (Q12 answered) |
| [dat.md](dat.md) | `AREA.DAT` | `tools/dat_reader.py` | CONFIRMED (Q13 answered) |
| [tlc.md](tlc.md) | CD `LEVELnn.TLC` | `tools/tlc_reader.py` | CONFIRMED (closure memo corrected) |
| [palette.md](palette.md) | `*.PAL`, `*.COL` | `tools/cps_reader.py --pal-from` | CONFIRMED (sizes); Q14 partly answered |
| [fnt.md](fnt.md) | `*.FNT` | `tools/fnt_reader.py` | CONFIRMED |
| [emc2.md](emc2.md) | `LEVELn.INF`, `LEVELn.INI`, `ITEM.INF`, `ONETIME.INF` | `tools/emc2_decompile.py` | CONFIRMED (all 60 scripts, both editions) |
| [tim.md](tim.md) | `*.TIM` | `tools/parse_tim.py` | CONFIRMED: container and command use (Q6 answered) |
| [drivers.md](drivers.md) | `*.ADV *.DRV *.TBL` | `tools/decode_dialogue.py` (TRIG.TBL) | CONFIRMED: drivers identified (code, not documented inside); TRIG.TBL decoded (Q5 answered) |

How the game works (scripts, rules, saves): [`../emc2_scripts.md`](../emc2_scripts.md), [`../executable_tables.md`](../executable_tables.md), [`../game_rules.md`](../game_rules.md), [`../savegame_format.md`](../savegame_format.md). Answered questions in detail: [`../unknowns/`](../unknowns/).

Inventory note (CONFIRMED, `pak_reader.py --check`): the closure memo's "81 PAKs, 1163 entries" covers only the top level of the CD `DATA/` folder. The CD also has `DATA/ENG`, `DATA/FRE`, `DATA/GER`, each with 17 PAKs and 378 members (INTRO1-9, FINALE*, HISTORY, INTROVOC, a language GENERAL/STARTUP, NEW6P/NEW8P/INTRO fonts, .TXT, .DIP). `DATA/ENG/GENERAL.PAK` is not byte-identical to `DATA/GENERAL.PAK`. The 30 `NN.TLK` files hold another 4912 members.
