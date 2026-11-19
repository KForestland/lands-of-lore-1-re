#!/usr/bin/env python3
"""Walk the CD DATA files that are not PAK or TLK archives.

A file counts as read when every byte sits in a header, a directory or an
entry. The six blend tables fail that walk and stay unread. The check pins
the structure that was measured: the blend-table sizes, the installer status
text, README.ENG at file +0x72, and the TDINFO tables on each symbol block. It also rebuilds both blend
tables as a self-blend of the paired finale palette (RETURN.CPS for BLEND.TAB,
FACE.CPS for BLEND2.TAB): all but the last four bytes match.

  lol1_loose.py --check
"""
from cli_errors import ReaderArgumentParser, run_cli
import argparse
import os
import struct

import fnt_reader
import lol1lib as L

COVERED = {
    "ENG/NEW6P.FNT", "FRE/NEW6P.FNT", "GER/NEW6P.FNT",
    "HARDRIVE/ENG.LM", "HARDRIVE/FRE.LM", "HARDRIVE/GER.LM",
    "HARDRIVE/SETUPENG.DIP", "HARDRIVE/SETUPFRE.DIP", "HARDRIVE/SETUPGER.DIP",
    "FILEDATA.FDT",
    "HARDRIVE/LANDS.ICO", "HARDRIVE/SETUP.ICO",
    "HARDRIVE/LANDS.PIF", "HARDRIVE/DOSETUP.PIF",
    "ENG/FINALE.EXE", "FRE/FINALE.EXE", "GER/FINALE.EXE",
    "HARDRIVE/LOLCD.EXE", "HARDRIVE/SETUP.EXE",
    "HARDRIVE/VDSPD.386", "HARDRIVE/VWWSD.386",
    "HARDRIVE/MAIN.EXE", "HARDRIVE/MAINW.EXE",
    "FRE/STATE.RST", "HARDRIVE/VISBIOS.COM",
    "ENG/FINALE.TDS", "FRE/FINALE.TDS", "GER/FINALE.TDS",
    "ENG/LANDS.EXE", "FRE/LANDS.EXE", "GER/LANDS.EXE",
}
OPEN = {
    "ENG/BLEND.TAB", "FRE/BLEND.TAB", "GER/BLEND.TAB",
    "ENG/BLEND2.TAB", "FRE/BLEND2.TAB", "GER/BLEND2.TAB",
}
# Declared MZ image size and header length, for the seven files whose image is the whole file.
MZ_EXACT = {
    "ENG/FINALE.EXE": (132328, 8704),
    "FRE/FINALE.EXE": (134122, 8704),
    "GER/FINALE.EXE": (134212, 8704),
    "HARDRIVE/LOLCD.EXE": (19356, 1024),
    "HARDRIVE/SETUP.EXE": (103188, 7168),
    "HARDRIVE/VDSPD.386": (10936, 64),
    "HARDRIVE/VWWSD.386": (5371, 64),
}
# File length and MZ image end. The tail is the unread symbol block.
LANDS = {
    "ENG/LANDS.EXE": (357509, 146176),
    "FRE/LANDS.EXE": (359338, 147952),
    "GER/LANDS.EXE": (359418, 148032),
}
TDS_SIZE = {"ENG/FINALE.TDS": 210583, "FRE/FINALE.TDS": 210724, "GER/FINALE.TDS": 210724}
# uint32 at +4: byte length of the trailing NUL-terminated string pool.
POOL_LEN = {
    "ENG/FINALE.TDS": 0xA5E4,
    "FRE/FINALE.TDS": 0xA600,
    "GER/FINALE.TDS": 0xA600,
    "ENG/LANDS.EXE": 0xA4F9,
    "FRE/LANDS.EXE": 0xA515,
    "GER/LANDS.EXE": 0xA515,
}
# uint16 at +8 (TDINFO name count): the number of NUL-terminated strings in that pool.
POOL_COUNT = {
    "ENG/FINALE.TDS": 3593,
    "FRE/FINALE.TDS": 3596,
    "GER/FINALE.TDS": 3596,
    "ENG/LANDS.EXE": 3583,
    "FRE/LANDS.EXE": 3586,
    "GER/LANDS.EXE": 3586,
}
# Borland Turbo Debugger symbol table (TDINFO): magic 0x52FB, version 0x0310.
SYMBOL = b"\xfb\x52\x10\x03"
BLEND_HEAD = b"\x38\xb6\xb7\xb7\xc1\x3e\x77\x3f"
BLEND2_HEAD = b"\x13\x13\x8a\x8a\x8c\x0a\x8e\x0b"
# PAL, COL and 768-byte picture palettes stored in the CD PAK files.
STORED_PALETTES = 300
# Distinct byte strings among those 300, and how many of SCROLL.CPS's 256 colours
# the blend-table diagonal names. The rest of the 300 are language copies.
DISTINCT_PALETTES = 109
SCROLL_DIAGONAL = {"BLEND.TAB": 240, "BLEND2.TAB": 233}
# mov cx, 256. A 256-step loop can be written another way; this only pins this encoding.
MOV_CX_256 = b"\xb9\x00\x01"
NAME_PINS = (
    ("HARDRIVE/MAIN.EXE", 0x334DC, b"FILEDATA.FDT\x00"),
    ("HARDRIVE/MAIN.EXE", 0x33C44, b"FILEDATA.FDT\x00ENG.LM\x00FRE.LM\x00GER.LM\x00"),
    ("HARDRIVE/MAINW.EXE", 0x32F82, b"FILEDATA.FDT\x00"),
    ("HARDRIVE/MAINW.EXE", 0x336E8, b"FILEDATA.FDT\x00ENG.LM\x00FRE.LM\x00GER.LM\x00"),
    ("HARDRIVE/SETUP.EXE", 0x17518, b"SETUP%s.DIP\x00"),
    ("ENG/LANDS.EXE", 0x20279, b"NEW6P.FNT\x00"),
    ("ENG/FINALE.EXE", 0x1D9C8, b"NEW6P.FNT\x00"),
    ("FRE/FINALE.EXE", 0x1E07A, b"NEW6P.FNT\x00"),
    ("GER/FINALE.EXE", 0x1E0C4, b"NEW6P.FNT\x00"),
    ("ENG/FINALE.EXE", 0x1DB04, b"VWWSD.386"),
)
INSTALL_PINS = (
    (0x7D69, b"SETUPENG.DIP\x00"),
    (0xFD78, b"VISBIOS.COM"),
    (0xFDCA, b"vdspd.386"),
    (0xFDFD, b"VWWSD.386"),
    (0xFEB5, b"LANDS.ICO\x00"),
    (0xFEEA, b"LANDS.PIF\x00"),
    (0xFF05, b"SETUP.ICO\x00"),
    (0xFF1A, b"DOSETUP.PIF\x00"),
)
ABSENT_FROM = (
    "HARDRIVE/MAIN.EXE", "HARDRIVE/MAINW.EXE", "HARDRIVE/SETUP.EXE", "HARDRIVE/LOLCD.EXE",
    "ENG/LANDS.EXE", "FRE/LANDS.EXE", "GER/LANDS.EXE",
    "ENG/FINALE.EXE", "FRE/FINALE.EXE", "GER/FINALE.EXE", "DRIVERS.PAK",
)
# Compared case-insensitively. INSTALL.EXE does contain the word "blend" (pinned below as
# INSTALL_BLEND), so the needles are the file names, not the word.
ABSENT_NEEDLES = (b"blend.tab", b"blend2.tab", b".tab", b"state.rst")
# INSTALL.EXE string-table entries (byte-length prefixed) 1049 and 1050 of the English block.
INSTALL_BLEND = (
    (0x12ABF, b"\x1eCreating intro blend tables..."),
    (0x12ADE, b"\x1fCreating finale blend tables..."),
)
# ENG/FINALE2.PAK: LOLFINAL.TIM TEXT strings 3 and 30, and the nested 0x19 function 6
# instructions that pass those string indexes (length 5, delay 0, opcode 0x0119, 6, index).
FINALE_BLEND = (
    (0xC9D0D, b"FORM"),
    (0xCAF7B, b"BLEND.TAB\x00"),
    (0xCB08F, b"BLEND2.TAB\x00"),
    (0xC9D49, bytes.fromhex("05000000190106000300")),
    (0xCA45B, bytes.fromhex("05000000190106001e00")),
)
VISBIOS_PINS = (
    (0x1C4, b"VIS video emulation"),
    (0x215, b"VIS synthesizer"),
    (0x513F, b"Installed OK."),
    (0x5151, b"VIS BIOS Extensions for Sensation"),
    (0x519F, b"Tandy Corporation"),
)
# LE header of the two Windows VxDs: file offset of LE, page count, last page bytes,
# data pages offset, non-resident name table offset and length.
LE_FIELDS = {
    "HARDRIVE/VDSPD.386": (0x80, 3, 641, 0x800, 0x2A81, 55),
    "HARDRIVE/VWWSD.386": (0x80, 2, 201, 0x400, 0x14C9, 50),
}
# FBOV directory rows (8 bytes) and the program name that follows the last row.
FBOV_ROWS = {"HARDRIVE/MAIN.EXE": (0x127, b"main.exe\x00"), "HARDRIVE/MAINW.EXE": (0x127, b"mainw.exe\x00")}
PALETTE_ROWS = (
    (122, b"ALTPAL3.PAL", 0x1B8B5),
    (204, b"CAV_PLT2.PAL", 0x1D72C),
    (206, b"CAV_PLT4.PAL", 0x1DD2C),
)


