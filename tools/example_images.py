#!/usr/bin/env python3
"""Check that every image in examples/ is exactly what today's tools make from the game files.

  example_images.py --data DATA --check            # regenerate each example in a temporary folder and compare pixels
  example_images.py --data DATA --out-dir new/     # write today's versions (to replace stale examples)

Each example is listed in EXAMPLES with the tool command that makes it (also in examples/README.md).
Pixels are compared after conversion to RGBA, so PNG compression settings do not matter.
"""
from cli_errors import run_cli
import os
import subprocess
import sys
import tempfile

import lol1lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(HERE, "..", "examples")

# example file -> (tool, arguments, the file the tool writes)
EXAMPLES = {
    "examples/guard_frame_000.png": ("shp_renderer.py", ["GUARD.SHP", "--level", "1"], "guard_000.png"),
    "examples/knowltk1_frame_000.png": ("wsa_extract.py", ["KNOWLTK1.WSA", "--pal-from", "KNOWLTK.CPS"], "knowltk1_000.png"),
    "examples/level01_schematic.png": ("level_renderer.py", ["--level", "1", "--schematic"], "level01_schematic.png"),
    "docs/images/level01_schematic.png": ("level_renderer.py", ["--level", "1", "--schematic"], "level01_schematic.png"),
    "docs/images/level12_schematic.png": ("level_renderer.py", ["--level", "12", "--schematic"], "level12_schematic.png"),
}
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def make(data_dir, name, out_dir):
    tool, args, produced = EXAMPLES[name]
    with tempfile.TemporaryDirectory() as tmp:
        p = subprocess.run([sys.executable, os.path.join(HERE, tool), *args, "--data", data_dir, "--out-dir", tmp],
                           capture_output=True, text=True)
        if p.returncode:
            raise ValueError(f"{name}: {tool} failed: {(p.stderr or p.stdout).strip()[-200:]}")
        source = os.path.join(tmp, produced)
        with open(source, "rb") as f:
            data = f.read()
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, os.path.basename(name)), "wb") as f:
            f.write(data)
    return data


def pixels(blob):
    import io
    from PIL import Image
    image = Image.open(io.BytesIO(blob)).convert("RGBA")
    return image.size, image.tobytes()


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("--out-dir", help="write today's versions of the examples here")
    a = ap.parse_args()
    if not (a.check or a.out_dir):
        ap.print_help(); return 2
    tracked = sorted(f"{d}/{n}" for d in ("examples", "docs/images")
                     for n in os.listdir(os.path.join(ROOT, d)) if n.lower().endswith(".png"))
    if not L.is_cd_layout(a.data):
        print("CHECK example_images: the examples are made from the CD edition; this copy is not compared")
        return 0
    stale = []
    for name in sorted(EXAMPLES):
        today = make(a.data, name, a.out_dir)
        path = os.path.join(ROOT, name)
        if a.check and (not os.path.exists(path) or pixels(open(path, "rb").read()) != pixels(today)):
            stale.append(name)
    unlisted = [n for n in tracked if n not in EXAMPLES]
    if a.check:
        if stale or unlisted:
            print(f"CHECK example_images: FAIL stale {stale or 'none'}, not made by a listed command {unlisted or 'none'}")
            return 1
        print(f"CHECK example_images: {len(EXAMPLES)} shown images (examples/ and docs/images/) equal today's tool output pixel for pixel")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
