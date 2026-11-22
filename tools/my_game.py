"""Make an offline guide from a player's copy of Lands of Lore."""
from collections import defaultdict

from cli_errors import game_path, input_path
from decode_dialogue import decode_raw, file_strings
from edition import identify, WITNESSES
from emc2_decompile import read_script
from exe_tables import find_images, OFFSETS, spells
from game_names import map_names, monster_sprites
from level_html import find_data
from level_renderer import level_numbers, render_schematic
from level_report import calls_by_entry, item_names
from lol1lib import find_member, level_member
from my_game_ui import LanguageError, MyGame, catalogue, edition_label, png_bytes, report


TITLE = "Lands of Lore · My Game"
LANGUAGES = {"ENG": "English", "FRE": "French", "GER": "German"}
MAP_LEGEND = """
<ul class="legend" aria-label="Map legend">
<li><span style="background:#ebe8dc"></span>Open square</li>
<li><span style="background:#282830"></span>Solid wall</li>
<li><span style="background:#e69632"></span>Partial wall, door or switch</li>
<li><span style="background:#c81e1e"></span>Decoration</li>
</ul>
"""


def game_data(folder):
    folder = input_path(folder).resolve()
    if folder.name.upper() in LANGUAGES and folder.parent.name.upper() == "DATA":
        return find_data(folder.parent, "DATA", "GENERAL.PAK")
    return find_data(folder, "DATA", "GENERAL.PAK")


def language_tables(data):
    tables = {}
    for code in LANGUAGES:
        for directory in (data, game_path(data, code)):
            if not directory.is_dir():
                continue
            try:
                _, raw = find_member("LANDS." + code, directory)
            except FileNotFoundError:
                continue
            tables[code] = file_strings(raw)
            break
    return tables


def language_options(folder, tables=None):
    folder = input_path(folder).resolve()
    data = game_data(folder)
    if tables is None:
        tables = language_tables(data)
    if folder.name.upper() in tables:
        code = folder.name.upper()
        return {code: LANGUAGES[code]}
    candidates = {code: LANGUAGES[code] for code in tables}
    if len(candidates) > 1:
        # A localized CD launcher copied to the install folder identifies its language.
        witnesses = WITNESSES["English CD 1.02"]
        _, found = identify(data)
        for code in candidates:
            witness = witnesses.get(f"{code}/LANDS.EXE")
            if witness and found.get("LANDS.EXE") == witness:
                return {code: LANGUAGES[code]}
    return candidates


def spell_rows(lands, image, program):
    for slot, record in enumerate(spells(program, OFFSETS["spells"][image])):
        sid = record["name id"]
        index = sid & 0x3FFF
        if sid >> 14 != 1 or index >= len(lands):
            continue
        name = decode_raw(lands[index]).strip()
        if name:
            yield name, slot, " / ".join(map(str, record["MP"])), " / ".join(map(str, record["HP"]))


def item_records(data, levels, titles):
    locations = defaultdict(set)
    for level in levels:
        for extension, kind in (("INI", "Level setup"), ("INF", "Level event")):
            raw = level_member(level, extension, data)
            if raw is None:
                continue
            for entry, (_, calls) in calls_by_entry(read_script(raw)).items():
                for function, args in calls:
                    if function == 0x11 and len(args) >= 5:
                        item, target, square = args[0], args[3], args[4]
                        if target not in levels or square is None or not 0 <= square < 1024:
                            continue
                        row, column = divmod(square, 32)
                        detail = f"Floor row {row + 1}, column {column + 1} ({kind.lower()} {entry})"
                        locations[item].add((titles.get(target, f"Level {target}"), detail))
                    elif function == 0x4C and args:
                        locations[args[0]].add((titles.get(level, f"Level {level}"), f"Pack grant ({kind.lower()} {entry})"))
    setup = read_script(find_member("ONETIME.INF", data)[1])
    for entry, (_, calls) in calls_by_entry(setup).items():
        for function, args in calls:
            if function == 0x4C and args:
                locations[args[0]].add(("Game setup", f"Pack grant (setup record {entry})"))
    return locations


def game_page(folder, language=None):
    data = game_data(folder)
    images = find_images(data)
    if not images and data.name.upper() == "DATA":
        images = find_images(data.parent)
    if not images:
        raise ValueError("missing program")
    image, _, _, program = images[0]
    layout = "Floppy" if image == "floppy" else "CD"
    edition = edition_label(data, identify, WITNESSES, f"{layout} edition layout (exact version unverified)")
    text = language_tables(data)
    if language is None:
        language = next(iter(language_options(folder, text)), None)
    if language not in text:
        if language is not None:
            raise LanguageError(f"The selected folder has no {LANGUAGES[language]} name table.")
        raise ValueError("missing name tables")
    lands = text[language]
    items, _ = item_names(data, lands)
    items = {key: name for key, name in items.items()
             if name and not name.startswith("string 0x")
             and not (name.startswith("[") and name.endswith("]"))}
    spell_list = list(spell_rows(lands, image, program))
    if not items or not spell_list:
        raise ValueError("missing named items or spells")
    levels = level_numbers("all")
    titles = map_names(image, program, lands)
    maps = ((level, titles.get(level, f"Level {level}"), png_bytes(render_schematic(level, data)), "png")
            for level in levels)
    creatures = ((name, titles.get(level, f"Level {level}"), slot)
                 for level in levels for slot, name in sorted(monster_sprites(data, level).items()))
    item_list = sorted(items.items(), key=lambda row: row[1].casefold())
    tables = (
        ("items", "Items", catalogue("items", "Items", ("Name", "Item ID"), ((name, key) for key, name in item_list))),
        ("spells", "Spells", catalogue("spells", "Spells", ("Name", "Slot", "MP by rank", "HP by rank"), spell_list)),
        ("creatures", "Creatures", catalogue("creatures", "Creatures", ("Sprite name", "Area", "Type"), creatures,
                                             "These labels come from the stored creature sprites.")),
    )
    locations = item_records(data, levels, titles)
    heading = "Where is it?"
    rows = ((name, area, record) for key, name in item_list for area, record in
            (sorted(locations[key]) or [("—", "No directly named placement or grant found.")]))
    found = catalogue("where", heading, ("Item", "Area", "Record"), rows,
                      "From direct placements and pack grants in the game scripts. Some depend on what you do in play.")
    note = f"Level, item and spell names are from the {LANGUAGES[language]} text table in your game."
    return report(TITLE, edition, maps, tables, legend=MAP_LEGEND, note=note, extras=(("where", heading, found),))


app = MyGame("LoL1 My Game", TITLE, "Lands of Lore", "DATA", game_page, tuple(LANGUAGES), language_options)
main = app.main
write_page = app.write_page


if __name__ == "__main__":
    raise SystemExit(main())
