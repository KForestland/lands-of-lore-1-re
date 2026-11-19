# TIM opcodes

A TIM file is an IFF FORM. The AVTL chunk is a little-endian uint16 array. An optional TEXT chunk holds C strings indexed by a little-endian uint16 offset table (`script_tim.cpp:643,703,756`). `TIMInterpreter::load` (`engines/kyra/script/script_tim.cpp:142-178`) reads both. The first words of AVTL are function entry indexes, up to `TIM::kCountFuncs` which is 10 (`script_tim.h:118`). WSA slots are 6 (`script_tim.h:133`).

An instruction is `length, delay, opcode_word, parameters...`. `length` is in words. The opcode is the low byte of word 2 (`script_tim.cpp:232`, `int8(cur.ip[2] & 0xFF)`). The next instruction is `ip + length` (`script_tim.cpp:258-259`). The delay added to the clock is the next instruction's word 1 (`script_tim.cpp:260-261`). CONFIRMED.

The high byte of every opcode word accepted by the walk below is 1. The runtime ignores it (native dispatch below). A separate compiler use of that byte is **UNCONFIRMED**.

`data/tim_analysis.json` lines 43-44 list opcodes 112 and 176. The command tables end at 0x1E. Those two numbers are not commands. The counts below replace that file's opcode map.

## Which table runs

CONFIRMED. The base table is `TIMInterpreter` (`script_tim.cpp:40-80`). `showIntro` and `showOutro` construct that class (`engines/kyra/sequence/sequences_lol.cpp:234` and `:1111`) and load `LOLINTRO.TIM` with `_timIntroOpcodes` (`sequences_lol.cpp:247`) and `LOLFINAL.TIM` with `_timOutroOpcodes` (`sequences_lol.cpp:1120`).

The running game constructs `TIMInterpreter_LoL` (`engines/kyra/engine/lol.cpp:563`). Its table is `script_tim.cpp:853-892`. `olol_loadTimScript` (`script_lol.cpp:1110-1115`) appends `.TIM` and loads with `_timIngameOpcodes`.

The 139 counts are the CD set: 139 `.TIM` names. floppy has 147. CD-only names: `BUCKBUY`, `COMPASSE`, `COMPASSF`, `COMPASSG`, `SPELLBKE`, `SPELLBKF`, `SPELLBKG`, `TYRUS1` through `TYRUS5`, `YFLETCH2`. floppy-only names include `LOLINTRO.TIM` (`INTRO.PAK`, 14086 bytes) and `LOLFINAL.TIM` (`FINALE2.PAK`, 5040 bytes). Intro and outro counts are those two floppy files and are not part of the 139. CONFIRMED.

The walk takes an entry when the instruction at that word has length 3..32, opcode-word high byte 1, and opcode at most 0x1E. It stops a function at the first word that fails, and does not count that word. Across the 139 CD files the stop count is 0. CONFIRMED.

## LoL command table, and use in the 139

The LoL column is `script_tim.cpp:853-892`. Where it matches the base table, the body is the base function. Parameter counts are the words the body reads. "Uses" is instruction count. "Files" is how many of the 139 contain it.

