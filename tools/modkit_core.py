"""Shared workspace, archive and output handling for the Lands of Lore tools."""
import argparse
from contextlib import contextmanager
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import struct
from tempfile import TemporaryDirectory

from cli_errors import ReaderArgumentParser, output_refusal

MANIFEST = "manifest.json"
WORK_FORMAT = "lol-mod-work-1"
WORK_README = """Each file in edits holds one table, script or text list from one game archive.
Change only what is inside "value"; keep "file", "entry", "key" and "kind", the
number of rows and the field names. Text stays inside double quotes; write a line
break as \\r or \\n, as the file already does, and keep codes such as \\u0002
(they set colours and layout). Do not rename or delete files.
Then run: modkit.py build GAME_FOLDER THIS_FOLDER NEW_OUTPUT_FOLDER
and:      modkit.py verify GAME_FOLDER THIS_FOLDER NEW_OUTPUT_FOLDER
The game folder is never changed. Copy the files from the output folder over a
backup copy of your game to try them.
"""


def digest(raw):
    return sha256(raw).hexdigest()


def read_json(path):
    if not path.is_file():
        raise ValueError(f"{path} is missing; unpack again into a new work folder")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise ValueError(f"{path} is not valid JSON ({error}); correct the edit or unpack again") from None


def game_folder(adapter, root):
    if not root.is_dir():
        raise ValueError(f"game folder not found: {root}; give {adapter.FOLDER}")
    # A DAT folder is read with the game folder above it, which holds the loose tables.
    return root.parent if root.name.upper() == "DAT" else root


def write_json(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=True, indent=2)
        file.write("\n")


def local_path(root, name, links=False):
    """root/name for a plain relative name. Only game files (links=True) may be symbolic links."""
    if not isinstance(name, str):
        raise ValueError("expected a relative file name")
    relative = PurePosixPath(name)
    if (not relative.parts or relative.is_absolute() or ".." in relative.parts
            or relative.as_posix() != name or any(c in name for c in "\\:\0")):
        raise ValueError(f"invalid relative file name {name!r}")
    path = root.joinpath(*relative.parts)
    if not links and path.resolve() != path:
        raise ValueError(f"symbolic links are outside the workspace contract: {name}")
    return path


def output_path(path, game, *inputs):
    """A new folder outside the game folder, any folder holding game archives,
    this repository and the other inputs (the work folder)."""
    refusal = output_refusal(path, game, repository=True)
    if refusal:
        raise ValueError(refusal)
    target = Path(path).resolve()
    for root in (Path(p).resolve() for p in inputs):
        if target == root or root in target.parents:
            raise ValueError(f"output must be outside {root}")
    if target.exists() or Path(path).is_symlink():
        raise ValueError(f"output already exists: {path}")
    return target


@contextmanager
def output_folder(path, game, *inputs):
    target = output_path(path, game, *inputs)
    with TemporaryDirectory(prefix=".lol-output-", dir=target.parent) as temp:
        staged = Path(temp) / "result"
        staged.mkdir()
        yield staged
        output_path(target, game, *inputs)
        staged.rename(target)


def game_files(root, suffixes, extras=()):
    folders = [root] + sorted(path for path in root.iterdir()
                              if path.name.upper() in ("DAT", "DATA") and path.is_dir())
    for folder in folders:
        for path in sorted(folder.iterdir()):
            if path.is_file() and (path.suffix.upper() in suffixes or path.name.upper() in extras):
                name = path.relative_to(root).as_posix()
                if not path.name.upper().startswith("CDCACHE"):
                    yield name


def archive_parts(adapter, name, raw):
    # A standalone table is presented as a single anonymous member.
    if adapter.is_loose(name):
        return [(None, 0, raw)]
    return adapter.members(raw)


def replace_members(adapter, name, original, rows, changes):
    changed = [(key, at, changes.get(i, blob)) for i, (key, at, blob) in enumerate(rows)]
    if all(len(old) == len(new) for (_, _, old), (_, _, new) in zip(rows, changed)):
        result = bytearray(original)
        for i, blob in changes.items():
            start = rows[i][1]
            result[start:start + len(blob)] = blob
        result = bytes(result)
    elif adapter.is_loose(name):
        result = changed[0][2]
    else:
        if adapter.repack(rows, rows, len(original)) != original:
            raise ValueError(f"{name}: archive writer does not reproduce the original layout")
        result = adapter.repack(changed, rows, len(original))
    if [(key, blob) for key, _, blob in archive_parts(adapter, name, result)] != [
            (key, blob) for key, _, blob in changed]:
        raise ValueError(f"{name}: changed archive did not read back")
    return result


