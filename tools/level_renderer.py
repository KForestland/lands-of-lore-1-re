#!/usr/bin/env python3
"""
LoL1 VCN + VMP Extractor and Level Renderer

VCN format (ScummVM):
  uint16 tile_count
  tile_count bytes: shift table
  128 bytes: color table
  384 bytes: palette (128 colors × 3 bytes, VGA 6-bit)
  tile_count × 32 bytes: pixel data (8×8 tiles, 4bpp packed)

VMP format:
  uint16 entry_count
  entry_count × uint16: tile indices into VCN

Rendering pipeline:
  CMZ blocks → walls[4] uint8 → WLL _wllVmpMap → VMP page → VCN tile
"""

import json
import struct
import os
import sys
from PIL import Image

sys.path.insert(0, '/home/bob')
from lol1_decompress_lcw import decompress_lcw

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_DIR = "/home/bob/lol1_levels_rendered"

# Level → area mapping (from ScummVM kLoLLevelShpListDOS)
AREA_LIST = [
    "KEEP", "FOREST1", "MANOR", "CAVE1", "SWAMP", "URBISH",
    "MINE1", "TOWER1", "YVEL1", "CATWALK", "RUIN", "CIMMERIA"
]

# shape_list_index per level (from WLL first word)
LEVEL_AREA_INDEX = {
    1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3,
    10: 1, 11: 4, 12: 5, 13: 6, 14: 6, 15: 6, 16: 6,
    17: 1, 18: 7, 19: 7, 20: 7, 21: 7, 22: 8, 23: 9,
    24: 1, 25: 9, 26: 10, 27: 11, 28: 11, 29: 11
}


