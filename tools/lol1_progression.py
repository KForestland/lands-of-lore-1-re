#!/usr/bin/env python3
"""Level-to-level table for Lands of Lore 1, from the level scripts.

Each row is one static call: loadNewLevel (function 0x3C) or a door call
(0x31 triggerDoorSwitch, 0x33 setDoorState, 0x86 blockDoor) in LEVEL<n>.INF
or LEVEL<n>.INI. The entries are the ORDR entries that reach that instruction
through jumps, both arms of ifNotJmp, and calls (pushRetOrPos 1 followed by
jmp). A return ends the path. The conditions are the ifNotJmp tests still
open on those paths, with the arm that was taken.

The stack model follows the EMC2 interpreter. The stack grows downward from
slot 99. A call pushes the return word and the old base, then sets the base
to the first argument. pushBPAdd reads that frame. Argument 0 is the top of
the stack.

  lol1_progression.py              # print the page
  lol1_progression.py --out FILE   # write the page
  lol1_progression.py --check      # the CD page equals docs/PROGRESSION.md and
                                   # every level sheet links its rows (both ways)
"""
from cli_errors import run_cli
from collections import defaultdict, deque
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lol1lib as L
import emc2_decompile as E
import level_report as R

PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "PROGRESSION.md")
DOOR = {0x31: "door switch", 0x33: "door state", 0x86: "block door"}
INTEREST = {0x3C: 3, 0x31: 2, 0x33: 2, 0x86: 1}
UNKNOWN = ("u",)
FACE = ("face",)
# getItemPara selectors read on the item in hand (getItemInHand, 0x53). CD
# MAIN.EXE+0x13888 jump table at +0x139B6: selector 4 is the item slot's word
# +0x0C (its type index), selector 8 the type record's byte +2 (shape index).
HAND = {4: "type", 8: "shape"}
# Visits to one address, per entry, before the walk stops following that entry.
CAP = 1000
STATE_CAP = 400_000


def const(value):
    if isinstance(value, tuple) and value and value[0] == "k":
        return value[1]
    return None


def call_of(value, func):
    if isinstance(value, tuple) and len(value) >= 3 and value[0] == "call" and value[1] == func:
        return value[2]
    return None


def signed(number):
    number &= 0xFFFF
    return number - 0x10000 if number >= 0x8000 else number


def named_compare(op, top, second):
    ordered = op in (">", ">=", "<", "<=")
    pairs = ((top, second),) if ordered else ((top, second), (second, top))
    for left, right in pairs:
        number = const(right)
        if number is None:
            continue
        if left == FACE or call_of(left, 0x1C) is not None:
            return ("face", op, number)
        if ordered:
            continue
        args = call_of(left, 0x08)
        if args is not None and const(args[0] if args else None) is not None:
            return ("flag", const(args[0]), op, number)
        args = call_of(left, 0x85)
        if args is not None and len(args) > 1 and const(args[1]) is not None:
            return ("item", const(args[1]), op, number)
        args = call_of(left, 0xA5)
        if args is not None and len(args) > 2 and const(args[2]) is not None:
            return ("find", const(args[2]), op, number)
        args = call_of(left, 0x6E)
        if args is not None and const(args[0] if args else None) is not None:
            return ("party", const(args[0]), op, number)
        args = call_of(left, 0x47)
        if args is not None and const(args[0] if args else None) is not None:
            return ("credits", const(args[0]), op, number)
        args = call_of(left, 0x12)
        if (args is not None and len(args) > 1 and const(args[1]) in HAND
                and call_of(args[0], 0x53) is not None):
            return ("hand", const(args[1]), op, number)
    return None


def invert(pred):
    if not pred or pred == ("comp",):
        return ("comp",)
    kind = pred[0]
    if kind == "and":
        return ("or", invert(pred[1]), invert(pred[2]))
    if kind == "or":
        return ("and", invert(pred[1]), invert(pred[2]))
    if kind == "flag":
        return ("flag", pred[1], "!=" if pred[2] == "==" else "==", pred[3])
    if kind in ("item", "find", "party"):
        return (kind, pred[1], "!=" if pred[2] == "==" else "==", pred[3])
    if kind == "credits":
        if pred[2] == ">=":
            return ("credits", pred[1], "<")
        if pred[2] == "<":
            return ("credits", pred[1], ">=")
        return ("credits", pred[1], "!=" if pred[2] == "==" else "==", pred[3])
    if kind == "hand":
        return ("hand", pred[1], "!=" if pred[2] == "==" else "==", pred[3])
    if kind == "face":
        return (kind, "!=" if pred[1] == "==" else "==", pred[2])
    return ("comp",)


