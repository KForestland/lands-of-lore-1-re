# Re-deriving a sample of confirmed statements

The two 19–20 November samples of 30 statements labelled confirmed were taken from the
current pages and checked again from the original bytes: the CD `DATA`
folder, the floppy folder, `MAIN.EXE` at raw file offsets disassembled as
16-bit code, and upstream ScummVM where the statement is about ScummVM.
No game, emulator or debugger was run, so a statement that rests on a
running-game observation is listed as not re-derived. Each list was
fixed before any statement on it was checked. The second sample shares no
statement with the first.

"Held" means the bytes give the same values as the page. "Part held"
means the checked part held and a broader part of the same statement
was not re-checked. "Wrong" and "Overstated" statements were corrected
on the page.

## First sample (19 November 2026)

Every third page, the first statement on it that names an address or
offset. 30 statements: **at most 27 held, 1 wrong (corrected), 2 not
re-derived.**

- Wrong: the floppy file catalog at `MAIN.EXE+0x2D060` has 1081 rows,
  not 375, and the `00000.VOC` rows are 11–225, not 222–225
  ([palette callers](unknowns/14_palette_callers.md)). Corrected.
- Not re-derived: the DOSBox session on the
  [running-game page](NEEDS_A_RUNNING_GAME.md) (its file facts hold), and
  a statement about ScummVM's C++ branch on the
  [YVEL2 page](unknowns/04_yvel2.md).
- The 27 are an upper bound. That check re-read some expected values
  from the pages instead of deriving them, which is how the wrong
  catalog count was first passed; a later independent re-check of six
  statements found it. 22 of the 27 were checked only once.

Pages: running game, CMZ, drivers, PAK, TLK, WLL, game rules, YVEL2,
native rules, `00000.VOC`, decoration positions, VCN colour banks,
cookbook, level assembly, status, executable tables, CPS, EMC2, loose
files, TIM, VCN/VMP, ADV/DRV/TBL, script exit, undefined walls, palette
callers, native save fields, open questions, round trip, tour and EMC2
scripts.

## Second sample (19–20 November 2026)

Every third page from a different starting page, the last statement on
it that names an address or offset. Statements from the first sample were
excluded. The list was fixed at 23:01 UTC; the first byte read was at
23:03. Line numbers are those of the pages when the list was fixed
(commit `354754d`). 30 statements: **20 held, 5 part held, 1 wrong and
2 overstated (all three corrected), 2 not re-derived.**

