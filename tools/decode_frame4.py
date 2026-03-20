#!/usr/bin/env python3
"""
LoL1 CPS Decoder — ScummVM-exact Frame4 (LCW) implementation

The key insight: Frame4/LCW has MIXED referencing:
  - Short back-ref (bit7=0): RELATIVE to current output position (dst - offs)
  - Medium copy (0xC0-0xFD): ABSOLUTE offset from output start (dstOrig + offs)
  - Large copy (0xFF): ABSOLUTE offset from output start (dstOrig + offs)
  - RLE fill (0xFE): no referencing
  - Literal copy (0x80-0xBF): no referencing
  - End marker: 0x80

This replaces the old decompress_lcw which incorrectly treated short back-refs
as absolute (standard mode) or always-relative (relative mode with 0x00 prefix).
The actual format has no mode flag — short refs are always relative, long refs always absolute.

Source: ScummVM engines/kyra/graphics/screen.cpp Screen::decodeFrame4()
"""

import struct
import os
import json
from PIL import Image

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
INDEX_FILE = "/home/bob/lol1_pak_index.json"


def decode_frame4(src, dst_size):
    """Exact ScummVM Screen::decodeFrame4 implementation."""
    dst = bytearray()
    sp = 0

    while len(dst) < dst_size and sp < len(src):
        remaining = dst_size - len(dst)
        code = src[sp]; sp += 1

        if not (code & 0x80):
            # Short back-reference: RELATIVE to current position
            length = min(remaining, (code >> 4) + 3)
            if sp >= len(src): break
            offs = ((code & 0x0F) << 8) | src[sp]; sp += 1
            ref_pos = len(dst) - offs
            for i in range(length):
                p = ref_pos + i
                dst.append(dst[p] if 0 <= p < len(dst) else 0)

        elif code & 0x40:
            length = (code & 0x3F) + 3

            if code == 0xFE:
                if sp + 2 >= len(src): break
                length = src[sp] | (src[sp+1] << 8); sp += 2
                if length > remaining: length = remaining
                fill = src[sp]; sp += 1
                dst.extend([fill] * length)

            elif code == 0xFF:
                if sp + 3 >= len(src): break
                length = src[sp] | (src[sp+1] << 8); sp += 2
                if sp + 1 >= len(src): break
                offs = src[sp] | (src[sp+1] << 8); sp += 2
                if length > remaining: length = remaining
                for i in range(length):
                    p = offs + i
                    dst.append(dst[p] if 0 <= p < len(dst) else 0)

            else:
                if sp + 1 >= len(src): break
                offs = src[sp] | (src[sp+1] << 8); sp += 2
                if length > remaining: length = remaining
                for i in range(length):
                    p = offs + i
                    dst.append(dst[p] if 0 <= p < len(dst) else 0)

        elif code != 0x80:
            length = min(remaining, code & 0x3F)
            dst.extend(src[sp:sp+length])
            sp += length

        else:
            break

    return bytes(dst)


def decode_cps(data):
    """Decode a complete CPS file to raw pixels + palette."""
    if len(data) < 10:
        return None, None

    file_size = struct.unpack_from('<H', data, 0)[0]
    comp_type = struct.unpack_from('<H', data, 2)[0]
    uncomp_size = struct.unpack_from('<I', data, 4)[0]
    pal_size = struct.unpack_from('<H', data, 8)[0]

    palette = None
    if pal_size >= 768:
        pal_raw = data[10:10+768]
        palette = []
        for i in range(256):
            r = (pal_raw[i*3] & 0x3F) * 4
            g = (pal_raw[i*3+1] & 0x3F) * 4
            b = (pal_raw[i*3+2] & 0x3F) * 4
            palette.append((r, g, b))

    payload = data[10 + pal_size:]

    if comp_type == 4:
        pixels = decode_frame4(payload, uncomp_size)
    elif comp_type == 0:
        pixels = payload[:uncomp_size]
    else:
        return None, None

    return pixels, palette


def cps_to_image(pixels, palette, width=320, height=200):
    """Convert CPS pixels + palette to PIL Image."""
    if not pixels or not palette:
        return None
    img = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if idx < len(pixels):
                ci = pixels[idx]
                img.putpixel((x, y), palette[ci] if ci < len(palette) else (0, 0, 0))
    return img


def main():
    """Decode all CPS files from the LoL1 corpus."""
    with open(INDEX_FILE) as f:
        index = json.load(f)

    output_dir = "/home/bob/lol1_cps_complete"
    os.makedirs(output_dir, exist_ok=True)

    total = 0
    success = 0
    fail = 0

    for pak_name, pak_info in sorted(index["pak_files"].items()):
        pak_path = os.path.join(PAK_DIR, pak_name)
        if not os.path.exists(pak_path):
            continue

        for entry in pak_info["entries"]:
            if not entry["name"].endswith(".CPS"):
                continue

            total += 1
            with open(pak_path, 'rb') as f:
                f.seek(entry["offset"])
                data = f.read(entry["size"])

            pixels, palette = decode_cps(data)
            if pixels and palette and len(pixels) >= 64000:
                img = cps_to_image(pixels, palette)
                if img:
                    out_name = entry["name"].replace(".CPS", ".png").lower()
                    img.save(os.path.join(output_dir, out_name))
                    success += 1
                    continue

            fail += 1
            print(f"  FAIL: {entry['name']} in {pak_name}")

    print(f"\nCPS decode: {success}/{total} success, {fail} failures")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
