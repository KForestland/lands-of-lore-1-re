#!/usr/bin/env python3
"""Attack and defense special arms in both MAIN.EXE editions.

Static read of the original programs. No game, no debugger.

  lol1_attack_types.py --check --data DATA
  lol1_attack_types.py --check --data DATA --floppy FLOPPY_DIR

On the CD folder the check reads HARDRIVE/MAIN.EXE. On a floppy folder it
reads MAIN.EXE. Pass --floppy as well to check that edition in the same run.
"""
import struct
from pathlib import Path

from cli_errors import ReaderArgumentParser, run_cli, game_path
import lol1lib as L


ATK_SIG = bytes.fromhex("268a474d98488bd883fb09")
DEF_SIG = bytes.fromhex("268a474f98488bd883fb05")
DICE = bytes.fromhex("666801006400")
CHANCE_CMP = bytes.fromhex("268a474c")
DEF_CHANCE = bytes.fromhex("268a474e")
ROLL_OK = bytes.fromhex("3bd07e")
PANIC_HEAD = bytes.fromhex("558becc45e0626834f1908")
PANIC_STORE = bytes.fromhex("8a460a26884715")
ATK_CALL = bytes.fromhex("575666ff76060e")
DEF_GATE = bytes.fromhex("f7460a0080751656ff760cff760eff760aff76fe53")

# First bytes of each arm, type 1 through 10 and defense 1 through 6.
ATK_PREFIX = [
    bytes.fromhex("6668ff070000"),
    bytes.fromhex("666864000100666880008800"),
    bytes.fromhex("666a20"),
    bytes.fromhex("666a0f"),
    bytes.fromhex("5f5e5dcb"),
    bytes.fromhex("8bde69db8200"),
    bytes.fromhex("5f5e5dcb"),
    bytes.fromhex("569a2000"),
    bytes.fromhex("c45e068b460c2601471d"),
    bytes.fromhex("6668480064006a40"),
]
DEF_PREFIX = [
    bytes.fromhex("8bc6253f003d0200"),
    bytes.fromhex("8bc6253f003d0200"),
    bytes.fromhex("f7c68000740e6a1e"),
    bytes.fromhex("83fe03"),
    bytes.fromhex("f7c68000"),
    bytes.fromhex("8bc62584003d8400"),
]

# File offsets by image size: prologues, panic, code segment base and
# segment number, the overlay directory word for that segment, and the arm
# addresses printed in docs/game_rules.md (types 1 to 10, then 1 to 6).
PLACES = {
    0x57240: {"atk": 0x1198C, "defn": 0x11BEA, "panic": 0x12243,
              "base": 0x10EC0, "seg": 0x0D6C, "ovl": 0x88,
              "mp": bytes.fromhex("2683bf6a3600"),
              "attack": [0x11A1A, 0x11BB4, 0x11A68, 0x11ABD, 0x11BD2,
                         0x11B2F, 0x11BD2, 0x11BCB, 0x119E8, 0x119D5],
              "defense": [0x11CB3, 0x11CB3, 0x11DBA, 0x11C50, 0x11C7B, 0x11C39],
              "atk_call": 0x11E67, "def_call": 0xB1FD},
    0x5B470: {"atk": 0x16428, "defn": 0x165F8, "panic": 0x16BE1,
              "base": 0x15960, "seg": 0x1116, "ovl": 0xC8,
              "mp": bytes.fromhex("2683bf4c3600"),
              "attack": [0x164B6, 0x165C2, 0x164E0, 0x16511, 0x165E0,
                         0x16561, 0x165E0, 0x165D9, 0x16484, 0x16471],
              "defense": [0x166BB, 0x166BB, 0x16773, 0x1665E, 0x16686, 0x16647],
              "atk_call": 0x16820, "def_call": 0xB11F},
}


def fail(message):
    print(f"CHECK attack_types FAILED: {message}")
    return 1


def one_sig(data, sig, label):
    at = data.find(sig)
    if at < 0 or data.find(sig, at + 1) >= 0:
        return None, f"{label} signature is not unique"
    return at, None


