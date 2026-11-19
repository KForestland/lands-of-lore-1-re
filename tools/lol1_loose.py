#!/usr/bin/env python3
"""Walk the CD DATA files that are not PAK or TLK archives.

A file counts as read when every byte sits in a header, a directory or an
entry. The twelve files that fail that walk stay unread: the check names
them and pins the signature that was actually found.

  lol1_loose.py --check
"""
import argparse
import os
import struct
import sys

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
}
OPEN = {
    "ENG/BLEND.TAB", "FRE/BLEND.TAB", "GER/BLEND.TAB",
    "ENG/BLEND2.TAB", "FRE/BLEND2.TAB", "GER/BLEND2.TAB",
    "ENG/FINALE.TDS", "FRE/FINALE.TDS", "GER/FINALE.TDS",
    "ENG/LANDS.EXE", "FRE/LANDS.EXE", "GER/LANDS.EXE",
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
SYMBOL = b"\xfb\x52\x10\x03"
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
    if suffix == "EXE":
        return mz_exact(data) or overlay_covers(data)
    return False


def covered(path):
    path = L_path(path)
    return covers(path.name, path.read_bytes())


def L_path(path):
    from pathlib import Path
    return path if hasattr(path, "read_bytes") else Path(path)


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
        elif rel in LANDS:
            size, declared = LANDS[rel]
            if len(data) != size or mz_declared(data) != declared or data[declared:declared + 4] != SYMBOL:
                return fail(f"{rel} tail differs")
            if header_bytes(data) != 10240:
                return fail(f"{rel} header differs")
            tail = data[declared:]
            if len(tail) in struct.unpack_from("<16I", tail, 0):
                return fail(f"{rel} tail length is a header dword")
        elif rel in TDS_SIZE:
            if len(data) != TDS_SIZE[rel] or data[:4] != SYMBOL:
                return fail(f"{rel} differs")
            if len(data) in struct.unpack_from("<16I", data, 0):
                return fail(f"{rel} length is a header dword")
        else:
            return fail(f"unexpected open file {rel}")
    if len(blends["BLEND.TAB"]) != 3 or len(blends["BLEND2.TAB"]) != 3:
        return fail("blend table count differs")
    if blends["BLEND.TAB"][0] != blends["BLEND.TAB"][1] or blends["BLEND.TAB"][1] != blends["BLEND.TAB"][2]:
        return fail("BLEND.TAB copies differ")
    if blends["BLEND2.TAB"][0] != blends["BLEND2.TAB"][1] or blends["BLEND2.TAB"][1] != blends["BLEND2.TAB"][2]:
        return fail("BLEND2.TAB copies differ")
    if blends["BLEND.TAB"][0] == blends["BLEND2.TAB"][0]:
        return fail("BLEND.TAB and BLEND2.TAB are the same bytes")
    ending = b"FILECHNG\x00new_size\x00.\\FILECHNG.C\x00"
    lands = left["ENG/LANDS.EXE"][1]
    if not left["ENG/FINALE.TDS"][1].endswith(ending) or not lands[mz_declared(lands):].endswith(ending):
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
    for offset, needle in INSTALL_PINS:
        if install[offset:offset + len(needle)] != needle:
            return fail(f"installer pin +{offset:#x} differs")
    for offset, needle in INSTALL_BLEND:
        if install[offset:offset + len(needle)] != needle:
            return fail(f"installer blend string +{offset:#x} differs")
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
    print("CHECK loose: 25 files reach the last byte "
          "(3 font, 6 string table, 1 inventory, 2 icon, 2 pif, 5 mz, 2 le, 2 overlay, 1 text, 1 com); "
          "12 open (6 blend tables, 3 symbol files, 3 LANDS tails)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    L.add_data_arg(parser)
    args = parser.parse_args()
    if not args.check:
        parser.print_help()
        return 2
    return check(args.data)


if __name__ == "__main__":
    sys.exit(main())
