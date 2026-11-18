#!/usr/bin/env python3
"""Read a Creative Voice (VOC) file from LoL1 and optionally write a WAV.

Used for sound effects (VOC.PAK etc.) and, on the CD edition, for every
speech sample inside the NN.TLK containers (see pak_reader.py).

Layout (ScummVM audio/decoders/voc.h:55-60, voc.cpp:38-62, 255-300):
  +0  char[19] "Creative Voice File" + 0x1A
  +20 uint16 offset of first data block (26)
  +22 uint16 version, +24 uint16 check value
  blocks: uint8 type, uint24 length, payload; type 0 ends the file.
  type 1 = sound data: uint8 rate divisor, uint8 codec (0 = 8-bit unsigned PCM);
  rate = 1000000 / (256 - divisor) (voc.cpp:459-471, 0xA5/0xA6 -> 11025).

  voc_reader.py VOC.PAK:SWING.VOC
  voc_reader.py 01.TLK:000_0.01 --wav out.wav
  voc_reader.py --check        # every VOC in PAKs and TLKs
"""
import argparse, os, struct, sys, wave
from collections import Counter
import lol1lib as L


def rate_of(div):
    if div in (0xA5, 0xA6): return 11025
    if div in (0xD2, 0xD3): return 22050
    return 1000000 // (256 - div)


def parse(blob):
    if blob[:19] != b"Creative Voice File":
        raise ValueError("no VOC signature")
    first, ver, chk = struct.unpack_from("<HHH", blob, 20)
    pos = first; blocks = []; pcm = bytearray(); rate = None
    while pos < len(blob):
        t = blob[pos]
        if t == 0:
            break
        ln = blob[pos + 1] | blob[pos + 2] << 8 | blob[pos + 3] << 16
        body = blob[pos + 4:pos + 4 + ln]
        blocks.append((t, ln))
        if t == 1:
            if body[1] != 0:
                raise ValueError(f"codec {body[1]}")
            rate = rate_of(body[0]); pcm += body[2:]
        elif t == 2:
            pcm += body
        pos += 4 + ln
    return {"header_size": first, "version": hex(ver), "check_ok": chk == ((~ver + 0x1234) & 0xFFFF),
            "blocks": blocks, "rate": rate, "samples": len(pcm)}, bytes(pcm)


def iter_all(data_dir):
    for n in sorted(os.listdir(data_dir)):
        if n.upper().endswith((".PAK", ".TLK")):
            d = open(os.path.join(data_dir, n), "rb").read()
            for name, off, sz in L.pak_entries(d):
                blob = d[off:off + sz]
                if blob[:19] == b"Creative Voice File" or name.upper().endswith(".VOC"):
                    yield n, name, blob


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", nargs="?", help="CONTAINER:MEMBER or a member name")
    ap.add_argument("--wav", help="write 8-bit mono WAV")
    ap.add_argument("--check", action="store_true")
    L.add_data_arg(ap)
    a = ap.parse_args()
    if a.check:
        rates = Counter(); types = Counter(); bad = []; where = Counter()
        for cont, name, blob in iter_all(a.data):
            where[cont.upper().endswith(".TLK")] += 1
            try:
                info, _ = parse(blob)
                rates[info["rate"]] += 1
                for t, _ in info["blocks"]: types[t] += 1
                if not info["check_ok"]: bad.append(f"{cont}:{name}:check")
            except Exception as ex:
                bad.append(f"{cont}:{name}:{ex}")
        print(f"CHECK voc: {where[False]} in PAKs + {where[True]} in TLKs, block types {dict(types)}, "
              f"rates {dict(rates.most_common(6))}, bad={bad[:5] or 'none'} ({len(bad)})")
        return 0 if not bad else 1
    if not a.ref:
        ap.print_help(); return 2
    if ":" in a.ref:
        cont, mem = a.ref.split(":", 1)
        blob = L.find_member(mem, a.data, cont)[1]
    else:
        blob = L.find_member(a.ref, a.data, a.pak)[1]
    info, pcm = parse(blob)
    print(info)
    if a.wav:
        with wave.open(a.wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(1); w.setframerate(info["rate"]); w.writeframes(pcm)
        print("wrote", a.wav)
    return 0


if __name__ == "__main__":
    sys.exit(main())
