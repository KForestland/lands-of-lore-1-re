#!/usr/bin/env python3
"""Print the static tables inside the LoL1 game program (MAIN.EXE, and on the CD MAINW.EXE).

Every table, offset and field name comes from docs/executable_tables.md,
docs/game_rules.md, docs/unknowns/06_tim_opcodes.md and docs/unknowns/07_native_rules.md.
Offsets are file offsets in the named program. A field the pages mark UNCONFIRMED
is printed as a raw value with its record offset, not under a name.

The programs are found by size: CD DATA/HARDRIVE/MAIN.EXE (0x57240 bytes) and
MAINW.EXE (0x56190), floppy MAIN.EXE (0x5B470) in the game folder itself.

  exe_tables.py                       # every table of every program found
  exe_tables.py --table spells        # one table (names: see --list)
  exe_tables.py --image floppy        # one program: cd, cdw (CD MAINW.EXE) or floppy
  exe_tables.py --check               # re-read the tables against the values the pages give

Prints to stdout only; writes nothing.
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse, os, struct
import lol1lib as L

IMAGES = {  # size -> (key, label); docs/executable_tables.md "Locating the executables"
    0x57240: ("cd", "CD MAIN.EXE"),
    0x56190: ("cdw", "CD MAINW.EXE"),
    0x5B470: ("floppy", "floppy MAIN.EXE"),
}

# table -> {image key: file offset}; None = the page gives no offset for that program
OFFSETS = {
    "characters":   {"cd": 0x29D60, "cdw": 0x29820, "floppy": 0x2B470},
    "char_mods":    {"cd": 0x2B4D2, "cdw": 0x2AF92, "floppy": 0x2CD72},
    "equip_layout": {"cd": 0x2B47A, "cdw": 0x2AF3A, "floppy": 0x2CD1A},
    "spells":       {"cd": 0x2B5E0, "cdw": 0x2B0A0, "floppy": 0x2CE80},
    "xp":           {"cd": 0x2B830, "cdw": 0x2B2F0, "floppy": 0x324F0},
    "difficulty":   {"cd": 0x2B85C, "cdw": 0x2B31C, "floppy": 0x3251C},
    "difficulty4":  {"cd": 0x2B86E, "cdw": 0x2B32E},
    "prices":       {"cd": 0x2F8C0, "cdw": 0x2F380},
    "timers":       {"cd": 0x33D68, "floppy": 0x3CFF0},
    "mode_flags":   {"cd": 0x33F53, "floppy": 0x3D1DD},
    "steps":        {"cd": 0x33F0A},
    "spell_effects": {"cd": 0x32EF4, "floppy": 0x39604},
    "wall_click":   {"cd": 0x342FC, "floppy": 0x3D558},
    "tim_commands": {"cd": 0x3389C, "floppy": 0x39768},
    "tim_nested":   {"cd": 0x33918, "floppy": 0x397E0},
}
TITLES = {
    "characters": "English character defaults, 9 x 130 bytes (executable_tables.md)",
    "char_mods": "Character modifier rows, 5 x 9 u16 (executable_tables.md)",
    "equip_layout": "Character equipment display layout, 4 x 22 bytes = 11 coordinate pairs (executable_tables.md)",
    "spells": "Spell properties, 17 x 28 bytes (executable_tables.md)",
    "xp": "Experience thresholds, 11 x u32 (executable_tables.md)",
    "difficulty": "Monster difficulty modifiers 1-3, easy/normal/hard, 256 = 1.0 (executable_tables.md)",
    "difficulty4": "Monster difficulty modifier 4, easy/normal/hard (executable_tables.md, CD only)",
    "prices": "Item price thresholds, 46 x u16 up to the final zero (executable_tables.md, CD only)",
    "timers": "Timer array, 12 x 19 bytes (unknowns/07_native_rules.md)",
    "mode_flags": "Monster mode flags 0-14, one byte each (unknowns/07_native_rules.md)",
    "steps": "Movement step words (game_rules.md: steps add 32 along each axis); count and layout not on the page: 16 raw words",
    "spell_effects": "Spell effect far pointers, 17 entries (unknowns/07_native_rules.md)",
    "wall_click": "Wall special-type click table, 7 far pointers, slot 0 null (unknowns/07_native_rules.md)",
    "tim_commands": "In-game TIM command far pointers up to the nested table; slot names from the ScummVM LoL table (unknowns/06_tim_opcodes.md)",
    "tim_nested": "In-game TIM nested (0x19) far pointers, 17 registered; names from the ScummVM list (unknowns/06_tim_opcodes.md)",
}

# Character default record, docs/executable_tables.md "Character default record".
CHAR_FIELDS = [  # (offset, format, name)
    (0x00, "<H", "flags"), (0x0D, "B", "race/class/sex"), (0x0E, "<h", "character ID"),
    (0x10, "B", "current face"), (0x11, "B", "temporary face"), (0x12, "B", "scream sound"),
    (0x17, "<8H", "item might"), (0x27, "<8H", "protection per category"), (0x37, "<H", "item protection"),
    (0x39, "<h", "current HP"), (0x3B, "<H", "max HP"), (0x3D, "<h", "current MP"), (0x3F, "<H", "max MP"),
    (0x41, "B", "shape selector"), (0x42, "<H", "damage suffered"), (0x44, "<H", "weapon hit"),
    (0x46, "<H", "total might multiplier"), (0x48, "<H", "total protection multiplier"),
    (0x4A, "<H", "base might"), (0x4C, "<H", "base protection"), (0x4E, "<h", "next animation countdown"),
    (0x50, "<11H", "default equipment types"), (0x66, "<3B", "skill levels"), (0x69, "<3b", "skill modifiers"),
    (0x6C, "<3i", "experience"), (0x78, "<5B", "update events"), (0x7D, "<5B", "update delays"),
]
# Timer entry, unknowns/07_native_rules.md "Lamp, regeneration and the clock".
TIMER_WORK = ["doors", "even monster slots", "odd monster slots", "character events", "flying objects",
              "level script timer", "level script timer", "level script timer", "regeneration",
              "portrait animation", "lamp oil", "text clearing"]

# Values the pages state, re-read by --check.
DOC = {
    "char_rows": [0, 0, 0, 1, 0, 0, 1, 2, 4],
    "xp": [0, 500, 1500, 5000, 25000, 50000, 80000, 120000, 180000, 270000, 2147483647],
    "difficulty": {"cd": [102, 256, 384, 256, 256, 192, 320, 256, 128],
                   "cdw": [102, 256, 384, 256, 256, 192, 320, 256, 128],
                   "floppy": [192, 256, 384, 256, 256, 192, 320, 256, 128]},
    "difficulty4": [128, 256, 256],
    "timer_periods": [15, 6, 6, 15, 1, 0, 0, 0, 1200, 10, 360, 360],
    "timer_callbacks": {"cd": [0xF40A, 0xF3CA, 0xF3CA, 0xF503, 0xF7CB, 0xF832, 0xF832, 0xF832, 0xF848, 0xF94A,
                               0xF9DE, 0xFD0B],
                        "floppy": [0x13DF8, 0x13DB8, 0x13DB8, 0x13EF1, 0x141B9, 0x14220, 0x14220, 0x14220,
                                   0x14236, 0x14338, 0x143C6, 0x146D4]},
    "timer_clock": {"cd": 0x3858, "floppy": 0x6F14},
    "mode_flags": [1, 0, 1, 3, 3, 0, 0, 3, 4, 1, 0, 0, 4, 0, 0],
    "spell_null": [7, 10, 11, 13, 14, 15],
    "wall_seg": {"cd": 0x13E8, "floppy": 0x174B},
    "tim_routines": {"cd": {0x07: 0x94B9, 0x0A: 0x94D1, 0x0B: 0x94D9, 0x0F: 0x9505, 0x12: 0x9522, 0x13: 0x9536,
                            0x1A: 0, 0x1B: 0},
                     "floppy": {0x07: 0x96A0, 0x0A: 0x96B8, 0x0B: 0x96E7, 0x0F: 0x9718, 0x12: 0x9735,
                                0x13: 0x9749, 0x1A: 0, 0x1B: 0}},
    "tim_nested": {"cd": {0x02: 0x9837, 0x03: 0x983F, 0x07: 0x99C6, 0x0D: 0x9AD9},
                   "floppy": {0x02: 0x9A02, 0x03: 0x9A0A, 0x07: 0x9B8D, 0x0D: 0x9C64}},
}


def header_size(exe):
    """MZ header size in bytes: u16 at +0x08 times 16."""
    return struct.unpack_from("<H", exe, 8)[0] * 16


def far(exe, off):
    """(offset, segment) of the DOS far pointer at off."""
    return struct.unpack_from("<HH", exe, off)


def resolve(exe, off):
    """File offset a resident far pointer points to (header + segment x 16 + offset); 0 for null."""
    o, s = far(exe, off)
    return 0 if (o, s) == (0, 0) else header_size(exe) + s * 16 + o


def characters(exe, base):
    out = []
    for i in range(9):
        r = exe[base + i * 0x82:base + (i + 1) * 0x82]
        rec = {"name": r[2:13].split(b"\0")[0].decode("latin-1"), "modifier pointer": far(r, 0x13)}
        for off, fmt, name in CHAR_FIELDS:
            v = struct.unpack_from(fmt, r, off)
            rec[name] = v[0] if len(v) == 1 else list(v)
        out.append(rec)
    return out


def char_row(exe, img, rec):
    """Modifier row (0-4) a character's far pointer resolves to, or None."""
    o, s = rec["modifier pointer"]
    target = header_size(exe) + s * 16 + o
    d = target - OFFSETS["char_mods"][img]
    return d // 18 if d >= 0 and d % 18 == 0 and d // 18 < 5 else None


