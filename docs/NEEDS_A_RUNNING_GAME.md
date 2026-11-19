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
route's behavior. Not reached yet: the launch works, but this needs a
level-8 save (or level 7 before the pit).

### Q7b. Which animation actually displays when a script selects mode 11?

Question: [Q7 in OPEN_QUESTIONS](OPEN_QUESTIONS.md).

**CONFIRMED.** In level 23 the monster-leaves script for block 105 selects
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
block. Let a monster leave that block to send event 0x0800. Break on
the far call to the script's mode setter at CD `+0x14FC1` or floppy `+0x19948`
(arguments pushed from CD `+0x14FBC` / floppy `+0x19943`).
Then capture the next draw of that same instance, recording the shape
bank, selector, direction offset and pending-damage state. Fixed frame
14 with selector 0 and no overriding direction or damage confirms
that fixed arm reached the screen. Any other frame should be accounted
for by the captured selector or draw flags. A write watch on that
instance's mode byte +0x14 also distinguishes an actual mode-10
transition from a frame picked while mode 11 remains set. Not
reached yet: the launch works, but this needs a level-23 save.

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
while brightness and oil stayed zero. Only the bulk save/load
calls accessed the three isolated bytes, which stayed zero at
`+0x268/+0x463/+0x486` in both new slots.
[Watch and native saves](unknowns/17_native_save_fields.md#cd-level-1-lamp-effect-reset)

**CONFIRMED, level-1 selected-character control.** The guard and
audience route reached block 273. The original overlay at
`MAIN.EXE+0x4C4AA/+0x4C4CB` twice changed the selected byte
0 → 99 → 0 with no access to the three isolated bytes. The native
save from block 272 still had one active character.
[Native stores, slot offsets and second-portrait test](unknowns/17_native_save_fields.md#cd-level-1-selected-character-control)

**UNCONFIRMED.** Any byte-specific writer or reader. Start a new
game, arm read and write watches after initialization, change the
active character and lamp state, enter another level, then save,
reload and save again. The known copy path gives equal saved and
live values. A byte-specific access outside that path identifies a
new producer or consumer. A stable zero and only bulk copies give
an unused-byte witness for that play sequence. Keep the watchpoints
active through the resume following the load. Movement, turning and
two load/save cycles are covered above. Not reached yet: an active oil or brightness change, a choice between two active portraits and a level change.

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
result to the actions taken. Not reached on this pass: see the CD
launch note.

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

**CONFIRMED (static).** No setup arms the optional callback through a
named store. Neither program has a store to CD `DS:361E` or floppy
`DS:63EA`; the only references are the test and the call. The file
image holds `0000:0000` (CD `MAIN.EXE+0x350EE`, floppy `+0x3DC4A`).
[Scan details](unknowns/08_native_script_exit.md#english-cd-quit-from-play).
A computed-address store is the only open route. A write watch on
that pointer from program start, in any setup, would rule it out.
The earlier [refusal to start](#an-earlier-launch-that-was-refused)
gives an unarmed control.
