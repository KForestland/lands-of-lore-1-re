# Open questions

Numbered so the format pages and [`STATUS.md`](STATUS.md) can point at them. Each is something not yet known about the original game files or rules. When one is answered, its page is updated and the entry says so. Detailed notes: [Q1](unknowns/01_shp_header.md), [Q2](unknowns/02_wll_header.md), [Q3](unknowns/03_level24_cmz.md), [Q4](unknowns/04_yvel2.md), [Q5](unknowns/05_adv_drv_tbl.md), [Q6](unknowns/06_tim_opcodes.md).

| ID | Question | Page |
|----|----------|------|
| Q1 | SHP shape header in every edition. **Answered for CD and floppy** (10-byte header, byte dumps match; 2026-11-18). Still open: the demo release, which was not read | [formats/shp.md](formats/shp.md) |
| Q2 | CMZ header bytes 0-3. **Answered:** `20 00 20 00` on all 29 levels of both editions, read by no engine code found. Calling them width and height (32 x 32) is a reading of the values, not of code | [formats/cmz.md](formats/cmz.md) |
| Q3 | Level 24's CMZ has 9 bytes per block instead of 4: what the extra 5 bytes hold, and why only this level. Measured (nine tail patterns, identical file in both editions); meaning still open | [formats/cmz.md](formats/cmz.md) |
| Q4 | When the level 22 scripts switch between YVEL1 and YVEL2. **Answered:** a click in a screen rectangle while block 145's north wall is type 8 loads YVEL2 and sets game flag 357; `LEVEL22.INI` reloads YVEL2 when flag 357 is set; another script path loads YVEL1 and clears the flag. Decorations stay YVEL1 | [formats/vcn_vmp.md](formats/vcn_vmp.md) |
| Q5 | The `.ADV`, `.DRV` and `.TBL` files. **Answered:** 7 Miles Design sound drivers (code), named by `LANDS.EXE`, `MAIN.EXE`, `FINALE.EXE`; `TRIG.TBL` is the copy-protection prompt string table | [formats/drivers.md](formats/drivers.md) |
| Q6 | The full TIM opcode table. **Answered** for the 139 CD scripts and the floppy intro/outro; a few ScummVM-unimplemented commands remain (see the page) | [formats/tim.md](formats/tim.md) |
| Q7 | Game rules as formulas: combat, magic, experience and skills, monster behaviour, light, time; meaning of the WLL wall flags and special types. **Written** ([game_rules.md](game_rules.md)): dice, hit test, armour and damage, experience thresholds and awards, spell damage tables and monster mode flags are checked in the original executables; magic effects, light, time, regeneration and most monster transitions are still ScummVM's version only. WLL flag meanings still open | [STATUS.md](STATUS.md#game-rules-and-executable-tables), [formats/wll.md](formats/wll.md) |
| Q8 | What script function 0x7E did in the original. **Answered:** in both executables the handler takes no arguments, calls one engine routine (game update and callback service) and returns 1. What that routine changes downstream is still open | [formats/emc2.md](formats/emc2.md) |
| Q9 | Which PAK wins when two PAKs hold the same member name | [formats/pak.md](formats/pak.md) |
| Q10 | Who plays the 59 `NNNNN.VOC` members of the CD speech files | [formats/tlk.md](formats/tlk.md) |
| Q11 | Wall types used in the CMZ of levels 2, 3 and 21 that the level's WLL does not define | [formats/cmz.md](formats/cmz.md) |
| Q12 | Bit 0x8000 in automap legend string ids | [formats/xxx.md](formats/xxx.md) |
| Q13 | Order of the ten decoration slots (which scene position each slot is) | [formats/dat.md](formats/dat.md) |
| Q14 | Who loads CAV_PLT2.PAL, CAV_PLT4.PAL and ALTPAL3.PAL | [formats/palette.md](formats/palette.md) |
| Q15 | Music: what "C55" stands for; the ADL layout field by field; no MIDI converter yet | [formats/music.md](formats/music.md) |
| Q16 | What decides the 16-colour bank (shift value) of each wall tile | [formats/vcn_vmp.md](formats/vcn_vmp.md) |
| Q17 | Save files: the native fields ScummVM skips. **Mostly answered** ([unknowns/17_native_save_fields.md](unknowns/17_native_save_fields.md)): the options word (difficulty, effects, music, cursor, scrolling), the full 100-word flag table and 100-entry script-global table, and on the CD language, text and three volume bytes. Open: three single bytes, and no original `_SAVEnnn.DAT` has been examined | [savegame_format.md](savegame_format.md) |
| Q18 | Native in-memory layout of item and monster records (the files only give the script arguments) | STATUS.md |
