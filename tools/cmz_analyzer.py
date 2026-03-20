#!/usr/bin/env python3
"""
LoL1 Task 1 (corrected): CMZ Wall Type Analysis

ScummVM reveals the actual CMZ structure:
  - loadBitmap decompresses CMZ (LCW)
  - Decompressed: bytes 0-3 unknown header, byte 4-5 = uint16 len (bytes per block)
  - Then 1024 blocks × len bytes each
  - First 4 bytes of each block = walls[4] (uint8 wall type indices)
  - Wall types index into WLL table → _wllVmpMap → VMP → VCN tiles

  LevelBlockProperty.walls[4]: N, E, S, W wall type IDs (uint8, 0-255)
  _wllVmpMap[wallType] → VMP page index (from WLL file)
  _vmpPtr[(page-1)*431 + offset] → VCN tile index
  _vcnBlocks[vcnIdx * 32] → 8×8 pixel tile data

This script extracts wall types (uint8) from all 29 CMZ files, NOT uint16 tile IDs.
"""

import json
import struct
import os
import sys
from collections import Counter

sys.path.insert(0, '/home/bob')
from lol1_decompress_lcw import decompress_lcw

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_FILE = "/home/bob/lol1_wall_type_analysis.json"


def read_pak_entry(pak_path, offset, size):
    with open(pak_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def decompress_cmz(data):
    if len(data) < 12:
        return None
    # Try relative mode first (works for CMZ)
    compressed = b'\x00' + data[10:]
    result = decompress_lcw(compressed)
    if result is None:
        result = decompress_lcw(data[10:])
    return result


def analyze_cmz_blocks(decompressed):
    """Parse CMZ as ScummVM does: header then 1024 blocks."""
    if decompressed is None or len(decompressed) < 8:
        return None

    # ScummVM: uint16 len = READ_LE_UINT16(&h[4]); const uint8 *p = h + 6;
    # But _screen->loadBitmap processes it first. The raw decompressed data
    # after LCW has its own layout. Let's check the header.

    # Header bytes
    header_hex = decompressed[:6].hex()

    # Try ScummVM approach: len at offset 4, data at offset 6
    len_val = struct.unpack_from('<H', decompressed, 4)[0]

    result = {
        "header_hex": header_hex,
        "len_per_block": len_val,
        "decompressed_size": len(decompressed),
    }

    # Expected: 6 + 1024 * len_val should be close to decompressed_size
    expected_size = 6 + 1024 * len_val
    result["expected_data_size"] = expected_size
    result["size_match"] = abs(expected_size - len(decompressed)) < 16

    if not result["size_match"]:
        # Try without the 6-byte header offset - maybe header is different
        # Or maybe the data starts at a different offset
        for hdr_off in [0, 2, 4, 6, 8, 10]:
            for test_len in range(1, 20):
                if hdr_off + 1024 * test_len == len(decompressed):
                    result["alt_header_offset"] = hdr_off
                    result["alt_len_per_block"] = test_len
                    len_val = test_len
                    break

    # Extract wall types from blocks
    data_start = 6
    if "alt_header_offset" in result:
        data_start = result["alt_header_offset"]

    all_wall_types = Counter()
    blocks = []

    for i in range(1024):
        block_offset = data_start + i * len_val
        if block_offset + 4 > len(decompressed):
            break

        walls = [decompressed[block_offset + d] for d in range(min(4, len_val))]
        blocks.append(walls)

        for w in walls:
            all_wall_types[w] += 1

    result["n_blocks_parsed"] = len(blocks)
    result["unique_wall_types"] = sorted(all_wall_types.keys())
    result["wall_type_counts"] = {f"0x{k:02x}": v for k, v in sorted(all_wall_types.items())}

    # Sample first few blocks
    result["sample_blocks"] = [
        {"block": i, "walls": [f"0x{w:02x}" for w in b]}
        for i, b in enumerate(blocks[:10])
    ]

    # Extra bytes per block (beyond the 4 walls)
    if len_val > 4 and len(blocks) > 0:
        extra_samples = []
        for i in [0, 1, 100, 500, 1000]:
            if i < len(blocks):
                block_offset = data_start + i * len_val
                extra = decompressed[block_offset + 4: block_offset + len_val]
                extra_samples.append({
                    "block": i,
                    "extra_hex": extra.hex()
                })
        result["extra_bytes_samples"] = extra_samples

    return result


def main():
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    results = {}
    all_wall_types = set()

    for level_num in range(1, 30):
        pak_name = f"L{level_num:02d}.PAK"
        cmz_name = f"LEVEL{level_num}.CMZ"

        if pak_name not in index["pak_files"]:
            print(f"  SKIP: {pak_name} not in index")
            continue

        cmz_entry = None
        for entry in index["pak_files"][pak_name]["entries"]:
            if entry["name"] == cmz_name:
                cmz_entry = entry
                break

        if cmz_entry is None:
            continue

        pak_path = os.path.join(PAK_DIR, pak_name)
        if not os.path.exists(pak_path):
            print(f"  SKIP: {pak_path} not on disk")
            continue

        raw = read_pak_entry(pak_path, cmz_entry["offset"], cmz_entry["size"])
        decompressed = decompress_cmz(raw)

        if decompressed is None:
            print(f"  FAIL: Level {level_num} decompression failed")
            continue

        analysis = analyze_cmz_blocks(decompressed)
        if analysis is None:
            print(f"  FAIL: Level {level_num} block analysis failed")
            continue

        all_wall_types.update(analysis["unique_wall_types"])
        results[f"level{level_num:02d}"] = analysis

        n_types = len(analysis["unique_wall_types"])
        size_ok = "OK" if analysis["size_match"] else f"MISMATCH(exp={analysis['expected_data_size']})"
        print(f"  Level {level_num:2d}: len={analysis['len_per_block']} "
              f"blocks={analysis['n_blocks_parsed']} "
              f"wall_types={n_types} "
              f"size={size_ok} "
              f"decomp={analysis['decompressed_size']}")

    print(f"\n=== SUMMARY ===")
    print(f"Levels analyzed: {len(results)}")
    print(f"Total unique wall types: {len(all_wall_types)}")
    print(f"Wall type range: 0x{min(all_wall_types):02x} - 0x{max(all_wall_types):02x}")

    output = {
        "description": "LoL1 CMZ wall type analysis (corrected per ScummVM)",
        "format_notes": {
            "cmz_structure": "LCW-compressed; decompressed = header + 1024 blocks",
            "block_structure": "len bytes per block; first 4 = walls[N,E,S,W] as uint8",
            "wall_pipeline": "wall_type → WLL._wllVmpMap[type] → VMP page → VCN tile",
            "grid": "32×32 = 1024 blocks per level",
            "source": "ScummVM engines/kyra/engine/scene_lol.cpp loadBlockProperties()"
        },
        "all_unique_wall_types": sorted(all_wall_types),
        "per_level": results
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
