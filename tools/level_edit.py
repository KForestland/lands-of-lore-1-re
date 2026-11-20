#!/usr/bin/env python3
"""Apply changes made on a LoL1 level plan and verify the copied archives."""
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
import os
from pathlib import Path
import struct
from tempfile import TemporaryDirectory

from cli_errors import ReaderArgumentParser, run_cli
import emc2_decompile as emc
from level_html import counted, find_data
from level_report import item_names
from lol1_level_writer import parse_maze, parse_walls, write_maze
import lol1lib as game
import modkit
import patch
from modkit_core import digest, output_folder, replace_members, write_json

FORMAT = "lol1-level-changes-1"
EXTENSIONS = ("CMZ", "WLL", "INI", "INF")
SPECIAL = {1: "Clickable shape", 2: "Next wall on click", 3: "Previous wall on click",
           4: "Click event", 5: "Door switch", 6: "Item niche"}


@dataclass(frozen=True)
class Placement:
    site: int
    block_word: int
    args: tuple


def placement_sites(script, level):
    """Literal, same-level createLevelItem calls in INI entry 1."""
    header = next((at for at, entries in script.entries.items() if 1 in entries), None)
    if header is None:
        raise ValueError("This level has no initialization entry 1 for item placements.")
    end = min((at for at in script.entries if at > header), default=len(script.words))
    rows = [ins for ins in script.instructions if header < ins.address < end]
    if (not rows or (rows[-1].opcode, rows[-1].argument) != (8, 1)
            or any((ins.opcode, ins.argument) == (8, 1) or ins.opcode == 18 for ins in rows[:-1])):
        raise ValueError("This level's initialization entry has an unfamiliar return.")
    targets = {ins.target for ins in script.instructions}
    placements = {}
    for i, ins in enumerate(rows):
        if (ins.opcode, ins.argument) != (14, 0x11) or i < 8 or i + 1 == len(rows):
            continue
        pushes = rows[i - 8:i]
        cleanup = rows[i + 1]
        if ((cleanup.opcode, cleanup.argument) != (12, 8)
                or any(op.opcode not in (3, 4) for op in pushes)
                or any(op.address in targets for op in rows[i - 7:i + 2])):
            continue
        args = tuple(op.argument for op in reversed(pushes))
        if args[3] == level and 0 <= args[4] < 1024:
            placements[ins.address] = Placement(ins.address, pushes[3].address, args)
    return placements, rows[-1].address


def level_sources(data, level):
    preferred = f"L{level:02d}.PAK"
    for extension in EXTENSIONS:
        name = f"LEVEL{level}.{extension}"
        for pak in (preferred, None):
            try:
                archive, raw = game.find_member(name, data, pak)
            except FileNotFoundError:
                continue
            if archive is None:
                raise ValueError(f"{name} sits outside a PAK. Use a copy with the original level archives.")
            yield extension, (archive, name, raw)
            break
        else:
            raise ValueError(f"{name} is missing. Give --data the complete game folder or its DATA folder.")


def monsters(script):
    """The last five pushes to initMonster hold its location, facing and type."""
    rows = script.instructions
    targets = {ins.target for ins in rows} | set(script.entries)
    found = {}
    for i, ins in enumerate(rows):
        if (ins.opcode, ins.argument) != (14, 0x38) or i < 5 or i + 1 == len(rows):
            continue
        cleanup = rows[i + 1]
        if cleanup.opcode != 12 or cleanup.argument not in range(8, 12):
            continue
        if any(push.opcode not in (3, 4) for push in rows[i - 5:i]):
            continue
        if any(op.address in targets for op in rows[i - 4:i + 1]):
            continue
        pushes = rows[i - 5:i][::-1]
        block, x, y, facing, kind = args = tuple(op.argument for op in pushes)
        if 0 <= block < 1024 and 0 <= x < 256 and 0 <= y < 256 and 0 <= facing < 4:
            found[ins.address] = args, tuple(op.address for op in pushes)
    return found


def monster_types(script):
    rows = script.instructions
    return sorted({arg.argument for arg, call in zip(rows, rows[1:])
                   if (call.opcode, call.argument) == (14, 0x3F)
                   and arg.opcode in (3, 4) and 0 <= arg.argument <= 4})


