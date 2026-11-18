# LoL1 executable and script tables

[EMC2 script format and corpus locations](emc2_scripts.md)

Evidence references use ScummVM revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`. **CONFIRMED** marks observations on the original CD and floppy data. **UNCONFIRMED** marks an interpretation from the reference implementation without proof from the native data or code. Hex offsets are file bytes unless marked as DATA words.

## Locating the executables

**CONFIRMED** The reference CD stores its DOS executables in `WESTWOOD.001`. The little-endian `u32` at `0x03` gives the length of the CRLF-delimited member list at `0x07`. The first list line names the list itself. For each subsequent line, read a length `u32 LE` and then that many payload bytes. The walk consumes the whole archive (end `0x3139A1`). The two gameplay images are also loose under CD `DATA/HARDRIVE`, where both match their archive member byte for byte. Both start with MZ headers. The archive member length includes overlay bytes beyond the MZ-declared image. The floppy executable is the loose floppy `MAIN.EXE`. See `WESTWOOD.001+0x07` for names and the prefix offsets below, and floppy `MAIN.EXE+0x00` for its MZ header.

| Image | CD length prefix | CD archive start | Member size |
| --- | ---: | ---: | ---: |
| `MAIN.EXE`, CD | `0x28C42` | `0x28C46` | `0x57240` |
| `MAINW.EXE`, CD | `0x7FE86` | `0x7FE8A` | `0x56190` |
| `MAIN.EXE`, floppy | — | — | `0x5B470` |

## Static executable tables

**CONFIRMED** Offsets below are relative to the named EXE, so add the CD archive start to read directly from `WESTWOOD.001`. Whole numeric spans were matched little-endian against the listed ScummVM providers. The character records have independent evidence from both their repeated layout and their MZ relocations.

| Table | CD MAIN | CD MAINW | floppy MAIN | Layout and reference |
| --- | ---: | ---: | ---: | --- |
| English character defaults | `0x29D60` | `0x29820` | `0x2B470` | 9 × 130 bytes. See record below. `devtools/create_kyradat/resources/lol_dos_cd_english.h:1–67`, `lol_dos_english.h:1–67`, `engines/kyra/resource/staticres_lol.cpp:52–99`. |
| Character modifier rows | `0x2B4D2` | `0x2AF92` | `0x2CD72` | 5 consecutive rows of 9 × `u16 LE` (18 bytes each). Native pointers reference rows 0, 1, 2 and 4. Row 3 repeats row 0's values. `lol_dos_cd.h:591–617`, `lol_dos.h:543–569`; MZ relocations described below. |
| Character equipment display layout | `0x2B47A` | `0x2AF3A` | `0x2CD1A` | 4 × 22 bytes, 11 pairs of coordinate bytes per layout. `devtools/create_kyradat/resources/lol_dos_cd.h:575–589`, `engines/kyra/gui/gui_lol.cpp:323,871–878`. |
| Spell properties | `0x2B5E0` | `0x2B0A0` | `0x2CE80` | 17 × 28 bytes, 14 `u16 LE` values per row. Byte-identical in these three images. `lol_dos_cd.h:501–521`, `lol_dos.h:453–473`, `staticres_lol.cpp:102–122`. |
| Experience thresholds | `0x2B830` | `0x2B2F0` | `0x324F0` | 11 × `u32 LE`, identical in both editions. Values are 0, 500, 1500, 5000, 25000, 50000, 80000, 120000, 180000, 270000, 2147483647. `lol_dos_cd.h:619–624`, `lol_dos.h:571–576`. |
| Monster difficulty modifiers 1–3 | `0x2B85C` | `0x2B31C` | `0x3251C` | 3 rows of 3 × `u16 LE`, easy/normal/hard, with 256 representing 1.0. The first row's easy value is 102 on CD and 192 on floppy. `lol_dos_cd.h:626–642`, `lol_dos.h:578–594`. |
| Monster difficulty modifier 4 | `0x2B86E` | `0x2B32E` | — | 3 × `u16 LE`, values 128, 256, 256. **UNCONFIRMED** whether a floppy analogue exists elsewhere. ScummVM selects this provider for talkie (`lol_dos_cd.h:644–648`, `devtools/create_kyradat/resources.cpp:5192–5195,5423–5427`). |
| Item price thresholds | `0x2F8C0` | `0x2F380` | — | 46 × `u16 LE` including final zero. **UNCONFIRMED** whether a floppy analogue exists elsewhere. The matching span is absent in floppy `MAIN.EXE`; the ScummVM CD provider and consumer are `lol_dos_cd.h:794–803`, `engines/kyra/script/script_lol.cpp:2329–2347`. |

Short references `lol_dos_cd.h`, `lol_dos.h` and `lol_dos_english.h` are under `devtools/create_kyradat/resources/`. `staticres_lol.cpp` is under `engines/kyra/resource/`. `script_lol.cpp` below is under `engines/kyra/script/`.

### Character default record

**CONFIRMED** In all three images the nine records have stride `0x82`. All bytes of corresponding records match between the CD images and floppy except the segment word of the far pointer at `+0x15`. The pointer's segment word has an MZ relocation in all nine records of each image. To find the referenced modifier row on disk, add the MZ header size (`u16 at +0x08` × 16), pointer segment × 16 and pointer offset. The records point to rows 0, 0, 0, 1, 0, 0, 1, 2, 4 in order. This is evidence from the character table bases above and the MZ relocation table (`+0x06` entry count and `+0x18` table offset). Field names and serialization follow `staticres_lol.cpp:52–95` and `engines/kyra/engine/lol.h:49–79`.

| Offset | Field |
| --- | --- |
| `00` | `u16` flags |
| `02` | 11-byte name buffer |
| `0D` | `u8` race/class/sex |
| `0E` | `i16` character ID |
| `10`, `11`, `12` | `u8` current face, temporary face, scream sound |
| `13` | DOS 16:16 far pointer, offset first, segment second. ScummVM's static reader discards this word pair and maps the modifier row when adding the character (`engines/kyra/engine/lol.cpp:1204–1210`). |
| `17`, `27` | 8 × `u16` item might and 8 × `u16` protection against each item category |
| `37` | `u16` item protection |
| `39`, `3B`, `3D`, `3F` | Current and max HP, current and max MP, each a 16-bit word. Current values are signed. |
| `41` | `u8` field of unresolved purpose (**UNCONFIRMED**). |
| `42`, `44` | `u16` damage suffered and weapon hit |
| `46`, `48` | `u16` total might and total protection multipliers |
| `4A`, `4C` | `u16` base might and protection |
| `4E` | `i16` next animation update countdown |
| `50` | 11 × `u16` default equipment type indexes. ScummVM turns nonzero entries into item handles on joining (`engines/kyra/engine/lol.cpp:1219–1223`). |
| `66`, `69` | 3 × `u8` skill levels and 3 × `i8` modifiers |
| `6C` | 3 × `i32` experience totals |
| `78`, `7D` | 5 × `u8` update events and 5 × `u8` delays |

### Spell property record

**CONFIRMED** All 17 rows match the DOS providers byte for byte. Fields below are `u16 LE`. The first 10 rows are populated. The last seven are zero. The first row's MP array is 5, 10, 15, 25. See CD `WESTWOOD.001+0x54226`, floppy `MAIN.EXE+0x2CE80`, and `staticres_lol.cpp:102–122`.

| Offset | Field |
| --- | --- |
| `00` | Name language ID |
| `02` | MP costs, four words in rank order |
| `0A`, `0C` | `field_a`, `field_c`. Their native meanings remain **UNCONFIRMED**. |
| `0E` | HP costs, four words in rank order |
| `16`, `18` | `field_16`, `field_18`. Further native use **UNCONFIRMED**. |
| `1A` | **CONFIRMED** Both executables use bit 8 to check the forward wall and the low byte to index the paid-cast dispatch table (CD `MAIN.EXE+0x4FEEE–0x4FF17, +0x4FFE6–0x50018`, floppy `+0x5A1F3–0x5A21C, +0x5A2E9–0x5A31B`). ScummVM uses the low byte for the Heal target click (`engines/kyra/engine/lol.cpp:2091–2122`, `engines/kyra/gui/gui_lol.cpp:1469–1476`). |

## Item types and item properties

**CONFIRMED** The 285 type definitions are embedded in `ONETIME.INF` bytecode. The record is a set of stack arguments of variable encoded length. In both editions, syscall `0x0D` at DATA word `0x06` allocates 285 slots. The next 285 calls to `0x0E` supply exactly one definition for each index 0 through 284. Check CD `STARTUP.PAK+0x212A5` for the allocation and `+0x212C1` for the first property call, or floppy `GENERAL.PAK+0xDAAFC` and `+0xDAB18`. The code leading into each call supplies the arguments in reverse push order and occasionally uses constant expressions. The reference loader runs `ONETIME.INF` at startup and separately loads `ITEM.INF` for event code (`engines/kyra/engine/lol.cpp:857–858`, `script_lol.cpp:234–261`).

| Stack slot | Field | Reference storage |
| --- | --- | --- |
| 0 | Definition index | Index into property array |
| 1 | Name language ID | `u16` |
| 2 | Shape index | `u8` |
| 3 | Equipment/type code | `u16` |
| 4 | Item script entry | `u8` |
| 5 | Might | `i8` |
| 6 | Skill/attack category | `u8` |
| 7 | Protection | `u8` |
| 8 | Flags | `u16` |
| 9 | `unkB` | `u16` |

The table gives the script ABI checked on data and reference field widths from `script_lol.cpp:241–261` and `engines/kyra/engine/lol.h:156–167`. The native 13-byte record has no extra `unkD` byte. The word at `+0B` still has an **UNCONFIRMED** purpose. See [native record layout](unknowns/18_native_records.md#item-definition) for the stores in both executables.

**CONFIRMED** Four decoded rows differ between editions. Indexes 243 and 249 use shape indexes 45 and 44 on CD, 43 and 42 on floppy. Indexes 263 and 264 use equipment/type 0 on CD, 5 on floppy. The reference definition loader special-cases 264 (`script_lol.cpp:249–252`). For indexes 243, 249, 263 and 264 respectively, see CD `STARTUP.PAK+0x2319B, +0x23279, +0x2346F, +0x2348F` and floppy `GENERAL.PAK+0xDC9F2, +0xDCAD0, +0xDCCC6, +0xDCCE6`.

## Monster properties

**CONFIRMED** Both editions define monster properties through 79 static calls to `0x3F`, each with 42 constant arguments. Calls occur in the 29 level INIs, `LEVEL23.INF`, `LEVEL29.INF` and `ITEM.INF`. The destination slot is part of each call, so several records may supply the same slot at different times. The first level's `0x3F` is at DATA word `0x7C` in both editions (CD `L01.PAK+0xF3B3`, floppy `CHAPTER1.PAK+0x61B53`). There are late-game examples at CD `L29.PAK+0x40D11`, floppy `CHAPTER8.PAK+0x423BE`, CD `STARTUP.PAK+0x11F8F` and floppy `GENERAL.PAK+0xDA94E`.

| Stack slots | Fields and conversion in the reference | Source |
| --- | --- | --- |
| 0–1 | Destination property slot and shape slot. Maximum width is derived from the loaded shapes. | `script_lol.cpp:928–939` |
| 2–8 | Hit modifier, protection modifier, raw evade value, speed modifier, then three additional modifiers. For slots 2, 3 and 5–8 multiply by 256 and divide by 100. Stored fighting stat 1 is fixed at 256, stat 8 at 0. | `script_lol.cpp:941–949` |
| 9–16 | Eight equipment-might values. | `script_lol.cpp:951–952` |
| 17–24 | Eight protection percentages. Multiply by 256 and divide by 100. | `script_lol.cpp:951–954` |
| 25–27 | Item protection, base HP, flags. Speed wait initially uses the literal 1. | `script_lol.cpp:956–959` |
| 28–29 | 28 is discarded by the reference. 29 becomes `unk5`; the field's native meaning is **UNCONFIRMED**. | `script_lol.cpp:960–962` |
| 30–34 | Ranged attack count, ranged weapon count, three ranged weapon entries. | `script_lol.cpp:964–967` |
| 35–38 | Attack chance, attack skill type, defense chance, defense skill type. | `script_lol.cpp:969–972` |
| 39–41 | Three sound IDs. | `script_lol.cpp:974–975` |

The call layout and argument counts above are **CONFIRMED** at the listed data offsets. The reference uses typed memory records in `engines/kyra/engine/lol.h:92–112`. The [native monster definition](unknowns/18_native_records.md#monster-definition) is 83 bytes and has its own far pointer to the fighting stats. A duplicate copy of the script definitions inside the images remains **UNCONFIRMED**.
