#!/usr/bin/env python3
"""Shared readers for the Lands of Lore 1 (DOS) data files.

Small, dependency-free helpers used by the *_reader.py tools:

  - PAK container listing and member extraction
  - TLK container listing
  - Frame4 / LCW decompression (Westwood "format 80")
  - CPS / "bitmap" header parsing (also used by CMZ, VCN, VMP)
  - locating a member file anywhere in the game DATA folder

Sources (ScummVM, engines/kyra/):
  PAK  resource/resource_intern.cpp:246-380  ResLoaderPak::isLoadable / load
  TLK  resource/resource_intern.cpp:118-132, 459-492  TlkArchive / ResLoaderTlk
  LCW  graphics/screen.cpp:2484-2530  Screen::decodeFrame4
  CPS  graphics/screen.cpp:3355-3401  Screen::loadBitmap

The game DATA folder defaults to $LOL1_DATA, else the project reference
corpus path below. No game data is stored in this repository.
"""

import os
import struct

DEFAULT_DATA = os.environ.get(
    "LOL1_DATA", "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA")


# --------------------------------------------------------------------------
# PAK
# --------------------------------------------------------------------------

def pak_entries(data):
    """Return [(name, offset, size)] for a PAK file image (bytes).

    Layout (ResLoaderPak::load): repeated [uint32 LE offset][NUL-terminated
    name]; the list ends at an empty name or when the next offset equals the
    file size. Each member runs from its offset to the next member's offset.
    """
    entries = []
    pos = 0
    size = len(data)
    offset = struct.unpack_from("<I", data, 0)[0]
    pos = 4
    names = []
    while pos < size:
        end = data.index(b"\0", pos)
        name = data[pos:end].decode("latin-1")
        pos = end + 1
        if not name:
            break
        names.append((name, offset))
        if pos + 4 > size:
            break
        offset = struct.unpack_from("<I", data, pos)[0]
        pos += 4
        if offset == 0 or offset == size:
            break
    for i, (name, off) in enumerate(names):
        nxt = names[i + 1][1] if i + 1 < len(names) else size
        entries.append((name, off, nxt - off))
    return entries


def read_pak(path):
    with open(path, "rb") as f:
        data = f.read()
    return {name.upper(): data[off:off + sz]
            for name, off, sz in pak_entries(data)}


def tlk_entries(data):
    """Return [(id, offset, size)] for a TLK file image.

    Layout (ResLoaderTlk::load, TlkArchive::createReadStreamForMember):
    uint16 count; count x (uint32 id, uint32 offset); at each offset a
    uint32 size followed by `size` bytes, served as "%08u.AUD".
    """
    count = struct.unpack_from("<H", data, 0)[0]
    out = []
    for i in range(count):
        fid, off = struct.unpack_from("<II", data, 2 + i * 8)
        sz = struct.unpack_from("<I", data, off)[0]
        out.append((fid, off + 4, sz))
    return out


# --------------------------------------------------------------------------
# Locating files
# --------------------------------------------------------------------------

def list_paks(data_dir=DEFAULT_DATA):
    return sorted(p for p in os.listdir(data_dir) if p.upper().endswith(".PAK"))


def find_member(name, data_dir=DEFAULT_DATA, pak=None):
    """Return (pak_name, bytes) for the first PAK holding `name`.

    `pak` restricts the search to one PAK file. A loose file of that name in
    the DATA folder is returned with pak_name None.
    """
    name = name.upper()
    loose = os.path.join(data_dir, name)
    if pak is None and os.path.isfile(loose):
        with open(loose, "rb") as f:
            return None, f.read()
    for p in ([pak] if pak else list_paks(data_dir)):
        members = read_pak(os.path.join(data_dir, p))
        if name in members:
            return p, members[name]
    raise FileNotFoundError(f"{name} not found in {data_dir}")


def find_all(suffix, data_dir=DEFAULT_DATA):
    """Yield (pak_name, member_name, bytes) for every member ending in suffix."""
    suffix = suffix.upper()
    for p in list_paks(data_dir):
        for name, blob in read_pak(os.path.join(data_dir, p)).items():
            if name.endswith(suffix):
                yield p, name, blob


# --------------------------------------------------------------------------
# Frame4 / LCW
# --------------------------------------------------------------------------

