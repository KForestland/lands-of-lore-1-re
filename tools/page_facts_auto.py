"""Recognize common raw citations and arithmetic stated on measured pages."""
from dataclasses import dataclass
import re

FILE = r"(?:(?:DAT|HARDRIVE)[/\\])?[A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:DAT|EXE|MIX|PAK|WSX|TLK|LCF|HDR|ICO|PIF)"
OFFSET = r"0x[0-9A-Fa-f]+"
BYTE = r"[\da-fA-F]{2}"
BYTES = BYTE + r"(?:[ \t]+" + BYTE + r"){1,31}"
DECIMAL = r"(?:\d{1,3}(?:,\d{3})+|\d+)"
DIRECT = re.compile(
    rf"`(?P<file>{FILE})\+(?P<offset>{OFFSET})`\s+"
    rf"(?:has|holds|starts with|contains|is|with)\s+(?:bytes\s+)?`(?P<value>{BYTES})`"
)
SIZE = re.compile(rf"`(?P<file>DAT[/\\][A-Za-z0-9_.-]+)`\s*\((?P<value>{DECIMAL}) bytes\)")
PAIR_SIZE = re.compile(rf"`(?P<a>HARDRIVE[/\\][\w.]+)` and `(?P<b>HARDRIVE[/\\][\w.]+)`"
                       rf"\s+are (?P<value>{DECIMAL}) bytes\b")
STORES = re.compile(rf"`(?P<file>{FILE})\+(?P<offset>{OFFSET})`\s+stores\s+"
                    r"(?:the full )?`(?P<value>[^`\n]+)`")
STRING = re.compile(
    rf"\b(?:suffix|literal|string)\s+`(?P<value>[^\s`]+)`\s+(?:at|from)\s+"
    rf"`(?P<file>{FILE})\+(?P<offset>{OFFSET})`"
)
PAIRED = re.compile(
    rf"\b(?:LE|PE) `\+{OFFSET}` and `\+{OFFSET}`"
    rf"\s*\(file `\+(?P<a>{OFFSET})` and `\+(?P<b>{OFFSET})`,"
    rf"\s+bytes `(?P<x>{BYTES})` and `(?P<y>{BYTES})`\)"
)
RECORD = re.compile(
    rf"\btable of (?P<total>{DECIMAL})-byte [^.\n]+\s+definitions\.\s*"
    rf"Its (?P<body>{DECIMAL})-byte [^.\n]+ is followed by a (?P<tag>{DECIMAL})-byte"
)
COMMAND = re.compile(r"`(?:python3?\s+)?(?:tools/)?([\w-]+\.py)\s+--check(?:[^`\n]+)?`")


@dataclass(frozen=True)
class Claim:
    line: int
    shown: str
    expected: object
    reader: tuple
    edition: str = ""


def parse_number(text):
    return int(text.replace(",", ""))


def probes(text, measured, config):
    """Find supported citation forms. Each probe records its own source line."""
    def line(offset):
        return text.count("\n", 0, offset) + 1

    def eligible(match):
        return line(match.start()) in measured

    def edition(match):
        prefix = text[text.rfind("\n", 0, match.start()) + 1:match.start()]
        qualifiers = re.findall(r"\b(CD|floppy)\b", prefix)
        return qualifiers[-1] if qualifiers else ""

    found = []
    for regex, kind in ((DIRECT, "bytes_at"), (STRING, "string_at"), (STORES, "string_at")):
        for match in regex.finditer(text):
            if eligible(match):
                value = match["value"]
                expected = bytes.fromhex(value) if kind == "bytes_at" else value
                found.append(Claim(line(match.start("value")), value, expected,
                                   (kind, match["file"], int(match["offset"], 16)), edition(match)))
    for match in SIZE.finditer(text):
        if eligible(match):
            value = match["value"]
            found.append(Claim(line(match.start("value")), value, parse_number(value),
                               ("file_size", match["file"])))
    for match in PAIR_SIZE.finditer(text):
        if eligible(match):
            value = match["value"]
            found.append(Claim(line(match.start("value")), value, parse_number(value),
                               ("loose_size", match["a"], match["b"]), "CD"))
    if config.get("executable"):
        for match in PAIRED.finditer(text):
            if eligible(match):
                for offset, value in (("a", "x"), ("b", "y")):
                    found.append(Claim(line(match.start(offset)), match[offset], bytes.fromhex(match[value]),
                                       ("bytes_at", config["executable"], int(match[offset], 16))))
    for match in RECORD.finditer(text):
        if eligible(match):
            found.append(Claim(line(match.start("body")), match["body"], parse_number(match["body"]),
                               ("arithmetic", parse_number(match["total"]), parse_number(match["tag"]))))
    counts = config.get("counts", {})
    for command in COMMAND.finditer(text):
        if not eligible(command):
            continue
        tail = text[command.end():command.end() + 200].split("\n\n", 1)[0]
        for unit, reader in counts.get(command[1], {}).items():
            match = re.search(rf"(?<![\d,])({DECIMAL})\s+{re.escape(unit)}\b", tail)
            if match:
                found.append(Claim(line(command.end() + match.start()), match[1], parse_number(match[1]),
                                   tuple(reader)))
    return found


def observed(claim, data, read_witness, original_file):
    kind, *parts = claim.reader
    if kind == "arithmetic":
        total, tag = parts
        return total - tag, f"stated record size {total} minus tag size {tag}"
    if data is None:
        return None
    if kind == "file_size":
        name, = parts
        return original_file(data, name).stat().st_size, name
    if kind not in {"bytes_at", "string_at"}:
        return read_witness(data, claim.reader)
    name, offset = parts
    path = original_file(data, name)
    with path.open("rb") as source:
        source.seek(offset)
        if kind == "bytes_at":
            value = source.read(len(claim.expected))
        else:
            raw = source.read(256)
            value = raw.split(b"\0", 1)[0].decode("ascii", errors="backslashreplace")
            if b"\0" not in raw:
                raise ValueError(f"no NUL-terminated string at {name}+{offset:#x}")
    return value, f"{name}+{offset:#x}"
