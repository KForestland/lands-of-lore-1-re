#!/usr/bin/env python3
"""Read LoL1 WSA animation chunks and their palette inputs.

Rewritten 2026-11-18 to follow ScummVM exactly; the March version used its
own offset model ("4-byte gap", absolute vs relative guesses) plus a
palette-offset fix for two files. See docs/formats/wsa.md.

Layout (ScummVM engines/kyra/graphics/wsamovie.cpp:361-456, WSAMovie_v2::open):
  +0  uint16 frame count n      +2 int16 x add    +4 int16 y add
  +6  uint16 width              +8 uint16 height  +10 uint16 delta buffer size
  +12 uint16 flags (bit0: 768-byte palette follows the offset table)
  +14 uint32 offset[0..n+1]; offset[0] == 0 means "no first frame"; offset[1]
      is then the base. The table ends at 22 + 4n either way. Frame i lies at
      (start of frame data) + offset[i] - offset[0] (wsamovie.cpp:418-433);
      the frame data starts after the table and the palette.
  palette (if bit0), then frame data.
Each frame: Frame4 data that decodes (into the delta buffer) to a delta
stream; the delta is XORed onto the previous picture (Screen::decodeFrameDelta,
engines/kyra/graphics/screen.cpp:2533-2594). Frame 0 is XORed onto a blank
picture (wsamovie.cpp:133-147, :208-218). Entry n is the loop-back frame.

  wsa_extract.py NAME.WSA                         # header and frame table
  wsa_extract.py NAME.WSA --out f/ [--all]    # frame 0 PNG, or every frame
  wsa_extract.py --check                          # decode every frame of every WSA
"""
from cli_errors import run_cli
import os
import struct

import lol1lib as L


def delta_xor(dst, src, limit):
    """Screen::decodeFrameDelta (XOR form). Returns True when it ends cleanly."""
    s = d = 0
    try:
        while True:
            code = src[s]; s += 1
            if code == 0:
                ln = src[s]; v = src[s + 1]; s += 2
                for _ in range(ln):
                    dst[d] ^= v; d += 1
            elif code & 0x80:
                code -= 0x80
                if code:
                    d += code
                else:
                    sub = src[s] | src[s + 1] << 8; s += 2
                    if sub == 0:
                        return d <= limit
                    if sub & 0x8000:
                        sub -= 0x8000
                        if sub & 0x4000:
                            v = src[s]; s += 1
                            for _ in range(sub - 0x4000):
                                dst[d] ^= v; d += 1
                        else:
                            for _ in range(sub):
                                dst[d] ^= src[s]; d += 1; s += 1
                    else:
                        d += sub
            else:
                for _ in range(code):
                    dst[d] ^= src[s]; d += 1; s += 1
    except IndexError:
        return False


def parse(b):
    n, xa, ya, w, h, dbs, flags = struct.unpack_from("<HhhHHHH", b, 0)
    p = 14
    first = struct.unpack_from("<I", b, p)[0]; p += 4
    has_first = first != 0
    if not has_first:
        first = struct.unpack_from("<I", b, p)[0]
    offs = [first]
    for i in range(1, n + 2):
        offs.append(struct.unpack_from("<I", b, p)[0]); p += 4
    pal = b[p:p + 768] if flags & 1 else None
    return {"frames": n & 0x7FFF, "x_add": xa, "y_add": ya, "width": w, "height": h,
            "delta_buffer": dbs, "flags": flags, "has_first_frame": has_first,
            "offsets": offs, "palette": pal, "data_start": p + (768 if flags & 1 else 0)}


def frames(b, info=None):
    """Yield (index, picture bytes, clean) for frames 0..n-1."""
    info = info or parse(b)
    w, h = info["width"], info["height"]
    pic = bytearray(w * h)
    for i in range(info["frames"]):
        if i == 0 and not info["has_first_frame"]:
            yield i, bytes(pic), True
            continue
        off = info["data_start"] + info["offsets"][i] - info["offsets"][0]
        delta = L.decode_frame4(b[off:], info["delta_buffer"])
        ok = delta_xor(pic, delta, w * h)
        yield i, bytes(pic), ok


def main():
    ap = L.tool_args(__doc__, out_help="write the selected frame PNGs to this directory", out_aliases=("--out-dir",))
    ap.add_argument("name", nargs="?")

    ap.add_argument("--all", action="store_true", help="write every frame, not only frame 0")
    ap.add_argument("--pal-from", default="PARCH.CPS", help="palette when the WSA has none")
    a = ap.parse_args()
    if a.check:
        nfiles = nframes = clean = 0; bad = []; first_ok = 0
        for pak, name, b in L.find_all(".WSA", a.data):
            nfiles += 1
            info = parse(b)
            first_ok += info["offsets"][0] == info["data_start"]
            for i, pic, ok in frames(b, info):
                nframes += 1; clean += ok
                if not ok:
                    bad.append(f"{name}#{i}")
        print(f"CHECK wsa: {nfiles} files, {nframes} frames, every delta ends at its terminator inside "
              f"width*height: {clean}/{nframes}; offset[0] == start of frame data: {first_ok}/{nfiles}; "
              f"bad={bad[:6] or 'none'} ({len(bad)})")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, b = L.find_member(a.name, a.data, a.pak)
    info = parse(b)
    print(a.name, pak, {k: v for k, v in info.items() if k not in ("palette", "offsets")},
          "offsets[:4]", info["offsets"][:4])
    if a.out:
        from PIL import Image
        pal = info["palette"]
        if pal is None:
            _, pb = L.find_member(a.pal_from, a.data)
            pal = L.load_bitmap(pb)[1] if a.pal_from.upper().endswith(".CPS") else pb[:768]
        flat = [c for rgb in L.vga_palette(pal) for c in rgb]
        os.makedirs(a.out, exist_ok=True)
        stem = a.name.rsplit(".", 1)[0].lower()
        for i, pic, ok in frames(b, info):
            img = Image.frombytes("P", (info["width"], info["height"]), pic)
            img.putpalette(flat + [0] * (768 - len(flat)))
            img.save(os.path.join(a.out, f"{stem}_{i:03d}.png"))
            if not a.all:
                break
        print("wrote PNGs to", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
