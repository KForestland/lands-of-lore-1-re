# TIM sequence scripts

**What:** small scripts that run cut-ins and talking scenes: they start WSA animations, show dialogue, play sound, loop.

**Edition read:** CD (139 in `DATA/`, 6 per language folder), floppy (147).

## Container

IFF `FORM` with type `AVFS`; chunks `TEXT` (strings) and `AVTL` (code, 16-bit words). CONFIRMED: all 139 CD files start `FORM`, bytes 8-11 `AVFS`. Loader: `TIMInterpreter::callback` / `load` `engines/kyra/script/script_tim.cpp:115-170`.

## Commands

An AVTL instruction is `length, delay, opcode word, parameters…` (words, little-endian); the opcode is the low byte of word 2 and the next instruction is `ip + length` (`engines/kyra/script/script_tim.cpp:232`, `:258-261`). The first up to 10 words of AVTL are the entry points of up to 10 parallel functions (`:173-175`). The in-game table is `TIMInterpreter_LoL` (`script_tim.cpp:853-892`); command 0x19 dispatches to a nested list of game functions (`engines/kyra/script/script_lol.cpp:3020-3048`).

Use in the 139 CD scripts (instructions / files), CONFIRMED by two independent walkers:

| Opcode | Command | Uses | Files |
|--------|---------|------|-------|
| 0x01 | stop all functions | 139 | 139 |
| 0x02 | init WSA animation (slot, name, x, y, offscreen, flags) | 74 | 50 |
| 0x03 | release WSA slot | 60 | 43 |
| 0x06 | display WSA frame (slot, frame) | 4658 | 138 |
| 0x07 | display text (not implemented for the in-game table in ScummVM; natively a return-1 stub in both editions, [Q6](../unknowns/06_tim_opcodes.md)) | 2 | 1 |
| 0x14 | set loop point | 175 | 118 |
| 0x15 | continue loop (pause) | 175 | 118 |
| 0x17 | reset all run times | 170 | 76 |
| 0x18 | return 1 | 88 | 59 |
| 0x19 | run a nested game function | 807 | 67 |
| 0x1D | dialogue box (function, three string ids) | 113 | 56 |

The other commands of the table (0x00, 0x04, 0x05, 0x08-0x13, 0x16, 0x1A-0x1C, 0x1E) occur in none of the 139. Nested functions used (count): scene-window dialogue on/off 5/5, give item 2, set party position 2, fade/clear window 23, copy screen region 497, character chat 25, draw scene 6, update 71, clear text field 9, load sound file 4, play music 5, play dialogue/talk text 77, play sound effect 71, start background animation 4; one call of an unimplemented slot (0x02) in `VICTOR4.TIM`.

The full table with parameters, ScummVM lines, and the intro (`LOLINTRO.TIM`) and outro (`LOLFINAL.TIM`) lists of the floppy edition: [`../unknowns/06_tim_opcodes.md`](../unknowns/06_tim_opcodes.md).

## Correction

The March 2026 `data/tim_analysis.json` listed opcodes 112 and 176; those are not commands (the table ends at 0x1E). The file was regenerated on 2026-11-18 by `tools/parse_tim.py` without that opcode map and without the raw script words it used to copy; the counts above replace it.

The [native table selection](../unknowns/06_tim_opcodes.md#floppy-intro-table-selection)
identifies the separate intro and finale tables from the original
floppy executables. CONFIRMED.

## Extra argument words

**CONFIRMED** Nested 0x07 and 0x0D pass the operand pointer and a start index (3 and 1) into the formatter at CD `MAIN.EXE+0x1705E`. Each `%n`, `%s`, `%d`, `%u`, `%x` or `%X` reads one word at `operand[index]`; `%a` reads none, and the formatter handles no other code. Six CD calls resolve a level string with one `%n`, so the extra word is that character index, and it is 0. Six more resolve a string with no `%` code, so that call does not read the extra 0. Nested 0x03 pushes three words and does not pass its fourth word, which is 0 at both calls. On the floppy, `BUCK03.TIM`, `BUCK04.TIM`, `BUCK05.TIM` and `BUCK14.TIM` pass 20, 10, 10 and 100 into one `%d` each. Offsets: [Q6](../unknowns/06_tim_opcodes.md).

## Worked example

CD `AUTOMAP.TIM` starts:

```
46 4f 52 4d 00 00 01 36 41 56 46 53   41 56 54 4c 00 00 01 1e   01 00   03 00 00 00 18 01   09 00 00 00 02 01 …
```

| Bytes | Meaning |
|-------|---------|
| `FORM`, `00 00 01 36`, `AVFS` | IFF form, type AVFS |
| `AVTL`, `00 00 01 1e` | 286 bytes of code (little-endian words from here on) |
| `01 00` | function 0 starts at word 1 |
| `03 00 00 00 18 01` | instruction: length 3 words, delay 0, opcode word 0x0118: command 0x18 (return 1) |
| `09 00 00 00 02 01 …` | instruction: length 9, delay 0, command 0x02 (init WSA) with 6 parameters |

**Tool:** `tools/parse_tim.py` (`--list NAME.TIM` prints one file command by command; chunk structure; `--check` rebuilds the file list and statistics of `data/tim_analysis.json`: 139/139, chunks AVTL 139, TEXT 51).