def words(exe, off, n, fmt="H"):
    return list(struct.unpack_from(f"<{n}{fmt}", exe, off))


def spells(exe, base):
    rows = []
    for i in range(17):
        w = words(exe, base + i * 28, 14)
        rows.append({"name id": w[0], "MP": w[1:5], "raw+0A": w[5], "raw+0C": w[6], "HP": w[7:11],
                     "raw+16": w[11], "raw+18": w[12], "property": w[13]})
    return rows


def timers(exe, base):
    out = []
    for i in range(12):
        e = base + i * 19
        out.append({"callback": far(exe, e), "callback file": resolve(exe, e),
                    "period": struct.unpack_from("<I", exe, e + 4)[0],
                    "initial state": struct.unpack_from("<I", exe, e + 8)[0],
                    "argument": struct.unpack_from("<H", exe, e + 12)[0],
                    "clock": far(exe, e + 14), "enable": exe[e + 18]})
    return out


def find_images(data_dir):
    """[(key, label, path, bytes)] for every known program under the game folder."""
    found = []
    for sub in ("HARDRIVE", ""):
        for name in ("MAIN.EXE", "MAINW.EXE"):
            p = os.path.join(data_dir, sub, name) if sub else os.path.join(data_dir, name)
            if os.path.isfile(p):
                with open(p, "rb") as f:
                    b = f.read()
                if len(b) in IMAGES and b[:2] == b"MZ":
                    key, label = IMAGES[len(b)]
                    if key not in [f[0] for f in found]:
                        found.append((key, label, p, b))
    return found


