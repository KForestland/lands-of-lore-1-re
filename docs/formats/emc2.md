# EMC2 level scripts (INF, INI)

**What:** compiled level scripts. `LEVELn.INI` runs once when the level is loaded (`engines/kyra/engine/scene_lol.cpp:69`); `LEVELn.INF` holds the level's event functions (`:78`).

**Edition read:** CD (31 INF, 29 INI). LANDSoL: same counts.

## Container

IFF `FORM` with type `EMC2`; chunks `TEXT` (optional strings), `ORDR` (function start table), `DATA` (16-bit code words). CONFIRMED: all 60 CD files start `FORM`, bytes 8-11 `EMC2`. Loader: `EMCInterpreter::load` / `callback` `engines/kyra/script/script.cpp:61-146`.

## Full documentation

The detailed pages are being added in the same pass and are not in this checkout yet:

- `docs/emc2_scripts.md`: container details (the FORM length includes the 8 header bytes; ORDR word indexes and entry headers; TEXT offsets), the 19 VM opcodes and 18 `eval` operators, the full 192-entry LoL1 function table with call counts per edition, and where each script sits in its PAK. With a disassembler `tools/emc2_decompile.py` and a test that disassembles all 60 scripts of both editions.
- `docs/executable_tables.md`: the 285 item definitions and 79 monster definitions are supplied by script calls (`ONETIME.INF`, level scripts); argument layouts.

Their content was re-checked against the data with an independent decoder (function table vs ScummVM's 192-entry dispatch table, call counts, item and monster argument counts, the four item rows that differ between editions).

## Open

- [Q8](../OPEN_QUESTIONS.md): native effect and arguments of function 0x7E (called once on CD, twice on floppy; no handler in ScummVM).
- Native handler bodies were not checked; function effects are ScummVM's (UNCONFIRMED for the original).