def nz_pred(value):
    """What is true when `value` is nonzero. ('const', n) when it is a constant."""
    number = const(value)
    if number is not None:
        return ("const", number)
    args = call_of(value, 0x08)
    if args is not None and const(args[0] if args else None) is not None:
        return ("flag", const(args[0]), "!=", 0)
    args = call_of(value, 0x85)
    if args is not None and len(args) > 1 and const(args[1]) is not None:
        return ("item", const(args[1]), "!=", 0)
    args = call_of(value, 0xA5)
    if args is not None and len(args) > 2 and const(args[2]) is not None:
        return ("find", const(args[2]), "!=", 0)
    args = call_of(value, 0x6E)
    if args is not None and const(args[0] if args else None) is not None:
        return ("party", const(args[0]), "!=", 0)
    args = call_of(value, 0x47)
    if args is not None and const(args[0] if args else None) is not None:
        return ("credits", const(args[0]), ">=")
    if isinstance(value, tuple) and value and value[0] == "cmp":
        return named_compare(value[1], value[2], value[3]) or ("comp",)
    if isinstance(value, tuple) and value and value[0] == "not":
        inner = nz_pred(value[1])
        if inner[0] == "const":
            return ("const", 0 if inner[1] else 1)
        return invert(inner)
    if isinstance(value, tuple) and value and value[0] in ("and", "or"):
        left, right = nz_pred(value[1]), nz_pred(value[2])
        if left[0] == "const" and right[0] == "const":
            if value[0] == "and":
                return ("const", 1 if left[1] and right[1] else 0)
            return ("const", 1 if left[1] or right[1] else 0)
        if left[0] == "const" or right[0] == "const":
            if value[0] == "and":
                if left == ("const", 0) or right == ("const", 0):
                    return ("const", 0)
                return right if left[0] == "const" else left
            if (left[0] == "const" and left[1]) or (right[0] == "const" and right[1]):
                return ("const", 1)
            return right if left[0] == "const" else left
        if left == ("comp",) and right == ("comp",):
            return ("comp",)
        return (value[0], left, right)
    return ("comp",)


def render(pred):
    if pred == ("comp",):
        return "computed"
    kind = pred[0]
    if kind == "flag":
        return f"flag {pred[1]} {pred[2]} {pred[3]}"
    if kind == "item":
        return f"item {pred[1]} {pred[2]} {pred[3]}"
    if kind == "find":
        return f"finds item {pred[1]} {pred[2]} {pred[3]}"
    if kind == "party":
        return f"party member {pred[1]} {pred[2]} {pred[3]}"
    if kind == "credits":
        if pred[2] in (">=", "<"):
            return f"credits {pred[2]} {pred[1]}"
        return f"credits {pred[1]} {pred[2]} {pred[3]}"
    if kind == "hand":
        return f"hand item {HAND[pred[1]]} {pred[2]} {pred[3]}"
    if kind == "face":
        return f"facing {pred[1]} {pred[2]}"
    if kind in ("and", "or"):
        return f"({render(pred[1])}) {kind} ({render(pred[2])})"
    return "computed"


def fold_bin(op, top, second):
    a, b = const(top), const(second)
    if a is not None and b is not None:
        if op == 0:
            return ("k", 1 if b and a else 0)
        if op == 1:
            return ("k", 1 if b or a else 0)
        if op == 2:
            return ("k", 1 if a == b else 0)
        if op == 3:
            return ("k", 1 if a != b else 0)
        if op == 4:
            return ("k", 1 if a > b else 0)
        if op == 5:
            return ("k", 1 if a >= b else 0)
        if op == 6:
            return ("k", 1 if a < b else 0)
        if op == 7:
            return ("k", 1 if a <= b else 0)
        if op == 8:
            return ("k", signed(b + a))
        if op == 9:
            return ("k", signed(b - a))
        if op == 10:
            return ("k", signed(b * a))
        if op == 11 and a:
            return ("k", int(b / a))
        if op == 12:
            return ("k", b >> a)
        if op == 13:
            return ("k", signed(b << (a & 15)))
        if op == 14:
            return ("k", b & a)
        if op == 15:
            return ("k", b | a)
        if op == 16 and a:
            return ("k", b % a)
        if op == 17:
            return ("k", b ^ a)
        return UNKNOWN
    names = {2: "==", 3: "!=", 4: ">", 5: ">=", 6: "<", 7: "<="}
    if op == 0:
        return ("and", second, top)
    if op == 1:
        return ("or", second, top)
    if op in names:
        return ("cmp", names[op], top, second)
    return UNKNOWN


