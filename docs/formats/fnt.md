# FNT fonts

**What:** Westwood DOS bitmap fonts.

**Edition read:** CD `DATA/` (4: FONT6P, FONT9P in STARTUP.PAK; FONT6PN, FONT9PN in GENERAL.PAK), CD `DATA/ENG` (7, adds NEW6P, NEW8P, INTRO), LANDSoL (9).

## Layout

Source: `DOSFont::load` `engines/kyra/graphics/screen.cpp:3678-3706`; `DOSFont::drawChar` `:3714-3760`.

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 | file size |
| 2 | uint16 | signature 0x0500 |
| 4 | uint16 | descriptor offset D |
| 6 | uint16 | offset of glyph bitmap offsets (uint16 per glyph) |
| 8 | uint16 | offset of width table (uint8 per glyph) |
| 12 | uint16 | offset of height table (2 bytes per glyph: blank rows on top, drawn rows) |
| D+3 | uint8 | last glyph index (glyphs = value + 1) |
| D+4 | uint8 | font height |
| D+5 | uint8 | max width |

Glyph bitmap: 4 bits per pixel, low nibble = left pixel, ceil(width/2) bytes per row. Bitmap offset 0 = glyph not drawn.

Use: FONT9P/FONT6P are the normal fonts (`engines/kyra/engine/lol.cpp:598-599`, `:4232-4233`); FONT9PN/FONT6PN while the automap is open (`:4176-4177`).

## Confirmed

`tools/fnt_reader.py --check`:
- CD: `FONT6PN 226 glyphs 172 drawn h6; FONT9PN 226/172 h9; FONT6P 226/172 h6; FONT9P 226/172 h9, bad=none` (size field = file size, every glyph inside the file and inside the font height).
- CD ENG: adds `INTRO.FNT 174 glyphs 170 drawn h19; NEW6P.FNT 226/172 h8; NEW8P.FNT 226/172 h11`.
- LANDSoL: FONT6P, FONT9P, FONT9PN have **128 glyphs** (all drawn); FONT6PN 226. Edition difference CONFIRMED.

The memo's "226 glyphs per font, 172 with bitmaps" holds for the CD fonts only.

## Tool

`tools/fnt_reader.py FONT9P.FNT [--png atlas.png]`, `--check`.
