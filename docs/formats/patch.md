# Lands of Lore patch format

A patch describes small changes to files in your own copy of LoL1, LoL2 or
LoL3. It records the length and SHA-256 of each byte span it replaces and the
new bytes. The game name selects the matching repository's tool.
`tools/patch.py` reads your installation and writes the results to a new path
outside the game and this repository.

## Rules

- Share only your own edits. Keep the original files, exported text tables,
  rebuilt archives, and the undo file private.
- Patches must never remove or bypass copy protection, including disc checks,
  serial checks and manual look-ups. The author is responsible for what a
  program edit does.
- Use a copy of the game to try your changes.
- Native ports and engine work are outside the scope of this project.

## Make, apply and undo

Run the commands from the repository. Put quotes around paths with spaces.
On Windows you can use `py -3` in place of `python3`. Give the game's folder
with `--data` or as the first positional path.

```sh
python3 tools/patch.py make --data "GAME" "CHANGED" --title "My edit" --out "../my edit.json"
python3 tools/patch.py apply --data "GAME" "../my edit.json" --out "../patched files"
python3 tools/patch.py apply --data "GAME COPY" "../patched files/undo.json" --out "../restored files"
```

1. `make` compares `CHANGED` with your original. Keep the files at their
   original relative paths, as in the output of `modkit.py build`. The tool
   ignores unchanged files and writes `lol-patch-3`. It detects the kind from
   the changed files. You can give `--kind` explicitly.
2. `apply` reads the expected old span from your copy and checks its SHA-256.
   It refuses a mismatch before writing an output folder. For a program
   patch it also verifies the whole-file SHA-256. It checks that applying
   the undo restores the original bytes exactly.
3. Copy the patched files, with their folders, into your game copy. Keep
   `undo.json` in the output folder. To reverse the edit, apply that undo
   file to the patched copy and then copy the restored files back.
   **`undo.json` holds original game bytes from your copy. Do not share it.**

The reader accepts previously downloaded `lol-patch-2` files and validates
their stored old bytes against your copy. Keep those files private when
they carry original game bytes. Their undo is generated locally.
The undo file has format `lol-patch-undo-1`. Its `new` field holds the
bytes being restored and its old-span hash checks the current bytes.

The [level editor](../LEVEL_EDITOR.md) can also write a data patch and
private undo file with `--patch`.

## The file

This example uses synthetic data.

```json
{
  "format": "lol-patch-3",
  "game": "lol2",
  "kind": "data",
  "title": "Adjust a test number",
  "description": "Change one value in a synthetic fixture.",
  "changes": [
    {
      "file": "DAT/TEST.MIX",
      "entry": 0,
      "offset": 16,
      "old_length": 1,
      "old_sha256": "e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db",
      "new": "09"
    }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `game` | `lol1`, `lol2` or `lol3` |
| `kind` | `data` or `program`. A program patch has a top-level `sha256` object mapping each file to its full hash before the change. |
| `file` | The path under the game-specific folder below, with the spelling on disk and forward slashes. |
| `entry` | Zero-based archive directory index. Use 0 for a loose file or program. |
| `offset` | Decimal byte offset into the member or loose file before applying this patch. |
| `old_length` | Number of bytes to remove. For insertion it is zero. |
| `old_sha256` | SHA-256 of those bytes as 64 lowercase hexadecimal digits. For insertion it is the SHA-256 of the empty string. |
| `new` | Replacement bytes as lowercase hexadecimal pairs. For deletion it is empty. |

At least one unchanged byte must separate two spans in one member.
`make` trims equal bytes from both ends of a difference and considers
repeated byte runs when matching resized members. Version 3 refuses a
span with unchanged prefix or suffix bytes or a run of eight or more
bytes common to the old and new values. Keep such unchanged bytes
outside the patch. For a data patch the format reader must rebuild the
edited member in both directions. A program change keeps the file
length and the `MZ` signature.

## Size limits

| | Bytes per change, each side | Bytes per patch, each side | Changes per patch |
| --- | --- | --- | --- |
| Data patch | 256 | 4,096 | 1,024 |
| Program patch | 16 | 256 | 1,024 |

The replaced span is counted by its length. The new span is counted by
its decoded byte count. `make` compares resized members up to 65,536 bytes.

## LoL1

The [level editor](../LEVEL_EDITOR.md) writes the same format with `--patch`.
Data patches accept PAKs at any depth below the data folder and loose
`.ENG`, `.FRE`, `.GER`, `.TIM`, `.INI` and `.INF` files. The patch
checks that each changed member matches a supported reader and writer.
For `.CMZ` members, the tool checks that only the four decoded wall bytes
per square change. It also preserves the palette, header fields other
than the derived stored size, and extra bytes outside those wall fields.
The original CMZ loaders at CD `MAIN.EXE+0x48540` and floppy `+0x51C10`
read the four wall bytes. [CMZ layout](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/cmz.md)

**File names** start at the folder holding the PAK archives: the CD's
`DATA` folder, or the floppy game folder. If you give the folder above
`DATA`, the tool uses `DATA`. An output folder inside the installation
folder around `DATA` is refused as well.

**Program files** are `HARDRIVE/MAIN.EXE` and `HARDRIVE/MAINW.EXE` below
the CD's `DATA` folder, or `MAIN.EXE` in the floppy game folder. The CD
also stores copies inside `WESTWOOD.001` at `+0x28C46` and `+0x7FE8A`;
the tool does not patch those.
[Executable locations and offsets](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/executable_tables.md#locating-the-executables)

**CONFIRMED.** The original DOS program under DOSBox uses the game files
and the program image it runs.

**CONFIRMED.** A data patch can also affect ScummVM when it recognizes the
release and reads the same resource. For example, its startup loads
`GENERAL.PAK`, runs `ONETIME.INF` and loads `ITEM.INF`. Its level loader
also reads `LEVELn.INI` and `LEVELn.INF` (`engines/kyra/engine/lol.cpp:591–594,857–858`,
`engines/kyra/engine/scene_lol.cpp:64–79`).

**CONFIRMED.** Program patches have no effect in ScummVM. Its metaengine
constructs `LoLEngine`, and that engine loads its static tables from its
own `KYRA.DAT` (`engines/kyra/metaengine.cpp:274–275`,
`engines/kyra/resource/resource.h:1252`,
`engines/kyra/resource/staticres.cpp:138–162`). This covers the character
defaults, character modifiers, equipment display layout, spell properties
including MP and HP costs, experience thresholds, monster difficulty
modifiers, and the CD item price thresholds
(`engines/kyra/resource/staticres_lol.cpp:254–286`,
`engines/kyra/gui/gui_lol.cpp:870–877`).
[Original table offsets and ScummVM providers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/executable_tables.md#static-executable-tables)

### ScummVM detection

**CONFIRMED.** ScummVM revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`
uses the MD5 of up to the first 1 MiB of each listed file and compares an
exact size on entries that specify one. Changes to the hashed bytes or
a required size can affect recognition (`engines/kyra/detection.cpp:55–60`,
`engines/advancedDetector.cpp:480–498,653–669,780–812`). `make` and
`apply` print a warning whenever a patch touches a file name from the table.

