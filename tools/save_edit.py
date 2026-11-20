#!/usr/bin/env python3
"""Change one documented field in a new copy of an original LoL1 save; the save itself is only read."""
from pathlib import Path
import struct

from cli_errors import ReaderArgumentParser, run_cli
from modkit_core import output_path
import save_page
from save_reader import read_original_save

FIELDS = ("name", "block", "facing", "money", "lamp-oil")
# Fields a CD 1.02 edited-save run has shown the game loading (docs/savegame_format.md).
CONFIRMED = {"block", "facing", "lamp-oil"}
LAYOUTS = {b"CD04\0": (0x1427F, 0x254, 0x1D87), b".13\0_": (0x1426E, 0x249, 0x1D76)}


def name_bytes(value, width):
    try:
        raw = value.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("the name must use plain ASCII letters, digits and punctuation") from None
    if not raw or len(raw) >= width or not all(32 <= byte <= 126 for byte in raw):
        raise ValueError(f"the name must have 1 to {width - 1} printable ASCII characters")
    return raw + b"\0"


def integer(value, low, high):
    try:
        number = int(value, 16) if value.lower().startswith("0x") else int(value, 10)
    except ValueError:
        raise ValueError(f"the value must be a whole number from {low} to {high}, not {value!r}") from None
    if not low <= number <= high:
        raise ValueError(f"the value must be a whole number from {low} to {high}, not {number}")
    return number


def layout(raw):
    tag = raw[60:65]
    if tag not in LAYOUTS:
        raise ValueError("this is not an original LoL1 save (CD 1.02 or floppy .13 slot)")
    size, base, levels = LAYOUTS[tag]
    if size != len(raw) or (tag == b"CD04\0" and raw[65:76] not in (b"V CD1.02 D\0", b"V CD1.02 W\0")):
        raise ValueError("the save has the wrong size or version for an original CD 1.02 or floppy slot")
    mask, = struct.unpack_from("<I", raw, base + 553)
    for index in range(30):
        if mask & (1 << index):
            count, = struct.unpack_from("<I", raw, levels + index * 2500)
            if not 0 < count <= 2496:
                raise ValueError(f"the save is damaged: level {index + 1} does not fit its slot")
    return base


def shown(field, save):
    state = save["state"]
    return {"name": repr(save["description"]), "block": state["block"], "facing": state["facing"],
            "money": state["money"], "lamp-oil": state["lamp_oil"]}[field]


def edit(raw, field, value):
    """The edited copy and a line 'field old -> new'."""
    base = layout(raw)
    before = read_original_save(raw)
    result = bytearray(raw)
    expect = {}
    if field == "name":
        name = name_bytes(value, 60)
        result[:len(name)] = name
    elif field == "block":
        block = integer(value, 0, 1023)
        x = 256 * (block % 32) + 128
        y = 256 * (block // 32) + 128
        struct.pack_into("<3H", result, base, block, x, y)
        expect.update(block=block, x=x, y=y)
    elif field == "facing":
        facing = integer(value, 0, 3)
        struct.pack_into("<H", result, base + 15, facing)
        expect["facing"] = facing
    elif field == "money":
        money = integer(value, 0, 65535)
        struct.pack_into("<H", result, base + 528, money)
        expect["money"] = money
    elif field == "lamp-oil":
        oil = integer(value, 0, 100)
        effect = 2 * (3 - (oil - 1) // 25) if oil and before["state"]["brightness"] else 8
        result[base + 525:base + 527] = bytes([oil, effect])
        expect.update(lamp_oil=oil, lamp_effect=effect)
    else:
        raise ValueError(f"unknown field {field}; give one of {', '.join(FIELDS)}")
    changed = bytes(result)
    after = read_original_save(changed)
    old = shown(field, before)
    before["state"].update(expect)
    if field == "name":
        before["description"] = value
    if not after["size_ok"] or after != before:
        raise ValueError("the edited copy did not read back as requested; nothing was written")
    return changed, f"{field} {old} -> {shown(field, after)}"


def status(raw, field):
    if raw[60:65] != b"CD04\0":
        return ("UNCONFIRMED: no edited floppy save has been loaded by the game yet; "
                "keep a backup of your saves")
    if field in CONFIRMED:
        return "CONFIRMED: the CD 1.02 game loaded copies edited this way"
    return "UNCONFIRMED: no edited copy of this field has been loaded by the game yet; keep a backup of your saves"


def page_fields(raw):
    layout(raw)
    save = read_original_save(raw)
    state = save["state"]
    names = (("name", "Slot name", save["description"], 59),
             ("block", "Block", state["block"], 1023),
             ("facing", "Facing", state["facing"], 3),
             ("money", "Crowns", state["money"], 65535),
             ("lamp-oil", "Lamp oil", state["lamp_oil"], 100))
    facts = [("Edition", save.get("version_text", save["tag"])),
             ("Location (X / Y)", f'{state["x"]} / {state["y"]}'),
             ("Current level", state["level"]),
             ("Lamp brightness", state["brightness"]),
             ("Visited levels stored", len(save["levels"]))]
    return [(key, label, value, value, max_value, status(raw, key))
            for key, label, value, max_value in names], facts


def main():
    try:
        return run()
    except OSError as error:
        reason = (error.strerror or "the system refused").lower()
        raise ValueError(f"cannot use {error.filename or 'a file'}: {reason}") from None


def run():
    parser = ReaderArgumentParser(
        description=__doc__,
        epilog="Example: save_edit.py set \"/path/to/my saves/_SAVE001.DAT\" money 5000 --out \"my edited save.DAT\"")
    commands = parser.add_subparsers(dest="command", metavar="{page,set}")
    commands.required = True
    setter = commands.add_parser("set", help="write a copy of the save with one field changed",
                                 description="Write a copy of the save with one field changed.")
    setter.add_argument("save", type=Path, help="an original save file; only read")
    setter.add_argument("field", choices=FIELDS)
    setter.add_argument("value", help="the new value: a name, block 0-1023, facing 0-3, money 0-65535 or lamp oil 0-100")
    setter.add_argument("--out", required=True, type=Path, help="the new save file to write, outside the game and save folders")
    viewer = commands.add_parser("page", help="write an offline page for the save's documented fields")
    viewer.add_argument("save", type=Path, help="an original save file; only read")
    viewer.add_argument("--out", required=True, type=Path, help="a new .html file outside the game and save folders")
    args = parser.parse_args()
    if not args.save.is_file():
        raise ValueError(f"save not found: {args.save}")
    if args.command == "page":
        try:
            fields, facts = page_fields(args.save.read_bytes())
        except (struct.error, IndexError, KeyError, UnicodeError):
            raise ValueError("The save could not be read as an original LoL1 slot.") from None
        path = save_page.write(args.save, args.out, "LoL1", fields, facts)
        print(f"Wrote {path}. Open it in your browser.")
        return 0
    path = output_path(args.out, args.save.resolve().parent, args.save)
    if not path.parent.is_dir():
        raise ValueError(f"the folder {path.parent} does not exist; create it first or choose another place")
    raw = args.save.read_bytes()
    try:
        changed, change = edit(raw, args.field, args.value)
    except (struct.error, IndexError, KeyError, UnicodeError):
        raise ValueError("the save could not be read; it may be damaged or not an original LoL1 save") from None
    with path.open("xb") as target:
        target.write(changed)
    print(f"set: {change}; copy written to {path}; the original save was only read")
    print(status(raw, args.field))
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
