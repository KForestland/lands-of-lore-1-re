# Edit a level on its plan

Open a level from your own LoL1 installation. You can change walls and door states, place items, and edit existing monster placements. The browser downloads a small change file. The Python tool applies it to copied archives in a new folder and reads the result back.

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
3. A square with a recognized pair of opposite door faces has a **Stored door state** menu. Pick **Open** or **Closed**. Both faces in that square change together. In Level 1, click a square to see its number and whether the door menu is available.
4. Choose a **Monster placement**. Set the square and its X/Y coordinates (0–255), facing and type. **Use selected square** fills in the square from the plan. Click **Stage monster edit** to see the moved marker, then export. Type names come from the level's loaded shape-file names. A slot can name
   more than one shape if the level replaces it. A move into a square whose
   four faces draw wall graphics is refused.
5. Click **Download changes**. Move the downloaded `level02-changes.json` into your current folder, or give its full path in the next command. Use **Clear edits** to restore the preview to the original layout before exporting.

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

The tool reports how many archives, square edits and placement edits it verified. The folder holds the affected PAK archive copies. Every other member in those archives reads back unchanged. An empty edit file produces byte-identical copies. With `--patch` and edits, the folder also holds `level-patch.json` and `undo.json`. The shared format limits the size of each replaced span and its replacement. A limit error names the archive entry and its relative offset when relevant. If it refuses a large change, apply without `--patch` for a local copy or export smaller sets of edits. [Patch size limits](formats/patch.md#size-limits)

Share `level-patch.json` with someone who has the matching edition. They apply it to a fresh folder. To reverse a patch, use the patched output as the data source, its `undo.json` as the patch, and a fresh output folder. Keep backup copies if you later install an edited archive. [Apply and undo commands](formats/patch.md#make-apply-and-undo)

## What the editor changes

- **CONFIRMED.** CMZ stores north, east, south and west at decoded offset `6 + square × stride`. The editor preserves the five extra bytes per level 24 square and only changes the chosen wall bytes. The names in the menus are descriptions from the actual WLL row fields, not filenames or labels stored in those rows. CD `MAIN.EXE+0x48540`, `+0x48764` and `+0x47350–0x47421`. [CMZ](formats/cmz.md) · [WLL](formats/wll.md)
- **CONFIRMED.** An editable item comes from a call to `0x11` in entry 1 of a level's INI, with eight literal arguments and the original stack cleanup. For example, in `L02.PAK+0x10D77` or floppy `CHAPTER1.PAK+0x61C63`, `LEVEL2.INI` DATA word `0x19C` creates item type 121 on square 69. A move changes the square argument and keeps the seven others. A removal skips creation and sets the return value to zero, leaving the argument cleanup. An addition runs before the original return, with local X/Y 128 and height 0, a centred ground placement patterned on the literal calls in `LEVEL4.INI` at `L04.PAK+0xBB2A`. The editor restores the original return value after its additions. Branch and entry addresses are updated when the number of words changes. CD `MAIN.EXE+0x137DC`, floppy `+0x1819F`, and the native instruction runner at CD `+0x12F20–0x133A1`. [EMC2 instruction and function tables](emc2_scripts.md)
- **CONFIRMED.** The native door routine chooses an axis from WLL bit `0x08`, walks the consecutive wall IDs to an end-state flag and writes the same wall ID to opposite faces of that block. The editor pairs consecutive, visually matching frames marked `0x28` at the closed end and `0x18` at the open end, using only the state and side bits. CD `MAIN.EXE+0x17A80–0x17AC3, +0x17B0A–0x17B43` and `L01.PAK+0x109E9` witness the state logic and first wall group. [Native wall behavior](unknowns/07_native_rules.md#wll-flags-and-special-types)
- **CONFIRMED.** Calls to `0x38` place monsters. The editor changes only the five literal pushes nearest the call, for square, X/Y, facing and property type. The other arguments and cleanup stay in place, including computed flags, mode and equipment. For example, CD `LEVEL2.INI` in `L02.PAK+0x10D77` has a call at DATA word `0x187`. The native placement reader is at CD `MAIN.EXE+0x14619` and floppy `+0x18FB1`. The labels join property call `0x3F` argument 1 to shape slot `0x0B` argument 1
  and read the shape filename from the INI TEXT directory. In level 2, the
  INI loads `BOAR.SHP` into shape slot 0 and property slot 2 selects it. The
  CD handlers are `MAIN.EXE+0x47830` and `+0x4761D`. [Script functions](emc2_scripts.md)
- **CONFIRMED static check.** `level_edit.py --data "/path/to/LoL1" --check` wrote unchanged copies for all 29 levels in each edition and re-read an edited copy of each level. It also verified patch creation and byte-identical undo. The call filter found 197 editable placements in each edition. On CD 1.02, one prepared copy of `L02.PAK` moves the Stick from square 69 to 138. The reader verifies that placement and undo reproduces the original archive. **UNCONFIRMED in the running game.** A fresh visit to level 2 on that copy can check the moved item from arrival square 106. Use a save from before the first visit, so the game reads the edited archive for the level. On 21 November a fresh CD 1.02 copy with that archive, and an untouched copy, were each stood at the level-1 gate that leads to level 2; forward steps and clicks on the gate left the party in the keep, level 2 was not entered, and the moved item was not seen (launch folders 0063, 0064 and 0065).

## Keep placement in the original game

Both DOSBox comparisons started a new game in CD 1.02. From the throne, one click on the curved turn arrow faced the arch without taking a step. The edited copies used a same-length `L01.PAK` patch that moved a guard’s Halberd onto square 558. Applying the undo restored the archive byte for byte.

- **CONFIRMED in the running game.** Launch 0104 showed an empty floor. Launch 0105 used the edited archive (`513c19ce`). The Halberd appeared on the floor and stayed there after the click.
- **CONFIRMED in the running game.** The screenshots from launch 0108 showed the empty floor again. Launch 0109 used the nearer placement (`b0ab3383`). Its native save before the click shows the party facing east on square 557 and item 7, the Halberd, on square 558. The save after the click puts item 7 in the cursor hand. The party stayed on square 557.
- **CONFIRMED.** The CD floor-pick routine adds the absolute X and Y differences (`MAIN.EXE+0xC0FF`) and skips ground items at distances of 320 units or more (`MAIN.EXE+0x3F0C7`). From the party’s position, the first edit placed the Halberd 384 units away. The second edit put it 256 units away.

## Outside this version

| What | What an editor would need |
|---|---|
| Other monster edits | Adding or removing monsters and changing computation, equipment, flags or mode would need control-flow and runtime slot checks. Calls without five consecutive literal pushes stay read-only. CD `MAIN.EXE+0x14619`, floppy `+0x18FB1`. [Creature records](unknowns/18_native_records.md) |
| General scripts | A control-flow and event editor that understands the computed operands and entry headers. This version only edits the literal, same-level INI placements. Item calls in INF, calls through other entry points, and computed calls stay in the reader view. The VM starts entries through ORDR and runs the 19-opcode interpreter, CD `MAIN.EXE+0x12F20–0x133A1`. [EMC2](formats/emc2.md) |
| Scripted doors | The door state menu edits the two stored faces in a square. Switch scripts, links between squares, restored save states and the door animation setup need separate support. CD `MAIN.EXE+0x17871` and the special-wall table at `+0x342FC` show the switch path. [Wall behavior](unknowns/07_native_rules.md#wll-flags-and-special-types) |
| Automap legend | A legend editor needs separate symbol and exploration squares, a valid shape number and a text ID in the selected language. These are the six words of each 12-byte XXX record, read at `engines/kyra/engine/lol.cpp:4250–4280`. [XXX](formats/xxx.md) |
