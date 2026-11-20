# Native EMC2 handler comparison

Offsets below are physical file offsets in the English retail CD and
floppy `MAIN.EXE` files. The [function table](emc2_scripts.md#lol1-system-functions)
gives the names, dispatch entries, resolved bodies and upstream
ScummVM file and line references.

## Finding the handler

**CONFIRMED.** The opcode 0x0E arm at CD `+0x131A3–+0x131E3`
(floppy `+0x17B66–+0x17BA6`) gets a far table pointer from the
EMC2 context. It masks the operand with `0xFF`, multiplies by 4 and
reads the far handler pointer, offset word first. It calls the
handler with the script state and writes AX back to state +8. Native
wrappers index the word stack at state +0x2C with the current index
at +0x0C, as in CD `+0x13673–+0x1368E`.

**CONFIRMED.** For each table row the original MZ relocation list
(count at file +0x06, list at the u16 at +0x18) contains the row's
segment-word offset. The first slot with no segment-word relocation
ends the table. The MZ header length comes from +0x08. A resident
overlay stub segment stores its bank offset at +4. A five-byte
entry in the segment begins with `CD 3F` and its +2 word is the
offset into that bank. See the [overlay mapping](unknowns/07_native_rules.md).

| Original image | Table range, end exclusive | Slots | Overlay entries |
|---|---|---:|---:|
| CD `MAIN.EXE` | `+0x33F64..+0x34264` | 192 | 52 |
| CD `MAINW.EXE` | `+0x33A08..+0x33D08` | 192 | 52 |
| Floppy `MAIN.EXE` | `+0x3D1EE..+0x3D4DA` | 187 | 51 |

For example, CD slot 0x7D at `+0x34158` points to
`+0x30F90`, the first entry in the stub segment at `+0x30F70`.
Add the bank offset `0x11790` at `+0x30F74` to
`+0x3CC50`, the first byte after the FBOV header, and
the zero body offset at `+0x30F92` to reach `+0x4E3E0`.
The corresponding body starts at `+0x4DDC0` in MAINW and
`+0x57071` in floppy MAIN.EXE.

`exe_tables.py --table emc2` lists every original slot and its
resolved offset for the supplied edition. The executable check
validates the relocation walk and the digest of the ordered entry
and body offsets in each supplied image. It also compares the CD and
floppy handler columns of the function table with the resolved rows.

## Observed effects

**CONFIRMED.** “Agrees” covers the behavior stated in the row.
“Differs” records behavior absent or different in upstream.
“Partial” records the part of the reference followed in original code.
The comparisons cover CD and floppy MAIN.EXE where the slot exists.
ScummVM source locations are in the corresponding function-table rows.

| Slot | Comparison | Native read | CD MAIN.EXE | Floppy MAIN.EXE |
|---|---|---|---|---|
| 00 | Partial | Both wrappers test new wall flag 4 before one helper and then call the wall setter. The setter accepts side −1 and writes all four sides. | `+0x1345F–+0x134BC, +0x16C09–+0x16C22` | `+0x17E22–+0x17E7F, +0x1B374–+0x1B38D` |
| 01 | Agrees | Reads the wall byte of the 10-byte block record, masks the requested side with 3, and sign-extends the byte. | `+0x134BD–+0x134EF` | `+0x17E80–+0x17EB2` |
| 03 | Agrees | The two arguments go to the dice helper. It loops count times, scales a random draw by sides and adds the resulting 1-based values. | `+0x13433–+0x1345E, +0xC286–+0xC2DB` | `+0x17DF6–+0x17E21, +0xFAE0–+0xFB35` |
| 05 | Differs | The original reads a TEXT index, passes the string to a text routine and returns 1. | `+0x135FA–+0x13652` | `+0x17FBD–+0x18015` |
| 06 | Agrees | Adds the tick argument to the current tick counter, calling the update helper while the counter is below the deadline. | `+0x13653–+0x1366F, +0xC806–+0xC82F` | `+0x18016–+0x18032, +0x10022–+0x1004B` |
| 07 | Agrees | Uses bit `id & 15` of word `id >> 4`. Nonzero argument 1 sets it and zero clears it. Returns 1. | `+0x13670–+0x136C7` | `+0x18033–+0x1808A` |
| 08 | Agrees | Returns 0 for negative arguments. Otherwise tests the same bit that slot 07 writes and returns its truth value. | `+0x136C8–+0x13701` | `+0x1808B–+0x180C4` |
| 0C | Agrees | Saves the held handle, passes it to the item-removal helper, calls the same hand writer as A9 with 0, and returns the old handle. | `+0x13702–+0x13720` | `+0x180C5–+0x180E3` |
| 17 | Agrees | The original's no-argument stub returns 0. CD BF and floppy BA share this entry in their respective tables. | `+0x1342C–+0x13432` | `+0x17DEF–+0x17DF5` |
| 1C | Agrees | Returns the facing word used by the relative movement path. | `+0x13E2A–+0x13E31, +0x13567` | `+0x187F7–+0x187FE, +0x17F2A` |
| 2B | Differs | Writes 1 to +1 of the 0xB5-byte record selected by the argument and returns 1. | `+0x14114–+0x14133` | `+0x18AD6–+0x18AF5` |
| 2C | Differs | Writes 1 to both +0 and +1 of the same indexed record and returns 1. | `+0x14134–+0x1416B` | `+0x18AF6–+0x18B2D` |
| 2D | Partial | Uses a word index into the same global array that slot 2E writes. | `+0x14199–+0x141B2` | `+0x18B5B–+0x18B74` |
| 2E | Partial | Stores argument 1 at word index argument 0 in the global array and returns 1. | `+0x1416C–+0x14198` | `+0x18B2E–+0x18B5A` |
| 33 | Agrees | Nonzero state clears mask 0x10 and sets 0x20. Zero state clears 0x20. The byte is at +9 of a ten-byte block record. | `+0x1651B–+0x1657C` | `+0x1AE1D–+0x1AE7E` |
| 34 | Agrees | Argument −1 uses side 0 for the A/B comparison and passes −1 to the wall setter. The selected wall is written to every side. | `+0x144AF–+0x144F3, +0x16C09–+0x16C22` | `+0x18E4A–+0x18E8B, +0x1B374–+0x1B38D` |
| 3E | Agrees | No argument reads or side effects. Returns 0. | `+0x148F5–+0x148FB` | `+0x1927C–+0x19282` |
| 42 | Differs | Toggles mask 0x80 according to argument 0, forwards the argument and returns 1. | `+0x4DDB8–+0x4DDE6` | `+0x56915–+0x56943` |
| 43 | Differs | Calls an overlay routine and returns 1. | `+0x4DDE7–+0x4DDF2` | `+0x56944–+0x5694F` |
| 4D | Differs | Passes the first two script words and sign-extends the third to a dword before calling a routine. Returns 1. | `+0x14CAB–+0x14CEF` | `+0x19632–+0x19676` |
| 53 | Agrees | The wrapper returns the handle word used by the hand setter and deletion path. | `+0x14DFD–+0x14E06, +0xC71A, +0xC7D1` | `+0x19784–+0x1978D, +0xFF4B` |
| 55 | Partial | Monster −1 returns 0. The other path passes the item and a 0x2E-stride monster pointer to its helper and returns 1. | `+0x14E07–+0x14E51` | `+0x1978E–+0x197D8` |
| 5A | Agrees | Masks side with 3, reads its wall byte and returns the corresponding flag byte, zero-extended. | `+0x134F0–+0x1352A` | `+0x17EB3–+0x17EED` |
| 66 | Agrees | Follows the block's assigned linked list and counts entries whose high bit is clear. | `+0x15208–+0x1524B` | `+0x19B82–+0x19BC5` |
| 67 | Differs | Uses both arguments and adds 10 times the skill sum. Chooses the first strict maximum above zero, then returns −1 if the 1d100 roll exceeds the maximum. | `+0x1524C–+0x152E4` | `+0x19BC6–+0x19C5E` |
| 68 | Agrees | Walks 30 records of stride 0x2E and counts positive signed HP at +0x1D except mode 13 at +0x14. | `+0x152E5–+0x15318` | `+0x19C5F–+0x19C92` |
| 6B | Partial | Returns the previous signed brightness byte, stores the new low byte and calls the palette helper only when argument 1 equals 1. | `+0x47C99–+0x47CF0` | `+0x51478–+0x514CF` |
| 6D | Agrees | The helper supplies count 2 and the script's sides argument to the same dice routine as slot 03. | `+0x154A5–+0x154BE, +0xB0A3–+0xB0B4` | `+0x19E17–+0x19E30, +0xAFC5–+0xAFD6` |
| 6E | Agrees | Tests the character flags against mask 9, compares the ID word against the argument, and returns 1 for a match among the four slots. | `+0x1532E–+0x1537F` | `+0x19CA0–+0x19CF1` |
| 74 | Differs | Returns 0 on the first empty slot. Returns 1 after scanning all 48 slots without finding a zero. | `+0x156BC–+0x156DA` | `+0x1A02E–+0x1A04C` |
| 76 | Differs | Uses argument 1 to select one of two calls and returns 1. | `+0x1586A–+0x15893` | `+0x1A1A5–+0x1A1CE` |
| 77 | Differs | Calls an overlay helper without a script argument and returns 1. | `+0x47C8D–+0x47C98` | `+0x5146C–+0x51477` |
| 7B | Agrees | The first matching type (or any type for −1) yields 0 for mode 1 and 1 otherwise. Exhausting the 30 slots also yields 1. | `+0x1592C–+0x15989` | `+0x1A239–+0x1A296` |
| 7D | Differs in floppy | The CD body returns 1. Floppy passes two script words to a comparison helper and returns its result. | `+0x4E3E0–+0x4E3E7` | `+0x57071–+0x5709B` |
| 7E | Differs | Invokes the original shutdown path and terminates with DOS status 0. See the [exit trace](unknowns/08_native_script_exit.md). | `+0x159A4, +0xC846–+0xC857, +0x396B–+0x3973` | `+0x1A2B1, +0x10062–+0x10073, +0x496B–+0x4973` |
| 80 | Partial | Copies argument 0 to a word and returns 1. A CD text path then takes that word and emits the format character 0x64. The floppy consumer was left open. | `+0x15A0D–+0x15A26, +0x17250–+0x17263` | `+0x1A31A–+0x1A333` |
| 83 | Agrees | Builds a bitmask from type arguments until −1. Counts selected types among the 30 records with signed mode below 14. | `+0x15B05–+0x15B77` | `+0x1A40D–+0x1A47F` |
| 86 | Agrees | Stores and returns the block argument. The native door path clears the word before running the block event and bypasses a subsequent door action if the script has set it. | `+0x15C95–+0x15CAB, +0x1789F–+0x178D6` | `+0x1A59D–+0x1A5B3, +0x1BECA–+0x1BF01` |
| 8A | Differs | When the backup flag is clear, obtains page 5, copies 0xFA00 bytes to the backup and sets the flag. Returns 1. | `+0x4D311–+0x4D31C, +0x4C5E4–+0x4C61E` | `+0x55EA9–+0x55EB4, +0x55259–+0x55293` |
| 8B | Differs | When backed up, tests six animation addresses against the page-5 range and frees the in-range slots. Copies 0xFA00 bytes back, clears the flag and returns 1. | `+0x4D31D–+0x4D328, +0x4C61F–+0x4C6C3` | `+0x55EB5–+0x55EC0, +0x55294–+0x55338` |
| 90 | Differs | Calls a helper with one script word and returns 1. | `+0x4D3E3–+0x4D3FE` | `+0x55F7B–+0x55F96` |
| 91 | Differs | Calls a different helper with one script word and returns 1. | `+0x4D3FF–+0x4D41A` | `+0x55F97–+0x55FB2` |
| 95 | Differs | Tests both halves of a helper's result and returns its Boolean value. | `+0x47C68–+0x47C8C` | `+0x51447–+0x5146B` |
| 96 | Agrees | Starts at the assigned-list head for previous −1, otherwise advances from the previous monster. Returns a monster index with bit 15 cleared, or −1. | `+0x15DFF–+0x15E76` | `+0x1A6F2–+0x1A769` |
| 97 | Agrees | Scans the initial run of monster handles, accepting the specified index or the first match for −1, then returns the untagged index or −1. | `+0x15E77–+0x15EDE` | `+0x1A76A–+0x1A7D1` |
| 99 | Partial | Passes two word locations and direction to a helper. A nonzero fourth argument returns the first location, zero returns the second. | `+0x15F84–+0x15FF1` | `+0x1A877–+0x1A8E4` |
| 9B | Partial | The CD helper clears the same byte slot 9C reads and passes 2 to a timer routine. Floppy clears the corresponding byte and forwards 2. | `+0x4D4EC–+0x4D4F7, +0x4C5BD–+0x4C5D4` | `+0x56084–+0x5608F, +0x55232` |
| 9C | Agrees | Returns the scene-restore byte written by the companion handlers. | `+0x4D4F8–+0x4D500, +0x4C586–+0x4C5E3` | `+0x56090–+0x56098, +0x5524A` |
| 9D | Agrees | Restarts at 0 on nonzero input, otherwise advances the retained index. Tests flag 1 in each character record, ending at 4 with return −1. | `+0x15FF2–+0x1603B` | `+0x1A8E5–+0x1A92E` |
| A0 | Agrees | Tests 48 pack slots, then 11 equipment slots in each eligible character record. Clears the first handle whose item type matches, returning 1 on success and 0 on exhaustion. | `+0x160D4–+0x161A6` | `+0x1A9C7–+0x1AA99` |
| A1 | Differs | Passes argument 0 to one routine and returns 1. | `+0x161A7–+0x161C3` | `+0x1AA9A–+0x1AAB6` |
| A2 | Differs | Passes argument 0 to a distinct routine and returns 1. | `+0x161C4–+0x161E0` | `+0x1AAB7–+0x1AAD3` |
| A7 | Agrees | Reads the signed word step indexed by direction, adds it to the block and masks to 0x3FF. B7 calls the same helper. | `+0x162AA–+0x162D5, +0xD423–+0xD436` | `+0x1AB9A–+0x1ABC5, +0x10BB1–+0x10BC4` |
| A9 | Agrees | Calls the same hand setter as 0C with the supplied handle and returns 1. | `+0x162D6–+0x162F2, +0xC7D1` | `+0x1ABC6–+0x1ABE2` |
| B7 | Agrees | A separate wrapper forwards the same arguments to the same helper as A7 in both images. | `+0x165F8–+0x16623` | `+0x1AEFA–+0x1AF25` |
| BA | Differs in floppy | CD mode 1 passes icon 133 to the cursor routine and other modes call the normal cursor path. Floppy returns 0 for every input. | `+0x4DED7–+0x4DF00` | `+0x17DEF–+0x17DF5` |
| BB | Partial | CD dispatches −1 and −2 through separate calls and forwards the other tracks with both remaining arguments. Floppy has no slot BB. | `+0x16795–+0x1680A` | — |
| BC | Agrees | The CD wrapper forwards both inputs. The callee adds 1000 and stores the speech ID and speaker if both inputs are nonzero. | `+0x1680B–+0x16836, +0x18DCF–+0x18DF5` | — |
| BD | Partial | For negative input tests magnitude against 50, then rounds up to a multiple of 100. For nonnegative input scans the price words until a value is at least the input or the zero terminator is reached. The native negative arm uses 16-bit arithmetic. | `+0x16837–+0x16897, +0x2F8C0` | — |
| BF | Agrees | Returns 0. The CD and CD MAINW entries share the slot-17 stub. Slot 3E has a separate return-zero body. | `+0x1342C–+0x13432` | — |

## Remaining body work

**UNCONFIRMED.** The 132 slots marked Open on the function page have
confirmed entry and body locations. Their behavior remains from the
ScummVM reference. The 60 comparisons above came from original body
reads, including the operands and side effects where visible, and a
callee trace when needed to identify the action. For the remaining
slots, use the resolved body offset, follow stack reads and calls
through the overlay directory, and match each claimed return or
state change to an instruction. Partial rows specify the part of
the original behavior already observed.
