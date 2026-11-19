# What's new

Newest first. One line per question worked on, new tool or visible change; each question bullet gives its state. Details are on the linked pages; the counts are in the [rating](../README.md#rating).

## 19 November 2026

- **Twelve loose files, second pass.** The blend tables and the symbol blocks now have a measured layout and a settling test. They stay unread: in each symbol block only the string pool at the end is walked, and the bytes before it are unread. None of the eleven simple index formulas tried (minimum, maximum, average rounded down or up, product /255 or >>8, sum, difference, OR, AND, XOR) reproduces a blend table; palette-based formulas were not tried ([loose files](formats/loose.md)).
- **Loose CD files.** `lol1_loose.py` walks 25 files that are not PAK or TLK archives through their last byte; these 25 are inside the 187 of 199 files counted as read. The twelve not counted are the six blend tables, the three `.TDS` symbol files and the three `LANDS.EXE` tails; the page gives the test that would finish each one.
- **TIM extra words (Q6, answered).** Nested 0x07 and 0x0D pass those words into the `%` formatter; `lol1_tim_words.py` re-reads the pushes and the strings.
- **Counted rating.** The README and [STATUS](STATUS.md) show four counted lines instead of a percentage; [how we rate](HOW_WE_RATE.md) explains them.
- **Example pictures remade.** The guard is drawn in its real colours, the talking head in its backdrop's palette, and level 1 as a readable map; a check now compares each example with today's tools pixel for pixel ([examples](../examples/README.md)).
- **Quitting the game (Q8, answered).** The answered probe is one quit from play on the English CD with Sound Blaster, traced and re-read in the program. Whether any setup registers a nonzero shutdown callback stays open.
- **Monster fields (Q7 and Q18, both mostly answered).** Both editions' programs were scanned for every reference to the monster skill and modifier fields ([native records](unknowns/18_native_records.md)). Computed aliases to those fields stay open (Q18), as do wall bit 0x40 and one mode-10 producer (Q7).
- **Unused clip and palettes (Q10 mostly answered, Q14 partly answered).** The finale program's file catalog names the silent speech clip, but no code that reaches that row is found. No caller of the three unused palettes is found in any program or the installer. Both stay open until a caller is found.
- **New checks:** `rating.py`, `example_images.py`, `lol1_name_callers.py`; `shp_renderer.py --level` draws monster shapes in their level's palette.

## 18 November 2026

- **Running-game results.** The CD launch works in the original game. The level-1 wall flags (a level-1 control for Q7) and three save bytes (a partial run for Q17) were checked; neither run answers its probe ([NEEDS_A_RUNNING_GAME](NEEDS_A_RUNNING_GAME.md)).
- **Game rules (Q7, mostly answered; wall bit 0x40 and one mode-10 producer remain) and many open questions answered** from both original programs: the 60 Hz clock, monster modes, the AdLib music layout, the C55 music set and more ([open questions](OPEN_QUESTIONS.md)).
- **Guides.** [Start here](START_HERE.md), [how the game works](HOW_THE_GAME_WORKS.md), a [quick reference](QUICK_REFERENCE.md) and a [worked example](tutorial-one-event.md).
- **Level sheets** for all 29 levels, and XMIDI and AdLib music converted to standard MIDI.
