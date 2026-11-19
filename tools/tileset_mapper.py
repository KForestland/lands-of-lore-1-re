#!/usr/bin/env python3
"""LoL1 level -> area tile set mapping, from the level files themselves.

Rewritten 2026-11-18. The March version read the CMZ map as uint16 "tile IDs"
and guessed the tile set from their high bytes; that reading was wrong (see
docs/formats/cmz.md) and its output data/tileset_mapping.json is replaced.

Two sources per level:

1. LEVELn.WLL bytes 0-1: index into the executable's area list, which picks
   AREA.SHP and AREA.DAT (ScummVM engines/kyra/engine/scene_lol.cpp:147-149;
   list devtools/create_kyradat/resources/lol_dos.h:669-699,
   kLoLLevelShpListDOS / kLoLLevelDatListDOS).
2. Every call of script function 0x09 loadLevelGraphics in LEVELn.INI and
   LEVELn.INF: its first argument names the VCN/VMP set, its sixth an
   optional override palette (engines/kyra/script/script_lol.cpp:208-212).
   The script scan is a minimal EMC2 reader: it remembers the constants
   pushed before a sysCall (opcodes 3/4) and reads string arguments from the
   TEXT chunk. For the full disassembler see the EMC2 work (docs/formats/emc2.md).

  tileset_mapper.py                 # table
  tileset_mapper.py --out map.json  # JSON
  tileset_mapper.py --check         # every level has a WLL area and >= 1 graphics load
"""
from cli_errors import run_cli
import struct

import lol1lib as L

AREAS = ["KEEP", "FOREST1", "MANOR", "CAVE1", "SWAMP", "URBISH", "MINE1",
         "TOWER1", "YVEL1", "CATWALK", "RUIN", "CIMMERIA"]


def emc_chunks(b):
    out, p = {}, 12
    while p + 8 <= len(b):
        tag = b[p:p + 4]
        n = struct.unpack_from(">I", b, p + 4)[0]
        out[tag] = b[p + 8:p + 8 + n]
        p += 8 + n + (n & 1)
    return out


def emc_text(chunk):
    if not chunk:
        return []
    first = struct.unpack_from(">H", chunk, 0)[0]
    offs = struct.unpack_from(f">{first // 2}H", chunk, 0)
    return [chunk[o:chunk.index(b"\0", o)].decode("latin-1") for o in offs]


def graphics_calls(script):
    """[(vcn_name, palette_name_or_None)] for each sysCall 0x09."""
    ch = emc_chunks(script)
    text = emc_text(ch.get(b"TEXT", b""))
    words = struct.unpack(f">{len(ch[b'DATA']) // 2}H", ch[b"DATA"])
    heads = {o for o in struct.unpack(f">{len(ch[b'ORDR']) // 2}H", ch[b"ORDR"]) if o != 0xFFFF}
    pushes, calls, i = [], [], 0
    while i < len(words):
        if i in heads:
            i += 1; pushes = []; continue
        w = words[i]; i += 1
        op, arg = (w >> 8) & 0x1F, 0
        if w & 0x8000:
            op = 0
        elif w & 0x4000:
            arg = (w & 0xFF) - (0x100 if w & 0x80 else 0)
        elif w & 0x2000:
            arg = words[i]; i += 1
            arg -= 0x10000 if arg & 0x8000 else 0
        if op in (3, 4):
            pushes.append(arg); continue
        if op == 14 and (arg & 0xFF) == 0x09 and len(pushes) >= 6:
            a0, a5 = pushes[-1], pushes[-6]
            name = text[a0] if 0 <= a0 < len(text) else f"?{a0}"
            pal = text[a5] if 0 <= a5 < len(text) else None
            calls.append((name, pal))
        pushes = []
    return calls


def build(data_dir):
    rows = {}
    for lv in range(1, 30):
        wll = L.level_member(lv, "WLL", data_dir)
        idx = struct.unpack_from("<H", wll, 0)[0] if wll else None
        gfx = []
        for ext in ("INI", "INF"):
            s = L.level_member(lv, ext, data_dir)
            if s and s[:4] == b"FORM":
                gfx += [(ext, n, p) for n, p in graphics_calls(s)]
        rows[lv] = {"wll_area_index": idx,
                    "area_shp_dat": AREAS[idx] if idx is not None and idx < len(AREAS) else None,
                    "loadLevelGraphics": [{"script": e, "vcn_vmp": n, "palette": p} for e, n, p in gfx]}
    return rows


def main():
    a = L.tool_args(__doc__).parse_args()
    rows = build(a.data)
    if a.check:
        bad = [lv for lv, r in rows.items() if r["area_shp_dat"] is None or not r["loadLevelGraphics"]]
        sets = sorted({g["vcn_vmp"].upper() for r in rows.values() for g in r["loadLevelGraphics"]})
        ncalls = sum(len(r["loadLevelGraphics"]) for r in rows.values())
        print(f"CHECK tileset: {len(rows)} levels, {ncalls} loadLevelGraphics calls, VCN sets named {sets}, bad={bad or 'none'}")
        return 0 if not bad else 1
    for lv, r in rows.items():
        g = "; ".join(f"{x['script']}:{x['vcn_vmp']}" + (f"+{x['palette']}" if x["palette"] else "")
                      for x in r["loadLevelGraphics"])
        print(f"L{lv:02d}  WLL area {r['wll_area_index']:2d} {r['area_shp_dat']:<9} graphics: {g}")
    if a.out:
        L.write_json(a.out, {
            "description": "LoL1 level -> area mapping from LEVELn.WLL bytes 0-1 and loadLevelGraphics calls in LEVELn.INI/INF (tools/tileset_mapper.py, 2026-11-18). Replaces the March uint16-tile-ID guess.",
            "areas": AREAS,
            "per_level": {f"level{lv:02d}": r for lv, r in rows.items()}})
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
