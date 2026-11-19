# Q7 — Spell effects, timers, monster updates and walls in native DOS

**CONFIRMED** offsets name physical bytes in the original `MAIN.EXE` for CD and floppy. Spell routines in the Borland overlays are file offsets into their resolved bodies. The MZ image ends at the `FBOV` header (CD `0x3CC40`, floppy `0x45DA0`). Its +8 field points to the segment directory. Overlay far-call segment words index bytes in that directory, whose entries are eight bytes with the load segment first. A resident overlay stub begins with `CD 3F 00 00`, its +4 dword gives the body offset relative to `FBOV+16`, and its five-byte entries from +0x20 give body entry offsets in their +2 words. This is how the cast calls below were followed into both files.

## Casting

**CONFIRMED** An ordinary cast requires MP ≥ the rank cost and HP > the rank cost, then subtracts both. If property `0x100` is set, a forward wall with flag `0x01` blocks the cast. Paid casts index the far pointers with the **low byte of the spell record's property word**. CD `0x4FE9D–0x5002A`, floppy `0x5A1A2–0x5A32D`.

**CONFIRMED** The direct effect path skips the cost check. CD accepts any negative caster, computes character slot `−caster − 1`, and dispatches by the supplied effect ID. floppy checks specifically for caster −1 and passes slot 0. CD `0x4FF33–0x4FF54`, floppy `0x5A238–0x5A257`. The 17 far-pointer entries start at CD `0x32EF4` and floppy `0x39604`. Slot 7 (Vortex) is zero in each, as are slots 10, 11 and 13–15. The paid spell record at index 9 has low byte 8, whereas a direct request for ID 9 selects Swarm. CD `0x2B6DC` and `0x32F14–0x32F1B`, floppy `0x2CF7C` and `0x39624–0x3962B`. The use of other fields in the index-9 record remains **UNCONFIRMED** beyond the cost and dispatch reads. ScummVM dispatches by the supplied spell index in `engines/kyra/engine/lol.cpp:2093–2124`.

**CONFIRMED** The MP costs below come from the 28-byte records at CD `0x2B5E0` and floppy `0x2CE80`. The four HP costs are zero in each listed row. All spell effects below were traced in both executables. Damage inputs are the arguments to the resistance helper, in rank order. A category selector of `0x80` picks resistance category 7. “Roll” in the table uses the native dice helper and “hit code” refers to the input to damage calculation. CD `0xAFD8–0xB052`, floppy `0xAEFA–0xAF74`.

| Direct ID | MP I–IV | Effect and formula | CD | floppy |
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

### Vortex's item and native call sites

**CONFIRMED** In both editions `ONETIME.INF` configures item type 239 with item script entry 14 and item might 7. Those operands are at CD `STARTUP.PAK+0x230E9–0x230F9` and floppy `GENERAL.PAK+0xDC940–0xDC950`. Item entry 14 reads the type's might field with `getItemPara` selector 11 and gives it to `addSpellToScroll` as the spell ID. The add call is at CD `STARTUP.PAK+0x117E9` and floppy `GENERAL.PAK+0xDA22C`. The native add routines store the supplied ID in the available-spell array (CD `MAIN.EXE+0x4FAC7–0x4FB32`, floppy `+0x59DFD–0x59E61`). Upstream `engines/kyra/script/script_lol.cpp:314–315,1580–1584`, `engines/kyra/engine/lol.cpp:3173–3193`.

**CONFIRMED** The menu reads the selected spell ID from that array, passes it with the caster and rank, and calls the cast routine at CD `MAIN.EXE+0x1092E` or floppy `+0x1526D`. Vortex's 28-byte spell record starts at CD `+0x2B6A4` or floppy `+0x2CF44`. The last two bytes `07 01` select effect slot 7 on the paid path and impose the forward-wall test. The four MP costs are 3, 6, 12 and 24. All four HP costs are zero. Upstream menu reference `engines/kyra/gui/gui_lol.cpp:1092–1115`.

| Casting step for Vortex | CD `MAIN.EXE` | floppy `MAIN.EXE` |
| --- | --- | --- |
| Cost paid on an accepted ordinary cast | `0x4FF57–0x4FFE4` | `0x5A25A–0x5A2E7` |
| Test both words of effect slot 7, containing `00 00 00 00` | `0x4FFF8–0x50000`, slot `0x32F10` | `0x5A2FB–0x5A303`, slot `0x39620` |
| Skip the indirect call and return 1 | Skips `0x50018`, returns at `0x50024–0x5002A` | Skips `0x5A31B`, returns at `0x5A327–0x5A32D` |