| Entry | Files used | `engines/kyra/detection_tables.h` |
| --- | --- | --- |
| DOS CD | `GENERAL.PAK`, `L01.PAK` | 1349–1420, 1466–1610 |
| DOS floppy | `WESTWOOD.1` for compressed editions, `GENERAL.PAK` and `CHAPTER7.PAK` for extracted editions | 1637–1689, 1702–1843 |
| Other supported releases | `LEVEL01.FRE` and `LEVEL02.FRE` for the Spanish CD fan translation, `GENERAL.PAK` with `CHAPTER7.PAK`, `MUS.PAK` or `TMUS.PAK` for Japanese editions | 1623–1624, 1828–1829, 1856–1857, 1870–1871 |
| Demos and diagnostic entries | `INTRO.PAK`, `INTROVOC.PAK`, `GENERAL.PAK`, `L01.PAK`, `VOC.PAK`, `GAME.DAT`. The diagnostic rows require sizes for one `GENERAL.PAK` and for the `VOC.PAK` and `GAME.DAT` pair. | 1435, 1451–1452, 1884–1940 |

[Measured CD and floppy detection bytes](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/edition_comparison.md#edition--build-difference)

## LoL2

**File names** start at the game folder holding `LOLG.DAT` and `DAT`. If
you give the `DAT` folder, the tool uses the folder above it. `GLOBAL.MIX`
ships twice, byte for byte the same: `GLOBAL.MIX` in the game folder and
`DAT/GLOBAL.MIX`. A patch names the one you changed. Which of the two the
game opens has not been shown (**UNCONFIRMED**), so change both in the
same way.

**Program files** are `LOLG.EXE` and `LOLG.DAT` in the game folder.
`LOLG.EXE+0x438` names `LOLG.DAT`. Most gameplay offsets in these pages
belong to that second image, whose embedded LE header starts at file
`+0x3BCB4`. Convert analysis addresses to file offsets before making a
patch.

**CONFIRMED.** The target is the original DOS game under DOSBox. Data
patches change files read by the DOS program, including MIX archives and
loose TRR tables.
[MIX and TRR readers](../ROUND_TRIP.md) ·
[Executable addresses](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-executable-tables.md)

## LoL3

**File names** start at the game folder holding `LOL3.DAT` and `DAT`. If
you give the `DAT` folder, the tool uses the folder above it. Some
archives ship both in `DAT` and beside it; a patch names the one you
changed. Compare the copies when a table ships more than once.

**Program files** are `LOL3.EXE` (the launcher) and `LOL3.DAT` (the
gameplay image) in the game folder. Their PE headers begin at file
offsets `+0xE0` and `+0xC8`. Use the section table of the chosen image to
convert a virtual address to a file offset.

**CONFIRMED.** The target is the original Windows game. Data patches
change the resources read by it, including WSX archives and TRR tables.
[WSX and TRR readers](../ROUND_TRIP.md) ·
[Executable layouts](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/executable.md) ·
[Launcher and gameplay image](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NEEDS_A_RUNNING_GAME.md)
