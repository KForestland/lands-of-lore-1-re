# Running the CD 1.02 game on a current machine

Read this against your own copy. The notes below come from the programs and the setup files in one English CD install, and from the strings those programs store. No game was launched for this page, so a setting is listed because a file names it, not because a play session scored it.

The retail build in that install reports `V CD1.02 D` at `MAIN.EXE+0x32A3F`. `MAINW.EXE` reports `V CD1.02 W` at `+0x324DF`.

## Which programs are which

| File | What it is | Role |
| --- | --- | --- |
| `LOLCD.BAT` | Three lines: turn echo off, enter `LOLCD`, run `LOLCD` | The CD start batch. |
| `LOLCD.EXE` | 19,356-byte MZ | The program that batch starts. |
| `MAIN.EXE` | 356,928-byte MZ | The CD game. It stores `V CD1.02 D`. |
| `MAINW.EXE` | 352,656-byte MZ | The other CD build. It stores `V CD1.02 W`. |
| `SETUP.EXE` | 103,188-byte MZ | Setup, beside the game. |
| `LANDS.EXE` | 357,509 bytes in `DATA/ENG` | Intro and character generation. The same name exists for French and German at different sizes. |
| `FINALE.EXE` | 132,328 bytes in `DATA/ENG` | Ending program for that language folder. |

The floppy edition is a different program. The tables tool recognizes a loose `MAIN.EXE` of 373,872 bytes as that edition. This install does not contain that file, so its bytes were not re-read here. Floppy text is English only. The CD text tables are English, French and German.

`MAIN.EXE` with no argument takes the refusal already described on the running-game page. The batch above is the start path this install uses.

## DOSBox settings read with this install

The configuration beside this install sets:

| Setting | Value |
| --- | --- |
| `machine` | `svga_s3` |
| `memsize` | `30` |
| `cycles` | `fixed 25000` |
| mixer | `nosound=true` on its own line |
| `sblaster` | `sb16`, IRQ 5, DMA 0, HDMA 5 |
| `gus` | `false` |
| speaker | off |

The autoexec mounts the installed disk and the CD, then runs `LOLCD.BAT`. This page did not raise the cycle count.

## Sound

`MAIN.EXE` names `LANDS.CFG` at `+0x32CD2` and `SBDIG.ADV` at `+0x33523`. In this install `LANDS.CFG` is 10 bytes: `b6 a2 a3 a0 a1 a6 a4 a5 00 b4`. This page does not turn those bytes into a card name.

The driver archive is `DATA/DRIVERS.PAK` (41,706 bytes) and `DATA/ENG/DRIVERS.PAK` (44,561 bytes). The seven drivers named on the drivers page are in that archive: AdLib Gold, Roland MT-32 / MPU-401, PC speaker, Sound Blaster, Sound Blaster Pro, Tandy, and `ALFX.DRV`. `SETUP.EXE` is the program that writes a setup. This page did not run it.

## Text

Spelling candidates in the text tables are listed by `tools/list_likely_spellings.py`. The command reads a DATA folder you name, prints rows, and writes no patch. See the [patch page](README.md).
