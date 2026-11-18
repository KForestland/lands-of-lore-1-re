#!/usr/bin/env python3
"""LoL1 SHP shape reader and renderer, following ScummVM's drawing code.

Rewritten 2026-11-18. The March version read each shape 2 bytes too early
(it took offsets from file start; they count from byte 2) and so saw a
"2-byte prefix", and it decoded pixels with a skip/copy-run model plus
catch-all fallbacks. Both are replaced here. See docs/formats/shp.md.

File (ScummVM engines/kyra/graphics/screen_v2.cpp:192-201 getPtrToShape;
engines/kyra/engine/scene_lol.cpp:216-233):
  +0 uint16 n; +2 uint32 offsets[n] (an end entry follows); shape i starts at
  offsets[i] + 2. Offset 0 = no shape.
  A few SHP files are themselves wrapped in the CPS bitmap container
  (Frame4); they are unwrapped first (e.g. FXPAL.SHP, loaded with
  loadBitmap at engines/kyra/engine/lol.cpp:1871).

Shape (engines/kyra/graphics/screen.cpp:1805-1842, Screen::drawShape;
header writer encodeShape :2833-2846):
  +0 uint16 flags   bit0 = colour table follows, bit1 = NOT Frame4-compressed,
                    bit2 = colour-table length byte follows (non-Kyra1)
  +2 uint8  height
  +3 uint16 width
  +5 uint8  height (again)
  +6 uint16 shape size (bytes of this shape)
  +8 uint16 frame size (size of the line data after decompression)
  +10 [uint8 colour count if bit2] [colour table: count (default 16) bytes if bit0]
  then line data (Frame4-compressed unless bit1).
  The demo edition has 2 extra leading bytes (useAltShapeHeader,
  engines/kyra/detection.h:51, detection_tables.h:63): --alt-header.

Line data (screen.cpp:2095-2108): per row, `width` pixels; a nonzero byte is
one pixel (mapped through the colour table when bit0), `0, n` skips n
transparent pixels.

  shp_renderer.py KEEP.SHP --out-dir shapes/ [--pal-from PARCH.CPS]
      (colours: monster and item shapes are drawn through the scene palette
       and runtime colour tables, so a CPS palette gives wrong colours)
  shp_renderer.py --check      # every shape in every SHP decodes exactly
  shp_renderer.py --out inv.json   # per-file inventory (data/shp_inventory.json)
"""
import os
import struct
import sys

import lol1lib as L


def unwrap(blob):
    """Undo the CPS bitmap container if the file has one."""
    if len(blob) > 10 and blob[2] == 4 and struct.unpack_from("<H", blob, 0)[0] + 2 == len(blob):
        return L.load_bitmap(blob)[2]
    return blob


def shape_offsets(d):
    n = struct.unpack_from("<H", d, 0)[0]
    return [struct.unpack_from("<I", d, 2 + 4 * i)[0] for i in range(n)]


def decode_shape(d, pos, alt=False):
    """Return dict(width, height, flags, pixels, consumed_ok) for the shape at pos."""
    if alt:
        pos += 2
    flags, h, w, h2, ssize, fsize = struct.unpack_from("<HBHBHH", d, pos)
    p = pos + 10
    ncol = 16
    if flags & 4:
        ncol = d[p]; p += 1
    ctab = None
    if flags & 1:
        ctab = d[p:p + ncol]; p += ncol
    if flags & 2:
        lines = d[p:p + fsize]
    else:
        lines = L.decode_frame4(d[p:], fsize)
    px = bytearray(w * h)
    s = 0
    ok = True
    for y in range(h):
        x = 0
        while x < w:
            if s >= len(lines):
                ok = False; break
            c = lines[s]; s += 1
            if c:
                px[y * w + x] = ctab[c] if ctab is not None and c < len(ctab) else c
                x += 1
            else:
                if s >= len(lines):
                    ok = False; break
                x += lines[s]; s += 1
        if x != w:
            ok = False
    return {"width": w, "height": h, "height2": h2, "flags": flags, "shape_size": ssize,
            "frame_size": fsize, "pixels": bytes(px),
            "exact": ok and s == fsize and h == h2 and len(lines) == fsize}


