# LoL1 Level → Tileset Mapping (ScummVM-verified)

**Date:** 2026-03-20
**Source:** ScummVM `engines/kyra/engine/scene_lol.cpp`, `devtools/create_kyradat/resources/lol_dos.h`

## Rendering Pipeline (corrected)

Previous assumption was wrong: CMZ does NOT contain uint16 "tile IDs" with a tileset byte.

Actual pipeline:
```
CMZ (LCW-compressed) → 1024 blocks × 4 bytes each
  → walls[4] = uint8 wall type IDs (N, E, S, W)
  → WLL file defines _wllVmpMap[wall_type] → VMP page (1-6)
  → VMP file: _vmpPtr[(page-1) * 431 + offset] → VCN tile index
  → VCN file: _vcnBlocks[vcnIdx * 32] → 8×8 pixel tile data
```

## Level → Area/Tileset Mapping

WLL byte 0-1 = `shape_list_index` → indexes `kLoLLevelShpListDOS[12]`:

| Index | Area | VCN + VMP | SHP + DAT | Levels |
|-------|------|-----------|-----------|--------|
| 0 | KEEP | KEEP.VCN/VMP | KEEP.SHP/DAT | 1 |
| 1 | FOREST1 | FOREST1.VCN/VMP | FOREST1.SHP/DAT | 2, 3, 10, 17, 24 |
| 2 | MANOR | MANOR.VCN/VMP | MANOR.SHP/DAT | 4 |
| 3 | CAVE1 | CAVE1.VCN/VMP | CAVE1.SHP/DAT | 5, 6, 7, 8, 9 |
| 4 | SWAMP | SWAMP.VCN/VMP | SWAMP.SHP/DAT | 11 |
| 5 | URBISH | URBISH.VCN/VMP | URBISH.SHP/DAT | 12 |
| 6 | MINE1 | MINE1.VCN/VMP | MINE1.SHP/DAT | 13, 14, 15, 16 |
| 7 | TOWER1 | TOWER1.VCN/VMP | TOWER1.SHP/DAT | 18, 19, 20, 21 |
| 8 | YVEL1 | YVEL1.VCN/VMP | YVEL1.SHP/DAT | 22 |
| 9 | CATWALK | CATWALK.VCN/VMP | CATWALK.SHP/DAT | 23, 25 |
| 10 | RUIN | RUIN.VCN/VMP | RUIN.SHP/DAT | 26 |
| 11 | CIMMERIA | CIMMERIA.VCN/VMP | CIMMERIA.SHP/DAT | 27, 28, 29 |

Note: YVEL2.VCN/VMP exists but is not in the base list — likely loaded for a specific subarea.

## CMZ Format (corrected)

```
[LCW compressed payload]
Decompressed structure:
  Bytes 0-5: header (6 bytes)
    [0-3]: unknown
    [4-5]: uint16 len = bytes per block (4 for standard, 9 for L24)
  Bytes 6+: 1024 blocks × len bytes each
    Block[i] bytes 0-3: walls[N, E, S, W] as uint8 wall type IDs
    Block[i] bytes 4+:  extra properties (L24 only, 5 extra bytes)
```

Grid: **32×32 = 1024 blocks** (NOT 64×32 as previously documented)

## WLL Format (from ScummVM)

```
Bytes 0-1: uint16 shape_list_index → area tileset index
Bytes 2+:  N records of 12 bytes each ((file_size - 2) / 12)
  Record:
    [0-1] uint16 wall_type_id
    [2]   uint8  vmp_map_value     → VMP page (1-6, or 0 = no geometry)
    [3]   (padding)
    [4-5] int16  shape_map_value   → decoration shape index
    [6]   uint8  special_wall_type
    [7]   (padding)
    [8]   uint8  wall_flags
    [9]   (padding)
    [10]  uint8  automap_data
    [11]  (padding)
```

## VMP Format

```
Bytes 0-1: uint16 entry_count
Bytes 2+:  entry_count × uint16 values
  Each VMP "page" = 431 entries (22×15 viewport + 101 overhead)
  _vmpPtr[(page - 1) * 431 + offset] = VCN tile index
```

## VCN Format

```
Bytes 0-1: uint16 tile_count
Bytes 2+:  tile_count bytes of shift table (_vcnShift)
  Then:    128 bytes of color table (_vcnColTable)
  Then:    384 bytes of palette (VGA 6-bit RGB × 128 colors)
  Then:    tile_count × 32 bytes of pixel data (8×8 @ 4bpp = 32 bytes per tile)
           OR tile_count × 64 bytes (8×8 @ 8bpp = 64 bytes per tile)
```

## Wall Type Consistency

- Wall types 0x01-0x02: VMP page 1 and 2 respectively, consistent across ALL 29 levels
- Wall types 0x03-0x16: VMP page 3, consistent (wall variants)
- Wall types 0x17+: VMP page varies by level (contextual: doors, decorations, special)
- Wall type 0x00: no VMP mapping (empty/passable space)

## Files Produced

- `/home/bob/lol1_wall_type_analysis.json` — all wall type IDs per level
- `/home/bob/lol1_wll_parsed.json` — complete WLL parse for all 29 levels
- `/home/bob/lol1_tileset_mapping.json` — (superseded, used wrong uint16 interpretation)

## Corrections to Prior Work

1. **Grid is 32×32 (1024 blocks), NOT 64×32 (2048 tiles)**
   - The old maps at `/home/bob/lol1_maps/` rendered 2048 uint16 values — these were actually pairs of adjacent wall bytes misread as single uint16 values
2. **CMZ contains uint8 wall type indices, NOT uint16 tile IDs**
   - The "high byte" analysis was actually seeing adjacent wall pairs
3. **Tileset mapping is NOT in the tile data** — it's in the WLL file header
4. **VMP page count is 6 max**, not 13 (one per VCN file)
5. **Level 1 is rendered from KEEP.VCN**, confirmed via shape_list_index=0
