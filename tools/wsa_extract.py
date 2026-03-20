#!/usr/bin/env python3
"""
Extract WSA (Westwood Screen Animation) files from LoL1 PAK corpus.
Decodes frame 0 of each WSA to PNG, produces inventory JSON.

WSA v2 header (14 bytes):
  uint16 numFrames
  int16  xAdd
  int16  yAdd
  uint16 width
  uint16 height
  uint16 deltaBufferSize
  uint16 flags  (bit 0 = WF_HAS_PALETTE)

Then: uint32[numFrames+1] frame offsets
Then: 4-byte gap (typically: uint32 fileSize or fileSize-768)

No palette (flags=0):
  - Offsets are absolute file positions
  - Frame i: offsets[i] .. offsets[i+1]
  - Gap value = fileSize

Has palette (flags & 1):
  - offsets[0] = palette position (right after gap)
  - 768-byte VGA 6-bit palette at offsets[0]
  - If offsets[1] > offsets[0]+768: offsets are absolute
    Frame 0: offsets[0]+768 .. offsets[1]
    Frame i: offsets[i] .. offsets[i+1]
  - If offsets[1] <= offsets[0]+768: offsets are relative to frameDataBase
    frameDataBase = offsets[0] + 768
    Frame i: frameDataBase+offsets[i] .. frameDataBase+offsets[i+1]

Frame decode pipeline:
  1. decodeFrame4 (LCW) compressed -> deltaBuffer
  2. decodeFrameDelta (skip/copy/RLE with XOR) -> currentFrame
"""

import struct
import os
import sys
import json
from PIL import Image

sys.path.insert(0, '/home/bob')
from lol1_decode_frame4 import decode_frame4

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_DIR = "/home/bob/lol1_wsa_frames"
INVENTORY_FILE = "/home/bob/lol1_wsa_inventory.json"


def decode_frame_delta(dst, src, no_xor=False):
    """ScummVM Screen::wrapped_decodeFrameDelta."""
    sp = 0
    dp = 0
    dst_len = len(dst)

    while sp < len(src):
        code = src[sp]; sp += 1

        if code == 0:
            if sp + 1 >= len(src):
                break
            length = src[sp]; sp += 1
            fill = src[sp]; sp += 1
            for _ in range(length):
                if dp < dst_len:
                    if no_xor:
                        dst[dp] = fill
                    else:
                        dst[dp] ^= fill
                    dp += 1

        elif code & 0x80:
            code -= 0x80
            if code != 0:
                dp += code
            else:
                if sp + 1 >= len(src):
                    break
                subcode = src[sp] | (src[sp + 1] << 8); sp += 2
                if subcode == 0:
                    break
                elif subcode & 0x8000:
                    subcode -= 0x8000
                    if subcode & 0x4000:
                        length = subcode - 0x4000
                        if sp >= len(src):
                            break
                        fill = src[sp]; sp += 1
                        for _ in range(length):
                            if dp < dst_len:
                                if no_xor:
                                    dst[dp] = fill
                                else:
                                    dst[dp] ^= fill
                                dp += 1
                    else:
                        for _ in range(subcode):
                            if sp >= len(src) or dp >= dst_len:
                                break
                            if no_xor:
                                dst[dp] = src[sp]
                            else:
                                dst[dp] ^= src[sp]
                            sp += 1; dp += 1
                else:
                    dp += subcode
        else:
            for _ in range(code):
                if sp >= len(src) or dp >= dst_len:
                    break
                if no_xor:
                    dst[dp] = src[sp]
                else:
                    dst[dp] ^= src[sp]
                sp += 1; dp += 1


def load_default_palette():
    """Load palette from first CPS file that has one."""
    with open(INDEX_FILE) as f:
        idx = json.load(f)

    for pak_name, pak_info in sorted(idx['pak_files'].items()):
        for entry in pak_info['entries']:
            if not entry['name'].upper().endswith('.CPS'):
                continue
            pak_path = os.path.join(PAK_DIR, pak_name)
            if not os.path.exists(pak_path):
                continue
            with open(pak_path, 'rb') as f:
                f.seek(entry['offset'])
                data = f.read(entry['size'])
            if len(data) < 10:
                continue
            pal_size = struct.unpack_from('<H', data, 8)[0]
            if pal_size >= 768:
                pal_raw = data[10:10 + 768]
                palette = []
                for i in range(256):
                    r = (pal_raw[i * 3] & 0x3F) * 4
                    g = (pal_raw[i * 3 + 1] & 0x3F) * 4
                    b = (pal_raw[i * 3 + 2] & 0x3F) * 4
                    palette.append((r, g, b))
                return palette

    return [(i, i, i) for i in range(256)]


def read_palette_vga(data, offset):
    """Read a 768-byte VGA 6-bit palette."""
    pal_raw = data[offset:offset + 768]
    palette = []
    for i in range(256):
        r = (pal_raw[i * 3] & 0x3F) * 4
        g = (pal_raw[i * 3 + 1] & 0x3F) * 4
        b = (pal_raw[i * 3 + 2] & 0x3F) * 4
        palette.append((r, g, b))
    return palette


