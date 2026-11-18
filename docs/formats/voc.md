# VOC sound samples

**What:** Creative Voice File, 8-bit unsigned mono PCM. Sound effects (`VOC.PAK`, level PAKs), intro speech (`INTROVOC.PAK`), and every CD speech sample inside `NN.TLK` ([tlk.md](tlk.md)).

**Edition read:** CD (`DATA/`, `DATA/ENG`), LANDSoL.

## Layout

Source: ScummVM `audio/decoders/voc.h:55-60` (header), `audio/decoders/voc.cpp:38-62` (header check), `:255-300` (blocks), `:459-471` (rate). Kyra opens VOC through `engines/kyra/sound/sound.cpp:338-347`.

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | char[19] + 0x1A | `Creative Voice File` |
| 20 | uint16 | offset of first block (26) |
| 22 | uint16 | version |
| 24 | uint16 | check = ~version + 0x1234 |
| 26 | blocks | uint8 type, uint24 length, payload; type 0 = end |

Block type 1 = sound data: uint8 rate divisor, uint8 codec (0 = 8-bit PCM), samples. Rate = 1000000 / (256 − divisor); ScummVM rounds divisor 0xA5/0xA6 to 11025 Hz and 0xD2/0xD3 to 22050 Hz.

## Confirmed

CONFIRMED, `tools/voc_reader.py --check`:
- CD `DATA/`: `215 in PAKs + 4912 in TLKs, block types {1: 11349}, rates {22050: 4908, 11025: 206, 5494: 10, 8196: 1, 11904: 1, 8000: 1}, bad=none`.
- CD `DATA/ENG`: `127 in PAKs, block types {1: 418}, rates {22050: 118, 11025: 7, 11904: 1, 16129: 1}`.
- LANDSoL: `277 in PAKs, block types {1: 277}, rates {11025: 194, 22050: 68, 5494: 10, …}`.

Only block type 1 occurs; every file passes the header check value.

**Correction to the memo:** "majority 11111 Hz" — the majority divisor is the 11025 Hz class (0xA5/0xA6) for effects and the 22050 Hz class for CD speech. The memo's figure is the raw formula for divisor 0xA6 (1000000/90 = 11111). Both are the same files; the label differs.

## Tool

`tools/voc_reader.py [CONTAINER:]MEMBER [--wav out.wav]`, `--check`.
