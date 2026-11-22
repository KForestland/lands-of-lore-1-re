#!/usr/bin/env python3
"""Read LoL1 player saves and print their fields.

Reads three kinds of file (layout: docs/savegame_format.md, docs/unknowns/
17_native_save_fields.md, docs/unknowns/18_native_records.md):

  original save   _SAVEnnn.DAT written by the DOS game (CD "CD04" or floppy ".13")
  level file      _LEVELn.TMP written by the DOS game for a visited level
  ScummVM save    lol-cd.nnn / lol-floppy.nnn etc. (gzip, "WWSV" header)

The original files are little-endian; ScummVM's are big-endian (except the
gzip wrapper). Field names follow the documentation.

  save_reader.py FILE [--full]          # summary (party, position, money, flags set, levels)
  save_reader.py FILE --json out.json   # every field
  save_reader.py --check [--data DIR] [--saves DIR]
      parses every _SAVE*.DAT and _LEVEL*.TMP in the game folder (and its parent)
      and every ScummVM LoL save in --saves (only when given),
      and checks that each file ends exactly where the layout says.
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse
import glob
import gzip
import json
import os
from pathlib import Path
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lol1lib as L

# ---------------------------------------------------------------------------
# records


def character(b, o, scummvm):
    """130-byte native / 126-byte ScummVM character record (executable_tables.md)."""
    e = ">" if scummvm else "<"
    r = {"flags": struct.unpack_from(e + "H", b, o)[0],
         "name": b[o + 2:o + 13].split(b"\0")[0].decode("latin-1"),
         "race_class_sex": b[o + 13],
         "id": struct.unpack_from(e + "h", b, o + 14)[0],
         "face": b[o + 16], "temp_face": b[o + 17], "scream_sound": b[o + 18]}
    p = o + 19
    if not scummvm:
        p += 4                                   # far pointer to the modifier row
    w = lambda k, fmt="H": struct.unpack_from(e + str(k) + fmt, b, p_[0])
    p_ = [p]

    def take(n, fmt):
        vals = struct.unpack_from(e + str(n) + fmt, b, p_[0])
        p_[0] += struct.calcsize(e + str(n) + fmt)
        return list(vals) if n > 1 else vals[0]
    r["item_might"] = take(8, "H")
    r["protection_against"] = take(8, "H")
    r["item_protection"] = take(1, "H")
    r["hp"], r["hp_max"], r["mp"], r["mp_max"] = take(1, "h"), take(1, "H"), take(1, "h"), take(1, "H")
    r["field_41"] = take(1, "B")
    r["damage_suffered"], r["weapon_hit"] = take(1, "H"), take(1, "H")
    r["total_might_mod"], r["total_protection_mod"] = take(1, "H"), take(1, "H")
    r["might_mod"], r["protection_mod"] = take(1, "H"), take(1, "H")
    r["next_anim_update"] = take(1, "h")
    r["items"] = take(11, "H")
    r["skill_levels"] = take(3, "B")
    r["skill_modifiers"] = take(3, "b")
    r["experience"] = take(3, "i")
    r["update_events"] = take(5, "B")
    r["update_delays"] = take(5, "B")
    return r, p_[0] - o


def item(b, o, e):
    f = struct.unpack_from(e + "HHBHHHbHH", b, o)
    return dict(zip(("next_assigned", "next_draw", "flying_height", "block", "x", "y",
                     "level", "property", "shape_and_flags"), f))


def item_rows(b, offset, endian):
    """Keep the table index, which is the handle stored on a character."""
    for handle in range(400):
        row = item(b, offset + 16 * handle, endian)
        if not row["shape_and_flags"] & 0x8000:
            yield handle, row


def monster(b, o, e, native):
    f = list(struct.unpack_from(e + "HHBHHHbHHBbbBBbBBBHHhBB", b, o))
    keys = ("next_assigned", "next_draw", "flying_height", "block", "x", "y", "shift_step",
            "dest_x", "dest_y", "dest_direction", "hit_offset_x", "hit_offset_y", "subframe",
            "mode", "fight_tick", "id", "direction", "facing", "flags", "damage_received",
            "hp", "speed_tick", "type")
    r = dict(zip(keys, f))
    p = o + 33 + (4 if native else 0)
    r["ranged_attacks"], r["ranged_weapon"], r["ranged_tick"] = b[p], b[p + 1], struct.unpack_from("b", b, p + 2)[0]
    r["assigned_item"] = struct.unpack_from(e + "H", b, p + 3)[0]
    r["equipment_shapes"] = list(b[p + 5:p + 9])
    return r


def flying(b, o, e):
    f = struct.unpack_from(e + "BBHhHHBBBbBBB", b, o)
    return dict(zip(("enabled", "type", "attacker", "item", "x", "y", "flying_height",
                     "direction", "distance", "field_D", "c", "flags", "wall_flags"), f))


def level_state(walls_flags, monsters_raw, flying_raw, e, native):
    return {"changed_walls": sum(1 for x in walls_flags[:4096] if x),
            "block_flags_set": sum(1 for x in walls_flags[4096:5120] if x),
            "monsters": [m for m in (monster(monsters_raw, i * (46 if native else 42), e, native)
                                     for i in range(30)) if m["mode"] < 16],
            "flying_objects": [f for f in (flying(flying_raw, i * 17, e) for i in range(8)) if f["enabled"]]}


# ---------------------------------------------------------------------------
# global state (savegame_format.md, "Global state")


def global_state(b, o, scummvm):
    e = ">" if scummvm else "<"
    g = {}
    g["block"], g["x"], g["y"], g["update_flags"] = struct.unpack_from(e + "4H", b, o)
    g["script_direction"], g["selected_spell"] = b[o + 8], b[o + 9]
    s = 10 if scummvm else 12
    if not scummvm:
        opt = struct.unpack_from("<H", b, o + 10)[0]
        g["options"] = {"word": opt, "difficulty": (opt & 0x30) >> 4, "effects": bool(opt & 1),
                        "music": bool(opt & 2), "floating_cursor": bool(opt & 4), "smooth_scrolling": bool(opt & 8)}
    g["scene_default_update"], g["compass_broken"], g["drain_magic"] = b[o + s], b[o + s + 1], b[o + s + 2]
    g["facing"], g["compass_direction"] = struct.unpack_from(e + "2H", b, o + s + 3)
    g["selected_character"] = struct.unpack_from("b", b, o + s + 7)[0]
    lv = o + (18 if scummvm else 21)
    g["level"] = b[lv]
    g["inventory"] = list(struct.unpack_from(e + "48h", b, lv + 1))
    p = lv + 1 + 96
    g["inventory_scroll"], g["hand_item"], g["last_mouse_region"] = struct.unpack_from(e + "3h", b, p)
    p += 6
    if scummvm:
        n = struct.unpack_from(">I", b, p)[0]; p += 4
        flags = b[p:p + n]; p += n
        # flag n is bit (n & 7) of byte n >> 3 (KyraEngine_v1::queryGameFlag, engines/kyra/engine/kyra_v1.cpp:522-525)
        g["flags_set"] = [i * 8 + k for i, v in enumerate(flags) for k in range(8) if v & (1 << k)]
    else:
        words = struct.unpack_from("<100H", b, p); p += 200
        g["flags_set"] = [i * 16 + k for i, v in enumerate(words) for k in range(16) if v & (1 << k)]
    g["script_globals"] = list(struct.unpack_from(e + "24h", b, p))
    p += 200 if not scummvm else 48
    g["brightness"], g["lamp_oil"] = b[p], b[p + 1]
    g["lamp_effect"] = struct.unpack_from("b", b, p + 2)[0]
    p += 3 if scummvm else 4
    g["money"] = struct.unpack_from(e + "H", b, p)[0]; p += 2
    g["secondary_globals"] = list(struct.unpack_from(e + "8h", b, p)); p += 16
    g["spells_available"] = list(b[p:p + 7]); p += 7
    g["level_mask"] = struct.unpack_from(e + "I", b, p)[0]; p += 4
    return g, p


# ---------------------------------------------------------------------------
# file kinds


def read_original_save(b, *, include_handles=False):
    tag = b[60:65]
    cd = tag[:4] == b"CD04"
    out = {"kind": "original save", "edition": "CD" if cd else "floppy",
           "description": b[:60].split(b"\0")[0].decode("latin-1"), "tag": tag.split(b"\0")[0].decode("latin-1")}
    p = 65
    if cd:
        out["version_text"] = b[65:76].split(b"\0")[0].decode("latin-1"); p = 76
    out["characters"] = []
    for i in range(4):
        c, n = character(b, p, False); out["characters"].append(c); p += 130
    g, end = global_state(b, p, False)
    p += 563 if cd else 557
    if cd:
        x = b[p - 6:p]
        g["cd_options"] = {"language": x[0], "text": x[1], "talk_volume": x[2], "sfx_volume": x[3],
                           "music_volume": x[4], "byte_0x232": x[5]}
    out["state"] = g
    rows = dict(item_rows(b, p, "<"))
    out["items"] = list(rows.values())
    if include_handles:
        out["item_handles"] = rows
    p += 400 * 16
    out["levels"] = {}
    for lv in range(30):
        if g["level_mask"] & (1 << lv):
            ln = struct.unpack_from("<I", b, p)[0]
            out["levels"][lv + 1] = read_level_file(b[p + 4:p + 4 + ln])
        p += 2500
    out["end"] = p
    out["size_ok"] = p == len(b)
    return out


def read_level_file(b):
    """_LEVELn.TMP (also the payload of a used slot in an original save)."""
    c = struct.unpack_from("<H", b, 0)[0]
    wf = L.decode_frame4(b[2:2 + c], 5120)
    diff = struct.unpack_from("<H", b, 2 + c)[0]
    mo = 4 + c
    st = level_state(wf, b[mo:mo + 30 * 46], b[mo + 30 * 46:mo + 30 * 46 + 8 * 17], "<", True)
    st.update({"kind": "level file", "compressed_bytes": c, "decoded_bytes": len(wf), "difficulty": diff,
               "end": mo + 30 * 46 + 8 * 17})
    st["size_ok"] = st["end"] == len(b) and len(wf) == 5120
    return st


def read_scummvm(raw, *, include_handles=False):
    b = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    if b[:4] != b"WWSV":
        raise ValueError("not a ScummVM Westwood save")
    out = {"kind": "ScummVM save", "version": struct.unpack_from(">I", b, 5)[0]}
    p = 9
    e = b.index(b"\0", p)
    out["description"] = b[p:e].decode("utf-8", "replace"); p = e + 1
    fl = struct.unpack_from(">I", b, p)[0]; p += 4
    out["edition"] = "floppy" if fl & 1 else "CD" if fl & 2 else "PC-98/FM Towns" if fl & 4 else "?"
    if b[p:p + 4] in (b"THMB", b"BMHT"):
        p += struct.unpack_from(">I", b, p + 4)[0]
    if out["version"] >= 21:
        t = struct.unpack_from(">7i", b, p); p += 28
        out["saved_at"] = f"{t[5]:04d}-{t[4] + 1:02d}-{t[3]:02d} {t[2]:02d}:{t[1]:02d}"
        out["play_seconds"] = struct.unpack_from(">I", b, p)[0]; p += 4
    out["characters"] = []
    for i in range(4):
        c, n = character(b, p, True); out["characters"].append(c); p += 126
    g, p = global_state(b, p, True)
    out["state"] = g
    rows = dict(item_rows(b, p, ">"))
    out["items"] = list(rows.values())
    if include_handles:
        out["item_handles"] = rows
    p += 400 * 16
    out["levels"] = {}
    for lv in range(29):
        if g["level_mask"] & (1 << lv):
            walls_flags = b[p:p + 5120]
            st = level_state(walls_flags, b[p + 5120:p + 5120 + 30 * 42], b[p + 5120 + 1260:p + 5120 + 1260 + 136], ">", False)
            st["difficulty"] = b[p + 6516]
            out["levels"][lv + 1] = st
            p += 6517
    out["end"] = p
    out["size_ok"] = p == len(b)
    return out


def read_any(path, *, include_handles=False):
    raw = Path(path).read_bytes()
    if raw[:2] == b"\x1f\x8b" or raw[:4] == b"WWSV":
        return read_scummvm(raw, include_handles=include_handles)
    if len(raw) > 65 and (raw[60:64] == b"CD04" or raw[60:63] == b".13"):
        return read_original_save(raw, include_handles=include_handles)
    return read_level_file(raw)


def summary(r):
    lines = [f"{r['kind']}" + (f", {r['edition']}" if "edition" in r else "") +
             (f", version {r['version']}" if "version" in r else "") +
             (f": \"{r['description']}\"" if r.get("description") else "") +
             f"; ends at {r['end']} as the layout predicts: {r['size_ok']}"]
    if "characters" in r:
        for c in r["characters"]:
            if c["name"]:
                lines.append(f"  {c['name']:<10} HP {c['hp']}/{c['hp_max']}  MP {c['mp']}/{c['mp_max']}  "
                             f"skills {c['skill_levels']}  XP {c['experience']}")
        g = r["state"]
        lines.append(f"  level {g['level']}, block {g['block']} (x {g['block'] % 32}, y {g['block'] // 32}), "
                     f"facing {g['facing']}, money {g['money']}, {len(g['flags_set'])} game flags set, "
                     f"levels stored {sorted(r['levels'])}, {len(r['items'])} items in use")
        if "options" in g:
            lines.append(f"  options: {g['options']}")
    else:
        lines.append(f"  difficulty {r['difficulty']}, {r['changed_walls']} changed wall bytes, "
                     f"{len(r['monsters'])} monster slots in use, {len(r['flying_objects'])} flying objects")
    return "\n".join(lines)


def default_save_dir():
    return os.path.join(os.path.expanduser("~"), ".local", "share", "scummvm", "saves")


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--out", "--json", help="write every field as JSON")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--data", default=L.DEFAULT_DATA, help="game DATA folder searched for _SAVE*.DAT and _LEVEL*.TMP (with --check)")
    ap.add_argument("--saves", default=None,
                    help=f"a ScummVM save folder to include in --check (not read unless given; on Linux usually {default_save_dir()})")
    a = ap.parse_args()
    if a.check:
        files = []
        for d in filter(None, [a.data, os.path.dirname(os.path.normpath(a.data)) if a.data else None]):
            for pat in ("_SAVE*.DAT", "_LEVEL*.TMP", "_save*.dat", "_level*.tmp"):
                files += glob.glob(os.path.join(d, pat))
        files = sorted(set(files))
        svm = sorted(glob.glob(os.path.join(a.saves, "lol-*.[0-9][0-9][0-9]"))) if a.saves and os.path.isdir(a.saves) else []
        kinds, bad = {}, []
        for f in files + svm:
            try:
                r = read_any(f)
                kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
                if not r["size_ok"]:
                    bad.append(os.path.basename(f))
            except Exception as ex:
                bad.append(f"{os.path.basename(f)}:{type(ex).__name__}")
        # no original _SAVEnnn.DAT has been available; check the reader on empty files of the
        # exact sizes the layout gives (CD 0x1427F, floppy 0x1426E) so its section walk is exercised
        for tag, size in ((b"CD04\0", 0x1427F), (b".13\0_", 0x1426E)):
            blank = bytearray(size); blank[60:65] = tag
            for i in range(400):                      # mark every item slot free
                blank[(76 if tag[:2] == b"CD" else 65) + 520 + (563 if tag[:2] == b"CD" else 557) + i * 16 + 15] = 0x80
            if not read_original_save(bytes(blank))["size_ok"]:
                bad.append(f"layout self-test {tag[:4].decode()}")
        found = ", ".join(f"{v} {k}{'s' if v != 1 else ''}" for k, v in sorted(kinds.items())) or "no save files found"
        print(f"CHECK save: {found}; original-save layout self-test (CD and floppy sizes); "
              f"every file ends where the layout predicts: bad={bad or 'none'}")
        return 0 if not bad else 1
    if not a.file:
        ap.print_help(); return 2
    try:
        r = read_any(a.file)
    except (EOFError, ValueError, IndexError, struct.error) as error:
        raise ValueError("Choose a complete LoL1 save or a temporary level file.") from error
    print(summary(r))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(r, f, indent=1)
        print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