**CONFIRMED** An accepted ordinary Vortex cast spends MP and runs no spell effect. The separate no-cost path uses the supplied effect ID directly at CD `0x4FF4D` and floppy `0x5A250`. Its indirect call lacks the paid path's zero-pointer guard. EMC `0xAD` reaches the cast routine at CD `0x16353` and floppy `0x1AC43`. The five `0xAD` calls per edition are in `ITEM.INF`. Four of them pass `-1 - caster` and take the no-cost path; one (CD `STARTUP.PAK+0x11CBB`) passes the caster itself and takes the paid path. None of the five can supply ID 7. Their fixed effects are 4 and 12, and the other three use item attributes. In the startup definitions, the item handlers feeding those three calls supply 3, 5, 6, 9 (entry 20), 4, 5, 9, 16 (entry 24), and 8 (entry 29). For example, entry 20's getter and cast are CD `STARTUP.PAK+0x11A97–0x11AFD` and floppy `GENERAL.PAK+0xDA49E–0xDA4EE`. The corresponding startup definitions span CD `STARTUP.PAK+0x22FD1–0x2302D, +0x234AF–0x23525` and floppy `GENERAL.PAK+0xDC828–0xDC884, +0xDCD06–0xDCD7C`.

**UNCONFIRMED** An ordinary shipped-play route that awards item 239 remains open. The definition and its reading path are present. The corpus check tested literal uses of 239 in the level scripts and found it as a block or rectangle operand, e.g. in CD `L01.PAK+0xD5D7` and floppy `CHAPTER1.PAK+0x58B4D`. To verify reachability, trace native item grants and placements filtered by type 239, including the shop and any computed script arguments.

## Lamp, regeneration and the clock

**CONFIRMED** The oil event decrements oil once if flags 251 and 250, brightness, and oil are all nonzero. The lamp effect is 8 with no oil or brightness. Otherwise let `O = min(oil, 100)` and compute `2 × (3 − floor((O − 1) / 25))`. When only the low indicator bit changes, the next deadline is current tick `+10+1d30`. CD `0xF9DE–0xFA04, 0xFBAF–0xFD0A`, floppy `0x143C6–0x143EC, 0x14578–0x146D3`. For example 25 oil gives 6, 26 oil gives 4, and 100 gives 0 (same instructions).

**CONFIRMED** Palette base factor is `32 × (8 − brightness)`. With a present lamp and effect in [0, 7], replace it by `max(0, 256 − floor(32 × (effect & ~1) × (256 − base) / 256))`. Multiply the first 384 palette component bytes by the factor and divide by 256. CD `0xBF16–0xBFAA`, floppy `0xF7B4–0xF846`.

**CONFIRMED** Regeneration runs on active slots. Alive characters normally gain 1 HP and 1 MP. Item 228 replaces the HP increment with 4, and item 227 replaces the MP increment with `floor(max MP / 10)`. Poison bit `0x80` skips the HP call. The HP setter skips this call on a zero-HP target and caps at max HP. Magic drain selects `−floor(max MP / 32)` in place of the ordinary MP increment even for an active dead slot. Clamp MP to [0, max MP]. CD `0xF848–0xF949, 0xB34F–0xB39F`, floppy `0x14236–0x14337, 0xB271–0xB2C1`.

**CONFIRMED** The original timer arrays start at CD `0x33D68` and floppy `0x3CFF0`. Each 19-byte entry has a far callback at +0, period at +4, initial timing state at +8, callback argument at +12, far clock pointer at +14, and an enable byte at +18. The two monster entries share a callback, start with state 0 and 3, and have arguments 0 and 1.

| Slots | Work | Period in game ticks | CD callback | floppy callback |
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

### Native tick duration and pause

**CONFIRMED** Both DOS sound-driver initializers register the game-clock callback at frequency 60. CD `MAIN.EXE+0x52458–0x5247E` passes offset 2 with overlay segment index `0x458`. That index selects segment `0x2318` from the directory at `0x2FC50`, giving callback file offset `0x26982`. floppy `+0x57E0C–0x57E32` passes offset `0xC` with index `0x2F0`. Its directory at `0x36500` gives segment `0x24B8` and callback `0x2938C`. Frequency 60 is the literal `0x3C` in each registration path.

