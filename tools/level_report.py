#!/usr/bin/env python3
"""Write a "level sheet" for each Lands of Lore 1 level, made only from the data.

For level n it reads LEVELn.CMZ, LEVELn.WLL, LEVELn.XXX, LEVELn.INI and
LEVELn.INF (and ONETIME.INF / LANDS.<lang> for item and place names) and
writes docs/levels/levelNN.md with:

  - area, tile set and palettes loaded (loadLevelGraphics calls)
  - wall types used and how often, with their WLL properties
  - clickable walls (levers, switches, door switches, niches) by block
  - every script entry point: which block, which events it answers, and a
    one-line plain description built from the functions it calls
  - items and monsters the scripts place (with their numbers)
  - automap legend, and the text ids the scripts show (ids only)

How a level script is entered (ScummVM, upstream 3b4db303,
engines/kyra/script/script_lol.cpp:64-92 runLevelScriptCustom): entry number
= block index 0-1023, or 0x400 (level loaded), 0x401-0x403 (script timers,
engines/kyra/engine/timer_lol.cpp:148), 0x404 (a monster died,
engines/kyra/engine/sprites_lol.cpp:203). The word before the entry's code is
an event mask; the entry runs only if it shares a bit with the event.

  level_report.py --level 1            # print the sheet for level 1
  level_report.py --out DIR           # write all 29 sheets and an index
  level_report.py --check              # build all 29; every entry and call decodes
"""
import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lol1lib as L
import emc2_decompile as E
import decode_dialogue as T
import tileset_mapper

# event bits (callers of runLevelScript / runLevelScriptCustom, ScummVM upstream lines)
EVENTS = [
    (0x0001, "party steps in"),             # engines/kyra/engine/scene_lol.cpp:665
    (0x0002, "party arrives (second path)"),  # scene_lol.cpp:695; also setNextFunc, engine/lol.cpp:947
    (0x0004, "party leaves"),               # scene_lol.cpp:664
    (0x0008, "party leaves (second path)"),  # scene_lol.cpp:694
    (0x0020, "fireball ends here"),          # engine/lol.cpp:2708 (processMagicFireball)
    (0x0040, "wall clicked"),                # engine/scene_rpg.cpp:580, scene_lol.cpp:783, gui/gui_lol.cpp:1446
    (0x0080, "item put down"),               # engine/items_lol.cpp:374
    (0x0100, "item taken"),                  # items_lol.cpp:382
    (0x0200, "fireball passes"),             # engine/lol.cpp:2577
    (0x0800, "monster leaves"),              # engine/sprites_lol.cpp:289
    (0x8000, "thrown item hits"),            # items_lol.cpp:493
]
SPECIAL_ENTRIES = {0x400: "level loaded", 0x401: "script timer 0", 0x402: "script timer 1",
                   0x403: "script timer 2", 0x404: "a monster died"}
# WLL special wall types (gui/gui_lol.cpp:1413-1440, clickedWall)
SPECIAL_WALLS = {1: "clickable wall", 2: "lever (to on)", 3: "lever (to off)", 4: "click runs script",
                 5: "door / door switch", 6: "niche"}
SIDES = ["north", "east", "south", "west"]
EVAL = {8: lambda b, a: b + a, 9: lambda b, a: b - a, 10: lambda b, a: b * a, 12: lambda b, a: b >> a,
        13: lambda b, a: b << a, 14: lambda b, a: b & a, 15: lambda b, a: b | a, 17: lambda b, a: b ^ a}


