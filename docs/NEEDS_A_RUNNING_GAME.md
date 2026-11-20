# LoL1 questions to test in the original DOS game

Use a debugger-enabled DOS emulator (the DOSBox debugger or DOSBox-X)
and a disposable copy of your own original CD or floppy installation.
Check the edition by the size of `MAIN.EXE`: 356,928 bytes on the CD,
373,872 on the floppy. Record the edition and sound configuration.

To place a breakpoint, start the game, break into the debugger once it
is running, and list the memory blocks with the DOSBox debugger's
`MCBS` command: the PSP is the segment of the block owned by `MAIN`.
The load segment is PSP + 0x10. For resident code, a file offset `F` is at
`(load segment + (F − H) / 16) : ((F − H) mod 16)`, where the MZ header
size `H` is 0x3800 on the CD and 0x4800 on the floppy. `DS:` values
use the DS the debugger shows when stopped in game code. The
definition watchpoints below already use image-relative
segment:offset values (add the load segment).

Code in the FBOV overlay (CD file offsets from 0x3CC40, floppy from
0x45DA0) is not at a fixed place: after the overlay has loaded, search
conventional memory for its bytes and break at the match (the
procedures below give the pattern where one is needed).

Some probes were also tried on edited saves: copies of a game-written save with a few bytes changed. [Edited saves](EDITED_SAVES.md) lists those runs and what a game-written save would still add.

## Working launch for the English DOS CD

**CONFIRMED.** DOSBox 0.74-3 reached character selection and
level 1, and wrote an 82,559-byte native `_SAVE000.DAT` (written by the game in this run; not shipped, not tracked). The
installed 356,928-byte `MAIN.EXE` matched the copy on the disc at
`DATA/HARDRIVE/MAIN.EXE` (SHA-256 prefix `10a9bdce8e23`).
The resident code at file `+0x2689C` was at linear `0x24ABC`,
giving load segment `01A2` in this run. The wall getter at
`+0x134F0` was also present at its relocated address `0x11710`.
The save starts in level 1 (slot `+0x269` = 1).

1. Use a private display and a writable scratch disk. Mount that
   disk as `C:` and the copied CD root that contains `INSTALL.EXE`
   as `D:` with `mount d <cd-copy> -t cdrom -label LANDSOFLORE`.
2. Run `D:\INSTALL.EXE`, select English and accept source `D:`,
   destination `C:` and the default `\WESTWOOD\LOLCD`. Run
   Setup when the installer offers it. Choose Sound Blaster music,
   answer Yes to digitized samples and save the configuration. The
   setup summary selects Sound Blaster for music, effects and voice.
   The witnessed DOSBox used `core=normal`, `cputype=486_slow`,
   `cycles=fixed 25000`, 30 MiB, and emulated SB16 at port 220,
   IRQ 5, DMA 0 and high DMA 5. Host output was disabled using
   `SDL_AUDIODRIVER=dummy` and `[mixer] nosound=true`.
3. Close the installer notes with Escape. From `C:\WESTWOOD` run
   `LOLCD.BAT`, the installer-generated entry that changes to
   `LOLCD` and invokes `LOLCD.EXE`. The launcher and config file
   names are in `LOLCD.EXE+0x42BE` (`lands.cfg`) and
   `+0x4767` (`MAIN.EXE`). Skip the intro with Escape, select a
   character and confirm. Escape opens the in-play menu and
   **Save this game** writes a native slot in the install folder.

The mounted disc and original setup matter for reproducing this route.
Record the new load segment and DS from the game instance used for
each trace. Starting `MAIN.EXE` by itself does not work: without its one
argument it takes the refusal branch at file `0x51F00` and exits with
status 1 at `0x51F9D`.

Edited-save runs used this launch on a private display with host
audio off. Each run placed one edited copy of a game-written slot as
`_SAVE000.DAT` in its own scratch install, with one game instance at
a time. The original slots were not changed.

### An earlier launch that was refused

**CONFIRMED.** An earlier pass used the DOSBox 0.74-3 debugger,
SVGA S3, 32 MB of memory, a fixed 100000 cycles, and no sound hardware.
Drive C held only the launcher-side files: `MAIN.EXE` (356,928 bytes),
`MAINW.EXE`, `LOLCD.EXE`, `SETUP.EXE` and `LANDS.CFG`. Drive D was a
copy of the disc, mounted as a CD-ROM. The setup was English, with no
musical scores, no sound effects and no digitized sounds. The session
changed to drive C and the typed command was `debug main.exe`, with no
game argument. The debugger loaded `MAIN.EXE`. No later file open was
traced. The program printed the RAM and XMS lines and returned to the
DOS prompt on drive C, before a level loaded.

