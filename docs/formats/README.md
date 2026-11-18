# LoL1 file formats, one page each

Split from [`../closure_memo.md`](../closure_memo.md) (2026-03-20, kept as history) on 2026-11-18.
Each page says what the file is, its layout, who reads it, how it was confirmed, the tool that reads it, and what is still open.

**Conventions**

- `CONFIRMED` = checked on the game data with the named tool (the `--check` line is quoted).
- `UNCONFIRMED` = taken from ScummVM code or an earlier note, not yet checked on the data.
- ScummVM citations are `engines/kyra/<file>:<line>` in the project's ScummVM checkout (fork of upstream, commit `3b4db303`, 2026-03-26). Line numbers may drift on newer upstream.
- Editions: **CD** = the reference corpus (`DATA/` and its `ENG/ FRE/ GER/` folders, talkie). **LANDSoL** = the second witness (chapter PAKs, floppy-style, English). Every page says which one was read.
- No game data is stored in this repository. Tools take `--data <DATA folder>` or `$LOL1_DATA`.

| Page | Files | Reader | State |
|------|-------|--------|-------|
| [pak.md](pak.md) | `*.PAK`, CD `NN.TLK` | `tools/pak_reader.py` | CONFIRMED |
| [tlk.md](tlk.md) | CD speech `00.TLK`-`29.TLK` | `tools/pak_reader.py`, `tools/voc_reader.py` | CONFIRMED (memo corrected) |
| [lcw.md](lcw.md) | Frame4 / LCW compression | `tools/lol1lib.py` | CONFIRMED |
| [cps.md](cps.md) | `*.CPS` | `tools/cps_reader.py` | CONFIRMED |
| [shp.md](shp.md) | `*.SHP` | `tools/shp_renderer.py` | header per edition OPEN (Grok item 1) |
| [wsa.md](wsa.md) | `*.WSA` | `tools/wsa_all_frames_extract.py` | header CONFIRMED |
| [voc.md](voc.md) | `*.VOC` (and TLK members) | `tools/voc_reader.py` | CONFIRMED |
| [music.md](music.md) | `*.XMI *.C55 *.ADL *.PCS` | `tools/extract_music.py` | containers only |
| [text.md](text.md) | `*.ENG *.FRE *.GER` | `tools/decode_dialogue.py` | CONFIRMED (counts) |
| [cmz.md](cmz.md) | `LEVELn.CMZ` | `tools/lol1lib.py`, `tools/cmz_analyzer.py` | bytes 0-3, L24 extra 5 bytes OPEN (Grok items 2, 3) |
| [wll.md](wll.md) | `LEVELn.WLL` | `tools/wll_parser.py` | CONFIRMED |
| [vcn_vmp.md](vcn_vmp.md) | `AREA.VCN`, `AREA.VMP` | `tools/vcn_vmp_reader.py` | CONFIRMED; YVEL2 use OPEN (Grok item 4) |
| [xxx.md](xxx.md) | `LEVELn.XXX` | `tools/xxx_reader.py` | CONFIRMED |
| [dat.md](dat.md) | `AREA.DAT` | `tools/dat_reader.py` | CONFIRMED |
| [tlc.md](tlc.md) | CD `LEVELnn.TLC` | `tools/tlc_reader.py` | CONFIRMED (memo corrected) |
| [palette.md](palette.md) | `*.PAL`, `*.COL` | `tools/cps_reader.py --pal-from` | CONFIRMED (sizes) |
| [fnt.md](fnt.md) | `*.FNT` | `tools/fnt_reader.py` | CONFIRMED |
| [emc2.md](emc2.md) | `LEVELn.INF`, `LEVELn.INI` | Sol item 7 | container CONFIRMED; tables OPEN (Sol item 7) |
| [tim.md](tim.md) | `*.TIM` | `tools/parse_tim.py` | container CONFIRMED; opcode table OPEN (Grok item 6) |
| [drivers.md](drivers.md) | `*.ADV *.DRV *.TBL` | — | OPEN (Grok item 5) |

Inventory note (CONFIRMED, `pak_reader.py --check`): the memo's "81 PAKs, 1163 entries" covers only the top level of the CD `DATA/` folder. The CD also has `DATA/ENG`, `DATA/FRE`, `DATA/GER`, each with 17 PAKs and 378 members (INTRO1-9, FINALE*, HISTORY, INTROVOC, a language GENERAL/STARTUP, NEW6P/NEW8P/INTRO fonts, .TXT, .DIP). `DATA/ENG/GENERAL.PAK` is not byte-identical to `DATA/GENERAL.PAK`. The 30 `NN.TLK` files hold another 4912 members. See [../STATUS.md](../STATUS.md).
