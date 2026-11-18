# EMC2 level scripts (INF, INI)

**What:** compiled level scripts. `LEVELn.INI` runs once when the level is loaded (`engines/kyra/engine/scene_lol.cpp:69`); `LEVELn.INF` holds the level's event functions (`:78`).

**Edition read:** CD (31 INF, 29 INI). floppy: same counts.

## Container

IFF `FORM` with type `EMC2`; chunks `TEXT` (optional strings), `ORDR` (function start table), `DATA` (16-bit code words). CONFIRMED: all 60 CD files start `FORM`, bytes 8-11 `EMC2`. Loader: `EMCInterpreter::load` / `callback` `engines/kyra/script/script.cpp:61-146`.

## Full documentation

- [`../emc2_scripts.md`](../emc2_scripts.md): container details (the FORM length includes the 8 header bytes; ORDR word indexes and entry headers; TEXT offsets), the 19 VM opcodes and 18 `eval` operators, the full 192-entry LoL1 function table with call counts per edition and the native handler addresses, and where each script sits in its PAK.
- [`../executable_tables.md`](../executable_tables.md): the 285 item definitions and 79 monster definitions are supplied by script calls (`ONETIME.INF`, level scripts), with their argument layouts.
- Disassembler: `tools/emc2_decompile.py`; test: `tests/test_emc2_corpus.py` (all 60 scripts of both editions disassemble with no unknown opcode or function).

## Open

- [Q8](../OPEN_QUESTIONS.md), answered: function 0x7E exits the game to DOS ([`../unknowns/08_native_script_exit.md`](../unknowns/08_native_script_exit.md)). Before that was known: the original executables keep their own function tables (192 far pointers at CD `MAIN.EXE+0x33F64`, 187 at floppy `MAIN.EXE+0x3D1EE`, entries 0x00-0xBA: the floppy program simply has no functions 0xBB-0xBF, which only the CD scripts call). Entry 0x7E points to a handler that takes no arguments, calls one engine routine and returns 1. CONFIRMED (disassembled). Its downstream effect is UNCONFIRMED.
- Apart from 0x7E, native handler bodies were not checked; function effects are ScummVM's (UNCONFIRMED for the original).

## Worked example

CD `LEVEL1.INI` (670 bytes) starts:

```
46 4f 52 4d  00 00 02 9e  45 4d 43 32   4f 52 44 52  00 00 00 04  00 1b 00 9f   54 45 58 54  00 00 00 6d  00 14 00 19 …
```

| Bytes | Meaning |
|-------|---------|
| `FORM`, `00 00 02 9e`, `EMC2` | IFF form; the length 0x29E = 670 is the whole member, including these 8 bytes |
| `ORDR`, `00 00 00 04`, `00 1b 00 9f` | two entry points (big-endian): each points at a header word (DATA word 0x1B and 0x9F); the function's code starts on the next word (0x1C and 0xA0) |
| `TEXT`, `00 00 00 6d`, `00 14 00 19 …` | 109 bytes of strings; string 0 at 0x14 is `KEEP`, string 1 at 0x19 is `LEVEL01` |

`tools/emc2_decompile.py L01.PAK --entry LEVEL1.INI` lists the code; for example word 0x26 is `sysCall 0x09 loadLevelGraphics [arg0=TEXT[0] "KEEP"]`.