| Opcode | LoL command | Parameters | What it does | Uses | Files |
| --- | --- | --- | --- | --- | --- |
| 0x00 | `cmd_initFunc0` | 0 | Clears the 6 WSA slots and points function 0 at its AVTL (`script_tim.cpp:612-618`). `exec` already starts function 0 (`script_tim.cpp:206-208`). | 0 | 0 |
| 0x01 | `cmd_stopAllFuncs` | 0 | Base table uses `cmd_stopCurFunc` (`script_tim.cpp:45`, `:621-626`), which clears the current function. LoL waits while dialogue is up, clears every function ip, and returns -1 (`script_tim.cpp:1019-1028`), which ends `exec` (`script_tim.cpp:235-238`). | 139 | 139 |
| 0x02 | `cmd_initWSA` | 6: index, string id, x, y, offscreen, flags | Opens the named animation into that slot (`script_tim.cpp:634-645`). | 74 | 50 |
| 0x03 | `cmd_uninitWSA` | 1: index | Releases that slot (`script_tim.cpp:649-666`). | 60 | 43 |
| 0x04 | `cmd_initFunc` | 1: function | Points that function at its AVTL (`script_tim.cpp:669-676`). | 0 | 0 |
| 0x05 | `cmd_stopFunc` | 1: function | Clears that function's ip (`script_tim.cpp:679-683`). | 0 | 0 |
| 0x06 | `cmd_wsaDisplayFrame` | 2: slot, frame | Displays that frame (`script_tim.cpp:686-688`). | 4658 | 138 |
| 0x07 | unimplemented on LoL | Base: 2, text id and flags (`script_tim.cpp:691-696`) | LoL's slot is null. `execCommand` warns and returns 0 (`script_tim.cpp:1010-1012`). | 2 | 1 |
| 0x08 | `cmd_loadVocFile` | 2: string id, index | Resolves a TEXT string into a VOC slot (`script_tim.cpp:699-703`). | 0 | 0 |
| 0x09 | `cmd_unloadVocFile` | 1: index | Clears that slot (`script_tim.cpp:735-738`). | 0 | 0 |
| 0x0A | `cmd_playVocFile` | 2: index, volume | Volume is `param[1] * 255 / 100` (`script_tim.cpp:741-743`). | 0 | 0 |
| 0x0B | unimplemented | 0 | Warns and returns 0. | 0 | 0 |
| 0x0C | `cmd_loadSoundFile` | 1: string id | Loads that sound file (`script_tim.cpp:755-761`). | 0 | 0 |
| 0x0D | `cmd_return(1)` | 0 | Returns 1 (`script_tim.h:255-258`). | 0 | 0 |
| 0x0E | `cmd_playMusicTrack` | 1: track | Plays that track (`script_tim.cpp:765-767`). | 0 | 0 |
| 0x0F | unimplemented | 0 | Warns and returns 0. | 0 | 0 |
| 0x10 | `cmd_return(1)` | 0 | Returns 1. | 0 | 0 |
| 0x11 | `cmd_return(1)` | 0 | Returns 1. | 0 | 0 |
| 0x12 | unimplemented | 0 | Warns and returns 0. | 0 | 0 |
| 0x13 | unimplemented | 0 | Warns and returns 0. | 0 | 0 |
| 0x14 | `cmd_setLoopIp` | 0 | LoL override (`script_tim.cpp:1031-1040`): with speech it either stores the loop ip or advances to opcode 21; otherwise it stores the loop ip. | 175 | 118 |
| 0x15 | `cmd_continueLoop` | 1: factor | LoL override (`script_tim.cpp:1043-1060`). Factor 0 waits a fixed time. A nonzero factor adds a random wait. Returns -2, so the function pauses (`script_tim.cpp:241-242`). | 175 | 118 |
| 0x16 | `cmd_resetLoopIp` | 0 | Clears the loop ip (`script_tim.cpp:793-796`). | 0 | 0 |
| 0x17 | `cmd_resetAllRuntimes` | 0 | Sets every running function's next time to now (`script_tim.cpp:798-803`). | 170 | 76 |
| 0x18 | `cmd_return(1)` | 0 | Returns 1. | 88 | 59 |
| 0x19 | `cmd_execOpcode` | 1 + nested args | Dispatches `param[0]` into the TIM opcode list passed to `load` (`script_tim.cpp:806-824`). The nested table is below. | 807 | 67 |
| 0x1A | `cmd_initFuncNow` | 1: function | Starts that function now (`script_tim.cpp:827-832`). | 0 | 0 |
| 0x1B | `cmd_stopFuncNow` | 1: function | Stops that function now (`script_tim.cpp:835-838`). | 0 | 0 |
| 0x1C | `cmd_processDialogue` | 0 in the stream | Not encoded in any of the 139. `exec` calls command 28 when `procFunc` is set (`script_tim.cpp:217-218`). `cmd_dialogueBox` returns -3, which sets `procFunc` (`script_tim.cpp:245-247` and `:1103`). The body is `script_tim.cpp:1063-1080`. | 0 | 0 |
| 0x1D | `cmd_dialogueBox` | 4: function, three string ids | A string id of 0xFFFF is an empty button (`script_tim.cpp:1083-1103`). Returns -3. | 113 | 56 |
| 0x1E | `cmd_return(n1)` | 0 | Returns -1 (`script_tim.h:258`), which ends `exec`. Unused in the 139 and in both floppy intro and outro. Stopping is opcode 0x01. | 0 | 0 |

