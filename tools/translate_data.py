"""LoL1 language tables and script TEXT chunks."""
from pathlib import Path
import re
import struct

from decode_dialogue import decode_string1, decode_string2, encode_string
from level_html import find_data
from lol1_level_writer import LANGUAGES
from lol1lib import pak_entries

LOOSE = LANGUAGES | {".TIM", ".INI", ".INF"}


def decode(raw):
    return raw.decode("cp437")


def encode(text):
    return b"".join(bytes((ord(char) - 0xDC00,)) if 0xDC80 <= ord(char) <= 0xDCFF
                    else char.encode("cp437") for char in text)


def font_sources(base):
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.upper()
        if suffix == ".FNT":
            yield path.relative_to(base).as_posix(), path.read_bytes()
        elif suffix == ".PAK":
            raw = path.read_bytes()
            for label, at, size in pak_entries(raw):
                if label.upper().endswith(".FNT"):
                    yield f"{path.relative_to(base).as_posix()}/{label}", raw[at:at + size]


def root(path):
    return find_data(path, "DATA", "GENERAL.PAK")


def sources(base):
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        name = path.relative_to(base).as_posix()
        suffix = path.suffix.upper()
        if suffix == ".PAK":
            archive = path.read_bytes()
            for i, (label, start, size) in enumerate(pak_entries(archive)):
                raw = archive[start:start + size]
                if Path(label).suffix.upper() in LANGUAGES or script_text(raw):
                    yield name, i, label, start, raw
        elif suffix in LOOSE:
            raw = path.read_bytes()
            if suffix in LANGUAGES or script_text(raw):
                yield name, 0, path.name, 0, raw


def script_text(raw):
    if raw[:4] != b"FORM" or raw[8:12] not in (b"EMC2", b"AVFS"):
        return None
    at = 12
    while at + 8 <= len(raw):
        tag, length = struct.unpack_from(">4sI", raw, at)
        end = at + 8 + length
        if end > len(raw):
            raise ValueError("A script text chunk crosses the file end.")
        if tag == b"TEXT" and length > 2:
            return at, end, ">" if raw[8:12] == b"EMC2" else "<"
        at = end + (length & 1)
    return None


def pointers(raw, endian):
    first, = struct.unpack_from(endian + "H", raw)
    if first < 2 or first & 1 or first >= len(raw):
        raise ValueError("The text directory does not start at a valid offset.")
    offsets = struct.unpack_from(f"{endian}{first // 2}H", raw)
    if any(at < first or raw.find(b"\0", at) < 0 for at in offsets):
        raise ValueError("A text row points outside the table.")
    return offsets


def fields(blob):
    section = script_text(blob)
    if section is None:
        return blob, "<", True
    start, end, endian = section
    return blob[start + 8:end], endian, False


def decoded(raw, compressed):
    value = decode_string2(decode_string1(raw)) if compressed else raw
    return value.decode("cp437")


def locked(text, compressed):
    # Script strings also name resources and directories. Leave single tokens to
    # their consumers unless this is a separate language table.
    return not compressed and (not text.strip() or re.fullmatch(r"[A-Za-z0-9_?*./\\:-]+", text.strip()))


def read(label, blob):
    raw, endian, compressed = fields(blob)
    rows = []
    for i, at in enumerate(pointers(raw, endian)):
        value = raw[at:raw.index(b"\0", at)]
        text = decoded(value, compressed)
        limit = "locked" if locked(text, compressed) else f"{65535 - len(raw) + len(value)} encoded bytes"
        rows.append((i, text, limit))
    return rows


def write(label, blob, changes):
    raw, endian, compressed = fields(blob)
    offsets = pointers(raw, endian)
    replacements = {}
    expected = {}
    for i, at in enumerate(offsets):
        old = raw[at:raw.index(b"\0", at)]
        value = old
        if i in changes:
            text = changes[i]
            if locked(decoded(old, compressed), compressed):
                raise ValueError(f"Row {i} is a script resource name.")
            try:
                value = encode(text)
            except UnicodeError:
                raise ValueError(f"Row {i} has a character outside code page 437. Choose a character the game can store.") from None
            if compressed:
                value = encode_string(value)
            if b"\0" in value:
                raise ValueError(f"Row {i} contains a NUL, which ends a string.")
        if at in expected and expected[at] != value:
            raise ValueError(f"Row {i} shares its stored string with another row. Give both the same translation.")
        expected[at] = value
        if value != old:
            replacements[at] = (len(old), value)
    changes_by_offset = sorted(replacements.items())
    output, cursor = bytearray(), 0
    for at, (length, value) in changes_by_offset:
        if at < cursor or any(at < item <= at + length for item in offsets):
            raise ValueError(f"Text at +{at:#x} overlaps a second row. Leave that string unchanged.")
        output.extend(raw[cursor:at])
        output.extend(value)
        cursor = at + length
    output.extend(raw[cursor:])
    if len(output) > 65535:
        raise ValueError("The table exceeds 65,535 encoded bytes. Shorten the new text.")
    for i, at in enumerate(offsets):
        shift = sum(len(value) - old for start, (old, value) in changes_by_offset if start < at)
        struct.pack_into(endian + "H", output, 2 * i, at + shift)
    if compressed:
        return bytes(output)
    start, end, _ = script_text(blob)
    suffix = end + ((end - start - 8) & 1)
    pad = (blob[end:suffix] or b"\0") if len(output) & 1 else b""
    result = bytearray(blob[:start] + b"TEXT" + struct.pack(">I", len(output)) + output + pad + blob[suffix:])
    declared = struct.unpack_from(">I", blob, 4)[0]
    struct.pack_into(">I", result, 4, declared + len(result) - len(blob))
    return bytes(result)
