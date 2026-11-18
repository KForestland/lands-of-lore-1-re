# Open questions

Numbered so the format pages and [`STATUS.md`](STATUS.md) can point at them. Each is something not yet known about the original game files or rules. When one is answered, its page is updated and the entry says so. Each question links its detailed note in [unknowns/](unknowns).

## At a glance

One line per question: its state and what would settle what is left. Details are in the table below.

| ID | State | What would settle the rest |
|---|---|---|
| Q1 | Partly | Read the SHP files of the demo release; CD and floppy are answered |
| Q2 | Answered | — |
| Q3 | Answered for the game | The game never reads the 5 extra bytes; what the level author stored there would need the original editor |
| Q4 | Answered | — |
| Q5 | Answered | — |
| Q6 | Mostly | The extra argument words in a few calls and how the intro picks its table; 0x07 and nested 0x02 are native return-1 stubs in both editions |
| Q7 | Mostly | Trace the users of WLL wall bit 0x40 and the remaining monster mode branches |
| Q8 | Answered | Which optional sound/video shutdown callbacks run depends on the setup; run it on a chosen setup to list them |
| Q9 | Answered | — |
| Q10 | Mostly | Find any caller of the `00000.VOC` name (only `FINALE.EXE` lists it) |
| Q11 | Answered | Which earlier level supplies the row depends on the play order of a given game |
| Q12 | Answered | — |
| Q13 | Answered | — |
| Q14 | Partly | Find a caller of the three palettes; none is in scripts, TIM files or code read so far |
| Q15 | Answered | What the letters "C55" stand for is not in the files |
| Q16 | Answered | — |
| Q17 | Mostly | Three single bytes; read an original `_SAVEnnn.DAT` written by the DOS game |
| Q18 | Mostly | Trace who writes the monster critical-skill byte (zero in the image; no writer found) and the roles of a few monster modifiers |

## Questions