def number_view(blob, start, count, stride, fields):
    if not 0 <= start <= start + count * stride <= len(blob):
        raise ValueError("numeric table exceeds its entry")
    return [{name: struct.unpack_from("<" + fmt, blob, start + index * stride + at)[0]
             for name, at, fmt in fields} for index in range(count)]


def number_write(blob, start, count, stride, fields, values):
    if not isinstance(values, list) or len(values) != count:
        raise ValueError("numeric table row count changed")
    result = bytearray(blob)
    names = {name for name, _, _ in fields}
    for index, row in enumerate(values):
        if not isinstance(row, dict) or names != row.keys():
            raise ValueError("numeric table fields changed")
        for name, at, fmt in fields:
            if type(row[name]) is not int:
                raise ValueError(f"{name} must be an integer")
            struct.pack_into("<" + fmt, result, start + index * stride + at, row[name])
    return bytes(result)


def text_view(rows):
    return [field.decode("latin-1") for _, field in rows]


def text_fields(count, fields):
    if (not isinstance(fields, list) or len(fields) != count
            or any(not isinstance(s, str) or "\0" in s for s in fields)):
        raise ValueError("expected the same number of NUL-free text fields")
    return fields


def text_rows(rows, fields):
    text_fields(len(rows), fields)
    return [(key, field.encode("latin-1")) for (key, _), field in zip(rows, fields)]


def unpack(adapter, root, work):
    manifest = {"format": WORK_FORMAT, "game": adapter.GAME, "files": {}}
    count = 0
    with output_folder(work, root) as folder:
        for name in adapter.sources(root):
            raw = local_path(root, name, links=True).read_bytes()
            rows = archive_parts(adapter, name, raw)
            entries = {}
            for index, (key, _, blob) in enumerate(rows):
                view = adapter.view(name, key, blob)
                if view is None:
                    continue
                kind, value = view
                if adapter.encode(name, key, blob, kind, value) != blob:
                    raise ValueError(f"{name} entry {index}: unchanged edit does not encode byte-identically")
                label = "".join(c if c.isalnum() or c in "._-" else "_" for c in
                                f"{PurePosixPath(name).name}_{key if isinstance(key, str) else kind}")
                document = f"edits/{count:04d}_{label}.json"
                (folder / "edits").mkdir(exist_ok=True)
                write_json(folder / document, {"file": name, "entry": index, "key": key,
                                                "kind": kind, "value": value})
                entries[str(index)] = document
                count += 1
            if entries:
                manifest["files"][name] = {"sha256": digest(raw), "entries": entries}
        if not count:
            raise ValueError(f"nothing to unpack in {root}; give {adapter.FOLDER}")
        write_json(folder / MANIFEST, manifest)
        (folder / "README.txt").write_text(WORK_README, encoding="utf-8")
    return count


def builds(adapter, root, work):
    manifest = read_json(local_path(work, MANIFEST))
    if manifest["format"] != WORK_FORMAT or manifest["game"] != adapter.GAME or not manifest["files"]:
        raise ValueError(f"{work} was not unpacked by the {adapter.GAME.replace('lol', 'LoL')} mod kit; unpack the game folder first")
    sources = set(adapter.sources(root))
    for name, record in manifest["files"].items():
        if name not in sources:
            raise ValueError(f"{name} is not in {root}; give the game folder this work folder was unpacked from")
        original = local_path(root, name, links=True).read_bytes()
        if digest(original) != record["sha256"]:
            raise ValueError(f"{name} differs from the file that was unpacked; give the same game folder or unpack again")
        rows = archive_parts(adapter, name, original)
        changes = {}
        for index, document in record["entries"].items():
            index = int(index)
            if not 0 <= index < len(rows) or index in changes:
                raise ValueError(f"{name}: invalid or repeated entry {index}")
            key, _, blob = rows[index]
            edit = read_json(local_path(work, document))
            current = adapter.view(name, key, blob)
            if not isinstance(edit, dict) or [edit.get(k) for k in ("file", "entry", "key")] != [
                    name, index, key] or current is None or edit.get("kind") != current[0]:
                raise ValueError(f"{name} entry {index}: edited resource identity differs")
            try:
                changes[index] = adapter.encode(name, key, blob, edit["kind"], edit["value"])
            except (TypeError, AttributeError, KeyError) as error:
                raise ValueError(f"{name} entry {index}: malformed edit ({error})") from None
        yield name, record, original, replace_members(adapter, name, original, rows, changes)


