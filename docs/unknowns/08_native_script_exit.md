# Q8 — EMC2 function 0x7E exits to DOS

**CONFIRMED** Native EMC2 function `0x7E` takes no script arguments. In both original `MAIN.EXE` files it prepares engine shutdown, then invokes the DOS runtime exit routine with status 0. The wrapper contains a later instruction to return 1. Under normal DOS operation `INT 21h` with `AH=4Ch` terminates the process before the wrapper can execute it. The decompiler labels the function `exitGame`. ScummVM's dispatch marks it unimplemented (`engines/kyra/script/script_lol.cpp:2874–2878`, `engines/kyra/script/script.cpp:309–321`).

| Native step | CD file offset | floppy file offset |
| --- | --- | --- |
| EMC2 handler, then zero-argument shutdown preparation and `exit(0)` | `0x159A4–0x159B0`, `0xC846–0xC857` | `0x1A2B1–0x1A2BD`, `0x10062–0x10073` |
| Engine shutdown preparation | `0x2689C–0x2692F` | `0x1DAB8–0x1DB2D` |
| Runtime wrapper input 0 and two additional zero arguments | `0x3E54–0x3E62` | `0x4E54–0x4E62` |
| Drain registered callbacks from the last entry down, decrementing the count | `0x3DFD–0x3E26`, count `DS:3AE2` | `0x4DFD–0x4E26`, count `DS:6F26` |
| Restore interrupt vectors No. 0, 4, 5 and 6 from the saved pointers with DOS function 25h and call the last cleanup vectors | `0x39C0–0x39EC`, `0x3E2A–0x3E45` | `0x49C0–0x49EC`, `0x4E2A–0x4E45` |
| Pass the status byte in AL to DOS terminate-process function 4Ch | `0x3E46–0x3E4E` → `0x396B–0x3973` | `0x4E46–0x4E4E` → `0x496B–0x4973` |
| Program startup uses the same runtime wrapper with the value returned by the game's main routine | `0x394C–0x3956` | `0x494C–0x4956` |

## What the preparatory routine changes

**CONFIRMED** CD tests and clears a one-shot shutdown flag at `DS:3618` before its cleanup calls. It clears two service IDs to −1 and calls four more overlay routines (CD `0x2689F–0x268B3`, `0x52330–0x5236F`). floppy's prep instead starts with a call that clears one service ID to −1 (floppy `0x1DABB`, `0x57E5C–0x57E7D`). Both editions invoke an optional registered far callback, CD `DS:361E` and floppy `DS:63EA`. Both call BIOS video interrupt 10h to query current mode with `AX=0F00h`, compare AL with their saved mode, and invoke the mode-selection helper if different. That helper loads the saved mode for argument 9 (CD `0x268EB–0x26909`, `0x26C7F–0x26CE2`; floppy `0x1DAE2–0x1DB00`, `0x24FED–0x25050`).

**CONFIRMED** The two routines clear a pending pointer after calling its service shutdown if it is set (CD `0x56333–0x5636A`, floppy `0x25A44–0x25A7C`). Both optionally print a NUL-terminated byte string via DOS function 06h when their preceding runtime call returns −1 (CD `0x26914–0x2692B`, `0x2413E–0x2415E`; floppy `0x1DB06–0x1DB1A`, `0x27BC6–0x27BE5`). floppy also installs interrupt vector 3Fh from the saved pointer at `DS:E31E` with DOS function 25h (floppy `0x1DB1D–0x1DB29`, `0x4F92–0x4FA2`).

**UNCONFIRMED** Which optional service callbacks execute on a particular audio or video configuration is open. The static trace followed the resident and overlay targets and the DOS exit path. To identify the configuration-specific effects, record the indirect targets and registers on entry to the two prep routines and log interrupts 10h and 21h through process exit.

## Script evidence

**CONFIRMED** `LEVEL2.INF` calls 0x7D at DATA word `0x019A`, stores its result, and skips the exit block if the result is nonzero. On zero it runs a scene subroutine, plays sound 110, delays five times by nine ticks and calls 0x7E at word `0x01B9`. The common continuation starts with sound 111 and is reachable by the nonzero branch. CD `L02.PAK+0xF3CF–0xF40F`; floppy `CHAPTER1.PAK+0x5B313–0x5B353`. floppy `LEVEL19.INF` has the second 0x7E call in the same zero-result pattern at word `0x0418`, `CHAPTER5.PAK+0x2C644–0x2C68E`. CD's native 0x7D always returns 1 (resolved overlay `MAIN.EXE+0x4E3E0–0x4E3E7`). floppy's 0x7D consumes two arguments, invokes its comparison routine and returns its success value (resolved overlay `MAIN.EXE+0x57071–0x5709B`, comparison `0x57000–0x5701E`).

**CONFIRMED** Worked example: decompile `LEVEL2.INF` with `python3 tools/emc2_decompile.py "$LOL1_DATA/L02.PAK" --entry LEVEL2.INF`. The listing places `01B9  sysCall  0x7E exitGame` immediately before the branch target `L_01BA`. The call instruction is `4E 7E` at CD `L02.PAK+0xF40D`. It pushes no script argument and no result is read on the fall-through path (same DATA words).
