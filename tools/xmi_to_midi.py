#!/usr/bin/env python3
"""Convert Lands of Lore 1 XMIDI music (.XMI, also the XMIDI-container .C55
and .PCS files) to standard MIDI files, one per sequence.

XMIDI as read by ScummVM (audio/midiparser_xmidi.cpp, upstream 3b4db303):
  FORM XDIR (INFO: uint16 LE sequence count), then CAT XMID holding one
  FORM XMID per sequence with optional TIMB / RBRN chunks and an EVNT chunk.
  EVNT events (parseNextEvent, :157-320):
    - delay: a run of bytes below 0x80, summed (readVLQ2, :104-110)
    - no running status; every event has its status byte
    - 0x9n note on: note, velocity, then the note's duration as a standard
      MIDI variable-length number; there are no note-off events (:166-186)
    - 0x8n/0xAn/0xBn/0xEn two data bytes, 0xCn/0xDn one (:188-205)
    - 0xF0/0xF7 sysex and 0xFF meta: variable-length size + data (:296-311);
      meta 0x2F ends the sequence; tempo (0x51) is forced to 500000 us
  Timebase: 60 ticks per quarter note at 500000 us per quarter = 120 ticks
  per second (:510-512).

Output: standard MIDI file format 0, division 60, a 500000 us tempo at time
0, note-offs generated from the durations.

  xmi_to_midi.py LOREINTR.XMI --out-dir midi/     # one .mid per sequence
  xmi_to_midi.py LOREINTR.XMI                     # list sequences and event counts
  xmi_to_midi.py --check   # every sequence of every XMI (and C55, PCS) parses to its end-of-track,
                           # and the written MIDI re-reads cleanly with every note closed
"""
from cli_errors import run_cli
import os
import struct

import lol1lib as L


def vlq(b, p):
    v = 0
    while True:
        c = b[p]; p += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, p


def wvlq(v):
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append(0x80 | (v & 0x7F)); v >>= 7
    return bytes(reversed(out))


def sequences(data):
    """Return the EVNT payloads of all sequences, in order (IFF walk)."""
    out = []

    def walk(p, end):
        while p + 8 <= end:
            tag = data[p:p + 4]
            n = struct.unpack_from(">I", data, p + 4)[0]
            body = p + 8
            if tag in (b"FORM", b"CAT "):
                walk(body + 4, min(body + n, end))
            elif tag == b"EVNT":
                out.append(data[body:body + n])
            p = body + n + (n & 1)
    walk(0, len(data))
    return out


def parse_evnt(e):
    """Return (events, stats). events: (abs_time, bytes) in time order, incl. note-offs."""
    t = 0
    p = 0
    ev = []
    stats = {"notes": 0, "controllers": 0, "programs": 0, "meta": 0, "sysex": 0, "end": False}
    seq = 0
    while p < len(e):
        while p < len(e) and e[p] < 0x80:
            t += e[p]; p += 1
        if p >= len(e):
            break
        st = e[p]; p += 1
        hi = st >> 4
        if hi == 0x9:
            note, vel = e[p], e[p + 1]; p += 2
            dur, p = vlq(e, p)
            if vel == 0:
                ev.append((t, seq, bytes([0x80 | (st & 15), note, 0])))
            else:
                ev.append((t, seq, bytes([st, note, vel])))
                ev.append((t + max(dur, 1), -1, bytes([0x80 | (st & 15), note, 0])))
                stats["notes"] += 1
        elif hi in (0x8, 0xA, 0xB, 0xE):
            ev.append((t, seq, bytes([st, e[p], e[p + 1]]))); p += 2
            stats["controllers"] += hi == 0xB
        elif hi in (0xC, 0xD):
            ev.append((t, seq, bytes([st, e[p]]))); p += 1
            stats["programs"] += hi == 0xC
        elif st in (0xF0, 0xF7):
            n, p = vlq(e, p)
            ev.append((t, seq, bytes([st]) + wvlq(n) + e[p:p + n])); p += n
            stats["sysex"] += 1
        elif st == 0xFF:
            typ = e[p]; p += 1
            n, p = vlq(e, p)
            body = e[p:p + n]; p += n
            stats["meta"] += 1
            if typ == 0x2F:
                stats["end"] = True
                stats["end_time"] = t
                break
            if typ == 0x51:
                continue                      # tempo forced to 500000 below
            ev.append((t, seq, bytes([0xFF, typ]) + wvlq(n) + body))
        else:
            raise ValueError(f"unknown status 0x{st:02X} at EVNT+{p - 1}")
        seq += 1
    stats["consumed"] = p
    stats["length"] = len(e)
    # note-offs (seq -1) go before other events at the same tick
    ev.sort(key=lambda x: (x[0], x[1] != -1, x[1]))
    end = max([stats.get("end_time", 0)] + [x[0] for x in ev])
    return ev, end, stats


