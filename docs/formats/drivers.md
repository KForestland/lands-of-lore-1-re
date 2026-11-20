# ADV, DRV, TBL

**Edition read:** CD and floppy.

## Sound drivers: `DRIVERS.PAK`

Seven files, the same names in both editions but different bytes: `ALGDIG.ADV` (AdLib Gold), `MT32MPU.ADV` (Roland MT-32 / MPU-401 / LAPC-1), `PCSPKR.ADV` (PC speaker), `SBDIG.ADV` (Sound Blaster digital, also Media Vision Thunderboard), `SBPDIG.ADV` (Sound Blaster Pro digital), `TANDYDIG.ADV` (same device strings as SBDIG), and `ALFX.DRV`. CONFIRMED.

**CONFIRMED.** Every `.ADV` carries `Copyright (C) 1991,1992 Miles Design, Inc.` at member +2. Its first u16 points to a table of (number, offset) word pairs ending in `0xFFFF`. Each offset reaches a `55 8B EC` routine prologue. CD `SBDIG.ADV` has `64 00 3B 09 65 00 0D 0A` at member +0x3F, so IDs 100 and 101 point to +0x93B and +0xA0D. The CD `DATA` folder holds a second archive, `ENG/DRIVERS.PAK` (44,561 bytes), byte-identical in `FRE/` and `GER/`. Its `MT32MPU.ADV`, `PCSPKR.ADV` and `ALFX.DRV` equal the root copies. Its other four `.ADV` files differ from both the root and the floppy files, with tables at +0x36 like the floppy. `lol1_driver_tables.py --check` checks 150 entries in the root CD archive, 146 in the language copy and 146 on floppy, 442 in all. It requires unique IDs per file and checks every target against its member bounds. The bytes between the copyright and the table and the routine bodies are not read.

**CONFIRMED.** `ALFX.DRV` starts at `DRIVERS.PAK+0x87BA` (CD) or `+0x96D3` (floppy). Member +0 jumps to the dispatcher and member +3 jumps to a separate entry at +0xC76 or +0xB4E. The dispatcher compares BX against the maximum selector and branches to an `iret` if above it. Otherwise it doubles BX and reads a near target from the table in CS. All listed wrappers end in `iret`. On CD they fill `+0x19A2–+0x1A5C` without a gap, followed by the out-of-range `iret` at `+0x1A5D`. For example, selector 0 (`+0x19A2`) is `push cs; call +0x199A; iret`, and selector 10 (`+0x19F9`) pushes CX, DX and AX, calls `+0x7B7`, drops six bytes and returns with `iret`.

| Edition | Dispatcher (member offset) | Target words | Selector 13 |
|---|---|---|---|
| CD (root and `ENG/FRE/GER`) | `+0x1A8E–+0x1A99` | 24 from `+0x1A5E` | `+0x19CD` |
| Floppy | `+0x18D7–+0x18E2` | 18 from `+0x18B3` | `+0x1850` |

Selector 13 pushes CX, DX and AX, discards those six bytes and returns without a call. CD selectors 18–23 are outside the floppy bound. The read-only tool lists the selectors and member addresses and checks both near jumps, the dispatch instruction pattern and wrapper extents. Pass either original `DATA` folder to `python3 tools/lol1_driver_tables.py --data DATA --check`.

**UNCONFIRMED.** The game meanings of the `.ADV` IDs and of the called `.DRV` bodies. A game-side indirect call through the `.ADV` table would bind its IDs to the game's actions. For `.DRV`, the code installing the target of the interrupt and passing BX would connect those callers to the dispatch above.

Who loads them: the strings `ALGDIG.ADV`, `ALFX.DRV` and "Unable to load sound driver" sit in the floppy `LANDS.EXE`, `MAIN.EXE` and `FINALE.EXE`, which also name ten drivers that are not in either `DRIVERS.PAK` (`PASDIG.ADV`, `ADLIB.ADV`, `SBFM.ADV`, …). ScummVM loads none of them; it emulates the sound devices itself. CONFIRMED.

## Worked example: `TRIG.TBL`, copy-protection text

`GENERAL.PAK` holds `TRIG.TBL`, 166 bytes, identical in both editions. It has the same layout as the text files ([text.md](text.md)): five uint16 offsets (10, 71, 77, 159, 165), then NUL-terminated strings with the game's text compression. Decoded with the same routine as the `.ENG` files (`engines/kyra/engine/util.cpp:29-87`) they read:

0. "Halt!  What is the password?  You may find it on page %d, line %d word %d of Geron's Guide."
1. "Zanthia"
2. "I will give you one more chance to give me the correct password.  You may find it on page %d, line %d word %d of Geron's Guide."
3. "Zanthia"
4. (empty)

CONFIRMED (decoded on CD). It is the manual-lookup copy protection: the speaker name and two prompts that ask for a word from the printed manual (*Geron's Guide*). `MAIN.EXE` and `FINALE.EXE` name the file; ScummVM skips copy protection and does not read it.

Details: [`../unknowns/05_adv_drv_tbl.md`](../unknowns/05_adv_drv_tbl.md).

**Tool:** `tools/pak_reader.py list DRIVERS.PAK`; `tools/decode_dialogue.py TRIG.TBL --pak GENERAL.PAK` (the decoder works on any file with this layout).
