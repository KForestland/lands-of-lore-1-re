#!/usr/bin/env python3
"""Read LoL1 CPS images and decode their Frame4 payloads.


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

from cli_errors import run_cli
import struct
import os
import json


import lol1lib as L

USAGE = """
  decode_frame4.py --out cps/   # every CPS to PNG
  decode_frame4.py --check          # this file's decoder vs lol1lib.decode_frame4 on every
                                    # CPS, CMZ, VCN and VMP (two independent ports must agree)
"""


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
    from PIL import Image
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
    ap = L.tool_args(__doc__ + USAGE, out_help="write one decoded PNG per CPS to this directory", out_aliases=("--out-dir",))

    a = ap.parse_args()
    if a.check:
        n = same = 0; bad = []
        for ext in (".CPS", ".CMZ", ".VCN", ".VMP"):
            for pak, name, data in L.find_all(ext, a.data):
                h = L.bitmap_header(data)
                payload = data[10 + h["palette_size"]:]
                x = decode_frame4(payload, h["uncompressed_size"])
                y = L.decode_frame4(payload, h["uncompressed_size"])
                n += 1
                if x == y and len(x) == h["uncompressed_size"]:
                    same += 1
                else:
                    bad.append(name)
        print(f"CHECK frame4: {n} files (CPS, CMZ, VCN, VMP), both decoders agree and reach the stated size: "
              f"{same}/{n}, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.out:
        ap.print_help(); return 2
    os.makedirs(a.out, exist_ok=True)
    total = ok = 0
    for pak, name, data in L.find_all(".CPS", a.data):
        total += 1
        pixels, palette = decode_cps(data)
        if pixels and palette and len(pixels) >= 64000:
            img = cps_to_image(pixels, palette)
            if img:
                img.save(os.path.join(a.out, name.replace(".CPS", ".png").lower()))
                ok += 1
                continue
        print(f"  FAIL: {name} in {pak}")
    print(f"CPS decode: {ok}/{total}, output {a.out}")
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
