# Q18 — Native item and monster records

[Executable and script tables](../executable_tables.md) · [Save format](../savegame_format.md)

There are four different native layouts. An item or monster **definition** describes a type. An **instance** is an allocated world slot with position, state and a reference to a definition. The findings below are from English DOS CD `MAIN.EXE` and floppy `MAIN.EXE`. Offsets in record tables are hexadecimal, and all multi-byte fields are little-endian. Executable references are file offsets. Borland overlay code offsets are given at the file-backed body when the dispatch table points to a loading stub.

| Native layout | Stride | How the game locates it (**CONFIRMED**) |
| --- | ---: | --- |
| Item definition | `0x0D` | A far pointer in the main data segment at CD `DS:7FB2`, floppy `DS:B458`. Allocation multiplies the count by 13, and the setter scales the ID by 13. CD `+0x4A59B–0x4A6D4`; floppy `+0x53B6F–0x53CA8`. |
| Item instance | `0x10` | 400 records starting at engine-state offset `0x1CFD` (CD) or `0x1CDF` (floppy). The constructor shifts the slot index left four bits. Each save writes the consecutive `0x1900` bytes. CD `+0xB504, +0x48BAD–0x48BBF`; floppy `+0xD66E, +0x52208–0x5221A`. |
| Monster definition | `0x53` | The indexed base is engine-state offset `0x1B5E` (CD) or `0x1B40` (floppy). Five such positions fit between the definition base and the item instance array. CD `+0x47837–0x47851, +0x14724–0x14732`; floppy `+0x51016–0x51030`. |
| Monster instance | `0x2E` | 30 slots starting at engine-state offset `0x15FA` (CD) or `0x15DC` (floppy). The constructor clears 46 bytes and steps the same stride. The native temporary-level writer and reader transfer `0x564` bytes from/to this array. CD `+0x146A4–0x146D7, +0x148C8, +0x4863F–0x48654, +0x486F7–0x4870C`; floppy `+0x51D0F–0x51D24, +0x51DC7–0x51DDC`. |

## Item definition

**CONFIRMED** EMC2 syscall `0x0E` initializes the packed 13-byte record. Stack slot 0 is the index, and the remaining argument order is distinct from the packed record order. The native allocator/constructor confirms the record size in both editions. ScummVM's field names can be checked at `engines/kyra/script/script_lol.cpp:241–261` and `engines/kyra/engine/lol.h:156–167` at revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`.

| Record offset | Type and field | EMC slot | CD store | Floppy store |
| ---: | --- | ---: | ---: | ---: |
| `00` | `u16` name string ID | 1 | `0x4A5FA` | `0x53BCE` |
| `02` | `u8` shape index | 2 | `0x4A61A` | `0x53BEE` |
| `03` | `u16` flags | 8 | `0x4A67D` | `0x53C51` |
| `05` | `u16` type/equipment code | 3 | `0x4A63B` | `0x53C0F` |
| `07` | `u8` item-script entry | 4 | `0x4A65C` | `0x53C30` |
| `08`, `09`, `0A` | `i8` might, `u8` skill category, `u8` protection | 5, 6, 7 | `0x4A6C3–0x4A6CD` | `0x53C97–0x53CA1` |
| `0B` | `u16` auxiliary value, exposed by getter selector 14. Semantic purpose **UNCONFIRMED**. | 9 | `0x4A69E`, getter `0x1399C` | `0x53C72`, getter `0x1835F` |

Worked example (**CONFIRMED**). Definition 1 receives name `0x40F6`, shape 6, flags `0x1000`, type 0, script 25, might 8, skill 1, protection 0 and auxiliary 0. This creates the packed record `F6 40 06 00 10 00 00 19 08 01 00 00 00`. It follows from the stores above and the call in CD `STARTUP.PAK+0x212DD` and floppy `GENERAL.PAK+0xDAB34`. The record ends after the auxiliary word.

## Monster definition

**CONFIRMED** EMC2 syscall `0x3F` initializes the 83-byte record. Argument 0 is the destination index. The stat conversion in this table is signed integer `value × 256 / 100`. The two copies of the loader agree on the stores and their order (CD `+0x47830–0x47B76`; floppy `+0x5100F–0x51355`). ScummVM field names are in `engines/kyra/script/script_lol.cpp:919–977` and `engines/kyra/engine/lol.h:92–112`.

