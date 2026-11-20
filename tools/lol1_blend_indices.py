#!/usr/bin/env python3
"""Check the three-pass LoL1 finale blend lookups against the original files.

On the CD it pins the three localized readers, the source rows and the
modelled destination cells. On the floppy it pins that FINALE.EXE reader and
the four source pictures (the tables are the CD bytes).

  python3 tools/lol1_blend_indices.py --data DATA --check
  python3 tools/lol1_blend_indices.py --data DATA --indices

Reports palette-index ranges. Screens, fonts and animations are read in memory.
"""
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from cli_errors import run_cli, game_path
from fnt_reader import parse as font
import lol1lib as L
from parse_tim import tim_chunks, tim_text, walk_avtl
from wsa_extract import frames, parse as animation

WIDTH, HEIGHT = 320, 200
LOCALES = {
    "ENG": (0x1D7B0, 0x1E6AC, 0x9EB8, 0x14CAA, 0xAC2A, 0xADE6),
    "FRE": (0x1D780, 0x1EDAE, 0x9E82, 0x14C74, 0xABF4, 0xADB0),
    "GER": (0x1D780, 0x1EE08, 0x9E82, 0x14C74, 0xABF4, 0xADB0),
}
# Page-segment word table, and the two allocator stores that give an even page
# and the next odd page one segment (so page 5, where the picture is decoded,
# is the page-4 source buffer).
PAGE_PAIRS = {
    "ENG": (0x22AB, 0x1AE8C, 0x1AF16),
    "FRE": (0x29DD, 0x1AE56, 0x1AEE0),
    "GER": (0x2A37, 0x1AE56, 0x1AEE0),
}
# Floppy FINALE.EXE: the same handler at another address. Data segment, slot
# table, dispatcher, page-pointer routine, draw, lookup, handler, caller.
FLOPPY = (0x225F0, 0x261BE, 0xB193, 0x13EB1, 0xA529, 0xA6DB, 0x7BF1, 0x7D94, 0x4639, 0x1448E, 0x14518)
FLOPPY_PAIRS = (
    (387, "RETURN", "BLEND.TAB"),
    (853, "RICHARDF", "BLEND.TAB"),
    (1649, "FACE", "BLEND2.TAB"),
    (1799, "TAPPING", "BLEND2.TAB"),
)
FLOPPY_TIM_SHA = "4fba56be55d24a23e6cc65647cd68df4c9078d5e6c91679fad84ab691aa93be0"
TABLE_SHA = {
    "BLEND.TAB": "f709c1f4f765bd123cf4e0311b4b3f9e013c349e02e48a3602e00e87cb0bcc07",
    "BLEND2.TAB": "ff3043ebbc274a5ae80aaeafb3a15a8a4aa1155aa0ed248ad3e914e8b7749e85",
}
# Rows (source colours) each table can be indexed with, over all four calls.
SOURCE_ROWS = {"BLEND.TAB": (199, 0xEF), "BLEND2.TAB": (190, 0xEF)}
LOOKUP = "66ad66268b158af88ac232db65d7aa8afc8ac665d7aa66c1c81066c1ca108af88ac265d7aa8afc8ac665d7aa"
PAIRS = (
    (382, "RETURN", "BLEND.TAB"),
    (848, "RICHARDF", "BLEND.TAB"),
    (1818, "FACE", "BLEND2.TAB"),
    (1968, "TAPPING", "BLEND2.TAB"),
)
TIM_SHA = "a5786dd42879801d63129e8b1599fe6a2cb97be9ed8e1e91d5bb2bf78c22786e"
EXPECTED = {
    "BLEND.TAB": (7696, "af6532c592400931a329710082929435add542b806d8bf20defbb4f71fc0aa1f"),
    "BLEND2.TAB": (7876, "7f6babb543b16135d22ea4cd81729dabdacc9f7dcb7994e6aaa59a4a1ed095ce"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def far_target(image, operand):
    offset, segment = unpack_from("<2H", image, operand)
    return 16 * (unpack_from("<H", image, 8)[0] + segment) + offset


def check_program(image, locale):
    ds, table, dispatch, page_pointer, draw, lookup = LOCALES[locale]
    require(image[dispatch:dispatch + 2] == b"\xff\x9f"
            and ds + unpack_from("<H", image, dispatch + 2)[0] == table
            and far_target(image, table + 5 * 4) == 0x7AD5,
            f"{locale} nested slot 5")
    for at, want in (
        (0x7B0B, "b80400509a"), (0x7B1B, "b80200509a"),
        (0x7B9E, "b8010033d25052"), (0x7BBB, "b802005033c050b8c80050b828005033c05033c05033c05033c0509a"),
        (0x7C22, "b8050050b8070050"),
        (0x7C4A, "ff76eeff76ec168d86dcfe50b8020050b8c80050b840015033c05033c050168d46f85033c05033c050168d46f050"),
        (0x7CB1, "837eea037c87"), (0x7CCE, "b80400509a"),
        (page_pointer + 3, "8b4e0683e10f8bd983e3fed1e3"),
        (lookup, LOOKUP), (lookup - 10, "0fb55ef8"),
        (page_pointer - 0x1A + 3, "8b4e0683e10f8bd983cb01d1e3"),
    ):
        expected = bytes.fromhex(want)
        require(image[at:at + len(expected)] == expected, f"{locale} instruction +0x{at:X}")
    require(far_target(image, 0x7B10) == far_target(image, 0x7B20) == page_pointer
            and image[0x7C78] == 0x9A and far_target(image, 0x7C79) == draw
            and image[0x7C9B:0x7CA0] == image[0x7CD2:0x7CD7],
            f"{locale} page and draw calls")
    for operand in (0x7AE3, 0x7AF5):
        at = ds + unpack_from("<H", image, operand)[0]
        require(unpack_from("<4H", image, at) == (WIDTH, HEIGHT, 0, 0),
                f"{locale} blend rectangle +0x{at:X}")
    at = ds + unpack_from("<H", image, 0x7C06)[0]
    require(image[at:at + 5] == b".CPS\0", f"{locale} picture suffix")
    check_page_pair(image, *PAGE_PAIRS[locale], page_pointer, locale)


def check_page_pair(image, words, first, second, page_pointer, label):
    """Both page routines read one word table; the allocator fills both words of a pair."""
    word = words.to_bytes(2, "little")
    after = (words + 2).to_bytes(2, "little")
    require(image[page_pointer + 16:page_pointer + 20] == b"\x8b\x97" + word
            and image[page_pointer - 0x1A + 16:page_pointer - 0x1A + 20] == b"\x8b\x97" + word
            and image[first:first + 22] == bytes.fromhex("8bded1e38b46fa8987") + after
            + bytes.fromhex("8bded1e38b46fa8987") + word
            and image[second:second + 20] == bytes.fromhex("8997") + after + bytes.fromhex("8bded1e38b87")
            + after + bytes.fromhex("8bded1e38987") + word,
            f"{label} pages 4 and 5 share one buffer")


def check_floppy_program(image):
    ds, table, dispatch, page_pointer, draw, lookup, handler, caller, words, first, second = FLOPPY
    require(image[dispatch:dispatch + 2] == b"\xff\x9f"
            and ds + unpack_from("<H", image, dispatch + 2)[0] == table
            and far_target(image, table + 5 * 4) == handler,
            "floppy nested slot 5")
    for at, want in (
        (handler + 0x36, "b80400509a"), (handler + 0x46, "b80200509a"),
        (handler + 0xC9, "b8010033d25052"), (handler + 0x14D, "b8050050b8070050"),
        (handler + 0x1DC, "837eea037c87"), (handler + 0x1F9, "b80400509a"),
        (page_pointer + 3, "8b4e0683e10f8bd983e3fed1e3"),
        (lookup, LOOKUP), (lookup - 10, "0fb55ef8"),
        (page_pointer - 0x1A + 3, "8b4e0683e10f8bd983cb01d1e3"),
    ):
        expected = bytes.fromhex(want)
        require(image[at:at + len(expected)] == expected, f"floppy instruction +0x{at:X}")
    require(far_target(image, handler + 0x3B) == far_target(image, handler + 0x4B) == page_pointer
            and image[caller] == 0x9A and far_target(image, caller + 1) == draw
            and image[handler + 0x1C6:handler + 0x1CB] == image[handler + 0x1FD:handler + 0x202],
            "floppy page and draw calls")
    for at in (ds + 0xFE, ds + 0x106):
        require(unpack_from("<4H", image, at) == (WIDTH, HEIGHT, 0, 0), f"floppy blend rectangle +0x{at:X}")
    require(image[ds + 0x15A:ds + 0x15F] == b".CPS\0", "floppy picture suffix")
    check_page_pair(image, words, first, second, page_pointer, "floppy")


def floppy_sources(root):
    """Floppy edition: the same reader and tables; check the four sources only."""
    check_floppy_program(game_path(root, "FINALE.EXE").read_bytes())
    assets = L.read_pak(game_path(root, "FINALE1.PAK"))
    raw = L.read_pak(game_path(root, "FINALE2.PAK"))["LOLFINAL.TIM"]
    require(sha256(raw).hexdigest() == FLOPPY_TIM_SHA, "floppy LOLFINAL.TIM differs from the checked schedule")
    require(call_rows(raw) == FLOPPY_PAIRS, "floppy LOLFINAL.TIM blend calls differ")
    rows = {name: set() for name in TABLE_SHA}
    for _, stem, name in FLOPPY_PAIRS:
        table = game_path(root, name).read_bytes()
        require(sha256(table).hexdigest() == TABLE_SHA[name], f"floppy {name} differs from the CD table")
        source = bitmap(assets, stem)
        require(max(source) < 255, f"floppy {stem} uses source 255")
        rows[name].update(source)
    return source_rows(rows)


def source_rows(rows):
    found = {name: (len(colours), max(colours)) for name, colours in rows.items()}
    require(found == SOURCE_ROWS, "source colour rows differ")
    return found


def invocation_rows(raw):
    require(sha256(raw).hexdigest() == TIM_SHA, "LOLFINAL.TIM differs from the checked scene schedule")
    seen = call_rows(raw)
    require(seen == PAIRS, "LOLFINAL.TIM blend calls differ")
    return seen


def call_rows(raw):
    """(AVTL word, picture, table) of every nested slot-5 instruction."""
    chunks = tim_chunks(raw)
    avtl = chunks["AVTL"]
    rows, stops = walk_avtl(unpack_from(f"<{len(avtl) // 2}H", avtl))
    require(not stops, "LOLFINAL.TIM command walk stopped early")
    return tuple((at, tim_text(chunks["TEXT"], args[1]), tim_text(chunks["TEXT"], args[2]))
                 for _, at, _, _, op, args in rows if op == 0x119 and args[0] == 5)


def bitmap(assets, stem):
    _, _, pixels = L.load_bitmap(assets[stem + ".CPS"])
    require(len(pixels) == WIDTH * HEIGHT, f"{stem} does not fill the blit rectangle")
    return pixels


def apply_delta(scene, assets, stem, frame, x=0, y=0):
    """Apply a missing-first-frame WSA's cumulative XOR to the retained page."""
    data = assets[stem + ".WSA"]
    info = animation(data)
    w, h = info["width"], info["height"]
    x += info["x_add"]
    y += info["y_add"]
    require(not info["has_first_frame"] and 0 <= frame < info["frames"]
            and 0 <= x <= WIDTH - w and 0 <= y <= HEIGHT - h, f"{stem} delta extent")
    for n, pixels, ok in frames(data, info):
        require(ok, f"{stem} frame {n} has an incomplete delta")
        if n == frame:
            break
    result = bytearray(scene)
    for row in range(h):
        start = WIDTH * (y + row) + x
        result[start:start + w] = bytes(a ^ b for a, b in zip(scene[start:start + w], pixels[row*w:(row + 1)*w]))
    return bytes(result)


def death_caption(scene, assets):
    """Place caption 1 at x=y=0 with INTRO.FNT's native nibble-to-index map."""
    dip = assets["LOLFINAL.DIP"]
    start = unpack_from("<H", dip, 2)[0]
    caption = dip[start:dip.index(0, start)]
    font_data = assets["INTRO.FNT"]
    head, glyphs = font(font_data)
    lines = caption.split(b"\r")
    picture = bytearray(scene)
    for i, line in enumerate(lines):
        x, y = 0, i * (head["height"] - 4)
        require(y + head["height"] <= HEIGHT, "DEATH lines exceed picture height")
        for letter in line:
            glyph = glyphs[letter]
            width, rows, top, at = (glyph[k] for k in ("width", "rows", "top", "offset"))
            stride = (width + 1) // 2
            require(x + width <= WIDTH and top + rows <= head["height"], "DEATH glyph outside picture")
            if at:
                for row in range(rows):
                    for col in range(width):
                        value = font_data[at + row * stride + col // 2]
                        nibble = (value >> (4 * (col % 2))) & 15
                        require(nibble in (0, 1, 5, 6), "DEATH glyph uses another colour")
                        if nibble == 1:
                            picture[(y + top + row)*WIDTH + x + col] = 0xF2
            x += width
    return bytes(picture)


def observed_indices(source, destination, table):
    """Reapply the same source pixel while each lookup replaces its destination."""
    draws = []
    for _ in range(3):
        addresses = [(high << 8) | low for high, low in zip(source, destination)]
        draws.append(set(addresses))
        destination = bytes(table[index] for index in addresses)
    return draws


def scene_inputs(assets, script_assets, locale):
    death = bitmap(assets, "DEATH")
    deaths = [death_caption(death, script_assets)]
    if locale == "ENG":
        deaths.append(death)
    return_scene = bitmap(assets, "RETURN")
    return1 = apply_delta(return_scene, assets, "RETURN1", 63, 136, 84)
    # RETURN2's 0..2 frames occupy a disjoint rectangle. The stop command
    # prevents further changes but the stopped frame can depend on scheduling.
    return {
        "RETURN": [apply_delta(scene, assets, "DEATH", 56) for scene in deaths],
        "RICHARDF": [apply_delta(return1, assets, "RETURN2", i, 48, 32) for i in range(3)],
        "FACE": [bitmap(assets, "EYE")],
        "TAPPING": [apply_delta(bitmap(assets, "FACE"), assets, "BLINK", 11)],
    }


def runs(indices):
    """Printable inclusive hex ranges for an index set."""
    starts, ends = [], []
    for value in sorted(set(indices)):
        if ends and value == ends[-1] + 1:
            ends[-1] = value
        else:
            starts.append(value)
            ends.append(value)
    return " ".join(f"{a:02X}" if a == b else f"{a:02X}-{b:02X}" for a, b in zip(starts, ends))


def inspect(root, list_indices):
    table_unions = {name: set() for _, _, name in PAIRS}
    rows = {name: set() for _, _, name in PAIRS}
    scene_unions = {stem: [set() for _ in range(3)] for _, stem, _ in PAIRS}
    scene_common = {stem: None for _, stem, _ in PAIRS}
    for locale in LOCALES:
        folder = game_path(root, locale)
        check_program(game_path(folder, "FINALE.EXE").read_bytes(), locale)
        assets = L.read_pak(game_path(folder, "FINALE1.PAK"))
        script = L.read_pak(game_path(folder, "FINALE2.PAK"))
        destinations = scene_inputs(assets, script, locale)
        for _, stem, name in invocation_rows(script["LOLFINAL.TIM"]):
            source = bitmap(assets, stem)
            table = game_path(folder, name).read_bytes()
            require(len(table) == 0x10000 and max(source) < 255, f"{locale} {stem} blend extent or source 255")
            require(sha256(table).hexdigest() == TABLE_SHA[name], f"{locale} {name} differs")
            rows[name].update(source)
            for destination in destinations[stem]:
                phases = observed_indices(source, destination, table)
                used = set.union(*phases)
                if scene_common[stem] is None:
                    scene_common[stem] = used
                else:
                    scene_common[stem].intersection_update(used)
                table_unions[name].update(used)
                for phase, indices in zip(scene_unions[stem], phases):
                    phase.update(indices)
    source_rows(rows)
    if list_indices:
        for stem, phases in scene_unions.items():
            all_phases = set.union(*phases)
            print(f"{stem}: {len(all_phases)} indices, {len(scene_common[stem])} common to every input")
            print(f"  source {runs(i >> 8 for i in all_phases)}")
            for n, phase in enumerate(phases, 1):
                print(f"  pass {n}: {len(phase)} indices; destination {runs(i & 255 for i in phase)}")
        for name, indices in table_unions.items():
            print(f"{name} candidate indices: {runs(indices)}")
    return {name: (len(indices), sha256(bytes(i in indices for i in range(0x10000))).hexdigest())
            for name, indices in table_unions.items()}


def main():
    parser = L.tool_args(__doc__, writes=False)
    parser.add_argument("--indices", action="store_true", help="list candidate row, column and index ranges")
    args = parser.parse_args()
    root = Path(args.data)
    if not L.is_cd_layout(root):
        found = floppy_sources(root)
        print("CHECK finale blend: floppy FINALE.EXE, 4 calls; source rows "
              f"{', '.join(f'{name} {count} (highest {top:02X})' for name, (count, top) in found.items())}; "
              "no source 255; destinations are modelled on the CD only")
        return 0
    actual = inspect(root, args.indices)
    if args.check:
        require(actual == EXPECTED, "finale blend index census differs")
    print(f"CHECK finale blend: 3 languages, 4 calls, 3 passes each; source rows "
          f"{', '.join(f'{name} {count}' for name, (count, _) in SOURCE_ROWS.items())} (highest EF); "
          f"modelled cells {', '.join(f'{name} {count}' for name, (count, _) in actual.items())}; no source 255")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
