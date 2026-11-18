# EMC2 level scripts (INF, INI)

**What:** compiled level scripts. `LEVELn.INI` runs once when the level is loaded (`engines/kyra/engine/scene_lol.cpp:69`); `LEVELn.INF` holds the level's event functions (`:78`).

**Edition read:** CD (31 INF, 29 INI). LANDSoL: same counts.

## Container

IFF `FORM` with type `EMC2`; chunks `TEXT` (optional strings), `ORDR` (function start table), `DATA` (16-bit code words). CONFIRMED: all 60 CD files start `FORM`, bytes 8-11 `EMC2`. Loader: `EMCInterpreter::load` / `callback` `engines/kyra/script/script.cpp:61-146`.

## Open — Sol item 7

The opcode table, the LoL1 function table (number, name, parameters, effect), the decompiler tool and the all-60 test are Sol's item 7 (`docs/emc2_scripts.md`, `tools/`). The closure memo's "19 VM opcodes + 192 game-specific opcodes, 60/60 decompiled" refers to an archived decompiler whose `.asm` string listings are garbled (lead order, sources). Sol's item 7 is READY on branch `sol/lol1-unknowns-20261118` (commit f6d1469: `docs/emc2_scripts.md`, `tools/emc2_decompile.py`, `tests/test_emc2_corpus.py`; CD 60/60, LANDSoL 60/60). Opus review 2026-11-18: PASS with one text fix (CD-only call IDs are 0xBA-0xBE). This page will point at `../emc2_scripts.md` once the branches are merged.