def door_states(rows):
    table = {row[0]: row for row in rows if row[0] <= 255}
    states = {}
    for wall, row in table.items():
        if row[4] & 0x38 != 0x28:
            continue
        for at in range(wall + 1, min(wall + 6, 256)):
            following = table.get(at)
            if not following or following[1:4] != row[1:4] or not following[4] & 8:
                break
            if following[4] & 0x30:
                if following[4] & 0x30 == 0x10:
                    for frame in range(wall, at + 1):
                        states[frame] = [wall, at]
                break
    return states


def edit_monsters(raw, replacements, changes, types):
    script = emc.read_script(raw)
    sites = monsters(script)
    expected = {site: args for site, (args, _) in sites.items()}
    seen = set()
    for site, values in pairs(changes, "monster change"):
        if type(site) is not int or site not in sites or site in seen:
            raise ValueError("A monster placement was repeated or is unavailable in this script.")
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError("A monster change needs square, X, Y, facing and type.")
        seen.add(site)
        for value, hi, name in zip(values, (1023, 255, 255, 3, 4), ("square", "X", "Y", "facing", "type")):
            integer(value, 0, hi, f"Monster {name} must be between 0 and {hi}.")
        old, words = sites[site]
        if values[4] != old[4] and values[4] not in types:
            raise ValueError("Choose a monster type defined by this level.")
        expected[site] = tuple(values)
        for word, before, after in zip(words, old, values):
            if before != after:
                replacements[word] = push(after)
    return Counter(expected.values()), sum(expected[site] != args for site, (args, _) in sites.items())


def wall_name(row):
    ident, vmp, shape, special, flags, _ = row
    if special & 255 in SPECIAL:
        label = SPECIAL[special & 255]
    elif flags & 0x08:
        label = "Door side"
    else:
        label = f"Wall graphic {vmp & 255}" if vmp & 255 else "No wall graphic"
    if flags & 8:
        state = {0x10: "open", 0x20: "closed"}.get(flags & 0x30, "moving frame")
        label += f", {state}"
    if shape > 0:
        label += f", decoration {shape}"
    return f"{ident} · {label}"


def editor_data(sources, level, names):
    blobs = {key: row[2] for key, row in sources.items()}
    ini = emc.read_script(blobs["INI"])
    sites, _ = placement_sites(ini, level)
    wall_rows = parse_walls(blobs["WLL"])[1]
    return {
        "format": FORMAT,
        "level": level,
        "source": {key: digest(raw) for key, raw in blobs.items()},
        "types": [[row[0], wall_name(row), bool(row[1] & 255), row[2] > 0, row[4]]
                  for row in wall_rows if row[0] <= 255],
        "doors": door_states(wall_rows),
        "monsters": [[extension, site, *args] for extension in ("INI", "INF")
                     for site, (args, _) in monsters(emc.read_script(blobs[extension])).items()],
        "monster_types": monster_types(ini),
        "squares": [walls for walls, _ in parse_maze(blobs["CMZ"])[3]],
        "items": [[site, p.args[0], *p.args[4:8]] for site, p in sites.items()],
        "names": sorted(names.items(), key=lambda pair: (pair[1].casefold(), pair[0])),
    }


def push(value):
    if -128 <= value <= 127:
        return [0x4400 | (value & 255)]
    return [0x2300, value & 65535]


def add_item(level, item, block):
    args = (item, 0, 0, level, block, 128, 128, 0)
    return [word for value in reversed(args) for word in push(value)] + [0x4E11, 0x4C08]


