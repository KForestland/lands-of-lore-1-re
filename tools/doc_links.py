#!/usr/bin/env python3
"""Check that every relative link, image link and anchor in the docs resolves.

  doc_links.py --check
Pages scanned: README.md, tools/README.md, CONTRIBUTING.md, docs/**/*.md,
and examples/**/*.md and evidence/**/*.md when present.
This checks links and anchors only; it does not run any command shown in
the pages. Anchors follow GitHub's heading ids. A link or heading inside a
fenced code block (``` or ~~~) is an example and is skipped.
--data is accepted and ignored so check_all can pass the game folder.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HREF = re.compile(r'<a\s+[^>]*href="([^"]+)"', re.I)
HEAD = re.compile(r'^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$')
ANCHOR = re.compile(r'<a\s+[^>]*(?:id|name)="([^"]+)"', re.I)
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
MD_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def slug(text):
    """GitHub's heading id: visible text, lowercased, punctuation dropped
    except hyphen, underscore and space, then each space becomes a hyphen."""
    text = MD_LINK.sub(r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = "".join(ch for ch in text if ch.isalnum() or ch in " -_")
    return text.replace(" ", "-")


def prose_lines(text):
    """The page's lines with fenced code blocks left out."""
    kept = []
    fence = None
    for line in text.splitlines():
        if fence is None:
            match = FENCE_OPEN.match(line)
            if match:
                fence = match.group(1)
                continue
            kept.append(line)
        else:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                fence = None
    return kept


def heading_ids(text):
    seen = {}
    found = []
    lines = prose_lines(text)
    for line in lines:
        match = HEAD.match(line)
        if not match:
            continue
        base = slug(match.group(2))
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.append(base if count == 0 else f"{base}-{count}")
    found.extend(ANCHOR.findall("\n".join(lines)))
    return found


def pages():
    found = [ROOT / "README.md", ROOT / "tools" / "README.md", ROOT / "CONTRIBUTING.md"]
    for folder in ("docs", "examples", "evidence"):
        if (ROOT / folder).is_dir():
            found.extend(sorted((ROOT / folder).rglob("*.md")))
    return [page for page in found if page.is_file()]


def targets(text):
    body = "\n".join(prose_lines(text))
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
        for line in broken:
            print("BROKEN " + line)
        print(f"CHECK links: FAIL, {len(broken)} broken")
        return 1
    print("CHECK links: every relative link and anchor in the README files and docs resolves")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--data", default=None)
    args = parser.parse_args()
    if not args.check:
        parser.print_help()
        return 2
    return check()


if __name__ == "__main__":
    sys.exit(main())
