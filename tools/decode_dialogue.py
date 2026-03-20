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


def main():
    input_dir = '/home/bob/lol1_dialogue/'
    output_dir = '/home/bob/lol1_dialogue_decoded/'
    os.makedirs(output_dir, exist_ok=True)

    all_files = sorted(os.listdir(input_dir))
    json_files = [f for f in all_files if f.endswith('.json')]

    print(f"Found {len(json_files)} JSON files to decode.\n")

    # Process all files
    for fn in json_files:
        with open(os.path.join(input_dir, fn)) as f:
            data = json.load(f)

        decoded_strings = []
        for s in data['strings']:
            decoded_strings.append(decode_lol_string(s))

        out_data = {
            'file': data['file'],
            'string_count': data['string_count'],
            'strings': decoded_strings
        }
        if 'pak' in data:
            out_data['pak'] = data['pak']

        with open(os.path.join(output_dir, fn), 'w', encoding='utf-8') as f:
            json.dump(out_data, f, indent=2, ensure_ascii=False)

    # Show samples
    print("=" * 70)
    print("SAMPLE: First 10 strings from LANDS.ENG")
    print("=" * 70)
    with open(os.path.join(input_dir, 'lands_eng.json')) as f:
        data = json.load(f)
    for i, s in enumerate(data['strings'][:10]):
        decoded = decode_lol_string(s)
        print(f"\n[{i}] ENCODED: {s}")
        print(f"    DECODED: {decoded}")

    print("\n" + "=" * 70)
    print("SAMPLE: First 10 strings from LEVEL01.ENG")
    print("=" * 70)
    with open(os.path.join(input_dir, 'level01_eng.json')) as f:
        data = json.load(f)
    for i, s in enumerate(data['strings'][:10]):
        decoded = decode_lol_string(s)
        print(f"\n[{i}] ENCODED: {s}")
        print(f"    DECODED: {decoded}")

    # Stats
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    total_encoded = 0
    total_decoded = 0
    for fn in json_files:
        with open(os.path.join(input_dir, fn)) as f:
            data = json.load(f)
        total_encoded += len(data['strings'])
        for s in data['strings']:
            raw = parse_encoded_string(s)
            high_count = sum(1 for b in raw if b >= 0x80)
            total_decoded += high_count

    print(f"Total strings across {len(json_files)} files: {total_encoded}")
    print(f"Total high bytes decoded: {total_decoded}")
    print(f"Output written to: {output_dir}")


if __name__ == '__main__':
    main()
