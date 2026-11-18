# Q7 — Spell effects, timers, monster updates and walls in native DOS

**CONFIRMED** offsets name physical bytes in the original `MAIN.EXE` for CD and LANDSoL. Spell routines in the Borland overlays are file offsets into their resolved bodies. The MZ image ends at the `FBOV` header (CD `0x3CC40`, floppy `0x45DA0`). Its +8 field points to the segment directory. Overlay far-call segment words index bytes in that directory, whose entries are eight bytes with the load segment first. A resident overlay stub begins with `CD 3F 00 00`, its +4 dword gives the body offset relative to `FBOV+16`, and its five-byte entries from +0x20 give body entry offsets in their +2 words. This is how the cast calls below were followed into both files.

## Casting

**CONFIRMED** An ordinary cast requires MP ≥ the rank cost and HP > the rank cost, then subtracts both. If property `0x100` is set, a forward wall with flag `0x01` blocks the cast. Paid casts index the far pointers with the **low byte of the spell record's property word**. CD `0x4FE9D–0x5002A`, floppy `0x5A1A2–0x5A32D`.

**CONFIRMED** The direct effect path skips the cost check. CD accepts any negative caster, computes character slot `−caster − 1`, and dispatches by the supplied effect ID. LANDSoL checks specifically for caster −1 and passes slot 0. CD `0x4FF33–0x4FF54`, floppy `0x5A238–0x5A257`. The 17 far-pointer entries start at CD `0x32EF4` and floppy `0x39604`. Slot 7 (Vortex) is zero in each, as are slots 10, 11 and 13–15. The paid spell record at index 9 has low byte 8, whereas a direct request for ID 9 selects Swarm. CD `0x2B6DC` and `0x32F14–0x32F1B`, floppy `0x2CF7C` and `0x39624–0x3962B`. The use of other fields in the index-9 record remains **UNCONFIRMED** beyond the cost and dispatch reads. ScummVM dispatches by the supplied spell index in `engines/kyra/engine/lol.cpp:2093–2124`.

**CONFIRMED** The MP costs below come from the 28-byte records at CD `0x2B5E0` and floppy `0x2CE80`. The four HP costs are zero in each listed row. All spell effects below were traced in both executables. Damage inputs are the arguments to the resistance helper, in rank order. A category selector of `0x80` picks resistance category 7. “Roll” in the table uses the native dice helper and “hit code” refers to the input to damage calculation. CD `0xAFD8–0xB052`, floppy `0xAEFA–0xAF74`.