def script_write(raw, script, replacements):
    """Relocate stored branch targets and ORDR entries using instruction boundaries."""
    if not replacements:
        return raw
    words = []
    at_map = {}
    starts = sorted((*script.entries, *(ins.address for ins in script.instructions), len(script.words)))
    for at, end in zip(starts, starts[1:]):
        at_map[at] = len(words)
        words.extend(replacements.get(at, script.words[at:end]))
    if len(words) >= 0x8000:
        raise ValueError("Too many edits for the script address range. Apply fewer placements.")
    for ins in script.instructions:
        if ins.target is None:
            continue
        at = at_map[ins.address]
        target = at_map[ins.target]
        if ins.opcode == 0 and words[at] & 0x8000:
            words[at] = 0x8000 | target
        elif ins.opcode == 15 and words[at] & 0x6000 == 0x2000:
            words[at + 1] = (words[at + 1] & 0x8000) | target
        else:
            raise ValueError("The script has an unfamiliar branch encoding.")
    sections = {
        b"ORDR": [at_map.get(value, value) for value in emc.be_words(script.chunks[b"ORDR"][1])],
        b"DATA": words,
    }
    body = bytearray(b"EMC2")
    for tag, (start, payload) in script.chunks.items():
        if tag in sections:
            values = sections[tag]
            data = struct.pack(f">{len(values)}H", *values)
            body.extend(struct.pack(">4sI", tag, len(data)) + data)
        else:
            body.extend(raw[start - 8:start + len(payload) + (len(payload) & 1)])
    bias = len(raw) - struct.unpack_from(">I", raw, 4)[0]
    return b"FORM" + struct.pack(">I", 8 + len(body) - bias) + body


def integer(value, low, high, message):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(message)
    return value


def pairs(rows, label):
    for row in rows:
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError(f"Each {label} must contain two values. Export the change file again.")
        yield row


def changed_maze(raw, wall_blob, changes):
    header, palette, grid, original, packets = parse_maze(raw)
    types = {row[0] for row in parse_walls(wall_blob)[1]}
    rows = list(original)
    seen = set()
    for block, sides in pairs(changes, "square change"):
        integer(block, 0, 1023, "The square number must be between 0 and 1023.")
        if block in seen or not isinstance(sides, list) or len(sides) != 4:
            raise ValueError(f"Square {block} needs one North, East, South and West wall list.")
        seen.add(block)
        walls, tail = original[block]
        for old, new in zip(walls, sides):
            integer(new, 0, 255, "A wall type must be between 0 and 255.")
            if new != old and new not in types:
                raise ValueError(f"Wall type {new} is missing from this level's wall list.")
        rows[block] = tuple(sides), tail
    if rows == original:
        return raw, rows, 0
    edited = write_maze((header, palette, grid, rows, packets))
    return edited, rows, sum(a != b for a, b in zip(original, rows))


def changed_script(raw, level, changes, additions, names, replacements=None):
    script = emc.read_script(raw)
    sites, end = placement_sites(script, level)
    expected = {site: p.args for site, p in sites.items()}
    replacements = {} if replacements is None else replacements.copy()
    seen = set()
    prior = len(replacements)
    for site, block in pairs(changes, "item change"):
        integer(site, 0, 32767, "An item placement address must be a whole number.")
        p = sites.get(site)
        if p is None or site in seen:
            raise ValueError(f"Item placement at word {site} is unavailable or repeated.")
        seen.add(site)
        if block is None:
            # Discard the creation call and leave the original argument cleanup in place.
            replacements[site] = [0x0100] if not script.words[site] & 0x2000 else [0x2100, 0]
            del expected[site]
        else:
            integer(block, 0, 1023, "The square number must be between 0 and 1023.")
            if block != p.args[4]:
                replacements[p.block_word] = push(block)
                expected[site] = (*p.args[:4], block, *p.args[5:])
    extra, added = [], []
    for item, block in pairs(additions, "new item"):
        integer(item, 0, 32767, "The item type must be a whole number from the item list.")
        integer(block, 0, 1023, "The square number must be between 0 and 1023.")
        if item not in names:
            raise ValueError(f"Item type {item} is missing from this edition's item list.")
        extra.extend(add_item(level, item, block))
        added.append((item, 0, 0, level, block, 128, 128, 0))
    if extra:
        replacements[end] = [0x0200, *extra, 0x0800, script.words[end]]
    return script_write(raw, script, replacements), Counter([*expected.values(), *added]), len(replacements) - prior - bool(extra) + len(added)


