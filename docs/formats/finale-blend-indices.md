# Finale blend table inputs

## Which bytes the finale can address

**CONFIRMED.** In each of the three localized CD `FINALE.EXE` images,
nested TIM command 5 enters file `+0x7AD5`. The table pointer comes from
the second operand's TEXT name. `+0x7B9E–+0x7BAC` requests `0x10000`
bytes. The first operand supplies the picture name with `.CPS` added
at `+0x7C04–+0x7C34`. The latter call decodes the picture to page 5.
The source pointer is page 4 (`+0x7B0B–+0x7B1A`). The destination is
page 2 (`+0x7B1B`), first filled from page 0 by `+0x7BBB–+0x7BD6`.

**CONFIRMED.** Page 5 and page 4 are one buffer. The CPS loader asks the
page routine at English `+0x14C90` (`or bx, 1`) for page 5. The source
pointer comes from `+0x14CAA` (`and bx, 0xFFFE`) for page 4. Both read one
word table of page segments (`DS:0x22AB` in English, `0x29DD` French,
`0x2A37` German). Both allocator loops store one segment in the two words
of each even/odd page pair (English `+0x1AE8C–+0x1AEA1` and
`+0x1AF16–+0x1AF29`; French and German `+0x1AE56` and `+0x1AEE0`). The
loader (`+0x1A734`, then `+0x1A288`) reads the file into page 7. It
decompresses the pixels to offset 0 of page 5 and copies the palette to its
own buffer. It does not remap a pixel. Slot 5 also passes a 256-byte table
filled with 0 to 255 (`+0x7B4B–+0x7B62`) to the draw. The draw keeps that
pointer but its loop never reads it: `lgs bx, [bp-8]` at `+0xADDC` loads
the blend table, and that is the only table the loop reads.

| Edition | Slot 5 pointer in `FINALE.EXE` | Page mask entry | First lookup of a four-pixel group |
|---|---:|---:|---:|
| English | `+0x1E6C0` | `+0x14CAA` | `+0xADF2` |
| French | `+0x1EDC2` | `+0x14C74` | `+0xADBC` |
| German | `+0x1EE1C` | `+0x14C74` | `+0xADBC` |

**CONFIRMED.** The draw starts at file `+0xAC2A` (English) or `+0xABF4`
(French and German). The caller at `+0x7C78` sets both origins to zero
and passes a 320 × 200 rectangle. The draw takes BH from the source
byte and AL from the current destination byte, then reads
`table[(source << 8) | destination]` and stores the result to page 2.
The loop at `+0x7CB1` makes three passes without reloading either page
buffer. `+0x7C9B` copies page 2 to page 0 after each pass, and the loop
then only waits on the timer word `DS:0x2562`. Nothing in the loop
writes page 4: the draw stores to page 2 and the copy to page 0.
`+0x7CD2` copies the new picture on page 4 to page 0 after the final
pass. The high byte is always a pixel from the incoming CPS. A pixel
produced by a previous lookup can only change the low byte of a
subsequent lookup.

**CONFIRMED.** In all three language copies `FINALE2.PAK+0xC9D21`
starts the AVTL words of `LOLFINAL.TIM`. The nested slot 5 occurs at
exactly these four positions. The table gives English archive offsets
for the incoming pictures. The checked French and German images carry
the same decoded source colour sets.

| TIM word (archive offset) | Table | Incoming `FINALE1.PAK` picture | Source indices | Maximum |
|---|---|---|---:|---:|
| 382 (`+0xCA01D`) | `BLEND.TAB` | `RETURN.CPS+0` at `+0xB7313` | 113 | `0xB0` |
| 848 (`+0xCA3C1`) | `BLEND.TAB` | `RICHARDF.CPS+0` at `+0xBD178` | 93 | `0xEF` |
| 1818 (`+0xCAB55`) | `BLEND2.TAB` | `FACE.CPS+0` at `+0xA168D` | 161 | `0xEF` |
| 1968 (`+0xCAC81`) | `BLEND2.TAB` | `TAPPING.CPS+0` at `+0xC8782` | 102 | `0x6A` |

