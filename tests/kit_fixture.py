"""Make a tiny synthetic PAK installation with editable LoL1 records."""
import struct

from tests.test_level_editor import chunk
from tests.test_modkit import make_game
from tests.test_save_edit import source_slot
from decode_dialogue import encode_string
from lol1lib import pak_entries
from level_edit import add_item, push
from lol1_level_writer import write_walls
from lol1_pak_writer import write_pak
from lol1_script_writer import write_strings

DATA = "DATA"
LEVEL = "1"
ARCHIVE = "L01.PAK"
JOBS = ("level", "text", "translate", "music", "save", "patch", "mod")
TRANSLATE_FROM = "The test key"
SAVE_FIELD = "money"
SAVE_AT = 0x254 + 528


def script(*words):
    body = b"EMC2" + chunk(b"ORDR", [0xFFFF, 0]) + chunk(b"DATA", [0xFFFF, 0x8002, *words, 0x4801])
    return b"FORM" + struct.pack(">I", len(body) + 8) + body


def call(function, *args):
    return [word for value in reversed(args) for word in push(value)] + [0x4E00 | function, 0x4C00 | len(args)]


def make_fixture(game):
    data = game / DATA
    data.mkdir(parents=True)
    make_game(data)
    # The first archive also supplies English text. Add the remaining members below.
    original = (data / ARCHIVE).read_bytes()
    text_members = [(name, original[at:at + size]) for name, at, size in pak_entries(original)]
    stored = encode_string(TRANSLATE_FROM.encode("cp437")).decode("latin-1")
    land = write_strings({"offsets": [2], "strings": [stored, ""]}, "<")
    (data / "GENERAL.PAK").write_bytes(write_pak([
        ("LANDS.ENG", land), ("TEST.XMI", b"EVNT" + struct.pack(">I", 3) + bytes.fromhex("ff2f0000")), ("ONETIME.INF", script(*call(0x0E, 121, 0x4000, *([0] * 8)))),
    ]))
    grid = bytearray(struct.pack("<3H", 32, 32, 5) + bytes(5120))
    grid[6 + 5 * 51:10 + 5 * 51] = bytes((3, 0, 3, 0))
    maze = struct.pack("<HBBIH", len(grid) + 8, 0, 0, len(grid), 0) + grid
    walls = write_walls((0, [(0, 0, 0, 0, 0, 0), (3, 1, 0, 0, 0x28, 0), (4, 1, 0, 0, 0x18, 0)]))
    # --check exercises the entire numbered range. All maps are the same made-up grid.
    for level in range(1, 30):
        stem = f"LEVEL{level}"
        members = [
            (stem + ".CMZ", maze),
            (stem + ".WLL", walls),
            (stem + ".INI", script(*add_item(level, 121, 69), *add_item(level, 121, 70),
                                   *call(0x38, 30, 16, 16, 0, 1, 0, 0, 0))),
            (stem + ".INF", script()),
        ]
        (data / f"L{level:02d}.PAK").write_bytes(write_pak(members + (text_members if level == 1 else [])))
    return source_slot()


def inspect_jobs(test):
    test.assertIn(TRANSLATE_FROM, test.job("text", "--data", test.data, "LANDS.ENG", "--index", "0"))
    out = test.root / "midi files"
    test.assertIn("end-of-track: True", test.job("music", "--data", test.data, "TEST.XMI", "--out", out))
    test.assertEqual((out / "TEST_00.mid").read_bytes()[:4], b"MThd")