**CONFIRMED** The driver derives the logical period as integer `1,000,000 / frequency` microseconds, so 60 gives `16,666 μs`. It chooses the shortest registered period for the hardware clock. When that period is `16,666`, the integer PIT divisor is `floor(16666 × 10000 / 8380) = 19887` (`0x4DAF`). The timer setup writes `0x36` to port `0x43` and then the divisor's low and high bytes to port `0x40`. Other registrations can change the hardware interrupt period. The interrupt routine adds the current timer period to each enabled slot's accumulator. When it reaches the slot's period, the routine subtracts that period and calls its registered handler.

| Native evidence | CD `MAIN.EXE` | floppy `MAIN.EXE` |
| --- | --- | --- |
| Integer frequency-to-period conversion and slot write | `0x5679B–0x56853` | `0x26E73–0x26EB2, 0x26CE9–0x26D3C` |
| Pick shortest period | `0x566CA–0x56749` | `0x26A2A–0x26ABD` |
| Convert to divisor and write PIT ports | `0x56654–0x5667C, 0x564D2–0x564F3` | `0x269B6–0x269DE, 0x2698D–0x269B5` |
| Install the IRQ 0 vector and schedule enabled callbacks | `0x56947–0x5698D, 0x1F2FD–0x1F3A0` | `0x2690D–0x26953, 0x26827–0x26893` |
| Advance the game clock counters (CD: counters whose bit is set in `DS:3848` count down, initially `DS:3850`; `DS:384C` and `DS:3858` increment. floppy: `DS:6F18` counts down) | `0x26982–0x269C7` | `0x2938C–0x293D5` |
| Pause and resume the gameplay clock with argument 2 | `0x4C5B3–0x4C5D4, 0x269C8–0x26A49` | `0x5521A–0x55249, 0x24F85–0x24FEC` |

**CONFIRMED** At the nominal 60 ticks per second, 360 ticks of an enabled clock is about 6 seconds, and 1200 is about 20 seconds. The gameplay timer table uses the gated counter, CD `DS:3858` (enable bit 3 of `DS:384A`) or floppy `DS:6F14` (enable bit 1 of `DS:6F1C`). The delay clock is `DS:384C` or `DS:6F0C` and keeps advancing when those gameplay bits are cleared. The CD data image initializes its delay clock's enable bit 0 at `MAIN.EXE+0x3531A`. floppy advances the delay clock unconditionally in the callback. The script pause and resume entry points are `0x9A` and `0x9B` (CD wrappers `0x4D4E0–0x4D4F7`, floppy `0x56078–0x5608F`). ScummVM's DOS engine represents its interval as an integer `16 ms` (`engines/kyra/engine/kyra_v1.cpp:46–50,715–732`).

## Monster transitions

**CONFIRMED** The update returns for modes above 14. Mode flags 0–14 are `1,0,1,3,3,0,0,3,4,1,0,0,4,0,0` (CD `0x33F53`, floppy `0x3D1DD`). Increment the speed counter and compare the old value with the definition's wait byte. Flag 4 bypasses that wait. On update, reset the counter, regenerate `1d8` up to base HP if property flag `0x40` is set, and copy the party location to the destination if runtime flag 8 is set. A successful visibility check for mode flag 2 or a recent hit for mode flag 1 switches to mode 7 before dispatch. CD `0x1275F–0x12874`, floppy `0x170FD–0x17213`.

| Mode | CONFIRMED native path | CD | floppy |
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
| 10, 11 | Both use the common display cleanup. Mode 11 (like mode 14) also bypasses the shared shift-animation update. | `0x12830–0x1283C, 0x12A30–0x12A67, 0x12A7F–0x12A82` | `0x171CE–0x171DA, 0x173CF–0x17406, 0x1741E–0x17421` |
| 12 | Once the counter passes 13, invokes level event `0x404` with the monster ID. | `0x12879–0x128B6` | `0x17218–0x17255` |
| 13 | Calls death handling once the death counter passes 2. | `0x12A18–0x12A23` → `0x12214–0x12284` | `0x173B7–0x173C2` → `0x16BB2–0x16C22` |
| 14 | Clears the damage display and exits. | `0x12A25–0x12A2F` | `0x173C4–0x173CE` |
| 15 | Used temporarily during the collision query. The existing mode is saved and restored. | `0x1145D–0x114B5` | `0x15EF9–0x15F51` |
| 16 | An inactive slot value. | `0x12766–0x1276E` | `0x17104–0x1710C`, `_LEVEL5.TMP+0x63` (a level file the floppy game wrote during play, not shipped) |

