# LoL1 reverse-engineering status

**As of:** 2026-11-18. This page replaces the "~99.999%" figure in the README and the closure memo with what is actually documented, which tool reads it, and what was checked on the data. The closure memo (2026-03-20) stays in `docs/` as history.

**Columns**

- **Documented** — a page in [`formats/`](formats/README.md) (or the named doc) describes the layout with ScummVM citations.
- **Tool** — a reader in `tools/` that runs as shipped, has `--help`, and reads the original data (`--data` / `$LOL1_DATA`).
- **Checked on data** — the tool's `--check` (or the named test) parses every file of the kind in the corpus named. CD = reference corpus top-level `DATA/`; ENG = CD `DATA/ENG`; LS = LANDSoL.
- **Open** — what is not known yet, with the lane item that owns it.

Run every check at once: `python3 tools/check_all.py --data <DATA>`.

## File formats

| Format | Documented | Tool | Checked on data | Open |
|--------|-----------|------|-----------------|------|
| PAK container | [pak.md](formats/pak.md) | `pak_reader.py` | yes: CD 81 PAK / 1163 members, ENG 17/378, LS 15/1213 | which PAK wins for duplicate names |
| TLK speech (CD) | [tlk.md](formats/tlk.md) — memo corrected: PAK of VOC | `pak_reader.py`, `voc_reader.py` | yes: 30 files, 4912 VOC members | who plays the 59 `NNNNN.VOC` members |
| Frame4 / LCW | [lcw.md](formats/lcw.md) | `lol1lib.py` | yes: every CPS, CMZ, VCN, VMP in CD, ENG, LS decodes to its stated size | — |
| CPS | [cps.md](formats/cps.md) | `cps_reader.py` | yes: CD 85/85, ENG 60/60, LS 112/112 | — |
| SHP | [shp.md](formats/shp.md) | `shp_renderer.py` (does not run as shipped) | memo: 3492/3492 frames (old tool, not re-run) | header prefix per edition: Grok item 1 |
| WSA | [wsa.md](formats/wsa.md) | `wsa_all_frames_extract.py` (does not run as shipped) | header flags: CD 241 (219 flag 0, 22 flag 1); memo: 4480/4480 frames (not re-run) | — |
| VOC | [voc.md](formats/voc.md) | `voc_reader.py` | yes: CD 215 + 4912 in TLK, ENG 127, LS 277; only block type 1 | — |
| XMI / C55 / PCS | [music.md](formats/music.md) | `extract_music.py` (does not run as shipped) | containers: all `FORM…XDIR` (CD) | no decoder; meaning of "C55" |
| ADL | [music.md](formats/music.md) | — | first bytes only (CD 16) | layout not documented field by field |
| ENG / FRE / GER text | [text.md](formats/text.md) | `decode_dialogue.py` (does not run as shipped) | string counts: 2165 per language (CD) | — |
| CMZ level map | [cmz.md](formats/cmz.md) | `lol1lib.load_bitmap`; `cmz_analyzer.py` (does not run as shipped) | yes: 29/29, size = 6 + 1024 x len | header bytes 0-3 (`20 00 20 00` everywhere): Grok item 2; L24 9-byte blocks: Grok item 3 |
| WLL wall types | [wll.md](formats/wll.md) | `wll_parser.py` (does not run as shipped) | sizes: 29/29 (CD) | meaning of flag bits / special types: Sol item 8b |
| VCN / VMP | [vcn_vmp.md](formats/vcn_vmp.md) | `vcn_vmp_reader.py` | yes: 13/13 sets CD and LS; VMP = 330 + 431 x pages | when YVEL2 is loaded: Grok item 4 |
| XXX automap legend | [xxx.md](formats/xxx.md) | `xxx_reader.py` | yes: 29 files, 73 records, CD and LS | string-id bit 0x8000 |
| DAT decorations | [dat.md](formats/dat.md) | `dat_reader.py` | yes: 12/12 CD and LS, shape indexes inside the SHP | slot-to-scene-position order |
| TLC (CD) | [tlc.md](formats/tlc.md) — memo corrected: transparency tables | `tlc_reader.py` | yes: 29/29 CD; LS has none | — |
| PAL / COL | [palette.md](formats/palette.md) | `cps_reader.py --pal-from` | sizes: 11/11 = 768 (CD) | which level passes which `.PAL` (from Sol's script listings) |
| FNT | [fnt.md](formats/fnt.md) | `fnt_reader.py` | yes: CD 4, ENG 7, LS 9; LS FONT6P/9P/9PN have 128 glyphs | — |
| EMC2 scripts (INF/INI) | [emc2.md](formats/emc2.md); Sol's `docs/emc2_scripts.md` (branch `sol/lol1-unknowns-20261118`, f6d1469) | Sol's `tools/emc2_decompile.py` | yes: CD 60/60 and LS 60/60, 0 unknown opcodes/functions (Sol test; reviewed PASS by Opus, one text fix) | native effect of slot 0x7E; native handler bodies |
| TIM sequences | [tim.md](formats/tim.md) | `parse_tim.py` (does not run as shipped) | container: 139/139 `FORM…AVFS` (CD) | opcode table: Grok item 6 |
| ADV / DRV / TBL | [drivers.md](formats/drivers.md) | — | names and sizes only | Grok item 5 |

## Corpus coverage

| Corpus | Containers | Members | Covered by the memo's inventory |
|--------|-----------|---------|--------------------------------|
| CD `DATA/` | 81 PAK + 30 TLK | 1163 + 4912 | PAK members yes (1163); TLK members as "parsed" only |
| CD `DATA/ENG`, `FRE`, `GER` | 17 PAK each | 378 each | **no** — INTRO1-9, FINALE*, HISTORY, INTROVOC, language GENERAL/STARTUP, NEW6P/NEW8P/INTRO fonts |
| LANDSoL | 15 PAK | 1213 | compared in `docs/edition_comparison.md` |

The readers above have been run on all three. The JSON inventories in `data/` were made from CD `DATA/` only.

## Game rules and executable tables

All from Sol's items 8a-8c, not started in this branch.

| Topic | Documented | Tool | Checked on data | Open |
|-------|-----------|------|-----------------|------|
| Item types (285) and properties | partly: set by script function 0x0E `setItemProperty` (285 static call sites on CD, Sol's emc2 page) | Sol's decompiler | call count yes | full table: Sol 8a |
| Monster properties | partly: script function 0x3F `loadMonsterProperties` (79 calls) | Sol's decompiler | call count yes | full table: Sol 8a |
| Spells, characters, experience levels | — | — | — | Sol 8a |
| Combat (hit, damage, armour) | — | — | — | Sol 8b |
| Magic (cost, effect per level) | — | — | — | Sol 8b |
| Experience and skills | — | — | — | Sol 8b |
| Monster behaviour modes | — | — | — | Sol 8b |
| Light and time | — | — | — | Sol 8b |
| Save file | — | — | — | Sol 8c |

## Older tools in `tools/`

These come from the March workspace. They are kept, but as shipped they do not run against a fresh checkout:

| Tool | Problem |
|------|---------|
| `cmz_analyzer.py`, `level_renderer.py`, `tileset_mapper.py` | import `lol1_decompress_lcw` (not in the repo) |
| `shp_renderer.py`, `wsa_extract.py`, `wsa_all_frames_extract.py` | import `lol1_decode_frame4` (not in the repo; the code is `tools/decode_frame4.py`) |
| `decode_dialogue.py`, `decode_frame4.py`, `extract_dialogue.py`, `extract_music.py`, `parse_tim.py`, `wll_parser.py` | fixed paths under `/home/bob/…` (e.g. `/home/bob/lol1_pak_index.json`); fail without them |
| `pak_indexer.py`, `tlk_verify.py` | ignore `--help` and run at once, writing to `/home/bob/lol1_inventory_step1.json` and `/home/bob/lol2_out/lol1_tlk_verify/` |
| `tlk_verify.py` | its sample list pairs each TLK member name with the next member's offset |

Fixing them belongs to the GitHub cleanup after this order (the new readers already cover CPS, VOC, FNT, XXX, DAT, TLC, VCN/VMP, PAK/TLK).

## Corrections to the closure memo found in this pass

1. TLK is not "uint16 count + 8-byte entries"; CD TLK files are PAK archives of VOC samples ([tlk.md](formats/tlk.md)).
2. TLC is one 256-byte slot table plus twenty 256-byte blend rows for transparency, not "lighting/effect remaps" ([tlc.md](formats/tlc.md)).
3. VMP is 330 floor/ceiling words plus 431 words per wall page ([vcn_vmp.md](formats/vcn_vmp.md)); the "8bpp VCN" alternative in `level_tileset_map.md` does not occur in LoL1.
4. VOC "majority 11111 Hz": the effects use the 11025 Hz divisor class, CD speech 22050 Hz ([voc.md](formats/voc.md)).
5. "1163 files" covers only the CD top-level `DATA/` PAKs (see Corpus coverage).
6. SHP "2-byte prefix": ScummVM applies it only to the LoL demo; settled by Grok item 1 ([shp.md](formats/shp.md)).
7. The "bytes 0-3 unknown" header belongs to CMZ, not WLL ([cmz.md](formats/cmz.md)).
8. FNT "226 glyphs per font" holds for the CD; LANDSoL FONT6P/9P/9PN have 128 ([fnt.md](formats/fnt.md)).

## What "done" means here

A row is done when it has a page, a working reader, a passing check on both editions where they differ, and no open point. Today 5 of the 21 format rows meet that strictly (LCW, CPS, VOC, TLC, FNT). Six more have a page, a working reader and a passing check but one named open point (PAK, TLK, VCN/VMP, XXX, DAT, EMC2). The other ten wait on Grok items 1-6, on the older tools, or on music decoding. None of the game-rules rows is done yet.
