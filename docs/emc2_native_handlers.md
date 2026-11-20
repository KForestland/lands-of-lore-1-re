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

## Remaining slots read from the original

**CONFIRMED.** The following 132 comparisons add body reads to the
first 60 above. Together the tables cover every slot in CD MAIN.EXE.
The rightmost column is the inspected floppy body range. Where the
operation differs by edition, the note names the path and its
evidence. Argument descriptions use the function table's names for
the corresponding stack words. A partial row confirms the handler
operations described here. The upstream role of a forwarded word
or the final effect of an unnamed helper stays **UNCONFIRMED**
where the note only traces forwarding.

| Slot | Comparison | Script arguments | Original operation | CD evidence | Floppy body |
|---|---|---|---|---|---|
| 02 | Partial | draw mode | Forwards slot 0 to the dungeon-view entry. The wrapper returns 1. | `+0x13539–+0x13547 → +0xD229` | `+0x17EEE–+0x17F0A` |
| 04 | Differs | move mode | Modes 6–9 become (mode − 6 − facing) & 3. Modes 0–5 dispatch six movement calls. Modes 10–13 call the facing routine with mode − 10. That routine uses a signed delta from the current facing and steps left for a delta of −1 and right once for −3. The ScummVM path first takes the absolute value, so it steps right for −1 and left for −3. | `+0x13556–+0x135DD`, table `+0x135DE`, signed turn `+0x168A5–+0x168EA`; floppy turn `+0x1B033–+0x1B078` | `+0x17F0B–+0x17FA0` |
| 09 | Partial | base filename (TEXT), special color, weight, VCN length, VMP length, palette filename (TEXT or −1) | Resolves the base from TEXT and uses a null palette pointer for slot 5 equal to −1 or an empty string. Both length words are widened as unsigned before forwarding. The default-length branch in the callee remains open. | `+0x474E0–+0x475CD → +0x464DB` | `+0x50CA6–+0x50DB5` |
| 0A | Partial | filename (TEXT) | Resolves one TEXT name and hands its far pointer to the level block loader. Returns 1. | `+0x475ED–+0x47617 → +0x4642C` | `+0x50DB6–+0x50DFF` |
| 0B | Partial | filename (TEXT), monster shape slot, animation type | Resolves TEXT slot 0 and passes it with slots 1 and 2 to the shape routine. Returns 1. | `+0x4762F–+0x47683 → +0x46A5A` | `+0x50E00–+0x50E6B` |
| 0D | Agrees | count | Multiplies count by 13, calls the allocator and stores the far result in the definition-table pointer. | `+0x4A5AB–+0x4A5C7` | `+0x53B6F–+0x53B9F` |
| 0E | Differs | type index, name ID, shape, type, script entry, might, skill, protection, flags, extra word | Writes directly to the 13-byte definition. Slot 3 is stored as a word at record +5 for every index. The native writer has no item-264 substitution. Slots 5–7 are stored as bytes at +8 through +0x0A. | `+0x4A5DB–+0x4A6CD` | `+0x53BA0–+0x53CA8` |
| 0F | Partial | type index, shape/frame flags, placed flag | Passes three words to the same item allocation routine used by 11, 49 and 4C. Returns the allocated handle or the helper's failure value. | `+0x13732–+0x1375A → +0xB4ED` | `+0x180E4–+0x18121` |
| 10 | Partial | item, level, block, local X, local Y, flying height | Forwards six words and zero-extends the low bytes of the two local coordinates. Returns 1. | `+0x13770–+0x137D7 → +0x168F2` | `+0x18122–+0x1819E` |
| 11 | Agrees | type index, frame flags, placed flag, level, block, local X, local Y, flying height | Calls the item allocator with slots 0–2. Passes the resulting handle and slots 3–7 to the placement helper unless allocation returns −1. Returns the allocation result. | `+0x137EE–+0x13883` | `+0x1819F–+0x1824A` |
| 12 | Partial | item, selector | Handle below 1 returns 0. Uses a 16-byte instance and 13-byte type row. Selectors 0–5 return placement and instance fields, 7 and selectors above 17 return −1, and 15 masks frame/flags to 13 bits. Native selectors 16 and 17 return type-row +3 and the word formed from +8/+9. | `+0x13899–+0x139B4`, table `+0x139B6` | `+0x1824B–+0x18378` |
| 13 | Partial | character, selector, subindex | Indexes 130-byte character records. Selectors 2–4 return 0, 5–8 read the HP and MP words, 10 indexes the equipment array, and 15 reads record +0x0E. The table gives the storage addressed by the other arms. | `+0x13A6A–+0x13B5A`, table `+0x13B5E` | `+0x1841A–+0x18520` |
| 14 | Differs | character, selector, subindex, value | Writes selected fields in the same 130-byte character records. Native selector 10 stores slot 3 into the equipment word indexed by slot 2, including nonzero values. Selectors 5 and 7 call the HP/MP setter. The routine returns 0. | `+0x13C39–+0x13C46`, table `+0x13C8D`; floppy `+0x185FC–+0x18609` | `+0x18541–+0x1864F` |
| 15 | Partial | SHP filename (TEXT), DAT filename (TEXT) | Resolves two TEXT names and passes them and constant 1 to the shared shape-loading routine. Returns 1. | `+0x4768D–+0x47702 → +0x45FE0` | `+0x50E6C–+0x50EEA` |
| 16 | Partial | — | Calls the paired no-argument shape release routine and returns 1. | `+0x4770C → +0x4620C` | `+0x50EEB–+0x50EF6` |
| 18 | Agrees | filename (TEXT), shape 0, shape 1, first group override, second group override | Resolves TEXT slot 0, loads shape indices from slots 1 and 2, then sets door flag bits for 20 wall rows. Nonzero slots 3 and 4 clear mask 2 over the first or second ten. | `+0x47730–+0x4782A` | `+0x50EF7–+0x5100E` |
| 19 | Partial | filename (TEXT), animation slot, X, Y, delay, flags | Resolves a TEXT filename and passes it, the slot and four animation settings. Returns 1 when the far pointer result is nonzero, otherwise 0. | `+0x4D5A8–+0x4D643 → +0x4CDF8` | `+0x5612D–+0x561DF` |
| 1A | Agrees | animation slot, first frame, last frame, delay | Steps each frame from first through last, upward or downward. The draw helper receives the frame number minus 1. Uses the clock and delay word after each draw. | `+0x13D09–+0x13E23` | `+0x1866E–+0x187F6` |
| 1B | Partial | animation slot | Passes the slot to the same animation release helper called from page-5 restore. | `+0x4D656–+0x4D65B → +0x4D218` | `+0x561E0–+0x561F8` |
| 1D | Agrees | — | The first active character with a negative ID selects a sound from the table. The sound helper receives −1 if none qualify. Returns 1. | `+0x16580–+0x165DF` | `+0x1AE7F–+0x1AEE5` |
| 1E | Agrees | theme | Copies the theme word to the music-selection state and returns 1. | `+0x47F65–+0x47F6C` | `+0x51738–+0x51751` |
| 1F | Partial | X, Y, width, height, enable flags | Passes all five rectangle and flag words to the button setup helper. Returns 1. | `+0x4DE04–+0x4DE52 → +0x4DB3A` | `+0x56950–+0x569B3` |
| 20 | Partial | — | Calls the no-argument button reset and returns 1. | `+0x4DE5B → +0x4DBC1` | `+0x569B4–+0x569BF` |
| 21 | Partial | left, top, right, bottom | Passes four bounds to the coordinate comparison and returns its result. | `+0x13E43–+0x13E7D → +0xC004` | `+0x187FF–+0x1884E` |
| 22 | Differs in floppy | — | CD tests a control byte and the text setting before clearing the current dialogue rectangle and zeroing two text-position words. Floppy begins the clear path without that guard. | `+0x13E85–+0x13EEA`; floppy `+0x1884F–+0x188AA` | `+0x1884F–+0x188AB` |
| 23 | Agrees | animation slot, part, first frame, last frame, cycles, next part, part delay, flag, SFX index, SFX frame | Uses the 0xB5-byte animation and a 16-byte part. Slots 2–9 write eight words in order. Returns 0. | `+0x13F00–+0x13FED` | `+0x188AC–+0x189AD` |
| 24 | Partial | animation slot, part | Passes an animation slot and part to the start helper. The wrapper returns 1. | `+0x14000–+0x1401B → +0x174C8` | `+0x189AE–+0x189DC` |
| 25 | Partial | — | Calls the same mouse-hide routine used before region copies and returns 1. | `+0x14023 → +0x224A7` | `+0x189DD–+0x189E9` |
| 26 | Partial | — | Calls the mouse-show partner and returns 1. | `+0x14030 → +0x224BE` | `+0x189EA–+0x189F6` |
| 27 | Partial | — | Invokes the black fade with duration 10 and returns 1. | `+0x1403D → +0xC529` | `+0x189F7–+0x18A06` |
| 28 | Partial | — | Passes the loaded palette and transition values 10 and 0, then zeroes a palette state word. The color-mode path inside the helper is open. | `+0x1404D–+0x14065 → +0x22795` | `+0x18A07–+0x18A23` |
| 29 | Agrees | filename (TEXT), destination page | Resolves the TEXT bitmap name and forwards the palette buffer. For destination 2 it skips the extra copy. Otherwise it makes the page copy between mouse-hide and mouse-show calls. | `+0x1408F–+0x140F1` | `+0x18A24–+0x18AB8` |
| 2A | Partial | animation slot | Forwards one animation slot to the stop helper and returns 1. | `+0x14105–+0x1410F → +0x17596` | `+0x18AB9–+0x18AD5` |
| 2F | Differs in floppy | selector, subindex | CD dispatches selectors 0–14, with 7 and out-of-range values returning 0. Selector 6 reads an indexed word. Floppy bounds the table at 12, excluding CD selectors 13 and 14. | `+0x141DD`, table `+0x14243`; floppy `+0x18B9F`, table `+0x18BFC` | `+0x18B75–+0x18BFB` |
| 30 | Agrees | selector, subindex or value, value | Dispatches selectors 0–12. Selector 0 sets the block and runs follow-up location calls, 6 writes an indexed word, 7 does nothing, and 11/12 store the low byte of slot 1. | `+0x14295–+0x14355`, table `+0x1435A` | `+0x18C16–+0x18CEF` |
| 31 | Agrees | block, switch action | Tests mask 8 in side-0 wall flags, passes the resulting inverse flag, block and action to the shared door routine. Returns 1. | `+0x14385–+0x143C2 → +0x179D8` | `+0x18D0A–+0x18D5C` |
| 32 | Agrees | — | Walks four active character records and the first four nonzero equipment handles. Resolves the type record and returns 1 for script byte 0 or 2, otherwise 0. | `+0x143CD–+0x1443F` | `+0x18D5D–+0x18DD8` |
| 35 | Partial | wall/decoration index | Passes one index to the level decoration assignment helper and keeps its result. | `+0x47E2C → +0x460CA` | `+0x51602–+0x5161A` |
| 36 | Agrees | replacement byte | Copies the replacement byte into five entries starting at DS:5371 and five starting at DS:537B (floppy DS:8817 and DS:8821). Returns 1. | `+0x47DF0–+0x47E18` | `+0x515C5–+0x51601` |
| 37 | Partial | source X, source Y, destination X, destination Y, width, height, source page, destination page | Passes all eight words to the rectangular copy routine between mouse-hide and mouse-show calls. The wrapper returns 1. | `+0x14509–+0x145A6 → +0x213C4` | `+0x18E9C–+0x18F45` |
| 38 | Agrees | block, X, Y, facing, type slot, flags, mode, optional four equipment shapes | Takes the first empty non-mode-13 slot among 30. Scales base HP, applies a second roll-dependent factor outside the level-12/type-2 exception, then floors HP at 1. Equipment bytes are copied until the first zero. Returns the slot or −1. | `+0x146B3–+0x148D5` | `+0x18FB1–+0x19261` |
| 39 | Partial | — | Passes a duration of 10 to the same fade/clear helper used by the level change and returns 1. | `+0x145AE–+0x145B6 → +0xC024` | `+0x18F46–+0x18F55` |
| 3A | Agrees | — | Copies 384 bytes of the sequence palette, performs the fade with duration 10 and clears a palette state word. Returns 1. | `+0x145BE–+0x14607` | `+0x18F56–+0x18FA3` |
| 3B | Partial | — | Calls the playfield redraw and returns 1. The code in the helper remains the witness for its brightness effects. | `+0x1460F → +0x4D6EA` | `+0x18FA4–+0x18FB0` |
| 3C | Agrees | level, block, facing | Calls the level-state save path, stores block and facing, computes a centered X/Y and passes the level number to the loader. Clears the instruction pointer in the script state. | `+0x47D6A–+0x47DDB` | `+0x514D0–+0x515C4` |
| 3D | Partial | character | Passes the character slot to the nearest-monster routine and returns its result. | `+0x148E9 → +0xAB13` | `+0x19262–+0x1927B` |
| 3F | Agrees | property slot, shape, combat values, equipment strengths/resistances, HP, flags, ranged and skill settings, sounds | Populates an 83-byte monster definition from slots 0–41. Signed percentages become 8.8 words via (value × 256) / 100. The native writer stores slot 28 into +0x40 and overwrites that word with slot 29. ScummVM keeps the resulting value. | `+0x47842–+0x47B71`; floppy overwrite `+0x5129C–+0x512BC` | `+0x5100F–+0x51355` |
| 40 | Agrees | attacker, target, skill | Passes the attacker, target and skill words to the original battle hit-test routine and returns its result. The hit arithmetic is traced on the [rules page](game_rules.md). | `+0x1490D–+0x14935 → +0xAD0A` | `+0x19283–+0x192C0` |
| 41 | Agrees | target or −1, damage, attacker, skill, death flags | Passes the five script words to the damage helper. Target −1 repeats the call with each party slot 0–3. Returns 1. The helper is traced on the [rules page](game_rules.md). | `+0x14949–+0x14A06 → +0xB0B5` | `+0x192C1–+0x19392` |
| 44 | Agrees | monster, block, X, Y, facing | Acts in modes 1 and 2. Converts block and local coordinates into the destination words, doubles the input facing byte, and changes the movement heading when the destination differs from the current position. | `+0x14A32–+0x14AEA` | `+0x19393–+0x19475` |
| 45 | Partial | count, three lang IDs | Looks up three localized IDs, passes their string pointers and the count to the dialogue button builder, then returns 1. | `+0x14B00–+0x14B55 → +0x17F83` | `+0x19476–+0x194E0` |
| 46 | Agrees | signed credits | Negative input is negated and sent to the deduction helper. Zero or positive input goes to the addition helper. Both calls receive the extra constant 1. | `+0x14B72–+0x14B93` | `+0x194EB–+0x1951E` |
| 47 | Agrees | credits | Signed comparison with the credits word returns 1 when the requested amount is at most the balance. | `+0x14BA6–+0x14BB4` | `+0x1951F–+0x1953F` |
| 48 | Agrees | timer index, tick count | Adds 5 to the script timer index for the native callback array. Zero ticks disables the selected row. A nonzero count goes to the scheduling helper. | `+0x14BC7–+0x14BF6`; [timer rows](unknowns/07_native_rules.md) | `+0x19540–+0x19581` |
| 49 | Agrees | type index, frame flags, placed flag | Returns 0 for a nonempty hand. Otherwise allocates from the three script words, passes the result to the hand setter, then returns 1. | `+0x14BFE–+0x14C4B` | `+0x19582–+0x195D6` |
| 4A | Agrees | type index | Type ranges 70–74, 81–89, 93–97 and 102–106 select sound 12. Other types index a four-word sound table with the low two bits of definition byte +9. | `+0x16479–+0x164D3` | `+0x1AD6D–+0x1ADD9` |
| 4B | Agrees | signed character ID | Nonnegative ID is passed to the add-character routine. Negative ID checks four active slots for its magnitude, clears the active bit on a match and may reset the selected slot. | `+0x4E311–+0x4E3A4` | `+0x56DAC–+0x56E52` |
| 4C | Agrees | type index, frame flags, placed flag | Allocates an item from three words and tries to put it in the pack. If that call returns 0 it deletes the handle and returns 0. Returns 1 on success. | `+0x14C62–+0x14CA8` | `+0x195D7–+0x19631` |
| 4E | Agrees | TIM slot, TIM stem (TEXT) | Looks up the far pointer for the given TIM slot. If empty, resolves the TEXT stem, formats the filename and stores the loaded pointer. Returns 1. | `+0x14D03–+0x14D86` | `+0x19677–+0x19713` |
| 4F | Partial | TIM slot, loop mode | Looks up the saved TIM pointer and passes it with the loop mode to the TIM interpreter. Returns the interpreter's result. | `+0x14D9C–+0x14DBC → +0x9D65` | `+0x19714–+0x19747` |
| 50 | Agrees | TIM slot | Passes the TIM slot pointer to the release helper and clears both words of that pointer. Returns 1. | `+0x14DD0–+0x14DF7` | `+0x19748–+0x19783` |
| 51 | Partial | dialogue mode | Passes one dialogue-mode word to the scene-window initialization helper and returns 1. | `+0x4DD8E–+0x4DD97 → +0x4DA6A` | `+0x568DD–+0x568F8` |
| 52 | Partial | restore mode | Passes one restore-mode word to the paired scene-window helper and returns 1. | `+0x4DDAA–+0x4DDB3 → +0x4DAA5` | `+0x568F9–+0x56914` |
| 54 | Agrees | character, spell, level | Passes character, spell and level to the original resource check. The check returns 1 if MP cost exceeds current MP or HP cost reaches current HP. It returns 0 when both resources suffice. | `+0x16635–+0x1665D → +0xCED0`, comparisons `+0xCEFE/+0xCF6B`; floppy call `+0x1AF5A → +0x106E2` | `+0x1AF26–+0x1AF63` |
| 56 | Partial | basename (TEXT) | Converts slot 0 from TEXT index to a far string pointer, passes it to the language-file helper and returns 1. | `+0x47B91–+0x47BBB → +0x45EB0` | `+0x51356–+0x5139F` |
| 57 | Partial | sound ID | Passes the sound ID and 0 to the sound-effect routine and returns 1. | `+0x14E55–+0x14E6E → +0xA3A1` | `+0x197D9–+0x197F9` |
| 58 | Partial | — | Calls the dialogue processing entry without script arguments and returns AX from it. | `+0x14B5D → +0x17D21` | `+0x194E1–+0x194EA` |
| 59 | Agrees | TIM slot | Looks up the TIM slot, follows its function-array offset and zeros the first far pointer of each of ten 24-byte records. | `+0x14EC2–+0x14EFB` | `+0x19838–+0x19886` |
| 5B | Agrees | monster, selector, value | Masks bit 15 off the monster handle. The switch sets mode, writes HP, attempts to move to a block, sets doubled facing or ORs flags. Handle −1 and the unhandled selectors return 1. | `+0x14F11–+0x14FE4`, table `+0x14FE9` | `+0x19887–+0x1996F` |
| 5C | Agrees | monster, selector | Handle −1 returns 0. After masking bit 15, selectors 0–8 choose mode, HP, block, facing, type, base HP, live flags, definition flags or animation type. Out of range returns −1. | `+0x1500B–+0x150B6`, table `+0x150B8` | `+0x1997E–+0x19A3E` |
| 5D | Partial | — | Calls the monster-shape release entry and returns 0. | `+0x16722 → +0x48053` | `+0x1AFB9–+0x1AFC4` |
| 5E | Partial | character selector, speech parameter, lang ID | Resolves slot 2 as a localized ID and forwards slots 0 and 1 with the text and script state. CD performs the same two stop calls as slot 6A first. Floppy starts with the text path. | `+0x150DA–+0x15133`; floppy `+0x19A61–+0x19AAD` | `+0x19A5E–+0x19AB1` |
| 5F | Partial | — | Calls the engine update entry, also used by the delay loop, and returns 1. | `+0x150CD → +0xC58A` | `+0x19A51–+0x19A5D` |
| 60 | Agrees | sound ID, block or −1 | Substitutes the current block for slot 1 equal to −1 and passes the resulting block and sound ID. Returns 1. | `+0x14E82–+0x14EAC → +0xA295` | `+0x197FA–+0x19837` |
| 61 | Agrees | character, amount or heal level, redraw, magic mode | Nonzero slot 3 calls magical healing with character and level. The other path passes a signed amount to the HP helper and redraws only when slot 2 is nonzero. | `+0x15149–+0x151CC` | `+0x19AB2–+0x19B4A` |
| 62 | Agrees | layout index, disabled overlay | Selects a three-byte layout and draws the button with localized string ID 0x4033. Slot 1 equal to 1 enables an extra overlay draw. | `+0x4DC2C–+0x4DD26` | `+0x56758–+0x56889` |
| 63 | Partial | sound file index | Passes one signed sound-file index to the audio load entry. Returns 1. | `+0x151DF–+0x151E9 → +0x9FDE` | `+0x19B4B–+0x19B67` |
| 64 | Partial | track | Passes the track word to the audio selection routine and returns AX. | `+0x151FC → +0xA171` | `+0x19B68–+0x19B81` |
| 65 | Partial | block | Passes the current script's block to the same removal routine used by the flag-4 wall-change path. Returns 1. | `+0x1673C–+0x1674A → +0xD1AD` | `+0x1AFC5–+0x1AFE8` |
| 69 | Partial | — | Selects a finale variant from the lead character ID. CD waits for speech to finish and constructs the localized path. Floppy invokes a shorter formatting and launch path. Both handlers have a return-0 epilogue. | `+0x16669–+0x1671A`; floppy `+0x1AF68–+0x1AFB4` | `+0x1AF64–+0x1AFB8` |
| 6A | Partial | — | Stops portrait speech animation. CD also first calls the speech-stop routine with 1. Both return 1. | `+0x1531C–+0x15329`; floppy `+0x19C96–+0x19C9B` | `+0x19C93–+0x19C9F` |
| 6C | Agrees | attacker, target, hit type | Forwards attacker, target and hit-type words to the damage estimator. The helper is documented with the [combat arithmetic](game_rules.md). | `+0x15478–+0x154A0 → +0xB053` | `+0x19DD9–+0x19E16` |
| 6F | Agrees | style, lang ID, optional SFX, up to seven formatting values | Looks up slot 1 in the language table, renders with style slot 0 and formatting words 3–9, and plays slot 2 as a sound only if positive. | `+0x15392–+0x15461` | `+0x19CF2–+0x19DD8` |
| 70 | Agrees | item | If the item's block word is nonzero, first calls the unlink helper with block and handle. Then passes the handle to the delete routine and returns 1. | `+0x154CE–+0x15500` | `+0x19E31–+0x19E77` |
| 71 | Agrees | attacker, target, category, base damage, hit type | Forwards all five words to the per-category damage calculation and returns its value, traced on the [rules page](game_rules.md). | `+0x15517–+0x15563 → +0xAF63` | `+0x19E78–+0x19ED9` |
| 72 | Agrees | object type, item, block, local X, local Y, height, facing, flying record byte, attacker/flags | Slot 8 bit 15 selects the explicit local X/Y. Otherwise uses 0x80/0x80 within the block. Doubles facing and deletes the item if launch returns 0. The low byte of slot 7 goes into flying-record byte +0x0B. | `+0x1557D–+0x1566B`, store `+0xF2C7–+0xF2CA` | `+0x19EDA–+0x19FE1` |
| 73 | Partial | character, effect selector, redraw | Uses slot 0 to obtain a character pointer, passes it and two script words to the effect-removal entry, and returns 1. | `+0x15681–+0x156B7 → +0xF725` | `+0x19FE2–+0x1A02D` |
| 75 | Differs | from block, to block, level, include monsters, run script, include items | Walks the source block list. Slot 3 permits monsters to be set to mode 14 and re-placed. CD moves an item only when its frame word has flag 0x4000 and slot 5 is nonzero, preserving low X/Y. Floppy moves every item and does not read slot 5. In both editions slot 4 runs the destination event when the current level equals slot 2. Neither has ScummVM's level-21 substitution for block 0x3E0. Returns whether any object was handled. | `+0x156F3–+0x15863`, flag test `+0x15781`, level compare `+0x157F6`; floppy items `+0x1A0CB–+0x1A110`, level compare `+0x1A131` | `+0x1A04D–+0x1A1A4` |
| 78 | Agrees | spell, availability flag | Checks seven scroll entries for the supplied spell ID and rejects duplicates. On insertion of an ID above 1, passes the second slot into the scroll helper before writing the ID byte. The wrapper returns 1. | `+0x4FB44–+0x4FB5E → +0x4FAC7`, writes at `+0x4FB1C/+0x4FB25` | `+0x59E64–+0x59E91` |
| 79 | Agrees | lang ID, formatting arguments | Resolves slot 0 as a language ID and passes the script state for formatting. Uses text mode 3 and returns 1. | `+0x15897–+0x158C4 → +0x1731C` | `+0x1A1CF–+0x1A203` |
| 7A | Agrees | speech/lang ID, formatting arguments | CD tries speech and prints mode-4 text if speech fails or text is enabled. Floppy directly runs the mode-4 text path. Returns 1. | `+0x158CF–+0x15927`; floppy `+0x1A207–+0x1A234` | `+0x1A204–+0x1A238` |
| 7C | Partial | entry number | Writes one word to the next-entry state and returns 1. The entry consumer is separate from this wrapper. | `+0x15998–+0x1599F` | `+0x1A297–+0x1A2B0` |
| 7F | Agrees | monster | Masks bit 15 off the handle, sets mode 14, marks the block for update and calls the placement helper with zero. Returns 1. | `+0x159C2–+0x15A08` | `+0x1A2BE–+0x1A319` |
| 81 | Differs | forward polled event flag | Checks for pending input and rejects code zero or mask 0x800. Slot 0 acts as a Boolean. Nonzero forwards the polled event code, while ScummVM forwards slot 0 itself. Zero uses the consume path. Returns whether it handled input. | `+0x15A42–+0x15A7B`; floppy `+0x1A361–+0x1A377` | `+0x1A334–+0x1A384` |
| 82 | Agrees | text dimension, flags, lang ID, formatting arguments | Uses the dimension in slot 0. Flag 1 requests a clear, and either low flag bit resets both position words. Resolves slot 2 as a language ID and passes the script state for formatting. | `+0x15A8D–+0x15AFE` | `+0x1A385–+0x1A40C` |
| 84 | Agrees | block, side, frame, frame count, wall IDs | Uses the unsigned remainder of frame divided by frame count to pick a wall from the trailing words. Calls the shared wall setter, then returns 0. | `+0x15B98–+0x15BD2 → +0x16C00` | `+0x1A480–+0x1A4DD` |
| 85 | Agrees | character or −1, type index, equipped only | When equipped-only is zero, scans the 48 occupied inventory slots and the hand for a matching type. Then checks selected equipment, with −1 selecting all four character slots. | `+0x15BE9–+0x15C91`, equipment test `+0xE3A7` | `+0x1A4DE–+0x1A59C` |
| 87 | Differs in floppy | TIM slot | Both zero TIM word +2 and write a selection word to −1. CD also zeros a dialogue state word and substitutes 1 for a zero configured value when setting TIM +4. Floppy writes the configured word directly. | `+0x15CBD–+0x15CFD`; floppy `+0x1A5C5–+0x1A5F0` | `+0x1A5B4–+0x1A5F4` |
| 88 | Partial | block, local X or −1, local Y or −1, restart | Retains a search word across calls, accepts restart, masks coordinate filters to bytes except −1 and skips monster-tagged handles. Returns the matched item handle or 0. The list continuation deserves a separate trace. | `+0x15D11–+0x15DCC` | `+0x1A5F5–+0x1A6C2` |
| 89 | Partial | item, block | Passes item and block to the unlink helper used by slot 70 and returns 1. | `+0x15DDF–+0x15DFA → +0xB727` | `+0x1A6C3–+0x1A6F1` |
| 8C | Partial | mode, dialogue flag | Forwards the two setup words to the dialogue-sequence helper and returns 1. | `+0x4D338–+0x4D352 → +0x4C6C4` | `+0x55EC1–+0x55EEE` |
| 8D | Partial | restore mode | Calls the sequence-restore helper with one word and returns 1. | `+0x4D365–+0x4D36E → +0x4C866` | `+0x55EEF–+0x55F0A` |
| 8E | Partial | X, Y, width, height, enable flags | Passes five rectangle and flag words to the special-scene button helper and returns 1. | `+0x4D384–+0x4D3D2 → +0x4C94D` | `+0x55F0B–+0x55F6E` |
| 8F | Partial | — | Calls the no-argument restore helper, which checks two stored scene-state words before restoring button state. | `+0x4D3DB → +0x4C994–+0x4C9B6` | `+0x55F6F–+0x55F7A` |
| 92 | Partial | field type, dialogue flag, suspend GUI, allow scene update, control mode, fade flag | Forwards all six setup words to the special-scene entry and returns 1. | `+0x4D42C–+0x4D48C → +0x4CA4A` | `+0x55FB3–+0x56028` |
| 93 | Partial | fade flag, redraw playfield, release TIM scripts, scene update mode | Passes the four restore words to the paired special-scene helper and returns AX from it. | `+0x4D4A2–+0x4D4DB → +0x4CB41` | `+0x56029–+0x56077` |
| 94 | Agrees | filename (TEXT), sound ID | Resolves slot 0 from TEXT and passes it with the sound ID. The callee rejects IDs above 250, maps the ID to an entry and copies the name into its 10-byte filename slot. The wrapper returns 0. | `+0x47C1E–+0x47C63 → +0xA7ED–+0xA85F` | `+0x513ED–+0x51446` |
| 98 | Partial | source X, source Y, destination X, destination Y, width, height, source page, destination page | Hides the mouse, forwards all eight rectangle/page words to the crossfade routine, shows the mouse and returns 1. | `+0x15EE2–+0x15F7F → +0x494B0` | `+0x1A7D2–+0x1A876` |
| 9A | Agrees | — | Sets the scene-restore byte to 1, conditionally performs the portrait reset and passes 2 to the timer-disable routine. | `+0x4D4E4 → +0x4C586–+0x4C5BC` | `+0x56078–+0x56083` |
| 9E | Partial | character, effect type flag, immunity flags, hit chance, redraw | Passes all five words to the paralysis/poison application entry and returns its result. | `+0x1604D–+0x16099 → +0x41B9B` | `+0x1A92F–+0x1A990` |
| 9F | Agrees | character or −1 | Selects the all-portraits routine for −1 and otherwise passes the character to the single-slot redraw. Returns 1. | `+0x160AC–+0x160CF` | `+0x1A991–+0x1A9C6` |
| A3 | Agrees | animation slot | Reads the signed last-part byte from the 0xB5-byte animation row, resets it to 0xFF and returns the previous value. | `+0x161F2–+0x1621A` | `+0x1AAD4–+0x1AB11` |
| A4 | Agrees | wall shape index, subshape, X, Y, mirror | Slot 0 equal to 0 clears ten bytes of shape state. Otherwise the first two words select a shape pointer and the last three words are stored with it. | `+0x498CE–+0x4996A` | `+0x52F05–+0x52FB3` |
| A5 | Agrees | skip inventory flag, character selector, type index | Slot 0 equal to zero allows a scan of 48 pack handles and a matching type there returns 0. Then slot 1 equal to −1 permits a four-character scan of eleven equipment words per active slot. A concrete slot uses equal start and exclusive end, so the equipment loop is empty. Returns the slot on a match or −1. | `+0x16230–+0x16258 → +0x175CB–+0x17684` | `+0x1AB12–+0x1AB4F` |
| A6 | Agrees | — | Copies the saved 384-byte palette range back into the active buffer, applies the palette and zeroes a state word. | `+0x16260–+0x1629C` | `+0x1AB50–+0x1AB90` |
| A8 | Agrees | — | Returns the signed selected-character byte. The setter writes the same address. | `+0x162A4`, setter `+0xA978` | `+0x1AB91–+0x1AB99` |
| AA | Partial | cup variant selector, character | Passes 3 minus slot 0 and the character word to the Bezel Cup effect, then returns 1. | `+0x410AE–+0x410CC → +0x40DD7` | `+0x4A288–+0x4A2B9` |
| AB | Agrees | item, selector, value | Handle below 1 returns 0. Selector 4 writes the type word, selector 15 replaces the low 13 frame/flag bits, and other selectors return −1. | `+0x139EB–+0x13A53` | `+0x1839D–+0x18419` |
| AC | Partial | type index, redraw | Passes type and redraw words to the inventory/hand exchange helper and returns its result. | `+0x16302–+0x1631A → +0x101A0` | `+0x1ABE3–+0x1AC0E` |
| AD | Agrees | character, spell, level | Passes character, spell and level to the original cast entry and returns AX. The dispatch is documented with [native spell effects](unknowns/07_native_rules.md). | `+0x16330–+0x16358 → +0x4FE9D` | `+0x1AC0F–+0x1AC4C` |
| AE | Agrees | mode | Mode 1 redraws, invokes animation 9 and shakes the scene. Other modes choose a party sound, clear a scene rectangle and invoke animation 12. | `+0x4EB4E–+0x4EC1C` | `+0x5781C–+0x57906` |
| AF | Agrees | character, skill | Reads the selected skill level, subtracts current experience from the threshold and passes that amount to the grant routine. Returns the change in the skill byte. | `+0x4D514–+0x4D58E` | `+0x56099–+0x5612C` |
| B0 | Agrees | color selector | Builds a palette from slot 0, applies the temporary copy, waits and restores the original. A display-mode branch also uses a pixel remap and a scene copy. | `+0x1636F–+0x1645D`; floppy `+0x1AC5F–+0x1ACEF` | `+0x1AC4D–+0x1AD62` |
| B1 | Partial | — | Calls the original restoration routine with no script words and returns AX from it. | `+0x16464 → +0x415F0` | `+0x1AD63–+0x1AD6C` |
| B2 | Differs | page selector (2, 4, or 6), row count | Reads two words. First word 2, 4 or 6 selects DS:2124, 2128 or 212C on CD (floppy DS:221A, 221E or 2222). Another first word leaves the target pointer unset. Stores signed second word multiplied by 320 and returns 1. The page-5 restore uses DS:2128 in its saved-range end calculation. ScummVM's slot only returns 1. | `+0x4D694–+0x4D6E5`, use `+0x4C64E`; floppy `+0x5622C–+0x5627D` | `+0x5621B–+0x56281` |
| B3 | Partial | mode | Passes the control mode to the disable routine and returns its result. | `+0x4D66F → +0x4C4E6` | `+0x561F9–+0x56211` |
| B4 | Partial | — | Calls the paired enable routine without reading script arguments. | `+0x4D67E → +0x4C549` | `+0x56212–+0x5621A` |
| B5 | Partial | duration, width, height | Passes the three shake words and a fixed final 1 to the scene shake helper. Returns 1. | `+0x164EB–+0x16516 → +0x45D05` | `+0x1ADDA–+0x1AE1C` |
| B6 | Partial | block | Passes the block to the original gas-explosion entry and returns 1. | `+0x42C52–+0x42C5B → +0x429D7` | `+0x4BE64–+0x4BE7F` |
| B8 | Agrees | — | Requests dungeon draw mode 2, crossfades the 176 by 120 scene rectangle and calls the same redraw routine as B9. | `+0x16752–+0x16783` | `+0x1AFE9–+0x1B021` |
| B9 | Partial | — | Calls the page-2 redraw entry and returns 1. | `+0x1678B–+0x16790 → +0xC4FA` | `+0x1B022–+0x1B02E` |
| BE | Agrees | — | Sign-extends the current language byte. The CD finale uses the same byte to select localized data. | `+0x1689B–+0x168A0`, use `+0x1669B` | absent |

## Open parts of the comparison

**UNCONFIRMED.** Where a handler forwards arguments, its entry and
operand reads alone establish the inputs and return route. A
branch-by-branch read of the named callee would settle the remaining
effect details. For example, `+0x475C7` binds the level-graphics
arguments to `+0x464DB`, and `+0x4D486` binds the special-scene
arguments to `+0x4CA4A`. The file-offset reader also lists the
alternate CD MAINW addresses.