`cmd_execOpcode` rejects `opcode > list.size()` (`script_tim.cpp:814`), so an index equal to the list size passes the comparison and is then out of range. Valid indexes are 0 through size-1. No counted script uses an index past the last registered opcode. CONFIRMED.

The one CD file with no opcode 0x06 is `DRARCLE8.TIM`. It uses 0x01 once and 0x14, 0x15, 0x17, 0x18, 0x19, 0x1D twice each. CONFIRMED.

Opcode 0x07's two uses are both in `VICTOR4.TIM` in `O02B.PAK`. The AVTL chunk starts at file offset 20. The instructions are AVTL word 6 (file offset 32), parameters `0, 0`, and AVTL word 263 (file offset 546), parameters `2, 0`. Under `TIMInterpreter_LoL` they warn and return 0. The native in-game interpreter has a return-1 stub in both editions. See the native table below.

Opcode 0x19 parameter-word counts in the 139, including the nested opcode: 1 word on 80 instructions, 2 on 187, 3 on 16, 4 on 23, 5 on 4, 9 on 497. CONFIRMED.

## In-game nested opcodes

Registered in `script_lol.cpp:3020-3048`. The body lines are the reads. Counts are the opcode 0x19 sites in the 139. "Args" is words after the nested opcode.

| Opcode | Function | Args the body reads | Uses | Files | Args in the data |
| --- | --- | --- | --- | --- | --- |
| 0x00 | `tlol_initSceneWindowDialogue` | 1 (`script_lol.cpp:2416-2418`) | 5 | 5 | 1 on all 5 |
| 0x01 | `tlol_restoreAfterSceneWindowDialogue` | 1 (`:2422-2424`) | 5 | 5 | 1 on all 5 |
| 0x02 | unimplemented | 0 | 1 | 1 | 1 |
| 0x03 | `tlol_giveItem` | 3: type, frame, flags (`:2428-2430`) | 2 | 2 | 4 on both |
| 0x04 | `tlol_setPartyPosition` | 2: mode, then direction or block (`:2438-2445`) | 2 | 1 | 2 on both |
| 0x05 | `tlol_fadeClearWindow` | 1, switch 0..5 (`:2450-2494`) | 23 | 16 | 1 on all 23 |
| 0x06 | `tlol_copyRegion` | 8 (`:2500-2504`) | 497 | 10 | 8 on all 497 |
| 0x07 | `tlol_characterChat` | 3 (`:2508-2511`) | 25 | 17 | 3 on 23, 4 on 2 |
| 0x08 | `tlol_drawScene` | 1 (`:2514-2516`) | 6 | 6 | 1 on all 6 |
| 0x09 | `tlol_update` | 0 (`:2522-2525`) | 71 | 11 | 0 on all 71 |
| 0x0A | `tlol_clearTextField` | 0 (`:2528-2537`) | 9 | 4 | 0 on all 9 |
| 0x0B | `tlol_loadSoundFile` | 1 (`:2540-2542`) | 4 | 3 | 1 on all 4 |
| 0x0C | `tlol_playMusicTrack` | 1 (`:2546-2548`) | 5 | 4 | 1 on all 5 |
| 0x0D | `tlol_playDialogueTalkText` | reads `param[0]` and passes the pointer with count 1 (`:2552-2555`) | 77 | 40 | 1 on 67, 2 on 10 |
| 0x0E | `tlol_playSoundEffect` | 1 (`:2559-2561`) | 71 | 35 | 1 on all 71 |
| 0x0F | `tlol_startBackgroundAnimation` | 2 (`:2565-2567`) | 4 | 1 | 2 on all 4 |
| 0x10 | `tlol_stopBackgroundAnimation` | 1 (`:2571-2573`) | 0 | 0 | registered, unused by the 139 |

The 80 opcode-0x19 instructions with no argument word are the 71 updates plus the 9 text clears. The 497 instructions with 9 words are the 497 copies (opcode plus 8 arguments). CONFIRMED.

The argument counts in that table are the ScummVM bodies. The native reads follow; `MAIN.EXE+` addresses here are file offsets.

**CONFIRMED** Nested 0x03 at CD `MAIN.EXE+0x983F` (floppy `+0x9A0A`) pushes the three words at operand `+4`, `+2` and `+0` and drops them with `add sp, 6`. It does not pass the operand pointer. Both CD calls encode a fourth word 0 (`O01A.PAK+0x8DE4`, `O01E.PAK+0xA89`). That word is not a format argument.

