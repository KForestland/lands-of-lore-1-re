#!/usr/bin/env python3
"""Read a LoL1 DOS font (.FNT) and optionally write a glyph atlas PNG.

Layout (ScummVM engines/kyra/graphics/screen.cpp:3678-3706, DOSFont::load,
and :3714-3760 DOSFont::drawChar):
  +0  uint16 file size
  +2  uint16 signature 0x0500
  +4  uint16 offset of the descriptor (desc)
  +6  uint16 offset of the glyph bitmap-offset table (uint16 per glyph)
  +8  uint16 offset of the width table (uint8 per glyph)
  +12 uint16 offset of the height table (2 x uint8 per glyph: blank rows on
      top, drawn rows)
  desc+3 = last glyph index (numGlyphs - 1), desc+4 = height, desc+5 = width
  Glyph bitmap: 4 bits per pixel, low nibble first, rows of ceil(w/2) bytes.
  A glyph whose bitmap offset is 0 is not drawn.

Loaded as FONT6P/FONT9P (lol.cpp:596-597) and FONT6PN/FONT9PN for the
automap (lol.cpp:4123-4124).

  fnt_reader.py FONT9P.FNT [--png atlas.png]
  fnt_reader.py --check
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, struct
import lol1lib as L


def parse(b):
    size, sig, desc, bmo, wto, _, hto = struct.unpack_from("<7H", b, 0)
    n = b[desc + 3] + 1
    glyphs = []
    for i in range(n):
        off = struct.unpack_from("<H", b, bmo + 2 * i)[0]
        w = b[wto + i]; top = b[hto + 2 * i]; rows = b[hto + 2 * i + 1]
        glyphs.append({"offset": off, "width": w, "top": top, "rows": rows})
    return {"size_field": size, "signature": hex(sig), "glyphs": n,
            "height": b[desc + 4], "width": b[desc + 5]}, glyphs


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--out", "--png")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        out = []; bad = []
        for pak, name, b in L.find_all(".FNT", a.data):
            h, g = parse(b)
            drawn = sum(1 for x in g if x["offset"] and x["width"])
            ok = h["signature"] == "0x500" and h["size_field"] == len(b) and \
                all(x["top"] + x["rows"] <= h["height"] for x in g) and \
                all(not x["offset"] or x["offset"] + ((x["width"] + 1) // 2) * x["rows"] <= len(b) for x in g)
            out.append(f"{name}({pak}) {h['glyphs']} glyphs {drawn} drawn h{h['height']}")
            if not ok: bad.append(name)
        print("CHECK fnt:", "; ".join(out), "bad=", bad or "none")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, b = L.find_member(a.name, a.data, a.pak)
    h, g = parse(b)
    print(a.name, pak, h)
    if a.out:
        from PIL import Image
        cw = max(x["width"] for x in g) + 1; ch = h["height"] + 1
        img = Image.new("L", (16 * cw, ((len(g) + 15) // 16) * ch), 0)
        for i, x in enumerate(g):
            if not x["offset"]: continue
            p = x["offset"]; bw = (x["width"] + 1) // 2
            for r in range(x["rows"]):
                for c in range(x["width"]):
                    v = b[p + r * bw + c // 2]
                    v = (v >> 4) if c & 1 else (v & 15)
                    if v: img.putpixel(((i % 16) * cw + c, (i // 16) * ch + x["top"] + r), 255)
        img.save(a.out); print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