def to_smf(ev, end, division=60):
    trk = bytearray(b"\x00\xff\x51\x03\x07\xa1\x20")      # tempo 500000
    last = 0
    for t, _, data in ev:
        trk += wvlq(t - last) + data
        last = t
    trk += wvlq(end - last) + b"\xff\x2f\x00"
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, division) + b"MTrk" + struct.pack(">I", len(trk)) + bytes(trk)


def verify_smf(smf, division=60):
    """Strict re-read of a written file (separate from the writer): header,
    track length, every event parses, track ends exactly at its end-of-track,
    and every note-on has a matching note-off. Returns (ok, notes)."""
    if smf[:4] != b"MThd" or struct.unpack_from(">IHHH", smf, 4) != (6, 0, 1, division) or smf[14:18] != b"MTrk":
        return False, 0
    n = struct.unpack_from(">I", smf, 18)[0]
    t = smf[22:22 + n]
    if len(t) != n:
        return False, 0
    p, on, notes = 0, {}, 0
    while p < n:
        _, p = vlq(t, p)
        st = t[p]; p += 1
        if st == 0xFF:
            typ = t[p]; ln, p = vlq(t, p + 1); p += ln
            if typ == 0x2F:
                return p == n and not any(on.values()), notes
        elif st in (0xF0, 0xF7):
            ln, p = vlq(t, p); p += ln
        elif st >> 4 in (0x8, 0x9):
            key = (st & 15, t[p])
            if st >> 4 == 0x9 and t[p + 1]:
                on[key] = on.get(key, 0) + 1; notes += 1
            elif on.get(key):
                on[key] -= 1
            p += 2
        elif st >> 4 in (0xA, 0xB, 0xE):
            p += 2
        elif st >> 4 in (0xC, 0xD):
            p += 1
        else:
            return False, notes
    return False, notes


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument("name", nargs="?", help="music member, e.g. LOREINTR.XMI")
    ap.add_argument("--out-dir", help="write NAME_NN.mid per sequence here")
    a = ap.parse_args()
    if a.check:
        res = {}
        bad = []
        for ext in (".XMI", ".C55", ".PCS"):
            files = seqs = notes = 0
            for pak, name, blob in L.find_all(ext, a.data):
                files += 1
                for i, e in enumerate(sequences(blob)):
                    seqs += 1
                    try:
                        ev, end, st = parse_evnt(e)
                        notes += st["notes"]
                        smf = to_smf(ev, end)
                        ok, n2 = verify_smf(smf)
                        if not st["end"] or not ok or n2 != st["notes"]:
                            bad.append(f"{name}#{i}")
                    except Exception as ex:
                        bad.append(f"{name}#{i}:{ex}")
            res[ext] = f"{files} files/{seqs} sequences/{notes} notes"
        print(f"CHECK xmi: {res['.XMI']} (XMI), {res['.C55']} (C55), {res['.PCS']} (PCS); "
              f"every sequence parses to its end-of-track, converts, and re-reads as a valid MIDI file with all notes closed: bad={bad[:5] or 'none'} ({len(bad)})")
        return 0 if not bad else 1
    if not a.name:
        ap.print_help(); return 2
    pak, blob = L.find_member(a.name, a.data, a.pak)
    stem = a.name.rsplit(".", 1)[0]
    for i, e in enumerate(sequences(blob)):
        ev, end, st = parse_evnt(e)
        secs = end / 120
        print(f"{stem} #{i:02d}: {st['notes']} notes, {st['controllers']} controller, {st['programs']} program, "
              f"{st['meta']} meta, {st['sysex']} sysex events; {secs:.1f} s; end-of-track: {st['end']}")
        if a.out_dir:
            os.makedirs(a.out_dir, exist_ok=True)
            with open(os.path.join(a.out_dir, f"{stem}_{i:02d}.mid"), "wb") as f:
                f.write(to_smf(ev, end))
    if a.out_dir:
        print("wrote", a.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
