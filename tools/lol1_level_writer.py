#!/usr/bin/env python3
"""Read LoL1 CMZ mazes, WLL walls, decoration DATs and ENG/FRE/GER string tables from the PAKs in --data and rebuild them byte for byte.

A CMZ is rebuilt from its parsed fields and the parsed Frame4 packets of the
original: byte-identical because those packet choices are kept
(lol1_compression_writer's encoder is decode-identical only). Level 24's five
extra bytes per block are kept verbatim, unparsed (meaning open, docs/unknowns/03).
Edited wall fields keep the packets that still decode to the intended bytes."""
from collections import Counter
from itertools import groupby
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


def copy_packet(at, source, length):
    distance = at - source
    if length <= 10 and 0 < distance <= 0xFFF:
        return ("relative", length, distance)
    if length <= 64:
        return ("absolute", length, source)
    return ("long", length, source)


def update_frame4(packets, raw):
    """Keep the original packets that still decode to the requested bytes."""
    result = bytearray()
    at = 0
    for packet in packets:
        kind, *params = packet
        if kind == "end":
            break
        length = len(params[0]) if kind == "literal" else params[0]
        part = raw[at:at + length]
        if kind == "literal":
            result.extend(write_frame4([("literal", part)], b""))
        else:
            source = at - params[1] if kind == "relative" else params[1]
            reference = bytes([params[1]]) * length if kind == "fill" else raw[source:source + length]
            if reference == part:
                result.extend(write_frame4([packet], b""))
            else:
                other = raw.find(part, 0, at + length - 1) if length >= 3 else -1
                if 0 <= other < at:
                    result.extend(write_frame4([copy_packet(at, other, length)], b""))
                else:
                    start = 0
                    for same, run in groupby(a == b for a, b in zip(part, reference)):
                        width = sum(1 for _ in run)
                        if same and kind != "fill" and width >= 3:
                            kept = copy_packet(at + start, source + start, width)
                            result.extend(write_frame4([kept], b""))
                        else:
                            result.extend(encode_frame4(part[start:start + width])[:-1])
                        start += width
        at += length
    result.append(0x80)
    return bytes(result)


def write_maze(fields):
    header, palette, grid, rows, (packets, tail) = fields
    raw = struct.pack("<3H", *grid) + b"".join(bytes(walls) + unknown for walls, unknown in rows)
    size = header["size_field"]
    if packets is None:
        stored = raw + tail
    else:
        stored = write_frame4(packets, tail)
        if L.decode_frame4(stored, len(raw)) != raw:
            stored = update_frame4(packets, raw)
            verified_frame4(stored, raw)
            stored += tail
            size = 8 + len(palette) + len(stored)
    return struct.pack("<HBBIH", size, header["comp_type"], header["byte3"], len(raw), len(palette)) + palette + stored


def validate_maze_edit(original, edited):
    """Only decoded wall bytes may differ. Frame4 packet choices can change."""
    def unchanged_fields(raw):
        header, palette, grid, rows, (_, tail) = parse_maze(raw)
        if header["size_field"] != len(raw) - 2:
            raise ValueError("The CMZ size field disagrees with its length.")
        stable = (raw[2:10], palette, grid, tuple(extra for _, extra in rows), tail)
        return stable, tuple(walls for walls, _ in rows)

    before, walls = unchanged_fields(original)
    after, new_walls = unchanged_fields(edited)
    if before != after or walls == new_walls:
        raise ValueError("The CMZ patch must change only the four wall types per square.")


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
    reference = L.repo_json("dialogue_summary.json", str(data))
    expected_text = (Counter(Path(row["file"]).suffix for row in reference["files"])
                     if reference else Counter({".ENG": 30}))
    if counts[".CMZ"] != 29 or counts[".WLL"] != 29 or not counts[".DAT"]:
        raise ValueError("incomplete original level corpus")
    for suffix in expected_text.keys() | LANGUAGES:
        if counts[suffix] != expected_text[suffix]:
            raise ValueError(f"{suffix}: rebuilt {counts[suffix]} of {expected_text[suffix]} expected text tables")
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