**CONFIRMED.** That return is the no-argument refusal, not a quit from
play. At `MAIN.EXE+0x51F00` the image compares `SI` with 1 and, when
`SI` is less than or equal to 1, jumps to `+0x51F6A`. That block prints
the two lines and calls the runtime exit wrapper at `+0x3E54` with
status 1 (`+0x51F9D`). The one-shot setter at `+0x5197B` is not on this
path. The registered prep at `+0x2689C` still ran. In this run the load
segment was `01EB` and `DS` was `3018`. `DS:3618` was `0000` and
`DS:361E` was `0000:0000`, so the compare at `+0x2689F` jumped to
`+0x2692E`. The next break was `INT 21h` `AH=4Ch` at `+0x3972`. The working launch above starts the game through `LOLCD.EXE`.

`DATA/ENG/LANDS.EXE` (357,509 bytes) is the intro and character-generation program; it does not contain the `MAIN.EXE` prologues used for breakpoints. After character select it starts `MAIN.EXE` with one argument, and the `MAIN.EXE` breakpoints apply from then on (a new PSP).

## Launch-record rule and the runs of 20 November

Since 20 November 08:41 UTC every game launch must show four things in its record: (a) any debugger port listens on the local machine only, shown in the run log while it is up; (b) one new folder and one set of logs per launch, nothing overwritten; (c) a process listing after each launch; (d) every launch reported, failed ones included, with every live memory edit listed by address and bytes. The runs of 20 November below were made before that rule and did not meet it; their results stay as recorded observations, and no question state rests on them alone. A later run under the rule can confirm or replace them.

- The run for Q7b, Q7c, Q14 and Q10 (mode-11 setter, palettes, finale): (a) not shown, the debugger attached to the emulator process but no listing of open ports was recorded; (b) not met, scripts and a cleanup record were overwritten between sessions; (c) not met, one listing for several sessions; (d) not met, two earlier sessions that ended in defeat were not reported.
- The run for Q7b and Q18 (pose from behind; the level 27 fight): (a) not shown; (b) not met, three game processes in one folder and a probe script rewritten; (c) not met; (d) not met, the three launches were not each reported. Its live memory writes were three placements of monster row 0 (linear `0x2B04F`: `6a 00 80 0a 80 03`; `0x2B05E`: `02`; `0x2B06F`: `00`; `0x2B056`: `80 08 80 03`, `80 09 80 03`, `80 08 80 03`).

## Remaining probes

### Q7a. Can wall bit 0x40 change anything besides the EMC byte test?

