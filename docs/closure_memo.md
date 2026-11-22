> **History (March 2026).** The claim ~~closed at ~99.999%~~ was withdrawn on 18 November 2026. See [the current status and open questions](STATUS.md#where-this-stands) and [later corrections to this memo](#later-corrections).

# LoL1 March 2026 Research Memo

**Date:** 2026-03-20
**Scope:** LoL1 reverse-engineering and documentation only
**Status (March 2026):** ~~CLOSED at ~99.999%~~. Withdrawn on 18 November 2026. See [current status](STATUS.md#where-this-stands).
**Publication:** Ready for GitHub/wiki publication

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

### Fully Extracted After Final Fixes

| Asset Type | Files | Status | Output |
|-----------|-------|--------|--------|
| **WSA multi-frame** | 241 total | 241/241 fully sequenced (4480/4480 frames, 100%) | `lol1_wsa_all_frames/` |

### Documented / Identified

| Asset Type | Files | Status | Output |
|-----------|-------|--------|--------|
| **FNT fonts** | 4 | Glyph format decoded (DOSFont nibble-packed 4bpp); 4 atlas PNGs rendered | `lol1_fonts/` |
| **TIM timing scripts** | 139 | AVFS bytecode parsed; opcodes identified (WSA control, dialogue, audio, loops) | `lol1_tim_analysis.json` |
| **INF/INI scripts** | 60 | EMC2 compiled bytecode fully decompiled to readable ASM-like output | `lol1_scripts_decompiled/` |
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
- **WSA** (241 files): Westwood Screen Animation v2. 14-byte header: numFrames, xAdd, yAdd, width, height, deltaBufSize, flags. Two-stage decode: Frame4 → delta XOR. First frames extracted for all 241; full sequences for all 241 files (4480 total frames). Palette-containing WSAs (ESCAPE.WSA, CHANDELR.WSA) required a fix to skip the palette pointer at `offsets[0]`.

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
- **floppy**: chapter-based (CHAPTER1–8.PAK), English-focused
- 1213 entries | 1040 shared | 877 same-size | 176 different-size | 159 floppy-only | 123 old-only
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

## C. March 2026 Estimates

| Category | Estimate |
|----------|----------|
| Container / structural RE | **100%** |
| Edition comparison | **100%** |
| Image extraction (CPS + SHP) | **100%** |
| WSA animation (first frames) | **100%** |
| WSA animation (full sequences) | **100%** (241/241, 4480 frames) |
| Audio extraction (VOC) | **100%** |
| Music extraction (XMI/C55/ADL/PCS) | **100%** |
| Level rendering | **100%** |
| Text / dialogue | **100%** |
| Format documentation | **100%** |
| EMC2 script decompilation | **100%** (60/60 scripts, 117,099 words) |
| **Overall (March 2026)** | **~~About 99.999%~~. Withdrawn on 18 November 2026.** See [current status](STATUS.md#where-this-stands). |

---

## D. Fixes Recorded in March 2026

1. **WSA: 2 files failed multi-frame extraction** — FIXED. ESCAPE.WSA (51 frames) and CHANDELR.WSA (3 frames) were failing due to a palette-offset edge case where `offsets[0]` points to the embedded palette, not frame 0. Fix: `lol1_wsa_fix.py`. Result: 241/241 files, 4480/4480 frames (100%).
2. **EMC2 script decompilation** — DONE. Full decompiler built per ScummVM `engines/kyra/script/script.cpp`. 19 VM opcodes + 192 game-specific opcodes decoded. 60/60 scripts decompiled to readable ASM-like output in `lol1_scripts_decompiled/`.

The claim that only publication work remained was withdrawn on 18 November 2026. See the [open questions](OPEN_QUESTIONS.md).

---

## E. Key Files

| Artifact | Path |
|----------|------|
| This memo | `lol1_closure_memo_2026-03-20.md` (author's working copy, not in this repository) |
| Publication manifest | `lol1_publication_manifest.md` (author's working copy, not in this repository) |
| Corrected LCW decoder | `lol1_decode_frame4.py` (author's working copy, not in this repository) |
| SHP frame renderer | `lol1_shp_renderer.py` (author's working copy, not in this repository) |
| Level renderer | `lol1_vcn_extractor.py` (author's working copy, not in this repository) |
| WLL parser | `lol1_wll_vmp_mapper.py` (author's working copy, not in this repository) |
| Wall type analysis | `lol1_cmz_walltype_analysis.py` (author's working copy, not in this repository) |
| Dialogue extractor | `lol1_extract_dialogue.py` (author's working copy, not in this repository) |
| Dialogue decoder | `decode_lol1_dialogue.py` (author's working copy, not in this repository) |
| Music extractor | `lol1_extract_music.py` (author's working copy, not in this repository) |
| WSA extractor | `lol1_wsa_extract.py` (author's working copy, not in this repository) |
| WSA multi-frame extractor | `lol1_wsa_all_frames_extract.py` (author's working copy, not in this repository) |
| WSA palette fix | `lol1_wsa_fix.py` (author's working copy, not in this repository) |
| EMC2 decompiler | `lol1_emc2_decompiler.py` (author's working copy, not in this repository) |
| TIM parser | `lol1_parse_tim.py` (author's working copy, not in this repository) |
| Font extractor | `lol1_fonts/extract_fonts.py` (author's working copy, not in this repository) |
| Level→tileset map | `lol1_level_tileset_map.md` (author's working copy, not in this repository) |
| PAK index (1163 entries) | `lol1_pak_index.json` (author's working copy, not in this repository) |
| WLL parsed data | `lol1_wll_parsed.json` (author's working copy, not in this repository) |
| SHP inventory | `lol1_shp_inventory.json` (author's working copy, not in this repository) |
| SHP render results | `lol1_shp_render_results.json` (author's working copy, not in this repository) |
| WSA inventory | `lol1_wsa_inventory.json` (author's working copy, not in this repository) |
| Music inventory | `lol1_music_inventory.json` (author's working copy, not in this repository) |
| Dialogue summary | `lol1_dialogue_summary.json` (author's working copy, not in this repository) |
| TIM analysis | `lol1_tim_analysis.json` (author's working copy, not in this repository) |
| Font metadata | `lol1_fonts/font_info.json` (author's working copy, not in this repository) |
| floppy comparison | `lol1_landsol_comparison_2026-03-18.md` (author's working copy, not in this repository) |
| CPS images (85 PNG) | `lol1_cps_complete/` (author's working copy, not in this repository) |
| SHP frames (3492 PNG) | `lol1_shp_rendered/` (author's working copy, not in this repository) |
| WSA first frames (241 PNG) | `lol1_wsa_frames/` (author's working copy, not in this repository) |
| WSA full sequences (4480 PNG) | `lol1_wsa_all_frames/` (author's working copy, not in this repository) |
| Decompiled scripts (60 ASM) | `lol1_scripts_decompiled/` (author's working copy, not in this repository) |
| Level maps (29 PNG) | `lol1_levels_rendered/` (author's working copy, not in this repository) |
| VOC audio (215 WAV) | `lol1_audio_complete/` (author's working copy, not in this repository) |
| Music files (67) | `lol1_music/` (author's working copy, not in this repository) |
| Dialogue raw (90 JSON) | `lol1_dialogue/` (author's working copy, not in this repository) |
| Dialogue decoded (90 JSON) | `lol1_dialogue_decoded/` (author's working copy, not in this repository) |
| Font atlases (4 PNG) | `lol1_fonts/` (author's working copy, not in this repository) |
| Reference corpus | the CD edition's `DATA/` folder |
| floppy build | the floppy installation folder |

---

## F. Status

**March 2026 claim:** ~~This work was closed at ~99.999%.~~ Withdrawn on 18 November 2026. See [current status](STATUS.md#where-this-stands).

The March inventory counted 1163 entries in the CD's top-level PAK archives. It reported output for images (CPS 85/85, SHP 3492/3492 frames, WSA 241/241 sequences and 4480 frames), audio (VOC 215/215), music (67/67), level maps (29/29), dialogue (6495/6495 strings in 3 languages), fonts (4/4 atlases), palettes (11/11), tilesets (14/14 including YVEL2), timing scripts (139/139) and game scripts (60/60 EMC2). See [later corrections](#later-corrections) for the scope and errors in those results.

The March memo reported a renderer following CMZ → WLL → VMP → VCN, a comparison of the CD and floppy editions, and format notes cross-referenced to ScummVM.

The March memo called the work publication-ready. Its closure claim was withdrawn on 18 November 2026. See [current status](STATUS.md#where-this-stands).

---

## Later corrections

Added after the memo; the format pages give the details.

1. TLK is not "uint16 count + 8-byte entries": CD TLK files are PAK archives of VOC samples ([tlk.md](formats/tlk.md)).
2. TLC holds one 256-byte slot table and twenty 256-byte blend rows for transparency, not "lighting/effect remaps" ([tlc.md](formats/tlc.md)).
3. VMP is 330 floor/ceiling words plus 431 words per wall page; the "8bpp VCN" variant in `level_tileset_map.md` does not occur in LoL1 ([vcn_vmp.md](formats/vcn_vmp.md)).
4. VOC "majority 11111 Hz": the effects use the 11025 Hz divisor class, CD speech 22050 Hz ([voc.md](formats/voc.md)).
5. "1163 files" covers only the CD top-level `DATA/` PAKs (see [Corpus coverage](STATUS.md#corpus-coverage)).
6. SHP has no 2-byte prefix on CD or floppy. The March renderer read every shape 2 bytes early because it counted offsets from the file start instead of byte 2 ([shp.md](formats/shp.md)).
7. The "bytes 0-3 unknown" header belongs to CMZ, not WLL ([cmz.md](formats/cmz.md)).
8. FNT "226 glyphs per font" holds for the CD; floppy FONT6P/9P/9PN have 128 ([fnt.md](formats/fnt.md)).
9. WSA needs no per-file palette fix: frame offsets are relative to the frame data, which starts after the palette ([wsa.md](formats/wsa.md)).
10. `data/wall_type_analysis.json` was built with the old LCW bug and had wrong wall counts; regenerated ([cmz.md](formats/cmz.md)).
11. `data/tileset_mapping.json` (uint16 "tile ID" guess) replaced by the real level-to-set mapping. Level 25 draws its walls with CAVE1 and CAV_PLT3.PAL, not CATWALK ([vcn_vmp.md](formats/vcn_vmp.md)).
12. `data/tim_analysis.json` listed opcodes 112 and 176, which are not TIM commands, and copied the raw script words of 11 TIM files; regenerated without either (2.6 MB to 40 KB). Command counts: [tim.md](formats/tim.md).
13. `data/shp_inventory.json` (frame sizes up to 12,974,107 bytes) replaced; `data/shp_render_results.json` removed (it counted the old fallback decoder's output).
