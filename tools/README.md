# Tools

Public extraction and analysis helpers for LoL1 reverse engineering.

## Setup

- Python 3.8+
- Pillow (`pip install Pillow`) for render and image-output tools

## Tool Index

### Containers and Core Parsing
- `pak_indexer.py` — build structured indexes for `PAK` container contents
  - example: `python3 tools/pak_indexer.py --help`
- `tlk_verify.py` — verify and inspect `TLK` dialogue/container assumptions
  - example: `python3 tools/tlk_verify.py --help`
- `wll_parser.py` — parse wall definition/layout data
  - example: `python3 tools/wll_parser.py --help`
- `parse_tim.py` — parse TIM-related data structures used in the pipeline
  - example: `python3 tools/parse_tim.py --help`
- `cmz_analyzer.py` — inspect `CMZ` level-side content
  - example: `python3 tools/cmz_analyzer.py --help`

### Rendering and Visual Output
- `level_renderer.py` — render level-side outputs from the solved map pipeline
  - example: `python3 tools/level_renderer.py --help`
- `shp_renderer.py` — render `SHP` sprite outputs
  - example: `python3 tools/shp_renderer.py --help`
- `decode_frame4.py` — decode the relevant image/frame path used in the repo notes
  - example: `python3 tools/decode_frame4.py --help`

### Dialogue, Audio, and Animation
- `decode_dialogue.py` — inspect/decode dialogue-side content
  - example: `python3 tools/decode_dialogue.py --help`
- `extract_dialogue.py` — extract dialogue outputs
  - example: `python3 tools/extract_dialogue.py --help`
- `extract_music.py` — extract music outputs
  - example: `python3 tools/extract_music.py --help`
- `wsa_extract.py` — extract `WSA` animation outputs
  - example: `python3 tools/wsa_extract.py --help`
- `wsa_all_frames_extract.py` — multi-frame `WSA` extraction
  - example: `python3 tools/wsa_all_frames_extract.py --help`

### Mapping and Analysis
- `tileset_mapper.py` — map level tilesets and related outputs
  - example: `python3 tools/tileset_mapper.py --help`

### Format readers (added 2026-11-18)

Each takes `--data <DATA folder>` (default `$LOL1_DATA`), prints `--help`, and has a `--check` that parses every file of its kind and prints one line. Format pages: [`../docs/formats/`](../docs/formats/README.md).

- `lol1lib.py` — shared PAK/TLK listing, Frame4 (LCW), bitmap header, palette helpers
- `pak_reader.py` — list/extract PAK and CD `NN.TLK` members
- `cps_reader.py` — CPS header, decode, optional PNG
- `voc_reader.py` — VOC blocks/rate, optional WAV (PAK and TLK members)
- `fnt_reader.py` — DOS font header and glyphs, optional atlas PNG
- `xxx_reader.py` — automap legend records
- `dat_reader.py` — area decoration records
- `tlc_reader.py` — CD transparency tables
- `vcn_vmp_reader.py` — wall tile set and layouts, optional tile atlas PNG
- `check_all.py` — run every `--check`; exit 0 when all pass

Known issue with the older tools above: most import modules that are not in the repo (`lol1_decompress_lcw`, `lol1_decode_frame4`) or read fixed paths under `/home/bob`, and `pak_indexer.py` / `tlk_verify.py` ignore `--help` and run (writing their outputs). See `docs/STATUS.md`.

Working rule:

- keep the public tool surface smaller and cleaner than the full private workspace
