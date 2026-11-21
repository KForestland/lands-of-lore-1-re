#!/usr/bin/env python3
"""Print numeric tables from the original LoL1 executable and EMC2 definitions."""
from pathlib import Path

from cli_errors import run_cli
import emc2_decompile as emc
import exe_tables
from level_report import simulate
import lol1lib

PAGE = Path(__file__).resolve().parents[1] / "docs" / "NUMBERS.md"


def definitions(raw, function, arity):
    """Read the consecutive constant-producing instructions at each definition call."""
    script = emc.read_script(raw)
    instructions = script.instructions
    object.__setattr__(script, "_addr_index", {row.address: i for i, row in enumerate(instructions)})
    for index, row in enumerate(instructions):
        if (row.opcode, row.argument) != (14, function):
            continue
        start = index
        while start and instructions[start - 1].opcode in (3, 4, 16, 17):
            start -= 1
        [(_, values)] = simulate(script, instructions[start].address - 1, row.address + 1)
        if len(values) != arity or None in values:
            raise ValueError(f"nonconstant definition call {function:#x} at DATA word {row.address:#x}")
        yield script.chunks[b"DATA"][0] + 2 * row.address, values


def table(columns, rows):
    heading = "| " + " | ".join(columns) + " |"
    rule = "|" + "|".join("---" for _ in columns) + "|"
    return "\n".join([heading, rule] + ["| " + " | ".join(map(str, row)) + " |" for row in rows])


def matrix(values):
    return " / ".join(map(str, values))


def render(data):
    images = [(kind, label, image) for kind, label, _, image in exe_tables.find_images(data) if kind != "cdw"]
    if len(images) != 1:
        raise ValueError("expected one CD or floppy MAIN.EXE")
    kind, label, image = images[0]
    xp = exe_tables.OFFSETS["xp"][kind]
    magic = exe_tables.OFFSETS["spells"][kind]
    setup, one_time = lol1lib.find_member("ONETIME.INF", data)
    setup = setup.upper() if setup is not None else "loose"
    items = list(definitions(one_time, 0x0E, 10))
    if sorted(v[0] for _, v in items) != list(range(285)):
        raise ValueError("item definitions do not cover IDs 0–284")
    monster_sources = [("ITEM.INF", lol1lib.find_member("ITEM.INF", data)[1])]
    for level in range(1, 30):
        for extension in ("INI", "INF"):
            monster_sources.append((f"LEVEL{level}.{extension}", lol1lib.level_member(level, extension, data)))
    monsters = [(name, offset, row) for name, raw in monster_sources if raw
                for offset, row in definitions(raw, 0x3F, 42)]
    if len(monsters) != 79:
        raise ValueError("expected 79 static monster definitions")
    xp_rows = [(level, value, f"`+0x{xp+4*level:X}`")
               for level, value in enumerate(exe_tables.words(image, xp, 11, "I"))]
    spells = exe_tables.spells(image, magic)
    spell_rows = [(i, f"`{row['name id']:#06x}`", matrix(row["MP"]), matrix(row["HP"]), f"`+0x{magic+28*i:X}`")
                  for i, row in enumerate(spells)]
    item_rows = []
    for offset, row in sorted(items, key=lambda entry: entry[1][0]):
        item, _, _, equipment, entry, might, category, protection, _, _ = row
        might = (might + 128) % 256 - 128
        nominal = f"2–{2*might}" if might > 0 else "—"
        item_rows.append((item, equipment, entry, might, category, protection & 255, nominal, f"`+0x{offset:X}`"))
    monster_rows = [(name, f"`+0x{offset:X}`", row[0], row[1],
                     row[26],
                     row[2], matrix(row[9:17]), row[35], row[36])
                    for name, offset, row in monsters]

    return "\n\n".join([
        "# LoL1 numbers at a glance",
        f"Generated from the {label} and script data by `tools/lol1_numbers.py`. The spell and experience rows come from `MAIN.EXE`. The game fills the item and creature banks from EMC2 calls. [Executable tables](executable_tables.md)",
        "## Experience by current skill level",
        "The engine compares the cumulative total at the current skill index and advances on meeting the threshold. The table shows the stored comparison value. See the CD callback at `MAIN.EXE+0x41190` or the floppy one at `+0x4A310`. [Experience rules](game_rules.md#experience-and-skills)",
        table(("Current level", "Cumulative XP threshold", "MAIN.EXE offset"), xp_rows),
        "## Spell costs by rank",
        "Each 28-byte record has four MP words at +0x02 and four HP words at +0x0E. Columns are in rank order. Zero-filled records and the Vortex cost row are shown as stored. [Spell effect table](unknowns/07_native_rules.md#casting)",
        table(("Slot", "Name ID", "MP", "HP", "MAIN.EXE offset"), spell_rows),
        "## Item might and armour",
        f"`{setup}/ONETIME.INF` syscall 0x0E supplies signed might and unsigned protection (record +0x08 and +0x0A, CD setter `MAIN.EXE+0x4A6C3–0x4A6CD`, floppy `+0x53C97–0x53CA1`). The nominal range treats the listed positive might as the sides of the standard two-dice roll. Actual damage depends on the item script, hit test, other equipment and target factors. Armour is the stored item contribution. [Damage rules](game_rules.md#might-armour-and-damage)",
        table(("Item", "Equip code", "Script entry", "Might", "Category", "Armour", "Nominal 2d range", "ONETIME.INF offset"), item_rows),
        "## Creature definitions by level",
        "Rows are separate 0x3F calls, including the item script and definitions repeated later in a level. Hit factor is the argument as a percentage. The eight might-category values are the stored attack inputs. Base HP is argument 26. A new monster gets `floor(base HP × difficulty row 1 / 256)` (CD factors 102, 256 and 384, floppy 192, 256 and 384 for easy, normal and hard), then `floor(result × (192 + 1d128) / 256)`, and 1 if the signed result is not above 0; CD skips the second multiply for type 2 on level 12 (CD `MAIN.EXE+0x14740–0x147B1`, floppy `+0x190D8–0x19139`). Attack chance and attack type are arguments 35 and 36; what each attack type does is in the [attack type table](game_rules.md#monster-attack-and-defense-types). [Spawn HP](unknowns/07_native_rules.md#monster-transitions) · [Native records](unknowns/18_native_records.md#monster-definition)",
        table(("Script", "Offset", "Slot", "Shape", "Base HP", "Hit %", "Might by category", "Attack chance", "[Attack type](game_rules.md#monster-attack-and-defense-types)"), monster_rows),
    ]) + "\n"


def main():
    parser = lol1lib.tool_args(__doc__, out_help="write the generated Markdown page")
    args = parser.parse_args()
    if args.pak or (args.check and args.out):
        parser.error("use the full game folder and choose at most one of --check and --out")
    page = render(args.data)
    if args.check:
        if lol1lib.is_cd_layout(args.data):
            if PAGE.read_text(encoding="utf-8") != page:
                raise ValueError("docs/NUMBERS.md differs from the CD tables")
            print("CHECK numbers: CD tables match docs/NUMBERS.md")
        else:
            print("CHECK numbers: floppy tables render; docs/NUMBERS.md is the CD reference")
    elif args.out:
        Path(args.out).write_text(page, encoding="utf-8")
    else:
        print(page, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
