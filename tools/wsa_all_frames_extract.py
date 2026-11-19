#!/usr/bin/env python3
"""Extract every frame of every LoL1 WSA (or of the named ones) to PNG.

Rewritten 2026-11-18 as a batch front end for wsa_extract.py, which holds
the ScummVM-exact decoder (docs/formats/wsa.md). The March version only took
the top-20 files from an earlier inventory and needed a palette fix for
ESCAPE.WSA and CHANDELR.WSA; with the offsets read as ScummVM does
(relative to the start of frame data, after the palette) no fix is needed.

  wsa_all_frames_extract.py --out-dir frames/                 # all WSAs
  wsa_all_frames_extract.py --out-dir frames/ ESCAPE.WSA ...  # some
  wsa_all_frames_extract.py --check                           # same check as wsa_extract.py
"""
from cli_errors import run_cli
import os
import sys

import lol1lib as L
import wsa_extract as W


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("names", nargs="*")
    ap.add_argument("--out-dir")
    ap.add_argument("--pal-from", default="PARCH.CPS")
    a = ap.parse_args()
    if a.check:
        sys.argv = [sys.argv[0], "--check", "--data", a.data]
        return W.main()
    if not a.out_dir:
        ap.print_help(); return 2
    from PIL import Image
    _, pb = L.find_member(a.pal_from, a.data)
    default_pal = L.load_bitmap(pb)[1] if a.pal_from.upper().endswith(".CPS") else pb[:768]
    wanted = {n.upper() for n in a.names}
    files = frames = 0
    for pak, name, b in L.find_all(".WSA", a.data):
        if wanted and name not in wanted:
            continue
        info = W.parse(b)
        flat = [c for rgb in L.vga_palette(info["palette"] or default_pal) for c in rgb]
        d = os.path.join(a.out_dir, name.rsplit(".", 1)[0].lower())
        os.makedirs(d, exist_ok=True)
        for i, pic, ok in W.frames(b, info):
            img = Image.frombytes("P", (info["width"], info["height"]), pic)
            img.putpalette(flat + [0] * (768 - len(flat)))
            img.save(os.path.join(d, f"frame_{i:03d}.png"))
            frames += 1
        files += 1
    print(f"wrote {frames} frames of {files} WSA files to {a.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
