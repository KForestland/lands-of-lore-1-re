# ADV, DRV, TBL

**Edition read:** CD and LANDSoL.

## Sound drivers: `DRIVERS.PAK`

Seven files, the same names in both editions but different bytes: `ALGDIG.ADV` (AdLib Gold), `MT32MPU.ADV` (Roland MT-32 / MPU-401 / LAPC-1), `PCSPKR.ADV` (PC speaker), `SBDIG.ADV` (Sound Blaster digital, also Media Vision Thunderboard), `SBPDIG.ADV` (Sound Blaster Pro digital), `TANDYDIG.ADV` (same device strings as SBDIG), and `ALFX.DRV`. CONFIRMED.

Every `.ADV` carries `Copyright (C) 1991,1992 Miles Design, Inc.` and its device names from byte 2: they are drivers from the Miles Sound System (the "Audio Interface Library"), which many DOS games licensed. `ALFX.DRV` starts with an x86 `jmp` (0xE9). These are executable code, not data; their insides are not documented here. The first uint16 of each `.ADV` (0x003F, 0x002D; 0x0036 on the floppy) is UNCONFIRMED.

Who loads them: the strings `ALGDIG.ADV`, `ALFX.DRV` and "Unable to load sound driver" sit in the floppy `LANDS.EXE`, `MAIN.EXE` and `FINALE.EXE`, which also name ten drivers that are not in either `DRIVERS.PAK` (`PASDIG.ADV`, `ADLIB.ADV`, `SBFM.ADV`, …). ScummVM loads none of them; it emulates the sound devices itself. CONFIRMED.

## `TRIG.TBL`: copy-protection text

`GENERAL.PAK` holds `TRIG.TBL`, 166 bytes, identical in both editions. It has the same layout as the text files ([text.md](text.md)): five uint16 offsets (10, 71, 77, 159, 165), then NUL-terminated strings with the game's text compression. Decoded with the same routine as the `.ENG` files (`engines/kyra/engine/util.cpp:29-87`) they read:

0. "Halt!  What is the password?  You may find it on page %d, line %d word %d of Geron's Guide."
1. "Zanthia"
2. "I will give you one more chance to give me the correct password.  You may find it on page %d, line %d word %d of Geron's Guide."
3. "Zanthia"
4. (empty)

CONFIRMED (decoded on CD). It is the manual-lookup copy protection: the speaker name and two prompts that ask for a word from the printed manual (*Geron's Guide*). `MAIN.EXE` and `FINALE.EXE` name the file; ScummVM skips copy protection and does not read it.

**Tool:** `tools/pak_reader.py list DRIVERS.PAK`; `tools/decode_dialogue.py TRIG.TBL --pak GENERAL.PAK` (the decoder works on any file with this layout).
