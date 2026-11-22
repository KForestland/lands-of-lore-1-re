# Notes for whoever continues this work

This page is for a person or a program that takes over this repository without the people who built it. It says what the repository is, the rules it keeps, how to check your work, and the mistakes that were made and how they were caught. It works with any editor, assistant or harness: everything here is plain files, git and Python.

## What this is

Documentation and Python tools for *Lands of Lore: The Throne of Chaos* (Westwood, 1993, DOS): how its data files and rules work, checked against the game files and the original program. The reference copy is the English CD-ROM edition (CD1.02, its `DATA` folder) and an English floppy installation. The tools read a person's own copy; the repository holds no game files. Start with README.md, then docs/START_HERE.md and docs/STATUS.md.

## The rules

1. **No game content in the repository.** No game files, no extracted pictures, sounds, music, movies or text dumps, and no converted media. Examples in `examples/` are drawn by the tools without game pixels. `tools/repo_guard.py --check` rejects game files, media, files over 300 KB, machine paths and words on a private local list (`.git/info/private_words`, never committed).
2. **Every statement says how sure it is.** On the pages, `CONFIRMED` means backed by a cited program address or file offset that was checked; `UNCONFIRMED` means a reading, followed by the test that would settle it. A sentence that only restates another page links to it and carries no label. Write "labelled as proved" in prose that is not itself a statement, because the label words are counted.
3. **Narrow claims.** Say which edition, which program, which path through the code, and how many files a check covered. "All" and "every" need the count beside them. Keep proof from the program, proof from the files, and observation in a running game apart.
4. **The rating is counted, not typed.** `tools/rating.py` writes the rating block in README.md and docs/STATUS.md; never edit those lines by hand. The check and test counts on README, STATUS, START_HERE and tools/README are written by `tools/suite_counts.py --write` and verified by its `--check`; never type a count by hand.
5. **Patches** are `lol-patch-3` JSON files in `patches/` (format: docs/formats/patch.md). Each change names its file, offset, the SHA-256 of the span it replaces, and the new bytes. `tools/patch.py apply` writes the patched files and a private `undo.json` to a new folder; applying twice is refused; undoing must give the original bytes back exactly. A fix ships only if it gives back a path the game already has, and only after it was applied and undone on a copy. A patch never touches a disc check, serial check or other copy protection.
6. **Commits.** Author and committer are the project's noreply identity: `git -c user.name=KForestland -c user.email=261564562+KForestland@users.noreply.github.com commit ...`. No personal names, machine paths or internal working names in commit messages or pages; the guard checks commit messages too. Ask the owner before any release, tag or announcement.
7. **The review gate.** A change is reviewed from a clean export of the exact commit (for example `git archive`), not from the writer's working folder. The reviewer re-derives every changed proved line from the bytes, not from the page. `tools/page_facts.py --check` lists proved lines whose literals changed; each listed line is re-derived before merging. Only then is it merged and pushed.

## Addresses

Code addresses are file offsets in `MAIN.EXE` (or `MAINW.EXE`, `FINALE.EXE`) unless a page says otherwise. Overlay code (FBOV) has no fixed segment; a page that cites `segment:offset` gives the directory row it resolved through. Say which edition (CD or floppy) and which program every address belongs to; the two editions differ.

## How to check your work

Requirements: Python 3.10 or later; Pillow and capstone (`pip install -r requirements.txt`).

```sh
export LOL1_DATA=/path/to/your/copy   # the CD `DATA` folder, or the floppy install folder
python3 tools/check_all.py --data "$LOL1_DATA"   # last line: ALL n CHECKS PASSED (README.md shows n, generated)
python3 tools/rating.py --check --data "$LOL1_DATA"
python3 tools/page_facts.py --check --data "$LOL1_DATA"
python3 -m unittest
python3 tools/doc_links.py --check
python3 tools/suite_counts.py --check   # pages that show check and test counts; refresh with --write
python3 tools/doc_index.py --check   # after adding a page: python3 tools/doc_index.py --out docs/index.json
python3 tools/repo_guard.py --check --release
```

Without game files, the unit tests, doc_index, page_facts and repo_guard still run; GitHub Actions runs those on Linux, Windows and macOS with Python 3.10 and 3.12.

Run `tools/check_all.py` once on the CD `DATA` folder and once on the floppy installation folder. Both runs must pass. Run the full list on the exact commit you are about to hand over, not on an earlier one. The tools write only where you point them (`--out`); the tree must be clean after the checks.

## Where the open work is

- docs/OPEN_QUESTIONS.md: the numbered questions and their state.
- docs/NEEDS_A_RUNNING_GAME.md: what can only be settled in the running game, the probes, and the rules for a launch record.
- docs/STATUS.md: the open column of every row.
- patches/README.md: reported faults and where each one sits.
- docs/CORRECTIONS.md: what was wrong before and how it was caught.

## What "done" means

Here, "done" has a definition: docs/STATUS.md: a format row is done when it has a page, a working reader, a passing check on both editions where they differ, and no open point. Nothing is called complete or understood as a whole; the rating counts work, not a percentage.

## Ten mistakes we made, and how they were caught

1. **Summary words stronger than the evidence** ("almost fully understood"). A reader new to the pages caught it; the summary became a counted rating and an open-questions list.
2. **Counts typed by hand went stale** (check counts, question counts, file counts on several pages). Caught by fresh readers more than once. Counts are now generated (`tools/suite_counts.py`); when you add a check, run its `--write`.
3. **A byte layout misread** (a field read as little-endian that holds a big-endian value). Caught when an independent reader of the same bytes disagreed. Re-derive a layout with a second program before you build on it.
4. **Statements labelled as proved that only restated other pages,** or whose expected values were taken from the pages instead of the bytes. Caught in review. The reviewer re-derives from the original files only.
5. **A claim scoped to the wrong edition or program** (a filename named by the floppy programs only, written as true for the CD). Caught by an independent reviewer. Name the edition and program for every address.
6. **A breakpoint at code that does not run on the path in question** (a setup routine instead of the per-frame routine). Caught by a static second reading after runs failed to stop. List the callers before choosing a stop.
7. **A pixel colour decoded with the wrong format** (a 24-bit capture read as 16-bit). Caught by the writer's own audit of the raw capture. Read the capture's header and bytes, not a derived picture.
8. **A batch handed over without running the full checks on its exact commit;** one word of prose changed a counted label and the rating check failed. Caught by the final reviewer. Always run everything on the exact head.
9. **Hygiene leaks:** a machine temporary path in a report, an internal working name in a commit subject, converted game music committed. Caught before or at push; the guard now rejects each of them.
10. **A tool file named like a standard Python module** (`numbers.py`) broke another tool, and its check was not in `check_all.py`. Caught by the full check. Prefix tool names and register every new check.

Two habits caught most of these: an independent reader who did not write the work, and a sample of proved statements re-derived from the bytes (docs/CONFIRMED_SAMPLE.md, docs/CHECK_AUDIT.md).