**CONFIRMED** Spawn HP is `floor(base HP × difficulty modifier 1 / 256)`, then `floor(result × (192 + 1d128) / 256)`, with a floor of 1 HP. CD skips the second multiply for type 2 on level 12. floppy always takes it. For example with normal difficulty, base HP 40 and a roll of 64, the result is 40 in either edition (CD `0x14740–0x147B2`, floppy `0x190D8–0x19139`).

### Follow-up on modes 9–11

**CONFIRMED** In the walk helper, runtime flag 8 reverses the intended eight-way direction by XORing it with 4 before the movement search. This is the flag cleared by mode 9 on its return to mode 7 (CD `MAIN.EXE+0x1151F–0x1152F, +0x129E6–0x12A17`, floppy `+0x15FBB–0x15FCB, +0x17385–0x173B6`). Upstream `engines/kyra/engine/sprites_lol.cpp:1123–1129,1336–1344`.

**CONFIRMED** Modes 10 and 11 have the same update-table target, the shared cleanup at CD `0x12A30` and floppy `0x173CF`. The mode-10 and mode-11 table words are identical at CD `0x12A7F–0x12A82` and floppy `0x1741E–0x17421`. The earlier update code runs its one-in-four shift update for mode 10 and skips it for modes 11 and 14 (CD `0x12830–0x12860`, floppy `0x171CE–0x171FF`).

**CONFIRMED** The native renderer resolves the animation type from the monster's shape bank, then calls one of four frame selectors (CD `0x3DDEF–0x3DE52`, floppy `0x46F35–0x46F98`). The selected frame is an index within the shape bank. This is how the two modes differ in the four selectors.

| Animation type | Mode 10 result | Mode 11 result | CD / floppy selector |
| --- | --- | --- | --- |
| 0 | Uses the ordinary subframe. Direction flags are added when set. With no direction offset a pending damage display takes frame 12. | Direction offset and damage result take precedence as in mode 10. Otherwise uses fixed frame 14. | `0x3DC34–0x3DCD1` / `0x46D88–0x46E25`. Jump table at `0x3DCD2` / `0x46E26`. |
| 1 | Uses the HP band index 0, 4 or 8. CD calculates the thresholds from difficulty-adjusted base HP. Floppy uses raw base HP. | Fixed frame 12. | `0x3DCE4–0x3DD74` / `0x46E38–0x46EBA` |
| 2 | Uses the fight counter, capped above at 13. | Same counter rule. | `0x3DDD6–0x3DDEE` / `0x46F1C–0x46F34` |
| 3 | Uses the ordinary subframe or frame 5 when showing damage. | Fixed frame 5. | `0x3DD75–0x3DDD5` / `0x46EBB–0x46F1B` |

**CONFIRMED** There are three literal mode-11 assignments in `LEVEL23.INF` in each edition. They find a monster in block 105, 121 or 369, play sounds 88 and 87, then invoke EMC `0x5B` with selector 0 and value 11. The native selector 0 calls the mode setter (CD `MAIN.EXE+0x14FBC–0x14FC6`, floppy `+0x19943–0x1994D`). For example, the state change for block 105 is the call at CD `L23.PAK+0xC2AE` and floppy `CHAPTER6.PAK+0x6AC2D`. The other calls are CD `+0xC2DE, +0xC310` and floppy `+0x6AC5D, +0x6AC8F`.

**UNCONFIRMED** The intended gameplay entry into mode 10 remains open. The native update and frame tables establish what it does once set. The search checked direct immediate accesses to mode byte +0x14 and literal mode inputs to EMC `0x5B` and `0x38` in both 60-script corpora. It found the mode-11 witnesses above, and did not resolve every computed argument. A trace of mode writes in the original, conditioned on new value 10, or a static reconstruction of the computed parameters to those two EMC handlers would settle whether the state is used in shipped gameplay.

**CONFIRMED, probe setup.** The English CD launcher now reaches
play in the documented `MAIN.EXE`. Its native starting slot has
level 1 at `+0x269` (the current-level byte at `DS:7FE5`).
**UNCONFIRMED.** The live level-23 frame. The available native
slot has no level-23 start, and the CD launcher setup did not
provide a level selector. A played level-23 slot near block 105
can drive the original `L23.PAK+0xC2AE` case above. Record the
selector arguments and the eventual frame for the same instance.

