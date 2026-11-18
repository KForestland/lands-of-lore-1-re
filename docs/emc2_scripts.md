# Lands of Lore 1 EMC2 scripts

[Decompiler](../tools/emc2_decompile.py) · [Corpus test](../tests/test_emc2_corpus.py)

## Evidence

The CD edition is its `DATA` directory. The second edition is LANDSoL, an English floppy installation (see [formats/README.md](formats/README.md)). ScummVM line numbers refer to upstream revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`. Short source references in this page resolve under `engines/kyra/`: `VM` = `script/script.cpp`, `LoL` = `script/script_lol.cpp`, `ABI` = `script/script.h`, `V1` = `script/script_v1.cpp`. **CONFIRMED** marks checks on the original data. **UNCONFIRMED** marks an effect inferred from the ScummVM implementation without a check in the original executable. Corpus locations are in the last table.

## Container and entry points

All integer fields here are big-endian. File offsets are relative to the INF or INI member.

| Offset or chunk | Layout | Evidence |
| --- | --- | --- |
| `0x00` | Four-byte `FORM` tag. | **CONFIRMED** CD and LANDSoL `LEVEL1.INI+0x00`. |
| `0x04` | `u32` length. The original files in both corpora store the full member size, including the first eight bytes. | **CONFIRMED** CD and LANDSoL `LEVEL1.INI+0x04`, value `0x29E` for a 670-byte member. Same convention across the corpus. |
| `0x08` | Four-byte `EMC2` form type. | **CONFIRMED** CD and LANDSoL `LEVEL1.INI+0x08`. |
| `0x0C` onward | Chunks have a four-byte tag, a `u32` payload size, payload bytes and one pad byte after an odd-sized payload. | **CONFIRMED** both editions' `LEVEL1.INI`, where the 109-byte TEXT payload starts at `0x20`, pad is at `0x8D` and next header starts at `0x8E`. ScummVM `common/formats/iff_container.cpp:52–75` drives reading. |
| `ORDR` | Array of `u16` DATA **word indexes**, indexed by the external entry number. `0xFFFF` is absent. An active entry points to a header word, and execution begins at the following word. In level INF scripts ScummVM tests the header against the caller's event flags. | **CONFIRMED** both editions' `LEVEL1.INI+0x14` points to words `0x1B` and `0x9F`, with code at `0x1C` and `0xA0`. The level mask test is documented by VM:156–178 and LoL:68–89. |
| `TEXT` | Optional. Array of `u16` **byte offsets relative to this payload**, then NUL-terminated byte strings. The first offset equals twice the number of entries in both English corpora. Index 0 reads the first pointer at offset 0. | **CONFIRMED** both editions' `LEVEL1.INI+0x20`. The first pointer `0x0014` leads to `KEEP` at script offset `0x34`. ABI:68 implements lookup as `TEXT[BE16(TEXT + 2 × index)]`. |
| `DATA` | Array of `u16` words. A word can be an instruction, the operand of the previous word, or an ORDR entry header. Jump addresses are DATA word indexes. | **CONFIRMED** both editions' `LEVEL1.INI+0x96`; VM:81–89, 195–218, 228–230, 323–328. |

**UNCONFIRMED in the original caller:** ScummVM starts an INI at entry 0 and may call an additional entry. On INF load it dispatches entry `0x400` with flags `-1`. The level dispatch seeds registers 0–6 with event flags, character number, item, two caller-supplied values, block, and script direction. LoL:34–89.

A listing prints DATA word addresses in hex and string indexes in decimal. To locate a word in the PAK, add the script's PAK offset, its DATA payload offset and twice the word address. TEXT output follows the pointer table, preserving indexed entries. The listing annotates string operands when immediately preceding constant pushes identify them within the same straight-line span.

```sh
python3 tools/emc2_decompile.py /path/to/LEVEL1.INI
python3 tools/emc2_decompile.py /path/to/DATA/L01.PAK --entry LEVEL1.INI
python3 tests/test_emc2_corpus.py /path/to/CD/DATA /path/to/LANDSoL
```

## Instruction encoding and opcodes

**CONFIRMED** against both corpora (member locations below) and VM:195–218. An instruction starts with a word whose bits 8–12 select the opcode. Test the flags in this order.

| Flag or default | Operand and opcode |
| --- | --- |
| `0x8000` | Opcode 0, unsigned operand from bits 0–14 of the same word. |
| `0x4000` | Signed 8-bit operand from the low byte. |
| `0x2000` | Signed 16-bit operand in the next word. |
| Otherwise | Operand 0. |

Effects below describe the ScummVM implementation (**UNCONFIRMED** native behavior, with data coverage reported separately). `p` is the decoded operand, `SP` the top of the downward-growing stack and `BP` the frame base. The VM stores signed 16-bit values and uses `SP = 99`, `BP = 101` at init (ABI:47–59, VM:148–154).

| Hex | Opcode | Operand | Effect | ScummVM |
| --- | --- | --- | --- | --- |
| 00 | jmp | target | Set instruction pointer to DATA word `p`. | VM:228–230 |
| 01 | setRetValue | value | Set return register to `p`. | VM:232–234 |
| 02 | pushRetOrPos | selector | 0 pushes return value. 1 pushes next IP plus one, then old BP, and sets BP to SP plus two. Other values stop. | VM:236–251 |
| 03 | push | value | Push `p`. | VM:33–38, 253–255 |
| 04 | push | value | Push `p`. | VM:37–39, 253–255 |
| 05 | pushReg | register | Push register `p`. | VM:257–259 |
| 06 | pushBPNeg | index | Push stack word `BP - p - 2`. | VM:261–263 |
| 07 | pushBPAdd | index | Push stack word `BP + p - 1`. | VM:265–267 |
| 08 | popRetOrPos | selector | 0 pops to return value. 1 pops BP and return address or stops at the root frame. Other values stop. | VM:269–287 |
| 09 | popReg | register | Pop to register `p`. | VM:289–291 |
| 0A | popBPNeg | index | Pop to stack word `BP - p - 2`. | VM:293–295 |
| 0B | popBPAdd | index | Pop to stack word `BP + p - 1`. | VM:297–299 |
| 0C | addSP | count | Add `p` to SP, normally releasing words. | VM:301–303 |
| 0D | subSP | count | Subtract `p` from SP, normally reserving words. | VM:305–307 |
| 0E | sysCall | function | Use low 8 bits as table index. Dispatch using stack arguments and store the return value. A missing handler returns 0 in ScummVM. | VM:309–321 |
| 0F | ifNotJmp | target | Pop condition. If zero, jump to DATA word `p & 0x7FFF`. | VM:323–328 |
| 10 | negate | selector | Replace stack top with logical NOT (0), arithmetic minus (1), or bitwise complement (2). | VM:330–352 |
| 11 | eval | selector | Pop A, then B, and push the selected result. | VM:354–443 |
| 12 | setRetAndJmp | none | Stop at the root frame. Otherwise pop return value and target, clear stack slot 99, and jump. | VM:445–453 |

**UNCONFIRMED native behavior** for the `eval` selectors below. A is the first pop, B the second. Comparisons and logical operators return 0 or 1. Arithmetic and bitwise results are stored as 16-bit values. VM:354–443.

| Selector (decimal) | Result |
| --- | --- |
| 0, 1 | A AND B, A OR B (logical) |
| 2, 3 | A = B, A ≠ B |
| 4, 5, 6, 7 | A > B, A ≥ B, A < B, A ≤ B |
| 8, 9, 10, 11 | B + A, B − A, B × A, B ÷ A |
| 12, 13 | B shifted right by A, B shifted left by A |
| 14, 15, 16, 17 | B AND A, B OR A, B remainder A, B XOR A |

## LoL1 system functions

Numbering is hexadecimal. Arguments run from stack slot 0 upward, with `TEXT` for a string-table index and `lang ID` for a separate localized text identifier. Arguments can be read conditionally. Columns CD and Floppy count static call sites (**CONFIRMED**, corpus locations below). Unless a row cites native behavior, the names, arguments and effects describe the ScummVM implementation (**UNCONFIRMED** native semantics). A vacant ScummVM slot returns 0 in that interpreter (LoL:2683–2974, ABI:63–69, VM:309–321).

**CONFIRMED** Native tables are arrays of relocated 16:16 pointers with the offset word first. CD `MAIN.EXE+0x33F64` and `MAINW.EXE+0x33A08` have 192 entries. LANDSoL `MAIN.EXE+0x3D1EE` has 187 entries, ending at ID 0xBA. All segment words are MZ relocation targets. Table ends are the first following addresses without a segment relocation at this stride. The native handler columns give file offsets in the two `MAIN.EXE` files. They include entry stubs for overlay code. Resolve a table entry using image header bytes plus pointer segment × 16 plus pointer offset. The original stack accessor is visible in the CD and floppy 0x40 wrappers at `+0x148FC` and `+0x19283`. See [Executable tables](executable_tables.md#locating-the-executables) for the CD archive coordinates.

| ID | Function | Arguments | Effect | CD calls | Floppy calls | CD handler | Floppy handler | Source |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 00 | setWallType | block, side, wall ID | Sets wall type and may remove monsters if the new wall has flag 4. | 907 | 890 | `0x1345F` | `0x17E22` | LoL:2689, LoL:95–103 |
| 01 | getWallType | block, side | Reads wall type as a signed byte, masking side to 0–3. | 612 | 610 | `0x134BD` | `0x17E80` | LoL:2690, LoL:105–108 |
| 02 | drawScene | draw mode | Draws the dungeon scene. | 80 | 81 | `0x1352B` | `0x17EEE` | LoL:2691, LoL:110–114 |
| 03 | rollDice | count, sides | Rolls dice and returns the sum. | 439 | 437 | `0x13433` | `0x17DF6` | LoL:2692, LoL:116–119 |
| 04 | moveParty | move mode | Moves or rotates the party. Modes 0–5 use relative controls, 6–9 transform a compass movement, and 10–13 use the facing-change branch. | 85 | 85 | `0x13548` | `0x17F0B` | LoL:2695, LoL:121–180 |
| 05 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x135FA` | `0x17FBD` | LoL:2696, VM:309–321 |
| 06 | delay | ticks | Delays in engine ticks while updating. | 92 | 100 | `0x13653` | `0x18016` | LoL:2697, LoL:183–187 |
| 07 | setGameFlag | flag ID, enabled | Sets or clears game flag. | 531 | 517 | `0x13670` | `0x18033` | LoL:2698, LoL:189–198 |
| 08 | testGameFlag | flag ID | Tests game flag. Negative ID returns 0. | 638 | 625 | `0x136C8` | `0x1808B` | LoL:2701, LoL:200–206 |
| 09 | loadLevelGraphics | base filename (TEXT), special color, weight, VCN length, VMP length, palette filename (TEXT or −1) | Loads level graphics. A length of −1 uses the loader's default. | 35 | 35 | `0x30B49` | `0x37154` | LoL:2702, LoL:208–212 |
| 0A | loadBlockProperties | filename (TEXT) | Loads block collision and map properties. | 29 | 29 | `0x30B4E` | `0x37159` | LoL:2703, LoL:214–218 |
| 0B | loadMonsterShapes | filename (TEXT), monster shape slot, animation type | Loads monster shapes. | 77 | 78 | `0x30B53` | `0x3715E` | LoL:2704, LoL:220–224 |
| 0C | deleteHandItem | — | Deletes and clears held item. Returns old handle. | 80 | 80 | `0x13702` | `0x180C5` | LoL:2707, LoL:226–232 |
| 0D | allocItemPropertiesBuffer | count | Reallocates item property records. | 1 | 1 | `0x30D3E` | `0x3733E` | LoL:2708, LoL:234–239 |
| 0E | setItemProperty | type index, name ID, shape, type, script entry, might, skill, protection, flags, extra word | Sets the item property record. ScummVM changes type 5 to 0 at index 264. | 285 | 285 | `0x30D43` | `0x37343` | LoL:2709, LoL:241–261 |
| 0F | makeItem | type index, shape/frame flags, placed flag | Creates an item instance and returns its handle. | 110 | 110 | `0x13721` | `0x180E4` | LoL:2710, LoL:263–266 |
| 10 | placeMoveLevelItem | item, level, block, local X, local Y, flying height | Places or moves an existing item. Masks local coordinates to one byte. | 10 | 10 | `0x1375F` | `0x18122` | LoL:2713, LoL:268–272 |
| 11 | createLevelItem | type index, frame flags, placed flag, level, block, local X, local Y, flying height | Creates and positions an item. Returns handle or failure. | 228 | 228 | `0x137DC` | `0x1819F` | LoL:2714, LoL:274–281 |
| 12 | getItemPara | item, selector | Reads block, position, level, type, frame/flags, name, shape, script or combat fields according to selector. See LoL:283–333. | 259 | 260 | `0x13888` | `0x1824B` | LoL:2715, LoL:283–333 |
| 13 | getCharacterStat | character, selector, subindex | Reads character flags, race/class/sex, HP/MP, equipment, protection, might, skill or ID. See LoL:335–385. | 36 | 31 | `0x13A57` | `0x1841A` | LoL:2716, LoL:335–385 |
| 14 | setCharacterStat | character, selector, subindex, value | Writes a selected stat. Equipment selector 10 clears the selected slot. See LoL:387–450. | 17 | 17 | `0x13B7E` | `0x18541` | LoL:2719, LoL:387–450 |
| 15 | loadLevelShapes | SHP filename (TEXT), DAT filename (TEXT) | Loads level shapes and decoration definitions. | 17 | 17 | `0x30B58` | `0x37163` | LoL:2720, LoL:452–456 |
| 16 | closeLevelShapeFile | — | Closes the level shape file. | 17 | 17 | `0x30B5D` | `0x37168` | LoL:2721, LoL:458–463 |
| 17 | Unimplemented | — | **CONFIRMED** The native handler returns 0, sharing a stub with CD 0xBF. ScummVM leaves 0x17 unimplemented. | 0 | 0 | `0x1342C` | `0x17DEF` | LoL:2722, VM:309–321 |
| 18 | loadDoorShapes | filename (TEXT), shape 0, shape 1, first group override, second group override | Loads two door graphics and initializes door wall flags. | 21 | 21 | `0x30B62` | `0x3716D` | LoL:2725, LoL:465–496 |
| 19 | initAnimStruct | filename (TEXT), animation slot, X, Y, delay, flags | Initializes a TIM animation structure, returning success. | 175 | 174 | `0x30EC9` | `0x374A9` | LoL:2726, LoL:498–503 |
| 1A | playAnimationPart | animation slot, first frame, last frame, delay | Plays a frame interval. | 209 | 208 | `0x13CAB` | `0x1866E` | LoL:2727, LoL:505–509 |
| 1B | freeAnimStruct | animation slot | Frees the animation structure if present. | 121 | 120 | `0x30ECE` | `0x374AE` | LoL:2728, LoL:511–516 |
| 1C | getDirection | — | Returns current party facing. | 279 | 279 | `0x13E2A` | `0x187F7` | LoL:2731, LoL:518–521 |
| 1D | characterSurpriseFeedback | — | Plays a character-specific surprise sound for the first eligible active character. | 36 | 36 | `0x1657D` | `0x1AE7F` | LoL:2732, LoL:523–535 |
| 1E | setMusicTrack | theme | Sets current music theme. | 31 | 31 | `0x30B9E` | `0x371A9` | LoL:2733, LoL:537–541 |
| 1F | setSequenceButtons | X, Y, width, height, enable flags | Sets sequence buttons for the supplied rectangle. | 3 | 3 | `0x30F14` | `0x374F4` | LoL:2734, LoL:543–547 |
| 20 | setDefaultButtonState | — | Restores default button state. | 3 | 3 | `0x30F19` | `0x374F9` | LoL:2737, LoL:549–553 |
| 21 | checkRectForMousePointer | left, top, right, bottom | Tests whether the pointer is in the rectangle. | 477 | 391 | `0x13E32` | `0x187FF` | LoL:2738, LoL:555–558 |
| 22 | clearDialogueField | — | Clears dialogue and resets text positions when allowed by control and text modes. | 85 | 85 | `0x13E82` | `0x1884F` | LoL:2739, LoL:560–572 |
| 23 | setupBackgroundAnimationPart | animation slot, part, first frame, last frame, cycles, next part, part delay, flag, SFX index, SFX frame | Configures a background animation part. | 173 | 170 | `0x13EEF` | `0x188AC` | LoL:2740, LoL:574–578 |
| 24 | startBackgroundAnimation | animation slot, part | Starts background animation. | 133 | 127 | `0x13FF1` | `0x189AE` | LoL:2743, LoL:580–584 |
| 25 | hideMouse | — | Hides pointer. | 12 | 9 | `0x14020` | `0x189DD` | LoL:2744, V1:53–57 |
| 26 | showMouse | — | Shows pointer. | 12 | 9 | `0x1402D` | `0x189EA` | LoL:2745, V1:59–63 |
| 27 | fadeToBlack | — | Fades screen to black. | 33 | 33 | `0x1403A` | `0x189F7` | LoL:2746, LoL:586–590 |
| 28 | fadePalette | — | Fades to loaded palette or reapplies brightness in 16-color mode. | 14 | 14 | `0x1404A` | `0x18A07` | LoL:2749, LoL:592–600 |
| 29 | loadBitmap | filename (TEXT), destination page | Loads a bitmap and its palette, optionally copying to another page. | 52 | 52 | `0x1406A` | `0x18A24` | LoL:2750, LoL:602–608 |
| 2A | stopBackgroundAnimation | animation slot | Stops background animation. | 69 | 61 | `0x140F7` | `0x18AB9` | LoL:2751, LoL:610–614 |
| 2B | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x14114` | `0x18AD6` | LoL:2752, VM:309–321 |
| 2C | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x14134` | `0x18AF6` | LoL:2755, VM:309–321 |
| 2D | getGlobalScriptVar | index | Reads one of 24 script globals. | 26 | 30 | `0x14199` | `0x18B5B` | LoL:2756, LoL:616–620 |
| 2E | setGlobalScriptVar | index, value | Sets one of 24 script globals. | 20 | 20 | `0x1416C` | `0x18B2E` | LoL:2757, LoL:622–627 |
| 2F | getGlobalVar | selector, subindex | Reads a selected engine global, including position, level, hand, brightness, money, lamp or control state. See LoL:629–666. | 75 | 65 | `0x141B3` | `0x18B75` | LoL:2758, LoL:629–666 |
| 30 | setGlobalVar | selector, subindex or value, value | Changes an engine global, with selector-specific side effects. Selectors 11–12 take their value from slot 1. See LoL:668–740. | 404 | 404 | `0x14261` | `0x18C16` | LoL:2761, LoL:668–740 |
| 31 | triggerDoorSwitch | block, switch action | Processes a door switch. | 111 | 111 | `0x14374` | `0x18D0A` | LoL:2762, LoL:742–746 |
| 32 | checkEquippedItemScriptFlags | — | Tests whether any of the first four equipment slots of active characters refer to item script entry 0 or 2. | 2 | 2 | `0x143C7` | `0x18D5D` | LoL:2763, LoL:748–760 |
| 33 | setDoorState | block, state | Sets or clears block flag 0x20, clearing 0x10 when setting it. | 15 | 15 | `0x1651B` | `0x1AE1D` | LoL:2764, LoL:762–769 |
| 34 | updateBlockAnimations | block, side, wall A, wall B | Toggles wall type between A and B. | 55 | 55 | `0x14443` | `0x18DD9` | LoL:2767, LoL:771–777 |
| 35 | assignLevelDecorationShape | wall/decoration index | Assigns level decoration shapes. | 14 | 14 | `0x30B94` | `0x3719F` | LoL:2768, LoL:779–782 |
| 36 | resetBlockShapeAssignment | replacement byte | Resets two groups of five wall-to-shape mappings. | 14 | 14 | `0x30B8F` | `0x3719A` | LoL:2769, LoL:784–790 |
| 37 | copyRegion | source X, source Y, destination X, destination Y, width, height, source page, destination page | Copies a screen region and updates the visible screen for page 0. | 203 | 201 | `0x14506` | `0x18E9C` | LoL:2770, LoL:792–799 |
| 38 | initMonster | block, X, Y, facing, type slot, flags, mode, optional four equipment shapes | Places a monster in a free runtime slot, initializes scaled HP and returns slot or −1. | 308 | 308 | `0x14619` | `0x18FB1` | LoL:2773, LoL:801–851 |
| 39 | fadeClearSceneWindow | — | Fades and clears the scene window. | 64 | 64 | `0x145AB` | `0x18F46` | LoL:2774, LoL:853–857 |
| 3A | fadeSequencePalette | — | Fades to the sequence palette. | 67 | 67 | `0x145BB` | `0x18F56` | LoL:2775, LoL:859–870 |
| 3B | redrawPlayfield | — | Redraws playfield and reapplies brightness. | 10 | 11 | `0x1460C` | `0x18FA4` | LoL:2776, LoL:872–880 |
| 3C | loadNewLevel | level, block, facing | Snapshots the old level, loads a new one and stops this script. | 71 | 71 | `0x30B8A` | `0x37195` | LoL:2779, LoL:882–908 |
| 3D | getNearestMonsterFromCharacter | character | Returns nearest monster to the character. | 0 | 0 | `0x148DB` | `0x19262` | LoL:2780, LoL:910–913 |
| 3E | dummy0 | — | Returns 0. | 1 | 1 | `0x148F5` | `0x1927C` | LoL:2781, LoL:915–917 |
| 3F | loadMonsterProperties | property slot, shape, combat values, equipment strengths/resistances, HP, flags, ranged and skill settings, sounds | Loads a 42-position property definition. Argument layout is in [Executable and script tables](executable_tables.md), and the source assignments are at LoL:919–977. | 79 | 79 | `0x30B67` | `0x37172` | LoL:2782, LoL:919–978 |
| 40 | battleHitSkillTest | attacker, target, skill | Returns battle hit test result. | 4 | 4 | `0x148FC` | `0x19283` | LoL:2785, LoL:980–983 |
| 41 | inflictDamage | target or −1, damage, attacker, skill, death flags | Applies damage to one entity or all four party slots for target −1. | 66 | 66 | `0x1493A` | `0x192C1` | LoL:2786, LoL:985–995 |
| 42 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30F0A` | `0x374EA` | LoL:2787, VM:309–321 |
| 43 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30F0F` | `0x374EF` | LoL:2788, VM:309–321 |
| 44 | moveMonster | monster, block, X, Y, facing | Sets movement destination and facing for modes 1 or 2. | 17 | 17 | `0x14A0C` | `0x19393` | LoL:2791, LoL:997–1009 |
| 45 | setupDialogueButtons | count, three lang IDs | Creates dialogue choices from their localized labels. | 103 | 106 | `0x14AEF` | `0x19476` | LoL:2792, LoL:1011–1015 |
| 46 | giveTakeMoney | signed credits | Gives positive credits or takes the magnitude of a negative amount. | 41 | 41 | `0x14B64` | `0x194EB` | LoL:2793, LoL:1017–1026 |
| 47 | checkMoney | credits | Tests whether the party has at least this many credits. | 14 | 14 | `0x14B98` | `0x1951F` | LoL:2794, LoL:1028–1031 |
| 48 | setScriptTimer | timer index, tick count | Schedules timer 0x50 + index or disables it for count zero. | 59 | 59 | `0x14BB9` | `0x19540` | LoL:2797, LoL:1033–1046 |
| 49 | createHandItem | type index, frame flags, placed flag | Creates a held item if the cursor has no item. | 207 | 207 | `0x14BFB` | `0x19582` | LoL:2798, LoL:1048–1055 |
| 4A | playAttackSound | type index | Plays an attack sound selected by item skill and type. | 1 | 1 | `0x1646B` | `0x1AD6D` | LoL:2799, LoL:1057–1069 |
| 4B | addRemoveCharacter | signed character ID | Adds a character for a nonnegative ID. A negative ID removes that character from the active party. | 7 | 7 | `0x30F6A` | `0x3753F` | LoL:2800, LoL:1071–1098 |
| 4C | giveItem | type index, frame flags, placed flag | Creates an item for the inventory. Deletes it again if placement fails. | 12 | 13 | `0x14C50` | `0x195D7` | LoL:2803, LoL:1100–1108 |
| 4D | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x14CAB` | `0x19632` | LoL:2804, VM:309–321 |
| 4E | loadTimScript | TIM slot, TIM stem (TEXT) | Loads the named TIM in an empty slot. | 91 | 87 | `0x14CF0` | `0x19677` | LoL:2805, LoL:1110–1117 |
| 4F | runTimScript | TIM slot, loop mode | Executes the active TIM and returns its result. | 77 | 80 | `0x14D8D` | `0x19714` | LoL:2806, LoL:1119–1122 |
| 50 | releaseTimScript | TIM slot | Unloads the TIM. | 89 | 88 | `0x14DC1` | `0x19748` | LoL:2809, LoL:1124–1128 |
| 51 | initSceneWindowDialogue | dialogue mode | Initializes scene-window dialogue. | 15 | 15 | `0x30F00` | `0x374E0` | LoL:2810, LoL:1130–1134 |
| 52 | restoreAfterSceneWindowDialogue | restore mode | Restores scene window after dialogue. | 17 | 17 | `0x30F05` | `0x374E5` | LoL:2811, LoL:1136–1140 |
| 53 | getItemInHand | — | Returns held item handle. | 211 | 132 | `0x14DFD` | `0x19784` | LoL:2812, LoL:1142–1145 |
| 54 | checkMagic | character, spell, level | Tests whether the character can pay the spell's resource costs. | 1 | 1 | `0x16624` | `0x1AF26` | LoL:2815, LoL:1147–1150 |
| 55 | giveItemToMonster | monster, item | Gives an item to a monster, or returns 0 for monster −1. | 49 | 49 | `0x14E07` | `0x1978E` | LoL:2816, LoL:1152–1158 |
| 56 | loadLangFile | basename (TEXT) | Loads basename plus the current language extension. | 29 | 29 | `0x30B6C` | `0x37177` | LoL:2817, LoL:1160–1166 |
| 57 | playSoundEffect | sound ID | Plays a sound effect. | 640 | 604 | `0x14E52` | `0x197D9` | LoL:2818, LoL:1168–1172 |
| 58 | processDialogue | — | Processes dialogue and returns its result. | 29 | 33 | `0x14B5A` | `0x194E1` | LoL:2821, LoL:1174–1177 |
| 59 | stopTimScript | TIM slot | Stops all functions in the active TIM. | 41 | 42 | `0x14EB1` | `0x19838` | LoL:2822, LoL:1179–1183 |
| 5A | getWallFlags | block, side | Reads wall flags for the wall on that side. | 4 | 4 | `0x134F0` | `0x17EB3` | LoL:2823, LoL:1185–1188 |
| 5B | changeMonsterStat | monster, selector, value | Changes monster mode, HP, block, facing or flags. See LoL:1190–1229. | 47 | 49 | `0x14F00` | `0x19887` | LoL:2824, LoL:1190–1229 |
| 5C | getMonsterStat | monster, selector | Reads monster mode, HP, block, facing, type, base HP, runtime or property flags, or animation type. See LoL:1231–1263. | 23 | 19 | `0x14FF7` | `0x1997E` | LoL:2827, LoL:1231–1263 |
| 5D | releaseMonsterShapes | — | Releases shapes for all three monster slots. | 2 | 2 | `0x1671F` | `0x1AFB9` | LoL:2828, LoL:1265–1270 |
| 5E | playCharacterScriptChat | character selector, speech parameter, lang ID | Plays script chat. In talkie mode it first stops current speech and portrait animation. | 744 | 584 | `0x150D7` | `0x19A5E` | LoL:2829, LoL:1272–1279 |
| 5F | update | — | Runs the engine update. | 42 | 32 | `0x150CA` | `0x19A51` | LoL:2830, LoL:1288–1292 |
| 60 | playEnvironmentalSfx | sound ID, block or −1 | Plays environmental SFX at the given block or current block. | 57 | 57 | `0x14E73` | `0x197FA` | LoL:2833, LoL:1281–1286 |
| 61 | healCharacter | character, amount or heal level, redraw, magic mode | Uses spell healing when magic mode is set, otherwise adds HP and optionally redraws. | 5 | 5 | `0x15138` | `0x19AB2` | LoL:2834, LoL:1294–1304 |
| 62 | drawExitButton | layout index, disabled overlay | Draws an exit button and optionally adds a grid overlay. | 174 | 174 | `0x30EF6` | `0x374D6` | LoL:2835, LoL:1306–1335 |
| 63 | loadSoundFile | sound file index | Loads sound file. | 134 | 134 | `0x151D1` | `0x19B4B` | LoL:2836, LoL:1337–1341 |
| 64 | playMusicTrack | track | Plays a music track. | 121 | 120 | `0x151EE` | `0x19B68` | LoL:2839, LoL:1343–1346 |
| 65 | deleteMonstersFromBlock | block | Removes monsters from a block. | 1 | 1 | `0x1672B` | `0x1AFC5` | LoL:2840, LoL:1348–1352 |
| 66 | countBlockItems | block | Counts assigned items, skipping monsters. | 27 | 27 | `0x15208` | `0x19B82` | LoL:2841, LoL:1354–1366 |
| 67 | characterSkillTest | skill | Rolls against the highest active skill level plus modifier plus 25. Returns that slot or −1. | 67 | 67 | `0x1524C` | `0x19BC6` | LoL:2842, LoL:1368–1384 |
| 68 | countAllMonsters | — | Counts positive-HP monsters except mode 13. | 4 | 4 | `0x152E5` | `0x19C5F` | LoL:2845, LoL:1386–1396 |
| 69 | playEndSequence | — | Plays ending and quits or fades in demo mode. | 1 | 1 | `0x16662` | `0x1AF64` | LoL:2846, LoL:1398–1428 |
| 6A | stopPortraitSpeechAnim | — | Stops portrait speech animation and stops audio speech in talkie mode. | 73 | 41 | `0x15319` | `0x19C93` | LoL:2847, LoL:1430–1436 |
| 6B | setPaletteBrightness | brightness, apply now | Changes brightness and returns previous value. | 39 | 39 | `0x30B85` | `0x37190` | LoL:2848, LoL:1438–1445 |
| 6C | calcInflictableDamage | attacker, target, hit type | Calculates maximum inflictable damage across item categories. | 2 | 2 | `0x15467` | `0x19DD9` | LoL:2851, LoL:1447–1450 |
| 6D | getInflictedDamage | maximum | Rolls two dice with the supplied number of sides. | 8 | 8 | `0x154A5` | `0x19E17` | LoL:2852, LoL:1452–1456 |
| 6E | checkForCertainPartyMember | character ID | Tests matching character ID in slots whose flags intersect 9. | 19 | 17 | `0x1532E` | `0x19CA0` | LoL:2853, LoL:1458–1465 |
| 6F | printMessage | style, lang ID, optional SFX, up to seven formatting values | Prints a localized message and may play a sound. | 139 | 176 | `0x15380` | `0x19CF2` | LoL:2854, LoL:1467–1476 |
| 70 | deleteLevelItem | item | Unlinks a placed item and deletes it. | 7 | 7 | `0x154BF` | `0x19E31` | LoL:2857, LoL:1478–1486 |
| 71 | calcInflictableDamagePerItem | attacker, target, category, base damage, hit type | Calculates inflictable damage for one item category. | 6 | 6 | `0x15506` | `0x19E78` | LoL:2858, LoL:1488–1491 |
| 72 | distanceAttack | object type, item, block, X, Y, height, facing, unused, attacker/flags | Launches a flying item. Uses block center unless bit 15 of slot 8 is set. Deletes item on failure. | 57 | 57 | `0x15568` | `0x19EDA` | LoL:2859, LoL:1493–1511 |
| 73 | removeCharacterEffects | character, effect selector, redraw | Removes selected character effects. | 3 | 3 | `0x15670` | `0x19FE2` | LoL:2860, LoL:1513–1517 |
| 74 | checkInventoryFull | — | Returns 0 if any inventory slot is nonzero, otherwise 1 in this reference handler. | 13 | 14 | `0x156BC` | `0x1A02E` | LoL:2863, LoL:1519–1526 |
| 75 | moveBlockObjects | from block, to block, level, include monsters, run script, include items | Removes selected monsters and moves eligible placed items. May dispatch destination event 0x80. | 89 | 89 | `0x156DB` | `0x1A04D` | LoL:2864, LoL:1528–1578 |
| 76 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x1586A` | `0x1A1A5` | LoL:2865, VM:309–321 |
| 77 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30B80` | `0x3718B` | LoL:2866, VM:309–321 |
| 78 | addSpellToScroll | spell, availability flag | Changes spell scroll availability. | 2 | 2 | `0x31094` | `0x376D4` | LoL:2869, LoL:1580–1584 |
| 79 | playDialogueText | lang ID, formatting arguments | Prints dialogue text. | 1 | 35 | `0x15894` | `0x1A1CF` | LoL:2870, LoL:1586–1590 |
| 7A | playDialogueTalkText | speech/lang ID, formatting arguments | Plays speech and prints dialogue if speech fails or text is enabled. | 60 | 61 | `0x158C9` | `0x1A204` | LoL:2871, LoL:1592–1602 |
| 7B | checkMonsterTypeHostility | type or −1 | Checks the first matching monster. Returns 0 for mode 1, otherwise 1. | 8 | 8 | `0x1592C` | `0x1A239` | LoL:2872, LoL:1604–1612 |
| 7C | setNextFunc | entry number | Sets the next script function. | 5 | 5 | `0x1598A` | `0x1A297` | LoL:2875, LoL:1614–1618 |
| 7D | dummy1 | — | Returns 1. | 1 | 2 | `0x30F90` | `0x37575` | LoL:2876, LoL:1620–1622 |
| 7E | updateAndServiceCallbacks | — | **CONFIRMED** Native handler calls the game update and runtime callback dispatcher, then returns 1. The listing uses a descriptive name. ScummVM leaves this slot unimplemented. | 1 | 2 | `0x159A4` | `0x1A2B1` | CD `MAIN.EXE+0x159A4–0x159B0, +0xC846–0xC857, +0x3DFD`; floppy `+0x1A2B1–0x1A2BD, +0x10062–0x10073, +0x4DFD`; LoL:2877 |
| 7F | suspendMonster | monster | Sets mode 14 and removes its placement. | 26 | 24 | `0x159B1` | `0x1A2BE` | LoL:2878, LoL:1624–1631 |
| 80 | setScriptTextParameter | value | Sets the script text formatting parameter. | 0 | 1 | `0x15A0D` | `0x1A31A` | LoL:2881, LoL:1633–1637 |
| 81 | triggerEventOnMouseButtonClick | event ID | Polls input and optionally triggers the event. Returns whether it handled input. | 3 | 4 | `0x15A27` | `0x1A334` | LoL:2882, LoL:1639–1658 |
| 82 | printWindowText | text dimension, flags, lang ID, formatting arguments | Clears or resets the text area as requested, then prints localized text. | 14 | 14 | `0x15A7D` | `0x1A385` | LoL:2883, LoL:1660–1671 |
| 83 | countSpecificMonsters | type IDs followed by −1 | Counts monsters of those types in modes below 14. | 4 | 4 | `0x15B05` | `0x1A40D` | LoL:2884, LoL:1673–1688 |
| 84 | updateBlockAnimations2 | block, side, frame, frame count, wall IDs | Selects a wall from the list using frame modulo frame count. | 25 | 25 | `0x15B78` | `0x1A480` | LoL:2887, LoL:1690–1697 |
| 85 | checkPartyForItemType | character or −1, type index, equipped only | Checks equipped items and optionally inventory and cursor. | 21 | 13 | `0x15BD6` | `0x1A4DE` | LoL:2888, LoL:1699–1723 |
| 86 | blockDoor | block | Sets the blocked-door block and returns it. | 10 | 10 | `0x15C95` | `0x1A59D` | LoL:2889, LoL:1725–1729 |
| 87 | resetTimDialogueState | TIM slot | Resets TIM dialogue state. | 19 | 17 | `0x15CAC` | `0x1A5B4` | LoL:2890, LoL:1731–1735 |
| 88 | getItemOnPos | block, local X or −1, local Y or −1, restart | Looks up a placed item with optional coordinate filters using a cursor state. | 21 | 21 | `0x15D02` | `0x1A5F5` | LoL:2893, LoL:1737–1774 |
| 89 | removeLevelItem | item, block | Unlinks an item from a level block. | 1 | 1 | `0x15DD0` | `0x1A6C3` | LoL:2894, LoL:1776–1780 |
| 8A | savePage5 | — | Returns 1. The page-save code is commented out in the reference. | 40 | 40 | `0x30E83` | `0x37463` | LoL:2895, LoL:1782–1788 |
| 8B | restorePage5 | — | Frees six animation structures. The page-restore code is commented out. | 42 | 42 | `0x30E88` | `0x37468` | LoL:2896, LoL:1790–1798 |
| 8C | initDialogueSequence | mode, dialogue flag | Initializes a dialogue sequence. | 26 | 24 | `0x30E8D` | `0x3746D` | LoL:2899, LoL:1800–1804 |
| 8D | restoreAfterDialogueSequence | restore mode | Restores after dialogue sequence. | 21 | 20 | `0x30E92` | `0x37472` | LoL:2900, LoL:1806–1810 |
| 8E | setSpecialSceneButtons | X, Y, width, height, enable flags | Sets special-scene buttons in the rectangle. | 5 | 5 | `0x30E97` | `0x37477` | LoL:2901, LoL:1812–1816 |
| 8F | restoreButtonsAfterSpecialScene | — | Restores normal buttons after a special scene. | 4 | 4 | `0x30E9C` | `0x3747C` | LoL:2902, LoL:1818–1822 |
| 90 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30EA1` | `0x37481` | LoL:2905, VM:309–321 |
| 91 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30EA6` | `0x37486` | LoL:2906, VM:309–321 |
| 92 | prepareSpecialScene | field type, dialogue flag, suspend GUI, allow scene update, control mode, fade flag | Prepares a special scene. | 37 | 37 | `0x30EAB` | `0x3748B` | LoL:2907, LoL:1824–1828 |
| 93 | restoreAfterSpecialScene | fade flag, redraw playfield, release TIM scripts, scene update mode | Restores after a special scene and returns status. | 45 | 45 | `0x30EB0` | `0x37490` | LoL:2908, LoL:1830–1833 |
| 94 | assignCustomSfx | filename (TEXT), sound ID | Assigns a custom filename to a mapped sound entry. | 203 | 202 | `0x30B76` | `0x37181` | LoL:2911, LoL:1835–1851 |
| 95 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x30B7B` | `0x37186` | LoL:2912, VM:309–321 |
| 96 | findAssignedMonster | block, previous object or −1 | Returns next assigned monster index or −1. | 22 | 22 | `0x15DFF` | `0x1A6F2` | LoL:2913, LoL:1853–1862 |
| 97 | checkBlockForMonster | block, monster or −1 | Looks for a monster within the initial monster portion of the block list. | 4 | 4 | `0x15E77` | `0x1A76A` | LoL:2914, LoL:1864–1876 |
| 98 | crossFadeRegion | source X, source Y, destination X, destination Y, width, height, source page, destination page | Crossfades a screen region. | 10 | 10 | `0x15EDF` | `0x1A7D2` | LoL:2917, LoL:1878–1882 |
| 99 | calcCoordinatesAddDirectionOffset | X, Y, direction, return X flag | Offsets coordinates in a direction and returns one axis. | 4 | 4 | `0x15F84` | `0x1A877` | LoL:2918, LoL:1884–1890 |
| 9A | resetPortraitsAndDisableSysTimer | — | Resets portraits and suspends the system timer. | 15 | 15 | `0x30EB5` | `0x37495` | LoL:2919, LoL:1892–1896 |
| 9B | enableSysTimer | — | Clears scene restore request and enables system timer 2. | 18 | 17 | `0x30EBA` | `0x3749A` | LoL:2920, LoL:1898–1903 |
| 9C | checkNeedSceneRestore | — | Reads scene restore request. | 13 | 13 | `0x30EBF` | `0x3749F` | LoL:2923, LoL:1905–1908 |
| 9D | getNextActiveCharacter | restart | Starts or advances active-character iteration and returns slot or −1. | 4 | 4 | `0x15FF2` | `0x1A8E5` | LoL:2924, LoL:1910–1923 |
| 9E | paralyzePoisonCharacter | character, effect type flag, immunity flags, hit chance, redraw | Attempts a paralysis or poison effect. | 4 | 4 | `0x1603C` | `0x1A92F` | LoL:2925, LoL:1925–1928 |
| 9F | drawCharPortrait | character or −1 | Redraws a portrait and stats or redraws all of them. | 1 | 1 | `0x1609E` | `0x1A991` | LoL:2926, LoL:1930–1938 |
| A0 | removeInventoryItem | type index | Removes the first matching inventory or equipment reference and returns success. | 1 | 1 | `0x160D4` | `0x1A9C7` | LoL:2929, LoL:1940–1963 |
| A1 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x161A7` | `0x1AA9A` | LoL:2930, VM:309–321 |
| A2 | Unimplemented | Unknown | VM returns 0 in ScummVM. | 0 | 0 | `0x161C4` | `0x1AAB7` | LoL:2931, VM:309–321 |
| A3 | getAnimationLastPart | animation slot | Returns and resets the last animation part. | 9 | 9 | `0x161E1` | `0x1AAD4` | LoL:2932, LoL:1965–1968 |
| A4 | assignSpecialGuiShape | wall shape index, subshape, X, Y, mirror | Sets a special GUI shape, or clears it for first argument 0. | 2 | 2 | `0x30CAD` | `0x372AD` | LoL:2935, LoL:1970–1983 |
| A5 | findInventoryItem | skip inventory flag, character selector, type index | Returns 0 for inventory hit, otherwise an eligible character slot or −1. In this handler the equipment loop covers all four slots for selector −1 and is empty for a concrete slot. | 3 | 3 | `0x1621F` | `0x1AB12` | LoL:2936, LoL:1985–2012 |
| A6 | restoreFadePalette | — | Restores and applies saved palette colors. | 1 | 1 | `0x1625D` | `0x1AB50` | LoL:2937, LoL:2014–2020 |
| A7 | calcNewBlockPosition | block, direction | Returns the neighboring block in that direction. | 4 | 4 | `0x162AA` | `0x1AB9A` | LoL:2938, LoL:2275–2278 |
| A8 | getSelectedCharacter | — | Returns selected character slot. | 1 | 1 | `0x162A1` | `0x1AB91` | LoL:2941, LoL:2022–2025 |
| A9 | setHandItem | item | Sets held item. | 1 | 1 | `0x162D6` | `0x1ABC6` | LoL:2942, LoL:2027–2031 |
| AA | drinkBezelCup | cup variant selector, character | Applies Bezel Cup use with variant 3 minus the selector. | 1 | 1 | `0x30729` | `0x36CFF` | LoL:2943, LoL:2033–2037 |
| AB | changeItemTypeOrFlag | item, selector, value | Writes type for selector 4 or the low 13 frame/flag bits for selector 15. | 2 | 2 | `0x139DA` | `0x1839D` | LoL:2944, LoL:2039–2055 |
| AC | placeInventoryItemInHand | type index, redraw | Swaps the first matching inventory item with the held item and returns the old hand handle or −1. | 12 | 13 | `0x162F3` | `0x1ABE3` | LoL:2947, LoL:2057–2080 |
| AD | castSpell | character, spell, level | Casts a spell and returns its status. | 5 | 5 | `0x1631F` | `0x1AC0F` | LoL:2948, LoL:2082–2085 |
| AE | pitDrop | mode | Plays a pit-drop animation, sound and optional shake. | 28 | 28 | `0x30FF5` | `0x375D5` | LoL:2949, LoL:2087–2118 |
| AF | increaseSkill | character, skill | Grants enough experience to reach the current threshold and returns the level increase. | 1 | 1 | `0x30EC4` | `0x374A4` | LoL:2950, LoL:2120–2127 |
| B0 | paletteFlash | color selector | Flashes and restores the palette. | 11 | 11 | `0x1635D` | `0x1AC4D` | LoL:2953, LoL:2129–2182 |
| B1 | restoreMagicShroud | — | Plays the magic shroud restoration animation and palettes. | 1 | 1 | `0x16461` | `0x1AD63` | LoL:2954, LoL:2184–2251 |
| B2 | dummy1 | — | Returns 1 through the same handler as 0x7D. | 9 | 8 | `0x30EDD` | `0x374BD` | LoL:2955, LoL:1620–1622 |
| B3 | disableControls | mode | Disables controls. | 6 | 6 | `0x30ED3` | `0x374B3` | LoL:2956, LoL:2253–2256 |
| B4 | enableControls | — | Enables controls. | 4 | 4 | `0x30ED8` | `0x374B8` | LoL:2959, LoL:2258–2261 |
| B5 | shakeScene | duration, width, height | Shakes scene and restores it afterwards. | 6 | 6 | `0x164D8` | `0x1ADDA` | LoL:2960, LoL:2263–2267 |
| B6 | gasExplosion | block | Processes a gas explosion. | 3 | 3 | `0x308CF` | `0x36E9F` | LoL:2961, LoL:2269–2273 |
| B7 | calcNewBlockPosition | block, direction | Returns neighboring block, alias of 0xA7. | 1 | 1 | `0x165F8` | `0x1AEFA` | LoL:2962, LoL:2275–2278 |
| B8 | crossFadeScene | — | Draws and crossfades the scene, then refreshes page 2. | 3 | 3 | `0x1674F` | `0x1AFE9` | LoL:2965, LoL:2280–2286 |
| B9 | updateDrawPage2 | — | Updates draw page 2. | 13 | 13 | `0x16788` | `0x1B022` | LoL:2966, LoL:2288–2292 |
| BA | setMouseCursor | cursor mode | Sets icon 133 for mode 1, otherwise uses the held item cursor. **CONFIRMED** The floppy slot points to the return-zero stub. | 2 | 0 | `0x30F28` | `0x17DEF` | LoL:2967, LoL:2294–2301 |
| BB | characterSays | track, character ID, redraw | In talkie mode plays speech, stops it for track −1 or polls it for track −2. Returns 0 in floppy mode. | 20 | 0 | `0x16795` | — | LoL:2968, LoL:2303–2318 |
| BC | queueSpeech | speech ID, speaker | Queues speech ID plus 1000 if both arguments are nonzero. | 8 | 0 | `0x1680B` | — | LoL:2971, LoL:2320–2327 |
| BD | getItemPrice | price operand | For negative input, rounds the magnitude up to a hundred with a 50 minimum for values below 50. For nonnegative input, chooses the first price threshold at least that large or returns 0. | 11 | 0 | `0x16837` | — | LoL:2972, LoL:2329–2347 |
| BE | getLanguage | — | Returns current language index. | 5 | 0 | `0x16898` | — | LoL:2973, LoL:2349–2352 |
| BF | dummy0 | — | Returns 0 through the same handler as 0x3E. | 0 | 0 | `0x1342C` | — | LoL:2974, LoL:915–917 |

## Edition differences and verification

- **CONFIRMED** Both editions have the same 60 script names. CD and floppy share 24 byte-identical files, all INI. Read the test results and PAK offsets below to reproduce the comparison.
- **CONFIRMED** Call IDs present only on CD are 0xBA–0xBE (0xBA is called twice on CD and never on floppy, although the floppy executable's table has a slot for it). Examples are `L03.PAK+0x4CA6` (0xBB) and `L01.PAK+0xD2A3`, `+0xD255`, `+0xDA6B` (0xBC, 0xBD, 0xBE). Floppy-only 0x80 appears at `CHAPTER1.PAK+0x5E047`. The call-site totals above describe these particular corpora.
- **CONFIRMED** Dispatch slot 0x7E is called once on CD at `L02.PAK+0xF40D` and twice on floppy at `CHAPTER1.PAK+0x5B351` and `CHAPTER5.PAK+0x2C68C`. Both native handlers take zero stack arguments, run update callbacks and return 1, as shown in the function table. Further downstream effects remain **UNCONFIRMED**. ScummVM leaves it unimplemented (LoL:2877, VM:309–321).
- **CONFIRMED** All 60 members per edition decompile with zero invalid opcode numbers, out-of-range function IDs, or invalid branch targets using the input members below. DATA word totals include ORDR headers and operand words. Counts are static, including instructions outside the external entry points.

| Edition | Files | DATA words | Instructions | TEXT indexes | Files with TEXT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Reference CD | 60 | 124,298 | 109,845 | 756 | 54 |
| LANDSoL floppy | 60 | 120,706 | 106,782 | 746 | 54 |

**CONFIRMED** VM opcodes 0x01, 0x12 have no static occurrence in either edition. The function table uses the full dispatch numbering, including slots the scripts never call. VM:29–55 and LoL:2683–2974.

### Corpus locations

**CONFIRMED** These are PAK member start byte offsets. For level rows the same PAK contains the INF and INI. The final two rows use one entry per edition.

| Script base | CD PAK | CD INF | CD INI | LANDSoL PAK | Floppy INF | Floppy INI |
| --- | --- | --- | --- | --- | --- | --- |
| LEVEL1 | `L01.PAK` | `0xC259` | `0xF225` | `CHAPTER1.PAK` | `0x577BD` | `0x619C5` |
| LEVEL2 | `L02.PAK` | `0xE735` | `0x10D77` | `CHAPTER1.PAK` | `0x5A679` | `0x61C63` |
| LEVEL3 | `L03.PAK` | `0x2A28` | `0x541C` | `CHAPTER1.PAK` | `0x5CC15` | `0x621AB` |
| LEVEL4 | `L04.PAK` | `0xA5E2` | `0xBB2A` | `CHAPTER1.PAK` | `0x5F4DD` | `0x6279B` |
| LEVEL5 | `L05.PAK` | `0x2BE` | `0x12BC` | `CHAPTER1.PAK` | `0x609C9` | `0x62EA7` |
| LEVEL6 | `L06.PAK` | `0xE201` | `0xF721` | `CHAPTER2.PAK` | `0x1E5E3` | `0x254EB` |
| LEVEL7 | `L07.PAK` | `0x6C6A` | `0x8F72` | `CHAPTER2.PAK` | `0x1FA91` | `0x25A03` |
| LEVEL8 | `L08.PAK` | `0xB138` | `0xD34C` | `CHAPTER2.PAK` | `0x21D1F` | `0x25FD7` |
| LEVEL9 | `L09.PAK` | `0x5DAC` | `0x73B0` | `CHAPTER2.PAK` | `0x23EF5` | `0x263F7` |
| LEVEL10 | `L10.PAK` | `0xA756` | `0xD166` | `CHAPTER3.PAK` | `0x3975A` | `0x3FB3E` |
| LEVEL11 | `L11.PAK` | `0x137D0` | `0x17B0C` | `CHAPTER3.PAK` | `0x3BDF4` | `0x3FFE0` |
| LEVEL12 | `L12.PAK` | `0xC650` | `0xF5D4` | `CHAPTER4.PAK` | `0x15696` | `0x1ED4C` |
| LEVEL13 | `L13.PAK` | `0x77BE` | `0x8BEA` | `CHAPTER4.PAK` | `0x17FAE` | `0x1F0A4` |
| LEVEL14 | `L14.PAK` | `0x6C35` | `0x8E6F` | `CHAPTER4.PAK` | `0x193C0` | `0x1F4C8` |
| LEVEL15 | `L15.PAK` | `0xDAB3` | `0xF8E9` | `CHAPTER4.PAK` | `0x1B5B8` | `0x1F840` |
| LEVEL16 | `L16.PAK` | `0xCA7` | `0x27AD` | `CHAPTER4.PAK` | `0x1D396` | `0x1FC82` |
| LEVEL17 | `L17.PAK` | `0x9676` | `0xB228` | `CHAPTER5.PAK` | `0x27990` | `0x2FB78` |
| LEVEL18 | `L18.PAK` | `0x9C43` | `0xBCF7` | `CHAPTER5.PAK` | `0x29520` | `0x300EC` |
| LEVEL19 | `L19.PAK` | `0x5293` | `0x64D9` | `CHAPTER5.PAK` | `0x2B628` | `0x30874` |
| LEVEL20 | `L20.PAK` | `0xFC21` | `0x113F5` | `CHAPTER5.PAK` | `0x2C8D4` | `0x30D3C` |
| LEVEL21 | `L21.PAK` | `0x394E` | `0x5448` | `CHAPTER5.PAK` | `0x2E08E` | `0x310B2` |
| LEVEL22 | `L22.PAK` | `0x6AB5` | `0xBA8F` | `CHAPTER6.PAK` | `0x63B61` | `0x6E725` |
| LEVEL23 | `L23.PAK` | `0x9F64` | `0xD164` | `CHAPTER6.PAK` | `0x68917` | `0x6EC79` |
| LEVEL24 | `L24.PAK` | `0xB41A` | `0xD834` | `CHAPTER6.PAK` | `0x6BABB` | `0x6F2F3` |
| LEVEL25 | `L25.PAK` | `0x166` | `0xB4C` | `CHAPTER6.PAK` | `0x6DD43` | `0x6F66B` |
| LEVEL26 | `L26.PAK` | `0x7FF4` | `0xAAF4` | `CHAPTER7.PAK` | `0x144DC` | `0x16FC4` |
| LEVEL27 | `L27.PAK` | `0x8381` | `0xAB07` | `CHAPTER8.PAK` | `0x39FFC` | `0x3C78E` |
| LEVEL28 | `L28.PAK` | `0xF6C9` | `0x13881` | `CHAPTER8.PAK` | `0x3CB80` | `0x40CA8` |
| LEVEL29 | `L29.PAK` | `0x3F9BD` | `0x42517` | `CHAPTER8.PAK` | `0x41080` | `0x43BC4` |
| ITEM | `STARTUP.PAK` | `0x10D25` | — | `GENERAL.PAK` | `0xD982C` | — |
| ONETIME | `STARTUP.PAK` | `0x2127B` | — | `GENERAL.PAK` | `0xDAAD2` | — |


The static test verifies instruction boundaries, names and dispatch indexes. Runtime behavior for handlers documented only from ScummVM remains **UNCONFIRMED** on DOS. VM:187–221 and LoL:2683–2974.
