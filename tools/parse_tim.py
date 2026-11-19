#!/usr/bin/env python3
"""Parse LoL1 TIM files from PAK containers and document their IFF chunk structure."""

import json
import struct
import os
import sys

import sys

import lol1lib as L

USAGE = """
  parse_tim.py                     # summary + sample files
  parse_tim.py --out tim.json      # same shape as data/tim_analysis.json (raw script words left out;
                                   # --with-words keeps them for local study)
  parse_tim.py --check             # rebuild and compare with data/tim_analysis.json; on the CD
                                   # also re-count the commands of docs/unknowns/06_tim_opcodes.md
  parse_tim.py --list AUTOMAP.TIM  # one TIM file command by command, with the command names
                                   # of docs/unknowns/06_tim_opcodes.md (prints to stdout only)
See docs/formats/tim.md and docs/unknowns/06_tim_opcodes.md.
"""

# Command names: docs/unknowns/06_tim_opcodes.md, "LoL command table" (script_tim.cpp:853-892).
TIM_COMMANDS = {
    0x00: "cmd_initFunc0", 0x01: "cmd_stopAllFuncs", 0x02: "cmd_initWSA", 0x03: "cmd_uninitWSA",
    0x04: "cmd_initFunc", 0x05: "cmd_stopFunc", 0x06: "cmd_wsaDisplayFrame", 0x07: "unimplemented on LoL",
    0x08: "cmd_loadVocFile", 0x09: "cmd_unloadVocFile", 0x0A: "cmd_playVocFile", 0x0B: "unimplemented",
    0x0C: "cmd_loadSoundFile", 0x0D: "cmd_return(1)", 0x0E: "cmd_playMusicTrack", 0x0F: "unimplemented",
    0x10: "cmd_return(1)", 0x11: "cmd_return(1)", 0x12: "unimplemented", 0x13: "unimplemented",
    0x14: "cmd_setLoopIp", 0x15: "cmd_continueLoop", 0x16: "cmd_resetLoopIp", 0x17: "cmd_resetAllRuntimes",
    0x18: "cmd_return(1)", 0x19: "cmd_execOpcode", 0x1A: "cmd_initFuncNow", 0x1B: "cmd_stopFuncNow",
    0x1C: "cmd_processDialogue", 0x1D: "cmd_dialogueBox", 0x1E: "cmd_return(n1)",
}
# The floppy intro and outro run the base table (TIMInterpreter); the page names these two differently.
TIM_BASE_DIFFERENT = {0x01: "cmd_stopCurFunc", 0x07: "cmd_displayText"}
# Parameter names, same table ("Parameters" column).
TIM_PARAMS = {
    0x02: ("index", "string_id", "x", "y", "offscreen", "flags"), 0x03: ("index",), 0x04: ("function",),
    0x05: ("function",), 0x06: ("slot", "frame"), 0x08: ("string_id", "index"), 0x09: ("index",),
    0x0A: ("index", "volume"), 0x0C: ("string_id",), 0x0E: ("track",), 0x15: ("factor",),
    0x1A: ("function",), 0x1B: ("function",), 0x1D: ("function", "string_id", "string_id", "string_id"),
}
# Commands whose string id is a TEXT-chunk string (script_tim.cpp:643,703,756).
TIM_TEXT_PARAM = {0x02: 1, 0x08: 0, 0x0C: 0}
# Nested 0x19 functions: in-game (script_lol.cpp:3020-3048), intro (:2978-2991), outro (:2993-3018).
TIM_NESTED = {
    "in-game": ["tlol_initSceneWindowDialogue", "tlol_restoreAfterSceneWindowDialogue", "unimplemented",
                "tlol_giveItem", "tlol_setPartyPosition", "tlol_fadeClearWindow", "tlol_copyRegion",
                "tlol_characterChat", "tlol_drawScene", "tlol_update", "tlol_clearTextField",
                "tlol_loadSoundFile", "tlol_playMusicTrack", "tlol_playDialogueTalkText",
                "tlol_playSoundEffect", "tlol_startBackgroundAnimation", "tlol_stopBackgroundAnimation"],
    "intro": ["tlol_setupPaletteFade", "unimplemented", "tlol_loadPalette", "tlol_setupPaletteFadeEx",
              "tlol_processWsaFrame", "tlol_displayText", "unimplemented", "unimplemented"],
    "outro": ["tlol_setupPaletteFade", "unimplemented", "tlol_loadPalette", "tlol_setupPaletteFadeEx",
              "unimplemented", "tlol_fadeInScene", "tlol_unusedResourceFunc", "tlol_unusedResourceFunc",
              "tlol_fadeInPalette", "unimplemented", "unimplemented", "tlol_fadeOutSound",
              "tlol_displayAnimFrame", "tlol_delayForChat", "tlol_displayText", "unimplemented"],
}
# Uses / files of each command in the 139 CD files: docs/formats/tim.md and 06 ("Uses", "Files").
DOC_CD_USES = {0x01: (139, 139), 0x02: (74, 50), 0x03: (60, 43), 0x06: (4658, 138), 0x07: (2, 1),
               0x14: (175, 118), 0x15: (175, 118), 0x17: (170, 76), 0x18: (88, 59), 0x19: (807, 67),
               0x1D: (113, 56)}
