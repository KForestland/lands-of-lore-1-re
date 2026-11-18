# EMC2 level scripts (INF, INI)

**What:** compiled level scripts. `LEVELn.INI` runs once when the level is loaded (`engines/kyra/engine/scene_lol.cpp:69`); `LEVELn.INF` holds the level's event functions (`:78`).

**Edition read:** CD (31 INF, 29 INI). LANDSoL: same counts.

## Container

IFF `FORM` with type `EMC2`; chunks `TEXT` (optional strings), `ORDR` (function start table), `DATA` (16-bit code words). CONFIRMED: all 60 CD files start `FORM`, bytes 8-11 `EMC2`. Loader: `EMCInterpreter::load` / `callback` `engines/kyra/script/script.cpp:61-146`.

## Full documentation

Sol's lead-order items 7 and 8a (branch `sol/lol1-unknowns-20261118`, to be merged):

- [`../emc2_scripts.md`](../emc2_scripts.md) (f6d1469): container details (FORM length includes the 8 header bytes; ORDR word indexes and entry headers; TEXT offsets), the 19 VM opcodes and 18 `eval` operators, the full 192-entry LoL1 function table with call counts per edition, and corpus locations. Tool `tools/emc2_decompile.py`; test `tests/test_emc2_corpus.py` (CD 60/60, LANDSoL 60/60).
- [`../executable_tables.md`](../executable_tables.md) (df3b8e8): the 285 item definitions and 79 monster definitions come from script calls (`ONETIME.INF`, level scripts), with their argument layouts.

Opus review 2026-11-18 (independent decoder and checks): item 7 PASS with one text fix (the CD-only function IDs are 0xBA-0xBE, not 0xBB-0xBE); item 8a PASS.

## Open

- Native effect and arguments of function slot 0x7E (called once on CD, twice on LANDSoL; no handler in ScummVM).
- Native handler bodies were not checked; function effects are ScummVM's (UNCONFIRMED for the original).