def validate_document(document, source, level):
    base = {"format", "level", "source", "walls", "items", "add"}
    has_monsters = "monsters" in document
    if (set(document) != (base | {"monsters"} if has_monsters else base)
            or document["format"] != FORMAT or document["level"] != level
            or any(not isinstance(document[key], list) for key in ("walls", "items", "add"))
            or has_monsters and not isinstance(document["monsters"], dict)):
        raise ValueError("Give a level change file exported by the LoL1 editor.")
    keys = source if has_monsters else base_source(source)
    if document["source"] != {key: digest(row[2]) for key, row in keys.items()}:
        raise ValueError("This change file came from different level files. Open a plan from this copy and export again.")


def base_source(source):
    return {key: row for key, row in source.items() if key != "INF"}


def apply(data, document, output, *protected, share=False):
    if not isinstance(document, dict):
        raise ValueError("Give a level change file exported by the LoL1 editor.")
    level = integer(document.get("level"), 1, 29, "The change file needs a level number between 1 and 29.")
    source = dict(level_sources(data, level))
    validate_document(document, source, level)
    cmz, rows, wall_count = changed_maze(source["CMZ"][2], source["WLL"][2], document["walls"])
    names = item_names(data)[0] if document["add"] else {}
    edits = document.get("monsters", {})
    if set(edits) - {"INI", "INF"} or any(not isinstance(rows, list) for rows in edits.values()):
        raise ValueError("Monster edits must be lists grouped under INI or INF.")
    repl = {"INI": {}, "INF": {}}
    allowed = monster_types(emc.read_script(source["INI"][2]))
    expected, monster_count = {}, 0
    for extension in ("INI", "INF"):
        expected[extension], count = edit_monsters(source[extension][2], repl[extension], edits.get(extension, []), allowed)
        monster_count += count
    ini, items, item_count = changed_script(source["INI"][2], level, document["items"], document["add"], names, repl["INI"])
    inf = script_write(source["INF"][2], emc.read_script(source["INF"][2]), repl["INF"])

    by_archive = defaultdict(dict)
    updates = [("CMZ", cmz), ("INI", ini)]
    if repl["INF"]:
        updates.append(("INF", inf))
    for extension, value in updates:
        archive, name, _ = source[extension]
        by_archive[archive][name] = value
    with output_folder(output, data, *protected) as stage:
        verified = {}
        for name, updates in sorted(by_archive.items()):
            original = (data / name).read_bytes()
            members = modkit.members(original)
            indices = {i: updates[key] for i, (key, _, _) in enumerate(members) if key in updates}
            if len(indices) != len(updates):
                raise ValueError(f"{name} does not contain one copy of each requested level member.")
            rebuilt = replace_members(modkit, name, original, members, indices)
            path = stage / name
            path.write_bytes(rebuilt)
            reread = modkit.members(path.read_bytes())
            if ([(key, value) for key, _, value in reread] !=
                    [(key, indices.get(i, value)) for i, (key, _, value) in enumerate(members)]):
                raise ValueError(f"{name} did not read back as the requested archive.")
            verified.update({key: value for key, _, value in reread if key in updates})
        if (parse_maze(verified[source["CMZ"][1]])[3] != rows
                or Counter(p.args for p in placement_sites(emc.read_script(verified[source["INI"][1]]), level)[0].values()) != items):
            raise ValueError("The copied level does not read back as the requested changes.")
        for extension in ("INI", "INF"):
            raw = verified.get(source[extension][1], source[extension][2])
            if Counter(args for args, _ in monsters(emc.read_script(raw)).values()) != expected[extension]:
                raise ValueError(f"The copied {extension} does not read back as the requested monster placements.")
        if share and (wall_count or item_count or monster_count):
            title = f"Level {level} edits"
            try:
                shareable = patch.make(data, stage, title, "Walls, items or monsters edited on a LoL1 level plan.", kind="data")
                _, files, undo = patch.prepare(data, shareable)
            except patch.PatchLimitError as error:
                raise ValueError(f"{error}. Apply without --patch to write the copied archives, or export smaller edits.") from None
            if any(raw != (stage / name).read_bytes() for name, raw in files.items()):
                raise ValueError("The level patch did not reproduce the copied archive.")
            write_json(stage / "level-patch.json", shareable)
            write_json(stage / patch.UNDO, undo)
    return level, len(by_archive), wall_count, item_count + monster_count