class Mach:
    __slots__ = ("sp", "bp", "stack", "regs", "ret")

    def __init__(self, entry):
        self.sp = 99
        self.bp = 101
        self.stack = {99: ("k", 0)}
        self.regs = [UNKNOWN] * 30
        self.regs[5] = ("k", entry)
        self.regs[6] = FACE
        self.ret = UNKNOWN

    def clone(self):
        other = Mach(0)
        other.sp = self.sp
        other.bp = self.bp
        other.stack = dict(self.stack)
        other.regs = list(self.regs)
        other.ret = self.ret
        return other

    def push(self, value):
        self.sp -= 1
        self.stack[self.sp] = value

    def pop(self):
        value = self.stack.get(self.sp, UNKNOWN)
        self.sp += 1
        return value

    def key(self):
        items = tuple((slot, self.stack[slot]) for slot in range(self.sp, 100) if slot in self.stack)
        return (self.sp, self.bp, items, tuple(self.regs), self.ret)


def add_guard(guards, guard):
    """A guard is (DATA word of the ifNotJmp, 1 for the fall-through arm or 0 for the jump, test)."""
    if guard in guards:
        return guards
    return guards + (guard,)


def guard_pred(guard):
    return guard[2] if guard[1] else invert(guard[2])


def guard_text(guards):
    parts = []
    for guard in guards:
        text = render(guard_pred(guard))
        if text not in parts:
            parts.append(text)
    return "; ".join(parts) if parts else "none"


def show_args(values):
    shown = []
    for value in values:
        number = const(value)
        shown.append("?" if number is None else str(number))
    return tuple(shown)