Question: [Q7 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** The original corpus has bit 0x40 clear. The level-8
EMC example at CD `L08.PAK+0xCAA8` or floppy
`CHAPTER2.PAK+0x23687` compares the whole flag byte of block 172
face 1 against zero. Its native getter is CD `MAIN.EXE+0x134F0`
or floppy `+0x17EB3`. [Wall-flag evidence](unknowns/07_native_rules.md#follow-up-on-bit-0x40)

**CONFIRMED, level-1 control.** All 52 declared WLL wall IDs
matched their file bytes at `DS:531E + id` after movement and a
wall click, with bit `0x40` clear. The 256-byte read had the same
counts for each value before and after. The available
CD slot begins in level 1, so block 172 in level 8 was out of reach.
[Addresses and original record comparison](unknowns/07_native_rules.md#follow-up-on-bit-0x40)

**UNCONFIRMED.** Whether an additional indirect consumer responds
to this bit. Load level 8, stop at that getter with block 172 and
face 1, and follow the wall ID to its entry at CD `DS:531E + id`
or floppy `DS:87C4 + id`. Make an emulator save state (DOSBox-X) at the query. Set that
one live byte to 0 for the first run and 0x40 for the second. Repeat
the action and record each reader, its mask and its taken branch.
Also walk past and click that face from the same state in both runs.
A changed result only at the whole-byte EMC test is the expected
control. A second changed branch whose input is bit 0x40 identifies
an additional consumer. A match over this one route bounds that
route's behavior. Not reached yet with a native save: the launch works,
but the live-byte contrast needs a level-8 save written by the game
(or level 7 before the pit). An edited copy reached level 8 (below).

**CONFIRMED, edited-save run.** At level 8 block 113 the original
key click read wall ID 2 as `0x07` at `MAIN.EXE+0x13522`. The
bit-`0x40` contrast stays open.
[Byte changes and wall query](unknowns/07_native_rules.md#level-8-wall-click-from-an-edited-copy)

### Q7b. Which animation actually displays when a script selects mode 11?

Question: [Q7 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** In level 23 the monster script (event 0x0800) for block 105 selects
mode 11 through function 0x5B (CD `L23.PAK+0xC2AE`, floppy
`CHAPTER6.PAK+0x6AC2D`). The original CD frame selectors are reached
from `MAIN.EXE+0x3DDEF–0x3DE52`; the floppy range is
`+0x46F35–0x46F98`. Both ranges are in the FBOV overlay: after it
loads, search memory for `55 8B EC 56 8B 76 0A C4 5E 06 26 C4 5F 21`
(the selector entry, the same bytes in both editions) and break there. [Mode comparison](unknowns/07_native_rules.md#follow-up-on-modes-911)

**CONFIRMED, setup result.** The installed executable reaches play
and writes a native level-1 save (`+0x269`). No played level-23
slot was available for this run.
[Mode-selection evidence and next test](unknowns/07_native_rules.md#follow-up-on-modes-911)

**UNCONFIRMED.** Which selector and frame that encounter presents
on screen. Use the [level 23 sheet](levels/level23.md) to locate the
block. Let a monster step onto that block to send event 0x0800 (it runs
for the block a monster enters). Break on
the far call to the script's mode setter at CD `+0x14FC1` or floppy `+0x19948`
(arguments pushed from CD `+0x14FBC` / floppy `+0x19943`).
Then capture the next draw of that same instance, recording the shape
bank, selector, direction offset and pending-damage state. Fixed frame
14 with selector 0 and no overriding direction or damage confirms
that fixed arm reached the screen. Any other frame should be accounted
for by the captured selector or draw flags. A write watch on that
instance's mode byte +0x14 also distinguishes an actual mode-10
transition from a frame picked while mode 11 remains set.

**CONFIRMED, edited-save run.** The position edit reached block 105. Neither active-row sample had a monster on a pose square. The mode-11 frame still needs the original monster event (0x0800). [Byte changes and live placement](unknowns/07_native_rules.md#level-23-pose-squares-from-edited-placements)

**CONFIRMED, edited-save run with a live placement (2026-11-20).**
A copy of `477b08b82ecd` set to level 23, block 110, facing west and
30000 HP (bytes in [the setter on a pose square](unknowns/07_native_rules.md#the-mode-11-setter-on-a-pose-square))
loaded in the original. A debugger write into memory, not the save,
then put monster row 0 on block 105 in mode 2 with the party block as
destination. It walked 105, 106, 107, 106 and back to 105, its mode
byte changing only 15 → 2 at `MAIN.EXE+0x11474/+0x114AC`. On its
return to 105 the far call at CD `+0x14FC1` ran once and the setter
store at `+0x118FA` wrote 11 into row 0. Damage word +0x1B and
subframe +0x13 then read 0.

**UNCONFIRMED.** The mode-11 frame. The type-0 selector ran with
direction argument 0 (the watch stopped after six reads and did not
record the instance). The frame-14 arm (`+0x3DC8A`, the mode-11 entry
of the jump table at `+0x3DCD2`) was never fetched in two later
windows. The party stood five blocks from 105, and no picture shows a
monster there, so the row was probably not drawn; its animation type
was not recorded. Next: the same placement with the party one or two
blocks from 105 and facing it, logging the selector's instance and the
monster's animation type, with a picture of the frame.

**CONFIRMED, edited-save run with a live placement (2026-11-20).**
The same copy moved to block 107 (two blocks from 105, facing west),
with a debugger-placed row on block 106 heading west. The row stepped
onto 105, the setter wrote 11, and the next draw called the type-0
selector with argument 8, subframe 1 and no damage. The argument is a
view offset from the table at `DS:052F` (party facing × monster
facing): 8 means the monster faces away from the party. With a
nonzero argument the selector returns argument + subframe and never
reaches the mode table, so this draw was frame 9, the ordinary
back-view frame (from the code; eight logged mode-2 draws of the row
returned 8 + subframe). The figure in the pictures matches the back view of
`CABAL.SHP`. Event 0x0800 runs for the block a monster enters
(`MAIN.EXE+0x11711–0x11735`), so the pose script runs when a monster
steps onto 105. [Byte changes, selector and view table](unknowns/07_native_rules.md#the-mode-11-row-seen-from-behind)

**UNCONFIRMED.** Fixed frame 14 on screen, which needs view argument 0
(a mode-11 monster facing the party). Next: the same run with a live
write of the row's facing +0x18 to 1 (east) after the mode-11 store,
the party on 107 facing west, a read watch on the frame-14 arm
`+0x3DC8A`, the selector's return and a picture.

Not yet run on a native save; see [Probes not yet run](#probes-not-yet-run).

### Q7c. What writes mode 10 during ordinary play?

**CONFIRMED, new-game guard control.** In English CD level 1,
four hardware watches on instance +0x14 covered the approach to
the original guard event at `L01.PAK+0xD545`. Rows 2 and 3
temporarily changed from 1 to 15 at `MAIN.EXE+0x11474` and
back to 1 at `+0x114AC`. The game-written save has all four
rows in mode 1 after the encounter.
[Watch addresses and native slot rows](unknowns/07_native_rules.md#early-cd-guard-modes-in-a-new-game)

**CONFIRMED, static.** The direct stores to the instance mode byte are the ten CD sites and eight floppy sites on the rules page. None stores the constant 10, and no resolved caller or script value is 10. [Mode-byte stores](unknowns/07_native_rules.md#mode-byte-stores)

**UNCONFIRMED.** That nothing produces mode 10. The static search does not cover a store through a pointer already advanced to +0x14, an indirect call of the setter, or the value a save file brings in. In an encounter that
shows mode 10, watch +0x14 for the first write of 10. On CD, use
`2803:15FA + 46 × slot + 0x14` plus the load segment.
Record the writer, previous mode and object, then observe its
next animation selection. The tested guard encounter used only
modes 1 and 15.

**CONFIRMED, edited-save run with a live placement (2026-11-20).**
The level-23 row of [Q7b](#q7b-which-animation-actually-displays-when-a-script-selects-mode-11)
took only 2, 15 and 11 under the write watch; no 10. A read watch on
the first byte of the one byte store of 10 (CD `+0xF64E`, which
writes party byte +0x78, not a monster) saw no fetch of that store
before the watch was removed after eight other reads, early in the
same walk. Both bound only that stretch of play.

Not yet run on a native save; see [Probes not yet run](#probes-not-yet-run).

### Q17. Are the isolated save bytes touched during play?

There are three on the CD and two on the floppy (its block ends before `0x232`).

Question: [Q17 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** Initialization fills these bytes with zero and save
and load copy them as part of the full global block. The table gives
runtime data-segment and slot-file offsets. [Native global layout](unknowns/17_native_save_fields.md#isolated-bytes)

| Edition | Watch in the live data segment | Check in the native slot |
|---|---|---|
| CD | `7FE4`, `81DF`, `8202` | `0x268`, `0x463`, `0x486` |
| floppy | `B48A`, `B685` | `0x25D`, `0x458` |

**CONFIRMED, CD movement and round trip.** On two original
loads and saves, all three watched bytes were zero. The only
watch hits were DOS reads and writes of the global block.
Moving from block 557 to 526 and then turning at block 526
changed the expected fields in the new slots.
[Watch addresses and native save bytes](unknowns/17_native_save_fields.md#cd-movement-and-save-round-trip)

**CONFIRMED, level-1 lamp-effect reset.** The original CD menu's
store at `MAIN.EXE+0x4DE6C` changed `DS:81DE` from 0 to 0xFF
under GDB hardware watches on a local DOSBox build. Brightness
and oil read zero in the sampled states; only `DS:81DE` had a
value watch. Only the bulk save/load calls accessed the three
isolated bytes in the watched intervals. Both new slots, written
by the game in this run and not shipped, read zero at
`+0x268/+0x463/+0x486`. The second slot was written between
watch sessions, so its values come from the file only. In all
three slots flag word 15 (+0x2EE) has the lamp-available bit
0x0800 clear, so this start offers no active-lamp control.
[Watch and native saves](unknowns/17_native_save_fields.md#cd-level-1-lamp-effect-reset)

**CONFIRMED, level-1 selected-character control.** The guard and
audience route reached block 273. The original overlay at
`MAIN.EXE+0x4C4AA/+0x4C4CB` twice changed the selected byte
0 → 99 → 0 with no access to the three isolated bytes. The native
save from block 272, written by the game in this run and not
shipped, still had one active character. A later entry to block
273 sends the party back to block 272 while flag 39 is clear.
Flag 39 is first set by the level-4 block-73 event
(`L04.PAK+0xB516`), so level 1 alone cannot pass this point.
[Native stores, slot offsets and second-portrait test](unknowns/17_native_save_fields.md#cd-level-1-selected-character-control)

**UNCONFIRMED.** Any byte-specific writer or reader. Start a new
game, arm read and write watches after initialization, change the
active character and lamp state, enter another level, then save,
reload and save again. The known copy path gives equal saved and
live values. A byte-specific access outside that path identifies a
new producer or consumer. A stable zero and only bulk copies give
an unused-byte witness for that play sequence. Keep the watchpoints
active through the resume following the load. Movement, turning and
two load/save cycles are covered above.

**CONFIRMED, edited-save run.** The original lamp handler added 100 oil at `MAIN.EXE+0x1065B`. In a separate copy with two character records, the portrait clicks changed the live selected byte. On an edited level-8 copy with the lamp lit, the oil fell 1 → 0 at `MAIN.EXE+0xF9FF`, and a walk from level 8 to level 7 was watched. None of the isolated bytes was accessed by those actions in the sampled watches, except by the bulk write when saving. Depletion and a level change in a game-written save remain open. [Oil](unknowns/17_native_save_fields.md#level-1-oil-refill-on-an-edited-copy), [portraits](unknowns/17_native_save_fields.md#selecting-between-two-portraits-in-an-edited-copy), [dark lamp](unknowns/17_native_save_fields.md#dark-lamp-depletion-on-an-edited-level-8-copy) and [level change](unknowns/17_native_save_fields.md#level-8-to-level-7-with-the-isolated-bytes-watched)

### Q18. Which monster definition fields does an actual fight use?

Question: [Q18 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** In level 27, definition slot 1 has modifier words
256, 64 and 256, critical byte zero at initialization and final word
155 (CD `L27.PAK+0xACB9`, floppy `CHAPTER8.PAK+0x3C940`).
[Definition and pointer evidence](unknowns/18_native_records.md#additional-native-pointer-tests)

**CONFIRMED, level-1 saved control.** The CD slot the game wrote in the probe run contains
four active slot-1 monster rows, all with mode 1. The current level
byte at `+0x269` is 1. No played level-27 slot was available.
[Native row offsets and next test](unknowns/18_native_records.md#level-one-saved-control)

**UNCONFIRMED.** Reads of the three modifier words and final word
through a copied pointer, and any live write to the critical byte.
After the level-27 setter, add the program load segment to the
following segment numbers and attach data watchpoints.

| Edition | Modifier words | Critical byte | Final word |
|---|---|---|---|
| CD | `2803:1BBD/1BBF/1BC1` | `2803:1BEE` | `2803:1BF1` |
| floppy | `2DCF:1B9F/1BA1/1BA3` | `2DCF:1BD0` | `2DCF:1BD3` |

Let a slot-1 monster move, perform a normal attack, take a hit and
use a ranged attack. Check the adjacent +0x0A read as a positive
control. The known critical read computes `100 − value` (CD
`MAIN.EXE+0xAD82–0xAD8F`, floppy `+0xACC3–0xACD0`). A
nonzero write after setup identifies the producer. A word read with
its downstream calculation identifies that word's role. A trace
containing only the known critical and control reads bounds the
result to the actions taken.

**CONFIRMED, edited-save run.** A level-27 slot-1 battle read the critical byte and speed at `MAIN.EXE+0xAD87/+0x12744`. The first Hatchet slot-2 trial reached defeat without a watch hit. A second copy with 500 HP fought the Hatchets under read watches: the critical byte and speed were read (`+0xAD87/+0x12997`), and no read after initialization touched `+0x0C/+0x0E/+0x10` or `+0x40`. The ranged click did not fire, so the ranged attack is still untested. [Byte changes and fight trace](unknowns/18_native_records.md#level-27-fight-from-an-edited-placement) and [Hatchet read watches](unknowns/18_native_records.md#read-watches-on-the-hatchet-definition)

**Not a test (2026-11-20).** An edited copy at block 497 holding item
type 216 (a Salve) in the cursor ([recipe](EDITED_SAVES.md#q18-held-item-on-level-27))
reached "You have been defeated" twice. The launch routine
`MAIN.EXE+0xF1DF` (thrown items and monster missiles) was never
fetched, so no ranged attack happened, and +0x0C, +0x0E and +0x40 were
not read in that window; +0x10 was not watched. **CONFIRMED, static.**
The Hatchets cannot make one: the slot-2 definition call
(`LEVEL27.INI`, DATA `+0x23E`) passes 0 for all five ranged words
(+0x42–0x4A), and the monster missile path loads the weapon word and
skips the launch unless bit 0xC000 is set (`+0x1253F–0x12593`). The
slot-1 call (`+0x1B2`) passes ranged words −1, 1 and `0x8009` (item 9).
Next test: the slot-1 copy (block 345) with read watches on the slot-1
words +0x0C/+0x0E/+0x10/+0x40, standing in a line two or more blocks
from a slot-1 monster so that it throws, or a party throw of a held
item at a Hatchet; record the launch fetch at `+0xF1DF` and a picture.

## Probes not yet run

These running-game tests have no result yet. A reader with the original game and a debugger can run them; the question each belongs to keeps its state until then. Addresses are `MAIN.EXE` file offsets unless the
line names another program; turn them into breakpoints as described at
the top of this page.

- **Level 23 pose squares: which picture shows (not run).** Settles the
  mode-11 frame of [Q7](OPEN_QUESTIONS.md). Full test:
  [Q7b](#q7b-which-animation-actually-displays-when-a-script-selects-mode-11).
  Setup: an edited copy of a level-1 slot set to level 23, as in the
  [pose-square recipe](unknowns/07_native_rules.md#level-23-pose-squares-from-edited-placements),
  but with the party near block 105 (or 121, 369) while a monster
  walks toward that square. Watch: the far call to the mode setter
  at CD `+0x14FC1` (floppy `+0x19948`), then the overlay frame selector
  found by its byte pattern, and a write watch on that monster's byte
  +0x14. Play: wait until the monster walks onto the pose square, so the
  script at CD `L23.PAK+0xC2AE` runs. Result: frame 14 with selector 0
  and no view or damage offset means the fixed mode-11 frame
  reached the screen. Any other frame must match the captured selector
  or draw flags. A write of 10 to +0x14 means a real mode-10 change.
  Two edited-save runs with a live placement (2026-11-20) saw the setter
  write 11; in the second the row was drawn from behind, frame 9
  ([result](#q7b-which-animation-actually-displays-when-a-script-selects-mode-11));
  frame 14 needs the monster to face the party. The event fires when a
  monster steps onto the square, not off it.
- **Mode 10 in ordinary play (not run).** Tests the static result
  for the mode-10 producer of [Q7](OPEN_QUESTIONS.md). Full test:
  [Q7c](#q7c-what-writes-mode-10-during-ordinary-play). Setup: any
  game-written slot in a level with active monsters. Watch: a write
  watch for the value 10 on byte +0x14 of each monster slot, at CD
  `2803:15FA + 46 × slot + 0x14` or floppy
  `2DCF:15DC + 46 × slot + 0x14`, plus the load segment. Play: fight,
  flee and walk past monsters. Result: the first write of 10 gives the
  writer, the old mode and the monster; then check its next frame
  choice. No write of 10 over a stated stretch of play bounds that
  stretch only.
- **Who opens the three palettes (not run).** Settles
  [Q14](OPEN_QUESTIONS.md) (`CAV_PLT2.PAL`, `CAV_PLT4.PAL`,
  `ALTPAL3.PAL`). Setup: a new game from the intro, or any game-written
  slot. Watch: a breakpoint on the generic file open that logs the
  incoming name and stops only on these three. On the floppy the open
  routine is at `+0xB442` (row lookup `+0x236D3–0x2383E`). On the CD
  no open routine address is on these pages: break on DOS open
  (`INT 21h` `AH=3Dh`) and seek (`AH=42h`) instead. The CD members sit
  at `CAVE1.PAK+0x1D72C`, `CAVE1.PAK+0x1DD2C` and
  `FOREST1.PAK+0x1B8B5` (rows 204, 206 and 122 of `FILEDATA.FDT`), so
  a seek to one of those offsets after opening that archive is a hit.
  Play: the intro, one level change and, if a slot can reach it, the
  finale. Result: a stop on one of the three gives the caller address
  and the read length; that caller is the answer. The palettes named by
  the level 2, 3, 24 and 25 scripts (`ALTPAL1.PAL`, `ALTPAL2.PAL`,
  `CAV_PLT3.PAL`) are positive controls for the breakpoint. No stop
  over the whole run bounds only what was played. Details:
  [palette callers](unknowns/14_palette_callers.md#remaining-question).
  A partial run (2026-11-20, edited-save run with the Q7b bytes) broke
  on the DOS open: the introduction up to `RICH3.WSA` opened
  `BWPAL.PAL` and `COLPAL.PAL` only, and the level-23 load opened no
  palette. The game asks for the loose name before the archive, so the
  name break also sees archive members. Neither window covers a cave
  or forest level, the positive controls or the finale, so this bounds
  nothing for the three names.
- **Who plays `00000.VOC` in the finale (not run).** Settles
  [Q10](OPEN_QUESTIONS.md). Setup: the finale program
  `ENG/FINALE.EXE`. Its addresses are its own file offsets; use the
  same rule as for `MAIN.EXE` with that program's header size. No
  edited-save recipe reaches the finale yet, so this needs a slot near
  the end of the game. Watch: the catalog lookups at `+0xCDD1`, `+0xCE4D`
  and `+0xEB05`, stopping when the selected row's name pointer is the
  name at `DS:08D0` (`00000.VOC`); and a read watch on that name
  (startup sets DS to `0x1B5B` plus the load segment). Do not stop on
  index 40: the startup sort at `+0xF0B0` reorders rows 4 to 92.
  Play: the whole finale. Result: a stop gives the caller of the
  clip's catalog row (file `0x1D1D0`), and that caller is the answer. No stop over
  the whole finale means the row was not used in that run. Details:
  [00000.VOC](unknowns/10_nnnnn_voc.md#what-would-settle-it).
  Blocked (2026-11-20): started on its own from the CD, `FINALE.EXE`
  printed "Please run 'LANDS.EXE' from your hard drive" and returned
  to the prompt, so no finale ran. The test needs the game's own route
  into the finale.
- **Level 22 block 27: what the wall shows (not run).** Settles the
  last open point of [Q4](OPEN_QUESTIONS.md). Setup: a game-written slot
  in level 22, in both editions. Watch: nothing; this is a look.
  Play: walk to block 27 and face each of its four sides. All four
  faces use wall type 24, VMP page 5, which ScummVM indexes as words
  2054–2484, past the 2054 words of both YVEL sets; the loader copies
  4500 VMP bytes (2250 words), and the rest of the buffer is whatever
  followed the file. Result: a clean wall face, a blank face or stray
  tiles shows whether the renderer reads VMP entries past 2054.
  Details: [YVEL2](unknowns/04_yvel2.md) and the
  [wall page](formats/vcn_vmp.md).

## Answered probes

### Q8. Which shutdown callbacks run on a given installation?

Question: [Q8 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** Shutdown preparation can call the registered far
pointer in CD `DS:361E` or floppy `DS:63EA` and query video
mode (CD `MAIN.EXE+0x2689C–0x2692F`, floppy
`+0x1DAB8–0x1DB2D`). [Shutdown trace](unknowns/08_native_script_exit.md#what-the-preparatory-routine-changes)

**CONFIRMED, English CD with Sound Blaster.** The run quit from the
installed original after loading level 1. The prep at `MAIN.EXE+0x2689C`
cleared its armed one-shot flag. At `+0x268EB`, `DS:361E` was null.
The BIOS query returned mode `0x13` at `+0x268FC`, the helper at
`+0x26904` took argument 9 and returned with `AX=3` (read from code: entry 9 of
the mode table always restores the saved mode, here 3), and the DOS
exit at `+0x3972` used `AX=0x4C00`.
[Recorded shutdown calls](unknowns/08_native_script_exit.md#english-cd-quit-from-play)

**CONFIRMED (static).** The explicit-operand search found no direct store to the optional
callback at CD `DS:361E` or floppy `DS:63EA`. The test and the call
are the references found by that search. The file
image holds `0000:0000` (CD `MAIN.EXE+0x350EE`, floppy `+0x3DC4A`).
[Scan details](unknowns/08_native_script_exit.md#english-cd-quit-from-play).
A computed-address store is the only open route. A write watch on
that pointer from program start, in any setup, would rule it out.
The earlier [refusal to start](#an-earlier-launch-that-was-refused)
gives an unarmed control.