| Direct ID | MP I–IV | Effect and formula | CD | LANDSoL |
| --- | --- | --- | --- | --- |
| 0 Spark | 5 / 10 / 15 / 25 | Scan up to four blocks forward and use one target in the selected block. Inputs 7 / 15 / 25 / 60, category 5, hit code 2. | `0x4F15B–0x4F19C`, `0x4FBF0–0x4FC2F` | `0x594CB–0x5950C`, `0x59F10–0x59F4F` |
| 1 Heal | 5 / 10 / 25 / 60 | I–III select a character and IV uses all active slots. Cap missing HP at 25 / 45 / 10000 / 10000. III, IV and the above-IV custom amount branch also cure poison. For each healing step, keep the low eight bits of the accumulator, add `(capped missing HP × 256) / 16`, then restore the integer part with a one-point floor and max-HP cap. The healing setter allows a zero-HP target when called with this spell's flag. | `0x4FDF0–0x4FE9C`, `0x43983–0x43ACD`, `0x43BD1–0x43C12`, `0xB34F–0xB39F` | `0x5A0F5–0x5A1A1`, `0x4CD09–0x4CE57`, `0x4CF61–0x4CFA2`, `0xB271–0xB2C1` |
| 2 Freeze | 8 / 15 / 30 / 80 | I–III use 10 / 20 / 30 in the forward block, category 3, hit code 2. IV rolls `4d20 + 10` for each monster and passes its object ID to the resistance helper. On level 11 the branch for the swamp uses durations 20 / 28 / 40 / 60. The native rank-IV target differs from the literal slot 0 passed by ScummVM in `engines/kyra/engine/lol.cpp:2500–2511`. | `0x443B5`, `0x44512–0x44573`, `0x447A0–0x447C4` | `0x4DC03`, `0x4DD43–0x4DDA4`, `0x4DFEE–0x4E012` |
| 3 Fireball | 20 / 35 / 65 / 100 | Checks up to three blocks beginning at the party, firing level script event `0x200` with a temporary type-9 item. A wall matching any low-three flag bits or an occupied block ends the scan. Damage inputs 20 / 40 / 80 / 100, category 4, calculated with hit code 1 and passed to the damage applicator with hit code 2. | `0x41DDE–0x41EEB` | `0x4AE96–0x4AF9C` |
| 4 Hand of Fate | 30 / 60 / 90 / 120 | I–II try to move monsters ahead eight 32-unit steps, subject to a placement test. III–IV use 75 / 125, category selector `0x80`, hit code 1 for the calculation and 2 at application, attacker −1. | `0x43541–0x43683`, `0x43691–0x43703` | `0x4C7EC–0x4C939`, `0x4C93C–0x4C9AE` |
| 5 Mist of Doom | 30 / 60 / 90 / 150 | Forward block, inputs 30 / 70 / 110 / 200, category selector `0x80`, hit code 2. | `0x49A28–0x49A4C` | `0x530E2–0x5310A` |
| 6 Lightning | 25 / 30 / 50 / 100 | Forward block, inputs 18 / 35 / 50 / 72, category 5, hit code 2. | `0x45BF9–0x45C1C` | `0x4F409–0x4F42C` |
| 7 Vortex | 3 / 6 / 12 / 24 | The callback is a null far pointer. | `0x32F10` | `0x39620` |
| 8 Caustic Fog | 15 / 15 / 15 / 15 | Forward block, input 15, category 6, hit code 2, attacker −1. | `0x42921–0x42965` | `0x4BAD1–0x4BB15` |
| 9 Swarm | 15 / 15 / 15 / 15 | Forward block, input 10, category 0, hit code 2. Skip modes ≥13 and definitions with flag `0x2000`. | `0x5002B`, `0x50A30–0x50ACF` | `0x5A32E`, `0x5A8C0–0x5A953` |
| 12 Vaelan's Cube | 0 / 0 / 0 / 0 | In the forward block, clear the four walls when the wall's automap byte is 1 or 2, its flag 1 is clear and the level is other than 22. Deal 100 to monsters with definition flag `0x1000`. Wall 47 on levels 17 and 24 also sets the success flag. | `0x50EDE–0x50FD8` | `0x5AF1E–0x5B018` |
| 16 Guardian | 0 / 0 / 0 / 0 | Forward block, input 200, category selector `0x80`, hit code 2. | `0x431A1–0x431C0` | `0x4C461–0x4C480` |

**CONFIRMED** The common block loop used by Freeze I–III, Mist, Lightning and Guardian stops after an affected target with runtime flag `0x20`, except on level 22 (CD `0x4FC37–0x4FCB3`, floppy `0x59F57–0x59FD3`). Freeze IV has its own loop and stop check (CD `0x44897–0x448B1`, floppy `0x4E06E–0x4E088`).

## Lamp, regeneration and the clock

**CONFIRMED** The oil event decrements oil once if flags 251 and 250, brightness, and oil are all nonzero. The lamp effect is 8 with no oil or brightness. Otherwise let `O = min(oil, 100)` and compute `2 × (3 − floor((O − 1) / 25))`. When only the low indicator bit changes, the next deadline is current tick `+10+1d30`. CD `0xF9DE–0xFA04, 0xFBAF–0xFD0A`, floppy `0x143C6–0x143EC, 0x14578–0x146D3`. For example 25 oil gives 6, 26 oil gives 4, and 100 gives 0 (same instructions).

**CONFIRMED** Palette base factor is `32 × (8 − brightness)`. With a present lamp and effect in [0, 7], replace it by `max(0, 256 − floor(32 × (effect & ~1) × (256 − base) / 256))`. Multiply the first 384 palette component bytes by the factor and divide by 256. CD `0xBF16–0xBFAA`, floppy `0xF7B4–0xF846`.

