#!/usr/bin/env python3
"""Resolve every relative link and anchor in README.md and under docs/.

  doc_links.py --check
A link inside a fenced code block is an example, not a link, and is skipped.
--data is accepted and ignored so check_all can pass the game folder.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HREF = re.compile(r'<a\s+[^>]*href="([^"]+)"', re.I)
HEAD = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$', re.M)
ANCHOR = re.compile(r'<a\s+[^>]*(?:id|name)="([^"]+)"', re.I)
FENCE = re.compile(r"```.*?```", re.S)


def slug(text):
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = "".join(ch for ch in text if ch.isalnum() or ch in " -_")
    text = re.sub(r"\s+", "-", text.strip())
    return text


def heading_ids(text):
    seen = {}
    found = []
    for match in HEAD.finditer(text):
        base = slug(match.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.append(base if count == 0 else f"{base}-{count}")
    found.extend(ANCHOR.findall(text))
    return found


def pages():
    found = [ROOT / "README.md"]
    found.extend(sorted((ROOT / "docs").rglob("*.md")))
    return [page for page in found if page.is_file()]


def prose_of(text):
    return FENCE.sub("", text)


def targets(text):
    body = prose_of(text)
    return LINK.findall(body) + HREF.findall(body)


def check():
    broken = []
    cache = {}
    for page in pages():
        text = page.read_text(encoding="utf-8")
        for url in targets(text):
            if url.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = url.partition("#")
            dest = page if path == "" else (page.parent / path).resolve()
            try:
                dest.relative_to(ROOT)
            except ValueError:
                broken.append(f"{page.relative_to(ROOT)} leaves the repo: {url}")
                continue
            if not dest.exists():
                broken.append(f"{page.relative_to(ROOT)} missing {url}")
                continue
            if dest.is_dir():
                if anchor:
                    broken.append(f"{page.relative_to(ROOT)} anchor on a directory: {url}")
                continue
            if anchor and dest.suffix.lower() == ".md":
                ids = cache.get(dest)
                if ids is None:
                    ids = heading_ids(dest.read_text(encoding="utf-8"))
                    cache[dest] = ids
                if anchor not in ids:
                    broken.append(f"{page.relative_to(ROOT)} anchor {url}")
    if broken:
        print("CHECK links: " + broken[0])
        return 1
    print("CHECK links: every relative link and anchor in README.md and docs resolves")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data", default=None)
    args = parser.parse_args()
    if not args.check:
        parser.print_help()
        return 2
    return check()


if __name__ == "__main__":
    sys.exit(main())
