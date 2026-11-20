"""Read glyph coverage from original Westwood FNT resources."""
from struct import unpack_from

from translate_data import decode, encode, font_sources


def coverage(blob):
    if len(blob) < 20:
        raise ValueError("The FNT header is truncated.")
    size, sig, desc, offsets, widths, _, heights = unpack_from("<7H", blob)
    if sig != 0x0500 or size != len(blob) or desc + 6 > size:
        raise ValueError("The file does not have a complete 0x0500 FNT header.")
    last, height, _ = blob[desc + 3:desc + 6]
    count = last + 1
    if max(offsets + 2 * count, widths + count, heights + 2 * count) > size:
        raise ValueError("A FNT glyph directory crosses the file end.")
    drawn = set()
    for i in range(count):
        start, = unpack_from("<H", blob, offsets + 2 * i)
        width = blob[widths + i]
        top, rows = blob[heights + 2 * i:heights + 2 * i + 2]
        end = start + ((width + 1) // 2) * rows
        if end > size or top + rows > height:
            raise ValueError("A FNT glyph crosses the font bounds.")
        # The file can provide advance width for a blank space.
        if width and (i == 32 or (start and any(blob[start:end]))):
            drawn.add(i)
    return drawn


def installed(root):
    return [(name, coverage(blob)) for name, blob in font_sources(root)]


def show(root):
    fonts = installed(root)
    if not fonts:
        raise ValueError("No named font resources were found in this copy.")
    for name, drawn in fonts:
        text = " ".join(char if char.isprintable() and char != " " else f"\\x{i:02X}"
                        for i in sorted(drawn) if i >= 32 for char in decode(bytes((i,))))
        print(f"{name}: {text}")


def missing(text, fonts):
    for char in sorted(set(text)):
        # Game controls are byte values too, but they do not need glyphs.
        if ord(char) < 32 or ord(char) == 127:
            continue
        try:
            raw = encode(char)
        except UnicodeError:
            continue  # The table writer reports unrepresentable text separately.
        blanks = [name for name, drawn in fonts if len(raw) != 1 or raw[0] not in drawn]
        if blanks:
            yield f"{ascii(char)} has no drawn glyph in {', '.join(blanks)}. Choose a listed character or leave the original."