def walk(script):
    """{DATA word: {func, n, by_entry: {entry: {(guards, args)}}}} for the calls we list."""
    ins = script.instructions
    index = {item.address: i for i, item in enumerate(ins)}
    sites = {}
    capped = set()
    for i, item in enumerate(ins):
        if item.opcode == 14 and item.argument in INTEREST:
            nxt = ins[i + 1] if i + 1 < len(ins) else None
            count = nxt.argument if nxt is not None and nxt.opcode == 12 else INTEREST[item.argument]
            sites[item.address] = {"func": item.argument, "n": count, "by_entry": defaultdict(set)}

    def run(entry, start):
        mach = Mach(entry)
        work = deque([(start, mach, (), ())])
        seen = set()
        per_addr = defaultdict(int)
        while work:
            addr, mach, guards, rets = work.popleft()
            if addr not in index:
                continue
            token = (addr, guards, rets, mach.key())
            if token in seen:
                continue
            per_addr[addr] += 1
            # A hot address is a loop that keeps changing a register. The first
            # paths still record every call they reach. The cap stops the rest.
            if per_addr[addr] > CAP or len(seen) > STATE_CAP:
                capped.add(entry)
                continue
            seen.add(token)
            k = index[addr]
            item = ins[k]
            op, arg = item.opcode, item.argument
            if item.address in sites:
                count = sites[item.address]["n"]
                got = tuple(mach.stack.get(mach.sp + i, UNKNOWN) for i in range(count))
                sites[item.address]["by_entry"][entry].add((guards, got))
            if op == 0:
                work.append((arg, mach, guards, rets))
                continue
            if op == 15:
                pred = nz_pred(mach.pop())
                if pred[0] == "const":
                    if pred[1] == 0:
                        work.append((item.target, mach, guards, rets))
                    elif k + 1 < len(ins):
                        work.append((ins[k + 1].address, mach, guards, rets))
                    continue
                if k + 1 < len(ins):
                    work.append((ins[k + 1].address, mach.clone(), add_guard(guards, (addr, 1, pred)), rets))
                work.append((item.target, mach, add_guard(guards, (addr, 0, pred)), rets))
                continue
            if op == 18 or (op == 8 and arg == 1):
                if not rets:
                    continue
                mach.pop()
                mach.pop()
                ret_addr, saved_bp, ret_guards = rets[-1]
                mach.bp = saved_bp
                work.append((ret_addr, mach, ret_guards, rets[:-1]))
                continue
            if op in (3, 4):
                mach.push(("k", arg))
            elif op == 5:
                mach.push(mach.regs[arg] if 0 <= arg < 30 else UNKNOWN)
            elif op == 6:
                mach.push(mach.stack.get(mach.bp - (arg + 2), UNKNOWN))
            elif op == 7:
                mach.push(mach.stack.get(mach.bp + (arg - 1), UNKNOWN))
            elif op == 2 and arg == 0:
                mach.push(mach.ret)
            elif op == 2 and arg == 1:
                nxt = ins[k + 1] if k + 1 < len(ins) else None
                if nxt is not None and nxt.opcode == 0 and k + 2 < len(ins) and len(rets) < 12:
                    saved = mach.bp
                    mach.push(("k", nxt.address + 1))
                    mach.push(("k", saved))
                    mach.bp = mach.sp + 2
                    work.append((nxt.argument, mach, guards, rets + ((ins[k + 2].address, saved, guards),)))
                    continue
                mach.push(UNKNOWN)
            elif op == 8 and arg == 0:
                mach.ret = mach.pop()
            elif op == 9:
                value = mach.pop()
                if 0 <= arg < 30:
                    mach.regs[arg] = value
            elif op == 10:
                mach.stack[mach.bp - (arg + 2)] = mach.pop()
            elif op == 11:
                mach.stack[mach.bp + (arg - 1)] = mach.pop()
            elif op == 12:
                mach.sp += arg
            elif op == 13:
                for _ in range(max(arg, 0)):
                    mach.push(UNKNOWN)
            elif op == 14:
                nxt = ins[k + 1] if k + 1 < len(ins) else None
                count = nxt.argument if nxt is not None and nxt.opcode == 12 else 0
                got = tuple(mach.stack.get(mach.sp + i, UNKNOWN) for i in range(count))
                mach.ret = ("call", arg, got)
            elif op == 16:
                value = mach.pop()
                number = const(value)
                if number is not None and arg == 0:
                    mach.push(("k", 0 if number else 1))
                elif number is not None and arg == 1:
                    mach.push(("k", -number))
                elif number is not None and arg == 2:
                    mach.push(("k", signed(~number)))
                elif arg == 0:
                    mach.push(("not", value))
                else:
                    mach.push(UNKNOWN)
            elif op == 17:
                top = mach.pop()
                second = mach.pop()
                mach.push(fold_bin(arg, top, second))
            elif op == 1:
                mach.ret = ("k", arg)
            if k + 1 < len(ins):
                work.append((ins[k + 1].address, mach, guards, rets))

    for header, entries in script.entries.items():
        start = header + 1
        if start not in index:
            continue
        for entry in entries:
            run(entry, start)
    masks = {}
    for header, entries in script.entries.items():
        for entry in entries:
            masks[entry] = script.words[header]
    return sites, masks, capped


def entry_label(entry, ext):
    if ext == "INI":
        return f"INI {entry}"
    if entry in R.SPECIAL_ENTRIES:
        return f"{entry:#x} {R.SPECIAL_ENTRIES[entry]}"
    return str(entry)


def event_text(mask, entry, ext):
    if ext == "INI":
        return "level load"
    if entry >= 0x400:
        return R.SPECIAL_ENTRIES.get(entry, "none")
    names = [name for bit, name in R.EVENTS if mask & bit]
    rest = mask & ~sum(bit for bit, _ in R.EVENTS) & 0xFFFF
    if rest:
        names.append(f"bit {rest:#x}")
    return ", ".join(names) if names else "none"


def join_alts(values):
    items = list(values)
    if items and all(item == items[0] for item in items):
        return items[0]
    return " or ".join(items)


