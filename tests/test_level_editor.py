"""Editor checks with synthetic levels and script words."""
from collections import Counter
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import emc2_decompile as emc
import level_edit as edit
from lol1_level_writer import update_frame4, validate_maze_edit
from lol1lib import decode_frame4


def chunk(tag, values):
    payload = struct.pack(f">{len(values)}H", *values)
    return struct.pack(">4sI", tag, len(payload)) + payload


def startup():
    words = [0xFFFF, 0x8002, *edit.add_item(2, 121, 69), 0x4801]
    body = b"EMC2" + chunk(b"ORDR", [0xFFFF, 0]) + chunk(b"DATA", words)
    return b"FORM" + struct.pack(">I", len(body) + 8) + body


class LevelEditor(unittest.TestCase):
    def test_added_and_moved_placements_read_back(self):
        old = startup()
        sites, _ = edit.placement_sites(emc.read_script(old), 2)
        site, = sites
        new, expected, changed = edit.changed_script(old, 2, [[site, 412]], [[121, 9]], {121: "Example"})
        script = emc.read_script(new)
        self.assertEqual(changed, 2)
        self.assertEqual(script.instructions[0].target, 2)
        found = Counter(place.args for place in edit.placement_sites(script, 2)[0].values())
        self.assertEqual(found, expected)
        self.assertEqual({args[4] for args in found}, {9, 412})
        removed, expected, changed = edit.changed_script(old, 2, [[site, None]], [], {})
        self.assertEqual(edit.placement_sites(emc.read_script(removed), 2)[0], {})
        self.assertEqual((expected, changed), (Counter(), 1))

    def test_recompression_handles_overlapping_copies(self):
        packets = [("literal", b"abc"), ("relative", 9, 3), ("end",)]
        expected = b"xbcabcabcabc"
        rebuilt = update_frame4(packets, expected)
        self.assertEqual(decode_frame4(rebuilt, len(expected)), expected)

    def test_maze_patch_rejects_non_wall_bytes(self):
        grid = struct.pack("<3H", 32, 32, 5) + b"\0" * 5120
        header = struct.pack("<HBBIH", len(grid) + 8, 0, 0, len(grid), 0)
        original = header + grid
        world = bytearray(original)
        world[16] = 1
        validate_maze_edit(original, world)
        world[20] = 1
        with self.assertRaisesRegex(ValueError, "four wall types"):
            validate_maze_edit(original, world)
