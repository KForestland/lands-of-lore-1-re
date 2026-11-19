#!/usr/bin/env python3
"""Re-prove the extra TIM argument words as formatter operands.

Nested 0x07 and 0x0D push the operand pointer and a start index. The
formatter reads operand[index] once per %n, %s or %d. Nested 0x03 pushes
three words and does not pass the pointer.

  lol1_tim_words.py --data DATA --check
"""
import os
import struct

import decode_dialogue as D
import lol1lib as L

GIVE = 0x983F
CHAT = 0x99C6
TALK_PUSH = 0x9B08
GIVE_BODY = bytes.fromhex("558bec56c45e0626ff770426ff770226ff379a2d01bc0783c406")
CHAT_HEAD = bytes.fromhex("558bec6a0366ff7606")
TALK_HEAD = bytes.fromhex("6a0166ff7606")
FORWARD3 = bytes.fromhex("ff761866ff761466ff761066ff760c6a03900ee8")
FORWARD4 = bytes.fromhex("ff761866ff761466ff761066ff760c6a04900ee8")
TO_FMT = bytes.fromhex("ff761466ff761066ff760c66ff76080ee8")
READ_N = bytes.fromhex("8bc6d1e0c45e0e03d8268b07")
READ_S = bytes.fromhex("8bc646d1e0c45e0e03d826ff37")
NAME_ADD = bytes.fromhex("69c08200052f36")

# (pak, member, string index, pak file offset of the string, conversion letters)
CD_STRINGS = (
    ("L01.PAK", "LEVEL01.ENG", 0x08, 0x65FE, "n"),
    ("L02.PAK", "LEVEL02.ENG", 0x3E, 0xC338, "n"),
    ("L02.PAK", "LEVEL02.ENG", 0x43, 0xC415, "n"),
    ("L02.PAK", "LEVEL02.ENG", 0x4C, 0xC5CF, "n"),
    ("L02.PAK", "LEVEL02.ENG", 0x4E, 0xC63A, ""),
    ("L02.PAK", "LEVEL02.ENG", 0x50, 0xC688, ""),
    ("L02.PAK", "LEVEL02.ENG", 0x51, 0xC6D8, ""),
    ("L04.PAK", "LEVEL04.ENG", 0x02, 0x9178, "n"),
    ("L07.PAK", "LEVEL07.ENG", 0x11, 0x5F5B, "n"),
    ("L07.PAK", "LEVEL07.ENG", 0x0E, 0x5ECD, ""),
    ("L07.PAK", "LEVEL07.ENG", 0x0F, 0x5ED7, ""),
    ("L07.PAK", "LEVEL07.ENG", 0x12, 0x5F76, ""),
)
EXTRA_AT = {
    ("O01E.PAK", 0xA89), ("O01A.PAK", 0x8DE4),
    ("O07A.PAK", 0x5475), ("O04A.PAK", 0x27B8),
    ("O01E.PAK", 0x94D), ("O07A.PAK", 0x528F), ("O07A.PAK", 0x5375), ("O07A.PAK", 0x54AB),
    ("O02B.PAK", 0xC955), ("O02B.PAK", 0xCB7F), ("O02B.PAK", 0xD455),
    ("O02B.PAK", 0xD585), ("O02B.PAK", 0xD67F), ("O02B.PAK", 0xD863),
}
FL_CHAT = 0x9B8D
FL_TALK = 0x9C64
FL_GIVE = 0x9A0A
FL_GIVE_BODY = bytes.fromhex("558bec56c45e0626ff770426ff770226ff37")
FL_SI = 0x1B6BF
FL_READ_N = 0x1B7F5
FL_READ_S = 0x1B841
FL_READ_D = 0x1B8E6
FL_STRINGS = (
    ("CHAPTER1.PAK", "LEVEL03.ENG", 0x28, 0x56C74, "d"),
    ("CHAPTER1.PAK", "LEVEL03.ENG", 0x2A, 0x56C96, "d"),
    ("CHAPTER1.PAK", "LEVEL03.ENG", 0x2B, 0x56CB2, "d"),
    ("CHAPTER1.PAK", "LEVEL03.ENG", 0x2C, 0x56CCF, "d"),
)
FL_NONZERO = {
    ("CHAPTER1.PAK", "BUCK03.TIM", 20),
    ("CHAPTER1.PAK", "BUCK04.TIM", 10),
    ("CHAPTER1.PAK", "BUCK05.TIM", 10),
    ("CHAPTER1.PAK", "BUCK14.TIM", 100),
}


def fail(message):
    print(f"CHECK tim_words FAILED: {message}")
    return 1


