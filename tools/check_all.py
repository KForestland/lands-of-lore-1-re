#!/usr/bin/env python3
"""Read an original LoL1 DATA folder and run the repository checks.

  check_all.py --data DATA       # or set $LOL1_DATA
Exit code 0 when every check passes.
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, os, subprocess, sys
from time import monotonic
import lol1lib as L

READERS = ["pak_reader", "lol1_pak_writer", "pak_indexer", "tlk_verify", "decode_frame4", "lol1_compression_writer", "cps_reader", "voc_reader",
           "fnt_reader", "xxx_reader", "dat_reader", "tlc_reader", "vcn_vmp_reader",
           "wll_parser", "cmz_analyzer", "lol1_level_writer", "tileset_mapper", "level_renderer", "shp_renderer",
           "wsa_extract", "extract_dialogue", "decode_dialogue", "extract_music", "adl_to_midi", "parse_tim", "lol1_script_writer",
           "save_reader", "xmi_to_midi", "lol1_xmi_writer", "level_report", "repo_guard", "rating", "example_images",
           "lol1_name_callers", "lol1_tim_words", "lol1_loose", "exe_tables", "palette_reader", "doc_index", "doc_links", "doc_format_offsets", "monster_reference_scan", "lol1_numbers", "lol1_mode_paths", "lol1_attack_types"]

QUICK_SKIP = {"lol1_compression_writer"}


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None)
    ap.add_argument("--check", action="store_true", help="run all checks (the default)")
    ap.add_argument("--quick", action="store_true", help="skip the slow corpus checks and list each skip")
    a = ap.parse_args()
    started = monotonic()
    quick_skipped = QUICK_SKIP if a.quick else set()
    here = os.path.dirname(os.path.abspath(__file__))
    rc = 0
    failed = []
    for r in READERS:
        if r in quick_skipped:
            print(f"SKIP {r}: quick mode")
            continue
        before = monotonic()
        p = subprocess.run([sys.executable, os.path.join(here, r + ".py"), "--check", "--data", a.data],
                           capture_output=True, text=True)
        out = (p.stdout or p.stderr).strip().splitlines()
        print(f"{out[-1] if out else r + ': no output'} [{monotonic() - before:.2f}s]")
        rc |= p.returncode
        if p.returncode:
            failed.append(r)
    # EMC2 script corpus test (tests/test_emc2_corpus.py): every INF/INI disassembles
    test = os.path.join(here, "..", "tests", "test_emc2_corpus.py")
    before = monotonic()
    p = subprocess.run([sys.executable, test, a.data], capture_output=True, text=True)
    out = (p.stdout or p.stderr).strip().splitlines()
    line = out[-1].split(": ", 1)[-1] if out else "no output"
    print(f"CHECK emc2: {line} [{monotonic() - before:.2f}s]")
    rc |= p.returncode
    if p.returncode:
        failed.append("emc2 corpus test")
    n = len(READERS) + 1
    print(f"Total elapsed: {monotonic() - started:.2f}s")
    if failed:
        print(f"{len(failed)} of {n - len(quick_skipped)} attempted checks FAILED: {', '.join(failed)}")
    elif quick_skipped:
        print(f"{n - len(quick_skipped)} CHECKS PASSED, {len(quick_skipped)} SKIPPED (quick mode)")
    else:
        print(f"ALL {n} CHECKS PASSED")
    return rc


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
