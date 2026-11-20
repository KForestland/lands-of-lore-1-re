#!/usr/bin/env python3
"""Make, apply and undo small checked patches for your own copy of the game.

The same file is used in the three repositories; modkit.py says which game it is.
"""
from collections import defaultdict
from difflib import SequenceMatcher
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import struct
import sys

from cli_errors import ReaderArgumentParser, run_cli
import modkit as adapter
import modkit_core as core

FORMAT = "lol-patch-3"
LEGACY_FORMAT = "lol-patch-2"
UNDO_FORMAT = "lol-patch-undo-1"
KINDS = ("data", "program")
UNDO = "undo.json"
MAX_CHANGES = 1024
# Cap both the replaced span and its replacement, including in local undo files.
LIMITS = {"data": (256, 4096), "program": (16, 256)}
MAX_RESIZED = 65536
SHARED_RUN = 8
HEX = re.compile(r"(?:[0-9a-f]{2})*\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
NAMES = {"lol1": "LoL1", "lol2": "LoL2", "lol3": "LoL3"}
GAME = NAMES[adapter.GAME]

# Program files, relative to the folder the patch names files from.
PROGRAMS = {
    "lol1": ("MAIN.EXE", "MAINW.EXE", "HARDRIVE/MAIN.EXE", "HARDRIVE/MAINW.EXE"),
    "lol2": ("LOLG.DAT", "LOLG.EXE"),
    "lol3": ("LOL3.DAT", "LOL3.EXE"),
}
# The folder the file names in a patch start from.
BASE = {
    "lol1": "the folder holding the PAK archives (the CD DATA folder or the floppy game folder)",
    "lol2": "the game folder holding LOLG.DAT and DAT",
    "lol3": "the game folder holding LOL3.DAT and DAT",
}
COMPATIBILITY = {
    "lol1": (
        "Data patches are for the original program under DOSBox; ScummVM also reads the "
        "changed data when it still recognizes the release.",
        "Program patches are for MAIN.EXE or MAINW.EXE under DOSBox; ScummVM does not run "
        "these programs, so they have no effect there.",
    ),
    "lol2": (
        "Data patches are for the original DOS game under DOSBox.",
        "Program patches are for LOLG.DAT or LOLG.EXE of the original DOS release under DOSBox.",
    ),
    "lol3": (
        "Data patches are for the original Windows game.",
        "Program patches are for LOL3.DAT or LOL3.EXE of the original Windows release.",
    ),
}
# ScummVM 3b4db303, engines/kyra/detection_tables.h:1347-1940 (game id "lol").
LOL1_DETECTION_FILES = {
    "GENERAL.PAK", "L01.PAK", "WESTWOOD.1", "CHAPTER7.PAK", "LEVEL01.FRE", "LEVEL02.FRE",
    "MUS.PAK", "TMUS.PAK", "INTRO.PAK", "INTROVOC.PAK", "VOC.PAK", "GAME.DAT",
}


class PatchLimitError(ValueError):
    """The change cannot fit the shared patch format's limits."""


def plural(count, word):
    return f"{count:,} {word}" + ("" if count == 1 else "s")


def digest(raw):
    return sha256(raw).hexdigest()


# ---------------------------------------------------------------- folders

def base_folder(root):
    """The folder that the file names in a patch start from (see BASE)."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"game folder not found: {root}; give {BASE[adapter.GAME]}")
    if adapter.GAME == "lol1":
        # The CD keeps its archives in DATA; a patch names them from there.
        def archives(folder):
            return any(p.suffix.upper() == ".PAK" for p in folder.iterdir())
        inner = [p for p in root.iterdir() if p.name.upper() == "DATA" and p.is_dir()]
        if not archives(root) and inner and archives(inner[0]):
            return inner[0]
        return root
    return core.game_folder(adapter, root)


def protected(root, base):
    """Folders no output may be written into: the given folder, the base folder and,
    when the base is a DAT or DATA folder, the installation folder around it."""
    folders = [Path(root).resolve(), base]
    if base.name.upper() in ("DAT", "DATA"):
        folders.append(base.parent)
    return folders


def new_output(path, root, base, *inputs):
    """A path that does not exist yet, in an existing folder outside the game and inputs."""
    target = core.output_path(path, base, *inputs, *protected(root, base))
    if not target.parent.is_dir():
        raise ValueError(f"the folder {target.parent} does not exist; create it first or choose another place")
    return target


def program_files(base):
    found = {}
    for wanted in PROGRAMS[adapter.GAME]:
        folder, parts = base, wanted.split("/")
        for part in parts:
            match = [p for p in folder.iterdir() if p.name.upper() == part] if folder.is_dir() else []
            if not match:
                break
            folder = match[0]
        else:
            if folder.is_file():
                found[folder.relative_to(base).as_posix()] = folder
    return found


def source_files(base, kind):
    if kind == "data":
        return set(getattr(adapter, "patch_sources", adapter.sources)(base))
    return set(program_files(base))


def read_source(base, name):
    return core.local_path(base, name, links=True).read_bytes()


# ---------------------------------------------------------------- patch documents

def document(kind, title, description, changes, programs=None, *, version=FORMAT):
    patch = {"format": version, "game": adapter.GAME, "kind": kind, "title": title,
             "description": description}
    if kind == "program":
        patch["sha256"] = dict(sorted(programs.items()))
    patch["changes"] = changes
    return patch


def record(file, entry, offset, old, new):
    return {"file": file, "entry": entry, "offset": offset, "old_length": len(old),
            "old_sha256": digest(old), "new": new.hex()}


def check_document(patch):
    """Check a patch and group its changes by file and entry. Errors are sentences."""
    version = patch.get("format") if isinstance(patch, dict) else None
    if version not in (FORMAT, LEGACY_FORMAT, UNDO_FORMAT):
        raise ValueError(f"this is not a {FORMAT}, {LEGACY_FORMAT} or local undo file")
    legacy = version == LEGACY_FORMAT
    game = patch.get("game")
    if game != adapter.GAME:
        if isinstance(game, str) and game in NAMES:
            raise ValueError(f"this patch is for {NAMES[game]}; use patch.py from the "
                             f"{NAMES[game]} repository")
        raise ValueError("the patch does not say which game it is for (its \"game\" entry)")
    kind = patch.get("kind")
    if kind not in KINDS:
        raise ValueError("the patch kind must be \"data\" or \"program\"")
    keys = {"format", "game", "kind", "title", "description", "changes"}
    keys |= {"sha256"} if kind == "program" else set()
    if set(patch) != keys:
        extra = sorted(set(patch) - keys) or sorted(keys - set(patch))
        raise ValueError(f"the patch entries differ from the {version} format (check: {', '.join(extra)})")
    for key, limit in (("title", 120), ("description", 1000)):
        value = patch[key]
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise ValueError(f"the patch {key} must be text of 1 to {limit} characters")
    changes = patch["changes"]
    if not isinstance(changes, list) or not changes:
        raise ValueError("the patch has no changes")
    if len(changes) > MAX_CHANGES:
        raise PatchLimitError(f"the patch has {len(changes):,} changes; the limit is {MAX_CHANGES:,}")
    span, total = LIMITS[kind]
    sizes = [0, 0]
    groups = defaultdict(lambda: defaultdict(list))
    fields = ("file", "entry", "offset", "new") + (("old",) if legacy else ("old_length", "old_sha256"))
    for number, edit in enumerate(changes, 1):
        where = f"change {number}"
        if not isinstance(edit, dict) or set(edit) != set(fields):
            raise ValueError(f"{where} needs exactly {', '.join(fields)}")
        file, entry, offset, new = (edit[k] for k in ("file", "entry", "offset", "new"))
        if not isinstance(file, str) or not file:
            raise ValueError(f"{where}: the file must be a name such as DAT/GLOBAL.MIX")
        try:
            core.local_path(Path("."), file, links=True)
        except ValueError:
            raise ValueError(f"{where}: {file!r} is not a plain relative file name such as DAT/GLOBAL.MIX") from None
        if type(entry) is not int or entry < 0 or type(offset) is not int or offset < 0:
            raise ValueError(f"{where}: entry and offset must be whole numbers of 0 or more")
        if not isinstance(new, str) or not HEX.fullmatch(new):
            raise ValueError(f"{where}: new must be lowercase hexadecimal byte pairs")
        if legacy:
            old = edit["old"]
            if not isinstance(old, str) or not HEX.fullmatch(old):
                raise ValueError(f"{where}: old must be lowercase hexadecimal byte pairs")
            old_length = len(old) // 2
        else:
            old_length, old_sha = edit["old_length"], edit["old_sha256"]
            if type(old_length) is not int or old_length < 0:
                raise ValueError(f"{where}: old_length must be a whole number of 0 or more")
            if not isinstance(old_sha, str) or not SHA.fullmatch(old_sha):
                raise ValueError(f"{where}: old_sha256 must be 64 lowercase hexadecimal digits")
        new_length = len(new) // 2
        if kind == "program" and (entry != 0 or old_length != new_length or not old_length):
            raise ValueError(f"{where}: a program change uses entry 0 and replaces bytes "
                             "with the same number of bytes")
        if max(old_length, new_length) > span:
            raise PatchLimitError(f"{where} ({file}, entry {entry}, entry-relative offset +{offset:#x}) "
                                  f"has {max(old_length, new_length)} bytes; "
                                  f"a {kind} patch allows at most {span} bytes per change")
        sizes[0] += old_length
        sizes[1] += new_length
        if max(sizes) > total:
            raise PatchLimitError(f"a {kind} patch allows at most {total:,} bytes each "
                                  "of replaced spans and replacement values")
        new = bytes.fromhex(new)
        if legacy:
            old_sha = digest(bytes.fromhex(old))
        if old_length == new_length and old_sha == digest(new):
            raise ValueError(f"{where} changes nothing")
        groups[file][entry].append((offset, old_length, old_sha, new, version == FORMAT))
    if kind == "program":
        programs = patch["sha256"]
        if (not isinstance(programs, dict) or set(programs) != set(groups)
                or not all(isinstance(v, str) and SHA.fullmatch(v) for v in programs.values())):
            raise ValueError("a program patch needs the SHA-256 of each program it changes")
    return groups


def read_patch(path):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"patch file not found: {path}")
    try:
        patch = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError, ValueError):
        raise ValueError(f"{path} is not a patch file (it is not readable JSON text)") from None
    check_document(patch)
    return patch


# ---------------------------------------------------------------- byte edits

def trim(old, new):
    """Return the common prefix length and the two trimmed spans."""
    first = 0
    for left, right in zip(old, new):
        if left != right:
            break
        first += 1
    last = 0
    for left, right in zip(reversed(old[first:]), reversed(new[first:])):
        if left != right:
            break
        last += 1
    return first, old[first:len(old) - last], new[first:len(new) - last]


def validate_minimal(old, new, where):
    _, before, after = trim(old, new)
    if len(before) != len(old) or len(after) != len(new):
        raise ValueError(f"{where}: trim matching bytes from the ends of this change")
    if any(old[i:i + SHARED_RUN] in new for i in range(len(old) - SHARED_RUN + 1)):
        raise ValueError(f"{where}: split this change around the run of {SHARED_RUN} or more shared bytes")


def splice(name, entry, blob, changes):
    result, undo = bytearray(), []
    cursor = 0
    where = name if entry is None else f"{name} entry {entry}"
    for offset, length, expected, new, minimal in sorted(changes, key=lambda change: change[0]):
        if offset < cursor or (undo and offset == cursor):
            raise ValueError(f"{where}: two changes overlap or touch at +{offset:#x}")
        end = offset + length
        old = blob[offset:end]
        if offset > len(blob) or end > len(blob) or digest(old) != expected:
            raise ValueError(f"{where} +{offset:#x} does not hold the bytes this patch expects; "
                             "the patch is for another version, or it is already applied")
        if minimal:
            validate_minimal(old, new, f"{where} +{offset:#x}")
        result.extend(blob[cursor:offset])
        undo.append(record(name, entry or 0, len(result), new, old))
        result.extend(new)
        cursor = end
    result.extend(blob[cursor:])
    return bytes(result), undo


def edit_archive(name, original, entries):
    rows = core.archive_parts(adapter, name, original)
    changes, undo = {}, []
    validator_for = getattr(adapter, "patch_validator", None)
    for index, edits in sorted(entries.items()):
        if not 0 <= index < len(rows):
            raise ValueError(f"{name} has no entry {index}; the patch is for another version")
        key, _, blob = rows[index]
        validate = validator_for(name, key, blob) if validator_for else None
        if validate:
            edited, reverse = splice(name, index, blob, edits)
            validate(blob, edited)
        else:
            before = adapter.view(name, key, blob)
            if before is None:
                raise ValueError(f"{name} entry {index} is not a table or text the mod kit can edit")
            edited, reverse = splice(name, index, blob, edits)
            after = adapter.view(name, key, edited)
            if (after is None or before[0] != after[0]
                    or adapter.encode(name, key, blob, *after) != edited
                    or adapter.encode(name, key, edited, *before) != blob):
                raise ValueError(f"{name} entry {index}: the change goes outside the fields the mod kit edits")
        changes[index] = edited
        undo.extend(reverse)
    return core.replace_members(adapter, name, original, rows, changes), undo


def edit_program(name, original, entries):
    if len(original) < 64 or not original.startswith(b"MZ"):
        raise ValueError(f"{name} is not an original program file")
    edited, undo = splice(name, None, original, entries[0])
    if not edited.startswith(b"MZ") or len(edited) != len(original):
        raise ValueError(f"{name}: a program change must keep the file length and its MZ start")
    return edited, undo


def edit_file(kind, name, original, entries):
    try:
        return (edit_archive if kind == "data" else edit_program)(name, original, entries)
    except (struct.error, IndexError, KeyError, UnicodeError):
        raise ValueError(f"{name} could not be read; it may be damaged or from another edition") from None


def byte_deltas(name, index, old, new):
    if len(old) == len(new):
        start = None
        for at, (left, right) in enumerate(zip(old, new)):
            if left != right and start is None:
                start = at
            if left == right and start is not None:
                yield record(name, index, start, old[start:at], new[start:at])
                start = None
        if start is not None:
            yield record(name, index, start, old[start:], new[start:])
        return
    if max(len(old), len(new)) > MAX_RESIZED:
        raise PatchLimitError(f"{name} entry {index} changed size and is larger than {MAX_RESIZED:,} "
                              "bytes; keep its length or make a smaller edit")
    base, old, new = trim(old, new)
    for change, a, b, c, d in SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if change != "equal":
            first, before, after = trim(old[a:b], new[c:d])
            if before or after:
                yield record(name, index, base + a + first, before, after)


def file_deltas(kind, name, original, edited):
    if kind == "program":
        if len(original) != len(edited):
            raise ValueError(f"{name}: a changed program must keep its length")
        return list(byte_deltas(name, 0, original, edited))
    try:
        before = core.archive_parts(adapter, name, original)
        after = core.archive_parts(adapter, name, edited)
    except (struct.error, IndexError, KeyError, ValueError):
        raise ValueError(f"the changed {name} could not be read as an archive; build it again with modkit.py") from None
    if [key for key, _, _ in before] != [key for key, _, _ in after]:
        raise ValueError(f"the changed {name} has different entries; only change what is inside entries")
    return [edit for index, ((_, _, old), (_, _, new)) in enumerate(zip(before, after))
            if old != new for edit in byte_deltas(name, index, old, new)]


# ---------------------------------------------------------------- make and apply

def same_file(path, original):
    return (original.is_file() and original.stat().st_size == path.stat().st_size
            and original.read_bytes() == path.read_bytes())


def changed_names(root, base, changed, kinds):
    """Map each file in the changed folder to its name below base. The changed folder is
    laid out like the game folder given (a copy of DAT pairs with DAT) or, failing that,
    like base (as modkit.py build writes it); one layout holds for the whole folder."""
    given = Path(root).resolve()
    paths = [p for p in sorted(changed.rglob("*")) if p.is_file() and p.relative_to(changed).as_posix() != UNDO]
    layouts = [given] + [place for place in (base, base.parent) if place != given]
    if base.name.upper() not in ("DAT", "DATA"):
        layouts = [place for place in layouts if place != base.parent]
    first = None
    for place in layouts:
        pairs = {}
        for path in paths:
            relative = path.relative_to(changed).as_posix()
            target = place.joinpath(*relative.split("/"))
            try:
                name = target.relative_to(base).as_posix()
            except ValueError:
                name = None
            kind = next((k for k, names in kinds.items() if name in names), None)
            if kind and name not in pairs:
                pairs[name] = (kind, path)
            elif not (kind or same_file(path, target)):
                first = first or relative
                break
        else:
            return pairs
    raise ValueError(f"{first} in the changed folder is not a game file this tool can patch, or the "
                     f"folder is not laid out like the game folder {given}; keep only changed game "
                     "files there, at the same paths as in the game folder")


def make(root, changed, title, description, kind=None):
    base = base_folder(root)
    changed = Path(changed).resolve()
    if not changed.is_dir():
        raise ValueError(f"changed folder not found: {changed}")
    kinds = {k: source_files(base, k) for k in KINDS}
    pairs = changed_names(root, base, changed, kinds)
    different = {}
    for name, (file_kind, path) in sorted(pairs.items()):
        original, edited = read_source(base, name), path.read_bytes()
        if original != edited:
            different[name] = file_kind, original, edited
    if not different:
        raise ValueError("the changed folder has no differences from the game folder; nothing to patch")
    found = {k for k, _, _ in different.values()}
    if kind is None:
        if len(found) > 1:
            raise ValueError("both data and program files were changed; "
                             "make one patch with --kind data and one with --kind program")
        kind = found.pop()
    differences, programs = [], {}
    for name, (file_kind, original, edited) in different.items():
        if file_kind != kind:
            raise ValueError(f"{name} is a {file_kind} file; make a separate patch with --kind {file_kind}")
        edits = file_deltas(kind, name, original, edited)
        programs[name] = digest(original)
        groups = check_document(document(kind, title, description, edits, {name: programs[name]}))
        rebuilt, undo = edit_file(kind, name, original, groups[name])
        reverse = check_document(document(kind, title, description, undo, {name: digest(rebuilt)}))
        if rebuilt != edited or edit_file(kind, name, rebuilt, reverse[name])[0] != original:
            raise ValueError(f"{name}: the change could not be repeated and undone exactly")
        differences.extend(edits)
    patch = document(kind, title, description, differences, programs)
    check_document(patch)
    return patch


def prepare(root, patch):
    """Every changed file and the undo document, in memory; nothing is written."""
    groups = check_document(patch)
    kind = patch["kind"]
    base = base_folder(root)
    sources = source_files(base, kind)
    files, reverse, programs = {}, [], {}
    for name, entries in sorted(groups.items()):
        if name not in sources:
            raise ValueError(f"the patch changes {name}, which is not in {base}; give "
                             f"{BASE[adapter.GAME]}, of the same game and edition the patch was made for")
        original = read_source(base, name)
        if kind == "program" and digest(original) != patch["sha256"][name]:
            raise ValueError(f"{name} is not the program this patch was made for (its SHA-256 "
                             "differs); a program patch fits only the same edition and version")
        changed, undo = edit_file(kind, name, original, entries)
        programs[name] = digest(changed)
        undo_groups = check_document(document(kind, "Undo", "Undo", undo, {name: programs[name]}, version=UNDO_FORMAT))
        if edit_file(kind, name, changed, undo_groups[name])[0] != original:
            raise ValueError(f"{name}: the undo would not restore the file exactly")
        files[name] = changed
        reverse.extend(undo)
    title = "Undo " + patch["title"][:115]
    undo = document(kind, title, "Private undo file. It holds original game bytes. Do not share it.",
                    reverse, programs, version=UNDO_FORMAT)
    check_document(undo)
    return base, files, undo


def apply(root, patch, output):
    base, files, undo = prepare(root, patch)
    new_output(output, root, base)
    with core.output_folder(output, base, *protected(root, base)) as stage:
        for name, raw in files.items():
            target = core.local_path(stage, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        core.write_json(stage / UNDO, undo)
    return base, sorted(files)


def report_compatibility(patch):
    print(COMPATIBILITY[adapter.GAME][KINDS.index(patch["kind"])])
    if adapter.GAME == "lol1":
        for name in sorted({change["file"] for change in patch["changes"]}):
            if Path(name).name.upper() in LOL1_DETECTION_FILES:
                print(f"Warning: ScummVM recognizes the game by {name}; "
                      "a change there can stop ScummVM recognizing it.")


# ---------------------------------------------------------------- command line

def game_and_path(parser, args):
    paths, data = args.paths, args.data
    if len(paths) > 2:
        parser.error("too many paths; put quotes around paths with spaces")
    if len(paths) == 2:
        if data:
            parser.error("give the game folder once, with --data or as the first path")
        data, paths = paths[0], paths[1:]
    data = data or os.environ.get(adapter.DATA_ENV)
    if not data:
        parser.error(f"give the game folder with --data (or set {adapter.DATA_ENV})")
    return Path(data), Path(paths[0])


def run(argv=None):
    parser = ReaderArgumentParser(
        description=f"Make, apply and undo small checked patches for your own copy of {GAME}. "
                    "The game folder is only read; results go into a new folder.",
        epilog=" ".join(COMPATIBILITY[adapter.GAME]) + " Patches must not remove or bypass copy protection.")
    commands = parser.add_subparsers(dest="command", metavar="{make,apply}")
    commands.required = True
    make_parser = commands.add_parser(
        "make", help="compare the game folder with a folder of changed files and write a patch",
        description="Write a patch from the differences between the game folder and a folder "
                    "of changed files (such as the output of modkit.py build).")
    make_parser.add_argument("paths", nargs="+", metavar="CHANGED_FOLDER",
                             help="the folder with the changed files (the game folder may come first instead of --data)")
    make_parser.add_argument("--kind", choices=KINDS,
                             help="data or program (default: found from the changed files)")
    make_parser.add_argument("--title", required=True, help="a short name for the patch")
    make_parser.add_argument("--description", help="one or two sentences (default: the title)")
    make_parser.add_argument("--out", required=True, type=Path, help="the new patch file to write")
    apply_parser = commands.add_parser(
        "apply", help="write patched copies and a private undo.json into a new folder",
        description="Write patched copies and undo.json into a new folder. "
                    "Keep undo.json private because it holds original game bytes.")
    apply_parser.add_argument("paths", nargs="+", metavar="PATCH_FILE",
                              help="the patch (or an undo.json); the game folder may come first instead of --data")
    apply_parser.add_argument("--out", required=True, type=Path, help="the new folder to write")
    for sub in (make_parser, apply_parser):
        sub.add_argument("--data", help=f"{BASE[adapter.GAME]} (default: ${adapter.DATA_ENV}); only read")
    args = parser.parse_args(argv)
    root, path = game_and_path(parser, args)
    root = root.resolve()
    if args.command == "make":
        base = base_folder(root)
        changed = path.resolve()
        target = new_output(args.out, root, base, changed)
        patch = make(root, changed, args.title, args.description or args.title, args.kind)
        core.write_json(target, patch)
        files = sorted({change["file"] for change in patch["changes"]})
        print(f"make: {patch['kind']} patch with {plural(len(patch['changes']), 'change')} in "
              f"{plural(len(files), 'file')} ({', '.join(files)}) written to {target}")
    else:
        patch = read_patch(path)
        base, names = apply(root, patch, args.out)
        print(f"apply: {plural(len(names), 'file')} ({', '.join(names)}) and {UNDO} written to "
              f"{args.out.resolve()}; keep {UNDO} private and copy the patched files, with their folders, "
              f"into a copy of {BASE[adapter.GAME]}")
    report_compatibility(patch)
    return 0


def main(argv=None):
    try:
        return run(argv)
    except OSError as error:
        reason = (error.strerror or "the system refused").lower()
        raise ValueError(f"cannot use {error.filename or 'a file'}: {reason}") from None


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