| # | Page (line at `354754d`) | Statement | Result | Evidence and limits |
| ---: | --- | --- | --- | --- |
| 1 | [Round trip](ROUND_TRIP.md), line 25 | Re-encoded bitmap header | Wrong, corrected: the writer recalculates the size word at +0x00 (CD `PARCH.CPS` 12,665 becomes 61,471) | The CD PARCH.CPS size word at +0x00 changes from 12,665 to 61,471. BEZEL.WSA also changes delta size at +0x0A, and KEEP.SHP changes its directory from +0x02. The page now identifies the regenerated size word. |
| 2 | [Tour](TOUR.md), line 35 | Level 1 monster calls | Held | LEVEL1.INI ORDR entry 1 is 0x009F. Words 0x0A and 0x7C hold 0x4E38 and 0x4E3F. DATA starts at +0x96, making word 0x7C file +0x18E, with the stored 200 and 90 arguments upstream. |
| 3 | [EMC2 scripts](emc2_scripts.md), line 286 | Exit call sites | Held | The three stated archive offsets begin with 0x4E7E. The two original script corpora contain one CD and two floppy calls to that slot. The emulator behavior was outside the test. |
| 4 | [Formats](formats/README.md), line 7 | Edition identification | Held | CD MAIN.EXE writes its revision string at file +0x32A41. Upstream detection_tables.h:56,58,1349,1716 identifies the CD and English floppy entries. |
| 5 | [Music](formats/music.md), line 50 | XMIDI field round trip | Held | A direct INFO tally from song +0x14 gives 620 CD and 808 floppy sequences. The writer reproduced all 51 CD and 57 floppy files, including the LORESFX.XMI INFO at +0x0C and CAT at +0x16. |
| 6 | [SHP](formats/shp.md), line 50 | Retail shape headers | Held | The check followed the table at inner SHP +0x02 on three files in each edition and read header words at shape +0x06 and +0x08 for first, middle and last rows. The upstream alt-header flag is scoped to the cited demo flags at detection_tables.h:63. |
| 7 | [TLC](formats/tlc.md), line 24 | Transparency palette approximation | Held | In expanded FXPAL.SHP, shape 0 +0x0B gives the 20 indices. All 29 first TLC tables agree. A new vectorized comparison scored 3,611 at 128 candidates and 3,391 at 255 candidates for weight 70. |
| 8 | [XXX](formats/xxx.md), line 28 | Legend ids | Held | Reading u16 +0x0A from each 12-byte record gives 71 with bit 0x4000 and two 0xFFFF in each edition. Maximum map coordinates are 31. |
| 9 | [Levels](levels/README.md), line 29 | Step and queued dispatch | Part held: the pushes; not every caller | CD +0xD785/+0xD792 then +0xD805/+0xD812 and floppy +0x10F0B/+0x10F18 then +0x10F8B/+0x10F98 push 4, 1, 8, 2. CD +0x10E53 and floppy +0x1575C push 2 for the queued block. The universal caller exclusion was outside these instruction windows. |
| 10 | [Save format](savegame_format.md), line 155 | Edited-save acceptance | Overstated, corrected: limited to the tested edits; the program windows read do not rule out every possible check | CD +0x48923–0x48AEC shows block reads and the snapshot loop. Those windows and one accepted edit do not exclude every possible checksum check. The page now limits the statement to the accepted edits. The run was not repeated. |
| 11 | [Tutorial](tutorial-one-event.md), line 47 | Tutorial wall action | Held | LEVEL4.INF ORDR 74 leads to DATA words 745–752, with sound 38 and the wall syscall with side -1, block 74, and wall 0. LEVEL4.CMZ gives 1,42,2,2 and L04.PAK+0xD738 starts wall 0. |
| 12 | [Level 24 CMZ](unknowns/03_level24_cmz.md), line 29 | Reference CMZ copy | Held | Upstream scene_lol.cpp:246–251 and saveload_rpg.cpp:50–60,74–84 read the stride at +4 and copy the first four bytes per block. The two retail LEVEL24.CMZ files have stride 9. |
| 13 | [TIM opcodes](unknowns/06_tim_opcodes.md), line 236 | TIM text byte order | Held | Floppy CHAPTER1.PAK+0xE7926 gives little-endian 6, 60 and 191. Floppy MAIN.EXE+0x96CC adds the word at the computed string-table index. |
| 14 | [PAK order](unknowns/09_pak_order.md), line 29 | ScummVM CD archive protection | Part held: the ScummVM flags; not the original program's search | Upstream detection_tables.h:56 and :58 set different talkie flags. That verifies the flag input to the protection test. The original executable search order was outside this ScummVM assertion. |
| 15 | [Legend bit](unknowns/12_legend_bit.md), line 48 | Legend string mask | Held | CD +0xC352/+0xC360/+0xC364 and floppy +0xFBAB/+0xFBB9/+0xFBBD compare 0xFFFF, mask with 0x3FFF and test 0x4000, respectively. The original XXX census covers the claimed stored values. |
| 16 | [ADL and C55](unknowns/15_adl_and_c55.md), line 85 | AdLib projection | Held | Floppy GENERAL.PAK+0xA6DE contains 0x81,0x41,0x22. Re-running the converter check produces 2,207/2,235 projections and 9/23 unavailable IDs, with one documented out-of-range repeat on floppy. |
| 17 | [Native records](unknowns/18_native_records.md), line 197 | Edited level 27 arrival | Not re-derived (running game) | The listed bytes at slot +0x255, +0x263 and +0x269 describe the edited inputs. Arrival is an observation in the original program, which this audit did not start. |
| 18 | [How the game works](HOW_THE_GAME_WORKS.md), line 63 | Experience thresholds and awards | Held | CD +0x2B830 and floppy +0x324F0 contain 0, 500, 1500 and 5000. The award code at CD +0x41203–0x41344 and floppy +0x4A38E–0x4A4C9 has the distinct skill branches and mage MP addition of 17. |
| 19 | [CMZ](formats/cmz.md), line 48 | Undefined map wall ids | Held | Walking CMZ block rows from expanded +0x06 and WLL IDs from +0x02 reproduces the omissions on levels 2, 3 and 21, plus level 29 on floppy. The conclusion concerns undefined rows in stored data. |
| 20 | [Game rules](game_rules.md), line 110 | Rest intervals | Part held: the three intervals; not the whole rest path | The CD +0x4E5F5 and floppy +0x572CA sequences load 600, divide and add one, compare 30 or 15, and shift the third result. The three intervals were checked. The complete eligibility and wake-up path was outside the instruction windows. |
| 21 | [SHP header](unknowns/01_shp_header.md), line 64 | Floppy `GUARD.SHP` | Held | The member is 24,987 bytes, expands to 32,751, and starts its table at +0x02 with 49 entries. Shapes 0, 24 and 48 resolve to inner offsets 206, 30122 and 32624. |
| 22 | [YVEL2](unknowns/04_yvel2.md), line 83 | Floppy `LEVEL22.INF` path | Held | ORDR entry 152 points at header word 8243. DATA starts at +0xA02, putting syscall 9 at file +0x4B0E. The stated comparisons, pushes and flag-setting syscall are present. |
| 23 | [Native rules](unknowns/07_native_rules.md), line 349 | Edited level 23 arrival | Not re-derived (running game) | Slot +0x269 change is a recorded input. Arrival and the resulting view require program execution, outside this audit. |
| 24 | [`00000.VOC`](unknowns/10_nnnnn_voc.md), line 41 | Repeated payload | Held | Hashing all members with that name finds 59 copies of one 44,115-byte payload. The CD catalog registration and the separate open playback question remain distinct. |
| 25 | [Decoration positions](unknowns/13_decoration_positions.md), line 45 | Cell tables | Held | The 18-word tables start at CD +0x32017 and floppy +0x37E29, followed by the shape-index tables at +0x3203B and +0x37E4D. Cell 16 contains the corresponding -254 delta and zero shape index. |
| 26 | [Running game](NEEDS_A_RUNNING_GAME.md), line 373 | Optional shutdown callback | Overstated, corrected: the search covers explicit operands only | Both original file cells are zero at CD +0x350EE and floppy +0x3DC4A. This is compatible with a later computed write. The page now describes the scope of the explicit-operand search. |
| 27 | [Executable tables](executable_tables.md), line 111 | Native definition bank | Part held: the 415 zero bytes; not a whole-image search | Both banks at CD +0x2D38E and floppy +0x34030 are 415 zero bytes. That statement was checked. A whole-image absence claim for every recorded argument representation would need its own comparison. |
| 28 | [Loose files](formats/loose.md), line 99 | Symbol table layout | Part held: the table walk and the coverage and segment bounds; not every cross-table index | The six ENG/FRE/GER blocks start their symbols at +0x50. Prefix totals from the record counts through the four module bytes per row land at the first name. Boundaries and zero local counts were checked, without revalidating every cross-table index. |
| 29 | [Palette](formats/palette.md), line 7 | Palette call arguments | Held | All six CD PAL members are 768 bytes. Script opcode 0x09 points at ALTPAL2 in level 2 word 0x31, ALTPAL1 in levels 3/24 words 0x69/0x0B, and CAV_PLT3 in level 25 word 0x49. |
| 30 | [WLL header](unknowns/02_wll_header.md), line 36 | CMZ leading words | Held | In all 58 expanded files, +0x00/+0x02 are 32/32. The stride at +0x04 yields 4,102 bytes or 9,222 for level 24 in each edition. The referenced reader consumes stride and walls. |

A review re-derived five of these from the bytes again (picked at random,
seed 145): the PAK order, decoration positions, shutdown callback,
symbol table and CMZ leading-word statements. All five gave the result above.

## Trust round 2 on 21 November 2026

Independent readers took ten randomly sampled proved table rows from each
game's pages and checked the original files with their own readers. Across
the three games, 30 of 30 rows held within the scope checked. The full
statement was checked in 29 rows. On one Lands of Lore III texture row,
the layout held and the palette-source clause was outside the check.

All ten sampled Lands of Lore rows held on release `6523a4d`.
The formats were checked against the CD, ENG and floppy files.

A separate set of deliberately wrong statements tested what readers and
checks could catch. [Check audit](CHECK_AUDIT.md#trust-round-2-on-21-november-2026)
