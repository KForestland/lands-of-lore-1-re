#!/usr/bin/env python3
"""Check selected format-page offsets against the readers that decode them."""
from pathlib import Path
import re
import struct

from cli_errors import ReaderArgumentParser, run_cli
from doc_links import prose_lines
import dat_reader
import lol1lib as L
import shp_renderer
import wll_parser
import wsa_extract

DOCS = Path(__file__).resolve().parents[1] / "docs"
NUMBER = re.compile(r"0x[0-9a-f]+|[0-9]+", re.I)


def offsets(cell):
    return tuple(int(token, 16 if token.lower().startswith("0x") else 10)
                 for token in NUMBER.findall(cell))


def documented(page, label_column, starts_with, columns=(0,)):
    lines = prose_lines((DOCS / page).read_text(encoding="utf-8"))
    rows = [tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
            for line in lines if line.lstrip().startswith("|")]
    matches = [row for row in rows
               if len(row) > label_column and row[label_column].startswith(starts_with)]
    if len(matches) != 1:
        raise ValueError(f"{page}: expected one layout row for {starts_with}")
    try:
        observed = tuple(value for index in columns for value in offsets(matches[0][index]))
    except IndexError as error:
        raise ValueError(f"{page}: incomplete layout row for {starts_with}") from error
    if not observed:
        raise ValueError(f"{page}: {starts_with}: no documented offset")
    return observed[0]


def probe(page, field, offset, size, read):
    """Place a marker at the documented offset of a synthetic file and ask
    the reader for the field. A wrong offset on the page, or a reader that
    reads the field elsewhere, returns something other than the marker."""
    buffer = bytearray(256)
    marker = bytes(range(0xA1, 0xA1 + size))
    buffer[offset:offset + size] = marker
    try:
        got = read(buffer, marker)
    except (ValueError, IndexError, KeyError, struct.error) as error:
        got = f"error {error}"
    if got is not True:
        raise ValueError(f"{page}: {field}: documented +{offset:#x}, but the reader does not read it there"
                         + (f" ({got})" if got is not False else ""))


def check():
    # Each row is a documented offset on a format page and the reader function
    # that decodes that field. See the original examples in these six pages.
    rows = (
        ("pak", "name of member 0", 3,
         lambda b, m: [e[0] for e in L.pak_entries(struct.pack("<I", 64) + bytes(b[4:64]) + b"x")][:1] == [m.decode("latin-1")]),
        ("cps", "uncompressed size (", 4,
         lambda b, m: L.bitmap_header(bytes(b))["uncompressed_size"] == struct.unpack("<I", m)[0]),
        ("wsa", "delta buffer size", 2,
         lambda b, m: wsa_extract.parse(bytes(b))["delta_buffer"] == struct.unpack("<H", m)[0]),
        ("shp", "shape offsets,", 4,
         lambda b, m: shp_renderer.shape_offsets(struct.pack("<H", 1) + bytes(b[2:]))[0] == struct.unpack("<I", m)[0]),
        ("dat", "scaleFlag", 10,
         lambda b, m: dat_reader.parse(struct.pack("<H", 1) + bytes(b[:72]))[1][0]["scaleFlag"] == list(m)),
        ("wll", "`_wllAutomapData[c]`", 1,
         lambda b, m: wll_parser.parse_wll(struct.pack("<H", 0) + bytes(b[:12]))["records"][0]["automap_data"] == m[0]),
    )
    for page, label, size, read in rows:
        page = "formats/" + page + ".md"
        probe(page, label, documented(page, 2, label), size, read)
    print("CHECK format offsets: six documented PAK, CPS, WSA, SHP, DAT and WLL fields are where the readers read them")

def main():
    parser = ReaderArgumentParser(description=__doc__)
    parser.add_argument("--data", help="accepted for check_all compatibility")
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    check()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
