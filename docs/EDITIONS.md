# Identify your edition

Run this from the downloaded tools folder. Replace the example with the path to your own installation or its data folder. The command reads names, sizes and checksums and reports whether they match a measured copy. Each file is marked `matches`, `differs` or `missing`.

```sh
python3 tools/edition.py --data "/path/to/your/LoL1"
```

In Windows PowerShell, use `py -3` in place of `python3`, for example `py -3 tools/edition.py --data "C:\Games\LoL1"`. Requires Python 3.10 or later and the standard library.

Set `$LOL1_DATA` to the same folder to omit `--data`. Add `--check` to verify the complete fingerprint in one line.

## Measured files

**CONFIRMED.** Byte counts and SHA-256 cover every byte from file offset `+0x00` to EOF. File names start in the folder that contains `GENERAL.PAK`.

### English CD 1.02

| File | Bytes | SHA-256 |
|---|---:|---|
| `HARDRIVE/MAIN.EXE` | 356,928 | `10a9bdce8e234a917da36bbdfe5434add3d9ce01f0ea9b132a95b2fd1ef03e23` |
| `HARDRIVE/MAINW.EXE` | 352,656 | `3fb3b4a92ff4c5d4dccdaa66a1e3b6309c7bc30491cbb5eed9c63ef1f27fe935` |
| `HARDRIVE/LOLCD.EXE` | 19,356 | `80ea9411ca772d2c3d5ac2ae614f4a12f7f5b7b71a96938925469c815fc694c5` |
| `ENG/LANDS.EXE` | 357,509 | `5c0c5478df61a421a04d86ef10548ab73e775ed15d79d35bfa88c4ef5a5ec21c` |
| `ENG/FINALE.EXE` | 132,328 | `406c8460617d4553f17215fc1ea98d182c081a303296e83a037a1c0df1ac9550` |
| `FRE/LANDS.EXE` | 359,338 | `0eab44f69a5e99f07969027c13425f04a96df58d5d9a33bd0cfd3da1d645f529` |
| `FRE/FINALE.EXE` | 134,122 | `14522084432e13d045b17786a7e404b80de36e37ea18b80898a257303b8ec235` |
| `GER/LANDS.EXE` | 359,418 | `decc1cfce8adddd8aa880414ce569b97a9cb5bc4bfab45da5b0db805f65d204f` |
| `GER/FINALE.EXE` | 134,212 | `e2817d8e28040da8dd568c81bdc00a9aa68cfe34b6c83022fc8fd6a66a3b2384` |
| `GENERAL.PAK` | 1,225,033 | `e6a3ef89f39c1679b8de3cbe343bdaf20e1d4612eb7778d5bf75ca3015eab265` |
| `STARTUP.PAK` | 167,273 | `926e61c3c99a05c85a4820570345844de4fa0c99793191055071f787ab54d12d` |
| `L01.PAK` | 68,733 | `c52c240f093dafe405f6f318cbdc4bcaddbe05bea443e274bae18b75281ec2ac` |

### English floppy 1.05

| File | Bytes | SHA-256 |
|---|---:|---|
| `MAIN.EXE` | 373,872 | `4077ab84d19db6e16015b6d7752b4757344397dfce61a9caefd9b74701cc5a10` |
| `LANDS.EXE` | 129,490 | `01152602d9e6e8945b19de41b221f2c7e5f5aa63788872e08269c40595197438` |
| `FINALE.EXE` | 162,728 | `859f67e5b36abf79e3af96e0fe2715861fe7d65bb19834acceef2b327646cf8f` |
| `GENERAL.PAK` | 1,383,453 | `4248f0cea0489b804a15d68e70ce6afe5eb2dc7a6339ff7064b16b0125a92128` |
| `CHAPTER1.PAK` | 2,287,611 | `237e44d218ad8f52fd4520bf083f3ee3c0307b65d43507b2230a508ff3a89398` |
| `CHAPTER7.PAK` | 325,053 | `928129c3117978dcb61fc4f70ba7fbb2ad8b7c377b2675daff3c88e49fc97234` |

## Build strings and comparison

- **CONFIRMED.** The English CD programs identify themselves as 1.02. `HARDRIVE/MAIN.EXE+0x32B95` stores the full `V CD1.02 D` string, with `1.02 D` beginning at `+0x32B99`. `HARDRIVE/MAINW.EXE+0x32635` stores `V CD1.02 W`, with `1.02 W` beginning at `+0x32639`. Further DOS copies of `V CD1.02 D` start at `MAIN.EXE+0x32A3F, +0x32C9E, +0x32CA9`. Their version digits begin at `+0x32A43, +0x32CA2, +0x32CAD`. Floppy `MAIN.EXE+0x38AC5` holds `V 1.05`, between `LOLSYSEX` at `+0x38ABC` and `PLAIN` at `+0x38ACC`. **UNCONFIRMED.** The embedded build date of either edition. The DOS MZ header has no build date field. [Program locations](executable_tables.md#locating-the-executables)
- **CONFIRMED.** The CD first level is in `L01.PAK`, for example its CMZ at `+0x61EF`. The floppy first level is in `CHAPTER1.PAK`. The chapter archive starts with the absolute payload offset 3104 at `+0x00` and name `LEVEL1.XXX` at `+0x04`. Both follow the same PAK layout.
- **CONFIRMED.** The CD and floppy also match different ScummVM detection rows. Those rows use MD5 over at most the first MiB, so their values differ from the full SHA-256 values here. Upstream `engines/kyra/detection.cpp:55–60` and `engines/kyra/detection_tables.h:1349–1350, 1714–1717`. The companion files are `L01.PAK` and `CHAPTER7.PAK`, respectively.
- **CONFIRMED.** Both editions include 29 maps and 60 decoded level/item scripts. The native function table has 192 CD slots and 187 floppy slots, at `MAIN.EXE+0x33F64` and `+0x3D1EE` respectively. CD localized speech also uses numbered TLKs, which the floppy installation lacks. [Packaging and content comparison](edition_comparison.md) · [EMC2 differences](formats/emc2.md)

Other localizations and reissues have **not been measured here** as complete installations. The CD's French and German language programs in the table are part of the measured CD copy.