# Floppy intro and outro command counts: 06, "Intro opcodes" and "Outro opcodes".
DOC_FLOPPY_USES = {
    "LOLINTRO.TIM": {0x01: 3, 0x02: 14, 0x03: 16, 0x06: 1022, 0x08: 28, 0x09: 28, 0x0A: 100, 0x0C: 1, 0x0E: 1,
                     0x14: 2, 0x15: 2, 0x17: 12, 0x18: 12, 0x19: 83, 0x1A: 3, 0x1B: 3},
    "LOLFINAL.TIM": {0x01: 3, 0x02: 12, 0x03: 11, 0x06: 194, 0x07: 1, 0x08: 10, 0x09: 10, 0x0A: 28, 0x0C: 1,
                     0x0E: 3, 0x14: 2, 0x15: 2, 0x17: 9, 0x18: 10, 0x19: 110, 0x1A: 2, 0x1B: 2},
}


def tim_chunks(data):
    """{chunk id: bytes} of a TIM (IFF FORM AVFS) file."""
    if data[:4] != b"FORM" or len(data) < 12:
        raise ValueError("no FORM header")
    out = {}
    pos, end = 12, min(8 + struct.unpack_from(">I", data, 4)[0], len(data))
    while pos + 8 <= end:
        cid = data[pos:pos + 4].decode("latin-1")
        size = struct.unpack_from(">I", data, pos + 4)[0]
        out[cid] = data[pos + 8:pos + 8 + size]
        pos += 8 + size + (size & 1)
    return out


def tim_function_count(words):
    """Entry words at the start of AVTL: the first count words whose smallest value is count."""
    for count in range(1, 11):
        if count <= len(words) and min(words[:count]) == count:
            return count
    return 1


def walk_avtl(words):
    """Walk each function from its entry word (docs/unknowns/06_tim_opcodes.md): an instruction is
    taken while its length is 3..32 words, its opcode-word high byte is 1 and the opcode is at most 0x1E.
    A function also ends where another function's entry word starts, so no instruction is listed twice.
    Returns (instructions, stops); an instruction is (function, word index, length, delay, opcode word,
    parameters); stops counts functions ended by a failing word rather than the end of AVTL."""
    out, stops = [], 0
    nf = tim_function_count(words)
    entries = set(words[:nf])
    for f in range(nf):
        ip = words[f] if f < len(words) else len(words)
        seen = set()
        while ip < len(words) and ip not in seen and (ip == words[f] or ip not in entries):
            seen.add(ip)
            length = words[ip]
            if not 3 <= length <= 32 or ip + length > len(words) or words[ip + 2] >> 8 != 1 \
                    or (words[ip + 2] & 0xFF) > 0x1E:
                stops += 1
                break
            out.append((f, ip, length, words[ip + 1], words[ip + 2], list(words[ip + 3:ip + length])))
            ip += length
    return out, stops


def tim_text(text, sid):
    """TEXT string number sid: a uint16 LE offset table, then C strings."""
    if text is None or 2 * sid + 2 > len(text):
        return None
    off = struct.unpack_from("<H", text, 2 * sid)[0]
    if off >= len(text):
        return None
    end = text.find(b"\0", off)
    return text[off:end if end >= 0 else len(text)].decode("latin-1")


