#!/usr/bin/env python3
"""Read original LoL1 PAK-compatible containers and rebuild them in memory."""
from pathlib import Path
import struct

from cli_errors import run_cli
import lol1lib


def write_pak(members):
    """Build the observed DOS directory from ordered (name, bytes) pairs."""
    rows = [(name.encode("latin-1"), payload) for name, payload in members]
    if not rows or not rows[-1][1]:
        raise ValueError("a PAK needs a nonempty final member")
    if any(not name or b"\0" in name for name, _ in rows):
        raise ValueError("PAK member names must be nonempty and NUL-free")
    offset = 9 + sum(5 + len(name) for name, _ in rows)
    directory = bytearray()
    for name, payload in rows:
        directory.extend(struct.pack("<I", offset))
        directory.extend(name + b"\0")
        offset += len(payload)
    directory.extend(struct.pack("<I5x", offset))
    return bytes(directory) + b"".join(payload for _, payload in rows)


def check(data):
    root = Path(data)
    archives = sorted(path for path in root.rglob("*")
                      if path.is_file() and path.suffix.lower() in {".pak", ".tlk"})
    if not archives:
        raise ValueError("no PAK or PAK-layout TLK files found")
    counts = {".pak": 0, ".tlk": 0}
    members = 0
    for path in archives:
        original = path.read_bytes()
        rows = lol1lib.pak_entries(original)
        rebuilt = write_pak((name, original[start:start + size]) for name, start, size in rows)
        if rebuilt != original:
            raise ValueError(f"{path.relative_to(root)} differs from the DOS directory reconstruction")
        counts[path.suffix.lower()] += 1
        members += len(rows)
    print(f"CHECK pak write: {counts['.pak']} PAK and {counts['.tlk']} PAK-layout TLK files, "
          f"{members} ordered members; byte-identical")


def main():
    parser = lol1lib.tool_args(__doc__, writes=False)
    args = parser.parse_args()
    if not args.check or args.pak:
        parser.error("give --check for the full data folder")
    check(args.data)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
