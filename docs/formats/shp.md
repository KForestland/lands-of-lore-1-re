# SHP sprite shapes

**What:** shape files: monsters, items, decorations (`AREA.SHP`, read through the `AREA.DAT` table), portraits (`FACEnn.SHP`), GUI. A file is a table of shapes; each shape is a small header plus line-encoded pixels, optionally Frame4-compressed.

**Edition read:** CD (89 files in `DATA/`, 49 per language folder); LANDSoL (95).

## File layout

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | number of shapes n |
| 2 | uint32 x n | shape offsets, relative to byte 2 |

Source: `engines/kyra/engine/scene_lol.cpp:216-233` (`getLevelDecorationShapes`: seek `index*4 + 2`, read uint32, `+ 2`). CONFIRMED in code; on the data `KEEP.SHP` starts `4e 00` (78 shapes) then `3c 01 00 00 …`. CONFIRMED (byte dump, CD).

## Shape header — OPEN, see Grok item 1

The closure memo (section A and B.6) says the LoL shape header is 12 bytes with a 2-byte prefix ("alt shape header"). ScummVM's own flags say otherwise for the full game:

- `GameFlags::useAltShapeHeader` "alternative shape header (uses 2 bytes more, those are unused though)" — `engines/kyra/detection.h:51`.
- `Screen::drawShape` skips 2 bytes only when that flag is set — `engines/kyra/graphics/screen.cpp:1637-1638`; same for `getShapeSize` and friends at `:2834-2961`.
- The flag is set only by `LOL_DEMO_FLAGS` (`engines/kyra/detection_tables.h:63`); `LOL_CD_FLAGS` (`:56`) and `LOL_FLOPPY_FLAGS` (`:58`) leave it false.

So by the code, CD and floppy shapes have **no** 2-byte prefix and only the demo has it. UNCONFIRMED on the data: Grok's item 1 (byte dumps of three shapes per edition) settles it. `tools/shp_renderer.py` renders 3492/3492 frames (memo) with its own header model; how it handles the prefix is part of that review.

Remaining header fields (after any prefix), from `Screen::drawShape` `screen.cpp:1640ff`: byte 0 flags (bit 0 = compact/compressed, bit 1 = has colour table), height, width (uint16), height again, shape size, uncompressed size. UNCONFIRMED until item 1 lands.

## Tool

`tools/shp_renderer.py` (needs path edits, see STATUS).