The single nested opcode 0x02 is in `VICTOR4.TIM`, the same file as the two command-0x07 instructions. CONFIRMED. It warns and returns 0.

**CONFIRMED** The nested 0x07 handler at CD `MAIN.EXE+0x99C6` pushes start index 3, then the operand pointer (`6A 03 66 FF 76 06` at `+0x99C9–0x99CB`). The nested 0x0D handler starts at `+0x9AD9`: it first plays the voice for operand 0, and only when that returns 0 or byte `DS:81FE` is nonzero does it reach the same two pushes with start index 1 at `+0x9B08`. The floppy handlers `+0x9B8D` and `+0x9C64` make the same two pushes (the floppy 0x0D has no voice gate). 0x07 reaches `+0x16C6D`, which forwards the pointer and the start index for mode 0 at `+0x16DBC` and mode 1 at `+0x16E02`; mode 2 pushes a literal 3 and the pointer at `+0x16E56`. 0x0D calls `+0x1731C` directly. That function calls the formatter at `+0x1705E` (`+0x173FC` pushes the start index, the operand pointer, and the format string). The formatter loads SI from `[bp+0x12]` at `+0x17066`. While `[bp+0xA]` is 0, each `%n` (`+0x1719C`), `%s` (`+0x171E8`) and `%d`, `%u`, `%x` or `%X` (shared handler, read at `+0x1728D`) reads one word at `operand[SI]` and increments SI. The conversion table at `+0x172B8` (floppy `+0x1B911`) has only these codes and `%a`, which reads the word `DS:4BEA` and no operand; any other code is not handled. `%n` then uses `word * 0x82 + 0x362F` (`+0x171A8`). The text id comes from `+0xC348`, which masks with `0x3FFF` (`+0xC360`) and takes the string at `index * 2` (`+0x24C34`).

**CONFIRMED** Six of the twelve CD calls that encode an extra word resolve a level string with one `%n`, so the extra word is that character index. The word is 0 at all 14 CD sites.

| Call | Text id | String in the level file | Codes |
| --- | ---: | --- | --- |
| `O01E.PAK` `KING1.TIM` talk | 8 | `L01.PAK+0x65FE` `LEVEL01.ENG` | one `%n` |
| `O02B.PAK` `TIM1.TIM` talk | `0x3E` | `L02.PAK+0xC338` `LEVEL02.ENG` | one `%n` |
| `O02B.PAK` `TIM1.TIM` talk | `0x43` | `L02.PAK+0xC415` | one `%n` |
| `O02B.PAK` `VICTOR6.TIM` talk | `0x4C` | `L02.PAK+0xC5CF` | one `%n` |
| `O04A.PAK` `ROLAND1.TIM` chat | 2 | `L04.PAK+0x9178` `LEVEL04.ENG` | one `%n` |
| `O07A.PAK` `POD2.TIM` chat | `0x11` | `L07.PAK+0x5F5B` `LEVEL07.ENG` | one `%n` |

**CONFIRMED** The other six extra words are 0, and the string has no `%` code, so this formatter call does not read them: `LEVEL02.ENG` `0x4E` at `L02.PAK+0xC63A`, `0x50` at `+0xC688`, `0x51` at `+0xC6D8`; `LEVEL07.ENG` `0x0E` at `L07.PAK+0x5ECD`, `0x0F` at `+0x5ED7`, `0x12` at `+0x5F76`.

**CONFIRMED** Floppy `CHAPTER1.PAK` talk calls in `BUCK03.TIM`, `BUCK04.TIM`, `BUCK05.TIM` and `BUCK14.TIM` pass 20, 10, 10 and 100. Each is the `%d` of one `LEVEL03.ENG` string: `0x28` at `CHAPTER1.PAK+0x56C74`, `0x2B` at `+0x56CB2`, `0x2C` at `+0x56CCF`, `0x2A` at `+0x56C96`. The floppy formatter loads SI at `MAIN.EXE+0x1B6BF` and reads `operand[SI]` at `+0x1B7F5`, `+0x1B841` and `+0x1B8E6`.

## Intro opcodes, floppy LOLINTRO.TIM only

Four function entries, stop count 0. Nested list is `script_lol.cpp:2978-2991`.

