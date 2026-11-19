#!/usr/bin/env python3
"""Read LoL1 bitmap, WSA and SHP payloads and prove read-back in memory."""
from collections import Counter
from pathlib import Path
import re
import struct

from cli_errors import run_cli
from decode_frame4 import decode_frame4 as independent_frame4
import lol1lib as L
from shp_renderer import read_shp, shape_offsets, unwrap
from wsa_extract import delta_xor, frames, parse

FILL = re.compile(rb"(.)\1{5,}", re.DOTALL)
ZERO = re.compile(rb"\0{4,}")
BITMAPS = {".cps", ".cmz", ".vcn", ".vmp"}
FORMATS = BITMAPS | {".wsa", ".shp"}


def encode_frame4(data):
    """Use native literals, fills and the end command."""
    stream = bytearray()

    def literals(start, end):
        for offset in range(start, end, 63):
            part = data[offset:min(offset + 63, end)]
            stream.append(0x80 | len(part))
            stream.extend(part)

    start = 0
    for match in FILL.finditer(data):
        literals(start, match.start())
        remaining = len(match[0])
        while remaining:
            length = min(0xFFFF, remaining)
            stream.extend(struct.pack("<BHB", 0xFE, length, match[0][0]))
            remaining -= length
        start = match.end()
    literals(start, len(data))
    stream.append(0x80)
    return bytes(stream)


def encode_frame4_matches(data):
    """Use back-references when a small on-disk length field needs them."""
    stream = bytearray()
    literals = bytearray()
    recent = {}
    early = {}
    fills = iter(FILL.finditer(data))
    fill = next(fills, None)
    pos = 0

    def flush():
        if literals:
            stream.append(0x80 | len(literals))
            stream.extend(literals)
            literals.clear()

    while pos < len(data):
        while fill is not None and pos >= fill.end():
            fill = next(fills, None)
        repeat = min(0xFFFF, fill.end() - pos) if fill and fill.start() <= pos else 0
        length, source = 0, 0
        key = data[pos:pos + 4]
        if len(key) == 4:
            for previous in (recent.get(key), early.get(key)):
                if previous is None:
                    continue
                limit = min(0xFFFF, len(data) - pos) if previous <= 0xFFFF else 10 if pos - previous <= 0xFFF else 0
                if limit < 4:
                    continue
                size = 4
                while size < limit and pos + size < len(data) and data[previous + size] == data[pos + size]:
                    size += 1
                if size > length:
                    length, source = size, previous
        if repeat >= max(6, length):
            flush()
            stream.extend(struct.pack("<BHB", 0xFE, repeat, data[pos]))
            length = repeat
        elif length:
            flush()
            distance = pos - source
            if length <= 10 and distance <= 0xFFF:
                stream.extend((((length - 3) << 4) | (distance >> 8), distance & 0xFF))
            elif length <= 64:
                stream.extend(struct.pack("<BH", 0xC0 | (length - 3), source))
            else:
                stream.extend(struct.pack("<BHH", 0xFF, length, source))
        else:
            literals.append(data[pos])
            if len(literals) == 63:
                flush()
            length = 1
        for i in range(pos, min(pos + length, len(data) - 3)):
            key = data[i:i + 4]
            recent[key] = i
            if i <= 0xFFFF:
                early.setdefault(key, i)
        pos += length
    flush()
    stream.append(0x80)
    return bytes(stream)


def verified_frame4(encoded, decoded):
    # Read with capacity beyond the payload to exercise the end command.
    capacity = len(decoded) + 1
    if L.decode_frame4(encoded, capacity) != decoded or independent_frame4(encoded, capacity) != decoded:
        raise ValueError("Frame4 encoder changed the decoded bytes")


def checked_frame4(decoded, counts):
    encoded = encode_frame4(decoded)
    verified_frame4(encoded, decoded)
    counts["frame4"] += 1
    return encoded