## WLL flags and special types

**CONFIRMED** The loader skips the area word, then steps 12 bytes at a time. The six little-endian words give wall ID, VMP, shape, special type, wall flags and automap value. It stores the low bytes of the final three separately. CD `0x47350–0x47421`, floppy `0x50B33–0x50C04`. The WLL flag table in memory is CD `DS:531E` or floppy `DS:87C4`.

| Bit | Native use | CD | floppy |
| --- | --- | --- | --- |
| `0x01` | Blocks ordinary party movement and the gated cast path. The door toggle also uses it to determine whether to attempt closing or opening. | `0xD6B4`, `0x17A4D`, `0x4FEFF–0x4FF1D` | `0x10E3A`, `0x1C078`, `0x5A202–0x5A222` |
| `0x02` | Blocks ranged monster targeting and thrown items. | `0x124CF`, `0x1040B` | `0x16E6D`, `0x14D69` |
| `0x04` | Monster collision. The wall-changing routine checks it before removing monsters of the affected block. | `0x1145D–0x114B5`, `0x1349B` | `0x15EF9–0x15F51`, `0x17E5E` |
| `0x08` | Marks the door side for direction selection and drawing. | `0x17A2F`, `0x3EA36` | `0x1C05A`, `0x47B7C` |
| `0x10` | Fully open door end state. | `0x17AA8–0x17AC3`, mask pair at `0x34318, 0x3431A` | `0x1C0D5–0x1C0EE`, mask pair at `0x3D574, 0x3D576` |
| `0x20` | Fully closed end state. The timer selects a closing sound on this bit, and monsters with definition flag `0x1000` substitute it for their ordinary wall collision mask. | `0xF490`, `0x1147D–0x11489` | `0x13E7E`, `0x15F19–0x15F25` |
| `0x40` | **UNCONFIRMED**. None of the supplied wall records sets the bit. | WLL records loaded at `0x47350` | WLL records loaded at `0x50B33` |
| `0x80` | Draws the block's visible objects in the pass between two wall draws, when the block's render-object list is populated. The renderer also forces the bit for view entry 16. | `0x3E9E8–0x3EA35` | `0x47B2E–0x47B7B` |

**CONFIRMED** The click handler reads the forward wall's special byte. A zero byte skips dispatch. Nonzero values index a far-pointer table. CD `0x1797A–0x179D7`, table at `0x342FC`; floppy `0x1BFA5–0x1C002`, table at `0x3D558`.

| Type | Native click behavior | CD handler | floppy handler |
| --- | --- | --- | --- |
| 0 | No callback. | `0x179AA–0x179B0` | `0x1BFD5–0x1BFDB` |
| 1 | Hit-test the wall shape and run event `0x40` on a hit. | `0x17754` | `0x1BD87` |
| 2 | On a shape hit increment the wall ID, play sound 30 and run event `0x40`. | `0x1779C` | `0x1BDC7` |
| 3 | On a shape hit decrement the wall ID, play sound 29 and run event `0x40`. | `0x177FC` | `0x1BE27` |
| 4 | Run event `0x40` directly. | `0x1785C` | `0x1BE87` |
| 5 | Door switch hit-test, sound 78, event `0x40`, then a 15-tick delay and a toggle if the script leaves it enabled. | `0x17871` | `0x1BE9C` |
| 6 | Niche shape hit-test and placement of the held item at height 8, then clear the held item. | `0x178E1–0x17979` | `0x1BF0C–0x1BFA4` |

**CONFIRMED** CD `L01.PAK+0x109E9` and floppy `CHAPTER1.PAK+0xD1E` both record wall 3, special type 5 and flag byte `0xAF`. This is a clickable door switch. Its flags include `0x20` (closed), `0x08` (door side), and the three collision bits. In 29 WLL tables per edition, 1726 wall records per edition use special types 0–6 with frequencies 770 / 448 / 91 / 88 / 7 / 290 / 32. The table comparison begins with this L01 record and includes, for example, type 6 at CD `L04.PAK+0xD930`.

### Follow-up on bit 0x40

**CONFIRMED** The 29 tables in each edition have combined low-byte mask `0xBF` across all 1726 records. The native door-shape loader modifies those bytes with only `OR 0x07`, `AND 0xF8` and `AND 0xFD`. These operations preserve bit `0x40`. Compare CD `MAIN.EXE+0x477B7–0x47826`, floppy `+0x50F96–0x51005`, and upstream `engines/kyra/script/script_lol.cpp:465–493`.

