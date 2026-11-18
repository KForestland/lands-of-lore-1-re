#!/usr/bin/env python3
"""Run every reader's --check against a LoL1 DATA folder and print one line each.

  check_all.py [--data DATA]     # default $LOL1_DATA or the project reference path
Exit code 0 when every check passes.
"""
import argparse, os, subprocess, sys
import lol1lib as L

READERS = ["pak_reader", "pak_indexer", "tlk_verify", "decode_frame4", "cps_reader", "voc_reader",
           "fnt_reader", "xxx_reader", "dat_reader", "tlc_reader", "vcn_vmp_reader",
           "wll_parser", "cmz_analyzer", "tileset_mapper", "level_renderer", "shp_renderer",
           "wsa_extract", "extract_dialogue", "decode_dialogue", "extract_music", "parse_tim"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=L.DEFAULT_DATA)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    rc = 0
    for r in READERS:
        p = subprocess.run([sys.executable, os.path.join(here, r + ".py"), "--check", "--data", a.data],
                           capture_output=True, text=True)
        print((p.stdout or p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else f"{r}: no output")
        rc |= p.returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
