#!/usr/bin/env python3
"""List likely misspellings in the Lands of Lore 1 text tables.

Reads ENG, FRE and GER string tables from the DATA folder you name.
English words are compared with the system word list. A row is one word
that is a single small edit from a dictionary word. French and German
are checked only for a broken offset table or a bigram outside the
decode tables. Nothing here writes a patch or changes a game file.
A person judges the rows.
"""

import re
import struct
import sys

import decode_dialogue as D
from cli_errors import run_cli
import lol1lib as L

LETTERS = "abcdefghijklmnopqrstuvwxyz"
VOWELS = set("aeiou")
TOKEN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
CTRL = re.compile(r"\[(?:CTRL:[0-9A-F]{2}|PARA)\]")


DEFAULT_WORDS = "/usr/share/dict/words"


def dictionary(path=DEFAULT_WORDS):
    words = set()
    try:
        handle = open(path, encoding="latin-1")
    except OSError:
        raise ValueError(f"No English word list at {path}. Give one with --words FILE "
                         "(a plain text file, one word per line).") from None
    with handle:
        for line in handle:
            word = line.strip().lower()
            if word.isalpha() and len(word) >= 3:
                words.add(word)
    return words


def base_form(token):
    for suffix in ("'s", "'S", "n't", "N'T", "'re", "'ve", "'ll", "'d", "'t"):
        if token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def suggestions(word, words):
    """One-edit dictionary neighbours. Edits at the first letter are left out."""
    text = word.lower()
    hits = []
    for index in range(1, len(text) - 1):
        candidate = text[:index] + text[index + 1 :]
        if candidate in words:
            hits.append(("extra", candidate))
    if len(text) >= 5 and not text.endswith("s"):
        candidate = text[:-1]
        if candidate in words:
            hits.append(("extra", candidate))
    for index in range(1, len(text)):
        for letter in LETTERS:
            candidate = text[:index] + letter + text[index:]
            if candidate in words:
                hits.append(("missing", candidate))
    for index in range(len(text) - 1):
        if text[index] == text[index + 1]:
            continue
        candidate = text[:index] + text[index + 1] + text[index] + text[index + 2 :]
        if candidate in words:
            hits.append(("swap", candidate))
    for index, letter in enumerate(text):
        if letter not in VOWELS:
            continue
        for other in VOWELS:
            if other == letter:
                continue
            candidate = text[:index] + other + text[index + 1 :]
            if candidate in words:
                hits.append(("vowel", candidate))
    best = {}
    for kind, candidate in hits:
        shared = 0
        for left, right in zip(text, candidate):
            if left != right:
                break
            shared += 1
        missing_vowel = (
            kind == "missing"
            and shared < len(candidate)
            and candidate[shared] in VOWELS
        )
        if not missing_vowel and shared < 3 and kind != "swap":
            continue
        previous = best.get(kind)
        if previous is None or shared > previous[0]:
            best[kind] = (shared, candidate)
    return [(kind, item[1]) for kind, item in best.items()]


def ordinary_word(stem, words):
    lower = stem.lower()
    if not lower.isalpha() or len(lower) < 5 or lower in words:
        return False
    if lower.endswith("s") and lower[:-1] in words:
        return False
    if lower.endswith("es") and lower[:-2] in words:
        return False
    if lower.endswith("ies") and (lower[:-3] + "y") in words:
        return False
    return True


def table_strings(blob):
    """Return (strings, problem). problem is a short reason, or None."""
    if len(blob) < 2:
        return [], "short"
    count = struct.unpack_from("<H", blob, 0)[0] // 2
    if count <= 0 or 2 * count > len(blob):
        return [], "count"
    offsets = struct.unpack_from(f"<{count}H", blob, 0)
    strings = []
    for offset in offsets:
        if offset >= len(blob):
            return [], "offset"
        end = blob.find(b"\x00", offset)
        if end < 0:
            return [], "end"
        strings.append(blob[offset:end])
    return strings, None


def bigram_out(raw):
    return any(byte & 0x80 and (byte & 0x7F) >= len(D.decodeTable2) for byte in raw)


def scan(data_dir, words):
    files = {"ENG": 0, "FRE": 0, "GER": 0}
    string_count = 0
    bad_table = 0
    bad_bigram = 0
    rows = []
    seen = set()
    for _pak, name, blob in L.find_all("", data_dir):
        if not name.endswith((".ENG", ".FRE", ".GER")):
            continue
        language = name.rsplit(".", 1)[-1]
        files[language] = files.get(language, 0) + 1
        strings, problem = table_strings(blob)
        if problem:
            bad_table += 1
            continue
        for index, raw in enumerate(strings):
            string_count += 1
            if bigram_out(raw):
                bad_bigram += 1
            if language != "ENG":
                continue
            text = CTRL.sub(" ", D.decode_raw(raw))
            for match in TOKEN.finditer(text):
                if match.start() > 0 and text[match.start() - 1] == ".":
                    continue
                stem = base_form(match.group(0))
                if not ordinary_word(stem, words):
                    continue
                hits = suggestions(stem, words)
                if not hits:
                    continue
                key = (name, index, stem.lower(), hits[0][0], hits[0][1])
                if key in seen:
                    continue
                seen.add(key)
                rows.append((name, index, match.group(0), hits))
    return files, string_count, bad_table, bad_bigram, rows


def main():
    parser = L.tool_args(__doc__, writes=False)
    parser.add_argument("--words", default=DEFAULT_WORDS,
                        help=f"English word list, one word per line (default: {DEFAULT_WORDS})")
    args = parser.parse_args()
    if not args.data:
        print("name a DATA folder with --data", file=sys.stderr)
        return 1
    files, string_count, bad_table, bad_bigram, rows = scan(args.data, dictionary(args.words))
    print(
        f"tables ENG {files.get('ENG', 0)} FRE {files.get('FRE', 0)} GER {files.get('GER', 0)} "
        f"strings {string_count} bad-table {bad_table} bad-bigram {bad_bigram} "
        f"candidates {len(rows)}"
    )
    for name, index, token, hits in rows:
        shown = ", ".join(f"{kind}:{candidate}" for kind, candidate in hits)
        print(f"{name} string {index} word {token} suggestion {shown}")
    if args.check and (bad_table or bad_bigram or string_count == 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_cli(main))