def merge_paths(paths):
    """Drop a test whose two arms both reach the call: paths T + one arm and T + the other arm
    of the same ifNotJmp become T. A path that holds all the guards of another path is dropped."""
    paths = {frozenset(path): path for path in paths}
    changed = True
    while changed:
        changed = False
        for key in sorted(paths, key=len):
            for guard in key:
                other = (key - {guard}) | {(guard[0], 1 - guard[1], guard[2])}
                if other in paths:
                    path = paths[key]
                    del paths[key], paths[other]
                    rest = tuple(item for item in path if item != guard)
                    paths.setdefault(frozenset(rest), rest)
                    changed = True
                    break
            if changed:
                break
        for key in list(paths):
            if any(other < key for other in paths):
                del paths[key]
                changed = True
    return set(paths.values())


def row_for(level, ext, addr, rec, masks):
    argsets = set()
    paths = set()
    for entry, pairs in rec["by_entry"].items():
        for guards, got in pairs:
            argsets.add(show_args(got))
            paths.add(guards)
    texts = {guard_text(guards) for guards in merge_paths(paths)}
    if not argsets:
        argsets.add(tuple("?" for _ in range(rec["n"])))
        texts.add("none")
    ordered = sorted(argsets)
    columns = []
    width = rec["n"]
    for index in range(width):
        columns.append(join_alts(item[index] if index < len(item) else "?" for item in ordered))
    entries = sorted(rec["by_entry"])
    entry_cell = ", ".join(entry_label(entry, ext) for entry in entries) if entries else "none"
    events = []
    for entry in entries:
        text = event_text(masks.get(entry, 0), entry, ext)
        if text not in events:
            events.append(text)
    if len(events) <= 1:
        event_cell = events[0] if events else "none"
    else:
        event_cell = "; ".join(
            f"{entry_label(entry, ext)}: {event_text(masks.get(entry, 0), entry, ext)}" for entry in entries)
    return {
        "level": level,
        "func": rec["func"],
        "args": columns,
        "word": addr,
        "entries": entry_cell,
        "entry_ids": entries,
        "event": event_cell,
        "conditions": join_alts(sorted(texts)),
    }


def collect(data_dir, levels=range(1, 30)):
    exits, doors, stopped = [], [], []
    for level in levels:
        for ext in ("INF", "INI"):
            blob = L.level_member(level, ext, data_dir)
            if blob is None:
                if ext == "INF":
                    raise ValueError(f"LEVEL{level}.INF is absent")
                continue
            script = E.read_script(blob)
            sites, masks, capped = walk(script)
            if capped:
                stopped.append((level, ext, sorted(capped)))
            for addr, rec in sorted(sites.items()):
                row = row_for(level, ext, addr, rec, masks)
                if rec["func"] == 0x3C:
                    exits.append(row)
                else:
                    doors.append(row)
    return exits, doors, stopped


def cell(value):
    return str(value).replace("|", "/")


def edges_of(exits):
    found = {level: set() for level in range(1, 30)}
    for row in exits:
        if row["entry_ids"] and " or " not in row["args"][0] and row["args"][0] != "?":
            try:
                found[row["level"]].add(int(row["args"][0]))
            except ValueError:
                pass
        elif row["entry_ids"]:
            for part in row["args"][0].split(" or "):
                if part != "?":
                    try:
                        found[row["level"]].add(int(part))
                    except ValueError:
                        pass
    return found


def reachable_from(edges, start):
    seen = set()
    wave = [start]
    while wave:
        level = wave.pop()
        if level in seen or level not in edges:
            continue
        seen.add(level)
        wave.extend(sorted(edges[level]))
    return seen


def level_cell(level, pending):
    """The From cell. The first row of each level carries its anchor and its sheet link."""
    if level in pending:
        pending.remove(level)
        return f'<a name="level-{level}"></a>[{level}](levels/level{level:02d}.md)'
    return level


