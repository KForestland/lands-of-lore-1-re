#!/usr/bin/env python3
"""Extract dialogue text from all ENG/FRE/GER files in the LoL1 PAK corpus."""

import json
import os
import struct

PAK_INDEX = "/home/bob/lol1_pak_index.json"
PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA/"
OUTPUT_DIR = "/home/bob/lol1_dialogue/"
SUMMARY_FILE = "/home/bob/lol1_dialogue_summary.json"

LANG_EXTENSIONS = (".ENG", ".FRE", ".GER")


def decode_string(raw_bytes):
    """Convert raw bytes to readable text with control code markers."""
    parts = []
    for b in raw_bytes:
        if b == 0x0D:
            parts.append("[CR]")
        elif b == 0x0A:
            parts.append("[LF]")
        elif 32 <= b < 127:
            parts.append(chr(b))
        else:
            parts.append(f"[{b:02X}]")
    return "".join(parts)


def extract_strings(data):
    """Parse uint16 offset table and extract null-terminated strings."""
    if len(data) < 2:
        return []

    # First uint16 is the offset to the first string, which tells us the table size
    first_offset = struct.unpack_from("<H", data, 0)[0]

    # Sanity check
    if first_offset < 2 or first_offset > len(data) or first_offset % 2 != 0:
        return []

    num_entries = first_offset // 2

    # Read all offsets
    offsets = []
    for i in range(num_entries):
        off = struct.unpack_from("<H", data, i * 2)[0]
        if off >= len(data):
            break
        offsets.append(off)

    # Extract strings
    strings = []
    for off in offsets:
        # Find null terminator
        null_pos = data.find(b"\x00", off)
        if null_pos == -1:
            null_pos = len(data)
        raw = data[off:null_pos]
        strings.append(decode_string(raw))

    return strings


def main():
    with open(PAK_INDEX) as f:
        index = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Collect all language file entries
    lang_files = []
    for pak_name, pak_info in index["pak_files"].items():
        for entry in pak_info["entries"]:
            if any(entry["name"].endswith(ext) for ext in LANG_EXTENSIONS):
                lang_files.append({
                    "pak": pak_name,
                    "name": entry["name"],
                    "offset": entry["offset"],
                    "size": entry["size"],
                })

    lang_files.sort(key=lambda x: x["name"])

    summary = {
        "total_files": len(lang_files),
        "total_strings": 0,
        "by_language": {"ENG": 0, "FRE": 0, "GER": 0},
        "files": [],
    }

    total_strings = 0

    for lf in lang_files:
        pak_path = os.path.join(PAK_DIR, lf["pak"])

        with open(pak_path, "rb") as f:
            f.seek(lf["offset"])
            data = f.read(lf["size"])

        strings = extract_strings(data)

        # Determine output filename
        base = lf["name"].rsplit(".", 1)[0].lower()
        ext = lf["name"].rsplit(".", 1)[1].lower()
        out_name = f"{base}_{ext}.json"

        result = {
            "file": lf["name"],
            "pak": lf["pak"],
            "string_count": len(strings),
            "strings": strings,
        }

        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        lang = ext.upper()
        summary["by_language"][lang] += len(strings)
        summary["files"].append({
            "file": lf["name"],
            "pak": lf["pak"],
            "output": out_name,
            "string_count": len(strings),
        })
        total_strings += len(strings)

        print(f"  {lf['name']:20s} ({lf['pak']:15s}) -> {len(strings):4d} strings -> {out_name}")

    summary["total_strings"] = total_strings

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(lang_files)} files processed, {total_strings} total strings.")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Summary: {SUMMARY_FILE}")

    # Per-language breakdown
    for lang, count in summary["by_language"].items():
        print(f"  {lang}: {count} strings")


if __name__ == "__main__":
    main()
