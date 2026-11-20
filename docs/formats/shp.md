# SHP sprite shapes

**What:** a table of small sprites: monsters, items, doors, portraits (`FACEnn.SHP`), spell effects, GUI pieces, and the wall decorations of each area (`AREA.SHP`, used through the `AREA.DAT` table, see [dat.md](dat.md)).

**Edition read:** CD `DATA/` (89 files, 3492 shapes), CD `DATA/ENG` (49 files, 1269 shapes), floppy (95 files, 3601 shapes).

## File layout

77 of the 89 CD files are wrapped in the CPS bitmap container ([cps.md](cps.md), Frame4); unwrap them first. The 12 area decoration files (`KEEP.SHP`, `CAVE1.SHP`, …; there is no `YVEL2.SHP`, level 22 uses `YVEL1.SHP`) are stored plain, because the engine reads them piece by piece from the file (`engines/kyra/engine/scene_lol.cpp:216-233`). CONFIRMED (`tools/shp_renderer.py --out`, field `wrapped_in_bitmap_container`).

After unwrapping:

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | number of shapes n |
| 2 | uint32 x n | shape offsets, **counted from byte 2**: shape i starts at offset[i] + 2 |
| 2 + 4n | uint32 | end entry (offset of the end of the last shape) |

Source: `Screen_v2::getPtrToShape` `engines/kyra/graphics/screen_v2.cpp:192-201` (`shpFile + offset + 2`); `getLevelDecorationShapes` `scene_lol.cpp:220-222` (same). CONFIRMED: `KEEP.SHP` has n = 78, the table ends at 0x13E, offset[0] = 0x13C, so shape 0 starts at 0x13E, right after the table.

## Shape layout

Source: `Screen::drawShape` `engines/kyra/graphics/screen.cpp:1805-1842`; the header writer `Screen::encodeShape` `:2833-2846` writes the same fields.

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | flags: bit 0 = colour table follows; bit 1 = line data is **not** Frame4-compressed; bit 2 = a colour-count byte precedes the colour table |
| 2 | uint8 | height |
| 3 | uint16 | width |
| 5 | uint8 | height again |
| 6 | uint16 | shape size in bytes |
| 8 | uint16 | frame size: length of the line data after decompression |
| 10 | [uint8] | colour count (default 16), only when bit 2 |
| … | [count bytes] | colour table, only when bit 0: pixel values are looked up in it |
| … | | line data (Frame4 unless bit 1) |

Line data (`screen.cpp:2095-2108`, `drawShapeProcessLineNoScaleUpwind`): each row is exactly `width` pixels. A nonzero byte is one pixel. A zero byte followed by n skips n transparent pixels.

## Confirmed

`tools/shp_renderer.py --check` decodes every shape strictly: every row fills its width exactly, the line data is exactly the frame size, and the two height bytes agree.

- CD `DATA/`: 3492/3492 shapes. CD `DATA/ENG`: 1269/1269. floppy: 3601/3601. CONFIRMED.
- Negative control: with `--alt-header` (a 2-byte prefix before each header) no CD file decodes: most stop with a read past the end of their data, and of the 197 shapes that can be read at all, none decodes. CONFIRMED.

## Correction to the closure memo: no 2-byte prefix on CD or floppy

The closure memo (sections A and B.6) says shapes have a 12-byte header that starts with a 2-byte prefix. That came from the March 2026 renderer, which took the shape offsets as counted from the start of the file, not from byte 2. It therefore read each shape 2 bytes early. For shape 0 those 2 bytes are the high half of the table's end entry; for later shapes they are the last 2 bytes of the previous shape. The real header is the 10-byte one above.

**CONFIRMED.** Independent byte reads of `FOREST1.SHP`, `GUARD.SHP` and `ITEMICN.SHP` show the 10-byte header in both retail editions, two bytes after the stored shape offset. ScummVM selects the extra two-byte prefix only for the non-CD demo definitions (`engines/kyra/detection_tables.h:63–64,1880–1905,1907–1919`; header skip at `engines/kyra/graphics/screen.cpp:1637–1638`). The interactive CD demo has the regular header flag. The original demo bytes remain **UNCONFIRMED**. The local retail `DEMOS` directory has Dune II, Hand of Fate and Kyrandia CD copies. An original LoL demo archive matching the detection rows at `detection_tables.h:1884–1885,1898,1911–1912` would settle the file comparison below. [Q1](../OPEN_QUESTIONS.md) · [Retail byte reads](../unknowns/01_shp_header.md)