def avtl_words(blob):
    if blob[:4] != b"FORM":
        return None
    pos = 12
    end = min(8 + struct.unpack_from(">I", blob, 4)[0], len(blob))
    while pos + 8 <= end:
        cid = blob[pos:pos + 4]
        size = struct.unpack_from(">I", blob, pos + 4)[0]
        if cid == b"AVTL":
            data = blob[pos + 8:pos + 8 + size]
            return pos + 8, [struct.unpack_from("<H", data, i * 2)[0] for i in range(len(data) // 2)]
        pos += 8 + size + (size & 1)
    return None


def nfuncs(words):
    for count in range(1, 11):
        if count <= len(words) and min(words[:count]) == count:
            return count
    return 1


def in_game(rel):
    parts = rel.upper().split(os.sep)
    return not any(part.startswith(("STARTUP", "FINALE", "INTRO")) for part in parts)


def extra_sites(data_dir):
    """Yield (archive, member, extra-word file offset, nested, nargs, extra)."""
    for name in sorted(os.listdir(data_dir)):
        if not name.upper().endswith(".PAK"):
            continue
        raw = open(os.path.join(data_dir, name), "rb").read()
        try:
            entries = L.pak_entries(raw)
        except (OSError, ValueError, struct.error):
            continue
        for member, offset, size in entries:
            if not member.upper().endswith(".TIM"):
                continue
            got = avtl_words(raw[offset:offset + size])
            if not got:
                continue
            base, words = got
            seen = set()
            for entry in range(nfuncs(words)):
                ip = words[entry]
                guard = 0
                while 0 <= ip < len(words) - 2 and ip not in seen and guard < 10000:
                    seen.add(ip)
                    guard += 1
                    length = words[ip]
                    if length < 3 or ip + length > len(words):
                        break
                    params = words[ip + 3:ip + length]
                    if (words[ip + 2] & 0xFF) == 0x19 and params:
                        nested = params[0] & 0xFF
                        if nested in (0x03, 0x07, 0x0D):
                            word = ip + 2 + len(params)
                            yield (name, member, offset + base + word * 2, nested, len(params) - 1,
                                   params[-1] if len(params) > 1 else None)
                    ip += length


def conversions(text):
    return "".join(text[i + 1] for i in range(len(text) - 1) if text[i] == "%")


def string_at(data_dir, pak, member, index):
    raw = open(os.path.join(data_dir, pak), "rb").read()
    for name, offset, size in L.pak_entries(raw):
        if name.upper() != member:
            continue
        blob = raw[offset:offset + size]
        count = struct.unpack_from("<H", blob, 0)[0] // 2
        offs = struct.unpack_from(f"<{count}H", blob, 0)
        raw_s = blob[offs[index]:blob.index(b"\0", offs[index])]
        return offset + offs[index], conversions(D.decode_raw(raw_s))
    raise ValueError(f"{member} is not in {pak}")


def check_strings(data_dir, rows):
    for pak, member, index, at, letters in rows:
        got_at, got = string_at(data_dir, pak, member, index)
        if got_at != at or got != letters:
            return f"{pak} {member}[{index:#x}] is {got_at:#x} %{got}, not {at:#x} %{letters}"
    return None


def check_cd(data_dir):
    exe_path = os.path.join(data_dir, "HARDRIVE", "MAIN.EXE")
    try:
        exe = open(exe_path, "rb").read()
    except OSError as exc:
        return fail(str(exc))
    if len(exe) != 356928 or struct.unpack_from("<H", exe, 8)[0] * 16 != 0x3800:
        return fail(f"MAIN.EXE is {len(exe)} bytes")
    if exe[0x9630:0x9636] != bytes.fromhex("8b4606050200"):
        return fail("the 0x19 handler does not skip the nested selector at 0x9630")
    if exe[GIVE:GIVE + len(GIVE_BODY)] != GIVE_BODY:
        return fail("giveItem does not push three words and drop them")
    if exe[CHAT:CHAT + len(CHAT_HEAD)] != CHAT_HEAD or exe[TALK_PUSH:TALK_PUSH + len(TALK_HEAD)] != TALK_HEAD:
        return fail("characterChat or talk does not push the start index and the operand pointer")
    if exe[0x16DBC:0x16DBC + len(FORWARD3)] != FORWARD3 or exe[0x16E02:0x16E02 + len(FORWARD4)] != FORWARD4:
        return fail("0x16C6D does not forward the operand pointer and the start index")
    if exe[0x173FC:0x173FC + len(TO_FMT)] != TO_FMT or exe[0x17066:0x17069] != bytes.fromhex("8b7612"):
        return fail("the formatter does not take the start index in SI")
    if exe[0x1719C:0x1719C + len(READ_N)] != READ_N or exe[0x171E8:0x171E8 + len(READ_S)] != READ_S:
        return fail("the %n or %s handler does not read operand[SI]")
    if exe[0x1728D:0x1728D + len(READ_N)] != READ_N or exe[0x171A8:0x171A8 + len(NAME_ADD)] != NAME_ADD:
        return fail("the %d read or the %n name address is not the pinned bytes")
    if exe[0xC35E:0xC363] != bytes.fromhex("8bc225ff3f") or exe[0x24C34:0x24C38] != bytes.fromhex("8bc6d1e0"):
        return fail("the text helper does not mask the id and double it")
    counts = {(0x03, 4): 0, (0x07, 3): 0, (0x07, 4): 0, (0x0D, 1): 0, (0x0D, 2): 0}
    extras = []
    for archive, member, at, nested, nargs, extra in extra_sites(data_dir):
        if not in_game(archive):
            continue
        key = (nested, nargs)
        if key not in counts:
            return fail(f"unexpected {archive} {member} nested {nested:#x} has {nargs} words")
        counts[key] += 1
        if (nested == 0x03 and nargs == 4) or (nested == 0x07 and nargs == 4) or (nested == 0x0D and nargs == 2):
            if extra != 0:
                return fail(f"{archive}+{at:#x} extra word is {extra:#x}")
            extras.append((archive.upper(), at))
    expect = {(0x03, 4): 2, (0x07, 3): 23, (0x07, 4): 2, (0x0D, 1): 67, (0x0D, 2): 10}
    if counts != expect or set(extras) != EXTRA_AT:
        return fail(f"call counts {counts} sites {sorted(extras)}")
    bad = check_strings(data_dir, CD_STRINGS)
    if bad:
        return fail(bad)
    pak = open(os.path.join(data_dir, "O02B.PAK"), "rb").read()
    if pak[0xCEE1:0xCEE1 + 10] != bytes.fromhex("05000000190102000000"):
        return fail("O02B.PAK+0xCEE1 is not the 19/02 instruction whose argument is 0 at +0xCEE9")
    print("CHECK tim_words: 14 CD extra words are 0; 0x07 and 0x0D pass the operand pointer and a start index; "
          "6 level strings have one %n and 6 have none; giveItem pushes three words")
    return 0


def check_floppy(data_dir):
    exe = open(os.path.join(data_dir, "MAIN.EXE"), "rb").read()
    if len(exe) != 373872 or struct.unpack_from("<H", exe, 8)[0] * 16 != 18432:
        return fail(f"floppy MAIN.EXE is {len(exe)} bytes")
    fl_talk = bytes.fromhex("558bec6a0166ff7606")
    if exe[FL_CHAT:FL_CHAT + len(CHAT_HEAD)] != CHAT_HEAD or exe[FL_TALK:FL_TALK + len(fl_talk)] != fl_talk:
        return fail("floppy 0x07 or 0x0D does not push the start index and the operand pointer")
    if exe[FL_GIVE:FL_GIVE + len(FL_GIVE_BODY)] != FL_GIVE_BODY or exe[FL_GIVE + 23:FL_GIVE + 26] != bytes.fromhex("83c406"):
        return fail("floppy giveItem does not push three words and drop them")
    if exe[FL_SI:FL_SI + 3] != bytes.fromhex("8b7612"):
        return fail("floppy formatter does not load SI from the start index")
    if exe[FL_READ_N:FL_READ_N + len(READ_N)] != READ_N or exe[FL_READ_S:FL_READ_S + len(READ_S)] != READ_S:
        return fail("floppy %n or %s does not read operand[SI]")
    if exe[FL_READ_D:FL_READ_D + len(READ_N)] != READ_N:
        return fail("floppy %d does not read operand[SI]")
    nonzero = []
    for archive, member, _at, nested, nargs, extra in extra_sites(data_dir):
        if extra in (None, 0):
            continue
        if not ((nested == 0x0D and nargs == 2) or (nested == 0x07 and nargs == 4) or (nested == 0x03 and nargs == 4)):
            continue
        nonzero.append((archive.upper(), member.upper(), extra))
    if set(nonzero) != FL_NONZERO or len(nonzero) != 4:
        return fail(f"floppy nonzero extra words {sorted(nonzero)}")
    bad = check_strings(data_dir, FL_STRINGS)
    if bad:
        return fail(bad)
    pak = open(os.path.join(data_dir, "CHAPTER1.PAK"), "rb").read()
    if pak[0xE7548:0xE7548 + 10] != bytes.fromhex("05000000190102000000"):
        return fail("CHAPTER1.PAK+0xE7548 is not the 19/02 instruction whose argument is 0 at +0xE7550")
    print("CHECK tim_words: floppy 0x07 and 0x0D push the operand pointer and a start index; "
          "BUCK03/04/05/14 pass 20/10/10/100 into one %d each")
    return 0


def main():
    parser = L.tool_args(__doc__)
    args = parser.parse_args()
    if not args.check:
        parser.error("this tool only checks; pass --check")
    if L.is_cd_layout(args.data):
        return check_cd(args.data)
    if not os.path.isfile(os.path.join(args.data, "MAIN.EXE")):
        print("CHECK tim_words: floppy layout, MAIN.EXE is not in this folder")
        return 0
    return check_floppy(args.data)


if __name__ == "__main__":
    raise SystemExit(main())
