# Q16 — Which 16-colour bank a DOS wall tile uses

**CONFIRMED** The bank is part of the VCN tileset. Each tile index has one stored shift byte. On the DOS VGA path, the renderer looks up the byte by the actual tile ID and ORs it with each of the tile's 4-bit pixel values. The result indexes a 128-entry table of VGA palette indices. The shift bytes are independent of the current lamp, brightness and replacement RGB palette.

| Step | CD `MAIN.EXE` | floppy `MAIN.EXE` |
| --- | --- | --- |
| Read tile count, skip the 2-byte header, copy exactly that many shift bytes, then advance to the colour table | `0x46561–0x465EC` | `0x4FD22–0x4FDAD` |
| Copy 64 words from the colour table into the drawing code's data | `0x1E80C–0x1E828` | `0x1F245–0x1F260` |
| Select RGB palette source and copy 384 bytes. The optional override applies here, after the shift and colour tables | `0x465EC–0x46622` | `0x4FDAD–0x4FDE3` |
| Pass the stored shift array to the scene rasterizer | `0x3EE8C–0x3EEA3` | `0x47FC7–0x47FDE` |
| Mask VMP mirror and overlay bits. Take the floor/ceiling tile for a zero base or overlay | `0x1E8DD–0x1E912` | `0x1F317–0x1F34C` |
| Fetch `shift[tile]`, OR with each nibble, look up the index, write the two pixels. Mirrored drawing reverses the pixel order | `0x1E912–0x1E9B2` | `0x1F34C–0x1F3EC` |
| For an overlay, fetch its own `shift[tile]`. Skip writes whose mapped palette index is zero | `0x1E9D3–0x1EA5A` | `0x1F40D–0x1F494` |

**CONFIRMED** ScummVM's VGA path implements this same choice. Its separate 16-colour platform path uses `_blockBrightness` when no VCN shift array is loaded. That fallback explains why the shared renderer also refers to brightness. See upstream `3b4db303`, `engines/kyra/engine/scene_lol.cpp:339–368`, `engines/kyra/engine/scene_rpg.cpp:347–430,444–461`, and `engines/kyra/engine/lol.cpp:1795–1823`.

## Worked example

**CONFIRMED** A read of all 13 VCN members in each edition yields 18,979 shift bytes per edition. The complete set of values is `00 10 20 30 40 50 60 70`. Dividing the stored byte by 16 gives the bank index, 0 through 7. For example, the compressed CD witnesses are `KEEP.PAK+0x9675` (VCN) and `+0xF8F4` (VMP). The corresponding floppy witnesses are `CHAPTER1.PAK+0xEEFB9` and `+0xFC6B4`. Their decompressed bytes agree on the following calculation.

- VMP word 330 at decoded offset `0x296` is `FA 00`, selecting wall tile 250.
- The shift at decoded VCN offset `2 + 250 = 0xFC` is `0x30`, bank 3. The first pixel byte at `514 + 1282 + 32 × 250 = 0x2644` is `0x33`.
- Either nibble produces lookup index `0x30 | 3 = 0x33`. The byte at decoded VCN offset `2 + 1282 + 0x33 = 0x537` is `0x64`, palette index 100.
- The next VMP word is `FB 80`, an overlay using tile 251 and its own stored shift. VMP word 0 selects floor tile 1, with shift `0x70`. Its first nibble is 1 and maps to palette index 98 through lookup index `0x71`.

**UNCONFIRMED** The original authoring procedure that assigned the shift bytes is open. The table inspection and executable trace establish where the renderer gets every bank. To identify whether an artist or a tool chose bank 3 for KEEP tile 250, the specific evidence needed is an original tileset source with that tile's bank metadata or an exporter that reproduces the shift table.

## Shift values in KEEP.VCN

**CONFIRMED** CD and floppy `KEEP.VCN` decompress to the same 42820-byte image: tile count 1282 (`02 05`), then the 1282-byte shift table. The only values in the table are the eight multiples of 16:

| Shift byte | Bank | Tiles |
| --- | --- | --- |
| 0 | 0 | 298 |
| 16 | 1 | 181 |
| 32 | 2 | 77 |
| 48 | 3 | 133 |
| 64 | 4 | 124 |
| 80 | 5 | 219 |
| 96 | 6 | 160 |
| 112 | 7 | 90 |

298 + 181 + 77 + 133 + 124 + 219 + 160 + 90 = 1282. The image size matches the layout: 2 + 1282 + 128 + 384 + 1282 times 32 = 42820.
