#!/usr/bin/env python3
"""Run every reader's --check against a LoL1 DATA folder and print one line each.

  check_all.py --data DATA       # or set $LOL1_DATA; runs 37 checks
Exit code 0 when every check passes.
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, os, subprocess, sys
import lol1lib as L

READERS = ["pak_reader", "pak_indexer", "tlk_verify", "decode_frame4", "cps_reader", "voc_reader",
           "fnt_reader", "xxx_reader", "dat_reader", "tlc_reader", "vcn_vmp_reader",
           "wll_parser", "cmz_analyzer", "tileset_mapper", "level_renderer", "shp_renderer",
           "wsa_extract", "extract_dialogue", "decode_dialogue", "extract_music", "adl_to_midi", "parse_tim",
           "save_reader", "xmi_to_midi", "level_report", "repo_guard", "rating", "example_images",
           "lol1_name_callers", "lol1_tim_words", "lol1_loose", "exe_tables", "palette_reader", "doc_links", "monster_reference_scan", "lol1_numbers"]


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    rc = 0
    failed = []
    for r in READERS:
        p = subprocess.run([sys.executable, os.path.join(here, r + ".py"), "--check", "--data", a.data],
                           capture_output=True, text=True)
        print((p.stdout or p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else f"{r}: no output")
        rc |= p.returncode
        if p.returncode:
            failed.append(r)
    # EMC2 script corpus test (tests/test_emc2_corpus.py): every INF/INI disassembles
    test = os.path.join(here, "..", "tests", "test_emc2_corpus.py")
    p = subprocess.run([sys.executable, test, a.data], capture_output=True, text=True)
    out = (p.stdout or p.stderr).strip().splitlines()
    print("CHECK emc2: " + (out[-1].split(": ", 1)[-1] if out else "no output"))
    rc |= p.returncode
    if p.returncode:
        failed.append("emc2 corpus test")
    n = len(READERS) + 1
    print(f"ALL {n} CHECKS PASSED" if not failed else f"{len(failed)} of {n} checks FAILED: {', '.join(failed)}")
    return rc


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