def read_shp(blob, alt=False):
    d = unwrap(blob)
    out = []
    for off in shape_offsets(d):
        out.append(None if off == 0 else decode_shape(d, off + 2, alt))
    return out


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("name", nargs="?", help="SHP member name, e.g. KEEP.SHP")
    ap.add_argument("--out-dir", help="write one PNG per shape here")
    ap.add_argument("--pal-from", default="PARCH.CPS", help="CPS (or .PAL/.COL) to take the palette from")
    ap.add_argument("--alt-header", action="store_true", help="demo edition: 2 extra bytes before each shape header")
    a = ap.parse_args()
    if a.check:
        files = shapes = exact = empty = 0; bad = []
        for pak, name, blob in L.find_all(".SHP", a.data):
            files += 1
            try:
                for i, sh in enumerate(read_shp(blob, a.alt_header)):
                    if sh is None:
                        empty += 1; continue
                    shapes += 1
                    if sh["exact"]:
                        exact += 1
                    else:
                        bad.append(f"{name}#{i}")
            except Exception as ex:
                bad.append(f"{name}:{type(ex).__name__}")
        print(f"CHECK shp: {files} files, {shapes} shapes (+{empty} empty slots), decoded exactly "
              f"(rows fill width, line data == frame size, height == height copy): {exact}/{shapes}, "
              f"bad={bad[:8] or 'none'}{' ...' if len(bad) > 8 else ''} ({len(bad)})")
        return 0 if not bad else 1
    if a.out and not a.name:
        files = []
        for pak, name, blob in L.find_all(".SHP", a.data):
            shapes = [x for x in read_shp(blob, a.alt_header) if x]
            flags = {}
            for x in shapes:
                flags[f"{x['flags']:#06x}"] = flags.get(f"{x['flags']:#06x}", 0) + 1
            files.append({"pak": pak, "name": name, "size": len(blob),
                          "wrapped_in_bitmap_container": unwrap(blob) is not blob,
                          "shapes": len(shapes), "decoded_exactly": sum(x["exact"] for x in shapes),
                          "flags": flags, "max_width": max((x["width"] for x in shapes), default=0),
                          "max_height": max((x["height"] for x in shapes), default=0)})
        L.write_json(a.out, {"description": "LoL1 SHP inventory from tools/shp_renderer.py (ScummVM-exact decode, 2026-11-18). "
                             "Replaces the March inventory and render results, which used a 2-byte offset slip and fallbacks.",
                             "total_files": len(files), "total_shapes": sum(f["shapes"] for f in files),
                             "decoded_exactly": sum(f["decoded_exactly"] for f in files), "files": files})
        return 0
    if not a.name:
        ap.print_help(); return 2
    pak, blob = L.find_member(a.name, a.data, a.pak)
    shapes = read_shp(blob, a.alt_header)
    for i, sh in enumerate(shapes):
        if sh:
            print(f"{i:3d} {sh['width']}x{sh['height']} flags={sh['flags']:#06x} frame_size={sh['frame_size']} exact={sh['exact']}")
    if a.out_dir:
        from PIL import Image
        _, pb = L.find_member(a.pal_from, a.data)
        pal = L.load_bitmap(pb)[1] if a.pal_from.upper().endswith(".CPS") else pb[:768]
        flat = [c for rgb in L.vga_palette(pal) for c in rgb]
        os.makedirs(a.out_dir, exist_ok=True)
        stem = a.name.rsplit(".", 1)[0].lower()
        for i, sh in enumerate(shapes):
            if not sh or not sh["width"] or not sh["height"]:
                continue
            img = Image.frombytes("P", (sh["width"], sh["height"]), sh["pixels"])
            img.putpalette(flat + [0] * (768 - len(flat)))
            img.info["transparency"] = 0
            img.save(os.path.join(a.out_dir, f"{stem}_{i:03d}.png"))
        print("wrote PNGs to", a.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
