#!/usr/bin/env python3
"""Verify the CD speech files NN.TLK: PAK containers of VOC samples.

Rewritten 2026-11-18. The March version ran on start (no --help), wrote into
fixed folders, and paired each member name with the next member's offset in
its sample list. See docs/formats/tlk.md.

Checks per file (ScummVM LoLEngine::loadTalkFile opens "%02d.TLK" as a PAK,
engines/kyra/engine/lol.cpp:1892-1902; names built in
engines/kyra/sound/sound_lol.cpp:59-81):
  - the PAK directory parses and the members tile the file exactly;
  - every member starts "Creative Voice File" and parses as VOC;
  - member names follow the speech patterns
      NNN<c><d>.TT  (id < 1000, speaker letter or "_", part digit, TLK number)
      NNN<c><d>.00  (hex id, global lines, TLK 00)
      @NNNN<c>.TT   (id >= 1000)
    or the NNNNN.VOC form (counted separately).

  tlk_verify.py                  # one line per TLK
  tlk_verify.py --out tlk.json   # per-file details
  tlk_verify.py --check          # one line, exit 1 on any failure
"""
import os
import re
import sys

import lol1lib as L
import voc_reader

SPEECH = re.compile(r"^(?:[0-9A-F]{3}[A-Z_][0-9]|@[0-9]{4}[A-Z_])\.([0-9]{2})$")
PLAIN = re.compile(r"^[0-9]{5}\.VOC$")


def verify(path):
    d = open(path, "rb").read()
    entries = L.pak_entries(d)
    tlk_no = os.path.basename(path)[:2]
    res = {"file": os.path.basename(path), "members": len(entries), "directory_end": entries[0][1] if entries else None,
           "tiles_exactly": bool(entries) and entries[-1][1] + entries[-1][2] == len(d),
           "voc_ok": 0, "speech_names": 0, "plain_voc_names": 0, "other_names": [], "wrong_tlk_number": []}
    for name, off, size in entries:
        try:
            voc_reader.parse(d[off:off + size]); res["voc_ok"] += 1
        except Exception:
            pass
        m = SPEECH.match(name)
        if m:
            res["speech_names"] += 1
            if m.group(1) not in (tlk_no, "00"):
                res["wrong_tlk_number"].append(name)
        elif PLAIN.match(name):
            res["plain_voc_names"] += 1
        else:
            res["other_names"].append(name)
    res["samples"] = [f"{n}@{o}" for n, o, _ in entries[:3]]
    return res


def main():
    a = L.tool_args(__doc__).parse_args()
    files = sorted(f for f in os.listdir(a.data) if re.match(r"^\d\d\.TLK$", f.upper()))
    results = [verify(os.path.join(a.data, f)) for f in files]
    if a.check:
        members = sum(r["members"] for r in results)
        bad = [r["file"] for r in results if not r["tiles_exactly"] or r["voc_ok"] != r["members"]
               or r["other_names"] or r["wrong_tlk_number"]]
        print(f"CHECK tlk: {len(results)} files, {members} members, all VOC: "
              f"{sum(r['voc_ok'] for r in results)}/{members}, speech-pattern names "
              f"{sum(r['speech_names'] for r in results)}, NNNNN.VOC names {sum(r['plain_voc_names'] for r in results)}, "
              f"bad={bad or 'none'}")
        return 0 if not bad and results else 1
    for r in results:
        print(f"{r['file']}: {r['members']} members, directory ends {r['directory_end']}, VOC {r['voc_ok']}, "
              f"first {', '.join(r['samples'])}, other names {r['other_names'][:3]}")
    if a.out:
        L.write_json(a.out, results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
