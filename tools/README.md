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

Working rule:

- keep the public tool surface smaller and cleaner than the full private workspace