def simulate(script, start, stop, caller=None, depth=0, budget=None):
    """Walk instructions from DATA word `start` (exclusive) up to `stop`, with a
    small stack model: constants are tracked, other values are None. A call into
    a subroutine (pushRetOrPos 1 + jmp, engines/kyra/script/script.cpp:236-251)
    is followed one level deep; there `pushBPAdd k` reads the caller's k-th-last
    push (stack[bp + k - 1], script.cpp:265-267). Returns [(function id, args)]."""
    ins = script.instructions
    at = script._addr_index
    budget = budget if budget is not None else [4000]
    stack, calls = [], []
    k = at.get(start + 1, None)
    if k is None:
        return calls
    while k < len(ins) and budget[0] > 0:
        budget[0] -= 1
        x = ins[k]
        if stop is not None and x.address >= stop:
            break
        op, arg = x.opcode, x.argument
        if op in (3, 4):
            stack.append(arg)
        elif op == 7 and caller is not None:
            stack.append(caller[-arg] if 0 < arg <= len(caller) else None)
        elif op in (5, 6, 7) or (op == 2 and arg == 0):
            stack.append(None)
        elif op == 2 and arg == 1:
            nxt = ins[k + 1] if k + 1 < len(ins) else None
            if nxt is not None and nxt.opcode == 0 and depth < 1:
                calls += simulate(script, nxt.argument - 1, None, list(stack), depth + 1, budget)
                k += 2
                continue
            stack.clear()
        elif op == 17 and len(stack) >= 2:
            a, b = stack.pop(), stack.pop()
            stack.append(EVAL[arg](b, a) if a is not None and b is not None and arg in EVAL else None)
        elif op == 16 and stack:
            v = stack.pop(); stack.append(-v if (v is not None and arg == 1) else None)
        elif op == 14:
            n = ins[k + 1].argument if k + 1 < len(ins) and ins[k + 1].opcode == 12 else 0
            args = list(reversed(stack[-n:])) if n else []
            calls.append((arg, args + [None] * (n - len(args))))
        elif op == 12:
            if arg:
                del stack[-arg:]
        elif op in (9, 10, 11, 15) or (op == 8 and arg == 0):
            if stack: stack.pop()
        elif depth and (op == 18 or (op == 8 and arg == 1)):
            break                       # return from the subroutine
        else:
            stack.clear()
        k += 1
    return calls


def calls_by_entry(script):
    """{entry number: (event mask, [(function id, [args or None])])}."""
    object.__setattr__(script, "_addr_index", {x.address: k for k, x in enumerate(script.instructions)})
    starts = sorted(script.entries)            # header word addresses
    out = {}
    for k, h in enumerate(starts):
        stop = starts[k + 1] if k + 1 < len(starts) else len(script.words)
        calls = simulate(script, h, stop)
        mask = script.words[h]
        for e in script.entries[h]:
            out[e] = (mask, calls)
    return out


def item_names(data_dir):
    lands = T.file_strings(L.find_member("LANDS.ENG", data_dir)[1])
    s = E.read_script(L.find_member("ONETIME.INF", data_dir)[1])
    names = {}
    for e, (mask, calls) in calls_by_entry(s).items():
        for fn, a in calls:
            if fn == 0x0E and a and a[0] is not None and a[1] is not None:
                sid = a[1]
                names[a[0]] = T.decode_raw(lands[sid & 0x3FFF]).strip() if sid & 0x4000 and (sid & 0x3FFF) < len(lands) else f"string {sid:#x}"
    return names, lands


def wall_target(side, block):
    if side == -1:
        return f"all four walls of block {block}"
    if side is not None and 0 <= side < len(SIDES):
        return f"the {SIDES[side]} wall of block {block}"
    return f"wall side {'?' if side is None else side} of block {block}"


