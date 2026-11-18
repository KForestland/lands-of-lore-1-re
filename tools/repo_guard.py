#!/usr/bin/env python3
"""Asset-policy guard: fail if the repository tracks game media or game files.

The repository may hold documentation, tools, small data tables and a few
images in examples/ and docs/images/ (README, asset policy). This check lists
the files git tracks (or every file, outside a git checkout) and fails on:

  - game file types: .PAK .TLK .CPS .SHP .WSA .VCN .VMP .CMZ .WLL .XXX .TLC
    .PAL .COL .FNT .TIM .INF .INI .ENG .FRE .GER .EXE .DAT .TMP .XMI .C55
    .ADL .PCS .VOC .AUD, and converted media .MID .MIDI .WAV .OGG .MP3 .FLAC
  - PNG files outside examples/ and docs/images/
  - any file larger than 300 KB, except the existing data tables in SIZE_ALLOWED
    (generated listings of game content are tool output, not tracked files)
  - in the git history: any author or committer address not in ALLOWED_AUTHORS
    (committers may also be GitHub's noreply@github.com); the address is not printed
  - in text files: machine paths (/home/, /media/, /mnt/, C:\\Users\\) and
    lane, agent or private names (list in NAMES below)

  repo_guard.py --check     # one line; exit 1 if anything is found
It needs no game data (--data is accepted and ignored, for check_all).
"""
import argparse
import os
import re
import subprocess
import sys

GAME = {".pak", ".tlk", ".cps", ".shp", ".wsa", ".vcn", ".vmp", ".cmz", ".wll", ".xxx", ".tlc", ".pal",
        ".col", ".fnt", ".tim", ".inf", ".ini", ".eng", ".fre", ".ger", ".exe", ".dat", ".tmp", ".xmi",
        ".c55", ".adl", ".pcs", ".voc", ".aud", ".mid", ".midi", ".wav", ".ogg", ".mp3", ".flac"}
PNG_OK = ("examples/", "docs/images/")


# Text rules: no machine paths and no lane, agent or private names in tracked files.
# This file is exempt because it holds the lists.
MACHINE_PATH = re.compile(r"/home/[a-z]|/media/[a-z]|/mnt/[a-z]|[A-Za-z]:\\Users\\")
NAMES = re.compile(r"\b(Grok|Sol|Opus|Fable|Codex|Gemini|Kimi|Astra|Claude)\b")


def text_findings(root, f):
    if f.endswith("tools/repo_guard.py") or f == "tools/repo_guard.py":
        return []
    try:
        with open(os.path.join(root, f), encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except (UnicodeDecodeError, OSError):
        return []
    out = []
    for n, line in enumerate(lines, 1):
        if MACHINE_PATH.search(line):
            out.append(f"{f}:{n} (machine path)")
        for m in NAMES.finditer(line):
            if line[m.start() - 1:m.start()] == '"' and line[m.end():m.end() + 1] == '"':
                continue  # a quoted name is game text, e.g. the bow "Gemini"
            out.append(f"{f}:{n} (name {m.group(1)!r})")
            break
    return out


def tracked(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True, check=True).stdout
        return [l for l in out.splitlines() if l]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for d, dirs, fs in os.walk(root):
            dirs[:] = [x for x in dirs if x not in (".git", "__pycache__", ".venv")]
            files += [os.path.relpath(os.path.join(d, f), root) for f in fs]
        return files


# Commit identity: every author and committer address in the history of the checked-out branch (HEAD,
# what gets published) must be one of these.
# GitHub's own web merges commit as noreply@github.com (committer only).
ALLOWED_AUTHORS = {'261564562+KForestland@users.noreply.github.com'}
ALLOWED_COMMITTERS = ALLOWED_AUTHORS | {"noreply@github.com"}


def identity_findings(root):
    """Authors and committers in the git history that are not on the allowed lists."""
    try:
        out = subprocess.run(["git", "-C", root, "log", "HEAD", "--format=%h %ae %ce"],
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return []  # not a git checkout (for example a downloaded archive): nothing to check
    bad = []
    for line in out.splitlines():
        h, author, committer = line.split(" ")
        if author not in ALLOWED_AUTHORS:
            bad.append(f"commit {h} (author address not allowed)")
        if committer not in ALLOWED_COMMITTERS:
            bad.append(f"commit {h} (committer address not allowed)")
    return bad


# No tracked file over 300 KB, except these existing data tables (listed by name).
SIZE_LIMIT = 300_000
SIZE_ALLOWED = {"data/music_inventory.json"}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--data", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if not a.check:
        ap.print_help(); return 2
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    files = tracked(root)
    bad = []
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        p = os.path.join(root, f)
        if ext in GAME:
            bad.append(f"{f} (game file type)")
        elif ext == ".png" and not f.startswith(PNG_OK):
            bad.append(f"{f} (PNG outside examples/ and docs/images/)")
        elif os.path.isfile(p) and os.path.getsize(p) > SIZE_LIMIT and f not in SIZE_ALLOWED:
            bad.append(f"{f} (larger than 300 KB)")
        if os.path.isfile(p):
            bad.extend(text_findings(root, f))
    bad.extend(identity_findings(root))
    print(f"CHECK repo_guard: {len(files)} tracked files; game files, converted media, stray PNGs, files over 300 KB, machine paths, private or assistant names, or commit identities: "
          f"{bad[:5] or 'none'}{' ...' if len(bad) > 5 else ''} ({len(bad)})")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
