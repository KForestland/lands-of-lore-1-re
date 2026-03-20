# LoL1 Lane — Final Closure Memo

**Date:** 2026-03-20
**Scope:** LoL1 reverse-engineering and documentation only
**Status:** CLOSED at ~99.5%
**Publication:** Ready for GitHub/wiki coordination with Codex

---

## Extraction Summary

### Fully Extracted (100%)

| Asset Type | Files | Items Extracted | Output |
|-----------|-------|-----------------|--------|
| **PAK containers** | 81 | 1163 entries indexed | `lol1_pak_index.json` |
| **TLK containers** | 30 | Parsed + validated | — |
| **CPS images** | 85 | 85 PNG (320×200) | `lol1_cps_complete/` |
| **SHP sprites** | 89 | 3492 frames as PNG | `lol1_shp_rendered/` |
| **VOC audio** | 215 | 215 WAV files | `lol1_audio_complete/` |
| **CMZ level maps** | 29 | 29 rendered with VCN tiles | `lol1_levels_rendered/` |
| **VCN tile graphics** | 13 | All parsed (4bpp, 8×8 tiles) | — |
| **VMP tile mapping** | 13 | All parsed (431-entry pages) | — |
| **WLL wall defs** | 29 | All parsed (12-byte records) | `lol1_wll_parsed.json` |
| **XXX automap legend** | 29 | 73 legend entries decoded | — |
| **DAT decorations** | 12 | 72-byte LevelDecorationProperty | — |
| **XMI/C55/ADL/PCS music** | 67 | All extracted + inventoried | `lol1_music/` |
| **TLC color remap** | 29 | 21×256-byte remap tables | — |
| **PAL/COL palettes** | 11 | 768-byte VGA RGB | — |
| **Dialogue (raw)** | 90 | 6495 strings (3 languages) | `lol1_dialogue/` |
| **Dialogue (decoded)** | 90 | 6495 clean readable strings | `lol1_dialogue_decoded/` |
| **WSA first frames** | 241 | 241 PNG thumbnails | `lol1_wsa_frames/` |

### Mostly Extracted

| Asset Type | Files | Status | Output |
|-----------|-------|--------|--------|
| **WSA multi-frame** | 241 total | 239/241 fully sequenced (4426/~4480 frames, 98.8%); 2 failures: ESCAPE.WSA, CHANDELR.WSA (palette-offset edge case) | `lol1_wsa_all_frames/` |

### Documented / Identified

| Asset Type | Files | Status | Output |
|-----------|-------|--------|--------|
| **FNT fonts** | 4 | Glyph format decoded (DOSFont nibble-packed 4bpp); 4 atlas PNGs rendered | `lol1_fonts/` |
| **TIM timing scripts** | 139 | AVFS bytecode parsed; opcodes identified (WSA control, dialogue, audio, loops) | `lol1_tim_analysis.json` |
| **INF/INI scripts** | 60 | Identified as IFF FORM/EMC2 compiled bytecode; chunk structure known; bytecode not decompiled | — |
| **YVEL2.VCN** | 1 | Parsed: 1379 tiles at 4bpp + matching VMP (2054 entries). Variant of YVEL1 for Level 22 sub-area. | — |

**Total: 1163 files across 27 format types.**

---

## A. Fully Solved Formats

### Container Formats
- **PAK**: Sequential offset + null-terminated filename directory. ScummVM-validated.
- **TLK**: uint16 count + 8-byte entries (uint32 ID + uint32 offset). ScummVM-validated.

### Compression
- **Frame4/LCW**: Fully implemented per ScummVM `Screen::decodeFrame4()`.
  - Short back-refs: RELATIVE to current output position
  - Medium/large copies: ABSOLUTE offset from buffer start
  - No mode flag — mixed referencing is fixed behavior
  - **Corrects prior bug** in old `decompress_lcw.py`

### Images
- **CPS** (85/85): 320×200 full-screen images with embedded VGA palettes. Frame4 compression.
- **SHP** (89 files, 3492/3492 frames): Sprite animations with LoL alt-shape header (2-byte prefix + flags + height + width + height_dup + shapeSize + uncompSize = 12 bytes). Pixel data is line-encoded (skip/copy runs), optionally Frame4-compressed. Area SHPs are raw decoration shapes; creature SHPs are Frame4-compressed.
- **WSA** (241 files): Westwood Screen Animation v2. 14-byte header: numFrames, xAdd, yAdd, width, height, deltaBufSize, flags. Two-stage decode: Frame4 → delta XOR. First frames extracted for all 241; full sequences for top 20 by frame count.

### Audio
- **VOC** (215/215): Creative Voice File format. Block type 1, 8-bit unsigned PCM. Sample rates: 5494–22222 Hz (majority 11111 Hz).

### Music
- **XMI** (18): Extended MIDI in IFF FORM/XDIR containers, 11 sub-sequences per track
- **C55** (17): Creative Music File, similar IFF structure
- **ADL** (16): Raw AdLib music data (Westwood proprietary, no IFF header)
- **PCS** (16): PC Speaker music in IFF containers