def switch(data, sig_at, base, count, epilogue):
    """Bounds test, out-of-range exit and jump table of one type switch."""
    after = sig_at + len(ATK_SIG)
    # jbe +3; jmp near epilogue; shl bx,1; jmp cs:[bx+table]
    if data[after:after + 3] != b"\x76\x03\xE9":
        return None, "the bound test does not skip to a near jump"
    out = after + 5 + struct.unpack_from("<h", data, after + 3)[0]
    if out != epilogue:
        return None, f"an out-of-range type goes to {out:#x}, not the epilogue"
    if data[after + 5:after + 10] != b"\xD1\xE3\x2E\xFF\xA7":
        return None, "the type switch has no jump table"
    table = base + struct.unpack_from("<H", data, after + 10)[0]
    words = struct.unpack_from("<" + "H" * count, data, table)
    return [base + word for word in words], None


def starts(data, targets, prefixes, label):
    if len(targets) != len(prefixes):
        return f"{label} has {len(targets)} arms"
    for index, (target, prefix) in enumerate(zip(targets, prefixes), 1):
        if data[target:target + len(prefix)] != prefix:
            return f"{label} type {index} at {target:#x} does not start with the arm"
    return None


def contains(data, target, needle, span, label):
    if needle not in data[target:target + span]:
        return f"{label} at {target:#x} lacks the expected bytes"
    return None


def near_calls(data, base, target):
    """E8 calls inside the 64 KiB code segment that land on target."""
    hits = []
    for at in range(base, min(len(data), base + 0x10000) - 3):
        if data[at] != 0xE8:
            continue
        rel = struct.unpack_from("<h", data, at + 1)[0]
        if at + 3 + rel == target:
            hits.append(at)
    return hits


def far_refs(data, offset, segments):
    """9A far calls and stored far pointers to offset in any of segments,
    searched over the whole file, overlay bodies included."""
    calls, pointers = [], []
    for seg in segments:
        pointer = struct.pack("<HH", offset, seg)
        at = data.find(pointer)
        while at >= 0:
            (calls if at > 0 and data[at - 1] == 0x9A else pointers).append(at)
            at = data.find(pointer, at + 1)
    return calls, pointers


