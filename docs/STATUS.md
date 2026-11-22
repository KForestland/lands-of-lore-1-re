# LoL1 reverse-engineering status

## Where this stands

- **Nearly done, with open questions.** Tools read the layout of [199 of 199 files in the English CD DATA folder](../README.md#rating).
- One of the six listed running-game tests is answered. The [shutdown trace](NEEDS_A_RUNNING_GAME.md#q8-which-shutdown-callbacks-run-on-a-given-installation) records a quit from play on the English CD with Sound Blaster. In separate CD trials, a [moved Halberd appeared and was picked up](LEVEL_EDITOR.md#keep-placement-in-the-original-game), and the [spelling patch showed two corrected item names](../patches/README.md#shipped-patch) using an edited save.
- Six of [18 numbered questions](OPEN_QUESTIONS.md#at-a-glance) still have open parts, including demo shapes, monster modes and which save fields are touched in play.
- The [rating](HOW_WE_RATE.md) keeps separate counts for files, rules and tests in play. An overall percentage would combine measures of different things.

<!-- suite-counts:begin -->
- **Original game files.** 54 checks with the required files and dependencies. Quick mode selects 52.
- **Synthetic data.** 133 unit tests.
<!-- suite-counts:end -->

**As of:** 2026-11-21. For every file format and rules topic: what is documented, which tool reads it, what was checked on the game data, and what is still open. Older notes kept as history ([`closure_memo.md`](closure_memo.md)) gave a single percentage; this table replaces it.

**Columns**

- **Documented**: a page in [`formats/`](formats/README.md) (or the named doc) describes the layout with ScummVM citations.
- **Tool**: a reader in `tools/` with `--help`, reading the original data through `--data <DATA folder>` or `$LOL1_DATA`.
- **Checked on data**: the tool's `--check` parses every file of that kind. CD = the top-level `DATA/` folder of the CD-ROM edition with spoken dialogue (version CD1.02); ENG = its `DATA/ENG` folder; floppy = an English floppy-edition installation (no speech, chapter-based PAKs). Details: [formats/README.md](formats/README.md).
- **Open**: what is not known yet, as numbered in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

Run every check at once: `python3 tools/check_all.py --data <DATA>` (all pass on the CD and on the floppy edition, about 102 seconds on the CD and 59 on the floppy, most of it the picture re-encoding check and the progression walk). The experience, spell cost, item and creature numbers are in [numbers at a glance](NUMBERS.md), generated and checked by `tools/lol1_numbers.py`.

**Rating** (counted by `tools/rating.py` on the CD edition; see [how we rate](HOW_WE_RATE.md)):

<!-- rating:begin -->
- **Files read:** 199 of 199 files in the CD `DATA` folder (289.0 of 289.0 MiB) have their whole layout read by a tool here: every byte belongs to a known header, directory or entry (what is inside an entry may still be only partly understood).
- **Rules traced:** the pages mark 574 statements CONFIRMED (labelled as proved with a cited address or offset) and 101 UNCONFIRMED (a reading not yet proved), on 108 current pages; old notes kept as history are not counted.
- **Seen in the running game:** 1 of 6 probes that need the original game running are answered (a question can have more than one probe); 0 of them rest on edited saves only.
- **Open questions:** 18 numbered questions: 12 answered, 4 mostly answered, 2 partly answered.
- **Page facts:** 24/6,881 candidate literals registered with byte witnesses. The rest are inventoried so changes can be reviewed.
<!-- rating:end -->

## File formats

**Running-game results.** Answered probes are counted in the rating; which ones and how: [NEEDS_A_RUNNING_GAME](NEEDS_A_RUNNING_GAME.md#answered-probes). Runs on hand-edited copies of a game-written save: [edited saves](EDITED_SAVES.md).

| Format | Documented | Tool | Checked on data | Open |
|--------|-----------|------|-----------------|------|
| PAK container | [pak.md](formats/pak.md) | `pak_reader.py`, `pak_indexer.py` | CD 81 PAK / 1163 members (rebuilds `data/pak_index.json`), ENG 17/378, floppy 15/1213 | Q9 answered ([page](unknowns/09_pak_order.md)) |
| TLK speech (CD) | [tlk.md](formats/tlk.md) | `tlk_verify.py`, `pak_reader.py`, `voc_reader.py`, `lol1_name_callers.py` | 30 files, 4912 VOC members; names follow the engine's speech patterns. The finale catalog row for `00000.VOC` is row 40 of 93 in the file, 44115 bytes; every catalog index is computed, none is the constant 40, and startup sorts rows 4 to 92 by name | Q10 mostly answered: one padding clip ([page](unknowns/10_nnnnn_voc.md)) |
| Frame4 / LCW | [lcw.md](formats/lcw.md) | `lol1lib.py`, `decode_frame4.py` | two independent ports agree on 140/140 CD files; every CPS/CMZ/VCN/VMP in CD, ENG, floppy decodes to its stated size | — |
| CPS | [cps.md](formats/cps.md) | `cps_reader.py` | CD 85/85, ENG 60/60, floppy 112/112 | — |
| SHP | [shp.md](formats/shp.md) | `shp_renderer.py` | strict decode CD 3492/3492, ENG 1269/1269, floppy 3601/3601; retail negative control with the extra two-byte prefix gives 0 valid shapes | Q1 (demo only) |
| WSA | [wsa.md](formats/wsa.md) | `wsa_extract.py`, `wsa_all_frames_extract.py` | CD 4480/4480 frames, ENG 2699/2699, floppy 5227/5227 | — |
| VOC | [voc.md](formats/voc.md) | `voc_reader.py` | CD 215 + 4912 in TLK, ENG 127, floppy 277 | — |
| XMI / C55 / PCS | [music.md](formats/music.md) | `extract_music.py` | IFF trees of all 51 IFF files among the 67 CD music files (rebuilds `data/music_inventory.json`); `xmi_to_midi.py` converts all 620 XMIDI sequences to MIDI | Q15 (what C55 stands for) |
| ADL | [music.md](formats/music.md), [Q15](unknowns/15_adl_and_c55.md) | `adl_to_midi.py` | both original track-map widths and a four-second MIDI projection of all usable entry programs in 16 CD and 18 floppy assets | native sound effects and timbre |
| ENG / FRE / GER text | [text.md](formats/text.md) | `decode_dialogue.py`, `extract_dialogue.py` | 90 files, 6495 strings, all bigram bytes in range (CD) | — |
| CMZ level map | [cmz.md](formats/cmz.md) | `cmz_analyzer.py`, `level_renderer.py` | 29/29, size = 6 + 1024 x len (rebuilds the corrected `data/wall_type_analysis.json`) | Q3 answered, Q11 answered ([page](unknowns/11_undefined_walls.md)) |
| WLL wall types | [wll.md](formats/wll.md) | `wll_parser.py` | 29/29, 1726 records (rebuilds `data/wll_parsed.json`) | Q7 mostly answered: wall bit 0x40 needs a runtime trace ([page](unknowns/07_native_rules.md)) |
| VCN / VMP | [vcn_vmp.md](formats/vcn_vmp.md) | `vcn_vmp_reader.py`, `tileset_mapper.py` | 13/13 sets CD and floppy; 35 `loadLevelGraphics` calls mapped | Q16 answered ([page](unknowns/16_vcn_colour_banks.md)) |
| XXX automap legend | [xxx.md](formats/xxx.md) | `xxx_reader.py` | 29 files, 73 records, CD and floppy | Q12 answered ([page](unknowns/12_legend_bit.md)) |
| DAT decorations | [dat.md](formats/dat.md) | `dat_reader.py` | 12/12 CD and floppy | Q13 answered ([page](unknowns/13_decoration_positions.md)) |
| TLC (CD) | [tlc.md](formats/tlc.md) | `tlc_reader.py` | 29/29 CD; floppy has none | — |
| PAL / COL | [palette.md](formats/palette.md) | `cps_reader.py --pal-from`, `lol1_name_callers.py` | 11/11 are 768 bytes (CD); level use of 3 PALs by script scan. The three unused names are absent from programs, payloads and the installer. No stride-20 index site loads their row numbers as a constant | Q14 partly answered: catalogued, no caller found ([page](unknowns/14_palette_callers.md)) |
| FNT | [fnt.md](formats/fnt.md) | `fnt_reader.py` | CD 4, ENG 7, floppy 9 | — |
| EMC2 scripts (INF/INI) | [emc2.md](formats/emc2.md), [emc2_scripts.md](emc2_scripts.md) | `emc2_decompile.py`, `tests/test_emc2_corpus.py` | CD 60/60, floppy 60/60, 0 unknown opcodes or functions; native table and handler reads checked for all 192 CD and 187 floppy slots | Q8 answered ([page](unknowns/08_native_script_exit.md)); 71 [partial verdicts](emc2_native_handlers.md#open-parts-of-the-comparison), including cases where the wrapper is known and the downstream effect remains open |
| TIM sequences | [tim.md](formats/tim.md) | `parse_tim.py`, `lol1_tim_words.py` | 139/139 `FORM…AVFS`; command use counted by two independent walkers. The 14 extra CD words and the four floppy `%d` words are re-read by `lol1_tim_words.py` | Q6 answered ([page](unknowns/06_tim_opcodes.md)) |
| ADV / DRV / TBL | [drivers.md](formats/drivers.md) | `decode_dialogue.py` (TRIG.TBL), `lol1_driver_tables.py` | drivers identified (Miles Sound System code). Entry tables of every `.ADV`: CD 150, the CD `ENG/FRE/GER` copy 146, floppy 146; `ALFX.DRV` dispatch: 24 CD and 18 floppy wrappers. TRIG.TBL prompt text decoded. The native call that opens it remains open | the game meaning of each `.ADV` ID and `.DRV` body; the routine bodies are not read |

## Level sheets

[`levels/`](levels/README.md) has one sheet per level, written by `tools/level_report.py` from the level's own files: 1475 script entries described, 241 item and 522 monster placements found through constant script arguments (including one level of subroutine calls), 659 text ids. Arguments computed while the game runs are shown as `?`; event bits 1 and 4 of a script entry run before a party step is drawn and bits 2 and 8 after it, CONFIRMED in the DOS step routine ([event bits](levels/README.md#events)). Level changes and door calls from those scripts are one row per static call on the [progression](PROGRESSION.md) page.

## Corpus coverage

| Corpus | Containers | Members | In the closure memo's inventory |
|--------|-----------|---------|------------------------|
| CD `DATA/` | 81 PAK + 30 TLK | 1163 + 4912 | PAK members yes (1163); TLK only as "parsed" |
| CD `DATA/ENG`, `FRE`, `GER` | 17 PAK each | 378 each | **no**: INTRO1-9, FINALE*, HISTORY, INTROVOC, language GENERAL/STARTUP, NEW6P/NEW8P/INTRO fonts |
| floppy | 15 PAK + `MAIN.EXE` + four `_LEVELn.TMP` level-state files the original game wrote while that copy was played (not shipped; a fresh install has none) | 1213 | compared in `docs/edition_comparison.md` |

The readers have been run on all three. The JSON files in `data/` describe CD `DATA/` only.

## Game rules and executable tables

Pages: [executable_tables.md](executable_tables.md), [savegame_format.md](savegame_format.md), [game_rules.md](game_rules.md). Their content was re-checked against the data independently.

| Topic | Documented | Checked on data | Open |
|-------|-----------|-----------------|------|
| Where the executables are | [executable_tables.md](executable_tables.md) | CD: inside `WESTWOOD.001` (the CD's install archive) and loose in `DATA/HARDRIVE` (`MAIN.EXE`, `MAINW.EXE`), byte-identical; floppy `MAIN.EXE` | — |
| Spells (17 x 28 bytes), experience thresholds, character defaults (9 x 130), difficulty modifiers, CD price table | [executable_tables.md](executable_tables.md) | offsets in all three executables, values equal ScummVM's tables | native meaning of a few fields |
| Item types (285) and monster properties (79 script calls) | [executable_tables.md](executable_tables.md), [emc2.md](formats/emc2.md) | supplied by scripts in both editions; 4 item rows differ between editions; native record layouts traced ([Q18](unknowns/18_native_records.md)) | a few field roles (Q18) |
| Save file (original `_SAVEnnn.DAT`, level-state `_LEVELn.TMP`, ScummVM saves) | [savegame_format.md](savegame_format.md); reader `tools/save_reader.py` | save-name and version strings and section sizes in both executables; 4 floppy `_LEVELn.TMP` files written by the game in one played installation; 11 ScummVM saves made for this check end where the layout predicts (not shipped; `save_reader.py --check --saves DIR` checks yours); skipped native fields traced in both executables ([Q17](unknowns/17_native_save_fields.md)) | three single bytes (Q17); the game-written CD `_SAVE000.DAT` slots were watched through save and load, and edited copies were loaded ([edited saves](EDITED_SAVES.md)) |
| Combat, magic, experience and skills, monster behaviour, light, time | [game_rules.md](game_rules.md) | in both executables (disassembled): dice and random generator, armour reduction; per the page also hit test, damage categories, experience awards; data: spell damage tables, experience thresholds, monster mode flags. Spell casting and effects, lamp oil, regeneration and the 12 timers, monster transitions and WLL flags: traced in both executables ([Q7](unknowns/07_native_rules.md)) | Q7: WLL wall bit 0x40 (static collision masks traced to 0/1/2/7; needs a runtime trace). The instance mode byte has ten CD and eight floppy direct stores; none stores 10, and whether anything produces mode 10 stays open (the clock is CONFIRMED at 60 ticks per second) |

## Tools

All tools in `tools/` run from a fresh checkout. Each has `--help`, needs `--data` or `$LOL1_DATA`, writes nothing unless given an output option (`--out`, `--out-dir`, `--png`, `--wav`; `emc2_decompile.py` uses `-o`/`--output`), and has a `--check`, except `emc2_decompile.py`, which `tests/test_emc2_corpus.py` checks on every script; `tools/check_all.py` runs the configured checks.

## Corrections to the closure memo

The statements of the old closure memo that were later corrected are listed in [the memo itself](closure_memo.md#later-corrections).

## What "done" means here

A row is done when it has a page, a working reader, a passing check on both editions where they differ, and no open point. On 21 November 2026, 13 of the 21 format rows met that: LCW, CPS, WSA, VOC, TLC, FNT, text, PAK, CMZ, VCN/VMP, XXX, DAT, TIM. Five more have a page, a reader and a passing check but one or more open points: TLK (why the padding clip is there), SHP (demo edition unread), WLL, EMC2 (some downstream effects), ADV/DRV/TBL (what each driver entry does). PAL/COL is only partly documented (Q14). XMI/C55/PCS and ADL have a page, readers and a check; open: what "C55" stands for, and timbre details (Q15). All five rules and tables rows are documented. Four are checked against the data; the game-rules row is checked in the original program for its core combat arithmetic, and the rest of it is now traced in both executables too ([Q7](unknowns/07_native_rules.md)); a few details stay open.

"Checked independently" in this page means a second program, written separately from the one that produced the claim, gave the same result on the same files (for example two separate Frame4 decoders, or two separate TIM walkers).