### Text / Dialogue
- **ENG/FRE/GER** (90 files): uint16 offset table + null-terminated strings with Westwood bigram compression. Decoded via ScummVM's `decodeString1` (16-entry common-char table + 128-entry context table) and `decodeString2` (escape handling for accented characters). 2165 strings per language, 6495 total. All three languages produce clean readable text with correct accented characters (ä, ö, ü, ß, é, è, ê, ç, etc.).

### Level Data
- **CMZ**: LCW-compressed. 1024 blocks (32×32 grid) × 4 bytes/block = walls[N,E,S,W] as uint8. Level 24 exception: 9 bytes/block.
- **WLL**: uint16 shape_list_index + N × 12-byte records (wall_type_id, vmp_map, shape_map, special_type, wall_flags, automap_data). Maps wall types to VMP pages.
- **VCN**: uint16 tile_count + shift_table + color_table + palette + 4bpp tile data (8×8 pixels).
- **VMP**: uint16 entry_count + uint16 tile indices. 431-entry pages, stride = 22×15 viewport + overhead.
- **XXX**: Automap legend data. 12-byte records: shapeDrawX, shapeDrawY, shapeIndex, labelBlockX, labelBlockY, stringID. ScummVM `loadMapLegendData()`.
- **DAT**: uint16 count + N × 72-byte LevelDecorationProperty (shapeIndex[10], scaleFlag[10], shapeX[10], shapeY[10], next, flags).
- **INF/INI**: IFF FORM/EMC2 compiled scripts with ORDR, TEXT, DATA chunks.
- **TLC**: 21 × 256-byte color remap tables per level (lighting/effect remaps).
- **TIM**: IFF FORM/AVFS containers with AVTL (bytecode) and TEXT (string references) chunks. Opcodes control WSA playback, dialogue display, audio, and looping.

### Rendering Pipeline (fully documented and implemented)
```
CMZ block → walls[4] uint8 wall type IDs
  → WLL._wllVmpMap[wall_type] → VMP page (1-6)
    → VMP._vmpPtr[(page-1)*431 + offset] → VCN tile index
      → VCN._vcnBlocks[tileIdx * 32] → 8×8 pixel data (4bpp + palette)
```

### Level → Area Tileset Mapping (ScummVM `kLoLLevelShpListDOS[12]`)

| Idx | Area | Levels |
|-----|------|--------|
| 0 | KEEP | 1 |
| 1 | FOREST1 | 2, 3, 10, 17, 24 |
| 2 | MANOR | 4 |
| 3 | CAVE1 | 5, 6, 7, 8, 9 |
| 4 | SWAMP | 11 |
| 5 | URBISH | 12 |
| 6 | MINE1 | 13, 14, 15, 16 |
| 7 | TOWER1 | 18, 19, 20, 21 |
| 8 | YVEL1 | 22 |
| 9 | CATWALK | 23, 25 |
| 10 | RUIN | 26 |
| 11 | CIMMERIA | 27, 28, 29 |

### Edition Comparison
- **Reference corpus**: 81 PAKs, per-level layout, multi-language (ENG/FRE/GER)
- **LANDSoL**: chapter-based (CHAPTER1–8.PAK), English-focused
- 1213 entries | 1040 shared | 877 same-size | 176 different-size | 159 LANDSoL-only | 123 old-only
- GENERAL.PAK differs materially; VOC.PAK and DRIVERS.PAK are stable

### Palettes
- **PAL/COL** (11 files): 768-byte raw VGA 6-bit RGB (256 colors × 3 bytes). Area-specific alt palettes (Cave ×3, Forest ×3) and special effect palettes (FXPAL, SWAMPICE, LITEPAL).

### Fonts
- **FNT** (4 files): ScummVM DOSFont format. 14-byte header with signature 0x0500, per-glyph width/height, nibble-packed 4bpp bitmap data. 226 glyphs per font, 172 with rendered bitmaps. Atlas PNGs produced.

---

## B. Corrections Applied During This Session

1. **CMZ grid is 32×32 (1024 blocks), NOT 64×32** — old maps read uint16 pairs incorrectly
2. **CMZ contains uint8 wall type indices, NOT uint16 tile IDs**
3. **Tileset mapping is in WLL header, NOT in tile data**
4. **LCW decompressor had referencing bug** — short refs are always relative, long refs always absolute
5. **CPS: 85/85 (100%), not 78/85** — all 7 "failures" were decompressor bugs
6. **SHP uses LoL alt-shape header** — 12-byte header (2-byte prefix + flags + height + width + height_dup + sizes), not 5-byte Kyra format
7. **SHP pixel data is line-encoded** (skip/copy runs), not flat — this fixed the last 72 frame failures
8. **SHP file count: 89/89 decompressable** (CIMDOOR.SHP works with corrected decoder)

---

## C. Final Percentage

