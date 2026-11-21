"""Find common citations in measured Markdown and read their sources."""
from dataclasses import dataclass
from fnmatch import fnmatchcase
from functools import lru_cache
from pathlib import Path
import re
from struct import unpack_from
import subprocess
import sys

FILE = r"(?:(?:DAT|HARDRIVE)[/\\])?[A-Za-z0-9_][A-Za-z0-9_.-]*\.[A-Za-z0-9_]{1,4}"
OFFSET = r"0x[0-9A-Fa-f]+"
HEX_BYTE = re.compile(r"[0-9a-fA-F]{2}")
HEX_BYTES = re.compile(rf"{HEX_BYTE.pattern}(?:[ \t]+{HEX_BYTE.pattern}){{0,31}}")
BYTE_WORDS = re.compile(r"[0-9A-Za-z]{2}(?:[ \t]+[0-9A-Za-z]{2}){1,31}")
DECIMAL = r"(?:\d{1,3}(?:,\d{3})+|\d+)"
QUOTED = r"[^`\n]{1,96}"
ADDRESS = rf"`(?P<file>{FILE})\+(?P<offset>{OFFSET})`"
FORWARD = re.compile(
    rf"{ADDRESS}\s+(?P<verb>has|holds|starts with|contains|is|stores|with)\s+"
    rf"(?:(?P<qualifier>the full|the literal|bytes)\s+)?`(?P<value>{QUOTED})`"
)
REVERSE = re.compile(
    rf"(?:\b(?:suffix|literal|string)\s+`(?P<value>{QUOTED})`\s+(?:at|from)\s+"
    rf"|`(?P<stored>{QUOTED})`\s+is stored at\s+){ADDRESS}"
)
SIZE = re.compile(rf"`(?P<file>{FILE})`\s*\((?P<value>{DECIMAL}) bytes\)")
PAIR_SIZE = re.compile(rf"`(?P<a>{FILE})` and `(?P<b>{FILE})`\s+are (?P<value>{DECIMAL}) bytes\b")
PAIRED = re.compile(
    rf"\b(?:LE|PE) `\+{OFFSET}` and `\+{OFFSET}`"
    rf"\s*\(file `\+(?P<a>{OFFSET})` and `\+(?P<b>{OFFSET})`,"
    r"\s+bytes `(?P<x>[^`\n]+)` and `(?P<y>[^`\n]+)`\)"
)
RECORD = re.compile(
    rf"\btable of (?P<total>{DECIMAL})-byte [^.\n]+\s+definitions\.\s*"
    rf"Its (?P<body>{DECIMAL})-byte [^.\n]+ is followed by a (?P<tag>{DECIMAL})-byte"
)
COMMAND = re.compile(r"`(?:python3?\s+)?(?:tools/)?([\w-]+\.py)\s+--check(?:[^`\n]+)?`")
ARCHIVE_ENTRY = re.compile(
    rf"`(?P<file>{FILE})`\s+entry\s+(?P<entry>\d+)\b\s*"
    rf"(?:is(?:\s+the [A-Z]+:)?|, the [A-Z]+: file offset {DECIMAL},)\s+(?P<value>{DECIMAL}) bytes\b"
)
ENTRY_SIZE = re.compile(rf"\bEntry (?P<entry>\d+) is (?P<value>{DECIMAL}) bytes\b")
PE_ROW = re.compile(
    rf"^\|\s*(?:`(?P<file>{FILE})`)?\s*\|\s*`(?P<section>[.\w]+)`\s*\|"
    + "".join(rf"\s*`(?P<{field}>{OFFSET})`\s*\|" for field in ("rva", "virtual", "offset", "stored"))
    + r"\s*$"
)
NAMED_LITERAL = re.compile(
    rf"`(?P<value>(?:-[A-Z][A-Z0-9_-]*|{FILE}))`\s+"
    rf"(?:occurs|appears|is (?:present|stored)) in `(?P<file>{FILE})`"
)
OPTION_LIST = re.compile(r"The strings are (?P<names>[^.\n]+), respectively at file `(?P<offsets>[^`\n]+)`")
OPERAND = re.compile(rf"\bat `(?P<value>{OFFSET})` \(`(?P<instruction>\+?{OFFSET})`\)")


@dataclass(frozen=True)
class Claim:
    line: int
    shown: str
    expected: object
    reader: tuple
    edition: str = ""
    error: str = ""


def parse_number(text):
    return int(text.replace(",", ""))


def edition_hint(text, offset):
    prefix = text[text.rfind("\n", 0, offset) + 1:offset]
    qualifiers = re.findall(r"\b(CD|floppy)\b", prefix, re.I)
    if not qualifiers:
        return ""
    return "CD" if qualifiers[-1].upper() == "CD" else "floppy"