**CONFIRMED** Regeneration runs on active slots. Alive characters normally gain 1 HP and 1 MP. Item 228 replaces the HP increment with 4, and item 227 replaces the MP increment with `floor(max MP / 10)`. Poison bit `0x80` skips the HP call. The HP setter skips this call on a zero-HP target and caps at max HP. Magic drain selects `−floor(max MP / 32)` in place of the ordinary MP increment even for an active dead slot. Clamp MP to [0, max MP]. CD `0xF848–0xF949, 0xB34F–0xB39F`, floppy `0x14236–0x14337, 0xB271–0xB2C1`.

**CONFIRMED** The original timer arrays start at CD `0x33D68` and floppy `0x3CFF0`. Each 19-byte entry has a far callback at +0, period at +4, initial timing state at +8, callback argument at +12, far clock pointer at +14, and an enable byte at +18. The two monster entries share a callback, start with state 0 and 3, and have arguments 0 and 1.

| Slots | Work | Period in game ticks | CD callback | LANDSoL callback |
| --- | --- | ---: | --- | --- |
| 0 | Doors | 15 | `0xF40A` | `0x13DF8` |
| 1, 2 | Even and odd monster slots | 6 | `0xF3CA` | `0x13DB8` |
| 3 | Character events | 15 | `0xF503` | `0x13EF1` |
| 4 | Flying objects | 1 | `0xF7CB` | `0x141B9` |
| 5–7 | Level script timers, initially disabled | 0 | `0xF832` | `0x14220` |
| 8 | Regeneration | 1200 | `0xF848` | `0x14236` |
| 9 | Portrait animation | 10 | `0xF94A` | `0x14338` |
| 10 | Lamp oil | 360 | `0xF9DE` | `0x143C6` |
| 11 | Text clearing, initially disabled | 360 | `0xFD0B` | `0x146D4` |

**CONFIRMED** Syscall `0x48` adds 5 to the script timer index. The callback adds `0x401` to its argument to get the script entry. CD `0x14BCB`, `0xF832–0xF847`, floppy `0x19552`, `0x14220–0x14235`. A native delay sets its deadline to the current 32-bit counter plus the requested delay, then services the engine until that deadline. The delay reads CD `DS:384C` or floppy `DS:6F0C` (CD `0xC806–0xC82F`, floppy `0x10022–0x1004B`). These addresses differ from the clock used by timer slots 0–10, which is `DS:3858` or `DS:6F14` in the tables.

**UNCONFIRMED** The conversion from these DOS clock counters to wall time is open. The floppy increment at `0x2938C–0x293D5`, deadline loops and clock pointers establish logical ticks. To settle cadence and pause behavior, trace the driver's interrupt period and compare the two counter deltas over 60 interrupts with and without pausing. ScummVM's 16-ms DOS timer unit is documented by `engines/kyra/engine/kyra_v1.cpp:46–50,715–732`.

## Monster transitions

**CONFIRMED** The update returns for modes above 14. Mode flags 0–14 are `1,0,1,3,3,0,0,3,4,1,0,0,4,0,0` (CD `0x33F53`, floppy `0x3D1DD`). Increment the speed counter and compare the old value with the definition's wait byte. Flag 4 bypasses that wait. On update, reset the counter, regenerate `1d8` up to base HP if property flag `0x40` is set, and copy the party location to the destination if runtime flag 8 is set. A successful visibility check for mode flag 2 or a recent hit for mode flag 1 switches to mode 7 before dispatch. CD `0x1275F–0x12874`, floppy `0x170FD–0x17213`.