def check_image(data):
    place = PLACES.get(len(data))
    if place is None:
        return fail(f"MAIN.EXE is {len(data):#x} bytes")
    fbov = data.find(b"FBOV")
    if fbov < 0:
        return fail("FBOV header is absent")
    header = struct.unpack_from("<H", data, 8)[0] * 16
    if header + place["seg"] * 16 != place["base"]:
        return fail("the code segment base does not match the MZ header")
    directory = struct.unpack_from("<I", data, fbov + 8)[0]
    if struct.unpack_from("<H", data, directory + place["ovl"])[0] != place["seg"]:
        return fail("the overlay directory word does not name the code segment")
    atk_at, error = one_sig(data, ATK_SIG, "attack")
    if error:
        return fail(error)
    def_at, error = one_sig(data, DEF_SIG, "defense")
    if error:
        return fail(error)
    if atk_at - 0x32 != place["atk"] or data[place["atk"]:place["atk"] + 3] != b"\x55\x8B\xEC":
        return fail("attack prologue is not the expected address")
    if def_at - 0x38 != place["defn"] or data[place["defn"]:place["defn"] + 3] != b"\x55\x8B\xEC":
        return fail("defense prologue is not the expected address")
    before = data[atk_at - 0x48:atk_at]
    if DICE not in before or CHANCE_CMP not in before or ROLL_OK not in before:
        return fail("the attack roll is not 1d100 against byte +0x4C")
    if DEF_CHANCE not in data[def_at - 0x30:def_at] or ROLL_OK not in data[def_at - 0x20:def_at]:
        return fail("the defense roll is not 1d100 against byte +0x4E")
    atk_end = place["attack"][4]
    if data[atk_end:atk_end + 4] != bytes.fromhex("5f5e5dcb"):
        return fail("the attack epilogue is not pop di, pop si, pop bp, retf")
    def_end = data.find(bytes.fromhex("5f5ec9cb"), def_at)
    attack, error = switch(data, atk_at, place["base"], 10, atk_end)
    if error:
        return fail("attack: " + error)
    defense, error = switch(data, def_at, place["base"], 6, def_end)
    if error:
        return fail("defense: " + error)
    if attack != place["attack"] or defense != place["defense"]:
        return fail("the arm addresses differ from docs/game_rules.md")
    error = starts(data, attack, ATK_PREFIX, "attack")
    if error:
        return fail(error)
    error = starts(data, defense, DEF_PREFIX, "defense")
    if error:
        return fail(error)
    if attack[4] != attack[6]:
        return fail("attack types 5 and 7 are not the epilogue")
    if defense[0] != defense[1]:
        return fail("defense types 1 and 2 do not share a body")
    error = contains(data, attack[5], place["mp"], 0x28, "attack type 6")
    if error:
        return fail(error)
    error = contains(data, attack[8], bytes.fromhex("263b473a"), 0x20, "attack type 9")
    if error:
        return fail(error)
    error = contains(data, defense[0], bytes.fromhex("6668ff070000"), 0x180, "defense removal")
    if error:
        return fail(error)
    error = contains(data, defense[0], bytes.fromhex("26807f4f01"), 0x180, "defense type byte")
    if error:
        return fail(error)
    for needle, label in ((bytes.fromhex("681c40"), "defense text 0x401C"),
                          (bytes.fromhex("681d40"), "defense text 0x401D")):
        error = contains(data, defense[0], needle, 0x180, label)
        if error:
            return fail(error)
    error = contains(data, defense[5], bytes.fromhex("26fe4725"), 0x20, "defense type 6")
    if error:
        return fail(error)
    segments = (place["seg"], place["ovl"])
    callers = near_calls(data, place["base"], place["atk"])
    if callers != [place["atk_call"]] or data[callers[0] - len(ATK_CALL):callers[0]] != ATK_CALL:
        return fail(f"attack near callers {[hex(c) for c in callers]}")
    calls, pointers = far_refs(data, place["atk"] - place["base"], segments)
    if calls or pointers:
        return fail(f"attack far references {[hex(c) for c in calls + pointers]}")
    if near_calls(data, place["base"], place["defn"]):
        return fail("the defense routine has a near caller")
    calls, pointers = far_refs(data, place["defn"] - place["base"], segments)
    if [c - 1 for c in calls] != [place["def_call"]] or pointers:
        return fail(f"defense far references {[hex(c) for c in calls + pointers]}")
    if data[place["def_call"] - len(DEF_GATE):place["def_call"]] != DEF_GATE:
        return fail("the defense call is not behind the attacker bit 0x8000 test")
    panic = place["panic"]
    if data[panic:panic + len(PANIC_HEAD)] != PANIC_HEAD:
        return fail("panic does not set bit 0x08")
    body = data[panic:panic + 0x50]
    if b"\x6A\x09" not in body or PANIC_STORE not in body:
        return fail("panic does not request mode 9 and store its argument")
    print("CHECK attack_types: 10 attack arms and 6 defense arms at the page addresses; "
          "types 5 and 7 and out-of-range types go to the epilogue; one same-segment attack call "
          "and one far defense call, no other reference")
    return 0


def main_exe(data_dir):
    root = Path(data_dir)
    if L.is_cd_layout(data_dir):
        return game_path(root, "HARDRIVE", "MAIN.EXE")
    return game_path(root, "MAIN.EXE")


def check_dir(data_dir):
    path = main_exe(data_dir)
    if not path.is_file():
        return fail("MAIN.EXE is not in the folder")
    return check_image(path.read_bytes())


def main():
    import argparse
    parser = ReaderArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None)
    parser.add_argument("--floppy", help="floppy install folder, checked in addition to --data")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")
    rc = check_dir(args.data)
    if rc:
        return rc
    if args.floppy:
        return check_dir(args.floppy)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