def byte_claim(line, value, name, offset, *, shown, edition=""):
    reader = ("bytes_at", name, offset)
    if HEX_BYTES.fullmatch(value):
        return Claim(line, shown, bytes.fromhex(value), reader, edition)
    return Claim(line, shown, None, reader, edition,
                 f"malformed hexadecimal byte list {value!r} at {name}+{offset:#x}")


def quoted_claim(line, value, name, offset, *, verb="", qualifier="", edition=""):
    # An unlabelled list can have one mistyped byte word and still be a byte citation.
    byte_words = BYTE_WORDS.fullmatch(value) and sum(
        not HEX_BYTE.fullmatch(token) for token in value.split()
    ) <= 1
    if qualifier == "bytes" or byte_words:
        return byte_claim(line, value, name, offset, shown=value, edition=edition)
    # A quoted number or field expression is not a NUL-terminated string.
    if re.fullmatch(r"[+−-]?(?:0x[\da-fA-F]+|\d+)", value):
        return None
    if not value.isascii() or not re.search(r"[A-Za-z]", value):
        return None
    if verb == "starts with":
        kind = "string_prefix"
    elif re.fullmatch(FILE, value):
        kind = "string_token"
    else:
        kind = "string_at"
    return Claim(line, value, value, (kind, name, offset), edition)


def probes(text, measured, config):
    """Recognize citations in positive evidence, preserving source line numbers."""
    def line(offset):
        return text.count("\n", 0, offset) + 1

    def eligible(match):
        row = line(match.start())
        initial = match[0].split("\n", 1)[0].strip()
        return row in measured and initial in measured[row]

    def loose(name):
        return any(fnmatchcase(name.upper(), pattern) for pattern in config.get("loose_files", []))

    found = []
    for regex in (FORWARD, REVERSE):
        for match in regex.finditer(text):
            if not eligible(match):
                continue
            fields = match.groupdict()
            key = "value" if fields.get("value") is not None else "stored"
            claim = quoted_claim(line(match.start(key)), match[key], match["file"], int(match["offset"], 16),
                                 verb=fields.get("verb", ""), qualifier=fields.get("qualifier", ""),
                                 edition=edition_hint(text, match.start()))
            if claim:
                found.append(claim)
    for match in SIZE.finditer(text):
        if eligible(match) and loose(match["file"]):
            value = match["value"]
            found.append(Claim(line(match.start("value")), value, parse_number(value),
                               ("file_size", match["file"]), edition_hint(text, match.start())))
    for match in PAIR_SIZE.finditer(text):
        if eligible(match) and loose(match["a"]) and loose(match["b"]):
            value = match["value"]
            for name in ("a", "b"):
                found.append(Claim(line(match.start("value")), value, parse_number(value),
                                   ("file_size", match[name]), edition_hint(text, match.start())))
    executable = config.get("executable")
    if executable:
        for match in PAIRED.finditer(text):
            if eligible(match):
                for offset, value in (("a", "x"), ("b", "y")):
                    found.append(byte_claim(line(match.start(offset)), match[value], executable,
                                            int(match[offset], 16), shown=match[offset]))
        for match in OPTION_LIST.finditer(text):
            if eligible(match):
                names = re.findall(r"`(-[A-Z][A-Z0-9_-]*)`", match["names"])
                offsets = re.findall(r"\+" + OFFSET, match["offsets"])
                if names and len(names) == len(offsets):
                    for option, offset in zip(names, offsets):
                        found.append(Claim(line(match.start("names")), option, option,
                                           ("string_at", executable, int(offset, 16))))
        if config.get("absolute_operands"):
            for match in OPERAND.finditer(text):
                if eligible(match):
                    value = match["value"]
                    found.append(Claim(line(match.start("value")), value, int(value, 16),
                                       ("absolute_operand", executable, int(match["instruction"], 16)),
                                       edition_hint(text, match.start())))
    for match in NAMED_LITERAL.finditer(text):
        if eligible(match):
            value = match["value"]
            found.append(Claim(line(match.start("value")), value, value,
                               ("string_in", match["file"]), edition_hint(text, match.start())))
    for match in RECORD.finditer(text):
        if eligible(match):
            found.append(Claim(line(match.start("body")), match["body"], parse_number(match["body"]),
                               ("arithmetic", parse_number(match["total"]), parse_number(match["tag"]))))
    extensions = tuple(config.get("archive_entries", []))
    if extensions:
        matches = [(match, match["file"]) for match in ARCHIVE_ENTRY.finditer(text)]
        title_archive = re.search(rf"^# [^\n]+ in (?P<file>{FILE})\s*$", text, re.M)
        if title_archive:
            matches.extend((match, title_archive["file"]) for match in ENTRY_SIZE.finditer(text))
        for match, name in matches:
            if eligible(match) and name.upper().endswith(extensions):
                value = match["value"]
                found.append(Claim(line(match.start("value")), value, parse_number(value),
                                   ("archive_size", name, int(match["entry"]))))
    if config.get("pe_sections"):
        current_file = None
        for row, content in enumerate(text.splitlines(), 1):
            match = PE_ROW.match(content)
            if not match:
                current_file = None
                continue
            if match["file"]:
                current_file = match["file"]
            if current_file and current_file in config["pe_sections"]:
                for field in ("rva", "virtual", "offset", "stored"):
                    value = match[field]
                    found.append(Claim(row, value, int(value, 16),
                                       ("pe_section", current_file, match["section"], field)))
    for command in COMMAND.finditer(text):
        if not eligible(command):
            continue
        tail = text[command.end():command.end() + 240].split("\n\n", 1)[0]
        for unit, reported in config.get("counts", {}).get(command[1], {}).items():
            match = re.search(rf"(?<![\d,])({DECIMAL})\s+{re.escape(unit)}\b", tail)
            if match and line(command.end() + match.start()) in measured:
                value = match[1]
                found.append(Claim(line(command.end() + match.start()), value, parse_number(value),
                                   ("check_count", command[1], reported), edition_hint(text, command.end() + match.start())))
    return found


