# TIM sequence scripts

**What:** small scripts that run cut-ins and talking scenes: they start WSA animations, show dialogue, play sound, loop.

**Edition read:** CD (139 in `DATA/`, 6 per language folder), LANDSoL (147).

## Container

IFF `FORM` with type `AVFS`; chunks `TEXT` (strings) and `AVTL` (code, 16-bit words). CONFIRMED: all 139 CD files start `FORM`, bytes 8-11 `AVFS`. Loader: `TIMInterpreter::callback` / `load` `engines/kyra/script/script_tim.cpp:115-170`.

## Open

The full opcode table (number, name, parameters, effect, how many of the 139 scripts use each) is [Q6](../OPEN_QUESTIONS.md); this page will hold it. Sources: ScummVM `engines/kyra/script/script_tim.cpp` and `data/tim_analysis.json`.

**Tool:** `tools/parse_tim.py` (chunk structure; `--check` rebuilds the file list and statistics of `data/tim_analysis.json`: 139/139, chunks AVTL 139, TEXT 51).
