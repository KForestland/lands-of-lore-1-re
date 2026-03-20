#!/usr/bin/env python3
"""Parse LoL1 TIM files from PAK containers and document their IFF chunk structure."""

import json
import struct
import os
import sys

DATA_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
PAK_INDEX = "/home/bob/lol1_pak_index.json"
OUTPUT = "/home/bob/lol1_tim_analysis.json"

def read_pak_entry(pak_path, offset, size):
    """Read a single entry from a PAK file."""
    with open(pak_path, "rb") as f:
        f.seek(offset)
        return f.read(size)

def parse_iff_chunks(data):
    """Parse IFF/FORM container, return list of chunks."""
    result = {
        "raw_size": len(data),
        "is_iff": False,
        "form_type": None,
        "form_size": None,
        "chunks": [],
        "errors": []
    }

    if len(data) < 12:
        result["errors"].append(f"Too small for IFF: {len(data)} bytes")
        return result

    # Check for FORM header
    magic = data[0:4]
    if magic != b"FORM":
        result["errors"].append(f"No FORM magic, got: {magic!r}")
        # Try to see if it starts with a known chunk type directly
        return result

    result["is_iff"] = True
    form_size = struct.unpack(">I", data[4:8])[0]  # IFF uses big-endian sizes
    form_type = data[8:12].decode("ascii", errors="replace")
    result["form_type"] = form_type
    result["form_size"] = form_size

    # Parse chunks within FORM
    pos = 12  # After FORM header + type
    end = min(8 + form_size, len(data))  # form_size includes type + chunks

    while pos + 8 <= end:
        chunk_id = data[pos:pos+4]
        try:
            chunk_id_str = chunk_id.decode("ascii")
        except:
            chunk_id_str = chunk_id.hex()

        chunk_size = struct.unpack(">I", data[pos+4:pos+8])[0]

        chunk_data_start = pos + 8
        chunk_data_end = min(chunk_data_start + chunk_size, len(data))
        chunk_data = data[chunk_data_start:chunk_data_end]

        chunk_info = {
            "id": chunk_id_str,
            "offset": pos,
            "size": chunk_size,
            "actual_data_size": len(chunk_data),
            "first_bytes_hex": chunk_data[:32].hex() if chunk_data else "",
        }

        # Decode known chunk types
        if chunk_id_str == "TEXT":
            # Null-terminated strings
            try:
                text_content = chunk_data.decode("ascii", errors="replace")
                # Split on null bytes
                strings = [s for s in text_content.split("\x00") if s]
                chunk_info["strings"] = strings
            except:
                pass

        elif chunk_id_str == "AVTL":
            # Array of uint16 LE values — instruction/opcode data
            n_words = chunk_size // 2
            words = []
            for i in range(min(n_words, len(chunk_data)//2)):
                w = struct.unpack_from("<H", chunk_data, i*2)[0]
                words.append(w)
            chunk_info["num_words"] = n_words
            chunk_info["words"] = words
            # First N values are function entry point offsets (up to 10)
            if words:
                num_funcs = min(10, n_words)
                # Find how many function pointers there are
                # Function pointers are offsets into the AVTL array itself
                entry_points = []
                for i in range(num_funcs):
                    if i < len(words) and words[i] < n_words:
                        entry_points.append(words[i])
                    else:
                        break
                chunk_info["function_entry_points"] = entry_points

        result["chunks"].append(chunk_info)

        # IFF chunks are padded to even size
        padded_size = chunk_size + (chunk_size & 1)
        pos = chunk_data_start + padded_size

    return result

def decode_avtl_instructions(words, entry_points):
    """Attempt to decode AVTL instruction stream.

    From ScummVM: instructions are [length][delay][opcode][params...]
    where opcode is at ip[2] & 0xFF
    """
    instructions = []

    for func_idx, ep in enumerate(entry_points):
        func_instrs = []
        ip = ep
        max_steps = 200  # safety limit
        steps = 0
        while ip < len(words) and steps < max_steps:
            steps += 1
            instr_len = words[ip] if ip < len(words) else 0
            if instr_len == 0:
                func_instrs.append({"offset": ip, "type": "END"})
                break

            delay = words[ip+1] if ip+1 < len(words) else 0
            opcode_word = words[ip+2] if ip+2 < len(words) else 0
            opcode = opcode_word & 0xFF

            params = []
            for p in range(3, instr_len):
                if ip+p < len(words):
                    params.append(words[ip+p])

            func_instrs.append({
                "offset": ip,
                "length": instr_len,
                "delay": delay,
                "opcode": opcode,
                "params": params
            })

            ip += instr_len

        instructions.append({
            "function_index": func_idx,
            "entry_point": ep,
            "instructions": func_instrs
        })

    return instructions


def main():
    with open(PAK_INDEX) as f:
        pak_index = json.load(f)

    # Collect all TIM files
    tim_files = []
    for pak_name, pak_info in pak_index["pak_files"].items():
        for entry in pak_info["entries"]:
            if entry["name"].upper().endswith(".TIM"):
                tim_files.append({
                    "pak": pak_name,
                    "name": entry["name"],
                    "offset": entry["offset"],
                    "size": entry["size"]
                })

    tim_files.sort(key=lambda x: (x["pak"], x["name"]))

    # Select a diverse sample of ~10 from different PAKs
    # Pick from: O00A (utility), O01A (dialogue), O01B, O01C, O01E, O02A, O03C, O08A, O17A, O27A
    sample_selection = [
        ("O00A.PAK", "AUTOMAP.TIM"),
        ("O00A.PAK", "BARRIER.TIM"),
        ("O01A.PAK", "NATE1.TIM"),
        ("O01A.PAK", "VICTOR1.TIM"),
        ("O01C.PAK", "TALAMSCA.TIM"),
        ("O01E.PAK", "KING1.TIM"),
        ("O02A.PAK", "SCOTIA1.TIM"),
        ("O03C.PAK", "BUCK01.TIM"),
        ("O08A.PAK", "DRARCLE2.TIM"),
        ("O17A.PAK", "HAG_S.TIM"),
        ("O27A.PAK", "ESCAPE.TIM"),
    ]

    sample_keys = {(pak, name) for pak, name in sample_selection}

    # Parse ALL TIM files but do detailed analysis on the sample
    all_results = []
    chunk_type_stats = {}
    form_type_stats = {}
    size_stats = {"min": 999999, "max": 0, "total": 0}

    for tf in tim_files:
        pak_path = os.path.join(DATA_DIR, tf["pak"])
        if not os.path.exists(pak_path):
            continue

        data = read_pak_entry(pak_path, tf["offset"], tf["size"])
        parsed = parse_iff_chunks(data)

        is_sample = (tf["pak"], tf["name"]) in sample_keys

        # Stats
        size_stats["min"] = min(size_stats["min"], tf["size"])
        size_stats["max"] = max(size_stats["max"], tf["size"])
        size_stats["total"] += tf["size"]

        if parsed["form_type"]:
            form_type_stats[parsed["form_type"]] = form_type_stats.get(parsed["form_type"], 0) + 1

        for chunk in parsed["chunks"]:
            cid = chunk["id"]
            chunk_type_stats[cid] = chunk_type_stats.get(cid, 0) + 1

        entry = {
            "pak": tf["pak"],
            "name": tf["name"],
            "size": tf["size"],
            "is_iff": parsed["is_iff"],
            "form_type": parsed["form_type"],
            "chunk_ids": [c["id"] for c in parsed["chunks"]],
            "chunk_sizes": {c["id"]: c["size"] for c in parsed["chunks"]},
        }

        if is_sample:
            entry["detailed"] = True
            entry["chunks"] = parsed["chunks"]

            # Decode AVTL instructions for sample files
            for chunk in parsed["chunks"]:
                if chunk["id"] == "AVTL" and "function_entry_points" in chunk:
                    decoded = decode_avtl_instructions(
                        chunk["words"],
                        chunk["function_entry_points"]
                    )
                    chunk["decoded_functions"] = decoded

            if parsed["errors"]:
                entry["errors"] = parsed["errors"]

        all_results.append(entry)

    # Build summary
    analysis = {
        "description": "LoL1 TIM file format analysis",
        "format_notes": {
            "container": "IFF FORM",
            "form_type": "AVFS (Animation/Video File Script)",
            "chunks_found": list(chunk_type_stats.keys()),
            "scummvm_reference": {
                "interpreter": "TIMInterpreter (script_tim.cpp)",
                "struct": "TIM struct with kCountFuncs=10 functions, kWSASlots=6 animation slots",
                "TEXT_chunk": "Null-terminated ASCII strings (dialogue text, filenames)",
                "AVTL_chunk": "Array of uint16 LE values. First N values are function entry-point offsets into the array. Instructions at those offsets: [length][delay][opcode][params...]. Opcode is ip[2]&0xFF. Up to 10 concurrent functions.",
                "execution": "TIMInterpreter dispatches opcodes to game-specific opcode tables (intro/outro/ingame)"
            }
        },
        "statistics": {
            "total_tim_files": len(tim_files),
            "total_parsed": len(all_results),
            "form_types": form_type_stats,
            "chunk_type_counts": chunk_type_stats,
            "size_min": size_stats["min"],
            "size_max": size_stats["max"],
            "size_avg": round(size_stats["total"] / len(all_results), 1) if all_results else 0,
            "size_total": size_stats["total"],
            "paks_containing_tim": len(set(t["pak"] for t in tim_files))
        },
        "files": all_results
    }

    with open(OUTPUT, "w") as f:
        json.dump(analysis, f, indent=2)

    # Print summary
    print(f"Parsed {len(all_results)}/{len(tim_files)} TIM files")
    print(f"\nFORM types: {form_type_stats}")
    print(f"Chunk types: {chunk_type_stats}")
    print(f"Size range: {size_stats['min']} - {size_stats['max']} bytes (avg {analysis['statistics']['size_avg']})")
    print(f"\nSample file details:")
    for entry in all_results:
        if entry.get("detailed"):
            print(f"\n  {entry['pak']}/{entry['name']} ({entry['size']} bytes)")
            print(f"    FORM type: {entry['form_type']}")
            for chunk in entry.get("chunks", []):
                print(f"    Chunk: {chunk['id']} size={chunk['size']}")
                if chunk["id"] == "TEXT" and "strings" in chunk:
                    for s in chunk["strings"][:5]:
                        print(f"      string: {s!r}")
                    if len(chunk.get("strings", [])) > 5:
                        print(f"      ... ({len(chunk['strings'])} total)")
                if chunk["id"] == "AVTL" and "decoded_functions" in chunk:
                    for func in chunk["decoded_functions"]:
                        n = len(func["instructions"])
                        opcodes_used = set(i.get("opcode", -1) for i in func["instructions"] if i.get("type") != "END")
                        print(f"      func[{func['function_index']}] ep={func['entry_point']}: {n} instructions, opcodes={sorted(opcodes_used)}")

    print(f"\nOutput saved to {OUTPUT}")

if __name__ == "__main__":
    main()