Commands: 0x01 x3 (0 params), 0x02 x14 (6), 0x03 x16 (1), 0x06 x1022 (2), 0x08 x28 (2), 0x09 x28 (1), 0x0A x100 (2), 0x0C x1 (1), 0x0E x1 (1), 0x14 x2 (0), 0x15 x2 (1), 0x17 x12 (0), 0x18 x12 (0), 0x19 x83, 0x1A x3 (1), 0x1B x3 (1). The 83 dispatches have 2, 3, and 6 parameter words on 19, 37, and 27 instructions. CONFIRMED.

| Nested | Function | Body reads | Uses | Args in the data |
| --- | --- | --- | --- | --- |
| 0x00 | `tlol_setupPaletteFade` | 1 (`script_lol.cpp:2356-2358`) | 10 | 1 |
| 0x01 | unimplemented | 0 | 0 | |
| 0x02 | `tlol_loadPalette` | 1, a string id (`:2363-2366`) | 4 | 1 |
| 0x03 | `tlol_setupPaletteFadeEx` | 1 (`:2370-2374`) | 5 | 1 |
| 0x04 | `tlol_processWsaFrame` | 5 (`:2379-2387`) | 27 | 5 |
| 0x05 | `tlol_displayText` | 2 when not the outro, 3 when it is (`:2407-2412`) | 37 | 2, which matches the non-outro path |
| 0x06 | unimplemented | 0 | 0 | |
| 0x07 | unimplemented | 0 | 0 | |

## Outro opcodes, floppy LOLFINAL.TIM only

Four function entries, stop count 0. Nested list is `script_lol.cpp:2993-3018`. `load` sets `isLoLOutro` for this filename (`script_tim.cpp:178`).

Commands: 0x01 x3, 0x02 x12 (6), 0x03 x11 (1), 0x06 x194 (2), 0x07 x1 (2), 0x08 x10 (2), 0x09 x10 (1), 0x0A x28 (2), 0x0C x1 (1), 0x0E x3 (1), 0x14 x2, 0x15 x2, 0x17 x9, 0x18 x10, 0x19 x110, 0x1A x2, 0x1B x2. The 110 dispatches have 1, 2, 3, and 4 parameter words on 2, 42, 61, and 5 instructions. The single 0x07 is the base `cmd_displayText`, because the outro uses `TIMInterpreter`, not `TIMInterpreter_LoL`. CONFIRMED.

| Nested | Function | Body reads | Uses | Args in the data |
| --- | --- | --- | --- | --- |
| 0x00 | `tlol_setupPaletteFade` | 1 | 0 | |
| 0x01 | unimplemented | 0 | 0 | |
| 0x02 | `tlol_loadPalette` | 1 | 0 | |
| 0x03 | `tlol_setupPaletteFadeEx` | 1 | 0 | |
| 0x04 | unimplemented | 0 | 0 | |
| 0x05 | `tlol_fadeInScene` | 2 string ids (`script_lol.cpp:2577-2580`) | 4 | 2 |
| 0x06 | `tlol_unusedResourceFunc` | the body returns 1 (`:2618-2621`); the debug line names `param[0]` | 19 | 1 |
| 0x07 | `tlol_unusedResourceFunc` | same function | 19 | 1 |
| 0x08 | `tlol_fadeInPalette` | 2: string id, fade steps (`:2624-2637`) | 1 | 2 |
| 0x09 | unimplemented | 0 | 0 | |
| 0x0A | unimplemented | 0 | 0 | |
| 0x0B | `tlol_fadeOutSound` | the body calls `beginFadeOut()` and does not use a parameter (`:2642-2645`); the debug line names `param[0]` | 2 | 0 |
| 0x0C | `tlol_displayAnimFrame` | 2 (`:2648-2651`) | 56 | 2 |
| 0x0D | `tlol_delayForChat` | 1 (`:2664-2667`) | 4 | 1 |
| 0x0E | `tlol_displayText` | 3 on the outro path (`:2409-2410`) | 5 | 3 |
| 0x0F | unimplemented | 0 | 0 | |

Both `tlol_fadeOutSound` calls encode zero argument words, so a build that evaluates the debug argument reads the next instruction's first word. `common/debug.h:33` makes `debugC` an empty inline when `DISABLE_TEXT_CONSOLE` is set, and a real call otherwise (`debug.h:88`). The native outro has a vestigial read and forwards no argument to the audio helper. See the executable trace below.

## Native DOS tables

