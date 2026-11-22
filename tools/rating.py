#!/usr/bin/env python3
"""Read original LoL1 files and documentation to compute the rating.

  rating.py --data DAT          # print the rating lines
  rating.py --data DAT --check  # also require README.md and docs/STATUS.md to carry them

The lines are explained in docs/HOW_WE_RATE.md:
  Files read      DATA files whose every byte a reader here accounts for, by count and by bytes
  Rules traced    evidence labels on the current pages: CONFIRMED against UNCONFIRMED
  Running game    probes on docs/NEEDS_A_RUNNING_GAME.md answered, out of all probes there
                  and how many of the answered ones rest on edited saves only
  Open questions  the state words of the At-a-glance table in docs/OPEN_QUESTIONS.md
"""
from cli_errors import run_cli
import re
from pathlib import Path

import os
import struct

import lol1_loose
import lol1lib
from page_facts import coverage

ROOT = Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- rating:begin -->", "<!-- rating:end -->"


def pak_covered(path):
    """A PAK (and a CD speech TLK, which is a PAK) counts when its name/offset directory ends at the first
    member (after an all-zero terminator of at most 8 bytes) and the members, each running to the next
    offset, reach the end of the file."""
    data = path.read_bytes()
    size = len(data)
    if size < 5:
        return False
    first = offset = struct.unpack_from("<I", data, 0)[0]
    position, offsets = 4, []
    while position < size:
        end = data.find(b"\0", position)
        if end < 0:
            return False
        name, position = data[position:end], end + 1
        if not name:
            break
        offsets.append(offset)
        if position + 4 > size:
            return False
        offset = struct.unpack_from("<I", data, position)[0]
        position += 4
        if offset in (0, size):
            break
    if not offsets or offsets[0] != first or position > first or first - position > 8:
        return False
    if data[position:first].strip(b"\0"):
        return False
    return all(b > a for a, b in zip(offsets, offsets[1:] + [size]))


def files_read(data_dir):
    """Every file under the DATA folder, sub-folders included.

    PAK and TLK archives count when pak_covered() holds. Any other file counts when
    lol1_loose.covered() walks it to the last byte, on the CD layout only (the
    loose walk and its pinned check are made for the CD DATA folder; a floppy
    copy keeps the PAK/TLK count alone).
    """
    loose = lol1lib.is_cd_layout(data_dir)
    total = read = total_bytes = read_bytes = 0
    for path in sorted(p for p in Path(data_dir).rglob("*") if p.is_file()):
        size = path.stat().st_size
        total += 1
        total_bytes += size
        if path.suffix.lower() in (".pak", ".tlk") and pak_covered(path):
            read += 1
            read_bytes += size
        elif loose and lol1_loose.covered(path):
            read += 1
            read_bytes += size
    return read, total, read_bytes, total_bytes


def history(text):
    return any(line.startswith("> **History") for line in text.splitlines()[:6])


