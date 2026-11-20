# How the three games gate progress and scale numbers

For the shared file formats, see [what the three games share](series-formats.md). For how the programs load levels, run scripts and save, see [how the engine changed](engine-evolution.md).

This page lines up how each game moves the player from level to level, how it guards those moves, and how it turns stored numbers into play values. Every sentence only restates what the linked page establishes, with its evidence. "Open" means the linked page marks it as not settled.

## Gating progress

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| What moves the player | EMC2 function 0x3C `loadNewLevel` (level, block, facing), 71 static call sites in each edition ([functions](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/emc2_scripts.md#lol1-system-functions), [progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#level-to-level)) | an opcode-2 command starting `02 01 00 00 1c`; byte 5 holds the level and the arrival entry ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)) | an opcode-2 command with subcommand 27 or 76; byte +5 holds the level row and the entry ([portal subcommands](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-opcodes.md#portal-subcommands-of-opcode-0x02)) |
| How a guard is written | the `ifNotJmp` tests still open on a path from a script entry to the call, outermost first, with the arm taken; the path follows jumps, both arms of `ifNotJmp` and calls ([progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md)) | a kind-19 trailer after the event record names a 5-byte predicate row ([event records](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-script-events.md#event-records)) | a kind-19 row after the event record names a 5-byte predicate row at MAP +0xBC ([predicates](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-events.md#predicates-and-global-bytes)) |
| Which matching record runs | no record list; a call site runs when an entry that reaches it runs and the `ifNotJmp` tests on its path pass ([progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md)) | every matching record, in list order; the later exit wins ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)) | only the first matching row whose guard passes ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)) |
| What exit guards test | flags, the hand item's type or shape, facing, a party member, credits, items, and `computed` for any other test ([progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md)) | shared bytes, level bytes and object byte +0x25 ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)) | shared bytes and object byte +0x31; no item or equipment test ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)) |
| Exit commands | 71 `loadNewLevel` call sites and 136 door calls ([progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#level-to-level)) | 72, 24 with a predicate ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)) | 131, 82 with a predicate ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)) |
| Levels with no exit | none; every level has a constant edge out; the graph is not a play trace ([graph](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#graph)) | none ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)) | SWOD4 ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)) |

### LoL1

EMC2 function 0x3C `loadNewLevel` takes a level, a block and a facing. The door functions sit in the same table: 0x18 `loadDoorShapes`, 0x31 `triggerDoorSwitch`, 0x33 `setDoorState` and 0x86 `blockDoor`. The call counts are measured. All five handlers have been read in the original program and agree with the names ([functions](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/emc2_scripts.md#lol1-system-functions), [native handlers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/emc2_native_handlers.md)).

The CD `LEVEL<n>.INF` and `.INI` scripts hold 71 `loadNewLevel` call sites and 136 door calls. A row's entries are the script entries whose call graph reaches the call, through jumps, both arms of `ifNotJmp` and calls; a return ends the path. Its conditions are the `ifNotJmp` tests still open on that path, outermost first, with the arm taken, so `flag 41 == 0` means that arm of the compare. `hand item type` and `hand item shape` are `getItemPara` selectors 4 and 8 on the item in hand, read from the selector jump table of the CD handler. `computed` is a test that is not a flag, an item, a party member, credits, a hand-item type or shape, or facing ([progression](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md), [level to level](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#level-to-level), [door calls](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#door-calls)).

Constant destinations from the reached sites leave every level on a path from level 1, and every level has an edge out. This graph is not a play trace, and no level is marked unreachable or a dead end from these sites alone ([graph](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#graph)).

Open: where the walk stopped following an entry at its loop limit, the entry, argument and condition cells can be incomplete ([walk limit](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/PROGRESSION.md#walk-limit)).

### LoL2

A level-transition command stores the destination level in the low 5 bits of byte 5 and the arrival entry in the high 3 bits. The 15 level archives hold 72 such commands, and 24 of the records that run them carry a kind-19 predicate ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md), [exit census](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-shared-predicates.md#exit-predicate-census)).

After a record matches, the walker checks whether the next record is kind 19 and, if so, evaluates the predicate it names ([event records](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-script-events.md#event-records)). A predicate row has an operator (equal, unequal, ≤, ≥, >, <, AND, OR) and two operands. An operand is a literal, a shared byte, a level byte, another predicate row, or the object byte +0x25 ([predicates](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-script-events.md#predicates-and-shared-bytes)).

Every matcher an exit uses runs all matching records in list order. Each guard is checked after earlier matching groups in the same walk have run. When two exits fire, the later one wins, because the exit only stores the pending level ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md)).

The exit guards name shared slot 52 (2 rows) and local slots 2 (9), 11 (1), 13 (1), 22 (1) and 55 (8). 10 rows are selectors: pairs from one record to one level that test one slot for 0 and for 1, so the slot picks the arrival and does not close the way ([progression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md#what-a-row-does-not-show)).

Every level has an exit command. No exit command leads to L1_DC. The level table counts command bytes and their records only; whether the player can reach each record is not part of it ([level to level](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md#level-to-level), [exit graph](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-level-graph.md#exit-graph-decoded)).

Open: 8 rows hang on object records, and what sends their events is not traced, so `none` on those rows does not mean the exit is free. The sender of region event 4, used by one row, is also open ([what a row does not show](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/PROGRESSION.md#what-a-row-does-not-show)).

### LoL3

The portal arm stores `(byte +5 & 31) + 2` as the level row and `byte +5 >> 5`, plus 8 for subcommand 76, as the second value. The 18 MAP scripts hold 131 portal commands: 125 with subcommand 27 and 6 with subcommand 76. A startup with no saved index loads row 17, QWOD0 ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md), [portal subcommands](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-opcodes.md#portal-subcommands-of-opcode-0x02)).

A walker runs only the first row of its list that matches and whose guard passes, then returns. So a row's real gate is its own guard together with NOT the guard of each earlier row the walker can take first ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)).

A guard index below 5000 selects a 5-byte predicate row. Its operands can be a literal, a shared byte, a level byte, another predicate row or the object byte +0x31. Indexes from 5000 up test an item key held (5000+n), an equipped item (6000+n) or a slot level (7000, 7100, 7200, 7300+n) ([predicates](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-events.md#predicates-and-global-bytes)). Every portal guard is a row below 5000, so none tests an item key or an equipped item ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md)).

82 of the 131 portal commands have a predicate. 49 rows have an earlier row the walker tries first. The guards name shared slots 9 (81), 10 (2) and 14 (2), and object+0x31 (7). SWOD4 has no portal command. 18 of 18 levels are reached from QWOD0 along all portal edges, and 14 along guarded edges only ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md), [level to level](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md#level-to-level)).

Open: 46 rows have no guard and no earlier row, so their gate is whatever sends their event. Whether all gates along a chain of steps can pass in one game is also open ([progression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md), [level to level](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/PROGRESSION.md#level-to-level)).

## Scaling numbers

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Experience table | 11 cumulative thresholds ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#experience-by-current-skill-level)) | — | — |
| Spell cost rows | 17 records of 28 bytes ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#spell-costs-by-rank)) | 113 effect records ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#cast-schools-and-effect-costs)) | 28 spell effect records of 87 bytes ([numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#spell-effects)) |
| Item rows | 285 ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#item-might-and-armour)) | 170 of 91 bytes ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#item-combat-inputs)) | 343 of 139 bytes ([numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#item-definitions)) |
| Creature rows | 79 definition calls ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#creature-definitions-by-level)) | 128 definitions of 147 bytes ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#creature-numbers-by-level)) | 334 rows of 147 bytes ([numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#creature-definitions-by-level-field-3-type-rows-not-placements-a-few-tags-are-objects)) |
| Creature health | base HP, scaled by difficulty and a random factor at spawn | definition +0x63, a health cap | definition +0x63, copied to the health ceiling |
| Creature attack input | eight might values by category | byte +0x81, with `max(1, B/10)` | byte +0x81, halved for +0xFA |

A dash means the numbers page lists no such table.

### Experience and levels

**LoL1.** The thresholds are 0, 500, 1500, 5000, 25000, 50000, 80000, 120000, 180000, 270000 and 2147483647. The program compares the threshold at the current level with the 32-bit total. When the total reaches it, the base level goes up by one and the check repeats; the total is kept. A level-up adds `4d6` HP for slot 0, `2d6` for slot 1, and `1d6` HP plus `(1d8 + 17) × modifier 6 / 256` MP for slot 2. Awards are the damage dealt plus the monster's base HP on a kill (CD), 2 for a projectile, and `rank index²` for a menu cast ([experience](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/game_rules.md#experience-and-skills), [numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#experience-by-current-skill-level)).

**LoL2.** Spell damage feedback takes a base from effect byte +1 and triples it when the damage is above 1. The award then depends on the hit's scale minus the skill byte: 0 below −3, the base at 0, and up to `2*v + v/2` above 4 ([hit requests and experience](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-spells.md#hit-requests-and-experience)).

**LoL3.** The numbers page lists no experience table. A guard index of 7000, 7100, 7200 or 7300+n tests whether slot 0–3 has its flag set and a level above n ([predicates](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-events.md#predicates-and-global-bytes)).

### Spell costs

**LoL1.** Each record has four MP words at +0x02 and four HP words at +0x0E, one per rank. All populated rows have zero HP costs. An ordinary cast needs MP ≥ the cost and HP > the cost ([magic](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/game_rules.md#magic), [casting](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/unknowns/07_native_rules.md#casting)).

**LoL2.** The 113 records are 64 costed levels in schools 0–12 and 49 zero-cost records in rows 13–14. A school row gives its first effect, and the charge is added to it. Byte +0 is the stored cost and +1 the experience input. Form 2 halves the debit. Whether the school's +1 byte bounds the charge in general is open ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#cast-schools-and-effect-costs), [cast tables](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-spells.md#cast-tables-and-resource-costs)).

**LoL3.** The cost of a special item definition is its dword +0x5B. With items 0x128, 0xD8, 0xDC and 0xDB all equipped, spell IDs 0x82–0x86 cost half. With item 0xE9 equipped, spell IDs 0x50–0x54 cost `trunc(cost/4)` less. A first hit reads one signed magnitude per variant: 10, 20, 40, 80, 10, 0, 10, 10, 60 ([player cast and cost](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-spell-dispatch.md#player-cast-and-cost), [numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#spell-effects)).

### Item stats

**LoL1.** Each item has signed might and unsigned protection. Damage sums eight might categories and rolls `2 d sum`, so a positive sum gives 2 to twice the sum. Armour removes at most 217/256 of the damage, and a hit that gets through does at least 2 ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#item-might-and-armour), [might, armour and damage](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/game_rules.md#might-armour-and-damage)).

**LoL2.** The item row holds a hit mask, hit flags, class, handler and strike countdown. A single armour or damage value per item is open, because the ordinary weapon path builds the amount from player cells, difficulty and the target ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#item-combat-inputs)). On difficulty 0 a hit on the player above 3 is divided by 3 and a hit by the player doubled. On difficulty 2 a hit on the player is doubled and a hit by the player above 2 halved ([hit context](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-combat-ai.md#hit-context-and-reduction)).

**LoL3.** A nonzero disk value `v` at +0x7D becomes `max(1, floor(256/v))`. What that value counts in play is open, and so is a per-item damage or armour value for the full table ([numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#item-definitions), [definition directory](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-item-dispatch.md#definition-directory)).

### Creature health and attack

**LoL1.** Base HP is argument 26 of the definition call. A new monster gets `floor(base HP × difficulty row 1 / 256)`, then `floor(result × (192 + 1d128) / 256)`, and 1 if the result is not above 0. Row 1 is 102, 256, 384 on CD and 192, 256, 384 on floppy for easy, normal and hard. CD skips the second multiply for type 2 on level 12 ([numbers](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/NUMBERS.md#creature-definitions-by-level), [monster behavior](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/game_rules.md#monster-behavior)).

**LoL2.** The constructor reads +0x63 as the health cap. Byte +0x81 is the attack input B, and `M = max(1, floor(B/10))`. The attack value is M, B or `max(M, floor(B*p/(p+q)))` by two actor bytes p and q. A frame hit gives `floor(attack × percent / 100)` ([numbers](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/NUMBERS.md#creature-numbers-by-level), [creature attack](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-combat-ai.md#creature-state-and-attack-output)).

**LoL3.** The constructor copies +0x63 to the health ceiling +0x108, and the setter clamps health to it. Actor +0xFA is half of byte +0x81, rounded down, and +0xF7 can cut it by a quarter. A kind-1 animation hit multiplies +0xFA by the frame percentage. The reader also sets +0x82 to `max(1, floor(+0x81/10))`; what uses +0x82 is open ([numbers](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/NUMBERS.md#creature-definitions-by-level-field-3-type-rows-not-placements-a-few-tags-are-objects), [creature definitions](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-combat-dispatch.md#creature-definitions-and-target-quantity)).

## How a level is put together

- **LoL1:** a CMZ grid of wall IDs, a WLL wall table, VCN/VMP tiles and an INI and INF script; the loader reads the WLL, runs the INI, then loads the INF and dispatches entry 0x400 ([LoL1 level](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/HOW_A_LEVEL_IS_PUT_TOGETHER.md)).
- **LoL2:** a level archive with a texture bank, an ODF and a MAP; the loader reads .tex, .odf and .map in that order, and the MAP reader copies predicates before the event lists and placements ([LoL2 level](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/HOW_A_LEVEL_IS_PUT_TOGETHER.md)).
- **LoL3:** a main archive with MAP, ODF, textures and a light map, plus a sound archive; the loader prepares the sound archive, then textures, LMF, ODF and MAP ([LoL3 level](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/HOW_A_LEVEL_IS_PUT_TOGETHER.md)).

## How the comparison was made

Each fact comes from that game's own pages, which carry the evidence. No rule is assumed to carry over from one game to the next. Where two games look alike, both pages measured it, for example the `max(1, floor(+0x81/10))` byte in the LoL2 and LoL3 creature rows.