def tim_listing(name, data):
    """Lines of a command-by-command listing of one TIM file."""
    ch = tim_chunks(data)
    avtl, text = ch.get("AVTL", b""), ch.get("TEXT")
    words = [struct.unpack_from("<H", avtl, i * 2)[0] for i in range(len(avtl) // 2)]
    up = name.upper()
    table = "intro" if up == "LOLINTRO.TIM" else "outro" if up == "LOLFINAL.TIM" else "in-game"
    nested = TIM_NESTED[table]
    instrs, stops = walk_avtl(words)
    nf = tim_function_count(words)
    lines = [f"{name}: AVTL {len(words)} words, {nf} function(s) at word(s) {words[:nf]}, "
             f"TEXT {'none' if text is None else str(len(text)) + ' bytes'}, {table} table"
             + (" (base table: 0x01 and 0x07 named as on the page)" if table != "in-game" else "")]
    lines.append("word  fn len delay opcode command parameters")
    for f, ip, length, delay, opw, params in instrs:
        op = opw & 0xFF
        cmd = TIM_COMMANDS[op] if table == "in-game" else TIM_BASE_DIFFERENT.get(op, TIM_COMMANDS[op])
        if op == 0x19 and params:
            sel = params[0]
            fn = nested[sel] if sel < len(nested) else "past the registered list"
            ps = f"nested 0x{sel:02X} {fn} args {params[1:]}"
        elif op in TIM_PARAMS:
            names = TIM_PARAMS[op]
            parts = [f"{names[i] if i < len(names) else 'word' + str(i)}={v}" for i, v in enumerate(params)]
            if op in TIM_TEXT_PARAM and TIM_TEXT_PARAM[op] < len(params):
                s = tim_text(text, params[TIM_TEXT_PARAM[op]])
                if s is not None:
                    parts[TIM_TEXT_PARAM[op]] += f' "{s}"'
            ps = " ".join(parts)
        else:
            ps = " ".join(str(v) for v in params)
        lines.append(f"{ip:4d}  {f:2d} {length:3d} {delay:5d} 0x{opw:04X} {cmd} {ps}".rstrip())
    lines.append(f"{len(instrs)} instructions, walk stops before the end of AVTL: {stops}")
    return lines

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
    ap = L.tool_args((__doc__ or "") + USAGE)
    ap.add_argument("--list", metavar="NAME.TIM", help="print one TIM file command by command")
    ap.add_argument("--with-words", action="store_true",
                    help="keep the raw AVTL words, decoded instructions and TEXT strings of the sample files in --out "
                         "(left out by default: they copy game script content)")
    a = ap.parse_args()
    if a.list:
        pak, blob = L.find_member(a.list, a.data, a.pak)
        print(f"{a.list.upper()} in {pak}")
        print("\n".join(tim_listing(a.list, blob)))
        return 0
    DATA_DIR = a.data
    tim_files = []
    for pak_name in L.list_paks(a.data):
        blob = open(os.path.join(a.data, pak_name), "rb").read()
        for name, off, size in L.pak_entries(blob):
            if name.upper().endswith(".TIM"):
                tim_files.append({"pak": pak_name, "name": name, "offset": off, "size": size})

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

    if not a.with_words:
        for f in analysis["files"]:
            for c in f.get("chunks", []):
                for k in ("words", "decoded_functions", "strings", "first_bytes_hex"):
                    c.pop(k, None)
    if a.check:
        ref = L.repo_json("tim_analysis.json", a.data)
        # compare what this tool produces (files and statistics)
        new = json.loads(json.dumps(analysis))
        skipped = ref is None
        same = skipped or new["files"] == ref["files"] and all(
            ref["statistics"].get(k) == v for k, v in new["statistics"].items())
        st = analysis["statistics"]
        # command-by-command walk of every distinct TIM name (docs/unknowns/06_tim_opcodes.md)
        uses, files, stops, seen, seq_ok, seq_n = {}, {}, 0, set(), True, 0
        for tf in tim_files:
            if tf["name"].upper() in seen:
                continue
            seen.add(tf["name"].upper())
            blob = read_pak_entry(os.path.join(DATA_DIR, tf["pak"]), tf["offset"], tf["size"])
            words = tim_chunks(blob).get("AVTL", b"")
            instrs, n = walk_avtl([struct.unpack_from("<H", words, i * 2)[0] for i in range(len(words) // 2)])
            stops += n
            if tf["name"].upper() in DOC_FLOPPY_USES:
                got = {}
                for i in instrs:
                    got[i[4] & 0xFF] = got.get(i[4] & 0xFF, 0) + 1
                seq_ok = seq_ok and got == DOC_FLOPPY_USES[tf["name"].upper()]
                seq_n += 1
            for op in {i[4] & 0xFF for i in instrs}:
                files[op] = files.get(op, 0) + 1
            for i in instrs:
                uses[i[4] & 0xFF] = uses.get(i[4] & 0xFF, 0) + 1
        counted = {op: (uses[op], files[op]) for op in uses}
        doc_ok = None if skipped else counted == DOC_CD_USES
        walk = (f"walk of {len(seen)} names: {sum(uses.values())} commands, stops {stops}, "
                f"uses and files per command match docs/unknowns/06: {'skipped (not the CD layout)' if skipped else doc_ok}")
        if seq_n:
            walk += f"; floppy intro/outro counts match 06: {seq_ok} ({seq_n} files)"
        print(f"CHECK tim: {st['total_parsed']}/{st['total_tim_files']} files, FORM types {st['form_types']}, "
              f"chunks {st['chunk_type_counts']}, files + statistics match data/tim_analysis.json: {'skipped (not the CD layout)' if skipped else same}; {walk}")
        return 0 if same and stops == 0 and doc_ok is not False and seq_ok else 1
    if a.out:
        L.write_json(a.out, analysis)

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

    return 0


if __name__ == "__main__":
    sys.exit(main())