def parse_and_render_wsa(data, file_size, default_palette):
    """Parse WSA file and render frame 0."""
    if len(data) < 14:
        return None

    numFrames = struct.unpack_from('<H', data, 0)[0]
    xAdd = struct.unpack_from('<h', data, 2)[0]
    yAdd = struct.unpack_from('<h', data, 4)[0]
    width = struct.unpack_from('<H', data, 6)[0]
    height = struct.unpack_from('<H', data, 8)[0]
    delta_buf_size = struct.unpack_from('<H', data, 10)[0]
    flags = struct.unpack_from('<H', data, 12)[0]

    if numFrames == 0 or numFrames > 10000:
        return None
    if width == 0 or height == 0 or width > 1024 or height > 1024:
        return None

    pixel_count = width * height

    # Read frame offsets (numFrames + 1 entries)
    offsets_needed = numFrames + 1
    offsets_end = 14 + offsets_needed * 4
    if offsets_end + 4 > len(data):
        return None

    offsets = []
    for i in range(offsets_needed):
        offsets.append(struct.unpack_from('<I', data, 14 + i * 4)[0])

    has_palette = bool(flags & 1)

    if has_palette:
        # Palette at offsets[0] (right after offset table + 4-byte gap)
        pal_pos = offsets[0]
        if pal_pos + 768 > len(data):
            return None

        # Verify it's valid VGA palette data
        pal_check = data[pal_pos:pal_pos + 768]
        if max(pal_check) <= 63:
            palette = read_palette_vga(data, pal_pos)
        else:
            palette = default_palette

        frame_data_base = pal_pos + 768

        # Determine if offsets are absolute or relative
        if offsets[1] >= frame_data_base:
            # Absolute: frame 0 from frame_data_base to offsets[1]
            frame0_start = frame_data_base
            frame0_end = offsets[1]
        else:
            # Relative: add frame_data_base to each offset
            frame0_start = frame_data_base + offsets[0]
            frame0_end = frame_data_base + offsets[1]
    else:
        palette = default_palette
        frame0_start = offsets[0]
        frame0_end = offsets[1] if numFrames > 1 else file_size

    if frame0_start >= len(data) or frame0_end > len(data) or frame0_start >= frame0_end:
        return None

    compressed = data[frame0_start:frame0_end]

    # Step 1: LCW decompress
    try:
        delta_buffer = decode_frame4(compressed, delta_buf_size)
    except Exception:
        return None

    if len(delta_buffer) == 0:
        return None

    # Step 2: Apply frame delta
    frame_buffer = bytearray(pixel_count)
    decode_frame_delta(frame_buffer, delta_buffer)

    # Create image
    img = Image.new('RGB', (width, height))
    pix = img.load()
    for y in range(height):
        for x in range(width):
            ci = frame_buffer[y * width + x]
            pix[x, y] = palette[ci] if ci < len(palette) else (0, 0, 0)

    return (numFrames, width, height, xAdd, yAdd, flags, delta_buf_size,
            has_palette, img)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INDEX_FILE) as f:
        index = json.load(f)

    default_palette = load_default_palette()
    print("Default palette loaded")

    wsa_files = []
    for pak_name, pak_info in sorted(index['pak_files'].items()):
        for entry in pak_info['entries']:
            if entry['name'].upper().endswith('.WSA'):
                wsa_files.append({
                    'name': entry['name'],
                    'pak': pak_name,
                    'offset': entry['offset'],
                    'size': entry['size']
                })

    print("Found %d WSA files" % len(wsa_files))

    inventory = []
    success = 0
    fail = 0
    fail_list = []

    for idx, w in enumerate(wsa_files):
        pak_path = os.path.join(PAK_DIR, w['pak'])
        if not os.path.exists(pak_path):
            fail += 1
            fail_list.append((w['name'], w['pak'], 'PAK not found'))
            continue

        with open(pak_path, 'rb') as f:
            f.seek(w['offset'])
            data = f.read(w['size'])

        result = parse_and_render_wsa(data, w['size'], default_palette)

        if result is None:
            fail += 1
            fail_list.append((w['name'], w['pak'], 'parse/decode failed'))
            continue

        numFrames, width, height, xAdd, yAdd, flags, deltaBufSize, hasPalette, img = result

        out_name = w['name'].replace('.WSA', '.png').replace('.wsa', '.png').lower()
        img.save(os.path.join(OUTPUT_DIR, out_name))

        inv_entry = {
            'filename': w['name'],
            'pak': w['pak'],
            'numFrames': numFrames,
            'width': width,
            'height': height,
            'xAdd': xAdd,
            'yAdd': yAdd,
            'fileSize': w['size'],
            'hasPalette': hasPalette,
            'deltaBufSize': deltaBufSize,
            'flags': flags
        }
        inventory.append(inv_entry)
        success += 1

        if (idx + 1) % 50 == 0:
            print("  Progress: %d/%d (success=%d, fail=%d)" %
                  (idx + 1, len(wsa_files), success, fail))

    with open(INVENTORY_FILE, 'w') as f:
        json.dump({
            'description': 'WSA file inventory from LoL1 PAK corpus',
            'total': len(wsa_files),
            'decoded': success,
            'failed': fail,
            'files': inventory
        }, f, indent=2)

    print("\nResults: %d/%d decoded, %d failed" % (success, len(wsa_files), fail))
    print("Output: %s" % OUTPUT_DIR)
    print("Inventory: %s" % INVENTORY_FILE)

    if fail_list:
        print("\nFailures (%d):" % len(fail_list))
        for name, pak, reason in fail_list:
            print("  %s in %s: %s" % (name, pak, reason))


if __name__ == "__main__":
    main()
