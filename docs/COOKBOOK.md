# Cookbook

Each recipe uses the tools on your own copy of the original game. Run them from the clone after:

```bash
export LOL1_DATA=/path/to/your/LOL1/DATA
```

Pictures and written sheets go outside the clone. The examples use `../lol1-out`. A save is a game-written player save (a file the game wrote when you saved), not a file in `DATA`.

## Write a full report

```bash
python3 tools/full_report.py --data "$LOL1_DATA" --out ../lol1-out/report
```

The tool writes `inventory.tsv` with the files in `DATA`, their sizes, the reader used and its result. For an archive, `complete` describes its directory and payload spans. Open `levels/README.md` for the level sheets. `text-counts.tsv` gives one count per table from the language tables inside PAK archives.

Choose an output folder outside the game and clone. Use a fresh folder for each report.

## Draw a level schematic

```bash
mkdir -p ../lol1-out
python3 tools/level_renderer.py --level level01 --schematic --out ../lol1-out/schematic
```

```text
Wrote schematic for level01 to ../lol1-out/schematic/level01_schematic.png.
```

The picture is a top-down drawing of level 1: light floors, dark walls, orange squares with partial walls, doors or switches, red marks on decorated walls. No game pixels.

## Find where an item is placed

```bash
python3 tools/level_report.py --level 2
```

The sheet starts:

```text
# Level 2

Made by `tools/level_report.py` from `LEVEL2.CMZ`, `.WLL`, `.XXX`, `.INI`, `.INF` (CD edition). How to read it: [README](README.md). Formats: [cmz](../formats/cmz.md), [wll](../formats/wll.md), [emc2](../formats/emc2.md), [xxx](../formats/xxx.md).
```

Further down, the placement table begins:

```text
## Items placed by the scripts

| Script entry | Item type | Name | Level | Block |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 121 | Stick | 2 | 69 |
```

Later rows are the same shape. One of them places item 43, Weathered dagger, on block 136.

## List a level's creatures

```bash
python3 tools/level_report.py --level 1
```

The sheet starts `# Level 1` and the same "Made by" line with `LEVEL1`. The creature table begins:

```text
## Monsters placed by the scripts

| Script entry | Block | Facing | Type slot | Mode |
|---|---|---|---|---|
| INI entry 1 (runs when the level loads) | 589 | 0 | 1 | 1 |
```

Level 1 has four rows in that table.

## Read your position from a save

```bash
python3 tools/save_reader.py /path/to/your/_SAVE000.DAT
```

On one CD save the first line was:

```text
original save, CD: "<your save name>"; ends at 82559 as the layout predicts: True
```

A character line follows. The position line after it was:

```text
level 1, block 557 (x 13, y 17), facing 0, money 41, 3 game flags set, levels stored [1], 10 items in use
```

## See what a switch does

```bash
python3 tools/level_report.py --level 7
```

The sheet starts `# Level 7`. One wall-click row is:

```text
| block 261 (x 5, y 8) | `0x084A` | wall clicked | operates the door switch at block 293 with action 0 |
```

## See what a cut-scene script does

```bash
python3 tools/parse_tim.py --list AUTOMAP.TIM
```

```text
AUTOMAP.TIM in O00A.PAK
AUTOMAP.TIM: AVTL 143 words, 1 function(s) at word(s) [1], TEXT 7 bytes, in-game table
word  fn len delay opcode command parameters
   1   0   3     0 0x0118 cmd_return(1)
   4   0   9     0 0x0102 cmd_initWSA index=0 string_id=0 "BOOK" x=288 y=32 offscreen=0 flags=40
```

The listing has 29 instructions in all; it ends `29 instructions, walk stops before the end of AVTL: 0`.

## Convert a music file to MIDI

```bash
python3 tools/xmi_to_midi.py LORE01A.XMI
```

Nothing is written. The first lines are:

```text
LORE01A #00: 0 notes, 0 controller, 0 program, 4 meta, 0 sysex events; 0.0 s; end-of-track: True
LORE01A #01: 0 notes, 0 controller, 0 program, 4 meta, 0 sysex events; 0.0 s; end-of-track: True
LORE01A #02: 8 notes, 8 controller, 3 program, 7 meta, 0 sysex events; 35.7 s; end-of-track: True
```

Add `--out ../lol1-out/midi` to write one `.mid` per sequence. The same lines are printed, then `wrote` and the folder.

## Read one line of game text

```bash
python3 tools/decode_dialogue.py LEVEL01.ENG --index 0
```

```text
[0] Welcome to Gladstone Keep. …
```

## Change text or numbers with the mod kit

The [mod kit](../tools/README.md#modkitpy) writes the game's text tables and script listings as files you can edit, and builds changed archives into a new folder. The game folder is only read.

```bash
python3 tools/modkit.py unpack "/path/to/LoL1/DATA" "my mod work"
```

Open the file in `my mod work/edits/` whose name ends in `_L01.PAK_LEVEL01.ENG.json` (the number in front may differ on your copy) in a text editor and change `Welcome to Gladstone Keep.` to `Welcome to Gladstone Castle.` inside `"value"`. Then build and verify:

```bash
python3 tools/modkit.py build "/path/to/LoL1/DATA" "my mod work" "my mod output"
python3 tools/modkit.py verify "/path/to/LoL1/DATA" "my mod work" "my mod output"
```

Each command ends with one summary line; build and verify print `62 archives or loose tables, 1 changed (L01.PAK)`. Copy `L01.PAK` from the output folder over a backup copy of your game to try it.

## Change one thing safely

This example copies an English CD installation. It changes only the high
byte of the first wall type's automap word, at `LEVEL1.WLL+0x0D` inside
`L01.PAK` (CD archive `+0x109D0`). The [WLL format](formats/wll.md) shows
this field and the original loader's low-byte read. **CONFIRMED** for that
installation.

The result is a modified copy for your own tests, not the original game.
This repository ships no game files and no changed files. The script only
reads your installation and writes only inside the new folder, so your
original stays untouched. Keep the changed copy to yourself and do not
share modified game files.

From this repository's root, set `source` to your game folder containing
`DATA`. Set `out` to a new directory outside both the repository and the
original installation. The script refuses any other output folder and
needs room for a full copy.

```bash
source="/path/to/LoL1"
out="/path/to/my-lol1-copy"
PYTHONPATH=tools python3 - "$source" "$out" <<'PY'
from pathlib import Path
import shutil
import sys

from cli_errors import output_refusal
from lol1_level_writer import parse_walls, write_walls
from lol1_pak_writer import write_pak
from lol1lib import pak_entries

source, out = (Path(arg).resolve() for arg in sys.argv[1:])
refusal = output_refusal(out, source, repository=True)
if refusal:
    raise SystemExit(refusal)
archive = Path("DATA/L01.PAK")
original = (source / archive).read_bytes()
members = [(name, original[start:start + size])
           for name, start, size in pak_entries(original)]
index, = (i for i, (name, _) in enumerate(members) if name == "LEVEL1.WLL")
name, member = members[index]
area, rows = parse_walls(member)
row = rows[0]
if row[0] != 0 or row[-1] != 0x003F:
    raise SystemExit("this is not the expected first wall row")
rows[0] = row[:-1] + (0x013F,)
members[index] = name, write_walls((area, rows))
rebuilt = write_pak(members)
shutil.copytree(source, out)
(out / archive).write_bytes(rebuilt)
PY
python3 tools/wll_parser.py --data "$out/DATA" --level 1 | sed -n '1,4p'
```

In row 0, the automap column still reads `0x3F`. The last of the four
displayed high bytes is now `01`. The original and copied archive have
the same length, and the single difference is at `L01.PAK+0x109D0`.

## Share a change as a patch

The [README](../README.md#change-a-number-in-your-own-copy) walks through the whole route on your own copy: unpack, change one number, build, make a patch, apply it to a copy, read it back and undo it. The [patch format](formats/patch.md) page gives every rule and limit.

- `make` compares the game folder (`--data`) with a folder of changed files. The output folder of `modkit.py build` works as it is, and so does a copy of the game folder in which only some files changed.
- File names in the patch start at the folder holding the PAK archives (the CD's `DATA` folder, or the floppy game folder). A patch made from the folder above `DATA` names the same files, and a patch made from either applies to both.
- `apply` writes nothing until every check has passed: each replaced span's SHA-256, the whole-file SHA-256 for a program patch, and the undo. Keep `undo.json` private because it holds original game bytes.
- Program patches: copy the program file (CD: `HARDRIVE/MAIN.EXE` below `DATA`; floppy: `MAIN.EXE`) into a new folder, at the same path it has in the game folder, change a byte with a hex editor, for example one letter of a message, and run `make` with that folder. The patch records the program's SHA-256 and applies only to that exact file. A program change may replace at most 16 bytes at a time and 256 in all, never changes the file length, and never touches copy-protection code.
- `make` and `apply` warn when a patch changes a file ScummVM uses to recognize the game ([ScummVM detection](formats/patch.md#scummvm-detection)).

## Change a saved game (a copy)

```bash
python3 tools/save_edit.py set "/path/to/your/_SAVE001.DAT" money 5000 --out "my edited save.DAT"
python3 tools/save_reader.py "my edited save.DAT"
```

The first command prints `set: money OLD -> 5000; copy written to ...`, with your save's old value for OLD, then one line saying how far the field is proven. The save itself is only read, and the copy must go outside the game and save folders. Copy it over a save in a **copy** of your game to load it.

| Field | Value | Proven |
| --- | --- | --- |
| `block` | 0–1023; writes the block and its centred X and Y | tested on the CD 1.02 (edited-save run) |
| `facing` | 0–3 | tested on the CD 1.02 |
| `lamp-oil` | 0–100; also sets the lamp effect by the documented oil rule | tested on the CD 1.02 |
| `money` | 0–65535; the same field `save_reader.py` prints as money | not yet tested: no edited copy loaded yet |
| `name` | the slot description, printable ASCII | not yet tested: no edited copy loaded yet |

The editor accepts CD 1.02 slots and floppy `.13` slots with the matching header and size. Not yet tested for any floppy field: no edited floppy save has been loaded by the game, and the floppy offsets differ. For `block`, choose a block you know can be walked on the current level. Numbers can be decimal or start with `0x`.
[Save offsets](savegame_format.md#global-state) ·
[What an edited copy must keep](savegame_format.md#editing-a-copy-of-an-original-slot) ·
[Lamp rule](unknowns/07_native_rules.md#lamp-regeneration-and-the-clock)

Map viewer and editor notes for tool makers: [tool makers](TOOL_MAKERS.md).

## Open an interactive level plan

```sh
python3 tools/level_viewer.py --data "$LOL1_DATA" --level 1 --out "../LoL1 plans"
```

Open `level01.html` in the new folder. Click a square to see its wall types.
Choose **Automap legend** to find symbol and exploration squares. Choose
**Script entries** to see their event masks and DATA words, or **Exits** to
see conditions on the level changes. The placement markers are static
calls read from the scripts. Computed values remain in the list.
Use `--level all` for the 29 levels.
[Automap legend fields](formats/xxx.md) · [Script entries](formats/emc2.md) ·
[Exit conditions](PROGRESSION.md#level-to-level)

## Find a tool by job

Run `python3 tools/lol.py` to see the job names. This example reads one
row of a text table.

```sh
python3 tools/lol.py text --data "$LOL1_DATA" LEVEL01.ENG --index 0
```

Use `python3 tools/lol.py level --help` to see the level viewer's options.
The original tool filenames also work.