def describe(calls, text, items):
    """One plain line from the calls of an entry."""
    phrases = []

    def add(s):
        if s not in phrases:
            phrases.append(s)

    def v(x, fmt="{}"):
        return fmt.format(x) if x is not None else "?"

    def stem(index):
        return text[index][1].decode("latin-1") if index is not None and 0 <= index < len(text) else "?"

    for fn, a in calls:
        g = lambda i: a[i] if i < len(a) else None
        if fn == 0x00:
            add(f"sets {wall_target(g(1), v(g(0)))} to type {v(g(2))}")
        elif fn == 0x01:
            side = g(1) & 3 if g(1) is not None else None
            add(f"checks {wall_target(side, v(g(0)))}")
        elif fn == 0x07:
            add(("sets" if g(1) else "clears" if g(1) == 0 else "sets/clears") + f" game flag {v(g(0))}")
        elif fn == 0x08:
            add(f"tests game flag {v(g(0))}")
        elif fn == 0x0C:
            add("deletes the held item")
        elif fn == 0x0F:
            add(f"creates item type {v(g(0))} and returns its handle")
        elif fn == 0x10:
            add(f"places or moves item handle {v(g(0))} to level {v(g(1))}, block {v(g(2))}")
        elif fn == 0x11:
            add(f"places item {v(g(0))} ({items.get(g(0), '?')}) on block {v(g(4))}")
        elif fn == 0x1E:
            add(f"sets music theme {v(g(0))}")
        elif fn == 0x2E:
            add(f"sets script global {v(g(0))} to {v(g(1))}")
        elif fn == 0x30:
            add(f"requests engine global change, selector {v(g(0))}, operands {v(g(1))}, {v(g(2))}")
        elif fn == 0x38:
            add(f"places a monster of type slot {v(g(4))} on block {v(g(0))} in mode {v(g(6))}")
        elif fn == 0x3C:
            add(f"moves the party to level {v(g(0))}, block {v(g(1))}, facing {v(g(2))}")
        elif fn == 0x31:
            add(f"operates the door switch at block {v(g(0))} with action {v(g(1))}")
        elif fn == 0x33:
            verb = "sets" if g(1) else "clears" if g(1) == 0 else "sets/clears"
            add(f"{verb} door state bit 0x20 on block {v(g(0))}")
        elif fn == 0x34:
            add(f"toggles {wall_target(g(1), v(g(0)))} between types {v(g(2))} and {v(g(3))}")
        elif fn == 0x4E:
            add(f"loads cut-scene {stem(g(1))}.TIM into slot {v(g(0))}")
        elif fn == 0x57:
            add(f"plays a sound (ID {v(g(0))})")
        elif fn == 0x60:
            where = "the party's block" if g(1) == -1 else f"block {v(g(1))}"
            add(f"plays a sound (ID {v(g(0))}) at {where}")
        elif fn == 0x64:
            add(f"plays music track {v(g(0))}")
        elif fn in (0x6F, 0x79, 0x82):
            add(f"shows text ID {v(g({0x6F: 1, 0x79: 0, 0x82: 2}[fn]), '{:#06x}')}")
        elif fn in (0x5E, 0x7A):
            add(f"plays chat/dialogue text ID {v(g(2 if fn == 0x5E else 0), '{:#06x}')}")
        elif fn == 0xBB:
            controls = {-1: "stops speech", -2: "checks speech playback"}
            add(controls.get(g(0), f"plays speech track {v(g(0))} for character {v(g(1))}"))
        elif fn == 0x45:
            add(f"sets up {v(g(0))} dialogue choices")
        elif fn == 0x58:
            add("reads the dialogue result")
        elif fn == 0x8C:
            add(f"starts a dialogue sequence in mode {v(g(0))}")
        elif fn == 0x46:
            add(("gives" if (g(0) or 0) >= 0 else "takes") + f" {v(abs(g(0)) if g(0) is not None else None)} crown(s)")
        elif fn == 0x4B:
            add(("a character joins" if (g(0) or 0) >= 0 else "a character leaves") + " the party")
        elif fn == 0x49:
            add(f"puts item {v(g(0))} ({items.get(g(0), '?')}) on an empty cursor")
        elif fn == 0x4C:
            add(f"gives item {v(g(0))} ({items.get(g(0), '?')}) if inventory placement succeeds")
        elif fn == 0x41:
            target = "the party" if g(0) == -1 else f"target {v(g(0))}"
            add(f"deals damage to {target} (amount {v(g(1))})")
        elif fn == 0x61:
            add(f"heals character {v(g(0))} with amount or spell level {v(g(1))}")
        elif fn == 0x48:
            if g(1) == 0:
                add(f"disables script timer {v(g(0))}")
            else:
                add(f"sets script timer {v(g(0))} to {v(g(1))} ticks")
        elif fn == 0x75:
            if g(3) != 0:
                prefix = "removes" if g(3) is not None else "may remove"
                add(f"{prefix} monsters from block {v(g(0))}")
            if g(5) != 0:
                prefix = "moves" if g(5) is not None else "may move"
                add(f"{prefix} items from block {v(g(0))} to level {v(g(2))}, block {v(g(1))}")
            if g(4) and g(5) != 0:
                add("requests the item-placement event on the current level")
        elif fn == 0x3F:
            add(f"defines monster type {v(g(0))}")
        elif fn == 0x0B:
            add(f"loads monster sprites {stem(g(0))} into slot {v(g(1))}")
        elif fn == 0x09:
            add(f"loads wall tiles {stem(g(0))}")
        elif fn == 0xAE:
            add("drops the party through a pit")
        elif fn == 0x72:
            add(f"launches a projectile from block {v(g(2))} in direction {v(g(6))}")
        elif fn == 0x5B:
            if g(0) == -1:
                continue
            monster = v(g(0) & 0x7FFF if g(0) is not None else None)
            fields = {0: "mode", 1: "HP", 2: "block", 3: "facing"}
            if g(1) in fields:
                add(f"sets monster {monster} {fields[g(1)]} to {v(g(2))}")
            elif g(1) == 6:
                add(f"sets monster {monster} flag bits {v(g(2), '{:#x}')}")
            else:
                add(f"requests monster {monster} change, selector {v(g(1))}, value {v(g(2))}")
        else:
            name = E.FUNCTIONS[fn] if fn < len(E.FUNCTIONS) and E.FUNCTIONS[fn] else f"function {fn:#x}"
            if name not in QUIET:
                add(re.sub(r"(?<!^)(?=[A-Z])", " ", name).lower())
    # game-changing actions first, checks and sounds last; the code order is kept within each rank
    rank = lambda t: (0 if t.startswith(("loads wall", "moves the party", "places", "loads cut", "sets the", "sets all", "toggles",
                                          "operates", "gives", "takes", "a character joins", "a character leaves",
                                          "drops the party", "deals", "heals", "puts item", "deletes", "removes monsters")) else
                      2 if t.startswith(("tests", "checks", "plays a sound", "set global", "set ")) else 1)
    phrases = sorted(phrases, key=rank)
    return "; ".join(phrases[:8]) + (" …" if len(phrases) > 8 else "") if phrases else "no action summarized"