def mz_declared(data):
    """Bytes the MZ page fields claim, or None when the header is not MZ."""
    if len(data) < 0x1C or data[:2] != b"MZ":
        return None
    last, pages = struct.unpack_from("<HH", data, 2)
    if pages == 0:
        return None
    return pages * 512 if last == 0 else (pages - 1) * 512 + last


def header_bytes(data):
    return struct.unpack_from("<H", data, 8)[0] * 16


def font_covers(data):
    """The font's parts tile the file with no gap and no overlap.

    Header 0..14 (seven words), descriptor D..D+6, bitmap-offset table (2 bytes per
    glyph), width table (1 byte per glyph), glyph bitmaps, height table (2 bytes per
    glyph). Glyphs may share one bitmap offset; a shared bitmap spans the largest
    size that points at it. The bitmaps must tile their region on their own.
    """
    try:
        header, glyphs = fnt_reader.parse(data)
        size, sig, desc, offsets, widths, _field10, heights = struct.unpack_from("<7H", data, 0)
    except (struct.error, IndexError, ValueError):
        return False
    if header["signature"] != "0x500" or size != len(data):
        return False
    if any(item["top"] + item["rows"] > header["height"] for item in glyphs):
        return False
    count = len(glyphs)
    bitmaps = {}
    for item in glyphs:
        if item["offset"]:
            span = ((item["width"] + 1) // 2) * item["rows"]
            bitmaps[item["offset"]] = max(bitmaps.get(item["offset"], 0), span)
    if not bitmaps:
        return False
    parts = [(0, 14), (desc, desc + 6), (offsets, offsets + 2 * count), (widths, widths + count),
             (heights, heights + 2 * count)]
    parts += [(start, start + span) for start, span in bitmaps.items()]
    cursor = 0
    for start, end in sorted(parts):
        if start != cursor or end <= start:
            return False
        cursor = end
    return cursor == len(data)


def strings_cover(data):
    """A uint16 offset table whose first offset is the first byte after the table.

    Each following offset starts at the previous string's NUL, and the last
    NUL is the last byte of the file.
    """
    if len(data) < 4:
        return False
    table = struct.unpack_from("<H", data, 0)[0]
    if table < 2 or table > len(data) or table % 2:
        return False
    offsets = struct.unpack_from("<" + "H" * (table // 2), data, 0)
    if offsets[0] != table:
        return False
    position = table
    for offset in offsets:
        if offset != position or offset >= len(data):
            return False
        end = data.find(b"\0", offset)
        if end < 0:
            return False
        position = end + 1
    return position == len(data)


def inventory_covers(data):
    """1275 records of 20 bytes, then NUL-terminated names through the last byte.

    The last record is 20 zero bytes. Every earlier record's first uint32 is a
    name offset, and those names tile the pool with no gap and no overlap.
    """
    if len(data) < 40:
        return False
    pool = struct.unpack_from("<I", data, 0)[0]
    if pool % 20 or pool < 20 or pool >= len(data):
        return False
    rows = pool // 20
    if rows != 1275:
        return False
    if data[(rows - 1) * 20:rows * 20] != b"\0" * 20:
        return False
    cursor = pool
    for index in range(rows - 1):
        offset = struct.unpack_from("<I", data, index * 20)[0]
        if offset != cursor or offset >= len(data):
            return False
        end = data.find(b"\0", offset)
        if end <= offset:
            return False
        if any(byte < 32 or byte > 126 for byte in data[offset:end]):
            return False
        cursor = end + 1
    return cursor == len(data)


def icon_covers(data):
    if len(data) < 62:
        return False
    reserved, kind, count = struct.unpack_from("<HHH", data, 0)
    if (reserved, kind, count) != (0, 1, 1):
        return False
    width, height, colors, _reserved, _planes, _bits, size, offset = struct.unpack_from("<BBBBHHII", data, 6)
    if offset != 22 or offset + size != len(data) or width == 0 or height == 0:
        return False
    bi_size, bi_width, bi_height, planes, bit_count = struct.unpack_from("<IiiHH", data, offset)
    if bi_size != 40 or bi_width != width or bi_height != height * 2 or planes != 1 or bit_count not in (1, 4, 8):
        return False
    if colors not in (0, 1 << bit_count):
        return False
    palette = (1 << bit_count) * 4

    def stride(pixels, bits):
        return ((pixels * bits + 31) // 32) * 4

    return 40 + palette + stride(width, bit_count) * height + stride(width, 1) * height == size


def pif_covers(data):
    """Windows PIF section chain. Data offsets are absolute file offsets.

    MICROSOFT PIFEX at byte 0x171 points its data field at the basic record.
    Each later header is 22 bytes (16-byte name, next, data offset, data size).
    The spans must meet, not overlap, and end on the last byte.
    """
    if len(data) < 0x171 + 22 or data[0x171:0x181].split(b"\0", 1)[0] != b"MICROSOFT PIFEX":
        return False
    spans = []
    position = 0x171
    seen = set()
    while True:
        if position in seen or position + 22 > len(data):
            return False
        seen.add(position)
        nxt, offset, size = struct.unpack_from("<HHH", data, position + 16)
        spans.append((position, position + 22))
        if size and (offset + size > len(data)):
            return False
        if size:
            spans.append((offset, offset + size))
        if nxt == 0xFFFF:
            break
        position = nxt
    cursor = 0
    for start, end in sorted(spans):
        if start != cursor:
            return False
        cursor = end
    return cursor == len(data)


def mz_exact(data):
    """The MZ page fields declare the whole file and the relocation table fits in the header."""
    declared = mz_declared(data)
    if declared is None:
        return False
    header = header_bytes(data)
    count, table = struct.unpack_from("<H", data, 6)[0], struct.unpack_from("<H", data, 0x18)[0]
    if not (0x1C <= table and table + 4 * count <= header):
        return False
    return declared == len(data) and 0x1C <= header < len(data)


def le_covers(data):
    """MZ stub + LE (Windows VxD) program.

    The MZ word at 0x3C points at `LE`. The loader and fixup sections end before
    the data pages, the gap up to the data pages is zero, the data pages
    ((pages - 1) * page size + last page bytes) end where the non-resident name
    table starts, and that table ends on the last byte.
    """
    if not mz_exact(data) or len(data) < 0x40:
        return False
    le = struct.unpack_from("<I", data, 0x3C)[0]
    if le < header_bytes(data) or le + 0x90 > len(data) or data[le:le + 4] != b"LE\0\0":
        return False

    def field(offset):
        return struct.unpack_from("<I", data, le + offset)[0]

    pages, page_size, last = field(0x14), field(0x28), field(0x2C)
    loader_end = le + field(0x40) + field(0x38) + field(0x30)
    data_pages, names, names_size = field(0x80), field(0x88), field(0x8C)
    if not pages or not 0 < last <= page_size or not loader_end <= data_pages:
        return False
    if data[loader_end:data_pages].strip(b"\0"):
        return False
    return data_pages + (pages - 1) * page_size + last == names and names + names_size == len(data)


def fbov_rows(data):
    """Rows of the FBOV directory: 8 bytes each (uint16 segment, size, kind, adjust).

    Walks rows while the segment field does not decrease; returns the row count
    and whether the last row's segment * 16 + header + size is the MZ image end.
    """
    declared = mz_declared(data)
    directory = struct.unpack_from("<I", data, declared + 8)[0]
    header = header_bytes(data)
    rows, previous = 0, -1
    while directory + 8 * (rows + 1) <= declared:
        segment = struct.unpack_from("<H", data, directory + 8 * rows)[0]
        if segment < previous or header + segment * 16 >= declared:
            break
        previous = segment
        rows += 1
    segment, size = struct.unpack_from("<HH", data, directory + 8 * (rows - 1))
    return rows, header + segment * 16 + size == declared


def overlay_covers(data):
    """MZ image, then a 16-byte FBOV header whose body-length field reaches EOF.

    The uint32 at FBOV+8 must fall inside the MZ image, after the DOS header.
    """
    declared = mz_declared(data)
    if declared is None or declared + 16 > len(data) or data[declared:declared + 4] != b"FBOV":
        return False
    body, directory, _third = struct.unpack_from("<III", data, declared + 4)
    header = header_bytes(data)
    if not (0x1C <= header <= directory < declared):
        return False
    return declared + 16 + body == len(data)


def text_covers(data):
    if not data or data[-1:] != b"\n":
        return False
    return all(byte in (10, 13) or 32 <= byte <= 126 for byte in data)


def com_covers(data):
    """A COM image: the file length is the image. Byte 0 jumps over the revision string."""
    revision = b"Revision 1.01 02/12/93"
    if len(data) != 30976 or data[:3] != b"\xe9\x1d\x00":
        return False
    # E9 is a near jump; the displacement is relative to the next instruction.
    if 3 + struct.unpack_from("<H", data, 1)[0] != 0x20:
        return False
    return data[4:4 + len(revision)] == revision and data[4 + len(revision)] == 0


def covers(filename, data):
    suffix = filename.rsplit(".", 1)[-1].upper() if "." in filename else ""
    if suffix == "FNT":
        return font_covers(data)
    if suffix in ("LM", "DIP"):
        return strings_cover(data)
    if filename.upper() == "FILEDATA.FDT":
        return inventory_covers(data)
    if suffix == "ICO":
        return icon_covers(data)
    if suffix == "PIF":
        return pif_covers(data)
    if suffix == "RST":
        return text_covers(data)
    if suffix == "COM":
        return com_covers(data)
    if suffix == "386":
        return le_covers(data)
    if suffix == "TDS":
        return symbol_block_covers(data)
    if suffix == "EXE":
        if mz_exact(data) or overlay_covers(data):
            return True
        declared = mz_declared(data)
        if declared is None or declared >= len(data) or data[declared:declared + 4] != SYMBOL:
            return False
        header = header_bytes(data)
        count = struct.unpack_from("<H", data, 6)[0]
        table = struct.unpack_from("<H", data, 0x18)[0]
        if not (0x1C <= table and table + 4 * count <= header and 0x1C <= header < declared):
            return False
        return symbol_block_covers(data[declared:])
    return False


def covered(path):
    path = L_path(path)
    return covers(path.name, path.read_bytes())


def L_path(path):
    from pathlib import Path
    return path if hasattr(path, "read_bytes") else Path(path)


def string_pool_reaches_end(block, pool_len, pool_count):
    """True when the last pool_len bytes are pool_count packed printable strings ending at EOF,
    and the uint16 at +8 is that string count."""
    if len(block) < 10 or block[:4] != SYMBOL:
        return False
    if struct.unpack_from("<I", block, 4)[0] != pool_len:
        return False
    if struct.unpack_from("<H", block, 8)[0] != pool_count:
        return False
    if pool_len < 8 or pool_len >= len(block):
        return False
    pos = len(block) - pool_len
    count = 0
    while pos < len(block):
        end = pos
        while end < len(block) and 32 <= block[end] < 127:
            end += 1
        if end == pos or end >= len(block) or block[end] != 0:
            return False
        pos = end + 1
        count += 1
    return count == pool_count


def word(block, offset):
    return struct.unpack_from("<H", block, offset)[0]


def symbol_block_covers(block):
    """True when a TDINFO header's counts size every table and the name pool ends the block.

    The header is 48 bytes plus the extension at +0x2E. Tables then follow, in order:
    symbols (9), modules (16), source files (6), line numbers (4), scopes (12),
    segments (16), correlations (8), types (8), members (5), then the extension
    tables classes (11), parents (2), overloads (8), scope classes (4), module
    classes (8) and browsers (6), then DataCount bytes from +0x2B. CoverageOffsetCount
    uint16 values and one uint16 per segment come next. Zero bytes run from there to
    the name pool. NamePoolOffset is relative to the first symbol byte. GlobalsCount
    sizes no table of its own, and LocalsCount is 0.
    """
    if len(block) < 80 or block[:4] != SYMBOL:
        return False
    pool = struct.unpack_from("<I", block, 4)[0]
    (names, types, members, symbols, _global_count, modules, _locals, scopes,
     lines, sources, segments, correlations) = struct.unpack_from("<12H", block, 8)
    if names == 0 or symbols == 0 or scopes == 0 or pool < 2 or pool >= len(block):
        return False
    if word(block, 0x14) != 0:
        return False
    extension = word(block, 0x2E)
    if extension < 24 or 48 + extension >= len(block):
        return False
    extra = block[48:48 + extension]
    classes, parents, global_classes, overloads, scope_classes, module_classes, coverage = struct.unpack_from("<7H", extra, 0)
    browsers = word(extra, 18)
    base = 48 + extension
    cursor = base

    def take(count, size):
        nonlocal cursor
        end = cursor + count * size
        if end > len(block):
            return None
        start = cursor
        cursor = end
        return start

    symbol_at = take(symbols, 9)
    module_at = take(modules, 16)
    source_at = take(sources, 6)
    if take(lines, 4) is None:
        return False
    scope_at = take(scopes, 12)
    segment_at = take(segments, 16)
    correlation_at = take(correlations, 8)
    type_at = take(types, 8)
    member_at = take(members, 5)
    for count, size in ((classes, 11), (parents, 2), (overloads, 8),
                        (scope_classes, 4), (module_classes, 8), (browsers, 6)):
        if take(count, size) is None:
            return False
    if take(word(block, 0x2B), 1) is None:
        return False
    coverage_at = take(coverage, 2)
    segment_words = take(segments, 2)
    if None in (symbol_at, module_at, source_at, scope_at, segment_at,
                correlation_at, type_at, member_at, coverage_at, segment_words):
        return False
    module_words = take(modules, 4)
    if module_words is None or global_classes:
        return False
    pool_at = base + struct.unpack_from("<I", extra, 14)[0]
    if cursor != pool_at or pool_at + pool != len(block) or block[module_words:cursor].strip(b"\0"):
        return False
    for index in range(symbols):
        name, type_index = struct.unpack_from("<HH", block, symbol_at + index * 9)
        if name > names or type_index > types:
            return False
    for index in range(modules):
        if not 1 <= word(block, module_at + index * 16) <= names:
            return False
    for index in range(sources):
        if not 1 <= word(block, source_at + index * 6) <= names:
            return False
    for index in range(scopes):
        start, count, parent, function = struct.unpack_from("<4H", block, scope_at + index * 12)
        if start + count > symbols or parent > scopes:
            return False
        if function not in (0xFFFE, 0xFFFF) and function > symbols:
            return False
    for index in range(segments):
        module, _code_seg, _code_off, _code_len, scope_index, scope_count, corr_index, corr_count = struct.unpack_from(
            "<8H", block, segment_at + index * 16)
        if not 1 <= module <= modules:
            return False
        if scope_index + scope_count > scopes + 1 or corr_index + corr_count > correlations + 1:
            return False
        if not 1 <= word(block, segment_words + index * 2) <= symbols:
            return False
    for index in range(correlations):
        segment, source, line, line_count = struct.unpack_from("<4H", block, correlation_at + index * 8)
        if not 1 <= segment <= segments or not 1 <= source <= sources or line + line_count > lines + 1:
            return False
    for index in range(types):
        name = word(block, type_at + index * 8 + 1)
        if name & 0x8000 == 0 and name > names:
            return False
    for index in range(members):
        offset = member_at + index * 5
        if word(block, offset + 1) > names or word(block, offset + 3) & 0x0FFF > types:
            return False
    for index in range(coverage):
        if word(block, coverage_at + index * 2) > lines:
            return False
    return string_pool_reaches_end(block, pool, names)


def index_formula_matches(data):
    """True when a 256-by-256 index formula reproduces every byte."""
    if len(data) != 65536:
        return False

    def matches(formula):
        for index, value in enumerate(data):
            if value != (formula(index >> 8, index & 255) & 255):
                return False
        return True

    formulas = (
        lambda row, col: min(row, col),
        lambda row, col: max(row, col),
        lambda row, col: (row + col) // 2,
        lambda row, col: (row + col + 1) // 2,
        lambda row, col: (row * col) // 255,
        lambda row, col: (row * col) >> 8,
        lambda row, col: row + col,
        lambda row, col: row - col,
        lambda row, col: row | col,
        lambda row, col: row & col,
        lambda row, col: row ^ col,
    )
    return any(matches(formula) for formula in formulas)


# Finale scene whose palette each blend table is built from (LOLFINAL.TIM nested
# function 5 pairs RETURN and RICHARDF with BLEND.TAB, FACE and TAPPING with BLEND2.TAB).
BLEND_SCENES = {"BLEND.TAB": ("RETURN.CPS", "RICHARDF.CPS"), "BLEND2.TAB": ("FACE.CPS", "TAPPING.CPS")}
BLEND_MODEL_MATCH = 65532
BLEND_TRAILER = b"\xe4\xd5\x02\x00"


def palette_rgb(palette):
    """768 palette bytes as 256 (r, g, b) tuples on 6 bits."""
    return [tuple(value & 63 for value in palette[index * 3:index * 3 + 3]) for index in range(len(palette) // 3)]


def nearest_colour(colour, rgb):
    """Index of the nearest palette colour (squared distance); a tie goes to the later index."""
    best, chosen = 1 << 30, 0
    red, green, blue = colour
    for index, (r, g, b) in enumerate(rgb):
        distance = (red - r) ** 2 + (green - g) ** 2 + (blue - b) ** 2
        if distance <= best:
            best, chosen = distance, index
    return chosen


def blend_model(palette):
    """table[row*size+col] = nearest colour to ((row*22)>>6) + ((col*42)>>6) per channel."""
    rgb = palette_rgb(palette)
    size = len(rgb)
    rows = [tuple((value * 22) >> 6 for value in colour) for colour in rgb]
    cols = [tuple((value * 42) >> 6 for value in colour) for colour in rgb]
    cache, out = {}, bytearray()
    for row in rows:
        for col in cols:
            mixed = (row[0] + col[0], row[1] + col[1], row[2] + col[2])
            chosen = cache.get(mixed)
            if chosen is None:
                chosen = cache[mixed] = nearest_colour(mixed, rgb)
            out.append(chosen)
    return bytes(out)


def cps_palette(member):
    """The 768-byte palette of a CPS member, or None."""
    if len(member) >= 778 and struct.unpack_from("<H", member, 8)[0] == 768:
        return member[10:778]
    return None


def open_kind(filename, data):
    upper = filename.upper()
    if upper in ("BLEND.TAB", "BLEND2.TAB") and len(data) == 65536:
        return "blend"
    if upper == "FINALE.TDS" and data[:4] == SYMBOL:
        return "symbol"
    if upper == "LANDS.EXE":
        declared = mz_declared(data)
        if declared is not None and declared < len(data) and data[declared:declared + 4] == SYMBOL:
            return "symbol"
    return None


def fail(message):
    print("CHECK loose: " + message)
    return 1


def diagonal_indexes(table):
    return [table[index * 256 + index] for index in range(256)]


def diagonal_is_same_colour(palette, indexes):
    """True when each diagonal byte names a colour equal to that row's colour."""
    return diagonal_hits(palette, indexes) == 256


def diagonal_hits(palette, indexes):
    hits = 0
    for index, chosen in enumerate(indexes):
        if palette[index * 3:index * 3 + 3] == palette[chosen * 3:chosen * 3 + 3]:
            hits += 1
    return hits


def scroll_palette(root):
    """The 768-byte palette of GENERAL.PAK SCROLL.CPS, or None."""
    path = root / "GENERAL.PAK"
    if not path.is_file():
        return None
    data = path.read_bytes()
    for name, offset, size in L.pak_entries(data):
        if name.upper() == "SCROLL.CPS" and size >= 778 and offset + 778 <= len(data):
            if struct.unpack_from("<H", data, offset + 8)[0] == 768:
                return data[offset + 10:offset + 778]
    return None


def stored_palettes(root):
    """768-byte palettes: PAL and COL members, and picture palettes of that size."""
    found = []
    for path in sorted(item for item in root.rglob("*.PAK") if item.is_file()):
        data = path.read_bytes()
        for name, offset, size in L.pak_entries(data):
            upper = name.upper()
            if upper.endswith((".PAL", ".COL")) and size >= 768 and offset + 768 <= len(data):
                found.append(data[offset:offset + 768])
            elif size >= 778 and offset + 778 <= len(data) and offset + 778 <= offset + size:
                if struct.unpack_from("<H", data, offset + 8)[0] == 768 and not upper.endswith((".PAL", ".COL")):
                    found.append(data[offset + 10:offset + 778])
    return found


def has_mov_cx_256(blob):
    return MOV_CX_256 in blob


def check(data_dir):
    from pathlib import Path
    root = Path(data_dir)
    if not L.is_cd_layout(data_dir):
        print("CHECK loose: floppy layout, the loose-file count is taken on the CD edition")
        return 0
    read, left = {}, {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.suffix.lower() in (".pak", ".tlk"):
            continue
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        if covers(path.name, data):
            read[rel] = data
        else:
            kind = open_kind(path.name, data)
            if kind is None:
                return fail(f"{rel} is neither walked to the last byte nor a known open file")
            left[rel] = (kind, data)
    if set(read) != COVERED or set(left) != OPEN:
        return fail("the walked set or the open set differs from this CD edition")
    fonts = [read[f"{lang}/NEW6P.FNT"] for lang in ("ENG", "FRE", "GER")]
    if fonts[0] != fonts[1] or fonts[1] != fonts[2]:
        return fail("the three NEW6P.FNT copies differ")
    if not font_covers(fonts[0]):
        return fail("NEW6P.FNT parts do not tile the file")
    header, glyphs = fnt_reader.parse(fonts[0])
    if header["glyphs"] != 226 or header["height"] != 8 or len(fonts[0]) != 3213:
        return fail("NEW6P.FNT is not the 226-glyph height-8 font of 3213 bytes")
    for rel, (le, pages, last, data_pages, names, names_size) in LE_FIELDS.items():
        data = read[rel]
        fields = struct.unpack_from("<I", data, 0x3C)[0], *(
            struct.unpack_from("<I", data, le + offset)[0] for offset in (0x14, 0x2C, 0x80, 0x88, 0x8C))
        if fields != (le, pages, last, data_pages, names, names_size) or not le_covers(data):
            return fail(f"{rel} LE layout differs")
    for rel, (size, header_len) in MZ_EXACT.items():
        data = read[rel]
        if len(data) != size or header_bytes(data) != header_len or not mz_exact(data):
            return fail(f"{rel} MZ image does not equal the file")
    for rel in ("HARDRIVE/MAIN.EXE", "HARDRIVE/MAINW.EXE"):
        if not overlay_covers(read[rel]):
            return fail(f"{rel} overlay does not reach the last byte")
    main, mainw = read["HARDRIVE/MAIN.EXE"], read["HARDRIVE/MAINW.EXE"]
    if mz_declared(main) != 248896 or struct.unpack_from("<III", main, 248896 + 4) != (0x1A5F0, 0x2FC50, 0x127):
        return fail("MAIN.EXE FBOV header differs")
    for rel, (rows, name) in FBOV_ROWS.items():
        blob = read[rel]
        directory = struct.unpack_from("<I", blob, mz_declared(blob) + 8)[0]
        third = struct.unpack_from("<I", blob, mz_declared(blob) + 12)[0]
        walked, ends = fbov_rows(blob)
        if walked != rows or third != rows or not ends:
            return fail(f"{rel} FBOV directory is not {rows:#x} rows ending at the MZ image end")
        if blob[directory + 8 * rows:directory + 8 * rows + len(name)] != name:
            return fail(f"{rel} FBOV directory is not followed by its program name")
    if len(main) != 356928:
        return fail("MAIN.EXE length differs")
    if mz_declared(mainw) != 247328 or struct.unpack_from("<III", mainw, 247328 + 4) != (0x19B60, 0x2F710, 0x127):
        return fail("MAINW.EXE FBOV header differs")
    if len(mainw) != 352656:
        return fail("MAINW.EXE length differs")
    if read["HARDRIVE/LANDS.PIF"][0x24:0x24 + 9] != b"LOLCD.EXE" or read["HARDRIVE/DOSETUP.PIF"][0x24:0x24 + 9] != b"SETUP.EXE":
        return fail("PIF program name differs")
    if len(read["HARDRIVE/LANDS.PIF"]) != 545 or len(read["HARDRIVE/LANDS.ICO"]) != 766:
        return fail("PIF or icon length differs")
    inventory = read["FILEDATA.FDT"]
    for index, name, member in PALETTE_ROWS:
        row = inventory[index * 20:(index + 1) * 20]
        offset = struct.unpack_from("<I", row, 0)[0]
        if struct.unpack_from("<I", row, 4)[0] != 0x300 or struct.unpack_from("<I", row, 0x0C)[0] != member:
            return fail(f"inventory row {index} differs")
        if struct.unpack_from("<H", row, 0x12)[0] != 0x1000 or inventory[offset:offset + len(name)] != name:
            return fail(f"inventory row {index} name or flags differ")
    english_lm = read["HARDRIVE/ENG.LM"]
    english_dip = read["HARDRIVE/SETUPENG.DIP"]
    if struct.unpack_from("<H", english_lm, 0)[0] != 0x58 or len(english_lm) != 1794:
        return fail("ENG.LM table differs")
    if struct.unpack_from("<H", english_dip, 0)[0] != 0xD6 or len(english_dip) != 3881:
        return fail("SETUPENG.DIP table differs")
    dip_offsets = struct.unpack_from("<107H", english_dip, 0)
    second = english_dip[dip_offsets[1]:english_dip.find(b"\0", dip_offsets[1])]
    if second != b"File Write Error":
        return fail("SETUPENG.DIP string 1 differs")
    if not read["FRE/STATE.RST"].startswith(b"[edit-]\r\n") or len(read["FRE/STATE.RST"]) != 187:
        return fail("STATE.RST differs")
    blends = {}
    for rel, (kind, data) in left.items():
        if kind == "blend":
            blends.setdefault(Path(rel).name, []).append(data)
        else:
            return fail(f"unexpected open file {rel}")
    for rel, (size, declared) in LANDS.items():
        data = read[rel]
        if len(data) != size or mz_declared(data) != declared or header_bytes(data) != 10240:
            return fail(f"{rel} image differs")
        tail = data[declared:]
        if data[declared:declared + 4] != SYMBOL or not symbol_block_covers(tail):
            return fail(f"{rel} symbol tail does not tile")
        if len(tail) in struct.unpack_from("<16I", tail, 0):
            return fail(f"{rel} tail length is a header dword")
        if struct.unpack_from("<I", tail, 0x20)[0] != declared:
            return fail(f"{rel} tail +0x20 is not the file offset of the tail")
        if not string_pool_reaches_end(tail, POOL_LEN[rel], POOL_COUNT[rel]):
            return fail(f"{rel} string pool or its +8 count differs")
    for rel, size in TDS_SIZE.items():
        data = read[rel]
        if len(data) != size or not symbol_block_covers(data):
            return fail(f"{rel} symbol block does not tile")
        if len(data) in struct.unpack_from("<16I", data, 0):
            return fail(f"{rel} length is a header dword")
        if not string_pool_reaches_end(data, POOL_LEN[rel], POOL_COUNT[rel]):
            return fail(f"{rel} string pool or its +8 count differs")
    if len(blends["BLEND.TAB"]) != 3 or len(blends["BLEND2.TAB"]) != 3:
        return fail("blend table count differs")
    if blends["BLEND.TAB"][0] != blends["BLEND.TAB"][1] or blends["BLEND.TAB"][1] != blends["BLEND.TAB"][2]:
        return fail("BLEND.TAB copies differ")
    if blends["BLEND2.TAB"][0] != blends["BLEND2.TAB"][1] or blends["BLEND2.TAB"][1] != blends["BLEND2.TAB"][2]:
        return fail("BLEND2.TAB copies differ")
    if blends["BLEND.TAB"][0] == blends["BLEND2.TAB"][0]:
        return fail("BLEND.TAB and BLEND2.TAB are the same bytes")
    if not blends["BLEND.TAB"][0].startswith(BLEND_HEAD) or not blends["BLEND2.TAB"][0].startswith(BLEND2_HEAD):
        return fail("blend table head differs")
    if blends["BLEND2.TAB"][0][:256] != blends["BLEND2.TAB"][0][256:512]:
        return fail("BLEND2.TAB first two rows differ")
    if blends["BLEND.TAB"][0][:256] == blends["BLEND.TAB"][0][256:512]:
        return fail("BLEND.TAB first two rows are equal")
    if index_formula_matches(blends["BLEND.TAB"][0]) or index_formula_matches(blends["BLEND2.TAB"][0]):
        return fail("a blend table matches a 256-by-256 index formula")
    finale1 = L.read_pak(str(root / "ENG" / "FINALE1.PAK"))
    model_rates = []
    for name, scenes in BLEND_SCENES.items():
        palette = cps_palette(finale1.get(scenes[0], b""))
        if palette is None or any(cps_palette(finale1.get(other, b"")) != palette for other in scenes[1:]):
            return fail(f"{name} scene palettes differ or are missing")
        table, model = blends[name][0], blend_model(palette)
        same = sum(a == b for a, b in zip(table, model))
        if same != BLEND_MODEL_MATCH or table[:BLEND_MODEL_MATCH] != model[:BLEND_MODEL_MATCH]:
            return fail(f"{name} self-blend of {scenes[0]} matches {same} bytes, not the first {BLEND_MODEL_MATCH}")
        if table[BLEND_MODEL_MATCH:] != BLEND_TRAILER:
            return fail(f"{name} last four bytes are not E4 D5 02 00")
        model_rates.append(f"{name} {same} of 65536 from {scenes[0]}")
    palettes = stored_palettes(root)
    if len(palettes) != STORED_PALETTES:
        return fail(f"stored palette count is {len(palettes)}, not {STORED_PALETTES}")
    if len(set(palettes)) != DISTINCT_PALETTES:
        return fail(f"stored palettes are {len(set(palettes))} distinct, not {DISTINCT_PALETTES}")
    scroll = scroll_palette(root)
    if scroll is None:
        return fail("GENERAL.PAK SCROLL.CPS has no 768-byte palette")
    for name in ("BLEND.TAB", "BLEND2.TAB"):
        indexes = diagonal_indexes(blends[name][0])
        if any(diagonal_is_same_colour(palette, indexes) for palette in palettes):
            return fail(f"a stored palette has the {name} diagonal")
        if diagonal_hits(scroll, indexes) != SCROLL_DIAGONAL[name]:
            return fail(f"SCROLL.CPS keeps a different number of {name} diagonal colours")
    ending = b"FILECHNG\x00new_size\x00.\\FILECHNG.C\x00"
    lands = read["ENG/LANDS.EXE"]
    if not read["ENG/FINALE.TDS"].endswith(ending) or not lands[mz_declared(lands):].endswith(ending):
        return fail("English symbol block does not end with FILECHNG.C")
    for rel, offset, needle in NAME_PINS:
        blob = read[rel] if rel in read else left[rel][1]
        if blob[offset:offset + len(needle)] != needle:
            return fail(f"name pin {rel}+{offset:#x} differs")
    install_path = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "INSTALL.EXE")
    if not os.path.isfile(install_path):
        return fail("INSTALL.EXE is not beside DATA")
    install = Path(install_path).read_bytes()
    if len(install) != 134819:
        return fail("INSTALL.EXE length differs")
    readme_path = os.path.join(os.path.dirname(os.path.abspath(data_dir)), "README.ENG")
    if not os.path.isfile(readme_path):
        return fail("README.ENG is not beside DATA")
    with open(readme_path, "rb") as handle:
        handle.seek(0x72)
        if handle.read(8) != b"LANDS OF":
            return fail("README.ENG+0x72 differs")
        handle.seek(0x10A)
        if handle.read(16) != b"January 10, 1994":
            return fail("README.ENG+0x10A differs")
    for offset, needle in INSTALL_PINS:
        if install[offset:offset + len(needle)] != needle:
            return fail(f"installer pin +{offset:#x} differs")
    for offset, needle in INSTALL_BLEND:
        if install[offset:offset + len(needle)] != needle:
            return fail(f"installer blend string +{offset:#x} differs")
    programs = [("INSTALL.EXE", install)]
    for rel in ("ENG/FINALE.EXE", "FRE/FINALE.EXE", "GER/FINALE.EXE"):
        programs.append((rel, read[rel]))
    for rel, (_size, declared) in LANDS.items():
        programs.append((rel + " image", read[rel][:declared]))
    for label, blob in programs:
        if has_mov_cx_256(blob):
            return fail(f"{label} contains mov cx, 256")
    finale2 = (root / "ENG" / "FINALE2.PAK").read_bytes()
    for offset, needle in FINALE_BLEND:
        if finale2[offset:offset + len(needle)] != needle:
            return fail(f"ENG/FINALE2.PAK+{offset:#x} differs")
    visbios = read["HARDRIVE/VISBIOS.COM"]
    for offset, needle in VISBIOS_PINS:
        if visbios[offset:offset + len(needle)] != needle:
            return fail(f"VISBIOS.COM+{offset:#x} differs")
    scanned = [(root / rel).read_bytes().lower() for rel in ABSENT_FROM]
    scanned.append(install.lower())
    for needle in ABSENT_NEEDLES:
        if any(needle in blob for blob in scanned):
            return fail(f"{needle.decode()} occurs in a scanned program")
    raw = [(root / rel).read_bytes() for rel in ABSENT_FROM] + [install]
    if any(BLEND_HEAD in blob or BLEND2_HEAD in blob for blob in raw):
        return fail("a blend-table head occurs in a scanned program")
    print("CHECK loose: 31 files reach the last byte "
          "(3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 5 mz, 2 le, 2 overlay, 1 text, 1 com, "
          "3 symbol, 3 mz plus symbol tail); "
          "6 open (6 blend tables; palette self-blend 22/42 matches "
          + ", ".join(model_rates) + ", last four bytes E4 D5 02 00 open)")
    return 0


def main():
    parser = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    L.add_data_arg(parser)
    args = parser.parse_args()
    if not args.check:
        parser.print_help()
        return 2
    return check(args.data)


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