@lru_cache(maxsize=16)
def check_output(tool, data):
    # Only names explicitly listed in the checked-in registry reach this reader.
    if not re.fullmatch(r"[a-z0-9_]+\.py", tool) or tool in {"check_all.py", "page_facts.py", "rating.py"}:
        raise ValueError(f"unsupported count source {tool}")
    path = Path(__file__).with_name(tool)
    result = subprocess.run([sys.executable, str(path), "--check", "--data", str(data)],
                            capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"{tool} --check failed while reading the original data")
    return result.stdout


def observed(claim, data, read_witness, original_file):
    kind, *parts = claim.reader
    if kind == "arithmetic":
        total, tag = parts
        return total - tag, f"stated record size {total} minus tag size {tag}"
    if data is None:
        return None
    if kind == "check_count":
        tool, unit = parts
        hits = re.findall(rf"(?<![\d,])({DECIMAL})\s+{re.escape(unit)}\b", check_output(tool, data))
        if len(hits) != 1:
            raise ValueError(f"{tool} --check did not print one count for {unit!r}")
        return parse_number(hits[0]), f"{tool} --check ({unit})"
    if kind == "file_size":
        name, = parts
        return original_file(data, name).stat().st_size, name
    if kind == "string_in":
        name, = parts
        literal = claim.expected.encode("ascii") + b"\0"
        found = literal in original_file(data, name).read_bytes()
        return claim.expected if found else "absent", name
    if kind not in {"bytes_at", "string_at", "string_prefix", "string_token"}:
        return read_witness(data, claim.reader)
    name, offset = parts
    with original_file(data, name).open("rb") as source:
        source.seek(offset)
        if kind == "bytes_at":
            value = source.read(len(claim.expected))
        elif kind == "string_prefix":
            value = source.read(len(claim.expected)).decode("ascii", errors="backslashreplace")
        else:
            raw = source.read(256)
            if b"\0" not in raw:
                raise ValueError(f"no NUL-terminated string at {name}+{offset:#x}")
            raw = raw.split(b"\0", 1)[0]
            if kind == "string_token":
                raw = raw.splitlines()[0] if raw else raw
            value = raw.decode("ascii", errors="backslashreplace")
    return value, f"{name}+{offset:#x}"


def x86_operand(code, width):
    """Read an immediate, moffs, or absolute ModRM displacement."""
    opcode = code[0]
    if opcode in {0x68, *range(0xB8, 0xC0), *range(0xA0, 0xA4)}:
        at = 1
    elif opcode in {0x8B, 0x89, 0x8D, 0xC7}:
        mod, rm = code[1] >> 6, code[1] & 7
        if mod == 0 and rm == (6 if width == 2 else 5):
            at = 2
        elif width == 4 and mod == 0 and rm == 4 and code[2] & 7 == 5:
            at = 3
        elif opcode == 0xC7 and mod == 0 and rm in {0, 1, 2, 3, 7}:
            at = 2
        else:
            raise ValueError("instruction has no supported absolute operand")
    else:
        raise ValueError("unsupported x86 instruction for an absolute operand")
    return unpack_from("<H" if width == 2 else "<I", code, at)[0]
