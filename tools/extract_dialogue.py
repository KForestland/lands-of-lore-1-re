#!/usr/bin/env python3
"""Extract the raw strings of every ENG/FRE/GER text file in the LoL1 PAKs.

Layout (docs/formats/text.md; ScummVM LoLEngine::getTableEntry
engines/kyra/engine/lol.cpp:1100-1104): uint16 offsets, count = first / 2,
NUL-terminated strings. Output keeps the bytes as text with [XX] for
non-ASCII bytes; decode_dialogue.py turns them into readable text.

  extract_dialogue.py --out-dir dialogue/   # one JSON per file + summary.json
  extract_dialogue.py --check               # counts vs data/dialogue_summary.json
"""

from cli_errors import run_cli
import json
import os
import struct

import lol1lib as L

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
    ap = L.tool_args(__doc__)
    ap.add_argument("--out-dir", help="write one JSON per text file and summary.json here")
    a = ap.parse_args()
    files = []
    for pak, name, data in L.find_all("", a.data):
        if name.endswith(LANG_EXTENSIONS):
            files.append((name, pak, extract_strings(data)))
    files.sort()
    summary = {"total_files": len(files), "total_strings": 0,
               "by_language": {"ENG": 0, "FRE": 0, "GER": 0}, "files": []}
    for name, pak, strings in files:
        base, ext = name.rsplit(".", 1)
        out_name = f"{base.lower()}_{ext.lower()}.json"
        summary["by_language"][ext] += len(strings)
        summary["total_strings"] += len(strings)
        summary["files"].append({"file": name, "pak": pak, "output": out_name, "string_count": len(strings)})
        if a.out_dir:
            os.makedirs(a.out_dir, exist_ok=True)
            with open(os.path.join(a.out_dir, out_name), "w", encoding="utf-8") as f:
                json.dump({"file": name, "pak": pak, "string_count": len(strings), "strings": strings},
                          f, indent=2, ensure_ascii=False)
    if a.check:
        ref = L.repo_json("dialogue_summary.json", a.data)
        key = lambda d: sorted((x["file"], x["pak"], x["string_count"]) for x in d["files"])
        skipped = ref is None
        same = skipped or key(ref) == key(summary) and ref["by_language"] == summary["by_language"]
        print(f"CHECK dialogue: {summary['total_files']} files, {summary['total_strings']} strings "
              f"{summary['by_language']}, matches data/dialogue_summary.json: {'skipped (not the CD layout)' if skipped else same}")
        return 0 if same else 1
    if a.out_dir:
        with open(os.path.join(a.out_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)
        print(f"wrote {len(files)} files to {a.out_dir}")
    print(f"{summary['total_files']} files, {summary['total_strings']} strings, {summary['by_language']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