def encode_delta(before, after):
    """Write an XOR delta with native long literal and skip commands."""
    if len(before) != len(after):
        raise ValueError("WSA pictures need the same dimensions")
    mask = bytes(a ^ b for a, b in zip(before, after))
    stream = bytearray()

    def literals(out, start, end):
        for offset in range(start, end, 0x3FFF):
            part = mask[offset:min(offset + 0x3FFF, end)]
            if len(part) < 128:
                out.append(len(part))
            else:
                out.extend(struct.pack("<BH", 0x80, 0x8000 | len(part)))
            out.extend(part)

    start = 0
    for match in ZERO.finditer(mask):
        literals(stream, start, match.start())
        start = match.end()
        # The end command can leave the unchanged suffix implicit.
        if start == len(mask):
            break
        remaining = len(match[0])
        while remaining:
            count = min(0x7FFF, remaining)
            if count < 128:
                stream.append(0x80 | count)
            else:
                stream.extend(struct.pack("<BH", 0x80, count))
            remaining -= count
    literals(stream, start, len(mask))
    # Dense masks can always be represented as one sequence of long literals.
    if len(stream) > len(mask) + 3 * ((len(mask) + 0x3FFE) // 0x3FFF):
        stream.clear()
        literals(stream, 0, len(mask))
    return bytes(stream) + b"\x80\0\0"


def encode_shape_lines(pixels, width, height, mapping=None):
    """Write one nonzero code per coloured pixel and zero runs per scanline."""
    if len(pixels) != width * height:
        raise ValueError("SHP pixel length differs from its dimensions")
    mapping = mapping or b""
    codes = {mapping[index] if index < len(mapping) else index: index
             for index in range(255, 0, -1)}
    packed = bytearray()
    for y in range(height):
        row = pixels[y * width:(y + 1) * width]
        at = 0
        for match in re.finditer(rb"\0+", row):
            packed.extend(codes[pixel] for pixel in row[at:match.start()])
            count = len(match[0])
            while count:
                skip = min(255, count)
                packed.extend((0, skip))
                count -= skip
            at = match.end()
        packed.extend(codes[pixel] for pixel in row[at:])
    return bytes(packed)


def write_bitmap(original, counts, pixels=None):
    header, palette, decoded = L.load_bitmap(original)
    if len(decoded) != header["uncompressed_size"]:
        raise ValueError("short bitmap payload")
    compressed = header["comp_type"] == 4
    if compressed and pixels is None:
        counts["frame4"] += 1
    decoded = decoded if pixels is None else pixels
    payload = encode_frame4(decoded) if compressed else decoded
    if compressed and 8 + len(palette) + len(payload) > 0xFFFF:
        payload = encode_frame4_matches(decoded)
    if compressed:
        verified_frame4(payload, decoded)
    size = 8 + len(palette) + len(payload)
    rebuilt = struct.pack("<HBBIH", size, header["comp_type"], header["byte3"], len(decoded), len(palette))
    rebuilt += palette + payload
    _, new_palette, new_pixels = L.load_bitmap(rebuilt)
    if (new_palette, new_pixels) != (palette, decoded):
        raise ValueError("rebuilt bitmap read-back differs")
    return rebuilt


def write_wsa(original, counts):
    info = parse(original)
    n = info["frames"]
    raw_offsets = struct.unpack_from(f"<{n + 2}I", original, 14)
    prefix_size = 14 + 4 * (n + 2)
    base = info["offsets"][0]
    old_picture = bytearray(info["width"] * info["height"])
    new_picture = bytearray(old_picture)
    chunks = bytearray()
    offsets = []
    buffer_size = info["delta_buffer"]
    for i in range(n + 1):
        at = raw_offsets[i]
        if not at:
            if i != 0:
                raise ValueError("a noninitial WSA delta has no offset")
            offsets.append(0)
            continue
        offsets.append(base + len(chunks))
        start = info["data_start"] + at - base
        end = info["data_start"] + raw_offsets[i + 1] - base if raw_offsets[i + 1] else len(original)
        # A WSA without a closing delta places the last visible frame's
        # end offset at EOF and leaves the final directory word zero.
        if i == n and start == end == len(original):
            continue
        if not info["data_start"] <= start < end <= len(original):
            raise ValueError("WSA delta span does not fit in the file")
        delta = L.decode_frame4(original[start:end], info["delta_buffer"])
        checked_frame4(delta, counts)
        if not delta_xor(old_picture, delta, len(old_picture)):
            raise ValueError("original WSA delta did not finish cleanly")
        encoded = encode_delta(new_picture, old_picture)
        buffer_size = max(buffer_size, len(encoded))
        wrapped = encode_frame4(encoded)
        if not delta_xor(new_picture, L.decode_frame4(wrapped, len(encoded) + 1), len(new_picture)):
            raise ValueError("rebuilt WSA delta did not finish cleanly")
        if old_picture != new_picture:
            raise ValueError("rebuilt WSA delta changed the frame")
        chunks.extend(wrapped)
        counts["wsa deltas"] += 1
    offsets.append(base + len(chunks) if raw_offsets[-1] else 0)
    header = bytearray(original[:14])
    struct.pack_into("<H", header, 10, buffer_size)
    rebuilt = bytes(header) + struct.pack(f"<{n + 2}I", *offsets) + original[prefix_size:info["data_start"]] + chunks
    if list(frames(original, info)) != list(frames(rebuilt)):
        raise ValueError("rebuilt WSA picture differs through the public reader")
    return rebuilt


def write_shp(original, counts):
    data = unwrap(original)
    if data is not original:
        checked_frame4(data, counts)
    originals = read_shp(original)
    count = len(originals)
    directory = bytearray(struct.pack("<H", count))
    body = bytearray()
    for offset, shape in zip(shape_offsets(data), originals):
        if shape is None:
            directory.extend(struct.pack("<I", 0))
            continue
        if not shape["exact"]:
            raise ValueError("original SHP shape does not finish on its last scanline")
        at = offset + 2
        flags, height, width, height2, size, expanded = struct.unpack_from("<HBHBHH", data, at)
        start = at + 10
        table_size = data[start] if flags & 4 else 16
        table_start = start + bool(flags & 4)
        pos = table_start + (table_size if flags & 1 else 0)
        mapping = data[table_start:pos]
        if not flags & 2:
            lines = L.decode_frame4(data[pos:at + size], expanded)
            if len(lines) != expanded:
                raise ValueError("short original SHP Frame4 payload")
            checked_frame4(lines, counts)
        encoded = encode_shape_lines(shape["pixels"], width, height, mapping)
        payload = encoded if flags & 2 else encode_frame4(encoded)
        if not flags & 2 and len(payload) > at + size - pos:
            alternate = encode_frame4_matches(encoded)
            if len(alternate) < len(payload):
                payload = alternate
        directory.extend(struct.pack("<I", count * 4 + len(body)))
        body.extend(struct.pack("<HBHBHH", flags, height, width, height2, 10 + pos - start + len(payload), len(encoded)))
        body.extend(data[start:pos])
        body.extend(payload)
        counts["shapes"] += 1
    rebuilt = bytes(directory + body)
    if data is not original:
        rebuilt = write_bitmap(original, counts, pixels=rebuilt)
    rebuilt_shapes = read_shp(rebuilt)
    if len(rebuilt_shapes) != len(originals):
        raise ValueError("rebuilt SHP has a different shape count")
    for old, new in zip(originals, rebuilt_shapes):
        if old is None or new is None:
            if old != new:
                raise ValueError("rebuilt SHP changed an empty slot")
        elif any(old[k] != new[k] for k in ("width", "height", "height2", "flags", "pixels", "exact")):
            raise ValueError("rebuilt SHP changed a shape")
    return rebuilt


def members(root):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in FORMATS:
            yield str(path.relative_to(root)), suffix, path.read_bytes()
        elif suffix == ".pak":
            data = path.read_bytes()
            for name, at, size in L.pak_entries(data):
                extension = Path(name).suffix.lower()
                if extension in FORMATS:
                    yield f"{path.relative_to(root)}+{at:#x}/{name}", extension, data[at:at + size]


def check(data):
    counts = Counter()
    exact = Counter()
    for name, extension, original in members(Path(data)):
        writer = write_bitmap if extension in BITMAPS else write_wsa if extension == ".wsa" else write_shp
        try:
            rebuilt = writer(original, counts)
        except (ValueError, IndexError, struct.error) as error:
            raise ValueError(f"{name}: {error}") from error
        counts[extension] += 1
        exact[extension] += rebuilt == original
    if not all(counts[extension] for extension in FORMATS):
        raise ValueError("one or more bitmap, WSA or SHP formats are absent")
    files = sum(counts[extension] for extension in FORMATS)
    print(f"CHECK compression write: {files} files ({', '.join(f'{counts[e]} {e}' for e in sorted(FORMATS))}); "
          f"{counts['frame4']} source Frame4 streams, {counts['wsa deltas']} WSA deltas and {counts['shapes']} SHP shapes "
          f"read back identically; {sum(exact.values())} files byte-identical")


def main():
    parser = L.tool_args(__doc__, writes=False)
    args = parser.parse_args()
    if not args.check or args.pak:
        parser.error("give --check for the full data folder")
    check(args.data)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