| Mode | CONFIRMED native path | CD | LANDSoL |
| --- | --- | --- | --- |
| 0, 1 | Shared branch checks the recent-hit flag and visits mode-1 monsters before moving toward the assigned destination. | `0x128B7` → `0x121BC` | `0x17256` → `0x16B5A` |
| 2 | Moves or changes direction toward the assigned destination. | `0x128C2` → `0x1215F` | `0x17261` → `0x16AFD` |
| 3 | Checks party visibility or adjacency for transition to pursuit. | `0x128CD` → `0x12285` | `0x1726C` → `0x16C23` |
| 4 | Stray movement after the pre-dispatch pursuit checks. | `0x128D8` → `0x122D9` | `0x17277` → `0x16C77` |
| 5 | Sets the wake flag and counts down. Aligns while the counter is positive, distance is ≤256 and runtime bit 8 is clear. Otherwise switches to 7. | `0x128E3–0x1294F` | `0x17282–0x172EE` |
| 6 | Counts down without aligning. Switches to 7 when the counter reaches zero or below. | `0x1292C–0x1294F` | `0x172CB–0x172EE` |
| 7 | Tries ranged action before the close-attack or movement path. | `0x12950–0x1296D` | `0x172EF–0x1730C` |
| 8 | Increments the counter, then switches to 5 when it exceeds 2. New counter is `trunc(2048 / speed)` narrowed to a signed byte before multiplying by difficulty modifier 3 and dividing by 256. | `0x1296E–0x129E5` | `0x1730D–0x17384` |
| 9 | Counts down. At zero, clear runtime bit 8 and switch to 7. Otherwise use the close-attack or movement path. | `0x129E6–0x12A17` | `0x17385–0x173B6` |
| 10, 11 | Both use the common display cleanup. Mode 11 also bypasses the shared shift-animation update. | `0x12830–0x1283C, 0x12A30–0x12A67, 0x12A7F–0x12A82` | `0x171CE–0x171DA, 0x173CF–0x17406, 0x1741E–0x17421` |
| 12 | Once the counter passes 13, invokes level event `0x404` with the monster ID. | `0x12879–0x128B6` | `0x17218–0x17255` |
| 13 | Calls death handling once the death counter passes 2. | `0x12A18–0x12A23` → `0x12214–0x12284` | `0x173B7–0x173C2` → `0x16BB2–0x16C22` |
| 14 | Clears the damage display and exits. | `0x12A25–0x12A2F` | `0x173C4–0x173CE` |
| 15 | Used temporarily during the collision query. The existing mode is saved and restored. | `0x1145D–0x114B5` | `0x15EF9–0x15F51` |
| 16 | An inactive slot value. | `0x12766–0x1276E` | `0x17104–0x1710C`, `_LEVEL5.TMP+0x63` |

**CONFIRMED** Spawn HP is `floor(base HP × difficulty modifier 1 / 256)`, then `floor(result × (192 + 1d128) / 256)`, with a floor of 1 HP. CD skips the second multiply for type 2 on level 12. LANDSoL always takes it. For example with normal difficulty, base HP 40 and a roll of 64, the result is 40 in either edition (CD `0x14740–0x147B2`, floppy `0x190D8–0x19139`). The renderer's complete treatment of mode 11 and the script role of mode 10 are **UNCONFIRMED**. The tables and update branch above establish the cleanup behavior. Trace assignments to the mode byte and the frame selector for a placed monster in each mode to label further effects.

## WLL flags and special types

**CONFIRMED** The loader skips the area word, then steps 12 bytes at a time. The six little-endian words give wall ID, VMP, shape, special type, wall flags and automap value. It stores the low bytes of the final three separately. CD `0x47350–0x47421`, floppy `0x50B33–0x50C04`. The WLL flag table in memory is CD `DS:531E` or floppy `DS:87C4`.

| Bit | Native use | CD | LANDSoL |
| --- | --- | --- | --- |
| `0x01` | Blocks ordinary party movement and the gated cast path. The door toggle also uses it to determine whether to attempt closing or opening. | `0xD6B4`, `0x17A4D`, `0x4FEFF–0x4FF1D` | `0x10E3A`, `0x1C078`, `0x5A202–0x5A222` |
| `0x02` | Blocks ranged monster targeting and thrown items. | `0x124CF`, `0x1040B` | `0x16E6D`, `0x14D69` |
| `0x04` | Monster collision. The wall-changing routine checks it before removing monsters of the affected block. | `0x1145D–0x114B5`, `0x1349B` | `0x15EF9–0x15F51`, `0x17E5E` |
| `0x08` | Marks the door side for direction selection and drawing. | `0x17A2F`, `0x3EA36` | `0x1C05A`, `0x47B7C` |
| `0x10` | Fully open door end state. | `0x17AA8–0x17AC3`, mask pair at `0x34319, 0x3431B` | `0x1C0D5–0x1C0EE`, mask pair at `0x3D574, 0x3D576` |
| `0x20` | Fully closed end state. The timer selects a closing sound on this bit, and monsters with definition flag `0x1000` substitute it for their ordinary wall collision mask. | `0xF490`, `0x1147D–0x11489` | `0x13E7E`, `0x15F19–0x15F25` |
| `0x40` | **UNCONFIRMED**. None of the supplied wall records sets the bit. | WLL records loaded at `0x47350` | WLL records loaded at `0x50B33` |
| `0x80` | Draws the block's visible objects in the pass between two wall draws, when the block's render-object list is populated. The renderer also forces the bit for view entry 16. | `0x3E9E8–0x3EA35` | `0x47B2E–0x47B7B` |