| ID | Question | Page |
|----|----------|------|
| Q1 | SHP shape header in every edition. **Answered for CD and floppy** (10-byte header, byte dumps match; 2026-11-18). Still open: the demo release, which was not read | [formats/shp.md](formats/shp.md) |
| Q2 | CMZ header bytes 0-3. **Answered:** `20 00 20 00` on all 29 levels of both editions, read by no engine code found. Calling them width and height (32 x 32) is a reading of the values, not of code | [formats/cmz.md](formats/cmz.md) |
| Q3 | Level 24's CMZ has 9 bytes per block instead of 4: what the extra 5 bytes hold, and why only this level. **Settled as far as the program goes:** both editions' `MAIN.EXE` copy 4 bytes per block and step over the rest, so the game never reads the tail ([unknowns/03_level24_cmz.md](unknowns/03_level24_cmz.md)). What the level's author stored there is still open | [formats/cmz.md](formats/cmz.md) |
| Q4 | When the level 22 scripts switch between YVEL1 and YVEL2. **Answered:** a click in a screen rectangle while block 145's north wall is type 8 loads YVEL2 and sets game flag 357; `LEVEL22.INI` reloads YVEL2 when flag 357 is set; another script path loads YVEL1 and clears the flag. Decorations stay YVEL1 | [formats/vcn_vmp.md](formats/vcn_vmp.md), [unknowns/04_yvel2.md](unknowns/04_yvel2.md) |
| Q5 | The `.ADV`, `.DRV` and `.TBL` files. **Answered:** 7 Miles Design sound drivers (code), named by `LANDS.EXE`, `MAIN.EXE`, `FINALE.EXE`; `TRIG.TBL` is the copy-protection prompt string table | [formats/drivers.md](formats/drivers.md) |
| Q6 | The full TIM opcode table. **Answered** for the 139 CD scripts and the floppy intro/outro; the commands ScummVM leaves unimplemented (0x07 in game, nested 0x02) are native return-1 stubs in both editions ([unknowns/06](unknowns/06_tim_opcodes.md)); open: extra argument words in a few calls and the intro table selection | [formats/tim.md](formats/tim.md) |
| Q7 | Game rules as formulas. **Mostly answered** ([game_rules.md](game_rules.md), [unknowns/07_native_rules.md](unknowns/07_native_rules.md)): combat arithmetic, spell dispatch (Vortex has no effect in either edition), the 12 timers with their periods, regeneration, lamp oil, monster mode flags and the WLL dispatch are traced in both executables. Open: WLL wall bit 0x40, some monster mode details (the clock is CONFIRMED at 60 ticks per second) | [game_rules.md](game_rules.md) |
| Q8 | What script function 0x7E did. **Answered** ([unknowns/08_native_script_exit.md](unknowns/08_native_script_exit.md)): it exits the game to DOS (shutdown preparation, then INT 21h AH=4Ch with status 0); called from level 2's script. Open only: which optional sound/video shutdown callbacks run on a given setup | [formats/emc2.md](formats/emc2.md) |
| Q9 | Which PAK wins when two PAKs hold the same member name. **Answered** ([unknowns/09_pak_order.md](unknowns/09_pak_order.md)): a loose file beats every PAK; an earlier-loaded archive beats a later one; inside one archive the later entry wins. The 81 game archives share no member names; only the prologue archives collide. | [formats/pak.md](formats/pak.md) |
| Q10 | Who plays the 59 `NNNNN.VOC` members of the CD speech files. **Mostly answered** ([unknowns/10_nnnnn_voc.md](unknowns/10_nnnnn_voc.md)): all 59 are one identical `00000.VOC` clip, the first and last entry of each TLK; no script or speech builder asks for it; the name appears only in a list in `FINALE.EXE`. | [formats/tlk.md](formats/tlk.md) |
| Q11 | Wall types used in the CMZ of levels 2, 3 and 21 (and, on the floppy, 29) that the level's WLL does not define. **Answered** ([unknowns/11_undefined_walls.md](unknowns/11_undefined_walls.md)): the wall loader does not clear the property tables, so such a type keeps the row of the last level that defined it; which order a game loads stays open. | [formats/cmz.md](formats/cmz.md) |
| Q12 | Bit 0x8000 in automap legend string ids. **Answered** ([unknowns/12_legend_bit.md](unknowns/12_legend_bit.md)): the bit is clear in every record of both editions and the drawer ignores it. | [formats/xxx.md](formats/xxx.md) |
| Q13 | Order of the ten decoration slots (which scene position each slot is). **Answered** ([unknowns/13_decoration_positions.md](unknowns/13_decoration_positions.md)): native draw loop, slot tables and mirroring traced in both executables; cell table included. | [formats/dat.md](formats/dat.md) |
| Q14 | Who loads CAV_PLT2.PAL, CAV_PLT4.PAL and ALTPAL3.PAL. **Partly answered** ([unknowns/14_palette_callers.md](unknowns/14_palette_callers.md)): all three are registered in the file catalogs (floppy table, CD `FILEDATA.FDT`) like every other file; no caller found in scripts, TIM files or code. | [formats/palette.md](formats/palette.md) |
| Q15 | Music. **Answered** ([unknowns/15_adl_and_c55.md](unknowns/15_adl_and_c55.md)): the ADL layout field by field (track map, program and instrument tables, bytecode, 11-byte instruments); C55 is the XMIDI set for General MIDI / Roland GS, chosen by the executable's sound selector. Open: what the letters "C55" stand for | [formats/music.md](formats/music.md) |
| Q16 | What decides the 16-colour bank (shift value) of each wall tile. **Answered** ([unknowns/16_vcn_colour_banks.md](unknowns/16_vcn_colour_banks.md)): the per-tile shift byte in the VCN; the DOS drawer ORs it into each pixel nibble before the colour table. | [formats/vcn_vmp.md](formats/vcn_vmp.md) |
| Q17 | Save files: the native fields ScummVM skips. **Mostly answered** ([unknowns/17_native_save_fields.md](unknowns/17_native_save_fields.md)): the options word (difficulty, effects, music, cursor, scrolling), the full 100-word flag table and 100-entry script-global table, and on the CD language, text and three volume bytes. Open: three single bytes, and no original `_SAVEnnn.DAT` has been examined | [savegame_format.md](savegame_format.md) |
| Q18 | Native in-memory layout of item and monster records. **Mostly answered** ([unknowns/18_native_records.md](unknowns/18_native_records.md)): item definitions 13 bytes, item slots 16, monster definitions 83, monster slots 46, field by field in both executables. Item word +0B is the base shop price. Open: who writes the monster critical-skill byte, and the roles of a few monster modifiers | [executable_tables.md](executable_tables.md) |
