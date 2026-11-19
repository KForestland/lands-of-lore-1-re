# Re-deriving a sample of confirmed statements

Two samples of 30 statements labelled confirmed were taken from the
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
23:03. 30 statements: **20 held, 5 part held, 1 wrong and 2 overstated
(all three corrected), 2 not re-derived.**

| Page | Statement | Result |
| --- | --- | --- |
| [Round trip](ROUND_TRIP.md) | Re-encoded bitmap header | Wrong, corrected: the writer recalculates the size word at +0x00 (CD `PARCH.CPS` 12,665 becomes 61,471) |
| [Tour](TOUR.md) | Level 1 monster calls | Held |
| [EMC2 scripts](emc2_scripts.md) | Exit call sites | Held |
| [Formats](formats/README.md) | Edition identification | Held |
| [Music](formats/music.md) | XMIDI field round trip | Held |
| [SHP](formats/shp.md) | Retail shape headers | Held |
| [TLC](formats/tlc.md) | Transparency palette approximation | Held |
| [XXX](formats/xxx.md) | Legend ids | Held |
| [Levels](levels/README.md) | Step and queued dispatch | Part held: the pushes; not every caller |
| [Save format](savegame_format.md) | Edited-save acceptance | Overstated, corrected: limited to the tested edits; the program windows read do not rule out every possible check |
| [Tutorial](tutorial-one-event.md) | Tutorial wall action | Held |
| [Level 24 CMZ](unknowns/03_level24_cmz.md) | Reference CMZ copy | Held |
| [TIM opcodes](unknowns/06_tim_opcodes.md) | TIM text byte order | Held |
| [PAK order](unknowns/09_pak_order.md) | ScummVM CD archive protection | Part held: the ScummVM flags; not the original program's search |
| [Legend bit](unknowns/12_legend_bit.md) | Legend string mask | Held |
| [ADL and C55](unknowns/15_adl_and_c55.md) | AdLib projection | Held |
| [Native records](unknowns/18_native_records.md) | Edited level 27 arrival | Not re-derived (running game) |
| [How the game works](HOW_THE_GAME_WORKS.md) | Experience thresholds and awards | Held |
| [CMZ](formats/cmz.md) | Undefined map wall ids | Held |
| [Game rules](game_rules.md) | Rest intervals | Part held: the three intervals; not the whole rest path |
| [SHP header](unknowns/01_shp_header.md) | Floppy `GUARD.SHP` | Held |
| [YVEL2](unknowns/04_yvel2.md) | Floppy `LEVEL22.INF` path | Held |
| [Native rules](unknowns/07_native_rules.md) | Edited level 23 arrival | Not re-derived (running game) |
| [`00000.VOC`](unknowns/10_nnnnn_voc.md) | Repeated payload | Held |
| [Decoration positions](unknowns/13_decoration_positions.md) | Cell tables | Held |
| [Running game](NEEDS_A_RUNNING_GAME.md) | Optional shutdown callback | Overstated, corrected: the search covers explicit operands only |
| [Executable tables](executable_tables.md) | Native definition bank | Part held: the 415 zero bytes; not a whole-image search |
| [Loose files](formats/loose.md) | Symbol table layout | Part held: the table walk and the coverage and segment bounds; not every cross-table index |
| [Palette](formats/palette.md) | Palette call arguments | Held |
| [WLL header](unknowns/02_wll_header.md) | CMZ leading words | Held |

A review re-derived five of these from the bytes again (picked at random,
seed 145): the PAK order, decoration positions, shutdown callback,
symbol table and CMZ leading-word statements. All five gave the result above.
