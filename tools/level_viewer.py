#!/usr/bin/env python3
"""Write interactive LoL1 map pages from your original PAK archives."""
from base64 import b64encode
from collections import defaultdict
from functools import lru_cache
from importlib import import_module
from io import BytesIO
from struct import iter_unpack

from cli_errors import run_cli
from game_names import level_names, monster_sprites
import decode_dialogue as text
import emc2_decompile as emc
from level_edit import editor_data, level_sources
from level_editor_ui import sections
from level_html import Plan, main
from level_renderer import level_blocks, level_numbers, render_schematic
from level_report import calls_by_entry, entry_label, events, item_names
from lol1_progression import collect
from lol1lib import level_member


def levels(_data, selection):
    import_module("PIL.Image")
    return [f"level{i:02d}" for i in level_numbers(selection)]


def progression(data, selected):
    exits, _, _ = collect(data, [int(stem[5:]) for stem in selected])
    rows = defaultdict(list)
    for row in exits:
        rows[f"level{row['level']:02d}"].append(row)
    return rows


def spot(block, dx=.5, dy=.5):
    return block % 32 + dx, block // 32 + dy


def map_block(value):
    return type(value) is int and 0 <= value < 1024


@lru_cache(maxsize=1)
def names(data):
    return item_names(data)


def argument(values, i):
    return values[i] if i < len(values) and values[i] is not None else "computed"


def place(plan, level, ext, entry, calls, items, counts, edit_sites, monster_sites, monster_markers, sprites):
    for function, args, site in calls:
        layer = ""
        if function == 0x11:
            item, destination, block = (argument(args, i) for i in (0, 3, 4))
            kind = "Items"
            info = {"Item type": item, "Name": items.get(item, "Unknown"), "Level": destination, "Block": block}
            on_map = map_block(block) and destination == level
            editable = ext == "INI" and entry == 1 and site in edit_sites
            layer = "editable-item" if editable else "read-only-item"
            info["Editor"] = "Editable initial placement" if editable else "Read-only script placement"
            color, prefix, x, y = "#79e3c8", "I", .68, .30
        elif function == 0x38:
            block = argument(args, 0)
            kind = "Monsters"
            info = {"Block": block, "Facing": argument(args, 3), "Type slot": argument(args, 4),
                    "Mode": argument(args, 6)}
            if sprite := sprites.get(info["Type slot"]):
                info["Sprite name"] = sprite
            on_map = map_block(block)
            editable = (ext, site) in monster_sites
            layer = "editable-monster" if editable else "read-only-item"
            info["Editor"] = "Editable placement" if editable else "Read-only script placement"
            info["Inside square X / Y"] = f"{argument(args, 1)} / {argument(args, 2)}"
            color, prefix, x, y = "#ffadbb", "M", .68, .68
        else:
            continue
        counts[kind] += 1
        slot = counts[kind]
        key = f"{prefix}-{slot}"
        if layer == "editable-monster":
            monster_markers[key] = f"{ext}:{site}"
        label = f"{kind[:-1]} placement {slot}"
        if function == 0x11 and info["Name"] != "Unknown":
            label = f"{info['Name']} — item placement {slot}"
        if function == 0x38 and "Sprite name" in info:
            label = f"{info['Sprite name']} — creature placement {slot}"
        info["Script entry"] = f"LEVEL{level}.{ext} entry {entry}"
        plan.legend[kind] = color
        if on_map:
            plan.dot(spot(block, x, y), key, label, kind, info, color, f"{prefix}{slot}", layer=layer)
        else:
            plan.note(key, label, kind, info)


