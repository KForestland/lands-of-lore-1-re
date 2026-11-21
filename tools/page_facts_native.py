"""Raw witnesses for the LoL1 floppy 1.05 and CD 1.02 archives."""
from functools import lru_cache
from struct import unpack_from

from cli_errors import game_path

DATA_ENV = "LOL1_DATA"


class WitnessUnavailable(ValueError):
    """A valid original edition without the referenced material."""


def is_cd(data):
    return game_path(data, "L01.PAK").is_file()


def game_file(data, name):
    if name.upper() == "MUSIC.PAK" and not is_cd(data):
        raise WitnessUnavailable("MUSIC.PAK citation applies to the CD edition")
    if name.upper() in {"MAIN.EXE", "MAINW.EXE"}:
        root = game_path(data, "HARDRIVE") if is_cd(data) else data
    else:
        root = data
    return game_path(root, name.replace(chr(92), "/").split("/")[-1])


def edition_status(data):
    if is_cd(data) or game_path(data, "CHAPTER1.PAK").is_file():
        return None
    return "neither the CD nor the floppy data root is present"


def pak_rows(path):
    """Read the original name and offset sequence through its EOF sentinel."""
    with path.open("rb") as source:
        first, = unpack_from("<I", source.read(4))
        source.seek(0)
        table = source.read(first)
    length = path.stat().st_size
    entries, pos, previous = [], 0, first
    while pos + 4 <= len(table):
        offset, = unpack_from("<I", table, pos)
        if not previous <= offset <= length:
            raise ValueError(f"{path.name}: invalid member offset {offset:#x}")
        if offset == length:
            if table[pos + 4:] != b"\0" * 5:
                raise ValueError(f"{path.name}: invalid archive trailer")
            return entries, length
        end = table.index(b"\0", pos + 4)
        entries.append((table[pos + 4:end].decode("ascii"), offset))
        pos = end + 1
        previous = offset
    raise ValueError(f"{path.name}: missing archive EOF sentinel")


@lru_cache(maxsize=12)
def member(path, name):
    rows, end = pak_rows(path)
    rows.append(("", end))
    for (entry, offset), (_, stop) in zip(rows, rows[1:]):
        if entry.upper() == name:
            with path.open("rb") as source:
                source.seek(offset)
                return source.read(stop - offset), offset
    raise ValueError(f"{path.name}: no {name}")


def chunk(script, tag):
    if script[:4] != b"FORM" or script[8:12] != b"EMC2":
        raise ValueError("missing EMC2 script header")
    cursor = 12
    while cursor + 8 <= len(script):
        size, = unpack_from(">I", script, cursor + 4)
        data = cursor + 8
        if script[cursor:cursor + 4] == tag and data + size <= len(script):
            return script[data:data + size], data
        cursor = data + size + (size & 1)
    raise ValueError(f"EMC2 chunk {tag!r} not found")


def frame4(source, size):
    """Decode one bounded LCW stream and require the exact expanded length."""
    out, pos = bytearray(), 0
    while len(out) < size:
        op = source[pos]
        pos += 1
        if op == 0x80:
            break
        if op & 0x80 == 0:
            count = (op >> 4) + 3
            offset = len(out) - ((op & 15) * 256 + source[pos])
            pos += 1
        elif op < 0xC0:
            count = op & 63
            out.extend(source[pos:pos + count])
            pos += count
            continue
        elif op == 0xFE:
            count, fill = unpack_from("<HB", source, pos)
            out.extend(bytes([fill]) * count)
            pos += 3
            continue
        else:
            count = (op & 63) + 3
            if op == 0xFF:
                count, = unpack_from("<H", source, pos)
                pos += 2
            offset, = unpack_from("<H", source, pos)
            pos += 2
        if not 0 <= offset < len(out) or len(out) + count > size:
            raise ValueError("LCW back-reference leaves the expanded frame")
        for i in range(count):
            out.append(out[offset + i])
    if len(out) != size:
        raise ValueError("LCW stream does not fill the frame")
    return bytes(out)


def complete_rows(lines, width, height, colours):
    pos = 0
    for _ in range(height):
        column = 0
        while column < width:
            pixel = lines[pos]
            pos += 1
            if pixel:
                if pixel >= colours:
                    return False
                column += 1
            else:
                column += lines[pos]
                pos += 1
        if column != width:
            return False
    return pos == len(lines)


def colour_width(wrapped):
    size, palette = unpack_from("<IH", wrapped, 4)
    data = frame4(wrapped[10 + palette:], size)
    at = 2 + unpack_from("<I", data, 2)[0]
    flags, height, width, height2, stored, expanded = unpack_from("<HBHBHH", data, at)
    if flags & 7 != 5 or height != height2 or at + stored > size:
        raise ValueError("FXPAL shape 0 is not a complete variable-colour frame")
    candidates = []
    for count_bytes, label in ((1, "byte"), (2, "word"), (4, "dword")):
        count_at = at + 10
        colors = int.from_bytes(data[count_at:count_at + count_bytes], "little")
        frame = count_at + count_bytes + colors
        try:
            if frame >= at + stored:
                continue
            lines = frame4(data[frame:at + stored], expanded)
            if complete_rows(lines, width, height, colors):
                candidates.append(label)
        except (ValueError, IndexError):
            continue
    if len(candidates) != 1:
        raise ValueError(f"FXPAL.SHP shape 0: no unique palette count width ({candidates})")
    return candidates[0]


def read_witness(data, spec):
    kind, *args = spec
    cd = is_cd(data)
    if kind in {"pak_count", "tlk_count"}:
        if not cd:
            raise WitnessUnavailable("CD DATA archive censuses do not apply to floppy")
        extensions = {".TLK"} if kind == "tlk_count" else {".PAK", ".TLK"}
        paths = sorted(path for path in data.iterdir() if path.suffix.upper() in extensions)
        return sum(len(pak_rows(path)[0]) for path in paths), f"CD DATA, {len(paths)} PAK/TLK directories"

    cd_name, floppy_name, name, *params = args
    label = cd_name if cd else floppy_name
    path = game_path(data, label)
    raw, base = member(path, name)
    source = f"{label}/{name} (archive +{base:#x})"
    if kind == "member_size":
        return len(raw), source
    if kind == "ordr_word":
        entries, offset = chunk(raw, b"ORDR")
        at = 2 * params[0]
        return unpack_from(">H", entries, at)[0], f"{source}, ORDR +{offset + at:#x}"
    if kind == "wll_decoration":
        wll, _ = member(path, "LEVEL1.WLL")
        area, = unpack_from("<H", wll)
        if area != params[0]:
            raise ValueError(f"LEVEL1.WLL area {area} differs")
        code, _ = chunk(raw, b"DATA")
        text, _ = chunk(raw, b"TEXT")
        # The two tiny pushes before slot 0x15 name the DAT and SHP.
        sites = [i for i in range(4, len(code), 2)
                 if code[i:i + 2] == b"\x4e\x15" and code[i - 4] == code[i - 2] == 0x44]
        if len(sites) != 1:
            raise ValueError("expected one level-decoration script call")
        at, = unpack_from(">H", text, 2 * code[sites[0] - 3])
        label = text[at:text.index(0, at)].decode("ascii")
        member(game_path(data, "KEEP.PAK" if cd else "CHAPTER1.PAK"), label)
        return label, f"{source}, decoration load and LEVEL1.WLL area {area}"
    if kind == "colour_width":
        return colour_width(raw), f"{source}, shape 0"
    raise ValueError(f"unknown byte witness {kind!r}")