| Record offset | Type and initialization | CD | Floppy |
| ---: | --- | ---: | ---: |
| `00` | `u8` shape bank, argument 1 | `0x47867` | `0x51046` |
| `01` | `u8` maximum width from 16 shapes | `0x47873–0x478CB` | `0x51052–0x510AA` |
| `02`, `04`, `06`, `08` | `u16` stats 0–3. Hit factor from converted arg 2, might factor 256, armour factor from converted arg 3, evade from raw arg 4 | `0x478CF–0x4793E` | `0x510AE–0x5111D` |
| `0A`, `0C`, `0E`, `10`, `12` | `u16` stats 4–8. Speed at `0A`, converted values from args 5–8, then literal zero for stat 8. Uses of stats 5–7 are **UNCONFIRMED**. | `0x47942–0x479EA` | `0x51121–0x511C9` |
| `14` | Far pointer with offset and segment words, targeting this record's own `+02` | `0x47A4B–0x47A5B` | `0x5122A–0x5123A` |
| `18` | 8 × `u16` might categories from args 9–16 | `0x479F2–0x47A0F` | `0x511D1–0x511EE` |
| `28` | 8 × two-byte category factors from converted args 17–24. Native damage applies the sign of the word. | `0x47A13–0x47A49, +0xAFD8–0xAFFF` | `0x511F2–0x51228, +0xAEFA–0xAF21` |
| `38`, `3A` | `u16` item protection and base HP, args 25 and 26 | `0x47A74, +0x47A8D` | `0x51253, +0x5126C` |
| `3C` | `u8` total speed wait, initialized to 1 | `0x47AAA` | `0x51289` |
| `3D` | One-byte critical skill level, read by the hit test. Loader leaves it unwritten. Writer or initialization source **UNCONFIRMED**. | `0xAD82–0xAD8F, +0x47AA6–0x47AAF` | `0xACC3–0xACD0, +0x51285–0x5128E` |
| `3E` | `u16` definition flags, arg 27 | `0x47AA6` | `0x51285` |
| `40` | `u16` auxiliary word. Arg 29 immediately overwrites arg 28. Interpretation **UNCONFIRMED**. | `0x47AAD–0x47ADD` | `0x5128C–0x512BC` |
| `42`, `44`, `46`, `48`, `4A` | Five `u16` words from args 30–34: ranged charge count, ranged weapon count, three ranged weapon IDs | `0x47AE1–0x47B08` | `0x512C0–0x512E7` |
| `4C`–`4F` | Four `u8` values from args 35–38: attack chance/type, defense chance/type | `0x47B0A–0x47B4A` | `0x512E9–0x51329` |
| `50`–`52` | Three `u8` sound IDs, args 39–41 | `0x47B4C–0x47B6F` | `0x5132B–0x5134E` |

The native attack test follows the embedded stat pointer at `+14`; the monster instance points to the start of the whole definition. For example, CD `LEVEL1.INI` submits hit percentage 200, armour percentage 100 and raw evade 100 at `L01.PAK+0xF3B3`. The setter stores `00 02` at `+02`, `00 01` at `+06` and `64 00` at `+08`. floppy's corresponding call is `CHAPTER1.PAK+0x61B53`. **CONFIRMED** using the stores above.

## Instances

**CONFIRMED** The DOS save writer copies the native item array directly, and the original level sidecar preserves the native monster array. The full field maps are the [item slot](../savegame_format.md#item-instance-record) and the **native** column of the [monster slot](../savegame_format.md#monster-slot). CD `MAIN.EXE+0x48BAD–0x48BBF, +0x4863F–0x48654`; floppy `+0x52208–0x5221A, +0x51D0F–0x51D24`. Some useful native accessors are:

| Native field | Evidence |
| --- | --- |
| Item `+05,+07,+09` block/X/Y, `+0B` level, `+0C` property index, `+0E` shape/frame and flags | CD getter `+0x138F3–0x13929`; floppy `+0x182B6–0x182EC`. |
| Item `+0E` bit 15 marks an available slot, low 13 bits can be replaced independently | CD `+0xB504–0xB517, +0x13A34–0x13A45`; floppy `+0xD66E–0xD681, +0x183F7–0x18408`. |
| Monster `+14` mode, `+16` ID, `+17` direction, `+18` facing, `+1D` current HP, `+20` type, `+21` far pointer to definition | CD spawn code `+0x146B3–0x14769`; floppy spawn body `+0x18FB1`. Active slot 0 in original floppy `_LEVEL1.TMP` starts at `0x69`, and its pointer bytes are at `0x8A`. |

## Remaining measurements

**UNCONFIRMED** The data and setter traces locate the fields with undecided meanings above. They do not identify a consumer of the item auxiliary word or a writer for monster critical skill level. An original execution watch on the two fields after allocation, or an independently sourced script call that uses item selector 14 in a typed operation, would settle those uses. A trace of writes to monster definition offsets `+0C` through `+12` beyond `0x3F` and reads of `+40` would settle those modifier roles.
