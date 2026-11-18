# WSA animations

**What:** Westwood Screen Animation (v2): a delta-coded frame sequence, used for scenes, cut-ins, TIM sequences.

**Edition read:** CD `DATA/` (241 files), `DATA/ENG` (96), LANDSoL (254).

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
| 14 | uint32 x (frames + 2) | frame offsets; if the first is 0 there is no first frame |
| … | 768 bytes | palette, when flags bit 0 |
| … | | frames: Frame4 data that decodes to a delta stream, applied with `Screen::decodeFrameDelta` (XOR when decoding off-screen, the default) — `wsamovie.cpp:133-155`, `screen.cpp:2533-2594` |

## Confirmed

- Flags on the CD data: 219 files flags 0, 22 files flags 1 (palette); none has bit 1. CONFIRMED (header scan with `tools/lol1lib.py`, CD `DATA/`).
- Memo: 241/241 files and 4480/4480 frames decoded by `tools/wsa_all_frames_extract.py` after the palette fix for ESCAPE.WSA and CHANDELR.WSA. UNCONFIRMED in this pass (the tool needs path edits before it runs here, see STATUS).

## Tool

`tools/wsa_extract.py`, `tools/wsa_all_frames_extract.py`.