Each picture supplies all 64,000 source bytes. None contains palette
index `0xFF`. All addresses `0xFF00–0xFFFF`, including the four bytes
at `0xFFFC–0xFFFF`, need that source index. Their exclusion holds for
every destination byte, independently of captions and animation timing.

**CONFIRMED.** The rows each table can be indexed with are the union of
its pictures' colours. `BLEND.TAB` has 199 such rows and `BLEND2.TAB` 190,
none above `0xEF`. So at most 50,944 and 48,640 cells can be read, all
below `0xF000`, whatever the destination holds. The bound does not use the
destination model below.

## Floppy reader

**CONFIRMED.** The floppy `FINALE.EXE` ships the same two tables
(byte-identical to the CD files) and the same reader. The dispatcher at
`+0xB193` takes slot 5 from the table at `+0x261BE` to `+0x7BF1`. That
handler asks for page 4 at `+0x7C27` and page 2 at `+0x7C37` and requests
`0x10000` bytes at `+0x7CBA`. It loads the picture to page 5 at `+0x7D3E`
and calls the draw `+0xA529` at `+0x7D94`, three times (`+0x7DCD`). The
lookup at `+0xA6DB` is the same byte sequence. The page routines at
`+0x13E97` and `+0x13EB1` read the table at `DS:0x4639`, and the allocator
fills both words of a pair at `+0x1448E` and `+0x14518`. The floppy
`LOLFINAL.TIM` is a different file. Its four slot-5 calls are AVTL words
387, 853, 1649 and 1799, with the same four picture and table pairs. The
four floppy pictures decode to the same pixels as the CD ones. The check
models destinations on the CD only.

## Destination colours by pass

**CONFIRMED.** Each pass reuses its own output as the next destination.
The check below reconstructs the incoming destination page under the
stored TIM schedule and enumerates the lookups at matching pixel
coordinates. It uses the stored table for the first and second feedback
passes. It does not pair every distinct source colour with every
distinct destination colour.

| Incoming picture | Destination before the first pass | Distinct cell addresses per pass | Union across passes | Common to all modelled inputs |
|---|---|---:|---:|---:|
| `RETURN` | `DEATH.CPS` with `DEATH.WSA` through frame 56 and the applicable caption | 1,867 / 1,311 / 983 | 3,240 | 3,141 |
| `RICHARDF` | `RETURN.CPS` with `RETURN1.WSA` frame 63 and `RETURN2.WSA` frame 0, 1 or 2 | 2,563 / 1,799 / 1,285 | 4,465 | 4,433 |
| `FACE` | `EYE.CPS` | 3,275 / 2,209 / 1,602 | 4,887 | 4,887 |
| `TAPPING` | `FACE.CPS` with `BLINK.WSA` through frame 11 | 2,880 / 2,034 / 1,440 | 4,402 | 4,402 |

These cell counts depend on the modelled destinations. They are not the
proof that row `0xFF` is never read; the source rows above are.

- AVTL word 65 opens `DEATH` with flag `0x16`, and word 361 is its
  final frame command. English `FINALE.EXE+0x71E7–+0x7278` tests bit
  `0x04`, loads the companion CPS and sets up frame 0. `DEATH.CPS` and
  `DEATH.WSA` start at `ENG/FINALE1.PAK+0x926B7` and `+0x837B`.
  AVTL word 91 passes caption index 1 and `-1` to the text handler.
  English `+0x7D96–+0x7DA6` can skip the caption. French and German
  `+0x7D69–+0x7D84` select it directly. English `+0x7EDE–+0x7EFF`
  and the corresponding localized path at `+0x7EAA–+0x7EC9` draw
  left-aligned from `(0,0)` and step down by the font height minus 4.
  The glyphs in `FINALE2.PAK+0xC751D` select index `0xF2` on nibble 1,
  the other nibbles used by this caption leave the destination unchanged.
  The caption begins at archive `+0xCD256` in English, `+0xCD2A5`
  in French and `+0xCD27E` in German. The localized changes explain
  why the three input pages can differ.
