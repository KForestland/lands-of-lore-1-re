# TIM opcodes

A TIM file is an IFF FORM. The AVTL chunk is a little-endian uint16 array. An optional TEXT chunk holds C strings indexed by a big-endian uint16 offset table. `TIMInterpreter::load` (`engines/kyra/script/script_tim.cpp:142-178`) reads both. The first words of AVTL are function entry indexes, up to `TIM::kCountFuncs` which is 10 (`script_tim.h:118`). WSA slots are 6 (`script_tim.h:133`).

An instruction is `length, delay, opcode_word, parameters...`. `length` is in words. The opcode is the low byte of word 2 (`script_tim.cpp:232`, `int8(cur.ip[2] & 0xFF)`). The next instruction is `ip + length` (`script_tim.cpp:258-259`). The delay added to the clock is the next instruction's word 1 (`script_tim.cpp:260-261`). CONFIRMED.

The high byte of every opcode word accepted by the walk below is 1. The interpreter ignores it. What that byte means is UNCONFIRMED.

`data/tim_analysis.json` lines 43-44 list opcodes 112 and 176. The command tables end at 0x1E. Those two numbers are not commands. The counts below replace that file's opcode map.

## Which table runs

CONFIRMED. The base table is `TIMInterpreter` (`script_tim.cpp:40-80`). `showIntro` and `showOutro` construct that class (`engines/kyra/sequence/sequences_lol.cpp:234` and `:1111`) and load `LOLINTRO.TIM` with `_timIntroOpcodes` (`sequences_lol.cpp:247`) and `LOLFINAL.TIM` with `_timOutroOpcodes` (`sequences_lol.cpp:1120`).

The running game constructs `TIMInterpreter_LoL` (`engines/kyra/engine/lol.cpp:563`). Its table is `script_tim.cpp:853-892`. `olol_loadTimScript` (`script_lol.cpp:1110-1115`) appends `.TIM` and loads with `_timIngameOpcodes`.

The 139 counts are the CD set: 139 `.TIM` names. LANDSoL has 147. CD-only names: `BUCKBUY`, `COMPASSE`, `COMPASSF`, `COMPASSG`, `SPELLBKE`, `SPELLBKF`, `SPELLBKG`, `TYRUS1` through `TYRUS5`, `YFLETCH2`. LANDSoL-only names include `LOLINTRO.TIM` (`INTRO.PAK`, 14086 bytes) and `LOLFINAL.TIM` (`FINALE2.PAK`, 5040 bytes). Intro and outro counts are those two LANDSoL files and are not part of the 139. CONFIRMED.

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
| 0x1E | `cmd_return(n1)` | 0 | Returns -1 (`script_tim.h:258`), which ends `exec`. Unused in the 139 and in both LANDSoL intro and outro. Stopping is opcode 0x01. | 0 | 0 |

`cmd_execOpcode` rejects `opcode > list.size()` (`script_tim.cpp:814`), so an index equal to the list size passes the comparison and is then out of range. Valid indexes are 0 through size-1. No counted script uses an index past the last registered opcode. CONFIRMED.

The one CD file with no opcode 0x06 is `DRARCLE8.TIM`. It uses 0x01 once and 0x14, 0x15, 0x17, 0x18, 0x19, 0x1D twice each. CONFIRMED.

Opcode 0x07's two uses are both in `VICTOR4.TIM` in `O02B.PAK`. The AVTL chunk starts at file offset 20. The instructions are AVTL word 6 (file offset 32), parameters `0, 0`, and AVTL word 263 (file offset 546), parameters `2, 0`. Under `TIMInterpreter_LoL` they warn and return 0. Whether the DOS in-game interpreter treated 0x07 as `cmd_displayText` is UNCONFIRMED.

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

`tlol_giveItem` reads three words and both call sites encode four. The fourth word is not read by this function. CONFIRMED. What a caller expected that word to do is UNCONFIRMED.

The single nested opcode 0x02 is in `VICTOR4.TIM`, the same file as the two command-0x07 instructions. CONFIRMED. It warns and returns 0.

`tlol_characterChat` reads three words. Two calls encode a fourth. `tlol_playDialogueTalkText` reads one word and passes a count of 1. Ten calls encode a second. Whether those extra words are read by the callee is UNCONFIRMED.

## Intro opcodes, LANDSoL LOLINTRO.TIM only

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

## Outro opcodes, LANDSoL LOLFINAL.TIM only

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

Both `tlol_fadeOutSound` calls encode zero argument words, so a build that evaluates the debug argument reads the next instruction's first word. `common/debug.h:33` makes `debugC` an empty inline when `DISABLE_TEXT_CONSOLE` is set, and a real call otherwise (`debug.h:88`). Whether the DOS outro read a parameter here is UNCONFIRMED.
