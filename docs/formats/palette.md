# PAL and COL palettes

**What:** raw VGA palettes: 256 colours x 3 bytes, 6-bit RGB (0..63), no header.

**Edition read:** CD `DATA/` (6 PAL, 5 COL), LANDSoL (11 PAL, 5 COL).

| File | Size (CD) | Loaded by |
|------|-----------|-----------|
| CAV_PLT2/3/4.PAL, ALTPAL1/2/3.PAL | 768 | as the override palette of `loadLevelGraphics` (first 384 bytes, `engines/kyra/engine/scene_lol.cpp:363-367`), name passed by the level script (`script/script_lol.cpp:208-212`). Which levels pass which file: UNCONFIRMED (Sol item 7 listing) |
| FXPAL.COL | 768 | transparency tables on floppy (`lol.cpp:1923`) |
| SWAMPICE.COL | 768 | level 11 ice palette (`scene_lol.cpp:375`, `lol.cpp:2486`) |
| LITEPAL1/2/3.COL | 768 | script function at `script/script_lol.cpp:2184-2215` (`olol_restoreMagicShroud`) |

Generic loader: `Screen::loadPalette` `engines/kyra/graphics/screen.cpp:3404-3447` (VGA: size / 3 colours).

All 11 CD files are 768 bytes. CONFIRMED (CD scan). CPS files carry their own 768-byte palette ([cps.md](cps.md)).

**Tool:** `tools/cps_reader.py NAME.CPS --png out.png --pal-from ALTPAL1.PAL`; `lol1lib.vga_palette()`.