def spell_names(data_dir, lang):
    """English (or --lang) spell names: name ids with bit 0x4000 index LANDS.<lang> (docs/formats/text.md)."""
    try:
        import decode_dialogue as T
        strings = T.file_strings(L.find_member("LANDS." + lang, data_dir)[1])
        return lambda sid: T.decode_raw(strings[sid & 0x3FFF]).strip() \
            if sid & 0x4000 and (sid & 0x3FFF) < len(strings) else ""
    except Exception:
        return lambda sid: ""


def print_table(t, img, exe, off, name_of):
    import parse_tim as P
    print(f"## {TITLES[t]}: +0x{off:X}")
    if t == "characters":
        for i, r in enumerate(characters(exe, off)):
            row = char_row(exe, img, r)
            o, s = r["modifier pointer"]
            print(f"{i} {r['name']}: modifier pointer {s:04X}:{o:04X} -> row {row}; "
                  + "; ".join(f"{n} {r[n]}" for _, _, n in CHAR_FIELDS if n != "flags")
                  + f"; flags 0x{r['flags']:04X}")
    elif t == "char_mods":
        for i in range(5):
            print(f"row {i} (+0x{off + i * 18:X}): modifiers 0-8 = {words(exe, off + i * 18, 9)}")
    elif t == "equip_layout":
        for i in range(4):
            b = exe[off + i * 22:off + i * 22 + 22]
            print(f"layout {i}: " + " ".join(f"({b[j]},{b[j + 1]})" for j in range(0, 22, 2)))
    elif t == "spells":
        for i, r in enumerate(spells(exe, off)):
            nm = name_of(r["name id"])
            print(f"{i:2d} name id 0x{r['name id']:04X}{' ' + repr(nm) if nm else ''}: MP {r['MP']} HP {r['HP']} "
                  f"property 0x{r['property']:04X} (bit 8 forward-wall test {r['property'] >> 8 & 1}, "
                  f"effect slot {r['property'] & 0xFF}); UNCONFIRMED words +0A={r['raw+0A']} +0C={r['raw+0C']} "
                  f"+16={r['raw+16']} +18={r['raw+18']}")
    elif t == "xp":
        print("levels 0-10:", words(exe, off, 11, "I"))
    elif t == "difficulty":
        for i in range(3):
            print(f"row {i + 1} (+0x{off + i * 6:X}): easy/normal/hard = {words(exe, off + i * 6, 3)}")
    elif t == "difficulty4":
        print(f"row 4: easy/normal/hard = {words(exe, off, 3)}")
    elif t == "prices":
        print(words(exe, off, 46))
    elif t == "timers":
        for i, e in enumerate(timers(exe, off)):
            o, s = e["callback"]
            co, cs = e["clock"]
            print(f"slot {i:2d} {TIMER_WORK[i]}: callback {s:04X}:{o:04X} (file 0x{e['callback file']:X}), "
                  f"period {e['period']}, initial state {e['initial state']}, argument {e['argument']}, "
                  f"clock {cs:04X}:{co:04X}, enable {e['enable']}")
    elif t == "mode_flags":
        print("modes 0-14:", list(exe[off:off + 15]))
    elif t == "steps":
        print("raw signed words:", words(exe, off, 16, "h"))
    elif t in ("spell_effects", "wall_click", "tim_commands", "tim_nested"):
        n = {"spell_effects": 17, "wall_click": 7, "tim_nested": 17,
             "tim_commands": (OFFSETS["tim_nested"][img] - off) // 4}[t]
        for i in range(n):
            o, s = far(exe, off + i * 4)
            label = ""
            if t == "tim_commands":
                label = " " + P.TIM_COMMANDS.get(i, "")
            elif t == "tim_nested":
                label = " " + P.TIM_NESTED["in-game"][i]
            tgt = resolve(exe, off + i * 4)
            where = "null" if not tgt else (f"file 0x{tgt:X}" if t != "spell_effects" else "overlay stub")
            print(f"0x{i:02X}{label}: {s:04X}:{o:04X} {where}")


def check(found):
    msgs, bad = [], []

    def need(cond, what):
        if not cond:
            bad.append(what)
    by = {k: b for k, _, _, b in found}
    for img, label, _, exe in found:
        o = OFFSETS
        chars = characters(exe, o["characters"][img])
        need([char_row(exe, img, r) for r in chars] == DOC["char_rows"], f"{img}:character rows")
        need(all(r["name"] for r in chars), f"{img}:character names")
        need(words(exe, o["char_mods"][img] + 54, 9) == words(exe, o["char_mods"][img], 9), f"{img}:row 3 = row 0")
        sp = spells(exe, o["spells"][img])
        need(all(any(words(exe, o["spells"][img] + i * 28, 14)) for i in range(10)), f"{img}:spell rows 0-9")
        need(not any(exe[o["spells"][img] + 280:o["spells"][img] + 476]), f"{img}:spell rows 10-16 zero")
        need(sp[0]["MP"] == [5, 10, 15, 25] and sp[7]["MP"] == [3, 6, 12, 24], f"{img}:spell MP")
        need(all(r["HP"] == [0, 0, 0, 0] and r["raw+16"] == 0 and r["raw+18"] == 0 for r in sp), f"{img}:spell zeros")
        need([r["raw+0A"] for r in sp] == [0] * 9 + [15] + [0] * 7 and not any(r["raw+0C"] for r in sp),
             f"{img}:spell +0A/+0C")
        need(sp[9]["property"] & 0xFF == 8 and sp[7]["property"] == 0x107, f"{img}:spell property words")
        need(words(exe, o["xp"][img], 11, "I") == DOC["xp"], f"{img}:xp")
        need(words(exe, o["difficulty"][img], 9) == DOC["difficulty"][img], f"{img}:difficulty")
        if img in o["difficulty4"]:
            need(words(exe, o["difficulty4"][img], 3) == DOC["difficulty4"], f"{img}:difficulty4")
            pr = words(exe, o["prices"][img], 46)
            need(pr[-1] == 0 and 0 not in pr[:-1], f"{img}:prices")
        else:  # floppy: no word run 128, 256, 256 and no six consecutive price words
            need(struct.pack("<3H", 128, 256, 256) not in exe, "floppy:128,256,256 run")
            if "cd" in by:
                pr = words(by["cd"], o["prices"]["cd"], 46)
                need(not any(struct.pack("<6H", *pr[i:i + 6]) in exe for i in range(41)), "floppy:price run")
        if img in o["timers"]:
            tm = timers(exe, o["timers"][img])
            need([e["period"] for e in tm] == DOC["timer_periods"], f"{img}:timer periods")
            need([e["callback file"] for e in tm] == DOC["timer_callbacks"][img], f"{img}:timer callbacks")
            need([e["clock"][0] for e in tm[:11]] == [DOC["timer_clock"][img]] * 11, f"{img}:timer clock")
            need([e["enable"] for e in tm] == [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0], f"{img}:timer enable")
            need([(e["initial state"], e["argument"]) for e in tm[1:3]] == [(0, 0), (3, 1)], f"{img}:monster timers")
            need(list(exe[o["mode_flags"][img]:o["mode_flags"][img] + 15]) == DOC["mode_flags"], f"{img}:mode flags")
            nulls = [i for i in range(17) if far(exe, o["spell_effects"][img] + i * 4) == (0, 0)]
            need(nulls == DOC["spell_null"], f"{img}:spell effect nulls")
            wc = [far(exe, o["wall_click"][img] + i * 4) for i in range(7)]
            need(wc[0] == (0, 0) and all(s == DOC["wall_seg"][img] for _, s in wc[1:]), f"{img}:wall click")
            for op, want in DOC["tim_routines"][img].items():
                need(resolve(exe, o["tim_commands"][img] + op * 4) == want, f"{img}:tim 0x{op:02X}")
            for op, want in DOC["tim_nested"][img].items():
                need(resolve(exe, o["tim_nested"][img] + op * 4) == want, f"{img}:tim 19/0x{op:02X}")
        if "steps" in o and img in o["steps"]:
            need(set(words(exe, o["steps"][img], 16, "h")) <= {0, 32, -32}, f"{img}:steps")
        msgs.append(label)
    # across programs: spell rows byte-identical; character records equal except the segment word at +0x15
    imgs = list(by)
    for a, b in zip(imgs, imgs[1:]):
        sa, sb = OFFSETS["spells"][a], OFFSETS["spells"][b]
        need(by[a][sa:sa + 476] == by[b][sb:sb + 476], f"spells {a}={b}")
        ca, cb = OFFSETS["characters"][a], OFFSETS["characters"][b]
        for i in range(9):
            ra = bytearray(by[a][ca + i * 130:ca + i * 130 + 130]); rb = bytearray(by[b][cb + i * 130:cb + i * 130 + 130])
            ra[0x15:0x17] = rb[0x15:0x17] = b"\0\0"
            need(ra == rb, f"character {i} {a}={b}")
    if not found:
        bad.append("no known MAIN.EXE or MAINW.EXE (CD DATA/HARDRIVE or floppy folder)")
    print(f"CHECK exe_tables: {', '.join(msgs) or 'no program'}: character rows 0,0,0,1,0,0,1,2,4, spells, "
          f"experience, difficulty rows, prices, timers, mode flags, spell/wall/TIM pointers as the pages give, "
          f"bad={bad or 'none'}")
    return 0 if not bad else 1


def main():
    ap = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None,
                    help="the game's DATA folder (default: $LOL1_DATA)")
    ap.add_argument("--table", help="print only this table")
    ap.add_argument("--image", choices=["cd", "cdw", "floppy"], help="print only this program")
    ap.add_argument("--lang", default="ENG", help="language of the spell names: ENG, FRE or GER")
    ap.add_argument("--list", action="store_true", help="list the table names and their offsets")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.list:
        for t, offs in OFFSETS.items():
            print(f"{t:14s} " + ", ".join(f"{k} +0x{v:X}" for k, v in offs.items()) + f"  {TITLES[t]}")
        return 0
    found = find_images(a.data)
    if a.check:
        return check(found)
    if a.table and a.table not in OFFSETS:
        print(f"unknown table {a.table}; see --list"); return 2
    if not found:
        print("no MAIN.EXE or MAINW.EXE of a known size in", a.data); return 1
    name_of = spell_names(a.data, a.lang)
    for img, label, path, exe in found:
        if a.image and img != a.image:
            continue
        print(f"# {label} ({len(exe)} bytes, MZ header 0x{header_size(exe):X})")
        for t, offs in OFFSETS.items():
            if (a.table and t != a.table) or img not in offs:
                continue
            print_table(t, img, exe, offs[img], name_of)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