- AVTL words 392 and 828 select `RETURN1.WSA` at `(136,84)` and draw
  through frame 63. Function 1 starts at word 2177, opens `RETURN2.WSA`
  at `(48,32)` and uses frames 0, 1, 2, 1. Word 833 stops that
  function before the second blend. The archive offsets of those WSAs
  are `ENG/FINALE1.PAK+0x62DE6` and `+0x76AA0`. Their rectangles
  remain disjoint after applying the header X/Y additions. The check
  enumerates three stopping images, frames 0, 1 and 2. Which frame the
  scheduler leaves on screen at word 833 is **UNCONFIRMED**, and so is
  whether `RETURN2` has drawn a frame by then. The union covers the three
  modelled images only; it is not an upper bound over every timing.
- AVTL word 1789 opens `EYE`, with no `EYE.WSA` in the shipped PAKs.
  English `+0x729E–+0x7330` tries the `.CPS` fallback, loads `EYE.CPS`
  at `ENG/FINALE1.PAK+0x96D02`, then copies the loaded picture to page 0.
  The intervening nested-8 handler at `+0x73CC–+0x7429` loads and
  applies a palette from page 3. English `+0x7A8E` is the resource
  release handler used by the intervening nested-7 instructions.
- AVTL word 1829 opens `BLINK.WSA` at `(0,0)` and word 1951 draws
  its last frame, 11. The WSA starts at `ENG/FINALE1.PAK+0x16A`,
  and its rectangle starts at the header's `(52,56)`.

**CONFIRMED.** The WSAs above omit the first frame (their first offset
at member `+0x0E` is zero). TIM flags `0x10` choose the direct page
path (`FINALE.EXE` English `+0x7086–+0x7098`, `+0x1B1B8–+0x1B1C9` and
`+0x9ACA–+0x9B05`). English `+0x1B5BF–+0x1B5D0` adds the WSA header
coordinates. `+0x1B62C–+0x1B69E` preserves the destination on a missing
first frame, and `+0x1BBB2–+0x1BBEF` and `+0x105BA–+0x105C7` send the
later deltas through the rectangle XOR path. The reconstruction applies
the cumulative XOR to those rectangles. For a worked example, the top
left pixel of `FACE.CPS` is `0x21` and that of `EYE.CPS` is `0x3F`.
The three reads are `BLEND2.TAB+0x213F`, `+0x2194` and `+0x21C4`.

Run the structure and byte-set check with:

```sh
python3 tools/lol1_blend_indices.py --data DATA --check
python3 tools/lol1_blend_indices.py --data DATA --indices
```

`--indices` prints the source colour ranges and the three destination
colour sets for each call, and the complete candidate address ranges
per table. The check pins the bit sets themselves as well as their
sizes. Over all modelled inputs the union is 7,696 cells of `BLEND.TAB`
and 7,876 of `BLEND2.TAB`. All are below `0xFF00`. On the floppy the
check pins the reader and the source rows. It fails if a source picture
holds colour 255.

## Rating

**CONFIRMED.** The six CD blend files count as read under the general rule of
[how we rate](../HOW_WE_RATE.md). Each is one 256 × 256 byte table, read whole
and addressed as `256 × source + destination`. The palette self-blend
reproduces bytes 0 to 65531, which hold every cell a shipped call can index.
The four bytes at `0xFFFC–0xFFFF` are stored in row `0xFF`, which no call can
index. **UNCONFIRMED:** the original writer and its reason for those four
values remain open ([loose files](loose.md)).

This is wrong if any of these is found:

- a program that reads a blend table with another extent or index;
- a shipped slot-5 call whose source can hold colour 255 (another picture,
  a remap of the source byte, or a write to page 4 before the last pass);
- a reachable cell that differs from the self-blend.

The first would undo the count. The other two would undo the reachable-value
claim. Finding the writer would settle where the four values come from.
