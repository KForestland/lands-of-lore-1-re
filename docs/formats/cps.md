# CPS full-screen images

**What:** 320x200 8-bit images (title screens, backgrounds, parchment, portraits sheet). Loaded with `Screen::loadBitmap`, which also loads CMZ, VCN and VMP.

**Edition read:** CD `DATA/` (85 files), CD `DATA/ENG` (60), LANDSoL (112).

## Layout

Source: `engines/kyra/graphics/screen.cpp:3355-3401` (`Screen::loadBitmap`).

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | size field — not read by `loadBitmap`; on the data always file size − 2 (CONFIRMED) |
| 2 | uint8 | compression type: 0 raw, 1, 3, 4 = Frame4 ([lcw.md](lcw.md)) |
| 3 | uint8 | 0 on every CPS (CONFIRMED); not read |
| 4 | uint32 | uncompressed size (64000 for 320x200) |
| 8 | uint16 | palette size in bytes (0 or 768) |
| 10 | palSize bytes | 6-bit VGA RGB palette |
| 10+palSize | | pixel data |

## Confirmed

CONFIRMED, `tools/cps_reader.py --check`:
- CD: `85 files, comp types {4: 85}, 85 with palette, size_field+2==file size and full decode: 85/85`.
- CD ENG folder: `60 files, comp types {4: 60}, 60 with palette … 60/60`.
- LANDSoL: `112 files, comp types {4: 112}, 112 with palette … 112/112`.

Only type 4 occurs in LoL1. Types 1 and 3 are handled by the engine for other games (UNCONFIRMED for LoL1, never seen).

## Tool

`tools/cps_reader.py NAME.CPS [--png out.png]`, `--check`. Older: `tools/decode_frame4.py`.
