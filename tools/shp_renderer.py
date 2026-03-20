#!/usr/bin/env python3
"""
LoL1 SHP Sprite Frame Renderer

SHP file structure:
  uint16 frame_count
  uint32[frame_count + 1] frame_offsets (last = end marker or file size)

SHP frame header (ScummVM Screen::drawShape, _useAltShapeHeader for LoL):
  Offset 0:  uint16 alt_prefix (skip value)
  Offset 2:  uint16 flags
  Offset 4:  uint8  height
  Offset 5:  uint16 width
  Offset 7:  uint8  height_dup (same as height)
  Offset 8:  uint16 shapeSize (compressed data size incl header fields)
  Offset 10: uint16 uncompSize (size of line-encoded data after LCW decompress)

Frame flags:
  bit 0 (0x01): has outline/color table (16 bytes after 12-byte header)
  bit 2 (0x04): pixel data is LCW compressed (decompress to uncompSize)
  bit 1 (0x02): 16-color mode (4bpp)

After 12-byte header:
  If flags & 0x01 && flags & 0x04: outline table = 1 byte count + count bytes
  If flags & 0x01 && !(flags & 0x04): color table = 16 bytes
  If !(flags & 0x01): no extra table

Pixel data is line-encoded (not flat):
  Each line: alternating transparency-skip and literal-pixel runs
  byte & 0x80: skip (byte & 0x7F) transparent pixels
  byte without 0x80: copy 'byte' literal pixels from stream
  0x80 alone can act as end-of-line or end-of-shape marker

The line decoder fills a width*height buffer with palette indices (0=transparent).
"""

import json
import struct
import os
import sys
from PIL import Image

sys.path.insert(0, '/home/bob')
from lol1_decode_frame4 import decode_frame4

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"
OUTPUT_DIR = "/home/bob/lol1_shp_rendered"

# Default VGA palette (grayscale fallback)
DEFAULT_PALETTE = [(i, i, i) for i in range(256)]


