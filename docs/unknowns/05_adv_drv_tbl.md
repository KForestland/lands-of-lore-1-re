# ADV, DRV, and TBL

`.ADV` and `.DRV` in `DRIVERS.PAK` are Miles Design DOS sound-driver code. The one `.TBL` in the game data is `TRIG.TBL`, a 166-byte table. ScummVM's Kyra engine does not load either kind. The DOS executables name them.

This note stops at the copyright string and the file's first instruction byte. The rest of each driver is code and is not disassembled.

## Drivers in DRIVERS.PAK

CONFIRMED. Both editions have one `DRIVERS.PAK` with these eight names. Sizes differ. The CD file and the LANDSoL file of each name are not the same bytes.

| Name | CD size | CD bytes 0-1 | LANDSoL size | LANDSoL bytes 0-1 | Identity string at byte 2, unless noted |
| --- | --- | --- | --- | --- | --- |
| ALFX.DRV | 6960 | `e9 8b` | 6521 | `e9 d4` | First byte is `E9`, a jmp. No copyright in the first bytes. |
| ALGDIG.ADV | 4449 | `3f 00` | 5584 | `36 00` | `Copyright (C) 1991,1992 Miles Design, Inc.` then `Ad Lib(R) Gold Music Synthesizer Card` |
| MT32MPU.ADV | 10378 | `2d 00` | 10625 | `2d 00` | same copyright, then `Roland MT-32 or compatible with Roland MPU MIDI Interface` and `Roland LAPC-1` |
| PCSPKR.ADV | 8153 | `2d 00` | 8352 | `2d 00` | same copyright, then `IBM PC or compatible internal speaker` |
| SBDIG.ADV | 3797 | `3f 00` | 4567 | `36 00` | same copyright, then `Creative Labs Sound Blaster(TM) Digital Sound` and `Media Vision Thunderboard(TM) Digital Sound` |
| SBPDIG.ADV | 4076 | `3f 00` | 4820 | `36 00` | same copyright, then `Creative Labs Sound Blaster Pro(TM) Digital Sound` |
| TANDYDIG.ADV | 3779 | `3f 00` | 4549 | `36 00` | same copyright and the same Sound Blaster / Thunderboard strings as `SBDIG.ADV` |

The first uint16 of an `.ADV` is 0x003F on the CD Ad Lib Gold, Sound Blaster, Sound Blaster Pro, and Tandy files, and 0x0036 on those four LANDSoL files. Roland and the PC speaker are 0x002D in both editions. The copyright string begins at file offset 2 in every `.ADV`. CONFIRMED. What the uint16 counts is UNCONFIRMED, because the following bytes are driver code.

## Who names them

CONFIRMED. The strings sit in the LANDSoL executables. Offsets are file offsets of the first matching byte.

`LANDS.EXE` (129490 bytes): `Unable to load sound driver` at 116100, `Initializing sound card.` at 117299, `ALGDIG.ADV` at 118830 and 120448, `ALFX.DRV` at 118898 and 120497. The same executable also names `PASDIG.ADV` at 120437, `PCSOUND.DRV` at 120510, `ADLIB.ADV` at 120571, `ADLIB.COM` at 120483, `TANDY.ADV` at 120537, `ADLIBG.ADV` at 120581, `PASFM.ADV` at 120592, `SBFM.ADV` at 120602, `SBP1FM.ADV` at 120611, and `SBP2FM.ADV` at 120622. Those ten names are not members of either `DRIVERS.PAK`. `MAIN.EXE` has the same ten names starting at 234059 (`PASDIG.ADV`). `FINALE.EXE` has them starting at 156827.

`MAIN.EXE` (373872 bytes): `TRIG.TBL` at 238876, `ALGDIG.ADV` at 234070, `ALFX.DRV` at 234119. It names the same extra drivers.

`FINALE.EXE` (162728 bytes): `Initializing sound card.` at 141258, `TRIG.TBL` at 144880, `ALGDIG.ADV` at 155047, `ALFX.DRV` at 155115. It names the same extra drivers.

A search of `engines/kyra` for `TRIG.TBL`, `ALGDIG`, `MT32MPU`, `PCSPKR`, `SBDIG`, `SBPDIG`, and `TANDYDIG` finds no match. The string `ALFX.DRV` at `detection_tables.h:580` is a Kyrandia 1 CD-demo detection entry, size 6531, hash `478116a7e6698b5cd51982ab48777fe6`. That is a different file from either Lands of Lore `ALFX.DRV` (6960 and 6521 bytes). CONFIRMED.

## TRIG.TBL

CONFIRMED. `TRIG.TBL` is in `GENERAL.PAK` in both editions, 166 bytes, byte-identical. It has no copyright string and does not start with `E9`. It is data.

The first five little-endian uint16s are 10, 71, 77, 159, 165. The value 10 is the size of those five words, so they are start offsets inside the file. The spans are:

| Start | End | Length |
| --- | --- | --- |
| 10 | 71 | 61 |
| 71 | 77 | 6 |
| 77 | 159 | 82 |
| 159 | 165 | 6 |
| 165 | 166 | 1 |

The last byte is `00`. CONFIRMED.

A 42-byte run at file offset 29 is repeated at file offset 117: `85 59 b3 20 f9 79 20 66 a0 e0 a2 84 a8 f5 67 88 25 e4 20 cc ac 20 25 e0 77 b1 e0 25 e0 b4 20 47 89 b0 27 b8 47 ef e1 2e 0d 00`. CONFIRMED as the bytes. What each span is used for is UNCONFIRMED. `MAIN.EXE` and `FINALE.EXE` name the file, and the Kyra sources do not.

Full file, 166 bytes:

```
0a004700 4d009f00 a500489b 74218557 d291a180 d020f573
7377b164 3f8559b3 20f97920 66a0e0a2 84a8f567 8825e420
ccac2025 e077b1e0 25e0b420 4789b027 b847efe1 2e0d005a
98906961 004986a4 c8676976 8879b384 ac20fac0 20dd98d8
80b26769 7688f880 d020dac7 65d920f5 737377b1 e58559b3
20f97920 66a0e0a2 84a8f567 8825e420 ccac2025 e077b1e0
25e0b420 4789b027 b847efe1 2e0d005a 98906961 0000
```
