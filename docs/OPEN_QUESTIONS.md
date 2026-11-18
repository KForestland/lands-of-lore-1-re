# Open questions

Numbered so the format pages and [`STATUS.md`](STATUS.md) can point at them. Each is something not yet known about the original game files or rules. When one is answered, its page is updated and the entry says where.

| ID | Question | Page |
|----|----------|------|
| Q1 | SHP shape header in every edition: byte dumps of sample shapes from the CD, floppy and demo releases (the code says only the demo has 2 extra header bytes) | [formats/shp.md](formats/shp.md) |
| Q2 | CMZ header bytes 0-3 (`20 00 20 00` on every level): what they are and whether anything reads them | [formats/cmz.md](formats/cmz.md) |
| Q3 | Level 24's CMZ has 9 bytes per block instead of 4: what the extra 5 bytes hold, and why only this level | [formats/cmz.md](formats/cmz.md) |
| Q4 | When the level 22 scripts switch between the YVEL1 and YVEL2 tile sets | [formats/vcn_vmp.md](formats/vcn_vmp.md) |
| Q5 | The `.ADV`, `.DRV` and `.TBL` files: what each is, which program reads it, and the format as far as it is data | [formats/drivers.md](formats/drivers.md) |
| Q6 | The full TIM opcode table: number, name, parameters, effect, how many scripts use each | [formats/tim.md](formats/tim.md) |
| Q7 | Game rules as formulas: combat, magic, experience and skills, monster behaviour, light, time; meaning of the WLL wall flags and special types | [STATUS.md](STATUS.md#game-rules-and-executable-tables), [formats/wll.md](formats/wll.md) |
| Q8 | What script function 0x7E did in the original (called 1x on CD, 2x on floppy; ScummVM has no handler) | [formats/emc2.md](formats/emc2.md) |
| Q9 | Which PAK wins when two PAKs hold the same member name | [formats/pak.md](formats/pak.md) |
| Q10 | Who plays the 59 `NNNNN.VOC` members of the CD speech files | [formats/tlk.md](formats/tlk.md) |
| Q11 | Wall types used in the CMZ of levels 2, 3 and 21 that the level's WLL does not define | [formats/cmz.md](formats/cmz.md) |
| Q12 | Bit 0x8000 in automap legend string ids | [formats/xxx.md](formats/xxx.md) |
| Q13 | Order of the ten decoration slots (which scene position each slot is) | [formats/dat.md](formats/dat.md) |
| Q14 | Who loads CAV_PLT2.PAL, CAV_PLT4.PAL and ALTPAL3.PAL | [formats/palette.md](formats/palette.md) |
| Q15 | Music: what "C55" stands for; the ADL layout field by field; no MIDI converter yet | [formats/music.md](formats/music.md) |
| Q16 | What decides the 16-colour bank (shift value) of each wall tile | [formats/vcn_vmp.md](formats/vcn_vmp.md) |
| Q17 | Save files: the native fields ScummVM skips; no original `_SAVEnnn.DAT` examined yet | STATUS.md |
| Q18 | Native in-memory layout of item and monster records (the files only give the script arguments) | STATUS.md |
