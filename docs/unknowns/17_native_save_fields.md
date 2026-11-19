# Q17 — Fields skipped when importing a DOS save

[Save file layout](../savegame_format.md) · [Executable locations](../executable_tables.md)

This page uses offsets from the start of the saved global-state block. Its file start is CD `0x0254` or floppy `0x0249`. In the tables below, both executable columns mean file offsets in that edition's `MAIN.EXE`. The comparison uses the English CD DOS 1.02 and English floppy writers and loaders. ScummVM's import path is `engines/kyra/gui/saveload_lol.cpp:55–67,107–186,237–245,255–289` at revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`.

## Global-state block

**CONFIRMED** The native writer copies consecutive bytes directly from the same data-segment range the corresponding reader fills. CD uses `DS:7FD0` and 563 bytes. Floppy uses `DS:B476` and 557 bytes. CD `+0x4898D–0x4899D, +0x48B92–0x48BA2`; floppy `+0x5204C–0x5205C, +0x521ED–0x521FD`. Subtract the saved range's base displacement from a native data address to locate the corresponding field in a save.

| Relative save offset | Measured layout and use | Native evidence |
| ---: | --- | --- |
| `0x00A` | **CONFIRMED** A `u16 LE` options word. Bits 4–5 select difficulty. Masks 1 and 2 are the effects and music toggles respectively. Mask 4 enables the floating cursor and mask 8 enables smooth scrolling. | CD `+0xCC86–0xCC93, +0x4B523–0x4B535, +0x4B566–0x4B58F, +0x4BF8A–0x4BFC9`. Floppy `+0x10498–0x104A5, +0x5205F–0x52094, +0x54DA9–0x54DE9, +0x54E73–0x54EF6`. The option order is at CD `+0x29BA1–0x29BD2`, floppy `+0x38E63–0x38EA8`. CD `STARTUP.PAK+0x8BBC–0x8BC7` has the label pointers. |
| `0x014` | **UNCONFIRMED** One intervening byte. The selected character at `0x013` and current level at `0x015` are both single-byte native reads. Test: [test Q17](../NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play). | CD `+0x162A4–0x162A9, +0x48B02–0x48B0C`; floppy `+0x1AB94–0x1AB99, +0x52173–0x5217D`. |
| `0x07C`–`0x143` | **CONFIRMED** 200 saved bytes from the flag-table base to the next table, enough for 100 consecutive flag words. For flag `k`, the native syscalls index word `k / 16` and mask `1 << (k % 16)`. ScummVM reads the first 40 words and advances over the following 120 bytes. **CONFIRMED** Shipped play never names a flag above 592 (CD) or 587 (floppy), so words 38–99 are unused. Every argument to EMC `0x07` and `0x08` in the 60 scripts per edition is a literal or resolves through its callers. The resolved values include CD `L07.PAK` LEVEL7.INF 140–145, `L11.PAK` LEVEL11.INF 274–280 and `L22.PAK` LEVEL22.INF 368–374. Three calls sit in two blocks that no branch, call or entry reaches: CD `L11.PAK` words `0x0202–0x0213` and `L29.PAK` word `0x02E0`, with the same blocks in floppy. In native code only the syscall handlers index the table (CD `+0x136A6, +0x136BF, +0x136F3`; floppy `+0x18069, +0x18082, +0x180B6`). Other code reads and writes fixed low words directly: bit `0x80` of word 0 (CD `+0x4DDCE, +0x4DDD6`; floppy `+0x5692B, +0x56933`) and word 15 at `DS:806A`, which has 24 direct references in the CD program (for example the lamp tests at `+0xBF56` and `+0xF9E1` and the menu lamp reset at `+0x4DE66` and `+0x4DE7B`). No absolute operand inside CD `DS:809C–8113` or floppy `DS:B542–B5B9` decodes on an instruction boundary. | CD `+0x13670–0x13701, +0x1416C–0x141B2`; floppy `+0x18033–0x180C4, +0x18B2E–0x18B74`; ScummVM `saveload_lol.cpp:134–164`. |
| `0x144`–`0x20B` | **CONFIRMED** 200 saved bytes from the indexed script-global table base through the byte before brightness. The native getters and setters use a two-byte stride. ScummVM reads indices 0–23, then skips the following 152 bytes. **CONFIRMED** Shipped play uses only indices 0–23. Every index argument to EMC `0x2D` and `0x2E` in the 60 scripts per edition is a literal (0, 1, 2, 5, 9–17, 22, 23) or a sum resolved through its callers. The sums are `6 + {0, 1, 2}` at CD `L01.PAK` LEVEL1.INF words `0x1277, 0x12A4` and `18 + 0` at `L19.PAK` LEVEL19.INI word `0x0075`, with the same floppy sites. In native code only the two syscall handlers index the table (CD `+0x14190, +0x141AD`; floppy `+0x18B52, +0x18B6F`). No absolute operand inside CD `DS:8144–81DB` or floppy `DS:B5EA–B681` decodes on an instruction boundary. | CD `+0x1416C–0x141B2, +0x1420E`; floppy `+0x18B2E–0x18B74, +0x18BD0`; ScummVM `saveload_lol.cpp:164–172`. |
| `0x20F` | **UNCONFIRMED** One intervening byte. Lamp effect at `0x20E` is a byte and credits at `0x210` are a word. Test: [test Q17](../NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play). | CD `+0xFC34, +0xFD06, +0x14213`; floppy `+0x145FD, +0x146CF, +0x18BD5`. |

## Six CD-only bytes after the level mask

**CONFIRMED** The CD global block extends through relative `0x232`. The floppy block ends at `0x22D` exclusive, immediately after the four-byte level mask. CD `+0x48B92–0x48BA2`; floppy `+0x521ED–0x521FD`.

| Block offset | CD save offset | Interpretation and evidence |
| ---: | ---: | --- |
| `0x22D` | `0x481` | **CONFIRMED** Language index. The menu displays localized ID `0x42D6 + index`. A change copies it to the live language selector and calls the language reload routine. CD `+0x4BED3–0x4BEDA, +0x4C187–0x4C1A6`. The English/French/German labels are CD `STARTUP.PAK+0x9094, +0x9096, +0x9098` (pointer words). |
| `0x22E` | `0x482` | **CONFIRMED** Dialogue text switch. The menu can toggle the byte, and the system forces text to 1 when speech is unavailable. CD `+0x4729F–0x472C7, +0x489F8–0x48A09, +0x4BEDC–0x4BEEB, +0x4BFDF–0x4C001`. CD `STARTUP.PAK+0x908C` points to the text toggle label. |
| `0x22F` | `0x483` | **CONFIRMED** Talking volume. UI selector 5 reads the byte, and the apply branch uses it for the talking-volume update. CD `+0x4B1F2–0x4B21F, +0x4B5BB–0x4B5F7`, and the selector/label row at `+0x29C30–0x29C3D`. Text ID `0x42DC` uses CD `STARTUP.PAK+0x90A0`. |
| `0x230` | `0x484` | **CONFIRMED** Sound-effect volume. UI selector 4 reads the byte and the load path sets effects availability from it. CD `+0x4B201–0x4B219, +0x489C6–0x489F2, +0x29C22–0x29C2F`. Text ID `0x42DA` uses CD `STARTUP.PAK+0x909C`. |
| `0x231` | `0x485` | **CONFIRMED** Music volume. UI selector 3 reads it and the load path enables or stops music according to the byte. CD `+0x4B200–0x4B214, +0x489A0–0x489C5, +0x29C14–0x29C21`. Text ID `0x42DB` uses CD `STARTUP.PAK+0x909E`. |
| `0x232` | `0x486` | **UNCONFIRMED** One final byte copied in the block. The next call serializes the independent item array. CD `+0x48B92–0x48BBF`. Test: [test Q17](../NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play). |

Example (**CONFIRMED**, CD `+0xCC86–0xCC93`; floppy `+0x10498–0x104A5`). The difficulty extraction is `(word & 0x0030) >> 4`. A word `20 00` at offset `0x025E` in a CD save or `0x0253` in a floppy save therefore selects difficulty index 2. These are constructed example bytes.

The four-byte character and monster fields skipped by the importer are native far pointers. The native character load paths replace the modifier pointer after loading (`CD MAIN.EXE+0x48923–0x4898B`; floppy `+0x51FE2–0x5204A`). The monster pointer is present in a floppy `_LEVEL1.TMP+0x8A` written by the game during play (not shipped; [save format](../savegame_format.md)), and ScummVM rebuilds it from the saved monster type (`saveload_lol.cpp:279–289`). A populated native level slot begins with a four-byte sidecar length. The original loaders consume that length and the fixed-size buffer to recreate the temporary file, while ScummVM uses the fixed slot stride (`CD MAIN.EXE+0x48A70–0x48AEC`; floppy `+0x520E1–0x5215D`; ScummVM `saveload_lol.cpp:237–245,309–310`).

## Isolated bytes

**CONFIRMED** The native game-state initialization zero-fills the entire saved global block, including these bytes. CD calls its byte-fill routine with zero, length `0x233` and `DS:7FD0` at `MAIN.EXE+0x4A437–0x4A445`. floppy calls the equivalent with zero, length `0x22D` and `DS:B476` at `MAIN.EXE+0x53A1D–0x53A2B`. Both fill the final odd byte as well as the whole words (CD `+0x7512–0x7535`, floppy `+0x7790–0x77B3`). The resident data image also starts each byte at zero.

| Block offset | CD save / runtime / initial executable byte | floppy save / runtime / initial executable byte |
| --- | --- | --- |
| `0x014` | `0x268` / `DS:7FE4` / `MAIN.EXE+0x39AB4` | `0x25D` / `DS:B48A` / `MAIN.EXE+0x42CEA` |
| `0x20F` | `0x463` / `DS:81DF` / `MAIN.EXE+0x39CAF` | `0x458` / `DS:B685` / `MAIN.EXE+0x42EE5` |
| `0x232` | `0x486` / `DS:8202` / `MAIN.EXE+0x39CD2` | Outside the saved block |

**CONFIRMED** The loader restores these bytes as part of its block read and the writer copies them again. No normalization of these particular bytes appears in the surrounding save and load code (CD `MAIN.EXE+0x4898D–0x48A09, +0x48B92–0x48BBF`, floppy `+0x5204C–0x52094, +0x521ED–0x52209`).

**UNCONFIRMED** The zero initialization and narrow accesses to the adjacent fields make alignment or unused space plausible. The targeted static check compared literal data addresses, direct memory operands, and accesses beginning at the preceding field. For example, the CD occurrence of word `81DF` at `MAIN.EXE+0x1EE77` straddles `add bx, di` and the next instruction, while `+0x4A8E1` is part of `mov bx, di` followed by `and bx, 0x7FFF`. Neither is a memory access. A repeat scan of both whole files agrees. Every access that decodes on an instruction boundary at CD `DS:7FE3`, `DS:81DE` and `DS:8201`, or floppy `DS:B489` and `DS:B684`, is byte-wide. No such access uses the isolated addresses. The individual meanings remain open because a pointer-relative access can avoid the literal address ([test Q17](../NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play)). The floppy witness is a level sidecar. The CD round trip below exercises the full save and load paths.


### CD movement and save round trip

**CONFIRMED.** In English CD 1.02, the memory watch addresses
for `DS:7FE4/81DF/8202` were linear `0x37CD4/37ECF/37EF2`
with the program data segment `2FCF`. The three bytes were zero
after startup. After attaching, the watchpoints returned two
loads and two saves for each byte. All six writes came from
INT 21h file reads and all six reads went to INT 21h file
writes, stopped at the same DOS interrupt dispatch site. These
are the bulk loads and saves at `MAIN.EXE+0x4898D–0x4899D`
and `+0x48B92–0x48BA2`. Movement, turning and ordinary menu
use between them produced no other access in this trial.

| CD slot written by the game in this run (not shipped, not tracked), SHA-256 prefix | Block at `+0x254` | Facing at `+0x263` | Bytes at `+0x268/+0x463/+0x486` |
|---|---:|---:|---|
| `477b08b82ecd` | 557 | 0 | 0, 0, 0 |
| `0ca8eaddc728` | 526 | 0 | 0, 0, 0 |
| `746b8748466f` | 526 | 1 | 0, 0, 0 |

The first save was taken in the initial room. The game loaded
it, moved forward and right, and wrote the second slot. It
then reloaded the second slot, turned right while staying on
block 526, and wrote the third. All three slots end at
`0x1427F` and hold level 1 at `+0x269`. **UNCONFIRMED.**
Byte-specific access during a lamp change, a party change, a
level transition, or other play. The three fields' general
roles and the floppy runtime result remain open
([test Q17](../NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play)).

### CD level-1 lamp-effect reset

**CONFIRMED.** The English CD 1.02 slot `477b08b82ecd`
loaded level 1, block 557 (slot +0x269 and +0x254), with
brightness, oil and lamp effect all zero at slot `+0x460..+0x462`.
The next two menu saves, from that same block
(written by the game in this run; not shipped), wrote `00 00 00` (`ecdc069aaa57`)
and `00 00 FF` (`6dd94ac6ac93`). All three isolated bytes
(`+0x268/+0x463/+0x486`) were zero in both of those saves.

On resume, a GDB hardware watch on `DS:81DE` in a local
DOSBox build captured 0 → 255 and
instruction bytes `C6 06 DE 81 FF` immediately before the
reported IP. They match `MAIN.EXE+0x4DE6C`, with the following
far call relocated in the running overlay. Read/write watches on
`DS:7FE4/81DF/8202` saw only bulk file reads and writes at
`F000:14A5` during this load/save sequence
(`MAIN.EXE+0x4898D–0x4899D/+0x48B92–0x48BA2`).
The menu resets the effect byte during the watched interval.
Only `DS:81DE` had a value watch: brightness and oil were zero
in the sampled states, not watched throughout. The menu and
rest-button clicks between the sessions have no log. The
second menu save (`6dd94ac6ac93`) was written between watch
sessions, so its isolated-byte values are confirmed from the
file only. In all three slots flag word 15 (+0x2EE) has the
lamp-available bit `0x0800` clear, the bit tested at
`MAIN.EXE+0xBF56`. That is why this start offers no active-lamp
control.

**UNCONFIRMED.** An active lamp or oil change on this route.
The starting level-1 state provides no lit-lamp control. To
settle active use, start with a lit lamp and oil through ordinary
play. Watch brightness, oil and effect at `DS:81DC–81DE` and
the three isolated bytes. Refill once using the native lamp
path `MAIN.EXE+0x105F3–0x1065B`, then let an admitted oil tick
run at `+0xF9DE–0xFA04`. Compare the live accesses and the
new slot with the menu-reset control above.

### CD level-1 selected-character control

**CONFIRMED.** Starting at block 557 in the same English CD slot,
normal movement and two door switches reached the guard in block
270 and the first audience in block 273 (event instructions
`L01.PAK+0xD545/+0xD76D`). The watches were attached at block
493; the walk from 557 to 493 was not watched. GDB hardware
watches on a local DOSBox build then twice saw `DS:7FE3` change
0 → 99 → 0. The overlay offsets within the
loaded segment, 0x4A and 0x6B, match the immediate store
`MAIN.EXE+0x4C4AA` and the saved-byte restoration
`+0x4C4CB`. The three isolated bytes had no access during the
two transitions. The first watch ended after the audience, and
the move from block 273 back to 272 happened between watch
sessions. A separate watch from block 272 through the menu save
recorded only the bulk save write (`+0x48B92–0x48BA2`).

The resulting native slot, `4bfff15d2666` (written by the
game in this run; not shipped), has level 1 and
block 272 at +0x269/+0x254. Its selected byte +0x267 and all
three isolated bytes are zero. The four character flags at
`+0x4C + 130*i` are `1, 0, 0, 0`. This is a live control
for a temporary change to the selected-character byte. The party
still contains one selectable character.

**UNCONFIRMED.** A selection between two active members. In
this slot, flag 4 is set at +0x2D0 and flag 39 is clear at
+0x2D4. On a later entry to block 273, after flag 4 is set,
the block-273 event tests flag 39 at `L01.PAK+0xD7FD`. While it
is clear, `setGlobalVar(0, 0, 272)` at `+0xD813` puts the party
back on block 272. Flag 39 is first set by the level-4 block-73
event (`setGameFlag(39, 1)` at `L04.PAK+0xB516`), so level 1
alone cannot open this route. The level-1 block-274
event contains the party calls
at `L01.PAK+0xDA3B/+0xDA41`. To settle selection, use an original
slot after a follower has joined. Click the other active portrait,
watch `DS:7FE3` and the three isolated cells, then check the
selected byte at slot +0x267 and the four character flags.

### Level-1 oil refill on an edited copy

**CONFIRMED, edited-save run.** In the English CD 1.02 slot from
block 557 (source SHA-256 prefix `477b08b82ecd`, 82,559 bytes), the
first trial changed exactly these bytes.

| Slot offset | Old → new | Field |
|---|---|---|
| `0x2EF` | `02 → 0E` | Set flags 250 and 251 in the high byte of flag word 15 |
| `0x460` | `00 → 01` | Brightness |
| `0x461` | `00 → 1A` | Oil, 26 |

The game loaded the copy (`c9fc6fca866f`), but at block 557 the
live brightness, oil and effect were `0, 26, 8` at `DS:81DC–81DE`.
Clicking the lamp reported low oil. The original writer produced
`5c87f471feb7`, with the same three values at `+0x460..+0x462` and
high flag byte `0A` at `+0x2EF`. The cleared brightness and flag 250
leave the oil-decrement gates at `MAIN.EXE+0xF9E9–0xF9F6` closed.

**CONFIRMED, edited-save run.** From the same original slot, the
refill trial changed only the following bytes. The inventory handle
names row 11 at `+0x537` in the 16-byte item array; unused rows carry
bit 15 in the word at row `+0x0E`.

| Slot offset | Old → new | Field |
|---|---|---|
| `0x2EF` | `02 → 0A` | Set flag 251 |
| `0x461` | `00 → 1A` | Oil, 26 |
| `0x270` | `00 → 0B` | Fourth inventory entry, low byte of handle |
| `0x542` | `00 → FF` | Item row 11 level, −1 for a carried item |
| `0x543` | `00 → F8` | Item row 11 property ID, 248 |
| `0x546` | `80 → 00` | Item row 11 high flag byte, mark in use |

The game loaded the copy (`ca2da634f398`), displayed the oil in the
fourth inventory cell, and accepted it when clicked onto the lamp.
A hardware write watch saw `DS:81DD` reach 126 at
`MAIN.EXE+0x1065B` after `add al, 0x64`. Simultaneous access
watches on `7FE4`, `81DF` and `8202` fired only in the DOS
bulk write (`F000:14A5` after the access) when saving. The original
writer's new slot (`5e0f69a88205`) has `00 7E 08` at
`+0x460..+0x462`, zeroes at `+0x268/+0x463/+0x486` and the used
oil row is free again (bit 15 at `+0x545`). The character and
lighting evidence remains scoped to this edited state.

**UNCONFIRMED.** The active oil-depletion event and exact
brightness-normalization writer. A native save in a dark level
with flags 250 and 251 set would allow a watch from the load through
the first `+0xF9FF` decrement and distinguish writes during load
from writes by a level event.

### Selecting between two portraits in an edited copy

**CONFIRMED, edited-save run.** The native defaults record at
`MAIN.EXE+0x29DE2..+0x29E63` supplied Timothy's second character
row at slot `+0xCE..+0x14F` in a copy of `477b08b82ecd`.
The original row was all zero. The complete byte changes are below.
The pointer at row `+0x13` was left zero for the loader to rebind
(`MAIN.EXE+0x48923–0x4898B`); the 11 equipment handles were left
zero because the default record holds property IDs there.

```text
offset (hex) : old → new (hex)
CE:00→01  D0:00→54  D1:00→69  D2:00→6D  D3:00→6F  D4:00→74
D5:00→68  D6:00→79  DC:00→02  E0:00→16  F6:00→01  F8:00→01
FA:00→01  FC:00→01  FE:00→01 100:00→01 102:00→01 104:00→01
107:00→1B 109:00→1B 10B:00→05 10D:00→05 115:00→01 117:00→01
134:00→03 135:00→02 136:00→01 13A:00→C4 13B:00→09 13E:00→E8
13F:00→03 142:00→FA
```

The copy (`f7692902d85c`) showed two portraits in level 1,
block 557. In that session, clicking right, left, right changed
`DS:7FE3` from 0 to 1 to 0 to 1 at overlay `3FED:0845` just
after the store, with no hits on the three isolated-byte access
watches. The temporary 99 → 0 pair also occurred twice before the
first persistent store. The attempted menu save produced no new
slot, so the selection witness is the live watch only.

**UNCONFIRMED, edited-save run.** A separate copy of
`4bfff15d2666` changed only slot `+0x2D4` from `00` to `80`
(flag 39, the gate at `L01.PAK+0xD7FD`). Moving east from block
272 reached the poisoned-king sequence. The trial ended during
dialogue without a second active portrait or a lead-byte change.
A native slot after a follower joins would test the selection
and its persistence through a normal save.
