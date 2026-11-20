# Edit a level on its plan

Open a level from your own LoL1 installation. You can change the four walls of a square and move, remove or add an item. The browser downloads a small change file. The Python tool applies it to copied archives in a new folder and reads the result back.

## Open level 2

Follow the [first ten minutes](FIRST_TEN_MINUTES.md) through the Python and Pillow setup. Run the command from the downloaded tools folder. Replace the example path with your LoL1 install folder or the folder holding `GENERAL.PAK`.

Linux

```sh
.venv/bin/python tools/lol.py level --data "/path/to/LoL1" --level level02 --out "../level plans"
xdg-open "../level plans/level02.html"
```

Windows PowerShell

```powershell
.\.venv\Scripts\python.exe tools/lol.py level --data "C:\Games\LoL1" --level level02 --out "..\level plans"
Start-Process "..\level plans\level02.html"
```

Use a fresh output folder name for each run.

1. Click **Edit level**. Click a square on the plan or type its number in **Square**. The four menus list the wall types defined for this level and describe how each is drawn or used. Changing one face leaves the adjacent square's own sides as they were.
2. Under **Placed item**, pick an item. Choose its destination square and click **Move to square**, or click **Remove item**. To add another, use **Item type to add** and **Add to square**. Level 2 has editable items in its initial placement list. Other script placements stay visible as read-only markers. Moving an item keeps its original X/Y and height within the square. When moving an item out of a niche, choose a compatible niche or remove it and add a floor placement.
3. Click **Download changes**. Move the downloaded `level02-changes.json` into your current folder, or give its full path in the next command. Use **Clear edits** to restore the preview to the original layout before exporting.

## Save a copy and share the edits

Use a new output folder whose parent already exists. Add `--patch` to include a shareable patch and its undo.

Linux

```sh
.venv/bin/python tools/level_edit.py --data "/path/to/LoL1" "level02-changes.json" --out "../edited level" --patch
```

Windows PowerShell

```powershell
.\.venv\Scripts\python.exe tools/level_edit.py --data "C:\Games\LoL1" "level02-changes.json" --out "..\edited level" --patch
```

The tool reports how many archives, square edits and item edits it verified. The folder holds the affected PAK archive copies. Every other member in those archives reads back unchanged. An empty edit file produces byte-identical copies. With `--patch` and edits, the folder also holds `level-patch.json` and `undo.json`. The shared format limits how many old and new bytes a patch can carry. A limit error names the archive entry and its relative offset when relevant. If it refuses a large change, apply without `--patch` for a local copy or export smaller sets of edits. [Patch size limits](formats/patch.md#size-limits)

Share `level-patch.json` with someone who has the matching edition. They apply it to a fresh folder. To reverse a patch, use the patched output as the data source, its `undo.json` as the patch, and a fresh output folder. Keep backup copies if you later install an edited archive. [Apply and undo commands](formats/patch.md#make-apply-and-undo)

## What the editor changes

- **CONFIRMED.** CMZ stores north, east, south and west at decoded offset `6 + square × stride`. The editor preserves the five extra bytes per level 24 square and only changes the chosen wall bytes. The names in the menus are descriptions from the actual WLL row fields, not filenames or labels stored in those rows. CD `MAIN.EXE+0x48540`, `+0x48764` and `+0x47350–0x47421`. [CMZ](formats/cmz.md) · [WLL](formats/wll.md)
- **CONFIRMED.** An editable item comes from a call to `0x11` in entry 1 of a level's INI, with eight literal arguments and the original stack cleanup. For example, in `L02.PAK+0x10D77` or floppy `CHAPTER1.PAK+0x61C63`, `LEVEL2.INI` DATA word `0x19C` creates item type 121 on square 69. A move changes the square argument and keeps the seven others. A removal skips creation and sets the return value to zero, leaving the argument cleanup. An addition runs before the original return, with local X/Y 128 and height 0, a centred ground placement patterned on the literal calls in `LEVEL4.INI` at `L04.PAK+0xBB2A`. The editor restores the original return value after its additions. Branch and entry addresses are updated when the number of words changes. CD `MAIN.EXE+0x137DC`, floppy `+0x1819F`, and the native instruction runner at CD `+0x12F20–0x133A1`. [EMC2 instruction and function tables](emc2_scripts.md)
- **CONFIRMED static check.** `level_edit.py --data "/path/to/LoL1" --check` wrote unchanged copies for all 29 levels in each edition and re-read an edited copy of each level. It also verified patch creation and byte-identical undo. The call filter found 197 editable placements in each edition. **UNCONFIRMED in the running game.** The first edition-specific play test would load a fresh level 2 into a copy with the archive replaced, then check the changed wall and all three item operations.

## Outside this version

| What | What an editor would need |
|---|---|
| Monsters | A separate placement editor for creature slots, position, facing and mode, with checks against the level's loaded creature definitions and equipment. These are the initializer and arguments of call `0x38`, CD handler `MAIN.EXE+0x14619`, floppy `+0x18FB1`. [Creature records](unknowns/18_native_records.md) |
| General scripts | A control-flow and event editor that understands the computed operands and entry headers. This version only edits the literal, same-level INI placements. Item calls in INF, calls through other entry points, and computed calls stay in the reader view. The VM starts entries through ORDR and runs the 19-opcode interpreter, CD `MAIN.EXE+0x12F20–0x133A1`. [EMC2](formats/emc2.md) |
| Scripted doors | Editing a wall type sets its stored face number. It leaves switch events, conditions, linked faces and the door animation setup alone. A door editor needs to check those links and both open and shut states. CD `MAIN.EXE+0x17871` and the special-wall table at `+0x342FC` show the switch path. [Wall behavior](unknowns/07_native_rules.md#wll-flags-and-special-types) |
| Automap legend | A legend editor needs separate symbol and exploration squares, a valid shape number and a text ID in the selected language. These are the six words of each 12-byte XXX record, read at `engines/kyra/engine/lol.cpp:4250–4280`. [XXX](formats/xxx.md) |
