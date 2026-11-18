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

Two editions were read: the CD-ROM edition with spoken dialogue (version CD1.02) and an English floppy-edition installation (called LANDSoL in these pages). Details in [`docs/formats/README.md`](docs/formats/README.md).

- Containers (PAK), compression (Frame4/LCW), full-screen images (CPS), sprites (SHP), animations (WSA), sound (VOC), fonts, level tile sets (VCN/VMP), automap legends and decoration tables are documented, have readers, and are checked on every file of both editions. The CD-only speech archives (TLK) and transparency tables (TLC) are checked on every CD file.
- The level map pipeline `CMZ -> WLL -> VMP -> VCN` is documented and rendered by `tools/level_renderer.py`.
- Text (all three CD languages) and the level scripts' container are documented and checked.
- Still open: see [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md). Among them: the TIM sequence-script opcode table, the sound driver files, a few header bytes in level maps, when level 22 switches to its alternate tile set (YVEL2), music decoding, and the game rules (combat, magic, experience, monsters, light, time).

The closure memo [`docs/closure_memo.md`](docs/closure_memo.md) is a March 2026 summary written when this work was first declared finished. It is kept as history; its corrections are listed in `docs/STATUS.md`.

## Repository layout

- [`docs/formats/`](docs/formats/README.md) — one page per file format
- [`docs/`](docs) — status, edition comparison, level/tileset map, closure memo (history)
- [`tools/`](tools) — readers and extraction scripts
- [`data/`](data) — structured JSON outputs and inventories
- [`examples/`](examples) — a few public-safe output examples

## Start here

1. [`docs/STATUS.md`](docs/STATUS.md)
2. [`docs/formats/README.md`](docs/formats/README.md) and the pages it lists
3. [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md)
4. [`docs/edition_comparison.md`](docs/edition_comparison.md)
5. History: [`docs/closure_memo.md`](docs/closure_memo.md), [`docs/level_tileset_map.md`](docs/level_tileset_map.md) (March 2026; corrected in the format pages)

## Quick start

```bash
git clone https://github.com/KForestland/lands-of-lore-1-re.git
cd lands-of-lore-1-re
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export LOL1_DATA=/path/to/your/LOL1/DATA   # your own copy of the game
python3 tools/check_all.py                 # 21 checks, one line each; all pass on the CD edition
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

More tools (each with `--help` and `--check`): `level_renderer.py`, `shp_renderer.py`, `wsa_extract.py`, `decode_dialogue.py`, `extract_music.py`, `parse_tim.py`, `wll_parser.py`, `cmz_analyzer.py`, `tileset_mapper.py`, `tlk_verify.py`, `pak_indexer.py`. See [`tools/README.md`](tools/README.md).

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