**CONFIRMED** Syscall `0x5A` returns the complete zero-extended WLL byte (CD `0x134F0–0x1352A`, floppy `0x17EB3–0x17EED`). There are four calls in each 60-script corpus. One compares the whole byte to zero, so a hypothetical set bit could affect that test when all other bits are clear. The example calls ask for block 172, face 1 at CD `L08.PAK+0xCAA8` and floppy `CHAPTER2.PAK+0x23687`. The other three call sites apply masks of 0 or 7 in the adjacent instructions (CD `L01.PAK+0xD08F`, `L12.PAK+0xEEFA`, `L13.PAK+0x823C`, floppy `CHAPTER1.PAK+0x58601`, `CHAPTER4.PAK+0x17CC4, +0x18A26`).

**UNCONFIRMED** A dedicated role for bit `0x40` remains open. The follow-up compared the original WLL records, the door flag writes, direct accesses to CD `DS:531E` and floppy `DS:87C4`, and the EMC queries. The direct tests inspected use masks such as collision 7, door state `0x30` and draw flag `0x80` (CD `0xC91C, 0x481AB, 0x3EA1A`, floppy `0x10138, 0x5198B, 0x47B60`). A trace of an isolated WLL copy with only bit `0x40` toggled would test for a hidden pointer-relative consumer. The known whole-byte zero test should be accounted for separately.