## What a demo copy would show

No demo release was read for this page. A reader who has one can close the question with the files and the two commands below.

Point `--data` (or `$LOL1_DATA`) at that release's DATA folder. Every `.SHP` in the folder is in scope. Three names are enough when the demo has them, because this page already records their CD headers: `FOREST1.SHP` (a raw offset table), `GUARD.SHP` (a bitmap whose image is the table), and `ITEMICN.SHP` (the same kind of bitmap). For each, read shape 0, the middle shape, and the last shape. `KEEP.SHP` is the worked example above: shape 0 is the 10 bytes at stored offset + 2.

Run both commands. They write nothing.

```
python3 tools/shp_renderer.py --data <demo DATA> --check
python3 tools/shp_renderer.py --data <demo DATA> --check --alt-header
```

`--alt-header` reads two bytes and then the 10-byte record. The demo uses that prefix when the second command prints `bad=none` and the first command does not. The demo uses the same 10-byte header as the CD when the first command prints `bad=none` and the second command does not. If both commands pass, or both fail, lay the three shapes' first 12 bytes next to the CD bytes on this page. The prefix is present when those 12 bytes are two bytes followed by flags, height, width, and the same height again.

The closure memo's "3492/3492 frames" count was right in number, but the March 2026 tool reached it with fallbacks that accept any bytes. The strict decode above is what confirms it.

## Colours

Monster and item shapes are drawn through the scene palette plus run-time colour tables (`sprites_lol.cpp:908-980`). Their colour table points into the 3D scene palette of the level that loads them, so render them with `--level N` (the level's VCN palette, or the override `.PAL` its script names); a fixed CPS palette gives the right shapes in the wrong colours. Example: `shp_renderer.py GUARD.SHP --level 1` (`LEVEL1.INI` loads `GUARD.SHP`).


## Worked example

CD `KEEP.SHP` (plain, not wrapped). First 10 bytes: `4e 00  3c 01 00 00  bf 05 00 00`: 0x4E = 78 shapes; shape 0 offset 0x13C, shape 1 offset 0x5BF. Shape 0 therefore starts at 0x13C + 2 = 0x13E:

```
01 00   4f   21 00   4f   83 04   f6 09   …
```

| Bytes | Meaning |
|-------|---------|
| `01 00` | flags 1: a 16-byte colour table follows the header; bit 1 clear, so the line data is Frame4-compressed |
| `4f` | height 79 |
| `21 00` | width 33 |
| `4f` | height again (79) |
| `83 04` | shape size 0x483 = 1155 bytes |
| `f6 09` | line data is 0x9F6 = 2550 bytes after decompression |

## Tool

`tools/shp_renderer.py NAME.SHP [--out-dir pngs/] [--pal-from X.CPS]`, `--check`, `--out inventory.json`. Inventory: `data/shp_inventory.json`. `tools/lol1_compression_writer.py --check` re-encodes every SHP shape (CD 7299, floppy 3601) in memory and reads it back through this reader with identical pixels; the rebuilt bytes differ from the original, so this is not the original encoder (see [tools/README](../../tools/README.md#lol1_compression_writerpy)).

## Close-out

**What was measured.** `ENG/FINALE1.PAK` holds one shape file named `DOOR.SHP` (657 bytes, one shape). Its unwrapped image header at offset `0x0A` is the ten bytes `00 00 2c 30 00 2c 76 02 40 08` (flags 0, height 44, width 48, the same height again, size 630, frame 2112), and that shape decodes from those ten bytes; the same record read two bytes later does not, because the two height bytes are `00` and `02`.

**What was tried.** The scan unwrapped that member and checked the ten-byte record against the record two bytes later. The page already compared `FOREST1.SHP`, `GUARD.SHP` and `ITEMICN.SHP` on the CD and the floppy, and did not read a demo DATA folder.

**What would settle it.** On a demo DATA folder, `shp_renderer.py --check` once plain and once with `--alt-header` would settle it. `FOREST1.SHP`, `GUARD.SHP` and `ITEMICN.SHP` (shapes 0, middle and last) cover a copy that does not hold every file; no demo copy was read here.
