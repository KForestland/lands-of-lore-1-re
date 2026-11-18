# EMC2 level scripts (INF, INI)

**What:** compiled level scripts. `LEVELn.INI` runs once when the level is loaded (`engines/kyra/engine/scene_lol.cpp:69`); `LEVELn.INF` holds the level's event functions (`:78`).

**Edition read:** CD (31 INF, 29 INI). LANDSoL: same counts.

## Container

IFF `FORM` with type `EMC2`; chunks `TEXT` (optional strings), `ORDR` (function start table), `DATA` (16-bit code words). CONFIRMED: all 60 CD files start `FORM`, bytes 8-11 `EMC2`. Loader: `EMCInterpreter::load` / `callback` `engines/kyra/script/script.cpp:61-146`.

## Full documentation

- [`../emc2_scripts.md`](../emc2_scripts.md): container details (the FORM length includes the 8 header bytes; ORDR word indexes and entry headers; TEXT offsets), the 19 VM opcodes and 18 `eval` operators, the full 192-entry LoL1 function table with call counts per edition and the native handler addresses, and where each script sits in its PAK.
- [`../executable_tables.md`](../executable_tables.md): the 285 item definitions and 79 monster definitions are supplied by script calls (`ONETIME.INF`, level scripts), with their argument layouts.
- Disassembler: `tools/emc2_decompile.py`; test: `tests/test_emc2_corpus.py` (all 60 scripts of both editions disassemble with no unknown opcode or function).

## Open

- [Q8](../OPEN_QUESTIONS.md), mostly answered: the original executables keep their own function tables (192 far pointers at CD `MAIN.EXE+0x33F64`, 187 at floppy `MAIN.EXE+0x3D1EE`, entry 0x00-0xBA). Entry 0x7E points to a handler that takes no arguments, calls one engine routine and returns 1. CONFIRMED (disassembled). Its downstream effect is UNCONFIRMED.
- Apart from 0x7E, native handler bodies were not checked; function effects are ScummVM's (UNCONFIRMED for the original).
