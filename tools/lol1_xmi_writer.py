#!/usr/bin/env python3
"""Reconstruct original XMIDI chunks and stored events without a MIDI conversion."""
from collections import Counter
from pathlib import Path
import struct

from cli_errors import run_cli
import lol1lib as L
from xmi_to_midi import vlq, wvlq

CHUNK = struct.Struct(">4sI")
CONTAINERS = {b"FORM", b"CAT "}


def read_quantity(raw, at):
    value, end = vlq(raw, at)
    return (value, end - at), end


def write_quantity(field):
    value, width = field
    body = wvlq(value)
    if len(body) > width:
        raise ValueError("value no longer fits the stored VLQ width")
    return b"\x80" * (width - len(body)) + body


def read_events(raw):
    rows, at = [], 0
    while at < len(raw):
        start = at
        while at < len(raw) and raw[at] < 0x80:
            at += 1
        if at == len(raw):
            break
        delay, status = list(raw[start:at]), raw[at]
        at += 1
        kind = status >> 4
        row = dict(delay=delay, status=status)
        if kind in (8, 9, 10, 11, 12, 13, 14):
            size = 1 if kind in (12, 13) else 2
            if at + size > len(raw):
                raise ValueError(f"short channel event at EVNT+{at:#x}")
            row["data"] = list(raw[at:at + size])
            at += size
            if kind == 9:
                row["duration"], at = read_quantity(raw, at)
        elif status in (0xF0, 0xF7, 0xFF):
            if status == 0xFF:
                row["type"] = raw[at]
                at += 1
            (size, width), at = read_quantity(raw, at)
            if at + size > len(raw):
                raise ValueError(f"short system event at EVNT+{at:#x}")
            row.update(data=raw[at:at + size], size_width=width)
            at += size
        else:
            raise ValueError(f"unrecognized event {status:#x} at EVNT+{at - 1:#x}")
        rows.append(row)
        if row.get("type") == 0x2F:
            return rows, raw[at:]
    raise ValueError("EVNT without end-of-track marker")


def write_events(rows, tail):
    out = bytearray()
    for row in rows:
        status = row["status"]
        out.extend(row["delay"])
        out.append(status)
        if status == 0xFF:
            out.append(row["type"])
        if "size_width" in row:
            out.extend(write_quantity((len(row["data"]), row["size_width"])))
        out.extend(row["data"])
        if "duration" in row:
            out.extend(write_quantity(row["duration"]))
    return bytes(out) + tail


def read_chunks(data):
    chunks, at = [], 0
    while at + CHUNK.size <= len(data):
        tag, size = CHUNK.unpack_from(data, at)
        start = at + CHUNK.size
        end = start + size
        if end > len(data):
            raise ValueError(f"{tag!r} at +{at:#x} exceeds its parent")
        raw = data[start:end]
        if tag in CONTAINERS:
            if size < 4:
                raise ValueError("container lacks a type")
            fields = (raw[:4], read_chunks(raw[4:]))
        elif tag == b"EVNT":
            fields = read_events(raw)
        elif tag == b"INFO" and size == 2:
            fields = struct.unpack("<H", raw)[0]
        else:
            fields = raw
        pad = data[end:end + (size & 1)]
        chunks.append((tag, fields, pad))
        at = end + len(pad)
    return chunks, data[at:]


def write_chunks(chunks, remainder):
    out = bytearray()
    for tag, fields, pad in chunks:
        if tag in CONTAINERS:
            kind, subchunks = fields
            body = kind + write_chunks(*subchunks)
        elif tag == b"EVNT":
            body = write_events(*fields)
        elif tag == b"INFO" and isinstance(fields, int):
            body = struct.pack("<H", fields)
        else:
            body = fields
        if len(pad) > 1:
            raise ValueError("IFF alignment field is more than one byte")
        out.extend(CHUNK.pack(tag, len(body)))
        out.extend(body)
        if len(body) & 1:
            out.extend(pad or b"\0")
    return bytes(out) + remainder


def count_events(chunks):
    count = Counter()
    for tag, fields, _ in chunks:
        if tag in CONTAINERS:
            count.update(count_events(fields[1][0]))
        if tag == b"EVNT":
            count["sequences"] += 1
            count["events"] += len(fields[0])
            count["post_end_bytes"] += len(fields[1])
    return count


def music_sources(data):
    for ext in (".XMI", ".C55", ".PCS"):
        yield from L.find_all(ext, data)
        for path in sorted(Path(data).iterdir()):
            if path.suffix.upper() == ext:
                yield None, path.name, path.read_bytes()


def check(data):
    counts, files = Counter(), Counter()
    for pak, name, raw in music_sources(data):
        try:
            tree = read_chunks(raw)
            if write_chunks(*tree) != raw:
                raise ValueError("reconstructed bytes differ")
            per_file = count_events(tree[0])
            if not per_file["sequences"]:
                raise ValueError("no EVNT sequence")
            counts.update(per_file)
            files[Path(name).suffix.upper()] += 1
        except (ValueError, struct.error, IndexError) as exc:
            raise ValueError(f"{pak or 'loose'}/{name}: {exc}") from exc
    if not files[".XMI"]:
        raise ValueError("no original XMI scores")
    print(f"CHECK XMI write: {sum(files.values())} byte-identical files "
          f"({files['.XMI']} XMI, {files['.C55']} C55, {files['.PCS']} PCS), "
          f"{counts['sequences']} sequences, {counts['events']} events, "
          f"{counts['post_end_bytes']} post-end bytes")


def main():
    parser = L.tool_args(__doc__, writes=False)
    args = parser.parse_args()
    if not args.check:
        parser.error("give --check to compare the original scores in memory")
    check(args.data)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
