#!/usr/bin/env python3
"""
LoL1 Task 1: Complete Tileset ID Mapping

Extracts all CMZ files from L##.PAK archives, decompresses them,
and maps tile ID high bytes to determine which VCN tileset each level uses.

Known VCN files (13):
  CATWALK, CAVE1, CIMMERIA, FOREST1, KEEP, MANOR, MINE1,
  RUIN, SWAMP, TOWER1, URBISH, YVEL1, YVEL2
"""

import json
import struct
import os
import sys

# Import the existing LCW decompressor
sys.path.insert(0, '/home/bob')
from lol1_decompress_lcw import decompress_lcw

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_FILE = "/home/bob/lol1_tileset_mapping.json"

# All 13 VCN tilesets
VCN_NAMES = [
    "CATWALK", "CAVE1", "CIMMERIA", "FOREST1", "KEEP", "MANOR",
    "MINE1", "RUIN", "SWAMP", "TOWER1", "URBISH", "YVEL1", "YVEL2"
]


def read_pak_entry(pak_path, offset, size):
    """Read raw bytes of an entry from a PAK file."""
    with open(pak_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def decompress_cmz(data):
    """Decompress CMZ: 10-byte header + LCW compressed tile data."""
    if len(data) < 12:
        return None
    # Try with relative mode (prepend 0x00) — known to work for CMZ
    compressed = b'\x00' + data[10:]
    result = decompress_lcw(compressed)
    if result is None:
        # Try standard mode
        result = decompress_lcw(data[10:])
    return result


def extract_tile_high_bytes(decompressed):
    """Extract unique high bytes from uint16 tile IDs in decompressed CMZ data.

    CMZ structure: 6-byte header + uint16 tile IDs in row-major order.
    """
    if decompressed is None or len(decompressed) < 8:
        return set(), {}

    # Skip 6-byte header, read uint16 tile IDs
    tile_data = decompressed[6:]
    n_tiles = len(tile_data) // 2

    high_byte_counts = {}
    high_bytes = set()

    for i in range(n_tiles):
        tile_id = struct.unpack_from('<H', tile_data, i * 2)[0]
        if tile_id == 0:
            continue  # Skip empty tiles
        high = (tile_id >> 8) & 0xFF
        low = tile_id & 0xFF
        high_bytes.add(high)
        if high not in high_byte_counts:
            high_byte_counts[high] = {"count": 0, "example_low_bytes": set()}
        high_byte_counts[high]["count"] += 1
        high_byte_counts[high]["example_low_bytes"].add(low)

    return high_bytes, high_byte_counts


def main():
    # Load PAK index
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    results = {}
    all_high_bytes = set()

    # Process each level PAK (L01-L29)
    for level_num in range(1, 30):
        pak_name = f"L{level_num:02d}.PAK"
        cmz_name = f"LEVEL{level_num}.CMZ"

        if pak_name not in index["pak_files"]:
            print(f"  SKIP: {pak_name} not found in index")
            continue

        pak_info = index["pak_files"][pak_name]

        # Find the CMZ entry
        cmz_entry = None
        for entry in pak_info["entries"]:
            if entry["name"] == cmz_name:
                cmz_entry = entry
                break

        if cmz_entry is None:
            print(f"  SKIP: {cmz_name} not found in {pak_name}")
            continue

        # Read and decompress
        pak_path = os.path.join(PAK_DIR, pak_name)
        if not os.path.exists(pak_path):
            print(f"  SKIP: {pak_path} not found on disk")
            continue

        raw = read_pak_entry(pak_path, cmz_entry["offset"], cmz_entry["size"])
        decompressed = decompress_cmz(raw)

        if decompressed is None:
            print(f"  FAIL: {cmz_name} decompression failed")
            continue

        high_bytes, high_byte_counts = extract_tile_high_bytes(decompressed)
        all_high_bytes.update(high_bytes)

        # Convert sets to sorted lists for JSON
        level_result = {
            "pak": pak_name,
            "cmz": cmz_name,
            "cmz_size": cmz_entry["size"],
            "decompressed_size": len(decompressed),
            "n_tiles": (len(decompressed) - 6) // 2,
            "high_bytes": sorted(high_bytes),
            "high_byte_detail": {}
        }

        for hb, info in sorted(high_byte_counts.items()):
            level_result["high_byte_detail"][f"0x{hb:02x}"] = {
                "count": info["count"],
                "unique_low_bytes": len(info["example_low_bytes"]),
                "max_low_byte": max(info["example_low_bytes"]),
            }

        results[f"level{level_num:02d}"] = level_result

        hb_str = ", ".join(f"0x{h:02x}({high_byte_counts[h]['count']})" for h in sorted(high_bytes))
        print(f"  Level {level_num:2d}: high_bytes=[{hb_str}]  tiles={level_result['n_tiles']}")

    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Levels processed: {len(results)}")
    print(f"All unique high bytes: {sorted(all_high_bytes)}")
    print(f"High byte hex: {[f'0x{h:02x}' for h in sorted(all_high_bytes)]}")

    # Build high-byte → levels mapping
    hb_to_levels = {}
    for level_key, lr in results.items():
        for hb in lr["high_bytes"]:
            hb_hex = f"0x{hb:02x}"
            if hb_hex not in hb_to_levels:
                hb_to_levels[hb_hex] = []
            hb_to_levels[hb_hex].append(level_key)

    print(f"\nHigh-byte → levels:")
    for hb_hex in sorted(hb_to_levels.keys()):
        levels = hb_to_levels[hb_hex]
        print(f"  {hb_hex}: {', '.join(levels)}")

    # Save full results
    output = {
        "description": "LoL1 tileset ID mapping — high byte → VCN correlation",
        "vcn_files": VCN_NAMES,
        "all_unique_high_bytes": [f"0x{h:02x}" for h in sorted(all_high_bytes)],
        "high_byte_to_levels": hb_to_levels,
        "per_level": results
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
