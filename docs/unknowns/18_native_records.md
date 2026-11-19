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
| `0B` | `u16` base shop price in crowns, exposed by getter selector 14. | 9 | `0x4A69E`, getter `0x1399C` | `0x53C72`, getter `0x1835F` |

Worked example (**CONFIRMED**). Definition 1 receives name `0x40F6`, shape 6, flags `0x1000`, type 0, script 25, might 8, skill 1, protection 0 and auxiliary 0. This creates the packed record `F6 40 06 00 10 00 00 19 08 01 00 00 00`. It follows from the stores above and the call in CD `STARTUP.PAK+0x212DD` and floppy `GENERAL.PAK+0xDAB34`. The record ends after the auxiliary word.

## Monster definition

**CONFIRMED** EMC2 syscall `0x3F` initializes the 83-byte record. Argument 0 is the destination index. The stat conversion in this table is signed integer `value × 256 / 100`. The two copies of the loader agree on the stores and their order (CD `+0x47830–0x47B76`; floppy `+0x5100F–0x51355`). ScummVM field names are in `engines/kyra/script/script_lol.cpp:919–977` and `engines/kyra/engine/lol.h:92–112`.

| Record offset | Type and initialization | CD | Floppy |
| ---: | --- | ---: | ---: |
| `00` | `u8` shape bank, argument 1 | `0x47867` | `0x51046` |
| `01` | `u8` maximum width from 16 shapes | `0x47873–0x478CB` | `0x51052–0x510AA` |
| `02`, `04`, `06`, `08` | `u16` stats 0–3. Hit factor from converted arg 2, might factor 256, armour factor from converted arg 3, evade from raw arg 4 | `0x478CF–0x4793E` | `0x510AE–0x5111D` |
| `0A`, `0C`, `0E`, `10`, `12` | `u16` stats 4–8. Speed at `0A`, converted values from args 5–8, then literal zero for stat 8. Uses of stats 5–7 are **UNCONFIRMED**; only the setter stores were found. Test: [test Q18](../NEEDS_A_RUNNING_GAME.md#q18-which-monster-definition-fields-does-an-actual-fight-use). | `0x47942–0x479EA` | `0x51121–0x511C9` |
| `14` | Far pointer with offset and segment words, targeting this record's own `+02` | `0x47A4B–0x47A5B` | `0x5122A–0x5123A` |
| `18` | 8 × `u16` might categories from args 9–16 | `0x479F2–0x47A0F` | `0x511D1–0x511EE` |
| `28` | 8 × two-byte category factors from converted args 17–24. Native damage applies the sign of the word. | `0x47A13–0x47A49, +0xAFD8–0xAFFF` | `0x511F2–0x51228, +0xAEFA–0xAF21` |
| `38`, `3A` | `u16` item protection and base HP, args 25 and 26 | `0x47A74, +0x47A8D` | `0x51253, +0x5126C` |
| `3C` | `u8` total speed wait, initialized to 1 | `0x47AAA` | `0x51289` |
| `3D` | One-byte critical skill level, read by the hit test. Starts at zero in the loaded executable image. The definition setter leaves it unwritten. | `0xAD82–0xAD8F, +0x47AA6–0x47AAF` | `0xACC3–0xACD0, +0x51285–0x5128E` |
| `3E` | `u16` definition flags, arg 27 | `0x47AA6` | `0x51285` |
| `40` | `u16` auxiliary word. Arg 29 immediately overwrites arg 28. Interpretation **UNCONFIRMED**; only the two setter stores were found. Test: [test Q18](../NEEDS_A_RUNNING_GAME.md#q18-which-monster-definition-fields-does-an-actual-fight-use). | `0x47AAD–0x47ADD` | `0x5128C–0x512BC` |
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
| Monster `+14` mode, `+16` ID, `+17` direction, `+18` facing, `+1D` current HP, `+20` type, `+21` far pointer to definition | CD spawn code `+0x146B3–0x14769`; floppy spawn body `+0x18FB1`. Active slot 0 in a floppy `_LEVEL1.TMP` written by the game during play (not shipped; [save format](../savegame_format.md)) starts at `0x69`, and its pointer bytes are at `0x8A`. |

## Item price in the original scripts


**CONFIRMED** The auxiliary word is the unrounded shop price. CD `LEVEL1.INF` calls getter `0x12` with selector 14 and uses the result as the argument to price routine `0xBD` (CD `L01.PAK+0xE559, +0xE55F`, native price handler `MAIN.EXE+0x16837`). A second branch passes the result shifted right by one to the same routine (CD `L01.PAK+0xE5EF–0xE5F9`). floppy passes the full result directly to credit adjustment `0x46` on one branch, and half on the other (floppy `CHAPTER1.PAK+0x5821B–0x58235`, native credit handler `MAIN.EXE+0x194EB`). The full and half values also reach the floppy dialogue at `CHAPTER1.PAK+0x59A69, +0x59AEB`.

**CONFIRMED** All 285 startup slot-9 values agree between editions. 113 are zero and 172 are nonzero, up to 3000. The definition for item 24 passes 300 at CD `STARTUP.PAK+0x2151F` and floppy `GENERAL.PAK+0xDAD76`. Item 51 passes 3000 at CD `+0x218E3` and floppy `+0xDB13A`. Static operand reconstruction across the 60 scripts per edition identifies nine CD and eleven floppy literal selector-14 calls. Three CD getter selectors and one floppy selector could not be settled from the immediate argument sequences. Corpus anchors are the shop calls above and CD `L03.PAK+0x3EB0`, floppy `CHAPTER1.PAK+0x5E023`.

## Remaining monster-field measurements

**CONFIRMED** All five 83-byte definition slots are zero in the resident engine-state image: CD `MAIN.EXE+0x2D38E–0x2D52C` and floppy `+0x34030–0x341CE`. The hit test reads the signed critical skill byte at `+0x3D` and computes `100 − value` (CD `+0xAD82–0xAD8F`, floppy `+0xACC3–0xACD0`). The definition setter stores `+0x3C` then proceeds to `+0x40` (CD `+0x47AA6–0x47AC4`, floppy `+0x51285–0x512A3`). The sidecar load rebuilds each active instance's definition pointer from its stored type byte, using the resident definitions (CD `+0x48828–0x4883F`, floppy `+0x51EF8–0x51F0F`).

**CONFIRMED** In all 79 original property-load calls per edition, modifier args 6–8 are jointly zero in 50 calls and each is nonzero in 29. A nonzero example is `LEVEL27.INI` at CD `L27.PAK+0xACB9` and floppy `CHAPTER8.PAK+0x3C940`, with inputs 100, 25, 100 and stored words 256, 64, 256. The same decoder finds that arg 28 spans 0–15 and arg 29 spans 20–1000 in both editions. For example, the inputs 10 and 768 in `LEVEL1.INI` leave 768 at `+0x40` because the second write immediately overwrites the first (CD `L01.PAK+0xF3B3`, floppy `CHAPTER1.PAK+0x61B53`, stores above).

**UNCONFIRMED** (superseded in scope by the [whole-program reference scan](#whole-program-reference-scan) below) No writer beyond startup initialization was found for `+0x3D`. A bounded search of direct far loads from instance `+0x21` and its displacement aliases found the hit-test reads above. It also verified speed lookup through the embedded pointer at `+0x14` (CD `+0x12740, +0x12993`, floppy `+0x170DE, +0x17332`), but found no use of modifier offsets `+0x0C–0x10` or the last word at `+0x40` from the same pointer-loading pattern. The CD selector table for EMC getter `0x5C` has no branch for these fields (`+0x1502C–0x150CA`). A watch on those definition fields during the original level-27 fights would distinguish unused fields from accesses through a generic pointer.

### Additional native pointer tests

**CONFIRMED** An executable-byte search for the far-pointer
load of instance +0x21 found 52 candidates in the CD image and
51 in floppy. The immediate accesses after those loads include
definition byte +1 for collision width (CD `+0x111C1–0x111C5`,
floppy `+0x15C5D–0x15C61`) and the four attack and defense
bytes at +0x4C–0x4F (CD `+0x119A5–0x119BE, +0x11C09–0x11C22`,
floppy `+0x16441–0x1645A, +0x16617–0x16630`). A separate
search for the far-pointer load of definition +0x14 finds two
exact matches per edition. Both read stat-pointer +8, which is
definition +0x0A (CD `+0x12740–0x12744, +0x12993–0x12997`,
floppy `+0x170DE–0x170E2, +0x17332–0x17336`). These
checked access paths do not consume +0x0C, +0x0E, +0x10 or +0x40.

**CONFIRMED** The level-27 example that sets the three modifiers
uses definition slot 1, with +0x40 = 155 after overwriting 7.
The next definition load uses slot 2, zero modifiers and +0x40
= 132 after overwriting 5 (CD `L27.PAK+0xACB9/0xAD45`,
floppy `CHAPTER8.PAK+0x3C940/0x3C9CC`). The definition
bank's 83-byte stride and the spawn path's segment and
base come from CD `MAIN.EXE+0x14675–0x1467F` and
floppy `+0x1900D–0x19017`.

**UNCONFIRMED** The bounded scan tracked the immediate
ES:BX access until a pointer reload, unconditional transfer or
call. It cannot settle a copied far pointer or a computed index.
After the slot-1 setter returns in level 27, watch reads of the
following original relative segment offsets (add the program's
load segment, PSP+0x10, at run time) while a slot-1
monster moves, attacks, takes damage and uses a ranged effect.

| Edition | Three modifier words | Critical byte | Last word |
|---|---|---|---|
| CD | `2803:1BBD/1BBF/1BC1` | `2803:1BEE` | `2803:1BF1` |
| floppy | `2DCF:1B9F/1BA1/1BA3` | `2DCF:1BD0` | `2DCF:1BD3` |

Record the first reading instruction and its result, and any
write to the critical byte beyond initialization or loading.
Use the adjacent +0x0A read as a control to verify the address
and active definition slot. The raw byte counts and attached
offsets above bound the static result.

### Level-one saved control

**CONFIRMED.** In the CD 1.02 slot written by the game in the probe run
(not shipped; SHA-256 prefix `746b8748466f`), the level byte at `+0x269` is 1 and the
level-1 chunk length at `+0x1D87` is 1,529. The four occupied
46-byte monster rows at `+0x1D98`, `+0x1DC6`, `+0x1DF4` and
`+0x1E22` have definition slot 1 and mode 1 (row +0x20 and
+0x14 respectively). Their blocks are 589, 524, 271 and 271
(row +5). These are the guard-level records loaded from the
first level, whose native initialization uses slot 1.
[Level 1 initializers](../levels/level01.md#level1ini)

**UNCONFIRMED.** The definition reads and critical-byte writes
in a level-27 fight. The original game was played to level 1
and no played level-27 slot was available. A native level-27
slot can drive the watches above and verify the +0x0A control
while the same monster takes and deals damage.

### Whole-program reference scan

**CONFIRMED** The scan covered every byte of each resident load image
and every byte of its appended FBOV area. The DOS header size comes from
file +8 and the resident file end from +2/+4. The FBOV body length
comes from FBOV +4. Ranges are half-open. The property setter and its five
stores are in the overlay; they reach the definition through a
stack-local pointer (`les bx,[bp-4]`), so the scan does not find them by
access form; the tool pins their bytes at the cited addresses instead.

| Edition | Resident file range | FBOV header and body | Definition bank | Instance-pointer displacement aliases |
|---|---|---|---|---|
| CD | `0x3800–0x3CC40` | `0x3CC40–0x57240` | `2803:1B5E` | `+0x21`, `+0x161B` |
| Floppy | `0x4800–0x45DA0` | `0x45DA0–0x5B470` | `2DCF:1B40` | `+0x21`, `+0x15FD` |

**CONFIRMED** Across those ranges, decode every candidate LES/LDS
including the explicit ES and DS forms. The instance displacements
above yield 57 CD and 58 floppy candidates. These counts include byte
patterns in noncode. Continue each candidate for up to 140 bytes
through ordinary register copies and immediate offset arithmetic,
ending at a call, jump, return, segment change or loss of its tracked
registers. The separate +0x14 embedded-stat-pointer displacement scan
gives seven candidates in each edition and verifies the two +0x0A
speed controls. For each of the five slots, match every 16-bit ES
memory displacement for its five queried field addresses. This found
zero direct-address matches in either program. The known, indexed bank
origins are the spawn, setter and save-load rebind, with base immediates
at CD file `0x1472A/0x4784A/0x48837` and floppy
`0x190C2/0x51029/0x51F07`. The overlay segment words
`0x5F8` and `0x460` in the setters resolve to those bank
segments through the FBOV directories at `0x2FC50` and `0x36500`.

| Field | CD confirmed references | Floppy confirmed references |
|---|---|---|
| +0x0C | Store `0x47992` | Store `0x51171` |
| +0x0E | Store `0x479BC` | Store `0x5119B` |
| +0x10 | Store `0x479E6` | Store `0x511C5` |
| +0x3D | Read `0xAD87` | Read `0xACC8` |
| +0x40 | Stores `0x47AC4`, `0x47ADD` | Stores `0x512A3`, `0x512BC` |

Run the check with Python and Capstone installed (`pip install -r requirements.txt`). With `--data` (or `$LOL1_DATA`) it checks that edition's `MAIN.EXE`; `tools/check_all.py` runs it this way.

```bash
python3 tools/monster_reference_scan.py --check --data /path/to/DATA
python3 tools/monster_reference_scan.py --check \
  --cd /path/to/cd/MAIN.EXE --floppy /path/to/floppy/MAIN.EXE
```

**UNCONFIRMED** References through computed aliases, stack reloads or
calls beyond the tracked block. Among the 57/58 instance-pointer and 7 stat-pointer candidates, the
only tracked field access is the one +0x3D read; none touches
+0x0C–+0x11 or +0x40–+0x41. The five setter stores are byte-checked in
the definition setter. A read/write watch on the slots above during a level-27 fight
would resolve the remaining alias question and detect any write to +0x3D.

### Level-27 fight from an edited placement

**CONFIRMED, edited-save run.** Two copies of the native CD
level-1 slot `477b08b82ecd` reached level 27. Both changed
`+0x269=01→1B`, `+0x255=02→01`, and `+0x263=00→03`
(level, high block byte and west facing). The additional
changed bytes were as follows.

| Copy and placement | Slot offset and old → new |
|---|---|
| `1fa09b2431df`, block 345 next to slot-1 actors | `0x254=2D→59, 0x257=0D→19, 0x259=11→0A` |
| `3d99217b84dd`, block 497 next to the shipped slot-2 placement | `0x254=2D→F1, 0x257=0D→11, 0x259=11→0F` |

Slot 1 uses shape bank 0 (`TCABAL.SHP`), set by the
`L27.PAK+0xACB9` call. Slot 2 uses `HATCHETS.SHP` in bank 1
(`+0xAD45`), with zero values for the three modifiers. At
block 345, an active slot-1 row was on adjacent block 344.
The first trial reached defeat. A reload with the watches
armed covered definition initialization and attacks with
the weapon button. The watch at definition +0x3D recorded two
reads at `MAIN.EXE+0xAD87`. The aligned watches covering
+0x0C/+0x0E/+0x10 and +0x40 recorded the initialization stores
in `+0x47942–0x479EA` and `+0x47AAD–0x47ADD`. During the
sampled fight, reads in those aligned spans instead selected
speed +0x0A (`+0x12744/+0x12997`), other earlier stats, and
adjacent definition flags +0x3E or ranged fields. The watch
found no fight-time access to the three modifier words or
+0x40 and no write to +0x3D in that window.

**UNCONFIRMED, edited-save run.** The actual slot-2 Hatchet trace
remains open. The block-497 copy restored at the requested position
but reached defeat before a hit in the four watched spans
(`2803:1C08/1C10/1C38/1C40`, eight bytes each, plus load segment).
A longer-lived native party, with watches armed before the load,
would capture the first slot-2 attack and more varied ranged/hit
cases. The slot-1 access record is a separate control.

### Read watches on the Hatchet definition

**CONFIRMED, edited-save run.** The English CD original loaded
`335aa1b42956` from source `477b08b82ecd`. Use the block-497
placement bytes in the table above and change `+0x85..+0x88`
from `14 00 14 00` to `F4 01 F4 01` (current and maximum HP,
20 to 500 in the first 130-byte character row). The visible attackers
used the two-axe shape. Their slot-2 definition is the bank-1
record initialized at `L27.PAK+0xAD45`.

The four eight-byte hardware read watches started at
`2803:1C08/1C10/1C38/1C40` plus the loaded segment. They were armed
in the first fight and stayed armed through a reload and a logged
five-second replay of a forward input, two weapon clicks, an
inventory pickup and an attempted ranged click. The first fight
showed party damage and defeat. The ranged click in the replay
left the item held, so it did not demonstrate a projectile.
The guest sites include the critical byte read at
`MAIN.EXE+0xAD87` and the speed read at `+0x12997`. Other hits
were to neighbouring fields or to initialization stores reported
during reload. No post-initialization read in the recorded
ranges addressed modifiers `+0x0C/+0x0E/+0x10` or auxiliary
word `+0x40`.

**UNCONFIRMED.** A successful ranged action on these watches
and the purposes of the four fields. Repeat with a ranged
weapon already equipped and follow an original projectile
through the release routine. Both slot-1 (nonzero modifiers)
and Hatchet slot-2 (zero modifiers) now have scoped read controls.
