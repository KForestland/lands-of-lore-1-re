#!/usr/bin/env python3
"""Read the EMC2 (.INF/.INI) and TIM scripts in the PAK archives and loose .TIM files
of a LoL1 DATA folder, or one lossless listing, and assemble listings back to the
original bytes.

  lol1_script_writer.py --check --data DATA     # every script rebuilds byte for byte
  lol1_script_writer.py LISTING.json --out NEW  # assemble one listing into a new file

Listings come from emc2_decompile.py --assembly or parse_tim.py --list NAME --assembly.
"""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import struct

from cli_errors import ReaderArgumentParser, run_cli
import emc2_decompile as emc
import lol1lib as L
import parse_tim as tim


def binary_strings(payload, byteorder):
    first, = struct.unpack_from(byteorder + "H", payload)
    if first < 2 or first & 1 or first >= len(payload):
        raise ValueError("invalid string directory start")
    offsets = list(struct.unpack_from(f"{byteorder}{first // 2}H", payload))
    if any(offset < first or offset >= len(payload) or payload.find(b"\0", offset) < 0 for offset in offsets):
        raise ValueError("string offset outside a NUL-terminated string")
    return {"offsets": offsets, "strings": payload[first:].decode("latin-1").split("\0")}


def write_strings(fields, byteorder):
    offsets = fields["offsets"]
    payload = struct.pack(f"{byteorder}{len(offsets)}H", *offsets)
    payload += "\0".join(fields["strings"]).encode("latin-1")
    if binary_strings(payload, byteorder) != fields:
        raise ValueError("rebuilt string directory does not agree with its fields")
    return payload


def emc_rows(script):
    words = script.words
    records = {at: {"header": words[at]} for at in script.entries}
    for ins in script.instructions:
        at, opcode, arg = ins.address, ins.opcode, ins.argument
        word = words[at]
        mode = 0x8000 if word & 0x8000 else word & 0x6000
        fields = {"opcode": opcode, "mnemonic": emc.OPCODES[opcode], "argument": arg, "mode": mode}
        if not mode & 0xC000:
            fields["low"] = word & 255
            if mode == 0x2000 and opcode == 14:
                fields["syscall_high"] = words[at + 1] >> 8
        records[at] = fields
    return [{"at": at, **record} for at, record in sorted(records.items())]


def tim_rows(payload):
    words = list(word for word, in struct.iter_unpack("<H", payload))
    rows = []
    at = 0
    found, _ = tim.walk_avtl(words)
    entries = tim.tim_function_count(words)
    for _, address, length, delay, opcode, args in sorted(found, key=lambda record: record[1]):
        if address < at:
            continue
        if address > at:
            rows.append({"at": at, "unread": words[at:address]})
        rows.append({"at": address, "delay": delay, "opcode": opcode, "operands": args})
        at = address + length
    if at < len(words):
        rows.append({"at": at, "unread": words[at:]})
    if rows and "unread" in rows[0] and len(rows[0]["unread"]) >= entries:
        remaining = rows[0].pop("unread")
        rows[0]["entries"] = remaining[:entries]
        if remaining[entries:]:
            rows.insert(1, {"at": entries, "unread": remaining[entries:]})
    return rows


def listing(blob):
    if len(blob) < 12 or blob[:4] != b"FORM" or blob[8:12] not in (b"EMC2", b"AVFS"):
        raise ValueError("expected EMC2 or AVFS FORM")
    form = blob[8:12].decode("ascii")
    bias = len(blob) - struct.unpack_from(">I", blob, 4)[0]
    if bias not in (0, 8, 12):
        raise ValueError("unrecognized FORM length convention")
    code = emc.read_script(blob) if form == "EMC2" else None
    chunks = []
    at = 12
    while at < len(blob):
        tag, length = struct.unpack_from(">4sI", blob, at)
        tag = tag.decode("ascii")
        start, end = at + 8, at + 8 + length
        if end > len(blob):
            raise ValueError("chunk outside its FORM")
        pad = blob[end:end + (length & 1)]
        payload = blob[start:end]
        if tag == "ORDR" and code:
            fields = list(emc.be_words(payload))
        elif tag == "DATA" and code:
            fields = emc_rows(code)
        elif tag == "AVTL" and form == "AVFS":
            fields = tim_rows(payload)
        elif tag == "TEXT":
            fields = binary_strings(payload, ">" if code else "<")
        else:
            fields = payload.hex()
        chunks.append({"tag": tag, "pad": pad.hex(), "fields": fields})
        at = end + len(pad)
    return {"form": form, "length_bias": bias, "chunks": chunks}