| Category | Estimate |
|----------|----------|
| Container / structural RE | **100%** |
| Edition comparison | **100%** |
| Image extraction (CPS + SHP) | **100%** |
| WSA animation (first frames) | **100%** |
| WSA animation (full sequences) | **98.8%** (239/241, 4426 frames) |
| Audio extraction (VOC) | **100%** |
| Music extraction (XMI/C55/ADL/PCS) | **100%** |
| Level rendering | **100%** |
| Text / dialogue | **100%** |
| Format documentation | **~98%** |
| **Overall lane** | **~99.5%** |

---

## D. Remaining True Gaps

1. **WSA: 2 files failed multi-frame extraction**: ESCAPE.WSA (51 frames) and CHANDELR.WSA (3 frames) fail due to a palette-offset edge case in the multi-frame extractor. First-frame thumbnails exist for both. Total: 54/4480 frames missing (1.2%).
2. **EMC2 script decompilation**: 60 INF/INI bytecode files are identified but not decompiled. ScummVM has the full interpreter; decompilation is possible but not attempted.

None of these gaps block publication or downstream use.

---

## E. Key Files

| Artifact | Path |
|----------|------|
| This memo | `/home/bob/lol1_closure_memo_2026-03-20.md` |
| Publication manifest | `/home/bob/lol1_publication_manifest.md` |
| Corrected LCW decoder | `/home/bob/lol1_decode_frame4.py` |
| SHP frame renderer | `/home/bob/lol1_shp_renderer.py` |
| Level renderer | `/home/bob/lol1_vcn_extractor.py` |
| WLL parser | `/home/bob/lol1_wll_vmp_mapper.py` |
| Wall type analysis | `/home/bob/lol1_cmz_walltype_analysis.py` |
| Dialogue extractor | `/home/bob/lol1_extract_dialogue.py` |
| Dialogue decoder | `/home/bob/decode_lol1_dialogue.py` |
| Music extractor | `/home/bob/lol1_extract_music.py` |
| WSA extractor | `/home/bob/lol1_wsa_extract.py` |
| WSA multi-frame extractor | `/home/bob/lol1_wsa_all_frames_extract.py` |
| TIM parser | `/home/bob/lol1_parse_tim.py` |
| Font extractor | `/home/bob/lol1_fonts/extract_fonts.py` |
| Level→tileset map | `/home/bob/lol1_level_tileset_map.md` |
| PAK index (1163 entries) | `/home/bob/lol1_pak_index.json` |
| WLL parsed data | `/home/bob/lol1_wll_parsed.json` |
| SHP inventory | `/home/bob/lol1_shp_inventory.json` |
| SHP render results | `/home/bob/lol1_shp_render_results.json` |
| WSA inventory | `/home/bob/lol1_wsa_inventory.json` |
| Music inventory | `/home/bob/lol1_music_inventory.json` |
| Dialogue summary | `/home/bob/lol1_dialogue_summary.json` |
| TIM analysis | `/home/bob/lol1_tim_analysis.json` |
| Font metadata | `/home/bob/lol1_fonts/font_info.json` |
| LANDSoL comparison | `/home/bob/lol1_landsol_comparison_2026-03-18.md` |
| CPS images (85 PNG) | `/home/bob/lol1_cps_complete/` |
| SHP frames (3492 PNG) | `/home/bob/lol1_shp_rendered/` |
| WSA first frames (241 PNG) | `/home/bob/lol1_wsa_frames/` |
| WSA full sequences (4426 PNG) | `/home/bob/lol1_wsa_all_frames/` |
| Level maps (29 PNG) | `/home/bob/lol1_levels_rendered/` |
| VOC audio (215 WAV) | `/home/bob/lol1_audio_complete/` |
| Music files (67) | `/home/bob/lol1_music/` |
| Dialogue raw (90 JSON) | `/home/bob/lol1_dialogue/` |
| Dialogue decoded (90 JSON) | `/home/bob/lol1_dialogue_decoded/` |
| Font atlases (4 PNG) | `/home/bob/lol1_fonts/` |
| Reference corpus | `/media/bob/Arikv/REFERENCE/game_files/lol1/DATA/` |
| LANDSoL build | `/media/bob/Arikv/new files or things/LANDSoL/` |

---

## F. Lane Status

**This lane is closed at ~99.5%.** All 1163 files in the corpus have been processed. Every major asset type — images (CPS 85/85, SHP 3492/3492 frames, WSA 239/241 fully sequenced with 4426 frames), audio (VOC 215/215), music (67/67), level maps (29/29), dialogue (6495/6495 decoded strings in 3 languages), fonts (4/4 atlases), palettes (11/11), tilesets (14/14 including YVEL2), and timing scripts (139/139 parsed) — has been extracted to usable formats.

The rendering pipeline (CMZ → WLL → VMP → VCN) is fully documented and implemented. Two distinct editions are compared and characterized. All format specifications are ScummVM-cross-referenced.

The remaining ~0.5% consists of: 2 WSA files with palette-offset edge cases (54 frames, first-frame thumbnails exist) and EMC2 script decompilation (60 files identified, not decompiled). Neither blocks publication.

**The lane is publication-ready.**