def build(adapter, root, work, out):
    changed, count = [], 0
    with output_folder(out, root, work) as folder:
        for name, _, original, expected in builds(adapter, root, work):
            target = local_path(folder, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(expected)
            changed += [name] if expected != original else []
            count += 1
    return count, changed


def verify(adapter, root, work, out):
    folder = Path(out).resolve()
    changed, count = [], 0
    for name, record, original, expected in builds(adapter, root, work):
        target = local_path(folder, name)
        if not target.is_file():
            raise ValueError(f"{name} is missing from {folder}; run build first")
        raw = target.read_bytes()
        if raw != expected:
            raise ValueError(f"{name}: output differs from the expected archive")
        # Read every edited entry back from the output with the game's reader.
        rows = archive_parts(adapter, name, raw)
        for index, document in record["entries"].items():
            key, _, blob = rows[int(index)]
            edit = read_json(local_path(work, document))
            current = adapter.view(name, key, blob)
            if current is None or current[0] != edit["kind"] or (
                    current[0] != "script" and current[1] != edit["value"]):
                raise ValueError(f"{name} entry {index}: the output does not read back as the edit")
        changed += [name] if raw != original else []
        count += 1
    if len([p for p in folder.rglob("*") if p.is_file()]) != count:
        raise ValueError("output contains unexpected files")
    return count, changed


def check(adapter, data):
    """Unpack, rebuild and verify the whole game folder in a temporary folder."""
    root = game_folder(adapter, Path(data).resolve())
    with TemporaryDirectory(prefix="lol-modkit-check-") as temp:
        temp = Path(temp)
        work = temp / "work"
        entries = unpack(adapter, root, work)
        count, changed = build(adapter, root, work, temp / "out")
        if verify(adapter, root, work, temp / "out") != (count, []) or changed:
            raise ValueError("an unchanged workspace did not rebuild byte-identically")
        archives = temp / "archives"
        archives.mkdir()
        for name in adapter.sources(root):
            (archives / PurePosixPath(name).name).touch()
        for place in (root, root / "out", work, work / "out", temp / "out", archives / "out",
                      Path(__file__).resolve().parents[1] / "out"):
            try:
                output_path(place, root, work)
            except ValueError:
                continue
            raise ValueError(f"the output guard accepted {place}")
    print(f"CHECK modkit: {count} archives or loose tables rebuilt byte-identically from {entries} "
          "unpacked entries; outputs in the game, work, archive and repository folders refused")
    return 0


def main(adapter):
    parser = ReaderArgumentParser(
        description=f"Unpack editable {adapter.GAME.upper()} text and numbers into a work folder, "
                    "rebuild changed copies into a separate output folder and verify them.",
        epilog="Steps: modkit.py unpack GAME WORK; edit the files in WORK/edits; "
               "modkit.py build GAME WORK OUTPUT; modkit.py verify GAME WORK OUTPUT. "
               f"GAME is {adapter.FOLDER}. WORK and OUTPUT are new folders outside the game folder. "
               "The game folder is only read.")
    parser.add_argument("--check", action="store_true",
                        help="unpack, rebuild and verify the --data folder inside a temporary folder")
    parser.add_argument("--data", default=os.environ.get(adapter.DATA_ENV),
                        help=f"game folder for --check (default: ${adapter.DATA_ENV}); "
                             "a DAT folder is read with the folder above it")
    commands = parser.add_subparsers(dest="command", metavar="{unpack,build,verify}")
    steps = {"unpack": "write the editable files into a new work folder",
             "build": "write the changed archives into a new output folder",
             "verify": "check an output folder against the work folder"}
    for command, summary in steps.items():
        tool = commands.add_parser(command, help=summary, description=summary[0].upper() + summary[1:] + ".")
        tool.add_argument("game_folder", type=Path, help=f"{adapter.FOLDER}; only read")
        tool.add_argument("work_folder", type=Path,
                          help="new folder to create" if command == "unpack" else "the folder unpack wrote")
        if command != "unpack":
            tool.add_argument("output_folder", type=Path, help="new folder to create" if command == "build"
                              else "the folder build wrote")
    args = parser.parse_args()
    if args.check:
        if args.command or not args.data:
            parser.error("--check takes --data and no command")
        return check(adapter, args.data)
    if not args.command:
        parser.error("give unpack, build, verify or --check --data DIR")
    root = game_folder(adapter, args.game_folder.resolve())
    work = args.work_folder.resolve()
    if args.command == "unpack":
        count = unpack(adapter, root, work)
        files = len(read_json(work / MANIFEST)["files"])
        print(f"unpack: {count} editable entries from {files} files written to {work}; "
              f"edit the files in its edits folder, then run build")
        return 0
    run = build if args.command == "build" else verify
    count, changed = run(adapter, root, work, args.output_folder)
    done = {"build": f"written to {args.output_folder.resolve()}; run verify next",
            "verify": "the output matches the work folder and reads back"}[args.command]
    names = f" ({', '.join(changed)})" if changed else ""
    print(f"{args.command}: {count} archives or loose tables, {len(changed)} changed{names}; {done}")
    return 0
