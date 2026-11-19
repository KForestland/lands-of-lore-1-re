# CPS full-screen images

**What:** 320x200 8-bit images (title screens, backgrounds, parchment, portraits sheet). Loaded with `Screen::loadBitmap`, which also loads CMZ, VCN and VMP.

**Edition read:** CD `DATA/` (85 files), CD `DATA/ENG` (60), floppy (112).

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
- floppy: `112 files, comp types {4: 112}, 112 with palette … 112/112`.

Only type 4 occurs in LoL1. No file read through this header uses type 1 or 3 in either edition: every CPS, CMZ, VCN and VMP member, and every SHP member with the same header, is type 4. CONFIRMED (scan of all PAK members, CD `DATA/`, `DATA/ENG` and floppy). Types 1 and 3 are handled by ScummVM's loader for other games; whether the DOS LoL1 loader accepts them is UNCONFIRMED and does not matter for the shipped data.


## Worked example

First 12 bytes of CD `PARCH.CPS` (the automap parchment):

```
79 31   04   00   00 fa 00 00   00 03   00 00 …
```

| Bytes | Meaning |
|-------|---------|
| `79 31` | 0x3179 = 12665 = file size − 2 |
| `04` | compression type 4 (Frame4) |
| `00` | unused |
| `00 fa 00 00` | uncompressed size 0xFA00 = 64000 = 320 x 200 |
| `00 03` | palette size 0x300 = 768 bytes, starting at byte 10 |

The pixel data starts at 10 + 768 = 778; [lcw.md](lcw.md) decodes its first bytes.

## Tool

`tools/cps_reader.py NAME.CPS [--png out.png]`, `--check`. Older: `tools/decode_frame4.py`.
