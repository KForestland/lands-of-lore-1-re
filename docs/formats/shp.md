# SHP sprite shapes

**What:** a table of small sprites: monsters, items, doors, portraits (`FACEnn.SHP`), spell effects, GUI pieces, and the wall decorations of each area (`AREA.SHP`, used through the `AREA.DAT` table, see [dat.md](dat.md)).

**Edition read:** CD `DATA/` (89 files, 3492 shapes), CD `DATA/ENG` (49 files, 1269 shapes), LANDSoL (95 files, 3601 shapes).

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

- CD `DATA/`: 3492/3492 shapes. CD `DATA/ENG`: 1269/1269. LANDSoL: 3601/3601. CONFIRMED.
- Negative control: with `--alt-header` (a 2-byte prefix before each header) no CD file decodes: most stop with a read past the end of their data, and of the 197 shapes that can be read at all, none decodes. CONFIRMED.

## Correction to the closure memo: no 2-byte prefix on CD or LANDSoL

The closure memo (sections A and B.6) says shapes have a 12-byte header that starts with a 2-byte prefix. That came from the March 2026 renderer, which took the shape offsets as counted from the start of the file, not from byte 2. It therefore read each shape 2 bytes early. For shape 0 those 2 bytes are the high half of the table's end entry; for later shapes they are the last 2 bytes of the previous shape. The real header is the 10-byte one above.

This agrees with ScummVM: the 2-byte prefix (`GameFlags::useAltShapeHeader`, `engines/kyra/detection.h:51`; skipped in `screen.cpp:1637-1638`) is set only for the LoL demo (`engines/kyra/detection_tables.h:63`), not for CD (`:56`) or floppy (`:58`). The demo itself was not read. Byte dumps per edition, including the demo, are [Q1](../OPEN_QUESTIONS.md).

The closure memo's "3492/3492 frames" count was right in number, but the March 2026 tool reached it with fallbacks that accept any bytes. The strict decode above is what confirms it.

## Colours

Monster and item shapes are drawn through the scene palette plus run-time colour tables (`sprites_lol.cpp:908-980`), so a PNG made with a fixed CPS palette shows the right shapes in the wrong colours.

## Tool

`tools/shp_renderer.py NAME.SHP [--out-dir pngs/] [--pal-from X.CPS]`, `--check`, `--out inventory.json`. Inventory: `data/shp_inventory.json`.
