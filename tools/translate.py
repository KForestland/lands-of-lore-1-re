#!/usr/bin/env python3
"""Export, build and verify the original game's text tables on copies."""
from collections import defaultdict
import csv
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import sys

from cli_errors import ReaderArgumentParser, run_cli
import modkit
from modkit_core import archive_parts, digest, local_path, output_folder, replace_members, write_json
import translate_data as data
import translate_fonts as fonts


FORMAT = "lol-translation-1"
COLUMNS = ("id", "original", "new", "length limit")


@dataclass(frozen=True)
class Resource:
    file: str
    member: int
    label: str
    offset: int
    raw: bytes


def visible(text):
    return "".join("\\\\" if char == "\\" else f"\\x{ord(char) & 0xFF:02X}" if
                    ord(char) < 32 or 127 <= ord(char) < 160 or 0xDC80 <= ord(char) <= 0xDCFF else char for char in text)


def literal(text):
    if text == r"\e":
        return ""

    def unescape(match):
        token = match.group(1)
        if token == "\\":
            return token
        index = int(token[1:], 16)
        return chr(index if index < 0x80 else 0xDC00 + index)
    return re.sub(r"\\(\\|x[0-9A-Fa-f]{2})", unescape, text)


def table_rows(resource):
    return [(str(ident), visible(text), "", limit) for ident, text, limit in data.read(resource.label, resource.raw)]


def file_name(index, resource):
    label = re.sub(r"[^A-Za-z0-9_.-]", "_", resource.label)
    return f"{index:03d}-{label}.csv"


def entry_for(resource, index):
    return {"name": file_name(index, resource), "file": resource.file, "entry": resource.member,
            "offset": resource.offset, "label": resource.label, "sha256": digest(resource.raw)}


def protected(root):
    return (root.parent,) if root.name.upper() == "DATA" else ()