def view(data, stem, gates):
    level = int(stem[5:])
    titles = level_names(data)
    title = titles.get(level, f"Level {level}")
    plan = Plan(f"{title} plan", [(0, 0), (32, 32)],
                f"The wall map comes from LEVEL{level}.CMZ and WLL. Markers show entries in the stored scripts and map symbols.",
                north_up=False)
    plan.legend.update({"Open square": "#ebe8dc", "Solid square": "#282830",
                        "Squares with some walls": "#e69632", "Decorated face": "#c81e1e",
                        "Exit square": "var(--exit)"})

    picture = BytesIO()
    render_schematic(level, data).save(picture, format="PNG")
    image = b64encode(picture.getvalue()).decode("ascii")
    x, y = plan.point((0, 0))
    width = plan.scale * 32
    plan.shapes.append(f'<image x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" height="{width:.3f}" '
                       f'style="image-rendering:pixelated" href="data:image/png;base64,{image}"/>')

    linked = defaultdict(list)
    for gate in gates:
        for block in gate["entry_ids"]:
            if map_block(block):
                destination = gate["args"][0]
                label = titles.get(destination, f"level {destination}")
                linked[block].append(f"To {label}: {gate['conditions']}")
    for block, walls in enumerate(level_blocks(level, data)):
        x, y = spot(block, 0, 0)
        details = {"X / Y": f"{x} / {y}", "Wall types N / E / S / W": " / ".join(map(str, walls)),
                   "Source": f"LEVEL{level}.CMZ, decoded block {block}"}
        if block in linked:
            details["Exit conditions"] = " • ".join(linked[block])
        plan.polygon(((x, y), (x+1, y), (x+1, y+1), (x, y+1)), f"block-{block}", f"Square {block}",
                     "Squares", details, "cell exit-region" if block in linked else "cell")

    items, lands = names(data)
    sprites = monster_sprites(data, level)
    model = editor_data(dict(level_sources(data, level)), level, items)
    edit_sites = {site for site, *_ in model["items"]}
    monster_sites = {(extension, site) for extension, site, *_ in model["monsters"]}
    model["monster_markers"] = {}
    counts = defaultdict(int)
    for ext in ("INI", "INF"):
        raw = level_member(level, ext, data)
        if not raw:
            continue
        script = emc.read_script(raw)
        addresses = {entry: word for word, entries in script.entries.items() for entry in entries}
        for entry, (mask, calls) in sorted(calls_by_entry(script, with_sites=True).items()):
            key = f"{ext}-{entry}"
            label = f"{ext} entry {entry}"
            details = {"Entry": entry_label(entry, ext).replace("`", ""), "Events": events(mask, entry, ext),
                       "Source": f"LEVEL{level}.{ext}, DATA word {addresses[entry]:#x}"}
            if ext == "INF" and map_block(entry):
                plan.dot(spot(entry, .25, .72), key, label, "Script entries", details, "#aabdfa", entry)
            else:
                plan.note(key, label, "Script entries", details)
            place(plan, level, ext, entry, calls, items, counts, edit_sites, monster_sites, model["monster_markers"], sprites)

    legend = level_member(level, "XXX", data) or b""
    for i, (x, y, shape, rx, ry, sid) in enumerate(iter_unpack("<6H", legend[:32*12]), 1):
        index = sid & 0x3fff
        name = text.decode_raw(lands[index]).strip() if sid != 0xffff and sid & 0x4000 and index < len(lands) else ""
        plan.dot((x + .24, y + .27), f"legend-{i}", name or f"Legend {i}", "Automap legend",
                 {"Symbol": shape, "Square X / Y": f"{x} / {y}", "Shown after exploring": f"{rx} / {ry}",
                  "Text ID": f"{sid:#06x}", "Source": f"LEVEL{level}.XXX +{(i-1)*12:#x}"}, "#fdd381", f"L{i}")

    for i, row in enumerate(gates, 1):
        level_to, block, facing = row["args"]
        source = next((entry for entry in row["entry_ids"] if map_block(entry)), None)
        destination = titles.get(level_to, f"level {level_to}")
        plan.note(f"exit-{i}", f"Exit {i} to {destination}", "Exits",
                  {"Gate": row["conditions"], "Event": row["event"], "Entries": row["entries"],
                   "Destination square / facing": f"{block} / {facing}", "DATA word": f"{row['word']:#x}"},
                  target=f"block-{source}" if source is not None else None)
    plan.edit_controls, plan.edit_script = sections(model, plan)
    return plan


if __name__ == "__main__":
    raise SystemExit(run_cli(main, __doc__, "DATA", "GENERAL.PAK", "1", levels, view, progression))
