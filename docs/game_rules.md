# LoL1 game rules

[Executable tables and offsets](executable_tables.md) · [EMC2 functions](emc2_scripts.md) · [Save-state fields](savegame_format.md) · [Native spell, timer, monster and WLL rules](unknowns/07_native_rules.md)

**CONFIRMED** marks original CD or LANDSoL bytes and instructions checked directly. **UNCONFIRMED** marks a rule whose expression is documented in the reference implementation but whose native behavior still needs a direct check. References use ScummVM revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`. CD executable addresses below refer to `DATA/HARDRIVE/MAIN.EXE`; floppy addresses refer to LANDSoL `MAIN.EXE`.

| Source shorthand | ScummVM file |
| --- | --- |
| LoL | `engines/kyra/engine/lol.cpp` |
| Sprites | `engines/kyra/engine/sprites_lol.cpp` |
| Scene | `engines/kyra/engine/scene_lol.cpp` |
| Timers | `engines/kyra/engine/timer_lol.cpp` |
| GUI | `engines/kyra/gui/gui_lol.cpp` |
| Script | `engines/kyra/script/script_lol.cpp` |
| Items | `engines/kyra/engine/items_lol.cpp` |

**CONFIRMED** `n d s` means roll `n` dice with `s` sides and add the results. In native DOS each die takes a 15-bit pseudo-random sample `U`, forms `1 + floor(U × s / 32768)`, and wraps once by subtracting `s` if the result exceeds it. The native sum is zero for nonpositive dice or sides. CD `MAIN.EXE+0x426A–0x428F, +0xC286–0xC2DB`; floppy `MAIN.EXE+0x526A–0x528F, +0xFAE0–0xFB35`. The ScummVM helper uses its own bounded RNG and optional additive constant (`engines/kyra/engine/kyra_rpg.cpp:386–395`). Fixed-point products `a × b / 256` discard the remainder at each step (CD `+0x1EC10`, floppy `+0x1F646`).

## Combat

### Attack and hit test

- **CONFIRMED** Standard unarmed item entry 3 uses hit test → maximum damage → two-dice damage syscall → apply damage. The hit code from syscall `0x40` gates the following calls and is passed through to the damage calculation. Both item scripts have these calls at DATA words `0x233, 0x23F, 0x244, 0x24D` (CD `STARTUP.PAK+0x1122D, +0x11245, +0x1124F, +0x11261`; floppy `GENERAL.PAK+0xD9D34, +0xD9D4C, +0xD9D56, +0xD9D68`). In the reference, the combat button dispatches item and level event `0x400` for each filled combat slot 0–3, decreasing an auxiliary argument by 10 after each weapon. With no occupied combat slot it dispatches entry 3 through item 0. Items:290–310, GUI:1030–1058, Script:980–995,1447–1456.
- **CONFIRMED** For a character attacker, the hit factor is default modifier 0. The critical threshold is `100 − (skill level + skill modifier)`; triple the modifier for Rogue first. A monster attacker instead supplies its own hit stat 0 and its own property skill level, with critical threshold `100 − monster skill level`. CD `MAIN.EXE+0xAD4D–0xAE04`, floppy `+0xAC8E–0xAD45`. The ScummVM monster-attacker branch reads the target-indexed slot here (LoL:3455–3457).
- **CONFIRMED** The defender's evade is character default modifier 3 or monster fighting stat 3. In native CD both target types use `evade × modifier 4 / 256` before the comparison. The difficulty row is `[128, 256, 256]` for easy/normal/hard. Native floppy passes the raw evade value. Compute `evade threshold = (evade × 256) / hit factor` with the adjusted or raw value for that edition. CD `MAIN.EXE+0xAE04–0xAEB4, +0x2B86E`, floppy `+0xAD45–0xADD6`. ScummVM scales the evade value only for a monster target (LoL:3466–3482).
- **CONFIRMED** Roll `1d100` once. A roll at or above the critical threshold returns 2 and bypasses the evade comparison. Of the remaining rolls, those below the evade threshold return 0 (miss), and all others return 1. An absent target returns 0. Sentinel attacker −1 returns 1 before the monster validity check. A monster target in mode 13 or higher gives 0 for other attackers. CD `MAIN.EXE+0xAD0A–0xAD4D, +0xAE52–0xAEB9`; floppy `+0xAC4B–0xAC8E, +0xAD93–0xADDB`; LoL:3440–3484.

### Might, armour and damage

| Rule | Formula and evidence |
| --- | --- |
| Displayed character might | **UNCONFIRMED** Sum eight item-might categories. If the sum is positive, add character base might. For a zero sum use default modifier 8. Multiply by default modifier 1 and divide by 256, then multiply by total might modifier and divide by 256. LoL:1405–1419. |
| Character armour | **CONFIRMED** Add item protection and base protection. Multiply by default modifier 2 and divide by 256. Multiply that integer result by total protection modifier and divide by 256 again. CD `MAIN.EXE+0xA8D7–0xA927, +0xA94F–0xA95E`; LoL:1439–1452. |
| Monster armour | **CONFIRMED** Multiply the monster's item protection by its protection factor (fighting stat 2) and divide by 256. The script supplies the factor as `protection percentage × 256 / 100`. CD `MAIN.EXE+0xA928–0xA95E`; LoL:1439–1452, Script:941–957. |
| One damage category | **CONFIRMED** Start with `item might × attacker factor / 256`. The factor is character default modifier 1, monster fighting stat 1, or 256 for attacker −1. Characters multiply again by total might modifier and divide by 256. Zero at either stage returns 0. CD `MAIN.EXE+0xAF63–0xAFD6`, floppy `MAIN.EXE+0xAE85–0xAEF8`; LoL:2060–2070,3635–3647. |
| Target category factor | **CONFIRMED** Multiply by the magnitude of the target's category factor, divide by 256, then restore the sign of that factor. Index bit 7 selects category 7. Native helpers treat the factor word as signed. ScummVM's literal load from a `uint16` array promotes to a nonnegative integer in this revision. CD `MAIN.EXE+0xAFD8–0xAFFF, +0x1EBED–0x1EC0F`; floppy `MAIN.EXE+0xAEFA–0xAF21, +0x1F624–0x1F645`; LoL:2068–2070,3649–3654. |
| Armour reduction | **CONFIRMED** For nonzero damage and hit code other than 2, divide `protection × 128` by pre-armour damage, cap the result above at 217, and subtract it from 256. Multiply damage by the resulting factor and divide by 256. Raise any result below 2 to 2 in that branch. For hit code 2, skip armour and turn damage 1 into 2. Zero stays zero. CD `MAIN.EXE+0xB001–0xB052`; floppy `MAIN.EXE+0xAF23–0xAF74`; LoL:3653–3658. |
| Total and dice | **CONFIRMED** Sum the terms for all eight item categories, starting at zero. The item syscall rolls `2 d sum`, so a positive sum gives damage from 2 through twice the sum. In the reference monster melee uses the same sequence. CD `MAIN.EXE+0xB053–0xB0B4`, floppy `+0xAF75–0xAFD6`; LoL:3487–3497, Script:1447–1456, Sprites:1291–1304. |
| Applying damage | **UNCONFIRMED** Subtract positive damage from HP. Monster HP is clipped between zero and base HP, with death mode 13 at zero. Negative damage uses a healing branch with a one-point floor. Party HP is clipped to current maximum by the setter, and zero marks death. Damage with flag value 4 is divided by four for a target wearing item 229 (Cloud Ring). LoL:1465–1483,3500–3588. |

**UNCONFIRMED** After a monster melee hit, the attack special succeeds on `1d100 ≤ attack chance` before the type-specific branch. Matching types can steal or destroy equipment, poison or stun, drain current MP into monster HP, heal for inflicted damage or paralyze the party. A damaged monster's defense special uses a separate `1d100 ≤ defense chance` check and the attack's flags. Its branches include equipment loss, 30-update panic, recovery of damage taken, and additional ranged attacks. Script:969–972, LoL:3711–3848, Sprites:1297–1304.

## Magic

**CONFIRMED** The 17 spell records agree across the two CD images and the floppy. Rows 0–9 have four MP amounts per rank plus four HP amounts; all populated rows have zero HP costs in all four columns. Native records at CD `MAIN.EXE+0x2B5E0` and floppy `MAIN.EXE+0x2CE80`; `devtools/create_kyradat/resources/lol_dos_cd.h:501–521` and `lol_dos.h:453–473`. English labels come from the original `LANDS.ENG` lookup words at CD `STARTUP.PAK+0x8B50–0x8B5F, +0x8F86` and floppy `GENERAL.PAK+0xD4F9F–0xD4FAE, +0xD53D5` (LoL:1066–1104).

**CONFIRMED** Ordinary casts require MP ≥ cost and HP > cost, then dispatch by the low byte of the spell property word. The direct effect path skips payment. CD decodes a negative caster as slot `−ID − 1`, and LANDSoL recognizes −1 and uses slot 0. Vortex has a cost record and a null effect pointer. See the [native spell effect table](unknowns/07_native_rules.md#casting) for each rank's effects, damage inputs and the executable offsets.

## Experience and skills

| Rule | Formula and source |
| --- | --- |
| Stored skill and display | **UNCONFIRMED** Fighter, Rogue and Mage use slots 0, 1 and 2. Display level is base level plus modifier. The general skill check chooses the active slot with the highest level plus modifier plus 25, keeping the earliest on ties, then requires `1d100 ≤ that sum`. LoL:1405–1434, Script:1368–1384. |
| Thresholds | **CONFIRMED** The native indexed thresholds are 0, 500, 1500, 5000, 25000, 50000, 80000, 120000, 180000, 270000, 2147483647. CD `MAIN.EXE+0x2B830`, floppy `+0x324F0`. **CONFIRMED** Both native editions add to the 32-bit running total and repeat the advancement callback while it returns nonzero. They skip monsters and characters with dead flag 8. CD `MAIN.EXE+0xA98F–0xA9E9`, floppy `+0xA8CB–0xA925`. **UNCONFIRMED** The reference advancement increments base level while total ≥ the threshold at the current level and retains the total. LoL:1532–1550. |
| Award values | **CONFIRMED** Native CD awards the inflicted amount to the supplied skill, plus the monster’s base HP on a kill by a player. For Fighter damage, its weapon-hit display accumulates the amount. The reference assigns the amount to the display field. CD `MAIN.EXE+0xB247–0xB25C, +0xB331–0xB346`. **UNCONFIRMED** In ScummVM a launched player projectile grants 2 Rogue XP. A successful GUI cast grants `rank index²` Mage XP (0, 1, 4, 9) plus any XP delivered by the effect. LoL:3525–3533,3574–3580, Items:417–436, GUI:1092–1111. |
| Level-up gains | **UNCONFIRMED** Fighter adds `4d6` to current and max HP, Rogue adds `2d6`, Mage adds `1d6` HP and `(1d8 + 17) × default modifier 6 / 256` to current and max MP. The level-up flag is `0x200 << skill`. LoL:1546–1581. |
| Attack recovery | **UNCONFIRMED** Let `Q = 256 × base interval / speed factor` (modifier/stat 4). For players at Rogue levels 4–7, subtract `Q / 4`; at 8+, subtract `Q / 2`. Base interval 8 is used for the GUI attack. If a weapon-hit number exists, wait four character updates, then clear it and wait a second interval with base 6. Otherwise initial wait is `Q + 4`. Item 230 (Zephyr Ring) halves the initial wait. Successful menu casting uses eight updates. Sprites:478–491, GUI:1060–1069,1105–1107, Timers:71–83. |

## Monster behavior

The [native monster update](unknowns/07_native_rules.md#monster-transitions) documents the 0–16 transitions, position and speed checks, and the edition difference in spawn HP on level 12.

- **UNCONFIRMED** In ScummVM, movement steps add 32 along each applicable axis and wrap to 13 bits. Ranged scans require a clear cardinal line, facing toward the target, within four blocks. A ranged attack uses one charge unless charges are 255, and sets its next counter to `speed stat × 8 / 256`. Melee uses forward distance at most 160 and absolute lateral distance at most 80, with matching facing and direction. Sprites:1205–1313,1381–1415,1428–1434.
- **CONFIRMED** Difficulty rows 1–3 in easy/normal/hard order are `[102,256,384]` CD or `[192,256,384]` floppy for row 1, `[256,256,192]` for row 2, and `[320,256,128]` for row 3 in both. Native CD `MAIN.EXE+0x2B85C`, floppy `+0x3251C`. **UNCONFIRMED** ScummVM uses them for initial HP, monster speed-based intervals and post-melee recovery, respectively. Restoring a level under different difficulty scales existing live HP by `old modifier / new modifier`, adds one if the new difficulty index is lower, and clamps zero to one. Sprites:478–483,1114–1119, `engines/kyra/gui/saveload_lol.cpp:547–561`.

## Light and time

| Rule | Formula and source |
| --- | --- |
| Oil, light, regular updates and passive regeneration | **CONFIRMED** Both executables contain the same timer periods, oil depletion, lamp band and flicker formulas, palette scaling and character regeneration. See the [native timer and formula tables](unknowns/07_native_rules.md#lamp-regeneration-and-the-clock) for offsets and examples. |
| Oil refill | **UNCONFIRMED** In ScummVM item type 248 adds 100 oil if the previous value is below 100. GUI:1802–1826. |
| Tick duration | **CONFIRMED** Both DOS versions schedule the game clock at 60 callbacks per second. Gameplay pause stops the timer-table clock. The delay clock continues. See the [native frequency and pause trace](unknowns/07_native_rules.md#native-tick-duration-and-pause). ScummVM's DOS port uses `floor(1000 / 60) = 16 ms` per tick and accumulates one second on its play clock per 1000 elapsed milliseconds. `engines/kyra/engine/kyra_v1.cpp:46–50,715–732`, LoL:929–971. |
| Poison and paralysis | **UNCONFIRMED** Ordinary poison attempts `1d2` damage per 10 character-event updates once inflicted. Item 225 blocks poison application. Paralysis sets the delay from literal 3600 in the reference, and stun from 20. The serialized delay elements are bytes, so 3600 narrows to 16 at assignment in this build. The raw configured delay and the effective stored delay are distinct. LoL:1248–1259,3865–3890,3909–3918, Timers:55–107, `engines/kyra/engine/lol.h:77–78`. |
| Resting | **UNCONFIRMED** Among active living party members let H be the largest max HP, M the largest max MP, and A the largest current HP among poisoned members. Every `min(30, 600 / H)` ticks heal an eligible member 1 HP, every `min(30, 600 / M)` ticks restore 1 MP, and every `min(15, 600 / A)` ticks deal 1 poison damage to poisoned members. The last interval is relevant when there are poisoned members. Counters apply to each eligible member on that deadline. Rest continues until no healing or MP gain is pending or input/AI wakes the party. GUI:1568–1710. |