**CONFIRMED** The click handler reads the forward wall's special byte. A zero byte skips dispatch. Nonzero values index a far-pointer table. CD `0x1797A–0x179D7`, table at `0x342FC`; floppy `0x1BFA5–0x1C002`, table at `0x3D558`.

| Type | Native click behavior | CD handler | LANDSoL handler |
| --- | --- | --- | --- |
| 0 | No callback. | `0x179AA–0x179B0` | `0x1BFD5–0x1BFDB` |
| 1 | Hit-test the wall shape and run event `0x40` on a hit. | `0x17754` | `0x1BD87` |
| 2 | On a shape hit increment the wall ID, play sound 30 and run event `0x40`. | `0x1779C` | `0x1BDC7` |
| 3 | On a shape hit decrement the wall ID, play sound 29 and run event `0x40`. | `0x177FC` | `0x1BE27` |
| 4 | Run event `0x40` directly. | `0x1785C` | `0x1BE87` |
| 5 | Door switch hit-test, sound 78, event `0x40`, then a 15-tick delay and a toggle if the script leaves it enabled. | `0x17871` | `0x1BE9C` |
| 6 | Niche shape hit-test and placement of the held item at height 8, then clear the held item. | `0x178E1–0x17979` | `0x1BF0C–0x1BFA4` |

**CONFIRMED** Worked example: CD `L01.PAK+0x109E9` and floppy `CHAPTER1.PAK+0xD1E` both record wall 3, special type 5 and flag byte `0xAF`. This is a clickable door switch. Its flags include `0x20` (closed), `0x08` (door side), and the three collision bits. In 29 WLL tables per edition, 1726 wall records per edition use special types 0–6 with frequencies 770 / 448 / 91 / 88 / 7 / 290 / 32. The table comparison begins with this L01 record and includes, for example, type 6 at CD `L04.PAK+0xD930`.

### Follow-up on bit 0x40

**CONFIRMED** The 29 tables in each edition have combined low-byte mask `0xBF` across all 1726 records. The native door-shape loader modifies those bytes with only `OR 0x07`, `AND 0xF8` and `AND 0xFD`. These operations preserve bit `0x40`. Compare CD `MAIN.EXE+0x477B7–0x47826`, LANDSoL `+0x50F96–0x51005`, and upstream `engines/kyra/script/script_lol.cpp:465–493`.

**CONFIRMED** Syscall `0x5A` returns the complete zero-extended WLL byte (CD `0x134F0–0x1352A`, LANDSoL `0x17EB3–0x17EED`). There are four calls in each 60-script corpus. One compares the whole byte to zero, so a hypothetical set bit could affect that test when all other bits are clear. The example calls ask for block 172, face 1 at CD `L08.PAK+0xCAA8` and LANDSoL `CHAPTER2.PAK+0x23687`. The other three call sites apply masks of 0 or 7 in the adjacent instructions (CD `L01.PAK+0xD08F`, `L12.PAK+0xEEFA`, `L13.PAK+0x823C`, LANDSoL `CHAPTER1.PAK+0x58601`, `CHAPTER4.PAK+0x17CC4, +0x18A26`).

**UNCONFIRMED** A dedicated role for bit `0x40` remains open. The follow-up compared the original WLL records, the door flag writes, direct accesses to CD `DS:531E` and floppy `DS:87C4`, and the EMC queries. The direct tests inspected use masks such as collision 7, door state `0x30` and draw flag `0x80` (CD `0xC91C, 0x481AB, 0x3EA1A`, floppy `0x10138, 0x5198B, 0x47B60`). A trace of an isolated WLL copy with only bit `0x40` toggled would test for a hidden pointer-relative consumer. The known whole-byte zero test should be accounted for separately.