def export(root, output):
    entries, rows = [], 0
    with output_folder(output, root, *protected(root)) as folder:
        for index, resource in enumerate((Resource(*row) for row in data.sources(root)), 1):
            entry = entry_for(resource, index)
            name = entry["name"]
            table = table_rows(resource)
            with (folder / name).open("x", encoding="utf-8-sig", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(COLUMNS)
                writer.writerows(table)
            entries.append(entry)
            rows += len(table)
        if not entries:
            raise ValueError(f"No text tables were found in {root}. Give --data the original game folder.")
        write_json(folder / "manifest.json", {"format": FORMAT, "game": modkit.GAME, "tables": entries})
    return len(entries), rows


def manifest(work):
    try:
        value = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
        if value["format"] != FORMAT or value["game"] != modkit.GAME or not value["tables"]:
            raise ValueError
        return value["tables"]
    except (OSError, ValueError, KeyError, TypeError):
        raise ValueError(f"{work} is not an export for this game. Use the folder written by translate export.") from None


def translation(resource, csv_path, report=None):
    before = table_rows(resource)
    try:
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            header, rows = next(reader, []), list(reader)
    except (OSError, UnicodeError, csv.Error):
        raise ValueError(f"Cannot read {csv_path.name}. Save the exported table as UTF-8 CSV and keep its columns.") from None
    if tuple(header) != COLUMNS or len(before) != len(rows):
        raise ValueError(f"Keep the four columns and all {len(before)} rows in {csv_path.name}.")
    translated = {}
    for i, ((ident, original, _, limit), line) in enumerate(zip(before, rows)):
        if len(line) != 4 or (line[0], line[1], line[3]) != (ident, original, limit):
            raise ValueError(f"Keep the ID, original text and limit on row {i + 2} of {csv_path.name}.")
        if not line[2]:
            continue
        if limit == "locked":
            raise ValueError(f"{csv_path.name} row {i + 2} is a resource name or tag. Keep its new column empty.")
        text = literal(line[2])
        preserve = getattr(data, "preserve_controls", None)
        if preserve:
            text = preserve(literal(original), text)
        try:
            data.encode(text)
        except UnicodeEncodeError as error:
            char = error.object[error.start]
            raise ValueError(f"{csv_path.name} row {i + 2}: {fonts.character(char)} is outside "
                             f"{data.CHARSET}. {fonts.substitute(char)}") from None
        if "\0" in text:
            raise ValueError(f"{csv_path.name} row {i + 2}: NUL ends a string. Remove that control code.")
        if text == literal(original):
            continue
        translated[i] = text
    if not translated:
        return resource.raw
    try:
        changed = data.write(resource.label, resource.raw, translated)
    except (ValueError, UnicodeError) as error:
        raise ValueError(f"{csv_path.name}: {error}") from None
    after = data.read(resource.label, changed)
    expected = [(str(ident), data.decode(data.encode(translated[i])) if i in translated else literal(text))
                for i, (ident, text, _, _) in enumerate(before)]
    if [(str(ident), text) for ident, text, _ in after] != expected:
        raise ValueError(f"{csv_path.name} did not read back as the requested rows.")
    if report is not None:
        for i, text in translated.items():
            report(resource, csv_path.name, i + 2, text)
    return changed


def updated_files(root, work, report=None):
    entries = manifest(work)
    grouped = defaultdict(list)
    expected = []
    for index, resource in enumerate((Resource(*row) for row in data.sources(root)), 1):
        entry = entry_for(resource, index)
        expected.append(entry)
        grouped[resource.file].append(entry)
    if entries != expected:
        raise ValueError("The source tables or manifest differ from the export. Use the same unmodified original copy.")
    for name, tables in grouped.items():
        original = local_path(root, name, links=True).read_bytes()
        rows = archive_parts(modkit, name, original)
        changes = {}
        for table in tables:
            index = table["entry"]
            if type(index) is not int or not 0 <= index < len(rows):
                raise ValueError(f"{name}: table entry is no longer present. Export from this copy again.")
            _, offset, raw = rows[index]
            if offset != table["offset"] or digest(raw) != table["sha256"]:
                raise ValueError(f"{name}: the text tables differ from the export. Use the same original copy.")
            resource = Resource(name, index, table["label"], offset, raw)
            csv_path = local_path(work, table["name"])
            edited = translation(resource, csv_path, report)
            if edited != raw:
                changes[index] = edited
        if changes:
            result = replace_members(modkit, name, original, rows, changes)
            yield name, result
            mirrors = getattr(data, "mirror_files", None)
            if mirrors:
                for mirror in mirrors(root, name):
                    yield mirror, result


def build(root, work, output):
    count = 0
    notes = []
    installed = None

    def report(resource, name, row, text):
        nonlocal installed
        select = data.warning_fonts(resource.file, resource.label)
        if not select:
            return
        if installed is None:
            installed = fonts.installed(root)
        relevant = [(name, drawn) for name, drawn in installed if select(name)]
        notes.extend(f"{name} row {row}: {note}" for note in fonts.missing(text, relevant))

    with output_folder(output, root, work, *protected(root)) as folder:
        for name, raw in updated_files(root, work, report):
            target = local_path(folder, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            count += 1
    for note in notes:
        print(f"Glyph warning: {note}", file=sys.stderr)
    return count


def verify(root, work, output):
    if not output.is_dir():
        raise ValueError(f"{output} does not exist. Build the translation first.")
    expected = set()
    for name, raw in updated_files(root, work):
        target = local_path(output, name)
        if not target.is_file() or target.read_bytes() != raw:
            raise ValueError(f"{name} in {output} differs from the verified translation. Build again into a new folder.")
        expected.add(name)
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != expected:
        raise ValueError(f"{output} contains unexpected files. Give verify the output folder made by translate build.")
    return len(expected)


def check(root):
    tables = rows = 0
    for name, _, label, at, blob in data.sources(root):
        original = data.read(label, blob)
        if data.write(label, blob, {}) != blob:
            raise ValueError(f"{name}+{at:#x}: unchanged text table did not rebuild exactly.")
        if any(data.decode(data.encode(value)) != value for _, value, _ in original):
            raise ValueError(f"{name}+{at:#x}: exported characters do not round-trip.")
        tables += 1
        rows += len(original)
    measured = fonts.installed(root)
    if not tables or not measured:
        raise ValueError("The text and font check needs an original installation.")
    print(f"CHECK translation: {tables:,} unchanged tables, {rows:,} rows, {len(measured)} indexed fonts.")


def main():
    parser = ReaderArgumentParser(description=__doc__)
    default = os.environ.get(modkit.DATA_ENV)
    parser.add_argument("--check", action="store_true", help="check installed text and font tables in memory")
    parser.add_argument("--data", default=default, help=modkit.FOLDER)
    commands = parser.add_subparsers(dest="job")
    for name, summary in (("export", "write one private CSV per text table"),
                          ("build", "write changed files to a new folder"),
                          ("verify", "read back the files written by build"),
                          ("fonts", "list glyphs in the original fonts")):
        command = commands.add_parser(name, help=summary, description=summary.capitalize() + ".")
        command.add_argument("--data", default=default, required=default is None, help=modkit.FOLDER)
        if name in ("build", "verify"):
            command.add_argument("--work", required=True, type=Path, help="the folder made by export")
        if name != "fonts":
            command.add_argument("--out", dest="destination", required=True, type=Path, help="the destination folder")
    args = parser.parse_args()
    if args.check:
        if args.job or not args.data:
            parser.error("Use --check with the original game folder.")
        check(data.root(Path(args.data).resolve()))
        return 0
    if not args.job:
        parser.error("Choose export, build, verify or fonts.")
    root = data.root(Path(args.data).resolve())
    if args.job == "fonts":
        fonts.show(root)
    elif args.job == "export":
        tables, rows = export(root, args.destination)
        print(f"Exported {tables:,} private CSV tables with {rows:,} rows to {args.destination}.")
    elif args.job == "build":
        count = build(root, args.work.resolve(), args.destination)
        print(f"Built and read back {count:,} changed file{'' if count == 1 else 's'} in {args.destination}.")
    else:
        count = verify(root, args.work.resolve(), args.destination.resolve())
        print(f"Verified {count:,} changed file{'' if count == 1 else 's'} in {args.destination}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