def labels():
    confirmed = unconfirmed = pages = 0
    for page in sorted((ROOT / "docs").rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        if history(text) or page.name == "HOW_WE_RATE.md":
            continue
        text = re.sub(re.escape(BEGIN) + ".*?" + re.escape(END), "", text, flags=re.S)  # the rating block itself
        if page.name == "GLOSSARY.md":
            text = ""  # the glossary only defines the label words; its page still counts
        pages += 1
        confirmed += len(re.findall(r"(?<![A-Z])(?:CONFIRMED|PROVEN)\b", text))
        unconfirmed += len(re.findall(r"\b(?:UNCONFIRMED|UNKNOWN)\b", text))
    return confirmed, unconfirmed, pages


def edited_only(body):
    """An answered probe rests on edited saves only when its section says "edited-save run" and none of its
    bold labels says "answered" without "edited-save" (a run on a game-written save)."""
    if "edited-save run" not in "\n".join(body):
        return False
    labels = [line[2:].split("**", 1)[0].lower() for line in body if line.startswith("**")]
    return not any("answered" in label and "edited-save" not in label for label in labels)


def probes():
    """Probe headings under "Answered probes" and "Remaining probes", and how many answered ones rest on
    edited saves only (edited_only)."""
    text = (ROOT / "docs" / "NEEDS_A_RUNNING_GAME.md").read_text(encoding="utf-8")
    counts, section, bodies = {"answered": 0, "remaining": 0}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            low = line.lower()
            section = "answered" if "answered probes" in low else "remaining" if "remaining probes" in low else None
        elif line.startswith("### ") and section:
            counts[section] += 1
            if section == "answered":
                bodies.append([])
                continue
        if section == "answered" and bodies and not line.startswith("## "):
            bodies[-1].append(line)
    edited = sum(edited_only(body) for body in bodies)
    return counts["answered"], counts["answered"] + counts["remaining"], edited


def questions():
    text = (ROOT / "docs" / "OPEN_QUESTIONS.md").read_text(encoding="utf-8")
    table = text.split("## At a glance", 1)[1].split("\n## ", 1)[0]
    states = [row.split("|")[2].strip() for row in table.splitlines() if re.match(r"\| Q\d+[a-z]? \|", row)]
    answered = sum(s.startswith("Answered") for s in states)
    mostly = sum(s.startswith("Mostly") for s in states)
    partly = sum(s.startswith("Partly") for s in states)
    return answered, mostly, partly, len(states)


def rating(data_dir):
    read, total, read_bytes, total_bytes = files_read(data_dir)
    confirmed, unconfirmed, pages = labels()
    seen, needed, edited = probes()
    answered, mostly, partly, count = questions()
    folder = "the CD `DATA` folder" if lol1lib.is_cd_layout(data_dir) else "the floppy game folder"
    return [
        f"- **Files read:** {read} of {total} files in {folder} ({read_bytes / 2**20:,.1f} of {total_bytes / 2**20:,.1f} MiB) have their whole layout read by a tool here: every byte belongs to a known header, directory or entry (what is inside an entry may still be only partly understood).",
        f"- **Rules traced:** the pages mark {confirmed:,} statements CONFIRMED (labelled as proved with a cited address or offset) and {unconfirmed:,} UNCONFIRMED (a reading not yet proved), on {pages} current pages; old notes kept as history are not counted.",
        f"- **Seen in the running game:** {seen} of {needed} probes that need the original game running are answered (a question can have more than one probe); {edited} of them rest on edited saves only.",
        f"- **Open questions:** {count} numbered questions: {answered} answered, {mostly} mostly answered, {partly} partly answered.",
        f"- **Page facts:** {coverage()} with byte witnesses. The rest are inventoried so changes can be reviewed.",
    ]


def block_of(path):
    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        return None
    return [line for line in text.split(BEGIN, 1)[1].split(END, 1)[0].splitlines() if line.strip()]


def main():
    parser = lol1lib.tool_args(__doc__)
    args = parser.parse_args()
    if args.out:
        parser.error("prints only")
    try:
        lines = rating(args.data)
        if not args.check:
            print("\n".join(lines))
            return 0
        if not lol1lib.is_cd_layout(args.data):
            print("CHECK rating: the rating is counted on the CD edition; this copy is not compared")
            return 0
        stale = [p.name for p in (ROOT / "README.md", ROOT / "docs" / "STATUS.md") if block_of(p) != lines]
        if stale:
            raise ValueError(f"rating block differs from the counts in {', '.join(stale)}; run rating.py and copy the lines")
        print("CHECK rating: README.md and docs/STATUS.md carry the counted rating (" +
              "; ".join(re.sub(r"[*`]", "", l[2:]).split(":", 1)[0] for l in lines) + ")")
        return 0
    except (OSError, ValueError, IndexError) as error:
        parser.exit(1, f"rating: {error}\n")


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
