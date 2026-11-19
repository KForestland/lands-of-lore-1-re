#!/usr/bin/env python3
"""Read LoL1 CMZ mazes, WLL walls, decoration DATs and ENG/FRE/GER string tables from the PAKs in --data and rebuild them byte for byte.

A CMZ is rebuilt from its parsed fields and the parsed Frame4 packets of the
original: byte-identical because those packet choices are kept
(lol1_compression_writer's encoder is decode-identical only). Level 24's five
extra bytes per block are kept verbatim, unparsed (meaning open, docs/unknowns/03).
An edited field that the packets no longer decode to is compressed afresh."""
from collections import Counter
from pathlib import Path
import struct

from cli_errors import run_cli
import dat_reader
from decode_dialogue import file_strings
from lol1_compression_writer import encode_frame4, verified_frame4
from lol1_script_writer import binary_strings, write_strings
import lol1lib as L
from wll_parser import parse_wll

WALL = struct.Struct("<HHhHHH")
DECORATION = struct.Struct("<10H10B10h10hBB")
LANGUAGES = {".ENG", ".FRE", ".GER"}


def parse_frame4(data):
    """Retain packet choices and bytes beyond the first end command."""
    packets = []
    cursor = 0
    while cursor < len(data):
        code = data[cursor]
        cursor += 1
        if code == 0x80:
            packets.append(("end",))
            break
        if code < 0x80:
            distance = (code & 15) << 8 | data[cursor]
            packets.append(("relative", (code >> 4) + 3, distance))
            cursor += 1
        elif code < 0xC0:
            length = code & 63
            if cursor + length > len(data):
                raise ValueError("truncated Frame4 literal")
            packets.append(("literal", data[cursor:cursor + length]))
            cursor += length
        elif code == 0xFE:
            length, value = struct.unpack_from("<HB", data, cursor)
            packets.append(("fill", length, value))
            cursor += 3
        elif code == 0xFF:
            length, offset = struct.unpack_from("<HH", data, cursor)
            packets.append(("long", length, offset))
            cursor += 4
        else:
            offset, = struct.unpack_from("<H", data, cursor)
            packets.append(("absolute", (code & 63) + 3, offset))
            cursor += 2
    return packets, data[cursor:]


def write_frame4(packets, tail):
    out = bytearray()
    for kind, *params in packets:
        if kind == "end":
            out.append(0x80)
        elif kind == "relative":
            length, distance = params
            out.extend((((length - 3) << 4) | (distance >> 8), distance & 255))
        elif kind == "literal":
            data, = params
            out.extend(bytes([0x80 | len(data)]) + data)
        elif kind == "fill":
            out.extend(struct.pack("<BHB", 0xFE, *params))
        elif kind == "long":
            out.extend(struct.pack("<BHH", 0xFF, *params))
        elif kind == "absolute":
            length, offset = params
            out.extend(struct.pack("<BH", 0xC0 | (length - 3), offset))
        else:
            raise ValueError("unknown Frame4 packet")
    return bytes(out) + tail


def parse_maze(blob):
    header, palette, raw = L.load_bitmap(blob)
    first, second, stride = struct.unpack_from("<3H", raw)
    if stride < 4 or len(raw) != 6 + 1024 * stride:
        raise ValueError("maze block stride does not tile its decoded payload")
    rows = [(tuple(raw[at:at + 4]), raw[at + 4:at + stride]) for at in range(6, len(raw), stride)]
    start = 10 + len(palette)
    storage = parse_frame4(blob[start:]) if header["comp_type"] == 4 else (None, blob[start + len(raw):])
    return header, palette, (first, second, stride), rows, storage


def write_maze(fields):
    header, palette, grid, rows, (packets, tail) = fields
    raw = struct.pack("<3H", *grid) + b"".join(bytes(walls) + unknown for walls, unknown in rows)
    size = header["size_field"]
    if packets is None:
        stored = raw + tail
    else:
        stored = write_frame4(packets, tail)
        if L.decode_frame4(stored, len(raw)) != raw:
            # An edited field: the original packet choices no longer fit, so
            # compress afresh (decode-identical, not the original bytes).
            stored = encode_frame4(raw)
            verified_frame4(stored, raw)
            stored += tail
            size = 8 + len(palette) + len(stored)
    return struct.pack("<HBBIH", size, header["comp_type"], header["byte3"], len(raw), len(palette)) + palette + stored


def replace_string(fields, index, text):
    """Replace one parsed string and move the offsets of the strings after it."""
    strings = list(fields["strings"])
    start = 2 * len(fields["offsets"]) + sum(len(s.encode("latin-1")) + 1 for s in strings[:index])
    shift = len(text.encode("latin-1")) - len(strings[index].encode("latin-1"))
    strings[index] = text
    offsets = [offset + shift if offset > start else offset for offset in fields["offsets"]]
    return {"offsets": offsets, "strings": strings}


def parse_walls(blob):
    return struct.unpack_from("<H", blob)[0], list(WALL.iter_unpack(blob[2:]))


def write_walls(fields):
    area, rows = fields
    return struct.pack("<H", area) + b"".join(WALL.pack(*row) for row in rows)


def write_decorations(rows):
    return struct.pack("<H", len(rows)) + b"".join(
        DECORATION.pack(*row["shapeIndex"], *row["scaleFlag"], *row["shapeX"], *row["shapeY"], row["next"], row["flags"])
        for row in rows)


def assets(root):
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and path.suffix.upper() == ".PAK":
            archive = path.read_bytes()
            for name, at, size in L.pak_entries(archive):
                yield f"{path.relative_to(root)}+{at:#x}/{name}", name.upper(), archive[at:at + size]


def check(data):
    counts = Counter()
    for where, name, blob in assets(Path(data)):
        suffix = Path(name).suffix
        try:
            if suffix == ".CMZ":
                rebuilt = write_maze(parse_maze(blob))
            elif suffix == ".WLL":
                rebuilt = write_walls(parse_walls(blob))
                if parse_wll(rebuilt) != parse_wll(blob):
                    raise ValueError("wall reader disagrees")
            elif suffix == ".DAT":
                _, rows = dat_reader.parse(blob)
                rebuilt = write_decorations(rows)
                if dat_reader.parse(rebuilt)[1] != rows:
                    raise ValueError("decoration reader disagrees")
            elif suffix in LANGUAGES:
                rebuilt = write_strings(binary_strings(blob, "<"), "<")
                if file_strings(rebuilt) != file_strings(blob):
                    raise ValueError("localized string reader disagrees")
            else:
                continue
            if rebuilt != blob:
                raise ValueError("original bytes differ")
        except (ValueError, IndexError, struct.error) as error:
            raise ValueError(f"{where}: {error}") from error
        counts[suffix] += 1
    if (counts[".CMZ"] != 29 or counts[".WLL"] != 29 or not counts[".DAT"] or counts[".ENG"] != 30
            or {counts[".FRE"], counts[".GER"]} - {0, 30}):
        raise ValueError("incomplete original level corpus")
    print(f"CHECK level fields write: {counts['.CMZ']} CMZ, {counts['.WLL']} WLL, {counts['.DAT']} decoration DAT, "
          f"{counts['.ENG']} ENG, {counts['.FRE']} FRE and {counts['.GER']} GER; byte-identical")


def main():
    parser = L.tool_args(__doc__, writes=False)
    args = parser.parse_args()
    if not args.check or args.pak:
        parser.error("give --check for the full DATA folder")
    check(args.data)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