**CONFIRMED** Native offsets below are file offsets. CD `MAIN.EXE+0x14D6C` and floppy `MAIN.EXE+0x196F3` call the in-game TIM loaders. The loaders request `AVTL` and `TEXT` at CD `+0x9C09–0x9CBC` and floppy `+0x9D64–0x9E17`. At dispatch the processor reads the signed low byte of the opcode word from instruction `+4`, passes the instruction's `+6` operand pointer, and indexes far pointers by 4. CD `+0x9EDA–0x9F04` uses `DS:1DCC` (file `+0x3389C`). Floppy `+0x9FCC–0x9FF6` uses `DS:1F08` (file `+0x39768`). The stepper adds two times the instruction's first word to the IP and reads the next instruction's signed delay word (CD `+0x9D26–0x9D64`, floppy `+0x9E81–0x9EB1`). The source counterpart is `engines/kyra/script/script_tim.cpp:232–261,853–892` at upstream `3b4db303`.

| Slot | CD routine | floppy routine | Native result (**CONFIRMED**) |
| --- | ---: | ---: | --- |
| `07` | `0x94B9` | `0x96A0` | Return 1. Both bodies leave the operands unread. |
| `0A` | `0x94D1` | `0x96B8` | CD returns 1. Floppy resolves the first word to a TIM TEXT offset, plays it through the voice helper and increments the original operand in memory (`0x96BB–0x96E2`, helper `0x11CD2–0x11D23`). |
| `0B` | `0x94D9` | `0x96E7` | CD returns 1. Floppy calls a voice-stop and buffer-release helper, then returns 1 (`0x11C71–0x11CAB`). |
| `0F` | `0x9505` | `0x9718` | Both call the music-stop helper and return 1. The helper stops/releases the current track when present (CD `0x1B22E–0x1B27E`, floppy `0x120BE–0x1210F`). |
| `12` | `0x9522` | `0x9735` | Both read one word and send it to the sound-effect track helper with default level `0xFF`, then return 1 (CD `0x1B566–0x1B5AA`, floppy `0x11DEE–0x11E32`). |
| `13` | `0x9536` | `0x9749` | Both stop and release up to four effect tracks, clearing their IDs to `FFFF`, then return 1 (CD `0x1B683–0x1B6D9`, floppy `0x12031–0x12087`). |
| `1A`, `1B` | `0x33904`, `0x33908` | `0x397D0`, `0x397D4` | Null in both native in-game tables. These have separate valid entries in the sequence executable. |
| `19/02` | `0x9837` | `0x9A02` | Return 1, with no read of the supplied word. The `19` handler indexes the nested table at CD `+0x33918` or floppy `+0x397E0` and skips the selector when passing the operand pointer (`0x9621–0x964B`, `0x980F–0x9839`). |

**CONFIRMED** Both editions store the same `VICTOR4.TIM` witness sequence. The `19/02` instruction starts at CD `O02B.PAK+0xCEE1` and floppy `CHAPTER1.PAK+0xE7548` (length word 5, opcode word `0x0119`, selector 2). Its argument word is 0 at CD `+0xCEE9` and floppy `+0xE7550`. The two `07` calls pass `(0, 0)` and `(2, 0)` at CD `+0xCEEB, +0xD0ED` and floppy `+0xE7552, +0xE774E`. Those arguments go to the return-1 routines above.

### floppy finale executable

**CONFIRMED** `FINALE.EXE+0x6ED7–0x6EE1` loads `LOLFINAL.TIM` using the name at `+0x2272A`. Its TIM dispatcher at `+0xB722–0xB741` uses `DS:3B52` (file `+0x26142`). Opcode `19` at `+0xB173–0xB1A4` dispatches through `DS:3BCE` (file `+0x261BE`). The DS segment is set at `+0x2E00–0x2E16`.