**CONFIRMED, level-1 runtime control.** English CD 1.02 reached
level 1 through the [installed launcher](../NEEDS_A_RUNNING_GAME.md#working-launch-for-the-english-dos-cd).
The resident getter at `MAIN.EXE+0x134F0` matched guest linear
`0x11710` (load segment `01A2`). With game `DS=2FCF`, the bytes
at `DS:531E + id` for all 52 original `LEVEL1.WLL` records matched
the shipped flags after a forward/turn/click sequence. The before and
after reads of the 256-byte table had the same counts for each byte
value, and the first 16 bytes matched in order. The declared IDs range
from 0 to 79, and every declared flag had bit `0x40` clear after the
sequence. Wall 3 stayed `0xAF` (record at `L01.PAK+0x109E9`, flag at record +8,
`+0x109F1`).
**UNCONFIRMED:** the proposed level-8
block-172 contrast still needs a native level-8 starting state.

### Additional wall consumers in both editions

**CONFIRMED** The ordinary click table uses resident far pointers. CD `MAIN.EXE+0x342FC` starts with null slot 0 and six consecutive entries at segment `0x13E8`. floppy `+0x3D558` uses segment `0x174B` for the same six slots. Type 1 has one edition difference after the hit test. CD calls `0x154C:0x000F` with 1 before forwarding event `0x40` (CD `+0x1777B–0x1778F`). floppy calls the event immediately (floppy `+0x1BDAE–0x1BDBA`).

**CONFIRMED** The monster movement search can act on a closed type-5 wall without using the click handler. It requires wall bit `0x20` and special type 5, then calls the door-frame helper with selector 1. The helper reads the mask from CD `+0x3431A` or floppy `+0x3D576`. The calling conditions are at CD `+0x115C4–0x115E6` and floppy `+0x16060–0x16082`. The helpers start at CD `+0x17A69` and floppy `+0x1C094`.

**CONFIRMED** Bit `0x80` also qualifies the separate held-item placement branch. The wall must have `0x80` set and `0x02` clear before the branch computes placement coordinates and invokes the item-placement routine. CD `MAIN.EXE+0x10AFC–0x10B6F`, floppy `+0x15440–0x154B3`. The click type and this flag test are separate decisions, as seen in the far call at CD `+0x179C1` and floppy `+0x1BFEC`.

**CONFIRMED** The generic native collision helper takes a caller-provided mask. Given a specific side it tests the opposite wall. With side `-1` it tests all four walls. Its three resident far-call sites pass mask 1 for party movement, 0 for the nearby-block search, and the caller's stack parameter for the all-sides collision test. CD `+0xC947–0xC9AD, +0xD6AE, +0xA362, +0x11159`, floppy `+0x10163–0x101C9, +0x10E34, +0xA3BA, +0x15BF5`. Both fixed door masks are `0x10` or `0x20`, and the script getter still exposes the entire wall byte.

**CONFIRMED** The all-sides mask chain bottoms out in two
resident callers in each edition. The movement wrapper passes its
word argument at BP+0x0E to all six calls to the side helper
(CD `+0x1122C–0x11239, +0x11297–0x112A4, +0x112F6–0x11303,
+0x11364–0x11371, +0x113CC–0x113D9, +0x1141C–0x11429`;
floppy supplies the same argument through the six sites in
`+0x15CC8–0x15EC5`). The side helper pushes this value at
`+0x11159` / `+0x15BF5`. Monster placement supplies fixed
mask 7 (CD `+0x14688–0x14695`, floppy `+0x19020–0x1902D`).
Flying-object movement supplies record byte +0x10 (CD
`+0xF34B–0xF37E`, floppy `+0x13D39–0x13D6C`), which its
17-byte record constructor sets to 2 (CD `+0xF274–0xF2DC`,
floppy `+0x13C62–0x13CCA`). The nearby mask selection
0x3F/0x100 is a different argument (CD `+0xF367–0xF377`,
floppy `+0x13D55–0x13D65`). Party movement and the
nearby-block search continue to pass the fixed masks 1 and 0.

**UNCONFIRMED** The recovered collision callers supply only
0, 1, 2 and 7. No dedicated consumer of 0x40 was found in the
literal wall-table search, and the supplied WLL records leave it
clear. To detect an indirect consumer, compare otherwise identical
wall bytes 0 and 0x40 on the level-8 block-172 face-1 witness.
An original runtime trace would record the instruction and input
mask at each access to that wall-table byte and separate the known
whole-byte EMC test from masked native checks. The watched bases
are CD DS:531E and floppy DS:87C4, each plus the wall ID.

### Additional mode branches

| Mode | CONFIRMED control flow | CD MAIN.EXE | Floppy MAIN.EXE |
|---|---|---|---|
| 0/1 | With instance +0x19 bit 4 set, scan 30 slots and request mode 7 for every slot in mode 1. With bit 4 clear, only mode 1 enters the destination helper. | `0x121C3–0x1220B` | `0x16B61–0x16BA9` |
| 2 | Compare both current coordinate words to the destination. If either differs, call the movement helper. When both match and +0x17 differs from +0x10, select the facing through the table at DS:241A (CD) or DS:5914 (floppy). | `0x12165–0x121B4` | `0x16B03–0x16B52` |
| 3 | Request mode 7 on the visibility test and independently on an adjacent-block party match. The adjacency loop checks four indices. | `0x12291–0x122D4` | `0x16C2F–0x16C72` |
| 4 | At zero counter, align to an even direction, test a step, and move if it is free. When it is blocked, use a sampled turn to change direction and load the counter. With a nonzero counter, rotate through candidate directions. Seven failed probes request mode 3. | `0x122E4–0x12365`, `0x12368–0x12421` | `0x16C82–0x16D03`, `0x16D06–0x16DBF` |
| 12 | Increment +0x15 and mark the current block. Only a counter above 13 calls the level event, using the monster ID in both stacked ID fields. | `0x12879–0x128B4` | `0x17218–0x17253` |
| 13/14 | Mode 13 increments +0x15, marks its block and, above 2, calls the death finalizer. The finalizer requests mode 14, marks the block and tests definition +0x3E bit 12 before setting block bit 7 on the eligible branch. The mode-14 update only clears +0x1B. | `0x1221A–0x1223B`, `0xAEBA–0xAF13`, `0x12A25–0x12A2E` | `0x16BB8–0x16BD9`, `0xADDC–0xAE35`, `0x173C4–0x173CD` |

**CONFIRMED** The whole-program byte scan finds 13 near calls to
the mode setter in each edition (target CD `0x11855`, floppy
`0x162F1`) and seven/eight far encodings respectively. The far entry
used by the script is CD `0x14FC1`, floppy `0x19948`. The scan
finds no literal ES:disp8 byte store of 10 at displacement +0x14
in either complete tested image. It corroborates the earlier
mode-10 search over the shipped scripts.

**UNCONFIRMED** The gameplay producer for mode 10. The measured
scope includes the direct setter encodings and the literal store
form. It leaves indirect calls and computed setter arguments open.
A watch on the mode setter's incoming argument equal to 10, or
the final +0x14 write at CD `0x118FA` or floppy `0x16396`,
would settle the producer.
