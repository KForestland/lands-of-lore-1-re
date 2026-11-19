#!/usr/bin/env python3
"""Read a LoL1 CPS image (320x200, 8-bit) and optionally write a PNG.

Header (ScummVM engines/kyra/graphics/screen.cpp:3355-3401, Screen::loadBitmap):
  +0 uint16  size field (not read by loadBitmap)
  +2 uint8   compression type (4 = Frame4/LCW, 0 = raw)
  +4 uint32  uncompressed size (64000 for a full screen)
  +8 uint16  palette size; palette bytes (6-bit VGA RGB) follow at +10
  then the (compressed) pixel data.

  cps_reader.py PARCH.CPS               # print header
  cps_reader.py PARCH.CPS --png out.png --pal-from SWAMP.CPS
  cps_reader.py --check                 # decode every CPS in the DATA folder
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse
import lol1lib as L


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--png", help="write a PNG (needs Pillow)")
    ap.add_argument("--pal-from", help="take the palette from another CPS or a .PAL/.COL file when this one has none")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        n = 0; bad = []; withpal = 0; types = {}
        for pak, name, blob in L.find_all(".CPS", a.data):
            n += 1
            try:
                h, pal, px = L.load_bitmap(blob)
                ok = len(px) == h["uncompressed_size"] and h["size_field"] + 2 == len(blob)
                types[h["comp_type"]] = types.get(h["comp_type"], 0) + 1
                withpal += bool(h["palette_size"])
                if not ok: bad.append(name)
            except Exception as ex:
                bad.append(f"{name}:{ex}")
        print(f"CHECK cps: {n} files, comp types {types}, {withpal} with palette, "
              f"size_field+2==file size and full decode: {n-len(bad)}/{n}, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, blob = L.find_member(a.name, a.data, a.pak)
    h, pal, px = L.load_bitmap(blob)
    if h["size_field"] + 2 != len(blob) or len(px) != h["uncompressed_size"]:
        raise ValueError(f"{a.name}: bitmap size does not match the bytes read")
    print(f"{a.name} in {pak}: {h}, decoded {len(px)} bytes")
    if a.png:
        from PIL import Image
        if not pal and a.pal_from:
            _, pb = L.find_member(a.pal_from, a.data)
            pal = L.load_bitmap(pb)[1] if a.pal_from.upper().endswith(".CPS") else pb[:768]
        img = Image.frombytes("P", (320, len(px) // 320), bytes(px))
        if pal:
            flat = [c for rgb in L.vga_palette(pal) for c in rgb]
            img.putpalette(flat + [0] * (768 - len(flat)))
        img.save(a.png); print("wrote", a.png)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
