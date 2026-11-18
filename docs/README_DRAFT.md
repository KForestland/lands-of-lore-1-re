<!--
DRAFT for the owner (item 9e of LOL1_RE_ORDER_20261118). Not the live README.
If approved, this text replaces README.md. Changes against the current README:
  1. "Status" no longer claims ~99.999%; it points to docs/STATUS.md and states what is and is not done.
  2. The duplicate "Then read" list after Quick Start is removed; one reading order remains.
  3. "Start Here" points to docs/formats/ (one page per format) and STATUS.md before the March memo.
  4. Tool list names the readers that run as shipped; the older tools are flagged until the cleanup.
  5. Game data location: tools take --data or $LOL1_DATA instead of fixed paths.
  6. "Remaining gaps are publication-only" is removed (it was not true: see STATUS.md).
Everything else (scope, asset policy, provenance) is unchanged in meaning.
-->

# Lands of Lore I RE

Reverse-engineering and documentation of the DOS version of *Lands of Lore: The Throne of Chaos* (Westwood, 1993): how its data files and rules work.

This repository covers:

- file format documentation, one page per format
- reader and extraction tools
- structured data (inventories, parsed tables)
- notes comparing the CD edition with a second edition

It does not distribute the original game data.

## Status

See [`docs/STATUS.md`](docs/STATUS.md) for the per-format table: documented, reader tool, checked on the original data, and what is still open.

In short:

- Containers (PAK, CD speech TLK), compression (Frame4/LCW), images (CPS), sound (VOC), fonts, palettes, level tile sets (VCN/VMP), automap legends, decoration tables and transparency tables are documented, have readers, and are checked on every file of the CD edition and of a second edition.
- The level rendering pipeline `CMZ -> WLL -> VMP -> VCN` is documented.
- The level scripts (EMC2 INF/INI) have a disassembler and a full function table, checked on all 60 scripts of both editions.
- Open: the SHP header per edition, two CMZ header details, the YVEL2 tile set's use, the TIM opcode table, the sound driver files, and the game rules and executable tables (items, monsters, spells, combat, experience, save file).

The March 2026 closure memo is kept in [`docs/closure_memo.md`](docs/closure_memo.md) as history. Corrections to it are listed in `docs/STATUS.md`.

## Repository layout

- [`docs/formats/`](docs/formats/README.md) — one page per file format
- [`docs/`](docs) — status, edition comparison, level/tileset map, closure memo (history)
- [`tools/`](tools) — readers and extraction scripts
- [`data/`](data) — structured JSON outputs and inventories
- [`examples/`](examples) — a few public-safe output examples

## Start here

1. [`docs/STATUS.md`](docs/STATUS.md)
2. [`docs/formats/README.md`](docs/formats/README.md)
3. [`docs/level_tileset_map.md`](docs/level_tileset_map.md)
4. [`docs/edition_comparison.md`](docs/edition_comparison.md)

## Quick start

```bash
git clone https://github.com/KForestland/lands-of-lore-1-re.git
cd lands-of-lore-1-re
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export LOL1_DATA=/path/to/your/LOL1/DATA   # your own copy of the game
python3 tools/check_all.py                 # one line per format, exit 0 when all pass
```

Readers (each has `--help` and `--check`):

```bash
python3 tools/pak_reader.py list GENERAL.PAK
python3 tools/cps_reader.py PARCH.CPS --png parch.png
python3 tools/vcn_vmp_reader.py KEEP --png keep_tiles.png
python3 tools/voc_reader.py 01.TLK:000_0.01 --wav line.wav
python3 tools/fnt_reader.py FONT9P.FNT --png font.png
python3 tools/xxx_reader.py LEVEL1.XXX
python3 tools/dat_reader.py KEEP.DAT
python3 tools/tlc_reader.py LEVEL01.TLC
```

The older tools in `tools/` (level renderer, SHP and WSA extractors, dialogue and music extractors) still expect the original workspace paths; see `docs/STATUS.md`. They are being cleaned up.

## Asset policy

This repo does not ship extracted copyrighted game assets.

Included:

- documentation
- scripts
- inventories
- structured analysis data

Not included:

- extracted image/audio corpora
- raw game files

You need your own copy of the game to run the tools.

## Provenance

Formats were cross-checked against the ScummVM Kyra engine source (file and line cited on each page) and against the original data. This is independent project documentation, not an official ScummVM output.
