#!/usr/bin/env python3
"""
LoL1 WLL Parser + Wall-to-VMP Mapping (ScummVM-verified)

WLL file format (from ScummVM loadLevelWallData):
  Bytes 0-1: uint16 shape_list_index → indexes into _levelShpList/_levelDatList
  Then N records of 12 bytes each ((file_size - 2) / 12):
    [0-1] uint16 wall_type_id
    [2]   uint8  vmp_map_value  → _wllVmpMap[wall_type_id]
    [3]   (skipped)
    [4-5] int16  shape_map     → _wllShapeMap[wall_type_id]
    [6]   uint8  special_type  → _specialWallTypes[wall_type_id]
    [7]   (skipped)
    [8]   uint8  wall_flags    → _wllWallFlags[wall_type_id]
    [9]   (skipped)
    [10]  uint8  automap_data  → _wllAutomapData[wall_type_id]
    [11]  (skipped)

VMP mapping: _wllVmpMap[wall_type] → VMP page (1-indexed)
  VMP tile data: _vmpPtr[(_wllVmpMap[c] - 1) * 431 + offset]
  Each VMP page = 431 uint16 entries = one wall face's tiles
"""

import json
import struct
import os
import sys

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_FILE = "/home/bob/lol1_wll_parsed.json"


def read_pak_entry(pak_path, offset, size):
    with open(pak_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def parse_wll(data):
    """Parse WLL file per ScummVM format."""
    if len(data) < 14:  # At least header + 1 record
        return None

    shape_list_idx = struct.unpack_from('<H', data, 0)[0]
    n_records = (len(data) - 2) // 12

    records = {}
    for i in range(n_records):
        off = 2 + i * 12
        wall_type_id = struct.unpack_from('<H', data, off)[0]
        vmp_map = data[off + 2]
        shape_map = struct.unpack_from('<h', data, off + 4)[0]  # signed int16
        special_type = data[off + 6]
        wall_flags = data[off + 8]
        automap_data = data[off + 10]

        records[wall_type_id] = {
            "vmp_map": vmp_map,
            "shape_map": shape_map,
            "special_type": special_type,
            "wall_flags": wall_flags,
            "automap_data": automap_data,
        }

    return {
        "shape_list_index": shape_list_idx,
        "n_records": n_records,
        "records": records,
    }


def main():
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)

    all_results = {}
    # Collect cross-level stats
    vmp_map_values = set()
    wall_type_to_vmp = {}

    for level_num in range(1, 30):
        pak_name = f"L{level_num:02d}.PAK"
        wll_name = f"LEVEL{level_num}.WLL"

        if pak_name not in index["pak_files"]:
            continue

        wll_entry = None
        for entry in index["pak_files"][pak_name]["entries"]:
            if entry["name"] == wll_name:
                wll_entry = entry
                break

        if wll_entry is None:
            continue

        pak_path = os.path.join(PAK_DIR, pak_name)
        if not os.path.exists(pak_path):
            continue

        raw = read_pak_entry(pak_path, wll_entry["offset"], wll_entry["size"])
        parsed = parse_wll(raw)

        if parsed is None:
            print(f"  Level {level_num}: parse failed")
            continue

        # Collect VMP map stats
        n_with_vmp = 0
        n_without = 0
        for wt, rec in parsed["records"].items():
            if rec["vmp_map"] > 0:
                n_with_vmp += 1
                vmp_map_values.add(rec["vmp_map"])
                if wt not in wall_type_to_vmp:
                    wall_type_to_vmp[wt] = {}
                wall_type_to_vmp[wt][level_num] = rec["vmp_map"]
            else:
                n_without += 1

        print(f"  Level {level_num:2d}: shape_idx={parsed['shape_list_index']} "
              f"records={parsed['n_records']} "
              f"with_vmp={n_with_vmp} without={n_without}")

        # Store in results (convert int keys to strings for JSON)
        level_result = {
            "shape_list_index": parsed["shape_list_index"],
            "n_records": parsed["n_records"],
            "wall_types": {}
        }
        for wt, rec in sorted(parsed["records"].items()):
            level_result["wall_types"][f"0x{wt:02x}"] = rec
        all_results[f"level{level_num:02d}"] = level_result

    # Summary
    print(f"\n=== CROSS-LEVEL SUMMARY ===")
    print(f"Unique VMP map values: {sorted(vmp_map_values)}")
    print(f"Max VMP page: {max(vmp_map_values) if vmp_map_values else 0}")

    # Show wall types that have VMP mapping (these are the visible walls)
    print(f"\nWall types with VMP mapping (visible geometry):")
    for wt in sorted(wall_type_to_vmp.keys()):
        vmp_vals = wall_type_to_vmp[wt]
        # Check if VMP value is consistent across levels
        unique_vmp = set(vmp_vals.values())
        levels = sorted(vmp_vals.keys())
        if len(unique_vmp) == 1:
            print(f"  wall 0x{wt:02x}: vmp={list(unique_vmp)[0]:2d} "
                  f"(consistent across {len(levels)} levels)")
        else:
            print(f"  wall 0x{wt:02x}: vmp varies {dict(sorted(vmp_vals.items()))} "
                  f"({len(levels)} levels)")

    output = {
        "description": "LoL1 WLL parsed data — wall type definitions per level",
        "format": {
            "source": "ScummVM engines/kyra/engine/scene_lol.cpp loadLevelWallData()",
            "record_size": 12,
            "fields": [
                "uint16 wall_type_id",
                "uint8 vmp_map (VMP page, 1-indexed; 0=no geometry)",
                "int16 shape_map (decoration shape index)",
                "uint8 special_type",
                "uint8 wall_flags",
                "uint8 automap_data"
            ],
            "vmp_usage": "_vmpPtr[(_wllVmpMap[wallType] - 1) * 431 + offset]"
        },
        "cross_level_vmp_values": sorted(vmp_map_values),
        "wall_type_vmp_consistency": {
            f"0x{wt:02x}": {
                "vmp_values": sorted(set(v.values())),
                "consistent": len(set(v.values())) == 1,
                "n_levels": len(v)
            }
            for wt, v in sorted(wall_type_to_vmp.items())
        },
        "per_level": all_results
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
