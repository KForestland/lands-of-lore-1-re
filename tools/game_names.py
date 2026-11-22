"""Names used by LoL1's automap and monster sprite loaders."""
from collections import defaultdict
from functools import lru_cache
from pathlib import PureWindowsPath
from struct import unpack_from

from decode_dialogue import decode_raw, file_strings
from emc2_decompile import read_script
from exe_tables import find_images
from level_report import calls_by_entry
from lol1lib import find_member, level_member


MAP_TITLES = {"cd": 0x287D0, "cdw": 0x28290, "floppy": 0x2A320}


def map_names(image, program, lands):
    # Word 0 is the sentinel. The other 29 words index the common text table.
    ids = unpack_from("<30H", program, MAP_TITLES[image])
    if ids[0] != 0xFFFF:
        return {}
    names = {}
    for level, sid in enumerate(ids[1:], 1):
        index = sid & 0x3FFF
        if sid >> 14 == 1 and index < len(lands):
            label = decode_raw(lands[index]).strip()
            if label:
                names[level] = label
    return names


@lru_cache(maxsize=1)
def level_names(data):
    images = find_images(data)
    if not images and data.name.upper() == "DATA":
        images = find_images(data.parent)
    if not images:
        return {}
    image, _, _, program = images[0]
    lands = file_strings(find_member("LANDS.ENG", data)[1])
    return map_names(image, program, lands)


def monster_sprites(data, level):
    """Match type and sprite slots only where the level supplies a unique name."""
    sprites = defaultdict(set)
    types = defaultdict(set)
    for extension in ("INI", "INF"):
        raw = level_member(level, extension, data)
        if raw is None:
            continue
        script = read_script(raw)
        for _, calls in calls_by_entry(script).values():
            for fn, args in calls:
                if len(args) < 2:
                    continue
                first, second = args[:2]
                if fn == 0x0B and second is not None:
                    label = ""
                    if first is not None and 0 <= first < len(script.strings):
                        label = PureWindowsPath(script.strings[first][1].decode("latin-1")).stem
                    sprites[second].add(label)
                if fn == 0x3F and first is not None:
                    types[first].add(None if second is None else second & 0xFF)
    names = {}
    for kind, slots in types.items():
        if len(slots) == 1:
            slot, = slots
            if len(sprites[slot]) == 1:
                label, = sprites[slot]
                if label:
                    names[kind] = label
    return names
