#!/usr/bin/env python3
"""Edit LoL1 text tables (decoded, code page 437) and EMC2/AVFS listings in separate copies."""
from pathlib import Path
from struct import error as StructError
from copy import deepcopy
import sys

from cli_errors import run_cli
from decode_dialogue import decode_string1, decode_string2, encode_string
from lol1_level_writer import LANGUAGES, replace_string
from lol1_pak_writer import write_pak
from lol1_script_writer import assemble, binary_strings, listing, write_strings
from lol1lib import pak_entries
import modkit_core as core

GAME = "lol1"
FOLDER = "the LoL1 folder holding GENERAL.PAK (the CD DATA folder or the floppy game folder)"
DATA_ENV = "LOL1_DATA"
DEFINITIONS = {
    0x0E: (10, {0: "item ID", 3: "equip code", 4: "script entry", 5: "might",
                6: "category", 7: "protection"}),
    0x3F: (42, {0: "creature slot", 1: "shape", 2: "hit factor", 26: "base HP",
                35: "attack chance", 36: "attack type"}),
}


def sources(root):
    return core.game_files(root, {".PAK"})


def is_loose(name):
    return False


def members(raw):
    return [(key, at, raw[at:at + size]) for key, at, size in pak_entries(raw)]


def repack(rows, _resize, _size):
    return write_pak((key, payload) for key, _, payload in rows)


def annotate(source):
    for chunk in source["chunks"]:
        if (chunk["tag"], source["form"]) != ("DATA", "EMC2"):
            continue
        rows = chunk["fields"]
        for i, row in enumerate(rows):
            if row.get("opcode") != 14 or row["argument"] not in DEFINITIONS:
                continue
            count, fields = DEFINITIONS[row["argument"]]
            args = rows[max(0, i - count):i][::-1]
            if len(args) == count and all(arg.get("opcode") in (3, 4) for arg in args):
                for index, title in fields.items():
                    args[index]["definition_field"] = title
    return source


def decode_text(stored):
    return decode_string2(decode_string1(stored.encode("latin-1"))).decode("cp437")


def view(_name, key, payload):
    if Path(key).suffix.upper() in LANGUAGES:
        return "text", [decode_text(s) for s in binary_strings(payload, "<")["strings"]]
    if payload[:4] == b"FORM" and payload[8:12] in (b"EMC2", b"AVFS"):
        try:
            script = listing(payload)
            if assemble(script) == payload:
                return "script", annotate(script)
        except (ValueError, KeyError, IndexError, StructError):
            return None
    return None


def encode(_name, _key, payload, kind, value):
    if kind == "text":
        fields = binary_strings(payload, "<")
        for index, text in enumerate(core.text_fields(len(fields["strings"]), value)):
            # The game stores the text bigram-compressed; edits are plain text.
            text = encode_string(text.encode("cp437")).decode("latin-1")
            old = fields["strings"][index]
            if old != text:
                start = 2 * len(fields["offsets"]) + sum(len(s) + 1 for s in fields["strings"][:index])
                if len(old) != len(text) and any(start < at <= start + len(old) for at in fields["offsets"]):
                    raise ValueError("cannot resize a string with an interior directory reference")
                fields = replace_string(fields, index, text)
        return write_strings(fields, "<")
    value = deepcopy(value)
    for chunk in value["chunks"]:
        if chunk["tag"] == "DATA" and value["form"] == "EMC2":
            chunk["fields"] = [{k: v for k, v in row.items() if k != "definition_field"}
                               for row in chunk["fields"]]
    return assemble(value)


if __name__ == "__main__":
    raise SystemExit(run_cli(core.main, sys.modules[__name__]))