def check(data):
    names = item_names(data)[0]
    sites_count = monster_levels = door_levels = 0
    with TemporaryDirectory(prefix="lol-level-edit-check-") as tmp:
        folder = Path(tmp)
        for level in range(1, 30):
            source = dict(level_sources(data, level))
            model = editor_data(source, level, names)
            example = {key: model[key] for key in ("format", "level", "source")}
            original = {**example, "walls": [], "items": [], "add": [], "monsters": {}}
            unchanged = folder / f"same-{level}"
            apply(data, original, unchanged)
            if any(raw.read_bytes() != (data / raw.name).read_bytes() for raw in unchanged.iterdir()):
                raise ValueError(f"Level {level} did not copy byte-identically without edits.")
            block = 629
            sides = list(model["squares"][block])
            sides[0] = next(row[0] for row in model["types"] if row[0] != sides[0])
            sites = model["items"]
            sites_count += len(sites)
            edits = []
            if sites:
                edits.append([sites[0][0], (sites[0][2] + 500) % 1024])
            if len(sites) > 1:
                edits.append([sites[1][0], None])
            changed = {**example, "walls": [[block, sides]], "items": edits, "add": [[121, block]], "monsters": {}}
            apply(data, changed, folder / f"edit-{level}", share=True)
            if model["monsters"]:
                extension, site, block, x, y, facing, kind = model["monsters"][0]
                values = [(block + 32) % 1024, x, y, (facing + 1) % 4, kind]
                monster_levels += 1
                apply(data, {**original, "monsters": {extension: [[site, values]]}}, folder / f"monster-{level}")
            flags = {row[0]: row[4] for row in model["types"]}
            for square, faces in enumerate(model["squares"]):
                side = 0 if flags.get(faces[0], 0) & 8 else 1
                endpoints = model["doors"].get(faces[side])
                if endpoints and faces[side] == faces[side ^ 2]:
                    door_levels += 1
                    faces = list(faces)
                    new = endpoints[0] if faces[side] == endpoints[1] else endpoints[1]
                    faces[side] = faces[side ^ 2] = new
                    apply(data, {**original, "walls": [[square, faces]]}, folder / f"door-{level}")
                    break
    if not door_levels or not monster_levels:
        raise ValueError("No door or monster fixture was checked.")
    print(f"CHECK level editor: 29 unchanged levels copy byte-identically. "
          f"29 edited levels read back, share and undo exactly. {sites_count} editable item placements. "
          f"{door_levels} door and {monster_levels} monster copies verified.")
    return 0


def read_changes(path):
    if not path.is_file():
        raise ValueError(f"The change file {path} is missing. Download changes from the level plan and give that file.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        raise ValueError(f"The change file {path} is not readable JSON. Download changes from the level plan again.") from None


def main():
    parser = ReaderArgumentParser(description=__doc__)
    parser.add_argument("changes", nargs="?", help="change file exported from the level plan")
    data = os.environ.get("LOL1_DATA")
    parser.add_argument("--data", default=data, required=data is None,
                        help="your game folder or its DATA folder (default: $LOL1_DATA)")
    parser.add_argument("--out", help="new output folder outside the game")
    parser.add_argument("--patch", action="store_true", help="also write a shareable patch and its undo")
    parser.add_argument("--check", action="store_true", help="verify all 29 levels using temporary copies")
    args = parser.parse_args()
    if args.check and (args.changes or args.out or args.patch):
        parser.error("Use --check with only --data.")
    if not args.check and not (args.changes and args.out):
        parser.error("Give the downloaded change file and a new --out folder, or use --check.")
    data = find_data(args.data, "DATA", "GENERAL.PAK")
    if args.check:
        return check(data)
    protected = patch.protected(args.data, data)
    level, archives, walls, items = apply(data, read_changes(Path(args.changes)), args.out, *protected, share=args.patch)
    extra = " Patch and undo included." if args.patch and (walls or items) else ""
    print(f"Level {level}: verified {counted(archives, 'archive')}, {counted(walls, 'square edit')} "
          f"and {counted(items, 'placement edit')} in {args.out}.{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
