#!/usr/bin/env python3
"""Read the repository's Markdown pages and build a page and question index.

The answers field follows the Page or Where column of OPEN_QUESTIONS.md.
The indexed question keeps the state written in that page's summary table.
Other question citations appear as references. Tool paths name existing tool
sources and include citations in command examples.
"""
from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from cli_errors import ReaderArgumentParser, run_cli
from doc_links import HEAD, MD_LINK, prose_lines, targets

ROOT = Path(__file__).resolve().parents[1]
INDEX = "docs/index.json"
QUESTIONS = "docs/OPEN_QUESTIONS.md"
PAGE_FOLDERS = (".github", "data", "docs", "evidence", "examples", "future-patches", "tools")
QUESTION_ROW = re.compile(r'^\|\s*(?:<a\b[^>]*></a>\s*)?(Q[1-9]\d*)\s*\|')
QUESTION_ID = re.compile(r"\bQ[1-9]\d*\b")
TOOL_PATH = re.compile(r"(?<![\w./-])(?:[\w.-]+/)*[\w-]+\.(?:py|c)\b")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)
YAML_NAME = re.compile(r"^name:[ \t]*([^\n]+)", re.MULTILINE)


def tracked_pages(root):
    """Return the Markdown files git tracks, or None outside a git checkout."""
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        if Path(top).resolve() != root.resolve():
            return None
        listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", "*.md"],
                                capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [root / name for name in listed.decode("utf-8").split("\0") if name]


def page_paths(root):
    # Inside a checkout, untracked local notes stay out of the index.
    tracked = tracked_pages(root)
    if tracked is None:
        paths = list(root.glob("*.md"))
        for name in PAGE_FOLDERS:
            paths.extend((root / name).rglob("*.md"))
    else:
        paths = [path for path in tracked if path.is_file() and (
            path.parent == root or path.relative_to(root).parts[0] in PAGE_FOLDERS)]
    return sorted(path.relative_to(root).as_posix() for path in paths)


def title(path, text):
    # GitHub issue templates carry their title in the front matter.
    front = FRONT_MATTER.match(text)
    name = YAML_NAME.search(front[1]) if front else None
    if name:
        return name[1].strip().strip("\"'")
    for line in prose_lines(text):
        heading = HEAD.match(line)
        if heading:
            return MD_LINK.sub(r"\1", heading[2]).replace("`", "").strip()
    return Path(path).stem.replace("_", " ").replace("-", " ")


def relative_target(page, link, root):
    parts = urlsplit(link)
    if parts.scheme or parts.netloc or not parts.path:
        return None
    target = (root / Path(page).parent / unquote(parts.path)).resolve()
    try:
        return target.relative_to(root).as_posix()
    except ValueError:
        return None


def linked_pages(page, text, paths, root):
    return {path for link in targets(text)
            if (path := relative_target(page, link, root)) in paths}


def question_tables(text, paths, root):
    questions = {}
    answers = {}
    references = defaultdict(set)
    section = ""
    for line in prose_lines(text):
        if line.startswith("## "):
            section = line[3:].strip()
        row = QUESTION_ROW.match(line)
        if row is None:
            continue
        question = row[1]
        if section == "At a glance":
            if question in questions:
                raise ValueError(f"{question} appears twice in the question summary")
            state = line[row.end():].split("|", 1)[0].strip()
            questions[question] = state
        elif section == "Questions":
            if question in answers:
                raise ValueError(f"{question} appears twice in the question detail table")
            cell = line.rsplit("|", 2)[-2]
            answers[question] = linked_pages(QUESTIONS, cell, paths, root)
        if section != "At a glance":
            for path in linked_pages(QUESTIONS, line, paths, root):
                references[path].add(question)
    if not questions or questions.keys() != answers.keys():
        raise ValueError("question summary and detail tables have different IDs")
    return {
        q: {"state": questions[q], "answer_pages": sorted(answers[q])}
        for q in sorted(questions, key=question_number)
    }, references


def question_number(question):
    return int(question[1:])


def cited_tools(page, text, root, sources):
    found = set()
    for token in TOOL_PATH.findall(text):
        path = relative_target(page, token, root)
        if path is not None and "/" in path and path in sources:
            found.add(path)
        elif "/" in token and token in sources:
            found.add(token)
        elif "/" not in token and len(sources.get(token, ())) == 1:
            found.add(sources[token][0])
    return sorted(found)


def build(root):
    paths = page_paths(root)
    texts = {path: (root / path).read_text(encoding="utf-8") for path in paths}
    questions, references = question_tables(texts[QUESTIONS], set(paths), root)
    answers = defaultdict(set)
    for question, row in questions.items():
        for page in row["answer_pages"]:
            answers[page].add(question)

    sources = defaultdict(list)
    for path in sorted((root / "tools").rglob("*")):
        if path.suffix in {".py", ".c"}:
            name = path.relative_to(root).as_posix()
            sources[name] = [name]
            sources[path.name].append(name)

    pages = []
    for path, text in texts.items():
        prose = "\n".join(prose_lines(text))
        mentioned = set(QUESTION_ID.findall(prose)) & questions.keys()
        for link in targets(prose):
            if relative_target(path, link, root) == QUESTIONS:
                question = urlsplit(link).fragment.upper()
                if question in questions:
                    mentioned.add(question)
        pages.append({
            "path": path,
            "title": title(path, text),
            "answers": sorted(answers[path], key=question_number),
            "question_references": sorted((references[path] | mentioned) - answers[path], key=question_number),
            "tools": cited_tools(path, text, root, sources),
        })
    return {"schema_version": 1, "question_source": QUESTIONS, "questions": questions, "pages": pages}


def main():
    parser = ReaderArgumentParser(description=__doc__)
    parser.add_argument("--data", help="accepted for the common runner; no game data needed")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--out", type=Path, help="write the generated JSON to this file")
    mode.add_argument("--check", action="store_true", help="compare the index with the current pages")
    args = parser.parse_args()
    result = build(ROOT)
    rendered = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check:
        if (ROOT / INDEX).read_bytes() != rendered:
            raise ValueError(f"{INDEX} differs from the current pages; regenerate with --out {INDEX}")
        print(f"CHECK doc_index: {len(result['pages'])} pages and {len(result['questions'])} questions match {INDEX}")
    elif args.out:
        args.out.write_bytes(rendered)
    else:
        sys.stdout.buffer.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
