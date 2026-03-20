#!/usr/bin/env python3
"""Verify the current LoL1 TLK filename+offset directory hypothesis."""

from __future__ import annotations

import json
import statistics
import struct
from pathlib import Path

ROOT = Path("/media/bob/Arikv/REFERENCE/game_files/lol1/DATA")
OUT_DIR = Path("/home/bob/lol2_out/lol1_tlk_verify")
OUT_JSON = OUT_DIR / "lol1_tlk_verify.json"
OUT_MD = OUT_DIR / "lol1_tlk_verify.md"


def parse_tlk(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    directory_size = struct.unpack_from("<I", data, 0)[0]
    pos = 4
    entries = []
    errors: list[str] = []

    while pos < directory_size:
        end = data.find(b"\x00", pos)
        if end < 0 or end >= directory_size:
            errors.append(f"entry {len(entries)}: missing null terminator before directory end")
            break
        if end + 5 > directory_size:
            errors.append(f"entry {len(entries)}: offset field crosses directory end")
            break
        name_bytes = data[pos:end]
        try:
            name = name_bytes.decode("ascii")
        except UnicodeDecodeError:
            name = name_bytes.decode("ascii", errors="replace")
            errors.append(f"entry {len(entries)}: non-ascii name bytes")
        offset = struct.unpack_from("<I", data, end + 1)[0]
        if not name and offset == 0 and end + 5 == directory_size:
            pos = directory_size
            break
        entries.append({"index": len(entries), "name": name, "offset": offset})
        pos = end + 5
    if pos != directory_size:
        errors.append(f"parser stopped at {pos}, directory size says {directory_size}")

    if entries:
        offsets = [entry["offset"] for entry in entries]
        if offsets != sorted(offsets):
            errors.append("offsets are not monotonic")
        if offsets[0] <= directory_size:
            errors.append(
                f"first payload offset {offsets[0]} does not land after directory end {directory_size}"
            )
        prev_end = offsets[0]
        for idx, entry in enumerate(entries):
            next_offset = offsets[idx + 1] if idx + 1 < len(offsets) else len(data)
            entry["size"] = next_offset - entry["offset"]
            if entry["offset"] < directory_size:
                errors.append(f"entry {idx}: payload overlaps directory")
            if next_offset > len(data):
                errors.append(f"entry {idx}: next offset beyond file end")
            if entry["size"] < 0:
                errors.append(f"entry {idx}: negative size")
            prev_end = next_offset

    ascii_name_count = sum(
        1 for entry in entries if entry["name"] and all(32 <= ord(ch) < 127 for ch in entry["name"])
    )
    voc_like_count = sum(1 for entry in entries if entry["name"].upper().endswith(".VOC"))
    dotted_count = sum(1 for entry in entries if "." in entry["name"])
    first_payload_header = data[entries[0]["offset"]:entries[0]["offset"] + 32].decode(
        "ascii", errors="replace"
    ) if entries else ""

    return {
        "file": path.name,
        "size": len(data),
        "directory_size": directory_size,
        "entries_parsed": len(entries),
        "directory_end_probe": pos,
        "ascii_name_fraction": round(ascii_name_count / len(entries), 4) if entries else 0.0,
        "voc_like_fraction": round(voc_like_count / len(entries), 4) if entries else 0.0,
        "dotted_name_fraction": round(dotted_count / len(entries), 4) if entries else 0.0,
        "first_payload_header": first_payload_header,
        "sample_entries": entries[:5],
        "errors": errors,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [parse_tlk(path) for path in sorted(ROOT.glob("*.TLK"))]
    directory_end_values = [item["directory_end_probe"] for item in results]
    dir_sizes = [item["directory_size"] for item in results]
    all_clean = all(not item["errors"] for item in results)
    all_dir_match = all(item["directory_size"] == item["directory_end_probe"] for item in results)

    payload = {
        "file_count": len(results),
        "all_clean": all_clean,
        "all_directory_size_match": all_dir_match,
        "directory_end_probe_min": min(directory_end_values) if directory_end_values else None,
        "directory_end_probe_max": max(directory_end_values) if directory_end_values else None,
        "directory_end_probe_mode_like": statistics.mode(directory_end_values) if directory_end_values else None,
        "directory_size_min": min(dir_sizes) if dir_sizes else None,
        "directory_size_max": max(dir_sizes) if dir_sizes else None,
        "files": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# LoL1 TLK Verification",
        "",
        "Corpus check for the current LoL1 TLK filename-plus-offset directory hypothesis.",
        "",
        f"- files checked: `{payload['file_count']}`",
        f"- all clean: `{payload['all_clean']}`",
        f"- all directory-size matches: `{payload['all_directory_size_match']}`",
        f"- directory_end_probe range: `{payload['directory_end_probe_min']}..{payload['directory_end_probe_max']}`",
        f"- directory_end_probe mode-like: `{payload['directory_end_probe_mode_like']}`",
        f"- directory-size range: `{payload['directory_size_min']}..{payload['directory_size_max']}`",
        "",
    ]
    for item in results:
        lines.append(f"## {item['file']}")
        lines.append(f"- directory size: `{item['directory_size']}`")
        lines.append(f"- parsed entries: `{item['entries_parsed']}`")
        lines.append(f"- directory end probe: `{item['directory_end_probe']}`")
        lines.append(f"- ascii-name fraction: `{item['ascii_name_fraction']}`")
        lines.append(f"- dotted-name fraction: `{item['dotted_name_fraction']}`")
        lines.append(f"- `.VOC`-suffix fraction: `{item['voc_like_fraction']}`")
        lines.append(f"- first payload header: `{item['first_payload_header']}`")
        if item["sample_entries"]:
            preview = ", ".join(
                f"`{entry['name']}`@{entry['offset']}" for entry in item["sample_entries"][:3]
            )
            lines.append(f"- sample entries: {preview}")
        if item["errors"]:
            lines.append("- errors:")
            for err in item["errors"]:
                lines.append(f"  - {err}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