| Slot in `FINALE.EXE` | File entry | Native observation (**CONFIRMED**) |
| --- | ---: | --- |
| `07` | `0xAE40` | Forwards the two operand words and fixed value `0xF2` to the text helper. The outro example at `FINALE2.PAK+0x750DE` supplies `(1, FFFF)`. |
| `0B`, `0F`, `12`, `13` | `0xAFAF`, `0xB042`, `0xB065`, `0xB07B` | Call the voice cleanup, music-stop and two effect helpers respectively, using one operand for `12`. Their callees are `0xC561`, `0xCA24`, `0xC704`, `0xC983`. Each returns 1. |
| `19/01` | `0x261C2` (table) | Null far pointer. |
| `19/04` | `0x78CC` | Reads multiple frame operands and branches on the high and low nibbles of word 3 (`0x78D4–0x7942`). |
| `19/06`, `19/07` | `0x7B80`, `0x7BAA` | Each reads a TEXT offset by the supplied index and forwards the resulting string to a separate resource routine (`+0x11DF0`, `+0x11C58`). `FINALE2.PAK+0x7503C` and `+0x7531C` provide examples. |
| `19/09`, `19/0A` | `0x7688`, `0x7838` | Both read word 0. The former scales it by `0x8C` and branches on word 1. The latter chooses one of four name pointers from a global and indexes a far-handle array by word 0. See `+0x768F–0x76D1` and `+0x783F–0x78A0`. |
| `19/0B` | `0x7820` | Compares the first following word to zero, with a zero-distance branch. Calls the audio helper at `0xCAFC` with no arguments and returns 1. Original commands at `FINALE2.PAK+0x75CC8, +0x75FA2` encode only the nested selector. |
| `19/0F` | `0xB1FD` | Calls three functions, with a fixed string pointer on the first call, and returns `FFFF` (`+0xB1FD–0xB21C`). Its fixed string is at `+0x261FE`. |

### Floppy intro table selection

**CONFIRMED** In `LANDS.EXE`, startup sets the relative DS segment
to 0x1A56 (`+0x1E00–0x1E16`), so DS-relative data starts at file
`+0x1C360`. The intro call at `+0x6EB7–0x6EC8` passes
DS:0684, the `LOLINTRO.TIM` name at `+0x1C9E4`, to the loader
at `+0x8539`. The loader selects AVTL at `+0x85EE–0x85FE`.
The caller saves the returned pointer and passes it to the TIM
runner at `+0x6ED3–0x6EEC`. The runner dispatches through
DS:06EC at `+0x895E–0x897D` (file table `+0x1CA4C`).
Outer slot 0x19 at `+0x1CAB0` resolves to `+0x83AF`.
That handler reads the first operand word as the nested selector, passes the following words, and indexes the nested far pointers
at DS:0768, file `+0x1CAC8` (`+0x83B5–0x83D3`).

**CONFIRMED** The first seven word pairs in that nested table
resolve to callbacks `0x786B, null, 0x77E5, 0x781F, 0x78B9,
0x80AF, 0x8439` in selector order. At `LANDS.EXE+0x78C1–0x78F6`,
selector 4 reads five words from its operand pointer, including word 0
as a 0x8C-byte record index and word 4 at +8. Selector 5 forwards
two words to its helper (`+0x80AF–0x80C6`). The selector-4
witness is `INTRO.PAK+0xB538B`. Upstream ScummVM's intro
selection and operand reads are in `engines/kyra/sequence/sequences_lol.cpp:234–247`
and `engines/kyra/script/script_lol.cpp:2379–2387,2407–2412,2978–2991`
at `3b4db303`.

**CONFIRMED** The same filename has a separate path in
`FINALE.EXE`. When its branch at `+0x6F72–0x6F7D` succeeds,
it frees the prior sequence and passes DS:0147 to the same loader
as the outro (`+0x6F85–0x6FB1` and `+0x6ED7–0x6EE8`).
That operand resolves to `LOLINTRO.TIM` at `+0x22737`.
Both calls place the returned pointer in DS:00CA/00CC.
The shared call at `+0x6EFC–0x6F0C` runs it through the
TIM runner at `+0xB5CA`, whose dispatcher is at `+0xB722–0xB741`. Its hard-coded nested table is DS:3BCE
(`+0xB193`), with selector 4 at file `+0x261CE` resolving to
`+0x78CC`. Thus the two sequence executables each have a fixed
table, and the `FINALE.EXE` branch uses its own table for either
filename. The two intro filename calls and their fixed tables can
thus be located without a runtime breakpoint.

**UNCONFIRMED** Higher-level names for several unused native
callbacks remain open.

**CONFIRMED** TEXT offsets in these files are little-endian. floppy `VICTOR4.TIM` stores its initial offsets as `06 00 3C 00 BF 00` at `CHAPTER1.PAK+0xE7926`; the floppy `0A` handler reads the offset word directly at `MAIN.EXE+0x96CC`. The equivalent read in ScummVM is `engines/kyra/script/script_tim.cpp:643,703,756`.
