# Lands of Lore I RE

Reverse-engineering, extraction, and documentation for the DOS version of *Lands of Lore: The Throne of Chaos*.

This repository is the canonical public source of truth for the LoL1 lane of the broader project. It focuses on:

- format documentation
- extraction and analysis tools
- structured data outputs
- edition comparison notes

It does not aim to redistribute the original game data.

## Status

LoL1 is effectively closed at about `99.999%`.

Major results:

- `PAK` and `TLK` container formats solved and cross-checked against ScummVM
- full level rendering pipeline documented: `CMZ -> WLL -> VMP -> VCN`
- `CPS`, `SHP`, `WSA`, `VOC`, dialogue, music, palettes, automap legend, and wall definitions extracted or documented
- full `WSA` multi-frame extraction completed
- full `EMC2` script decompilation completed
- second edition witness (`LANDSoL`) compared against the main reference corpus

Remaining gaps are effectively publication-only:

- repo assembly and curation
- release artifact packaging
- README/wiki polish

## Repository Layout

- [`docs/`](docs) - closure memo, edition comparison, and supporting writeups
- [`tools/`](tools) - extraction and analysis scripts
- [`data/`](data) - structured JSON outputs and inventories

## Start Here

Read:

1. [`docs/closure_memo.md`](docs/closure_memo.md)
2. [`docs/edition_comparison.md`](docs/edition_comparison.md)
3. [`docs/level_tileset_map.md`](docs/level_tileset_map.md)

Then use:

- [`tools/decode_frame4.py`](tools/decode_frame4.py)
- [`tools/level_renderer.py`](tools/level_renderer.py)
- [`tools/shp_renderer.py`](tools/shp_renderer.py)

## Asset Policy

This repo intentionally avoids shipping a full dump of extracted copyrighted game assets.

Included:

- documentation
- scripts
- inventories
- structured analysis data

Not included in the initial public repo:

- full extracted image/audio corpora
- raw game files

Those can be handled separately as private artifacts, release attachments, or on request depending on legal and preservation goals.

## Provenance

The work here was cross-checked against ScummVM where useful, but the repository is independent project documentation, not an official ScummVM output.