def read_pak_entry(pak_path, offset, size):
    with open(pak_path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def try_decompress(data):
    """Try LCW decompression with 10-byte header, fall back to raw."""
    if len(data) < 12:
        return data
    # Check if it looks like a 10-byte header (compressed size roughly matches)
    expected = struct.unpack_from('<H', data, 4)[0]
    if expected > 0 and expected < len(data) * 10:
        payload = data[10:]
        result = decode_frame4(payload, expected)
        if result and len(result) == expected:
            return result
    return data


def decode_frame3(src, dst_size):
    """Westwood RLE (Frame3) decoder."""
    dst = bytearray()
    sp = 0
    while len(dst) < dst_size and sp < len(src):
        code = src[sp]; sp += 1
        if code == 0:
            if sp + 2 >= len(src): break
            sz = src[sp] | (src[sp+1] << 8); sp += 2
            fill = src[sp]; sp += 1
            dst.extend([fill] * min(sz, dst_size - len(dst)))
        elif code & 0x80:
            count = 256 - code  # negative int8
            if sp >= len(src): break
            fill = src[sp]; sp += 1
            dst.extend([fill] * min(count, dst_size - len(dst)))
        else:
            count = min(code, dst_size - len(dst))
            dst.extend(src[sp:sp+count])
            sp += count
    return bytes(dst)


def decode_shape_lines(data, width, height):
    """Decode ScummVM LoL shape line-encoded format to flat pixels.

    Each line uses alternating skip/copy runs:
      byte & 0x80 set: skip (byte & 0x7F) pixels (transparent)
      byte & 0x80 clear, byte > 0: copy 'byte' literal pixel bytes
      0x80 alone: end marker (fill rest of line with transparent)
    """
    pixels = bytearray(width * height)
    sp = 0

    for y in range(height):
        x = 0
        while x < width and sp < len(data):
            code = data[sp]; sp += 1
            if code == 0x80:
                # End of line / end of shape
                break
            if code & 0x80:
                # Skip transparent pixels
                count = code & 0x7F
                x += count
            else:
                # Copy literal pixels
                count = code
                end = min(count, width - x)
                for i in range(end):
                    if sp < len(data):
                        pixels[y * width + x] = data[sp]
                        sp += 1
                        x += 1
                # Skip any extra source bytes if count > available width
                if count > end:
                    sp += (count - end)

    return bytes(pixels)


def parse_shp(data):
    """Parse SHP file into frame list."""
    if len(data) < 6:
        return None

    frame_count = struct.unpack_from('<H', data, 0)[0]
    if frame_count == 0 or frame_count > 500:
        return None

    # Read offset table
    offsets = []
    for i in range(frame_count + 1):
        off = 2 + i * 4
        if off + 4 > len(data):
            break
        offsets.append(struct.unpack_from('<I', data, off)[0])

    if len(offsets) < 2:
        return None

    frames = []
    for i in range(min(frame_count, len(offsets) - 1)):
        start = offsets[i]
        end = offsets[i + 1] if offsets[i + 1] > start else len(data)

        if start >= len(data) or start < 0:
            frames.append(None)
            continue

        frame_data = data[start:min(end, len(data))]
        if len(frame_data) < 7:
            frames.append(None)
            continue

        # Parse 12-byte alt shape header
        # alt_prefix = struct.unpack_from('<H', frame_data, 0)[0]
        flags = struct.unpack_from('<H', frame_data, 2)[0]
        height = frame_data[4]
        width = struct.unpack_from('<H', frame_data, 5)[0]

        if width == 0 or height == 0 or width > 320 or height > 200:
            frames.append(None)
            continue

        pixel_size = width * height
        pixels = None

        # Extended header fields (bytes 7-11)
        if len(frame_data) >= 12:
            # h_dup = frame_data[7]
            # shape_size = struct.unpack_from('<H', frame_data, 8)[0]
            uncomp_size = struct.unpack_from('<H', frame_data, 10)[0]

            # Determine data offset after header + optional tables
            data_offset = 12

            if flags & 0x01:
                if flags & 0x04:
                    # Outline table: 1 byte count + count palette entries
                    if data_offset < len(frame_data):
                        table_count = frame_data[data_offset]
                        data_offset += 1 + table_count
                else:
                    # Color replacement table: 16 bytes
                    data_offset += 16

            payload = frame_data[data_offset:]

            if flags & 0x04:
                # LCW compressed: decompress to uncompSize, then line-decode
                line_data = decode_frame4(payload, uncomp_size)
            else:
                # Raw line-encoded data
                line_data = payload[:uncomp_size] if len(payload) >= uncomp_size else payload

            if line_data and len(line_data) > 0:
                pixels = decode_shape_lines(line_data, width, height)
                if pixels and sum(1 for b in pixels if b != 0) == 0 and len(line_data) > 4:
                    # All zeros but had data -- might be valid (fully transparent frame)
                    pass  # keep it

        # Fallback: try the old approach if the new one failed
        if pixels is None or len(pixels) < pixel_size:
            for hdr_size in [7, 12]:
                if hdr_size >= len(frame_data):
                    continue
                pdata = frame_data[hdr_size:]
                # Try Frame4/LCW
                result = decode_frame4(pdata, pixel_size)
                if result and len(result) >= pixel_size:
                    pixels = result
                    break
                # Try RLE (Frame3)
                result = decode_frame3(pdata, pixel_size)
                if result and len(result) >= pixel_size:
                    pixels = result
                    break
                # Try raw
                if len(pdata) >= pixel_size:
                    pixels = pdata[:pixel_size]
                    break

        frames.append({
            'width': width,
            'height': height,
            'flags': flags,
            'pixels': pixels,
            'data_size': len(frame_data),
        })

    return frames


def load_palette_from_general():
    """Try to load a default palette from GENERAL.PAK CPS files."""
    with open(INDEX_FILE) as f:
        index = json.load(f)

    # Try to get palette from a known CPS file
    for pak_name in ['STARTUP.PAK', 'GENERAL.PAK']:
        if pak_name not in index['pak_files']:
            continue
        pak_path = os.path.join(PAK_DIR, pak_name)
        for entry in index['pak_files'][pak_name]['entries']:
            if entry['name'].endswith('.CPS'):
                data = read_pak_entry(pak_path, entry['offset'], entry['size'])
                pal_size = struct.unpack_from('<H', data, 8)[0]
                if pal_size >= 768:
                    pal_raw = data[10:10+768]
                    palette = []
                    for i in range(256):
                        r = (pal_raw[i*3] & 0x3F) * 4
                        g = (pal_raw[i*3+1] & 0x3F) * 4
                        b = (pal_raw[i*3+2] & 0x3F) * 4
                        palette.append((r, g, b))
                    return palette
    return DEFAULT_PALETTE


def render_frame(frame, palette, transparent_idx=0):
    """Render a single frame to PIL Image."""
    if frame is None or frame['pixels'] is None:
        return None

    w, h = frame['width'], frame['height']
    pixels = frame['pixels']

    if len(pixels) < w * h:
        return None

    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            idx = pixels[y * w + x]
            if idx == transparent_idx:
                continue  # transparent
            if idx < len(palette):
                r, g, b = palette[idx]
                img.putpixel((x, y), (r, g, b, 255))
            else:
                img.putpixel((x, y), (128, 0, 128, 255))

    return img


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INDEX_FILE) as f:
        index = json.load(f)

    palette = load_palette_from_general()
    print(f"Loaded palette ({len(palette)} colors)")

    total_files = 0
    total_frames_rendered = 0
    total_frames_failed = 0
    results = []

    for pak_name in sorted(index['pak_files'].keys()):
        pak_path = os.path.join(PAK_DIR, pak_name)
        if not os.path.exists(pak_path):
            continue

        for entry in index['pak_files'][pak_name]['entries']:
            if not entry['name'].endswith('.SHP'):
                continue

            total_files += 1
            raw = read_pak_entry(pak_path, entry['offset'], entry['size'])
            data = try_decompress(raw)
            frames = parse_shp(data)

            if frames is None:
                print(f"  SKIP: {entry['name']} in {pak_name} — parse failed")
                results.append({
                    'pak': pak_name, 'name': entry['name'],
                    'status': 'parse_failed', 'frames_rendered': 0
                })
                continue

            shp_name = entry['name'].replace('.SHP', '').lower()
            shp_dir = os.path.join(OUTPUT_DIR, shp_name)
            os.makedirs(shp_dir, exist_ok=True)

            rendered = 0
            failed = 0
            for fi, frame in enumerate(frames):
                img = render_frame(frame, palette)
                if img:
                    img.save(os.path.join(shp_dir, f"frame_{fi:03d}.png"))
                    rendered += 1
                else:
                    failed += 1
                    total_frames_failed += 1

            total_frames_rendered += rendered
            results.append({
                'pak': pak_name, 'name': entry['name'],
                'status': 'ok', 'total_frames': len(frames),
                'frames_rendered': rendered,
                'failures': failed
            })

            if rendered > 0:
                if failed > 0:
                    print(f"  {entry['name']:20s} ({pak_name:15s}): {rendered}/{len(frames)} frames ({failed} failed)")
                else:
                    print(f"  {entry['name']:20s} ({pak_name:15s}): {rendered}/{len(frames)} frames")
            else:
                print(f"  {entry['name']:20s} ({pak_name:15s}): 0/{len(frames)} frames (all failed)")

    print(f"\n=== SUMMARY ===")
    print(f"SHP files processed: {total_files}")
    print(f"Frames rendered: {total_frames_rendered}")
    print(f"Frames failed: {total_frames_failed}")
    print(f"Output: {OUTPUT_DIR}")

    with open('/home/bob/lol1_shp_render_results.json', 'w') as f:
        json.dump({
            'total_files': total_files,
            'total_frames_rendered': total_frames_rendered,
            'total_frames_failed': total_frames_failed,
            'files': results
        }, f, indent=2)


if __name__ == "__main__":
    main()
