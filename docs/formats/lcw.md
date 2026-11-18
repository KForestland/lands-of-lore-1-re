# Frame4 / LCW compression ("format 80")

**What:** the byte-oriented LZ used by CPS, CMZ, VCN, VMP (compression type 4 in the 10-byte bitmap header, see [cps.md](cps.md)), by WSA frames and by compressed SHP frames.

**Source:** `engines/kyra/graphics/screen.cpp:2484-2530` (`Screen::decodeFrame4`).

| Code byte | Meaning |
|-----------|---------|
| `0ccc oooo` + 1 byte | copy `ccc + 3` bytes from `out_pos - offset` (12-bit offset, **relative**) |
| `10cc cccc`, c != 0 | copy the next `c` bytes from the input |
| `1000 0000` (0x80) | end |
| `11cc cccc`, c < 0x3E | copy `c + 3` bytes from absolute offset `uint16` (from start of output) |
| `0xFE` + uint16 n + byte v | write `v` n times |
| `0xFF` + uint16 n + uint16 o | copy n bytes from absolute offset `o` |

There is no mode flag: short copies are always relative, medium and long always absolute. CONFIRMED in code (lines above) and on data: every CPS, CMZ, VCN and VMP in the CD and floppy corpora decodes to exactly the size in its header (`cps_reader.py --check` 85/85 CD, 60/60 ENG, 112/112 floppy; `vcn_vmp_reader.py --check` 13/13 both; CMZ 29/29 with `lol1lib.load_bitmap`).

**Correction history:** the closure memo (section B.4) records the earlier decoder bug (relative/absolute mixed up), fixed in `tools/decode_frame4.py`.


## Worked example

The pixel data of CD `PARCH.CPS` (after its 10-byte header and 768-byte palette) starts:

```
81 40   00 01   82 3b 3e   10 06 …
```

| Code | Meaning | Output so far |
|------|---------|---------------|
| `81` + `40` | 0x80 + 1: copy 1 literal byte | `40` |
| `00 01` | bit 7 clear: copy (0 >> 4) + 3 = 3 bytes from 1 byte back (relative) | `40 40 40 40` |
| `82` + `3b 3e` | copy 2 literal bytes | `40 40 40 40 3b 3e` |
| `10 06` | copy (1) + 3 = 4 bytes from 6 bytes back | `40 40 40 40 3b 3e 40 40 40 40` |

**Tool:** `tools/lol1lib.py: decode_frame4()` (port of the function above); `tools/decode_frame4.py` (the March 2026 port; `--check` runs both ports on all 140 CPS, CMZ, VCN and VMP files of the CD: identical output, 140/140).
