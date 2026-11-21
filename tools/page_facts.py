#!/usr/bin/env python3
"""Check documented literals against the original bytes and report coverage.

--check compares the Markdown with the witness registry and the reviewed
prose inventory. --list gives the page and reason for each prose-only
literal. --inventory prints a proposed inventory for review after a
documentation edit. It never rewrites the registry or inventory.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys

from cli_errors import ReaderArgumentParser, run_cli
from doc_links import FENCE_OPEN
from page_facts_auto import observed as observe_auto, probes as automatic_probes

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "data/page_facts.json"
INVENTORY = "data/page_facts_coverage.json"
PROSE_REASON = "No independent byte reader is registered for this claim yet."
LABEL = re.compile(r"(?<!\w)\*{0,2}(CONFIRMED|PROVEN|UNCONFIRMED|UNKNOWN)\b\*{0,2}")
HEADING = re.compile(r"^(#{1,6})\s+(.+)")
MEASURED = re.compile(r"^(?:confirmed\b|worked example\b)", re.I)
EXCLUDED = {"CORRECTIONS.md", "GLOSSARY.md", "HOW_WE_RATE.md"}
NUMBER = r"(?:\d{1,3}(?:,\d{3})+|\d+)"
LITERAL = re.compile(
    r"`[^`\n]+`|(?<![\w])(?:\+?0x[\da-fA-F]+|"
    + NUMBER + r"(?:\.\d+)?%?|[+−-]\d+)(?![\w])"
    r"|\b[A-Z][A-Z0-9_\\/.-]+\.[A-Z][A-Z0-9_]{1,4}\b"
)
VALUE = {
    "number": NUMBER,
    "hex": r"(?:0x)?[\da-fA-F]+",
    "name": r"[a-zA-Z0-9_./\\-]+",
    "step": r"[+−-]\d+",
    "word": r"[a-zA-Z]+",
    "text": r"[^`\n]+",
}
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


@dataclass(frozen=True)
class Fact:
    page: str
    line: int
    value: str
    witnessed: bool


def load(root, filename):
    return json.loads((root / filename).read_text(encoding="utf-8"))


def read_pages(root):
    for path in sorted((root / "docs").rglob("*.md")):
        body = path.read_text(encoding="utf-8")
        if path.name in EXCLUDED or any(x.startswith("> **History") for x in body.splitlines()[:6]):
            continue
        yield path.relative_to(root).as_posix(), body


def measured_fragment(prose, active):
    """Keep only the parts of a line within a positive evidence label."""
    parts = []
    pos = 0
    for index, match in enumerate(LABEL.finditer(prose)):
        positive = match[1] in {"CONFIRMED", "PROVEN"}
        if active or (index == 0 and positive):
            parts.append(prose[pos:match.start()])
        active = positive
        pos = match.start()
    if active:
        parts.append(prose[pos:])
    return " ".join(part.strip() for part in parts if part.strip()), active


def measured_lines(body):
    """Keep physical line numbers through comments, fences, headings and tables."""
    sections = []
    lines = HTML_COMMENT.sub(lambda m: "\n" * m[0].count("\n"), body).splitlines()
    fence = None
    group = []
    intro = False

    def flush():
        if not group:
            return
        measured = bool(sections and sections[-1][1])
        labels_in_group = [tag for _, prose in group for tag in LABEL.findall(prose)]
        if labels_in_group and set(labels_in_group) <= {"CONFIRMED", "PROVEN"}:
            measured = True
        for line, prose in group:
            fragment, measured = measured_fragment(prose, measured or intro)
            if fragment:
                yield line, fragment

    for line, prose in enumerate(lines, 1):
        if fence:
            closing = prose.strip()
            if len(closing) >= len(fence) and set(closing) == {fence[0]}:
                fence = None
            continue
        if not prose.strip() or HEADING.match(prose) or FENCE_OPEN.match(prose) or prose.lstrip().startswith("|"):
            yield from flush()
            if group:
                last = group[-1][1].rstrip()
                intro = last.endswith(":") and any(
                    match in {"CONFIRMED", "PROVEN"} for _, part in group for match in LABEL.findall(part)
                )
                group = []
            if not prose.strip():
                continue
            start = FENCE_OPEN.match(prose)
            if start:
                fence = start[1]
                intro = False
                continue
            heading = HEADING.match(prose)
            if heading:
                depth = len(heading[1])
                while sections and sections[-1][0] >= depth:
                    sections.pop()
                measured = bool(MEASURED.match(heading[2]) or (sections and sections[-1][1]))
                if re.match(r"(?:open|unconfirmed|unknown)\b", heading[2], re.I):
                    measured = False
                sections.append((depth, measured))
                intro = False
                continue
            fragment, _ = measured_fragment(prose, bool(intro or (sections and sections[-1][1])))
            if fragment:
                yield line, fragment
            continue
        if not group and intro and not re.match(r"\s*(?:[-*]|\d+\.)\s", prose):
            intro = False
        group.append((line, prose))
    yield from flush()


def normalize(value, kind):
    if kind == "hex":
        return int(value, 16)
    if kind in {"number", "step"}:
        return int(value.replace(",", "").replace("−", "-"))
    return value


def locate(body, anchor):
    """Anchors are literal surrounding text, with a single typed value."""
    start = re.escape(anchor["before"])
    end = re.escape(anchor["after"])
    kind = anchor["kind"]
    pattern = start + r"(?P<value>" + VALUE[kind] + r")" + end
    matches = list(re.finditer(pattern, body))
    if len(matches) != 1:
        # Point at the surviving anchor if the value spelling or the other side changed.
        offset = max(body.find(anchor["before"]), 0)
        raise ValueError(f"{body.count(chr(10), 0, offset) + 1}: expected one anchor {anchor['before']!r}")
    match = matches[0]
    return body.count("\n", 0, match.start("value")) + 1, match["value"]


def scan(root, registry, automatic=None):
    pages = dict(read_pages(root))
    anchors, claims, issues = defaultdict(Counter), {}, []
    for fact_id, fact in registry.items():
        claims[fact_id] = []
        for anchor in fact["anchors"]:
            page = anchor["page"]
            try:
                line, value = locate(pages.get(page, ""), anchor)
            except ValueError as error:
                issues.append(f"{page}:{error} ({fact_id})")
                continue
            anchors[page][(line, value)] += 1
            claims[fact_id].append((page, line, value, anchor["kind"]))

    facts, inventory, inferred = [], {}, []
    for page, body in pages.items():
        measured = dict(measured_lines(body))
        if automatic:
            for claim in automatic_probes(body, measured, automatic):
                inferred.append((page, claim))
                if claim.reader[0] != "arithmetic":
                    anchors[page][(claim.line, claim.shown)] += 1
        for line, _ in anchors[page]:
            measured.setdefault(line, body.splitlines()[line - 1])
        pending = []
        for line, prose in sorted(measured.items()):
            remaining = []
            on_line = Counter({value: count for (row, value), count in anchors[page].items() if row == line})
            for match in LITERAL.finditer(prose):
                value = match[0].strip("`")
                claimed = on_line[value] > 0
                if claimed:
                    on_line[value] -= 1
                facts.append(Fact(page, line, value, claimed))
                if not claimed:
                    remaining.append(value)
            # A typed value can be embedded in a backticked file+offset or formula.
            for value, count in on_line.items():
                facts.extend(Fact(page, line, value, True) for _ in range(count))
            if remaining:
                digest = sha256(" ".join(prose.split()).encode("utf-8")).hexdigest()[:32]
                pending.append([line, digest])
        if pending:
            inventory[page] = pending
    return facts, inventory, claims, issues, inferred


def inventory_errors(current, saved):
    for page in sorted(current.keys() | saved.keys()):
        old = Counter(digest for _, digest in saved.get(page, []))
        new = Counter(digest for _, digest in current.get(page, []))
        added, removed = new - old, old - new
        for line, digest in current.get(page, []):
            if added[digest]:
                yield f"{page}:{line}: unreviewed literal or changed prose-only claim"
                added[digest] -= 1
        # Deletions, including lost proof labels, also need review. The line is the prior location.
        for line, digest in saved.get(page, []):
            if removed[digest]:
                yield f"{page}:{line}: previously inventoried claim changed or disappeared"
                removed[digest] -= 1


def print_inventory(inventory):
    print('{"reason": ' + json.dumps(PROSE_REASON) + ', "pages": {')
    for index, (page, entries) in enumerate(inventory.items()):
        separator = "" if index == 0 else ",\n"
        print(separator + "  " + json.dumps(page) + ": [", end="")
        print(",\n    ".join(json.dumps(entry) for entry in entries), end="]")
    print("\n}}")


def summary(facts):
    return f"{sum(f.witnessed for f in facts):,}/{len(facts):,} candidate literals registered"


def coverage(root=ROOT):
    registry = load(root, REGISTRY)
    return summary(scan(root, registry["facts"], registry.get("automatic"))[0])


def main():
    from page_facts_native import DATA_ENV, WitnessUnavailable, edition_status, game_file, is_cd, read_witness

    parser = ReaderArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=os.environ.get(DATA_ENV))
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--list", action="store_true")
    modes.add_argument("--inventory", action="store_true")
    args = parser.parse_args()
    registry = load(ROOT, REGISTRY)
    facts, inventory, claims, issues, inferred = scan(ROOT, registry["facts"], registry.get("automatic"))
    if args.inventory:
        if not issues:
            print_inventory(inventory)
            return 0
    saved = load(ROOT, INVENTORY) if not args.inventory else None
    if args.list:
        for f in facts:
            if not f.witnessed:
                print(f"{f.page}:{f.line}: {f.value!r}: {saved['reason']}")
    if saved is not None:
        issues.extend(inventory_errors(inventory, saved["pages"]))

    detail = ""
    skipped = set()
    if args.check:
        skip = edition_status(args.data) if args.data else "no original data folder supplied"
        for page, claim in inferred:
            try:
                if not skip and claim.edition and claim.edition != ("CD" if is_cd(args.data) else "floppy"):
                    raise WitnessUnavailable(f"{claim.edition} file citations excluded on this edition")
                result = observe_auto(claim, None if skip else args.data, read_witness, game_file)
                if result is None:
                    continue
                observed, source = result
                if observed != claim.expected:
                    value = observed.hex(" ") if isinstance(observed, bytes) else repr(observed)
                    wanted = claim.expected.hex(" ") if isinstance(claim.expected, bytes) else repr(claim.expected)
                    issues.append(f"{page}:{claim.line}: {claim.shown!r} claims {wanted}, read {value} from {source}")
            except WitnessUnavailable as error:
                skipped.add(str(error))
            except (OSError, ValueError, IndexError) as error:
                issues.append(f"{page}:{claim.line}: {error}")
        if skip:
            detail = f"; skipped {registry['edition']} byte witnesses: {skip}"
        else:
            for fact_id, fact in registry["facts"].items():
                try:
                    observed, source = read_witness(args.data, fact["reader"])
                except WitnessUnavailable as error:
                    skipped.add(str(error))
                    continue
                except (OSError, ValueError, IndexError) as error:
                    issues.extend(f"{page}:{line}: {fact_id}: {error}" for page, line, _, _ in claims[fact_id])
                    continue
                for page, line, value, kind in claims[fact_id]:
                    if normalize(value, kind) != observed:
                        native = f"{observed:#x}" if kind == "hex" else repr(observed)
                        issues.append(f"{page}:{line}: {fact_id} claims {value!r}, read {native} from {source}")
    if skipped:
        detail += "; skipped " + ", ".join(sorted(skipped))
    for issue in issues:
        print(issue, file=sys.stderr)
    print(f"CHECK page facts: {summary(facts)}; {len(issues):,} issue(s){detail}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