# functions left out of the one-line descriptions (screen and input housekeeping)
QUIET = {"drawScene", "delay", "update", "hideMouse", "showMouse", "clearDialogueField", "fadeToBlack",
         "fadePalette", "copyRegion", "getDirection", "getGlobalVar", "getGlobalScriptVar", "getItemInHand",
         "checkRectForMousePointer", "redrawPlayfield", "updateDrawPage2", "savePage5", "restorePage5",
         "dummy0", "dummy1", "getItemPara", "getCharacterStat", "getMonsterStat", "getWallFlags",
         "releaseTimScript", "runTimScript", "freeAnimStruct", "stopTimScript", "resetTimDialogueState",
         "restoreAfterSceneWindowDialogue", "initSceneWindowDialogue", "restoreAfterSpecialScene",
         "prepareSpecialScene", "restoreAfterDialogueSequence", "fadeClearSceneWindow", "fadeSequencePalette",
         "crossFadeRegion", "crossFadeScene", "setDefaultButtonState", "restoreButtonsAfterSpecialScene",
         "stopPortraitSpeechAnim", "resetPortraitsAndDisableSysTimer", "enableSysTimer", "checkNeedSceneRestore",
         "setPaletteBrightness", "calcCoordinatesAddDirectionOffset", "calcNewBlockPosition", "rollDice",
         "getNextActiveCharacter", "getSelectedCharacter", "countBlockItems", "getItemOnPos", "findAssignedMonster",
         "checkBlockForMonster", "countAllMonsters", "countSpecificMonsters", "getLanguage", "setSequenceButtons",
         "setSpecialSceneButtons", "drawExitButton", "disableControls", "enableControls", "setMouseCursor",
         "drawCharPortrait", "triggerEventOnMouseButtonClick", "getAnimationLastPart", "initAnimStruct",
         "playAnimationPart", "setupBackgroundAnimationPart", "startBackgroundAnimation", "stopBackgroundAnimation",
         "loadBitmap", "loadLangFile", "loadSoundFile", "assignCustomSfx", "closeLevelShapeFile",
         "loadLevelShapes", "loadBlockProperties", "loadDoorShapes", "assignLevelDecorationShape",
         "resetBlockShapeAssignment", "allocItemPropertiesBuffer", "setScriptTextParameter", "checkMoney",
         "checkForCertainPartyMember", "checkPartyForItemType", "checkInventoryFull", "checkMonsterTypeHostility",
         "characterSkillTest", "battleHitSkillTest", "calcInflictableDamage", "calcInflictableDamagePerItem",
         "getInflictedDamage", "queueSpeech", "processDialogue", "playMusicTrack", "setMusicTrack"}