def assemble_code(records, form):
    words = []
    for record in records:
        if record["at"] != len(words):
            raise ValueError("script row address disagrees with emitted word count")
        if form == "AVFS":
            if "entries" in record:
                words.extend(record["entries"])
            elif "unread" in record:
                words.extend(record["unread"])
            else:
                args = record["operands"]
                words.extend((3 + len(args), record["delay"], record["opcode"], *args))
        elif "header" in record:
            words.append(record["header"])
        else:
            mode, opcode, arg = record["mode"], record["opcode"], record["argument"]
            if not 0 <= opcode < len(emc.OPCODES) or emc.OPCODES[opcode] != record["mnemonic"]:
                raise ValueError("EMC2 opcode and mnemonic disagree")
            if mode & 0x8000:
                if mode != 0x8000 or opcode or not 0 <= arg <= 0x7FFF:
                    raise ValueError("invalid embedded EMC2 jump")
                words.append(mode | arg)
            else:
                low = arg & 255 if mode & 0x4000 else record["low"]
                words.append(mode | (opcode << 8) | low)
                if mode == 0x2000:
                    operand = ((record["syscall_high"] << 8) | (arg & 255)) if opcode == 14 else arg & 0xFFFF
                    words.append(operand)
    endian = ">" if form == "EMC2" else "<"
    return struct.pack(f"{endian}{len(words)}H", *words)


def assemble(source):
    form = source["form"]
    bias = source["length_bias"]
    if form not in ("EMC2", "AVFS") or bias not in (0, 8, 12):
        raise ValueError("invalid script listing header")
    body = bytearray(form.encode("ascii"))
    for section in source["chunks"]:
        tag, data = section["tag"], section["fields"]
        if tag == "TEXT":
            data = write_strings(data, ">" if form == "EMC2" else "<")
        elif tag == "ORDR" and form == "EMC2":
            data = struct.pack(f">{len(data)}H", *data)
        elif (tag, form) in (("DATA", "EMC2"), ("AVTL", "AVFS")):
            data = assemble_code(data, form)
        else:
            data = bytes.fromhex(data)
        pad = bytes.fromhex(section["pad"])
        if len(pad) > len(data) % 2 or len(tag) != 4:
            raise ValueError("invalid chunk tag or alignment byte")
        body.extend(struct.pack(">4sI", tag.encode("ascii"), len(data)))
        body.extend(data + pad)
    rebuilt = b"FORM" + struct.pack(">I", len(body) + 8 - bias) + body
    if listing(rebuilt) != source:
        raise ValueError("assembled file does not read back as the listing")
    return rebuilt


def check(root):
    counts = Counter()
    for path in sorted(Path(root).rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.upper() == ".PAK":
            data = path.read_bytes()
            files = ((name, data[at:at + size]) for name, at, size in L.pak_entries(data))
        elif path.suffix.upper() == ".TIM":
            files = ((path.name, path.read_bytes()),)
        else:
            continue
        for name, raw in files:
            if raw[:4] != b"FORM" or raw[8:12] not in (b"EMC2", b"AVFS"):
                continue
            # Exercise exactly the textual interchange supplied by the CLI.
            try:
                rebuild = assemble(json.loads(json.dumps(listing(raw), ensure_ascii=True)))
                if rebuild != raw:
                    raise ValueError("original bytes differ")
            except (ValueError, struct.error) as error:
                raise ValueError(f"{path.name}/{name}: {error}") from error
            counts[raw[8:12]] += 1
    if counts[b"EMC2"] != 60 or not counts[b"AVFS"]:
        raise ValueError("incomplete script corpus")
    print(f"CHECK script assembly: {counts[b'EMC2']} EMC2 and {counts[b'AVFS']} TIM scripts, byte-identical")


def holds_game_data(folder):
    """True when folder or a folder above it holds a game archive (PAK or TLK)."""
    for place in (folder, *folder.parents):
        try:
            if any(entry.suffix.upper() in (".PAK", ".TLK") for entry in place.iterdir()):
                return True
        except OSError:
            continue
    return False


def main():
    parser = ReaderArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, default=os.environ.get("LOL1_DATA"),
                        help="the game's DATA folder (default: $LOL1_DATA)")
    parser.add_argument("--check", action="store_true", help="rebuild every script of --data and compare")
    parser.add_argument("listing", type=Path, nargs="?", help="a lossless listing (JSON) to assemble")
    parser.add_argument("--out", type=Path, help="new output file outside the game folder")
    args = parser.parse_args()
    if args.check and args.data and not (args.listing or args.out):
        check(args.data)
    elif args.listing and args.out and not args.check:
        output = args.out.resolve()
        roots = [Path(__file__).resolve().parents[1]]
        if args.data:
            roots.append(args.data.resolve())
        if any(root == output or root in output.parents for root in roots) or holds_game_data(output.parent):
            parser.error("give an output path outside the game data and repository")
        rebuilt = assemble(json.loads(args.listing.read_text(encoding="utf-8")))
        with output.open("xb") as dest:
            dest.write(rebuilt)
    else:
        parser.error("give --check with --data, or a listing and --out")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