def read_pak_entry(pak_path, offset, size):
    with open(pak_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def decompress_from_pak(pak_path, offset, size):
    """Read and LCW-decompress a file from a PAK."""
    raw = read_pak_entry(pak_path, offset, size)
    # ScummVM uses loadBitmap which handles the decompression
    # The files have a 10-byte header before LCW data
    if len(raw) < 12:
        return None
    compressed = b'\x00' + raw[10:]  # Relative mode
    result = decompress_lcw(compressed)
    if result is None:
        result = decompress_lcw(raw[10:])  # Try standard
    return result


def parse_vcn(data):
    """Parse a decompressed VCN file."""
    if data is None or len(data) < 4:
        return None

    tile_count = struct.unpack_from('<H', data, 0)[0]
    pos = 2

    shift_table = data[pos:pos + tile_count]
    pos += tile_count

    col_table = data[pos:pos + 128]
    pos += 128

    palette_raw = data[pos:pos + 384]
    pos += 384

    # Build RGB palette (VGA 6-bit → 8-bit)
    palette = []
    for i in range(128):
        r = (palette_raw[i * 3] & 0x3F) * 4
        g = (palette_raw[i * 3 + 1] & 0x3F) * 4
        b = (palette_raw[i * 3 + 2] & 0x3F) * 4
        palette.append((r, g, b))
    # Pad to 256 colors
    while len(palette) < 256:
        palette.append((0, 0, 0))

    # Tile pixel data: 4bpp packed, 8×8 = 32 bytes per tile
    tile_data_size = tile_count * 32
    remaining = len(data) - pos

    # Check if 4bpp or 8bpp
    if remaining >= tile_count * 64:
        bpp = 8
        bytes_per_tile = 64
    elif remaining >= tile_count * 32:
        bpp = 4
        bytes_per_tile = 32
    else:
        # Try without palette/color table
        bpp = 4
        bytes_per_tile = 32

    tiles = []
    for t in range(tile_count):
        tile_offset = pos + t * bytes_per_tile
        if tile_offset + bytes_per_tile > len(data):
            break

        pixels = []
        if bpp == 4:
            for b in range(32):
                byte = data[tile_offset + b]
                # 4bpp: high nibble first, then low nibble
                pixels.append((byte >> 4) & 0x0F)
                pixels.append(byte & 0x0F)
        else:
            for b in range(64):
                pixels.append(data[tile_offset + b])

        tiles.append(pixels)

    return {
        "tile_count": tile_count,
        "bpp": bpp,
        "shift_table": shift_table,
        "col_table": col_table,
        "palette": palette,
        "tiles": tiles,
        "data_size": len(data),
    }


def parse_vmp(data):
    """Parse a decompressed VMP file."""
    if data is None or len(data) < 4:
        return None

    entry_count = struct.unpack_from('<H', data, 0)[0]
    entries = []
    for i in range(entry_count):
        if 2 + i * 2 + 2 > len(data):
            break
        entries.append(struct.unpack_from('<H', data, 2 + i * 2)[0])

    return {
        "entry_count": entry_count,
        "entries": entries,
    }


def parse_cmz(data):
    """Parse decompressed CMZ into 1024 blocks."""
    if data is None or len(data) < 8:
        return None

    len_per_block = struct.unpack_from('<H', data, 4)[0]
    blocks = []
    for i in range(1024):
        off = 6 + i * len_per_block
        if off + 4 > len(data):
            break
        walls = [data[off + d] for d in range(4)]
        blocks.append(walls)

    return blocks


def parse_wll(data):
    """Parse WLL file, return vmp_map dict."""
    if len(data) < 14:
        return None, None

    shape_idx = struct.unpack_from('<H', data, 0)[0]
    n_records = (len(data) - 2) // 12
    vmp_map = {}

    for i in range(n_records):
        off = 2 + i * 12
        wall_type = struct.unpack_from('<H', data, off)[0]
        vmp_val = data[off + 2]
        vmp_map[wall_type] = vmp_val

    return shape_idx, vmp_map


def render_level_topdown(blocks, vmp_map, vcn, vmp, level_num, area_name):
    """Render a 32×32 top-down map using wall types → VMP → VCN tiles."""
    # For a top-down view, each block gets a representative color/tile
    # We'll render each block as 8×8 pixels using VCN tiles

    # Simple approach: for each block, use the dominant wall type's VMP page
    # to select a representative tile, then render it

    block_size = 8
    img_w = 32 * block_size
    img_h = 32 * block_size
    img = Image.new('RGB', (img_w, img_h), (0, 0, 0))

    palette = vcn["palette"]

    for by in range(32):
        for bx in range(32):
            block_idx = by * 32 + bx
            if block_idx >= len(blocks):
                continue

            walls = blocks[block_idx]

            # Check if this block is passable (all walls = 0 or all have vmp=0)
            has_wall = False
            best_vmp = 0
            for w in walls:
                vm = vmp_map.get(w, 0)
                if vm > best_vmp:
                    best_vmp = vm
                if w > 0 and vm > 0:
                    has_wall = True

            if not has_wall or best_vmp == 0:
                # Empty/passable block — dark color
                for py in range(block_size):
                    for px in range(block_size):
                        img.putpixel((bx * block_size + px, by * block_size + py),
                                     (20, 20, 30))
                continue

            # Get a VCN tile from VMP page
            vmp_entries = vmp["entries"]
            page_start = (best_vmp - 1) * 431
            # Use a tile from the middle of the page for representative look
            tile_offset = page_start + 165  # roughly center of 22×15 viewport

            if tile_offset < len(vmp_entries):
                vcn_idx = vmp_entries[tile_offset]
                # Strip flags
                flip = (vcn_idx & 0x4000) != 0
                vcn_idx = vcn_idx & 0x3FFF

                if vcn_idx < len(vcn["tiles"]):
                    tile_pixels = vcn["tiles"][vcn_idx]
                    for py in range(8):
                        for px in range(8):
                            pi = py * 8 + (7 - px if flip else px)
                            if pi < len(tile_pixels):
                                color_idx = tile_pixels[pi]
                                if color_idx < len(palette):
                                    color = palette[color_idx]
                                else:
                                    color = (128, 0, 128)
                                img.putpixel((bx * block_size + px,
                                              by * block_size + py), color)
                    continue

            # Fallback: solid color based on vmp page
            colors = [(100, 100, 100), (150, 100, 50), (80, 120, 80),
                      (60, 60, 100), (120, 80, 60), (90, 90, 90)]
            c = colors[min(best_vmp - 1, len(colors) - 1)]
            for py in range(block_size):
                for px in range(block_size):
                    img.putpixel((bx * block_size + px, by * block_size + py), c)

    return img


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    # Cache parsed VCN/VMP per area
    area_cache = {}

    def get_area_data(area_name):
        if area_name in area_cache:
            return area_cache[area_name]

        # Handle YVEL1/YVEL2 being in YVEL.PAK
        pak_name = f"{area_name}.PAK"
        if pak_name not in index["pak_files"]:
            # Try parent name (e.g., YVEL1 → YVEL.PAK)
            import re
            base = re.sub(r'\d+$', '', area_name)
            pak_name = f"{base}.PAK"
            if pak_name not in index["pak_files"]:
                print(f"    Area PAK not found for {area_name}")
                return None

        pak_path = os.path.join(PAK_DIR, pak_name)
        pak_info = index["pak_files"][pak_name]

        # Find VCN and VMP entries
        vcn_entry = vmp_entry = None
        for entry in pak_info["entries"]:
            if entry["name"] == f"{area_name}.VCN":
                vcn_entry = entry
            elif entry["name"] == f"{area_name}.VMP":
                vmp_entry = entry

        if not vcn_entry or not vmp_entry:
            print(f"    VCN/VMP not found in {pak_name}")
            return None

        vcn_data = decompress_from_pak(pak_path, vcn_entry["offset"], vcn_entry["size"])
        vmp_data = decompress_from_pak(pak_path, vmp_entry["offset"], vmp_entry["size"])

        vcn = parse_vcn(vcn_data)
        vmp = parse_vmp(vmp_data)

        if not vcn or not vmp:
            print(f"    Failed to parse VCN/VMP for {area_name}")
            return None

        result = {"vcn": vcn, "vmp": vmp}
        area_cache[area_name] = result
        print(f"    Area {area_name}: {vcn['tile_count']} VCN tiles ({vcn['bpp']}bpp), "
              f"{vmp['entry_count']} VMP entries")
        return result

    # Process each level
    for level_num in range(1, 30):
        pak_name = f"L{level_num:02d}.PAK"
        cmz_name = f"LEVEL{level_num}.CMZ"
        wll_name = f"LEVEL{level_num}.WLL"

        if pak_name not in index["pak_files"]:
            continue

        pak_path = os.path.join(PAK_DIR, pak_name)
        pak_info = index["pak_files"][pak_name]

        # Find CMZ and WLL entries
        cmz_entry = wll_entry = None
        for entry in pak_info["entries"]:
            if entry["name"] == cmz_name:
                cmz_entry = entry
            elif entry["name"] == wll_name:
                wll_entry = entry

        if not cmz_entry or not wll_entry:
            print(f"Level {level_num}: missing CMZ or WLL")
            continue

        # Parse CMZ
        cmz_raw = read_pak_entry(pak_path, cmz_entry["offset"], cmz_entry["size"])
        cmz_decompressed = decompress_from_pak(pak_path, cmz_entry["offset"], cmz_entry["size"])
        # Actually decompress correctly
        cmz_decompressed2 = None
        compressed = b'\x00' + cmz_raw[10:]
        cmz_decompressed2 = decompress_lcw(compressed)
        if cmz_decompressed2 is None:
            cmz_decompressed2 = decompress_lcw(cmz_raw[10:])

        blocks = parse_cmz(cmz_decompressed2)
        if not blocks:
            print(f"Level {level_num}: CMZ parse failed")
            continue

        # Parse WLL
        wll_raw = read_pak_entry(pak_path, wll_entry["offset"], wll_entry["size"])
        shape_idx, vmp_map = parse_wll(wll_raw)
        if vmp_map is None:
            print(f"Level {level_num}: WLL parse failed")
            continue

        area_idx = LEVEL_AREA_INDEX.get(level_num, shape_idx)
        area_name = AREA_LIST[area_idx] if area_idx < len(AREA_LIST) else "UNKNOWN"

        print(f"Level {level_num:2d} → {area_name} (idx={area_idx}), "
              f"blocks={len(blocks)}, wall_types={len(vmp_map)}")

        # Get area VCN/VMP
        area_data = get_area_data(area_name)
        if not area_data:
            print(f"  Skipping render — no area data")
            continue

        # Render
        img = render_level_topdown(blocks, vmp_map, area_data["vcn"],
                                    area_data["vmp"], level_num, area_name)

        out_path = os.path.join(OUTPUT_DIR, f"level{level_num:02d}_{area_name.lower()}.png")
        img.save(out_path)
        print(f"  Saved: {out_path}")

    print(f"\nDone! Rendered levels in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