def check_level_sheets(exits):
    """Two-way check: every level in the table has a sheet, every sheet has rows,
    and each sheet links its rows here and the numbers page."""
    directory = os.path.join(os.path.dirname(PAGE), "levels")
    mentioned = {row["level"] for row in exits}
    for row in exits:
        for part in row["args"][0].split(" or ") if row["args"] else []:
            if part.isdigit():
                mentioned.add(int(part))
    sheets = {int(name[5:7]) for name in os.listdir(directory)
              if len(name) == 10 and name.startswith("level") and name.endswith(".md") and name[5:7].isdigit()}
    sources = {row["level"] for row in exits}
    if sheets != mentioned or not sheets <= sources:
        raise ValueError(f"without a sheet: {sorted(mentioned - sheets)}; "
                         f"without a progression row: {sorted((sheets - mentioned) | (sheets - sources))}")
    for level in sorted(sheets):
        with open(os.path.join(directory, f"level{level:02d}.md"), encoding="utf-8") as source:
            text = source.read()
        for link in (f"](../PROGRESSION.md#level-{level})", "](../NUMBERS.md)"):
            if link not in text:
                raise ValueError(f"missing {link[2:-1]} link in level{level:02d}.md")
    return len(sheets)


def page(exits, doors, stopped):
    lines = [
        "# Progression",
        "",
        "Made by `tools/lol1_progression.py` from each level's `LEVEL<n>.INF` and `LEVEL<n>.INI` "
        "(CD edition). One row is one static call. `loadNewLevel` (function 0x3C) is the level change: "
        "level, block, facing. Door calls are `triggerDoorSwitch` (0x31), `setDoorState` (0x33) and "
        "`blockDoor` (0x86). The word column is the DATA word of that call. The entries column lists "
        "the script entries whose inspected paths reach the call, through jumps, both arms of `ifNotJmp` "
        "(only the arm taken when the tested value is a constant argument), and calls. "
        f"The walk can cut off paths after {CAP:,} visits to an address or once an entry has more than "
        f"{STATE_CAP:,} distinct states, so some entries are incomplete. "
        "A return ends that path, so a later subroutine is not credited to the entry. "
        "The conditions column lists the `ifNotJmp` tests still open on a path that reaches the call, "
        "outermost first. Paths that differ only in the arm of one test are merged, so a test whose two "
        "arms both lead to the call is not listed. `flag 41 == 0` means that arm of the compare. "
        "`hand item type` is `getItemPara` selector 4 on the item in hand (its type index) and "
        "`hand item shape` is selector 8 (its shape index), CONFIRMED by the selector jump table of "
        "the CD handler (`MAIN.EXE+0x13888`, table at `+0x139B6`). `finds item` is argument 2 of `findInventoryItem`. `item` is "
        "argument 1 of `checkPartyForItemType`. `computed` is a test that is not a flag, an item, "
        "a party member, credits, a hand-item type or shape, or facing. `none` means no such test is open. "
        "An entry cell of `none` means the instruction is in the script and no entry reaches it. "
        "A call in a shared subroutine is one row. Where callers pass different constants, the "
        "argument cells list each combination in the same order, separated by ` or `. "
        "A column that is the same in every combination is written once. "
        "Item and flag numbers are the script arguments.",
        "",
        f"{len(exits)} level changes and {len(doors)} door calls across levels 1 to 29.",
        "",
        "## Level to level",
        "",
        "| From | To | Block | Facing | Word | Entries | Event | Conditions |",
        "|---:|---|---|---|---:|---|---|---|",
    ]
    pending = set(range(1, 30))
    for row in exits:
        args = (row["args"] + ["?", "?", "?"])[:3]
        parts = [level_cell(row["level"], pending), args[0], args[1], args[2], f"0x{row['word']:04X}",
                 row["entries"], row["event"], row["conditions"]]
        lines.append("| " + " | ".join(cell(part) for part in parts) + " |")
    lines += [
        "",
        "## Door calls",
        "",
        "| Level | Call | Block | Argument | Word | Entries | Event | Conditions |",
        "|---:|---|---|---|---:|---|---|---|",
    ]
    for row in doors:
        args = (row["args"] + ["-", "-"])[:2]
        if row["func"] == 0x86:
            args = [row["args"][0] if row["args"] else "?", "-"]
        parts = [row["level"], DOOR[row["func"]], args[0], args[1], f"0x{row['word']:04X}",
                 row["entries"], row["event"], row["conditions"]]
        lines.append("| " + " | ".join(cell(part) for part in parts) + " |")
    edges = edges_of(exits)
    reached = reachable_from(edges, 1)
    outside = [str(level) for level in range(1, 30) if level not in reached]
    no_out = [str(level) for level in range(1, 30) if not edges[level]]
    lines += [
        "",
        "## Graph",
        "",
        "An edge is a constant destination level on a `loadNewLevel` row that a script entry reaches. "
        "All 29 levels are listed. Several rows can share one edge.",
        "",
        "| From | To |",
        "|---:|---|",
    ]
    for level in range(1, 30):
        dests = ", ".join(str(item) for item in sorted(edges[level])) if edges[level] else "none"
        lines.append(f"| {level} | {dests} |")
    lines += [
        "",
        "Constant destinations from the reached sites "
        + ("leave every level on a path from level 1, and every level has an edge out. "
           if not outside and not no_out else
           f"leave levels {', '.join(outside) or 'none'} off the paths from level 1, "
           f"and levels {', '.join(no_out) or 'none'} with no constant edge out. "),
        "UNCONFIRMED: this graph is not a play trace. A static edge does not show that the party can walk it, "
        "and no level is marked unreachable or a dead end from these sites alone.",
        "",
    ]
    if stopped:
        parts = [f"level {level} {ext} entr{'y' if len(ids) == 1 else 'ies'} "
                 + ", ".join(entry_label(entry, ext) for entry in ids) for level, ext, ids in stopped]
        lines += [
            "## Walk limit",
            "",
            f"The walk stops following one entry after {CAP} visits to one address with different register "
            "values (a loop). It stopped for " + "; ".join(parts) + ". For those entries the entry, "
            "argument and condition cells can be incomplete.",
            "",
        ]
    return "\n".join(lines)