TEXT_ARGS = {0x6F: [1], 0x5E: [2], 0x7A: [0], 0x79: [0], 0x82: [2], 0x45: [1, 2, 3]}


def build(level, data_dir, items, lands):
    wll = L.level_member(level, "WLL", data_dir)
    area = struct.unpack_from("<H", wll, 0)[0]
    rec = {}
    for i in range((len(wll) - 2) // 12):
        o = 2 + i * 12
        rec[struct.unpack_from("<H", wll, o)[0]] = {"vmp": wll[o + 2], "shape": struct.unpack_from("<h", wll, o + 4)[0],
                                                    "special": wll[o + 6], "flags": wll[o + 8], "automap": wll[o + 10]}
    img = L.load_bitmap(L.level_member(level, "CMZ", data_dir))[2]
    ln = struct.unpack_from("<H", img, 4)[0]
    blocks = [tuple(img[6 + i * ln:10 + i * ln]) for i in range(1024)]
    used = {}
    for walls in blocks:
        for w in walls:
            used[w] = used.get(w, 0) + 1
    clickable = []
    for bi, walls in enumerate(blocks):
        for side, w in enumerate(walls):
            sp = rec.get(w, {}).get("special", 0)
            if sp:
                clickable.append((bi, side, w, sp))
    gfx = tileset_mapper.build(data_dir)[level]
    scripts = {}
    for ext in ("INI", "INF"):
        raw = L.level_member(level, ext, data_dir)
        if raw:
            s = E.read_script(raw)
            scripts[ext] = (s, calls_by_entry(s))
    legend = []
    xxx = L.level_member(level, "XXX", data_dir) or b""
    for i in range(min(len(xxx) // 12, 32)):
        sx, sy, sh, rx, ry, sid = struct.unpack_from("<6H", xxx, i * 12)
        name = T.decode_raw(lands[sid & 0x3FFF]).strip() if sid != 0xFFFF and sid & 0x4000 and (sid & 0x3FFF) < len(lands) else ""
        legend.append((sx, sy, sh, rx, ry, sid, name))
    return {"level": level, "area": area, "area_name": tileset_mapper.AREAS[area], "len": ln, "wll": rec,
            "used": used, "clickable": clickable, "gfx": gfx, "scripts": scripts, "legend": legend,
            "items": items}


def entry_label(e, ext="INF"):
    if ext == "INI":
        return f"INI entry {e} (runs when the level loads)"
    if e in SPECIAL_ENTRIES:
        return f"`{e:#05x}` {SPECIAL_ENTRIES[e]}"
    if e < 1024:
        return f"block {e} (x {e % 32}, y {e // 32})"
    return f"`{e:#x}`"


def events(mask, e, ext="INF"):
    if e >= 0x400 or ext == "INI":
        return "—"
    names = [n for b, n in EVENTS if mask & b]
    rest = mask & ~sum(b for b, _ in EVENTS) & 0xFFFF
    return ", ".join(names + ([f"bits {rest:#x} (no engine caller found)"] if rest else [])) or "none"


def render(r):
    lv = r["level"]
    o = [f"# Level {lv}", "",
         f"Made by `tools/level_report.py` from `LEVEL{lv}.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` ({EDITION}). "
         "How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), "
         "[emc2](../formats/emc2.md), [xxx](../formats/xxx.md).", ""]
    g = r["gfx"]["loadLevelGraphics"]
    o += ["## Size, area and graphics", "",
          f"- Map: 32 x 32 blocks, {r['len']} bytes per block in the CMZ.",
          f"- Area (WLL header): {r['area']} = {r['area_name']} (decorations `{r['area_name']}.SHP` / `.DAT`).",
          "- Wall tiles loaded by the scripts: " + "; ".join(
              f"{x['vcn_vmp']}" + (f" with palette {x['palette']}" if x["palette"] else "") + f" ({x['script']})" for x in g) + ".", ""]
    o += ["## Wall types used", "", "| Type | Count | VMP page | Shape | Special | Flags | Automap |", "|---|---|---|---|---|---|---|"]
    for w in sorted(r["used"]):
        p = r["wll"].get(w)
        if p is None:
            o.append(f"| {w} | {r['used'][w]} | not in this level's WLL ([Q11](../OPEN_QUESTIONS.md)) | | | | |")
        else:
            sp = f"{p['special']} {SPECIAL_WALLS.get(p['special'], '')}".strip() if p["special"] else ""
            o.append(f"| {w} | {r['used'][w]} | {p['vmp'] or '—'} | {p['shape'] if p['shape'] > 0 else '—'} | {sp} | {p['flags']:#04x} | {p['automap']} |")
    o += ["", "## Clickable walls", ""]
    if r["clickable"]:
        o += ["| Block | Side | Wall type | What it is |", "|---|---|---|---|"]
        for bi, side, w, sp in r["clickable"]:
            o.append(f"| {bi} (x {bi % 32}, y {bi // 32}) | {SIDES[side]} | {w} | {SPECIAL_WALLS.get(sp, sp)} |")
    else:
        o.append("None.")
    names = r["items"]
    placed_items, placed_mon, text_ids = [], [], set()
    o += ["", "## Script entry points", "",
          "**CONFIRMED.** The DATA word is the ORDR target in the named original script. "
          "Its event mask identifies when the engine can run it ([event sources](README.md#events)).",
          "",
          "Descriptions summarize calls found by a bounded static walk. Different calls can belong to different branches. "
          "`?` marks an argument the walk could not recover. `…` marks additional actions. "
          "The [EMC2 table](../emc2_scripts.md#lol1-system-functions) gives the native handler offsets "
          "and marks effects inferred from ScummVM **UNCONFIRMED** for DOS where applicable.", ""]
    for ext in ("INI", "INF"):
        if ext not in r["scripts"]:
            continue
        s, ent = r["scripts"][ext]
        text = s.strings
        words = {entry: word for word, entries in s.entries.items() for entry in entries}
        o += [f"### LEVEL{lv}.{ext}", "", "| Entry | DATA word | Events | What it can do |", "|---|---:|---|---|"]
        for e in sorted(ent):
            mask, calls = ent[e]
            o.append(f"| {entry_label(e, ext)} | `0x{words[e]:04X}` | {events(mask, e, ext)} | {describe(calls, text, names)} |")
            for fn, a in calls:
                if fn == 0x11 and a:
                    placed_items.append((ext, e, a))
                if fn == 0x38 and a:
                    placed_mon.append((ext, e, a))
                for k in TEXT_ARGS.get(fn, []):
                    if k < len(a) and a[k] is not None and a[k] != -1:
                        text_ids.add(a[k] & 0xFFFF)
        o.append("")
    o += ["## Items placed by the scripts", ""]
    if placed_items:
        o += ["| Script entry | Item type | Name | Level | Block |", "|---|---|---|---|---|"]
        for ext, e, a in placed_items:
            t = a[0]
            o.append(f"| {entry_label(e, ext)} | {t if t is not None else '?'} | {names.get(t, '?')} | "
                     f"{a[3] if len(a) > 3 and a[3] is not None else '?'} | {a[4] if len(a) > 4 and a[4] is not None else '?'} |")
    else:
        o.append("None by constant script calls.")
    o += ["", "## Monsters placed by the scripts", ""]
    if placed_mon:
        o += ["| Script entry | Block | Facing | Type slot | Mode |", "|---|---|---|---|---|"]
        for ext, e, a in placed_mon:
            f = lambda i: a[i] if len(a) > i and a[i] is not None else "?"
            o.append(f"| {entry_label(e, ext)} | {f(0)} | {f(3)} | {f(4)} | {f(6)} |")
    else:
        o.append("None by constant script calls.")
    o += ["", "## Automap legend", ""]
    if r["legend"]:
        o += ["| Symbol at | Symbol | Shown after exploring | Text id | Name |", "|---|---|---|---|---|"]
        for sx, sy, sh, rx, ry, sid, name in r["legend"]:
            o.append(f"| x {sx}, y {sy} | {sh} | x {rx}, y {ry} | {sid:#06x} | {name} |")
    else:
        o.append("No legend file entries.")
    glob_ids = sorted(i for i in text_ids if i & 0x4000)
    lev_ids = sorted(i for i in text_ids if not i & 0x4000)
    o += ["", "## Text shown by the scripts (ids only)", "",
          f"- Level text file `LEVEL{lv:02d}.<lang>`: {len(lev_ids)} ids: " + (", ".join(str(i) for i in lev_ids) or "none") + ".",
          f"- Global text `LANDS.<lang>`: {len(glob_ids)} ids: " + (", ".join(f'{i:#06x}' for i in glob_ids) or "none") + ".",
          "", "Read any of them with `tools/decode_dialogue.py LEVEL%02d.ENG --index N`." % lv, ""]
    return "\n".join(o), {"entries": sum(len(v[1]) for v in r["scripts"].values()), "items": len(placed_items),
                          "monsters": len(placed_mon), "text_ids": len(text_ids)}


INDEX = """# Level sheets

One page per level, written by `tools/level_report.py` from the level's own files (CD edition): map, wall table, automap legend and scripts. No game text is copied except the short names of items and automap places.

## How to read a sheet

- **Wall types used**: every wall type number in the map, how many block sides carry it, and its entry in the level's WLL table ([wll.md](../formats/wll.md)): VMP page (how it is drawn; — = nothing), decoration shape, special type, flags, automap symbol.
- **Clickable walls**: block sides whose wall type has a WLL *special* type: 1 clickable wall, 2 lever (to on), 3 lever (to off), 4 click runs the script only, 5 door or door switch (clicking it plays the door sound and runs the script), 6 niche (ScummVM `gui/gui_lol.cpp:1413-1440`). Clicking one runs the block's script with event 0x40.
- **Script entry points**: the level's scripts are entered by block number (0-1023) or by a special number: 0x400 level loaded, 0x401-0x403 script timers, 0x404 a monster died (`engines/kyra/script/script_lol.cpp:64-92`, `engines/kyra/engine/timer_lol.cpp:148`, `engines/kyra/engine/sprites_lol.cpp:203`). The description is built from the game functions the entry's code calls ([emc2_scripts.md](../emc2_scripts.md)), with constant arguments; `?` means the value is computed while the game runs.
- **Items and monsters placed**: calls of `createLevelItem` (0x11) and `initMonster` (0x38) with their arguments. Item names come from `ONETIME.INF` and `LANDS.ENG`.
- **Text ids**: the ids the scripts pass to message and dialogue functions; ids with bit 0x4000 are in `LANDS.<lang>`, others in the level's own text file.

## Events

| Bit | Event | Engine caller (ScummVM upstream) |
|-----|-------|----------------------------------|
| 0x0001 | party steps in | `engines/kyra/engine/scene_lol.cpp:665` |
| 0x0002 | party arrives (second movement path; also the `setNextFunc` script function) | `scene_lol.cpp:695`, `engines/kyra/engine/lol.cpp:947` |
| 0x0004 | party leaves | `scene_lol.cpp:664` |
| 0x0008 | party leaves (second path) | `scene_lol.cpp:694` |
| 0x0020 | a fireball ends in the block | `lol.cpp:2708` |
| 0x0040 | wall clicked | `engines/kyra/engine/scene_rpg.cpp:580`, `scene_lol.cpp:783`, `engines/kyra/gui/gui_lol.cpp:1446` |
| 0x0080 | item put down | `engines/kyra/engine/items_lol.cpp:374` |
| 0x0100 | item taken | `items_lol.cpp:382` |
| 0x0200 | a fireball passes | `lol.cpp:2577` |
| 0x0800 | a monster leaves the block | `engines/kyra/engine/sprites_lol.cpp:289` |
| 0x8000 | a thrown item hits | `items_lol.cpp:493` |

The difference between bits 1 and 2 (and 4 and 8) is the movement path that raises them; which player actions take which path is UNCONFIRMED.

## Levels

"""


EDITION = "CD edition"


def main():
    global EDITION
    ap = L.tool_args(__doc__, out_help="write all 29 sheets and an index to this folder")
    ap.add_argument("--level", type=int)
    ap.add_argument("--out-dir", dest="out", help=argparse.SUPPRESS)
    a = ap.parse_args()
    EDITION = "CD edition" if any(os.path.isfile(os.path.join(a.data, n)) for n in ("L01.PAK", "l01.pak")) else "floppy edition"
    items, lands = item_names(a.data)
    levels = [a.level] if a.level else list(range(1, 30))
    stats = {}
    pages = {}
    for lv in levels:
        text, st = render(build(lv, a.data, items, lands))
        pages[lv] = text
        stats[lv] = st
    if a.check:
        tot = {k: sum(s[k] for s in stats.values()) for k in ("entries", "items", "monsters", "text_ids")}
        print(f"CHECK level_report: {len(stats)} levels; {tot['entries']} script entries, {tot['items']} item "
              f"placements, {tot['monsters']} monster placements, {tot['text_ids']} text ids; every script decodes")
        return 0 if len(stats) == len(levels) else 1
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        rows = []
        for lv, text in pages.items():
            with open(os.path.join(a.out, f"level{lv:02d}.md"), "w") as f:
                f.write(text)
            s = stats[lv]
            rows.append(f"| [{lv}](level{lv:02d}.md) | {s['entries']} | {s['items']} | {s['monsters']} | {s['text_ids']} |")
        if not a.level:
            with open(os.path.join(a.out, "README.md"), "w") as f:
                f.write(INDEX + "| Level | Script entries | Items placed | Monsters placed | Text ids |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
        print(f"wrote {len(pages)} sheets to {a.out}")
        return 0
    for text in pages.values():
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
