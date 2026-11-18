# WSA animations

**What:** Westwood Screen Animation (v2): a delta-coded frame sequence, used for scenes, cut-ins, TIM sequences.

**Edition read:** CD `DATA/` (241 files), `DATA/ENG` (96), floppy (254).

## Layout

Source: `engines/kyra/graphics/wsamovie.cpp:361-440` (`WSAMovie_v2::open`).

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | frame count (bit 15: unhandled flag, warning in ScummVM) |
| 2 | int16 | x add (drawing offset) |
| 4 | int16 | y add |
| 6 | uint16 | width |
| 8 | uint16 | height |
| 10 | uint16 | delta buffer size |
| 12 | uint16 | flags: bit 0 = 768-byte palette present, bit 1 = XOR / 16-colour palette |
| 14 | uint32 x (frames + 2) | frame offsets. Frame i starts at (start of frame data) + offset[i] − offset[0], `wsamovie.cpp:418-433`. If offset[0] is 0 there is no first frame and offset[1] is the base |
| … | 768 bytes | palette, when flags bit 0 |
| … | | frames: Frame4 data that decodes to a delta stream, applied with `Screen::decodeFrameDelta` (XOR when decoding off-screen, the default) — `wsamovie.cpp:133-155`, `screen.cpp:2533-2594` |

## Confirmed

- Flags on the CD data: 219 files flags 0, 22 files flags 1 (palette); none has bit 1. CONFIRMED (header scan).
- Every frame of every file decodes, and every delta stream ends at its terminator inside width x height: CD 4480/4480 frames in 241 files, CD `DATA/ENG` 2699 in 96, floppy 5227 in 254. CONFIRMED (`tools/wsa_extract.py --check`).
- offset[0] equals the start of the frame data in 219 of 241 CD files. In the other 22 (exactly the files with a palette) the offsets do not count the 768 palette bytes, which is why they must be taken relative to offset[0]. CONFIRMED. This explains the closure memo's special "palette fix" for ESCAPE.WSA and CHANDELR.WSA (section D.1): with the offsets read as ScummVM reads them, no per-file fix is needed.
- No CD file lacks a first frame. CONFIRMED.
- `data/wsa_inventory.json` (March 2026): its header fields match this parser for all 241 files. CONFIRMED.


## Worked example

First 30 bytes of CD `ESCAPE.WSA` (29,544 bytes):

```
33 00  04 00  00 00  88 00  68 00  43 07  01 00   e2 00 00 00  84 03 00 00  8c 03 00 00  f4 03 …
```

| Bytes | Meaning |
|-------|---------|
| `33 00` | 51 frames |
| `04 00`, `00 00` | draw at x + 4, y + 0 |
| `88 00`, `68 00` | 136 x 104 pixels |
| `43 07` | delta buffer 1859 bytes |
| `01 00` | flags 1: a 768-byte palette follows the offset table |
| `e2 00 00 00` | offset[0] = 226 = 14 + 4 x 53, the end of the table: it does not count the palette |
| `84 03 00 00` … | offset[1] = 900. Frame 1 starts at (226 + 768) + (900 − 226) = 1668 |

## Tool

`tools/wsa_extract.py NAME.WSA [--out-dir d/ --all]`, `--check`; `tools/wsa_all_frames_extract.py --out-dir d/` for every file.