def cd_spot_checks(exits, doors):
    tour = [row for row in exits if row["level"] == 1 and row["word"] == 0x130C]
    if len(tour) != 1:
        raise ValueError("level 1 DATA word 0x130C is missing")
    row = tour[0]
    if row["args"][:3] != ["2", "106", "2"] or "621" not in row["entries"].split(", "):
        raise ValueError("level 1 DATA word 0x130C lost loadNewLevel(2, 106, 2) from entry 621")
    if "facing == 2" not in row["conditions"]:
        raise ValueError("level 1 DATA word 0x130C lost the facing test")
    for row in exits:
        if row["level"] == 2 and "268" in row["entries"].split(", "):
            raise ValueError("level 2 entry 268 reaches a level change past its return")
    hand = [row for row in exits if row["level"] == 2 and "392" in row["entries"].split(", ")
            and "flag 41 == 0" in row["conditions"] and "hand item shape == 40" in row["conditions"]]
    if not hand:
        raise ValueError("level 2 entry 392 lost flag 41 == 0 or the hand-item shape test")
    typed = [row for row in doors if row["level"] == 23 and row["word"] == 0x0DDF
             and row["conditions"] == "hand item type == 254"]
    if not typed:
        raise ValueError("level 23 DATA word 0x0DDF lost the hand-item type test")
    if len(exits) != 71:
        raise ValueError(f"expected 71 loadNewLevel sites, found {len(exits)}")


def main():
    parser = L.tool_args(__doc__, out_help="write the progression page to this file")
    args = parser.parse_args()
    try:
        exits, doors, stopped = collect(args.data)
        text = page(exits, doors, stopped)
        if L.is_cd_layout(args.data):
            cd_spot_checks(exits, doors)
            if len(doors) != 136:
                raise ValueError(f"expected 136 door calls, found {len(doors)}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"CHECK progression: {error}\n")
    if args.check:
        if L.is_cd_layout(args.data):
            stored = open(PAGE, encoding="utf-8").read() if os.path.isfile(PAGE) else ""
            if stored != text:
                parser.exit(1, "CHECK progression: docs/PROGRESSION.md differs from the script table\n")
            try:
                covered = check_level_sheets(exits)
            except (OSError, ValueError) as error:
                parser.exit(1, f"CHECK progression: {error}\n")
            note = f"docs/PROGRESSION.md matches; {covered} linked level sheets"
        else:
            note = "CD page not compared"
        print(f"CHECK progression: {len(exits)} level changes, {len(doors)} door calls; {note}")
        return 0
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"wrote {args.out}")
        return 0
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
