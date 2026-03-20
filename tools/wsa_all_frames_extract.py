#!/usr/bin/env python3
"""
Extract ALL frames from top-20 WSA files (by frame count) in the LoL1 PAK corpus.

WSA frame decoding is sequential:
  Frame 0: LCW decompress -> delta decode (no_xor for first frame? Actually XOR with zeroed buffer = copy)
  Frame N>0: LCW decompress -> delta decode with XOR against previous frame buffer
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
INVENTORY_FILE = "/home/bob/lol1_wsa_inventory.json"
OUTPUT_BASE = "/home/bob/lol1_wsa_all_frames"
TOP_N = 999  # Process all WSA files


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
    """Load palette from first CPS file in STARTUP.PAK that has one."""
    with open(INDEX_FILE) as f:
        idx = json.load(f)

    # Try STARTUP.PAK first
    for pak_name in ['STARTUP.PAK'] + sorted(idx['pak_files'].keys()):
        if pak_name not in idx['pak_files']:
            continue
        for entry in idx['pak_files'][pak_name]['entries']:
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
                print(f"  Loaded default palette from {entry['name']} in {pak_name}")
                return palette

    return [(i, i, i) for i in range(256)]


def frame_to_image(frame_buffer, width, height, palette):
    """Convert indexed pixel buffer to PIL Image."""
    img = Image.new('RGB', (width, height))
    pix = img.load()
    for y in range(height):
        for x in range(width):
            ci = frame_buffer[y * width + x]
            pix[x, y] = palette[ci] if ci < len(palette) else (0, 0, 0)
    return img


def extract_all_frames(data, file_size, default_palette):
    """Parse WSA and extract ALL frames sequentially.

    Returns: (numFrames, width, height, palette, list_of_PIL_images) or None on failure.
    """
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

    # Read frame offsets: numFrames + 1 entries
    offsets_needed = numFrames + 1
    offsets_end = 14 + offsets_needed * 4
    if offsets_end > len(data):
        return None

    offsets = []
    for i in range(offsets_needed):
        offsets.append(struct.unpack_from('<I', data, 14 + i * 4)[0])

    # Handle palette
    has_palette = bool(flags & 1)
    palette_size_in_file = 0
    if has_palette:
        pal_pos = offsets[0]
        if pal_pos + 768 > len(data):
            return None
        pal_raw = data[pal_pos:pal_pos + 768]
        palette = []
        for i in range(256):
            r = (pal_raw[i * 3] & 0x3F) * 4
            g = (pal_raw[i * 3 + 1] & 0x3F) * 4
            b = (pal_raw[i * 3 + 2] & 0x3F) * 4
            palette.append((r, g, b))
        palette_size_in_file = 768
    else:
        palette = default_palette

    # Decode all frames sequentially
    frame_buffer = bytearray(pixel_count)
    images = []

    for frame_idx in range(numFrames):
        # Determine frame data range
        frame_start = offsets[frame_idx]
        if frame_idx == 0 and has_palette:
            frame_start += palette_size_in_file

        # Frame end
        if frame_idx + 1 < len(offsets):
            frame_end = offsets[frame_idx + 1]
        else:
            frame_end = file_size

        # Last offset can be 0 (loop frame) - skip it
        if frame_end == 0:
            frame_end = file_size

        if frame_start >= len(data) or frame_end > len(data) or frame_start >= frame_end:
            # Try to continue with what we have
            break

        compressed = data[frame_start:frame_end]

        # Step 1: LCW decompress
        try:
            delta_buffer = decode_frame4(compressed, max(delta_buf_size, pixel_count * 2))
        except Exception as e:
            print(f"    Frame {frame_idx}: LCW decode error: {e}")
            break

        if len(delta_buffer) == 0:
            # LCW returned nothing (first byte was 0x80 end marker).
            # The data may already be in frame-delta format directly (no LCW layer).
            delta_buffer = compressed

        # Step 2: Apply delta (XOR with previous frame buffer)
        # Frame 0 starts with zeroed buffer, XOR with zero = copy, so no special case needed
        decode_frame_delta(frame_buffer, delta_buffer, no_xor=False)

        # Save this frame
        img = frame_to_image(frame_buffer, width, height, palette)
        images.append(img)

    return (numFrames, width, height, palette, images)


def main():
    os.makedirs(OUTPUT_BASE, exist_ok=True)

    # Load inventory to find top N by frame count
    with open(INVENTORY_FILE) as f:
        inventory = json.load(f)

    # Load PAK index
    with open(INDEX_FILE) as f:
        pak_index = json.load(f)

    # Sort by frame count, take top N
    wsa_list = sorted(inventory['files'], key=lambda x: x.get('numFrames', 0), reverse=True)
    top_wsa = wsa_list[:TOP_N]

    print(f"Top {TOP_N} WSA files by frame count:")
    for w in top_wsa:
        print(f"  {w['filename']:25s}  {w['numFrames']:4d} frames  {w['width']}x{w['height']}  pak={w['pak']}")

    # Load default palette
    default_palette = load_default_palette()

    # Build lookup: filename -> PAK entry info
    pak_lookup = {}
    for pak_name, pak_info in pak_index['pak_files'].items():
        for entry in pak_info['entries']:
            if entry['name'].upper().endswith('.WSA'):
                key = (entry['name'].upper(), pak_name.upper())
                pak_lookup[key] = {
                    'pak': pak_name,
                    'offset': entry['offset'],
                    'size': entry['size']
                }

    total_frames_extracted = 0
    results = []

    for w in top_wsa:
        fname = w['filename']
        pak_name = w['pak']
        key = (fname.upper(), pak_name.upper())

        if key not in pak_lookup:
            print(f"\n  SKIP {fname}: not found in PAK index")
            continue

        info = pak_lookup[key]
        pak_path = os.path.join(PAK_DIR, info['pak'])
        if not os.path.exists(pak_path):
            print(f"\n  SKIP {fname}: PAK file not found: {pak_path}")
            continue

        print(f"\n  Processing {fname} ({w['numFrames']} frames, {w['width']}x{w['height']})...")

        with open(pak_path, 'rb') as f:
            f.seek(info['offset'])
            data = f.read(info['size'])

        result = extract_all_frames(data, info['size'], default_palette)

        if result is None:
            print(f"    FAILED: could not parse WSA header")
            results.append({'file': fname, 'expected': w['numFrames'], 'extracted': 0, 'status': 'FAIL'})
            continue

        numFrames, width, height, palette, images = result

        # Save frames
        base_name = fname.replace('.WSA', '').replace('.wsa', '').lower()
        out_dir = os.path.join(OUTPUT_BASE, base_name)
        os.makedirs(out_dir, exist_ok=True)

        for i, img in enumerate(images):
            out_path = os.path.join(out_dir, f"frame_{i:03d}.png")
            img.save(out_path)

        total_frames_extracted += len(images)
        print(f"    Extracted {len(images)}/{numFrames} frames to {out_dir}/")
        results.append({
            'file': fname,
            'expected': numFrames,
            'extracted': len(images),
            'width': width,
            'height': height,
            'status': 'OK' if len(images) == numFrames else 'PARTIAL'
        })

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_frames_extracted} total frames extracted from {len(top_wsa)} WSA files")
    print(f"{'='*60}")
    for r in results:
        status = r['status']
        print(f"  {r['file']:25s}  {r['extracted']:4d}/{r['expected']:4d}  [{status}]")

    # Save summary
    summary_path = os.path.join(OUTPUT_BASE, "extraction_summary.json")
    with open(summary_path, 'w') as f:
        json.dump({
            'total_frames_extracted': total_frames_extracted,
            'files_processed': len(results),
            'results': results
        }, f, indent=2)
    print(f"\nSummary saved to {summary_path}")


if __name__ == "__main__":
    main()
