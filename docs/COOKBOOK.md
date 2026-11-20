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
python3 tools/level_renderer.py --level 1 --schematic --out ../lol1-out
```

```text
wrote ../lol1-out/level01_schematic.png
```

The picture is a top-down drawing of level 1: light floors, dark walls, orange doors and switches, red marks on decorated walls. No game pixels.

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

Open `my mod work/edits/0000_L01.PAK_LEVEL01.ENG.json` in a text editor and change `Welcome to Gladstone Keep.` to `Welcome to Gladstone Castle.` inside `"value"`. Then build and verify:

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
