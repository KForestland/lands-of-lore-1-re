# Tools

Readers and extractors for the *Lands of Lore: The Throne of Chaos* (DOS) data files. Format documentation: [`../docs/formats/`](../docs/formats/README.md).

## Setup

- Python 3.8+
- Pillow (`pip install Pillow`) for the tools that write PNG files
- Your own copy of the game. Point the tools at its `DATA` folder with `--data /path/to/DATA` or `export LOL1_DATA=/path/to/DATA`.

## Common options

Every tool has `--help`, takes `--data`, and writes nothing unless you give it `--out` (a JSON file) or `--out-dir` (a folder). Every tool has a `--check` that reads all files of its kind and prints one line; exit code 0 means the check passed. `check_all.py` runs all 21 checks.

## Tool index

### Shared code and containers
- `lol1lib.py`: shared code: PAK/TLK listing, Frame4 (LCW) decompression, the 10-byte bitmap header, palette helpers
- `pak_reader.py`: list or extract members of a PAK (and of the CD speech `NN.TLK` files)
- `pak_indexer.py`: index of every PAK member (`data/pak_index.json`); `--survey` lists every file under the game folder
- `tlk_verify.py`: checks the CD speech archives `NN.TLK` (PAK archives of VOC samples)
- `decode_frame4.py`: an independent Frame4 port; `--check` compares it with `lol1lib`; `--out-dir` writes every CPS as PNG

### Images and animation
- `cps_reader.py`: CPS full-screen images (header, PNG)
- `shp_renderer.py`: SHP sprites (strict decode, PNG per shape, `--out` inventory as in `data/shp_inventory.json`)
- `wsa_extract.py`: WSA animations (header, frame 0 or every frame as PNG)
- `wsa_all_frames_extract.py`: every frame of every WSA (or of the named ones)
- `fnt_reader.py`: fonts (header, glyph atlas PNG)

### Levels
- `cmz_analyzer.py`: wall-type statistics of the level maps (`data/wall_type_analysis.json`)
- `wll_parser.py`: wall-type tables (`data/wll_parsed.json`)
- `vcn_vmp_reader.py`: wall tile sets and tile layouts (tile atlas PNG)
- `tileset_mapper.py`: which tile set, decorations and palette each level uses (`data/tileset_mapping.json`)
- `level_renderer.py`: top-down map PNG per level
- `xxx_reader.py`: automap legend records
- `dat_reader.py`: wall decoration records
- `tlc_reader.py`: CD transparency tables

### Text, sound, music, scripts
- `extract_dialogue.py`: raw strings of every text file (`data/dialogue_summary.json`)
- `decode_dialogue.py`: decoded, readable text, straight from the game data
- `voc_reader.py`: VOC sound samples (WAV output)
- `extract_music.py`: music file inventory (`data/music_inventory.json`), raw extraction
- `parse_tim.py`: TIM sequence-script chunk structure (`data/tim_analysis.json`)
- `check_all.py`: runs every `--check`

Where a `data/*.json` file is named, the tool's `--out` produces it and its `--check` compares with it.
