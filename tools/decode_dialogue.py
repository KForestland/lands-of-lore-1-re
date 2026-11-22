#!/usr/bin/env python3
"""
Decode Westwood bigram-compressed text in LoL1 dialogue strings.

The compression scheme (from ScummVM's Util::decodeString1):
- Bytes < 0x80 are literal ASCII characters
- Bytes >= 0x80: clear high bit to get 7-bit value `v`
  - index1 = (v & 0x78) >> 3  -> lookup in decodeTable1 (first char)
  - index2 = v               -> lookup in decodeTable2 (second char)
  - Emit both characters

After decodeString1, decodeString2 handles escape sequences:
- 0x1B followed by a byte X -> emit (X + 0x7F)
  This is used for literal high bytes (accented chars etc.)

In our JSON files, bytes are stored as [XX] hex notation.
"""

from cli_errors import run_cli
import json
import os
import re
import sys

# From ScummVM engines/kyra/engine/util.cpp
decodeTable1 = bytes([
    0x20, 0x65, 0x74, 0x61, 0x69, 0x6E, 0x6F, 0x73,
    0x72, 0x6C, 0x68, 0x63, 0x64, 0x75, 0x70, 0x6D
])

decodeTable2 = bytes([
    0x74, 0x61, 0x73, 0x69, 0x6F, 0x20, 0x77, 0x62,
    0x20, 0x72, 0x6E, 0x73, 0x64, 0x61, 0x6C, 0x6D,
    0x68, 0x20, 0x69, 0x65, 0x6F, 0x72, 0x61, 0x73,
    0x6E, 0x72, 0x74, 0x6C, 0x63, 0x20, 0x73, 0x79,
    0x6E, 0x73, 0x74, 0x63, 0x6C, 0x6F, 0x65, 0x72,
    0x20, 0x64, 0x74, 0x67, 0x65, 0x73, 0x69, 0x6F,
    0x6E, 0x72, 0x20, 0x75, 0x66, 0x6D, 0x73, 0x77,
    0x20, 0x74, 0x65, 0x70, 0x2E, 0x69, 0x63, 0x61,
    0x65, 0x20, 0x6F, 0x69, 0x61, 0x64, 0x75, 0x72,
    0x20, 0x6C, 0x61, 0x65, 0x69, 0x79, 0x6F, 0x64,
    0x65, 0x69, 0x61, 0x20, 0x6F, 0x74, 0x72, 0x75,
    0x65, 0x74, 0x6F, 0x61, 0x6B, 0x68, 0x6C, 0x72,
    0x20, 0x65, 0x69, 0x75, 0x2C, 0x2E, 0x6F, 0x61,
    0x6E, 0x73, 0x72, 0x63, 0x74, 0x6C, 0x61, 0x69,
    0x6C, 0x65, 0x6F, 0x69, 0x72, 0x61, 0x74, 0x70,
    0x65, 0x61, 0x6F, 0x69, 0x70, 0x20, 0x62, 0x6D
])


def parse_encoded_string(s):
    """Convert JSON string with [XX] hex notation back to raw bytes."""
    result = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '[':
            # Look for closing bracket
            close = s.find(']', i + 1)
            if close != -1:
                tag = s[i+1:close]
                # Check for special tags like [CR]
                if tag == 'CR':
                    result.append(0x0D)  # carriage return
                    i = close + 1
                    continue
                # Try to parse as hex byte
                try:
                    byte_val = int(tag, 16)
                    if 0 <= byte_val <= 255 and len(tag) == 2:
                        result.append(byte_val)
                        i = close + 1
                        continue
                except ValueError:
                    pass
            # Not a valid hex tag, treat '[' as literal
            result.append(ord('['))
            i += 1
        else:
            result.append(ord(s[i]))
            i += 1
    return bytes(result)


def decode_string1(raw_bytes):
    """Apply Westwood bigram decompression (ScummVM's decodeString1)."""
    result = bytearray()
    for b in raw_bytes:
        if b & 0x80:
            v = b & 0x7F
            index1 = (v & 0x78) >> 3
            result.append(decodeTable1[index1])
            if v < len(decodeTable2):
                result.append(decodeTable2[v])
            else:
                result.append(ord('?'))
        else:
            result.append(b)
    return bytes(result)


def decode_string2(raw_bytes):
    """Handle escape sequences (ScummVM's decodeString2).
    0x1B + X -> (X + 0x7F)
    """
    result = bytearray()
    i = 0
    while i < len(raw_bytes):
        if raw_bytes[i] == 0x1B and i + 1 < len(raw_bytes):
            result.append((raw_bytes[i + 1] + 0x7F) & 0xFF)
            i += 2
        else:
            result.append(raw_bytes[i])
            i += 1
    return bytes(result)


# Every pair the bigram bytes stand for; no pair has two codes.
BIGRAMS = {(decodeTable1[v >> 3], decodeTable2[v]): 0x80 | v for v in range(len(decodeTable2))}


