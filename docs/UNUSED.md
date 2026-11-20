# Unused content and development leftovers

These counts refer to the original CD and floppy files in [Editions](EDITIONS.md). A zero count in the shipped scripts describes the stored instructions. It leaves open what a native caller or a computed filename might reach.

## Unused bytes in native readers

- **CONFIRMED.** Level 24 has 5,120 extra square bytes (1,024 × 5), beginning at decoded `LEVEL24.CMZ+0x0A` and repeated every nine bytes. The CD reader at `MAIN.EXE+0x48540, +0x48764` and floppy at `+0x51C10, +0x51E34` copy the four wall bytes and skip the five. [CMZ and its level-24 example](formats/cmz.md#confirmed)
- **CONFIRMED.** The row for source colour 255 is unreachable in each of the six localized CD blend tables. That is 256 possible cells per file, including its four final bytes at `+0xFFFC–0xFFFF`. The finale addresses a cell as `256 × source + destination` and none of its shipped source pictures contains colour 255. The four slot-5 call sites and the CD index calculation are on the proof page. [Finale blend indices](formats/finale-blend-indices.md)

## Commands and function slots

- **CONFIRMED.** Both sets of 60 EMC2 scripts use 17 of 19 VM opcodes. The two absent instructions are `0x01` (set the return value) and `0x12` (set return and jump). The interpreter still contains their cases. Its 19-word jump table is at CD `MAIN.EXE+0x133C6` and floppy `+0x17D89`. [EMC2 VM](emc2_scripts.md)
- **CONFIRMED.** The same census counts native function slots with zero stored `sysCall` instructions. The CD table begins at `MAIN.EXE+0x33F64` and floppy at `+0x3D1EE`. Each slot is four bytes. [Function table with stored call counts](emc2_scripts.md)

  | Witness | Slots with zero stored calls | Slot IDs in hex |
  |---|---:|---|
  | CD | 17 of 192 | 05, 17, 2B, 2C, 3D, 42, 43, 4D, 76, 77, 80, 90, 91, 95, A1, A2, BF |
  | Floppy | 16 of 187 | 05, 17, 2B, 2C, 3D, 42, 43, 4D, 76, 77, 90, 91, 95, A1, A2, BA |

- **CONFIRMED.** TIM `0x1E` is absent from the 139 scanned CD members and both floppy intro/outro sequences. ScummVM's TIM `0x1C` shows why absence in the bytecode is a narrower claim than absence in execution. No scanned CD TIM stores it, and the reference interpreter dispatches it internally when `procFunc` is set, at upstream `engines/kyra/script/script_tim.cpp:217–218`. [TIM tables and counts](unknowns/06_tim_opcodes.md)

## Registered resources with open callers

| Count | Resource and source | What is established |
|---|---|---|
| 3 distinct palettes, one copy per edition | `CAV_PLT2.PAL` and `CAV_PLT4.PAL` at CD `CAVE1.PAK+0x1D72C` and `+0x1DD2C`, `ALTPAL3.PAL` at `FOREST1.PAK+0x1B8B5`. Floppy copies at `GENERAL.PAK+0x5B2, +0xBB2, +0x14B2`. | **CONFIRMED.** None of the names occurs in the 60 EMC2 scripts of either edition or in the 139 CD and 147 floppy TIM members scanned. **UNCONFIRMED.** The generic filename lookup can open a computed name. No caller for those three has been identified. [Palette callers](unknowns/14_palette_callers.md) |
| 59 entries, 1 distinct clip | `00000.VOC`, first payload at `01.TLK+0x19F0`. One catalog registration in English `FINALE.EXE+0x1D1D0`, row 40 on disk. | **CONFIRMED.** All 59 entries match byte for byte. No searched instruction provides literal index 40. The lookup at `+0xCDD1` takes a computed index and startup prepares rows 4–92 for sorting at `+0xF0B0`. **UNCONFIRMED.** Whether a filename or runtime index ever opens the clip. [The 59 entries](unknowns/10_nnnnn_voc.md) |

## Development leftovers

**CONFIRMED.** The CD ships three standalone Borland symbol files (`ENG/FINALE.TDS`, `FRE/FINALE.TDS` and `GER/FINALE.TDS`) with a TDINFO header at `+0x00`. The three matching `LANDS.EXE` language programs carry symbol tables after their MZ images at offsets `0x23B00`, `0x241F0` and `0x24240`. The six byte ranges are development data. Their table layout, counts and file ends are checked by `tools/lol1_loose.py --check`. [Symbol table layout](formats/loose.md)

**UNCONFIRMED.** A list of native debug command-line switches for these LoL1 gameplay executables. The symbol tables above identify development data, and the native startup paths catalogued in the [mode and lookup notes](unknowns/07_native_rules.md) do not give a confirmed argument parser for such a list. The search of printable main-program strings did not settle it.