def decode_frame4(src, dst_size):
    """Port of Screen::decodeFrame4 (graphics/screen.cpp:2484-2530).

    Short copies (bit7 clear) are relative to the output position; medium
    (0xC0-0xFD) and long (0xFF) copies are absolute from output start;
    0xFE = fill; 0x81-0xBF = literal run; 0x80 = end.
    """
    dst = bytearray()
    sp = 0
    n = len(src)
    while len(dst) < dst_size and sp < n:
        count = dst_size - len(dst)
        code = src[sp]; sp += 1
        if not code & 0x80:
            ln = min(count, (code >> 4) + 3)
            offs = ((code & 0x0F) << 8) | src[sp]; sp += 1
            p = len(dst) - offs
            for i in range(ln):
                dst.append(dst[p + i])
        elif code & 0x40:
            ln = (code & 0x3F) + 3
            if code == 0xFE:
                ln = min(count, src[sp] | src[sp + 1] << 8); sp += 2
                dst.extend(bytes([src[sp]]) * ln); sp += 1
            else:
                if code == 0xFF:
                    ln = src[sp] | src[sp + 1] << 8; sp += 2
                offs = src[sp] | src[sp + 1] << 8; sp += 2
                ln = min(ln, count)
                for i in range(ln):
                    dst.append(dst[offs + i])
        elif code != 0x80:
            ln = min(count, code & 0x3F)
            dst.extend(src[sp:sp + ln]); sp += ln
        else:
            break
    return bytes(dst)


# --------------------------------------------------------------------------
# CPS-style bitmap container (CPS, CMZ, VCN, VMP all go through loadBitmap)
# --------------------------------------------------------------------------

def bitmap_header(data):
    """Parse the 10-byte header read by Screen::loadBitmap.

    +0 uint16 size field (not read by loadBitmap)
    +2 uint8  compression type (0 raw, 1, 3, 4 = Frame4)
    +4 uint32 uncompressed size
    +8 uint16 palette size (palette bytes follow the header)
    """
    return {
        "size_field": struct.unpack_from("<H", data, 0)[0],
        "comp_type": data[2],
        "byte3": data[3],
        "uncompressed_size": struct.unpack_from("<I", data, 4)[0],
        "palette_size": struct.unpack_from("<H", data, 8)[0],
    }


def load_bitmap(data):
    """Return (header, palette_bytes, pixels) like Screen::loadBitmap."""
    h = bitmap_header(data)
    pal = data[10:10 + h["palette_size"]]
    payload = data[10 + h["palette_size"]:]
    if h["comp_type"] == 0:
        pixels = payload[:h["uncompressed_size"]]
    elif h["comp_type"] == 4:
        pixels = decode_frame4(payload, h["uncompressed_size"])
    else:
        raise ValueError(f"compression type {h['comp_type']} not handled")
    return h, pal, pixels


def vga_palette(raw):
    """6-bit VGA RGB triples -> list of 8-bit (r, g, b)."""
    return [((raw[i] & 63) * 255 // 63, (raw[i + 1] & 63) * 255 // 63,
             (raw[i + 2] & 63) * 255 // 63) for i in range(0, len(raw) - 2, 3)]


def add_data_arg(parser):
    parser.add_argument("--data", default=DEFAULT_DATA,
                        help="game DATA folder (default: $LOL1_DATA or %(default)s)")
    parser.add_argument("--pak", default=None,
                        help="search only this PAK (default: all PAKs, loose files first)")


# --------------------------------------------------------------------------
# Shared command line for the older tools
# --------------------------------------------------------------------------

REPO_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def tool_args(doc, out_help="write the JSON result here (default: print a summary only)"):
    """argparse parser with --data, --pak, --out and --check."""
    import argparse
    ap = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_data_arg(ap)
    ap.add_argument("--out", help=out_help)
    ap.add_argument("--check", action="store_true",
                    help="parse the whole corpus and compare with the repo's data/ JSON where one exists; one line, exit 1 on mismatch")
    return ap


def level_member(level, ext, data_dir=DEFAULT_DATA):
    """Bytes of LEVELn.<ext> from Lnn.PAK, or None when absent."""
    try:
        return find_member(f"LEVEL{level}.{ext}", data_dir, f"L{level:02d}.PAK")[1]
    except (FileNotFoundError, OSError):
        return None


def repo_json(name):
    import json
    p = os.path.join(REPO_DATA, name)
    if not os.path.isfile(p):
        return None
    with open(p) as f:
        return json.load(f)


def write_json(path, obj):
    import json
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print("wrote", path)
