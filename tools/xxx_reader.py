#!/usr/bin/env python3
"""Read a LoL1 automap legend file LEVELn.XXX.

Layout (ScummVM engines/kyra/engine/lol.cpp:4250-4280, loadMapLegendData;
use at :4416-4440): up to 32 records of 12 bytes (6 x uint16 LE):
  +0  symbol_x   (l[3])  map square where the legend symbol is drawn
  +2  symbol_y   (l[4])
  +4  symbol     (l[5])  index into the automap symbols, 0xFFFF = none
  +6  reveal_x   (l[0])  the legend line shows only once this square
  +8  reveal_y   (l[1])  is fully explored (block flags & 7 == 7)
  +10 string id       (l[2])  legend text, 0xFFFF = no text
Block index = x + y * 32.

  xxx_reader.py LEVEL1.XXX
  xxx_reader.py --check
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, struct
import lol1lib as L

FIELDS = ("symbol_x", "symbol_y", "symbol", "reveal_x", "reveal_y", "string_id")


def parse(b):
    return [dict(zip(FIELDS, struct.unpack_from("<6H", b, i * 12))) for i in range(min(len(b) // 12, 32))]


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", nargs="?")
    ap.add_argument("--lang", default="ENG", help="language of the legend text: ENG, FRE or GER")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        n = recs = 0; bad = []; noshape = 0; ids = set()
        for pak, name, b in L.find_all(".XXX", a.data):
            n += 1; r = parse(b); recs += len(r)
            if len(b) % 12 or len(b) // 12 > 32: bad.append(name)
            for x in r:
                if not (x["symbol_x"] < 32 and x["symbol_y"] < 32 and x["reveal_x"] < 32 and x["reveal_y"] < 32) and x["symbol"] != 0xFFFF:
                    bad.append(f"{name}:coords")
                noshape += x["symbol"] == 0xFFFF
                ids.add(x["string_id"] >> 14)
        print(f"CHECK xxx: {n} files, {recs} records (all sizes multiple of 12, <=32 records), "
              f"{noshape} without shape, string-id top bits {sorted(ids)}, bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, b = L.find_member(a.name, a.data, a.pak)
    lands = None
    try:    # legend text: ids with bit 0x4000 are in LANDS.<lang> (docs/formats/text.md)
        import decode_dialogue as T
        lands = T.file_strings(L.find_member("LANDS." + a.lang, a.data)[1])
    except Exception:
        pass
    for i, x in enumerate(parse(b)):
        text = ""
        if lands and x["string_id"] != 0xFFFF and x["string_id"] & 0x4000 and (x["string_id"] & 0x3FFF) < len(lands):
            text = '  "' + T.decode_raw(lands[x["string_id"] & 0x3FFF]).strip() + '"'
        print(i, " ".join(f"{k}={v:#06x}" if k in ("symbol", "string_id") else f"{k}={v}" for k, v in x.items()) + text)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