def encode_string(text):
    """Inverse of decode_string2(decode_string1(...)): escape bytes from 0x80 as
    0x1B + (byte - 0x7F), then join pairs into bigram bytes from the left. This
    re-creates every string of the CD and floppy editions byte for byte."""
    escaped = bytearray()
    for b in text:
        escaped.extend((0x1B, b - 0x7F) if b >= 0x80 else (b,))
    result = bytearray()
    i = 0
    while i < len(escaped):
        code = BIGRAMS.get(tuple(escaped[i:i + 2]))
        result.append(code or escaped[i])
        i += 2 if code else 1
    result = bytes(result)
    if decode_string2(decode_string1(result)) != text:
        raise ValueError("text cannot be stored (a 0x1B or 0xFF byte)")
    return result


def format_control_codes(decoded_bytes):
    """Convert decoded bytes to readable string, marking control codes."""
    result = []
    for b in decoded_bytes:
        if b == 0x0D:
            result.append('\n')
        elif 0x20 <= b < 0x7F:
            result.append(chr(b))
        elif b >= 0x80:
            # After decoding, remaining high bytes are likely
            # extended chars (CP437) or control codes
            try:
                result.append(bytes([b]).decode('cp437'))
            except:
                result.append(f'[0x{b:02X}]')
        elif b == 0x00:
            pass  # null terminator
        elif b < 0x20:
            # Control codes: some have special meaning in LoL
            # Common ones: 0x05 = paragraph break, etc.
            ctrl_names = {
                0x01: '[CTRL:01]',
                0x02: '[CTRL:02]',
                0x03: '[CTRL:03]',
                0x04: '[CTRL:04]',
                0x05: '[PARA]',
                0x06: '[CTRL:06]',
                0x07: '[CTRL:07]',
                0x08: '[CTRL:08]',
                0x09: '\t',
                0x0A: '\n',
                0x0B: '[CTRL:0B]',
                0x0C: '[CTRL:0C]',
            }
            result.append(ctrl_names.get(b, f'[CTRL:{b:02X}]'))
        else:
            result.append(chr(b))
    return ''.join(result)


def decode_lol_string(encoded_str):
    """Full decode pipeline for a LoL1 dialogue string."""
    raw = parse_encoded_string(encoded_str)
    decoded1 = decode_string1(raw)
    decoded2 = decode_string2(decoded1)
    return format_control_codes(decoded2)


def decode_raw(raw):
    """ScummVM getLangString path: decodeString1 then decodeString2 (util.cpp:29-87)."""
    return format_control_codes(decode_string2(decode_string1(raw)))


def file_strings(data):
    import struct
    n = struct.unpack_from("<H", data, 0)[0] // 2
    offs = struct.unpack_from(f"<{n}H", data, 0)
    return [data[o:data.index(b"\0", o)] for o in offs]


USAGE = """
  decode_dialogue.py LEVEL01.ENG [--index 5]   # decode straight from the game data
  decode_dialogue.py --in-dir raw/ --out decoded/   # decode extract_dialogue.py output
  decode_dialogue.py --check     # decode all strings; every bigram byte maps inside the tables
"""


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import lol1lib as L
    ap = L.tool_args("Read original game text from LoL1 language tables.\n" + USAGE, out_help="write decoded JSON files to this directory", out_aliases=("--out-dir",))
    ap.add_argument("name", nargs="?")
    ap.add_argument("--index", type=int)
    ap.add_argument("--in-dir")
    a = ap.parse_args()
    if a.check:
        n = files = bad = accented = 0
        for pak, name, data in L.find_all("", a.data):
            if not name.endswith((".ENG", ".FRE", ".GER")):
                continue
            files += 1
            for raw in file_strings(data):
                n += 1
                if any(b & 0x80 and (b & 0x7F) >= len(decodeTable2) for b in raw):
                    bad += 1
                t = decode_raw(raw)
                accented += any(ord(c) > 127 for c in t)
        print(f"CHECK decode_dialogue: {files} files, {n} strings decoded, bigram index out of table: {bad}, "
              f"strings with accented characters: {accented}")
        return 0 if bad == 0 and n else 1
    if a.name:
        _, data = L.find_member(a.name, a.data, a.pak)
        strings = file_strings(data)
        if a.index is not None and not 0 <= a.index < len(strings):
            ap.error(f"String {a.index} is outside {a.name}, which contains {len(strings)} strings.")
        for i, raw in enumerate(strings):
            if a.index is None or a.index == i:
                print(f"[{i}] {decode_raw(raw)}")
        return 0
    if a.in_dir and a.out:
        os.makedirs(a.out, exist_ok=True)
        for fn in sorted(f for f in os.listdir(a.in_dir) if f.endswith(".json") and f != "summary.json"):
            with open(os.path.join(a.in_dir, fn)) as f:
                d = json.load(f)
            d["strings"] = [decode_lol_string(x) for x in d["strings"]]
            with open(os.path.join(a.out, fn), "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
        print("wrote", a.out)
        return 0
    ap.print_help()
    return 2


if __name__ == '__main__':
    raise SystemExit(run_cli(main))
