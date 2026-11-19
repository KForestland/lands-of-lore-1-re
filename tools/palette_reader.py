#!/usr/bin/env python3
"""Print a LoL1 palette: its 256 colours as 6-bit VGA values (0-63) and 8-bit RGB.

Sources: docs/formats/palette.md (PAL and COL files: 256 x 3 bytes, 6-bit RGB, no
header) and docs/formats/cps.md (a CPS carries its 768-byte palette after the
10-byte header). 8-bit value = 6-bit value x 255 // 63, as lol1lib.vga_palette.

  palette_reader.py ALTPAL1.PAL                  # 256 rows: index, 6-bit, 8-bit, hex
  palette_reader.py PARCH.CPS                    # the palette inside a CPS
  palette_reader.py FXPAL.COL --out-dir DIR      # also write DIR/FXPAL_COL_swatch.png (16 x 16 squares)
  palette_reader.py --check                      # every PAL, COL and CPS palette in the game folder

Writes nothing unless --out-dir is given, and then only the swatch PNG there.
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, os
import lol1lib as L


def palette_bytes(name, blob):
    """Raw 6-bit palette bytes of a PAL/COL file or of a CPS (empty if the CPS has none)."""
    if name.upper().endswith(".CPS"):
        return bytes(L.load_bitmap(blob)[1])
    return bytes(blob)


def rows(raw, count=256):
    """[(index, (r6, g6, b6), (r8, g8, b8))] for the first `count` colours."""
    n = min(count, len(raw) // 3)
    eight = L.vga_palette(raw[:n * 3])
    return [(i, tuple(raw[i * 3:i * 3 + 3]), eight[i]) for i in range(n)]


def swatch(raw, path, cell=16):
    """16 x 16 grid of colour squares, index 0 top left, row by row."""
    from PIL import Image
    img = Image.new("RGB", (16 * cell, 16 * cell), (0, 0, 0))
    for i, _, rgb in rows(raw):
        x, y = (i % 16) * cell, (i // 16) * cell
        img.paste(rgb, (x, y, x + cell, y + cell))
    img.save(path)


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?", help="a .PAL, .COL or .CPS file (PAK member or loose)")
    ap.add_argument("--out-dir", help="write <name>_swatch.png here (needs Pillow)")
    ap.add_argument("--all", action="store_true", help="print every RGB triple of a file larger than 768 bytes")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        counts, bad, odd = {}, [], []
        for ext in (".PAL", ".COL"):
            for pak, name, b in L.find_all(ext, a.data):
                counts[ext] = counts.get(ext, 0) + 1
                if len(b) % 3 or max(b) > 63:
                    bad.append(name)
                if len(b) != 768:
                    odd.append(f"{name} {len(b)}")
        cps = withpal = 0
        for pak, name, b in L.find_all(".CPS", a.data):
            cps += 1
            pal = palette_bytes(name, b)
            if pal:
                withpal += 1
                if len(pal) != 768 or max(pal) > 63:
                    bad.append(name)
        print(f"CHECK palette: {counts.get('.PAL', 0)} PAL, {counts.get('.COL', 0)} COL, "
              f"other than 768 bytes: {odd or 'none'}; {withpal} of {cps} CPS carry a 768-byte palette; "
              f"every value 0-63 and sizes a multiple of 3, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, blob = L.find_member(a.name, a.data, a.pak)
    raw = palette_bytes(a.name, blob)
    if not raw:
        print(f"{a.name} in {pak}: no palette"); return 1
    if len(raw) % 3:
        raise ValueError(f"{a.name}: incomplete RGB triple")
    print(f"{a.name.upper()} in {pak}: {len(raw)} palette bytes = {len(raw) // 3} colours"
          + ("" if len(raw) <= 768 or a.all else "; first 256 shown (--all for every one)"))
    print("index  6-bit r  g  b   8-bit   r   g   b  hex")
    for i, six, rgb in rows(raw, len(raw) // 3 if a.all else 256):
        print(f"{i:5d}        {six[0]:2d} {six[1]:2d} {six[2]:2d}         {rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d}  "
              f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}")
    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
        path = os.path.join(a.out_dir, a.name.upper().replace(".", "_") + "_swatch.png")
        swatch(raw, path)
        print("wrote", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
