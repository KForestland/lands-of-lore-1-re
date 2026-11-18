# Q15 — ADL records and the C55 music set

## C55

**CONFIRMED** C55 is the XMIDI set for General MIDI and Roland GS (the Sound Canvas family). In both original executables the audio selector string table pairs `MT32MPU.ADV` with `XMI` and then pairs the same driver with `C55`. The next entry pairs `ADLIB.ADV` with `ADL` (CD `MAIN.EXE+0x3363A–0x33667`, floppy `MAIN.EXE+0x392D1–0x392FE`). ScummVM selects `.C55` for General MIDI and `.XMI` for MT-32, and uses its XMIDI parser for both (`engines/kyra/sound/sound_pc_midi.cpp:34–50,440–452`, upstream `3b4db303`).

**CONFIRMED** All 17 CD and 19 floppy C55 files start with IFF `FORM` and type `XDIR`. For example, `LORE01A.C55` begins with `FORM 00 00 00 0E XDIR INFO 00 00 00 02 0B 00`, describing 11 sequences (CD `MUSIC.PAK+0x479D0`, floppy `CHAPTER1.PAK+0x8106E`). The dedicated `LOLSYSEX.C55` setup sequence contains Roland's GS reset bytes `41 10 42 12 40 00 7F 00 41` (CD `GENERAL.PAK+0x31DC`, floppy `GENERAL.PAK+0x9134`, matched to `audio/mididrv.cpp:457–464`). The original track set and its reset message support reading the name as a Sound Canvas/SC-55 designation. The literal expansion Westwood used for “C55” remains **UNCONFIRMED**. The shipped selector spells the extension only, at CD `MAIN.EXE+0x33656` and floppy `MAIN.EXE+0x392ED`. A contemporary setup manual, driver-selection label or Westwood asset manifest spelling it out would settle the name.

## ADL file and offset tables

**CONFIRMED** LoL1 ADL files store Westwood AdLib driver programs and instrument records. Let `B` be the byte offset of the sound data within the ADL file. All subsequent offsets stored in the two offset tables are relative to `B`. Numeric fields longer than one byte are little-endian. Data layout agrees with ScummVM's full-game version-4 reader for the 16 CD files and 17 of the 18 floppy files (`engines/kyra/sound/sound_pc_v1.cpp:53–56,161–172,240–258`, `engines/kyra/sound/drivers/adlib.cpp:166–171,319–323`, `engines/kyra/sound/drivers/pc_base.h:55–74`). The floppy `LORESFX.ADL` short-ID variant is established by the original bytes below.

| File offset | Size | Field and interpretation |
| --- | ---: | --- |
| `0` | 500 normally | 250 track IDs, each a `u16`. Entry `t` at `2t` is a program ID. `FFFF` is an empty track. `B=500`. |
| `0`, floppy `LORESFX.ADL` | 250 | 250 track IDs, each a `u8`. Entry `t` at `t` is a program ID. `FF` is the empty-track code in this map. `B=250`. |
| `B+0x000` | 1000 | 500 `u16` program offsets. Program `p` starts at `B + word(B + 2p)`. |
| `B+0x3E8` | 1000 | 500 `u16` instrument offsets. Instrument `i` starts at `B + word(B + 1000 + 2i)`. |
| `B+0x7D0` onwards | variable | Program bodies, instrument records and bytecode-addressed data. Program 0 begins here in all 34 files. |

**CONFIRMED** The program and instrument tables have both `0000` and `FFFF` empty entries. Offsets can repeat. File size bounds each reference and no length field follows the offset. A track may refer to a missing program. For example, CD `LORESFX.ADL` track 198 at `GENERAL.PAK+0x5F2` contains `0025`, and program 37 is `FFFF` at `GENERAL.PAK+0x6A4`. The lookup reader skips zero and out-of-bounds offsets (`engines/kyra/sound/drivers/pc_base.h:55–74`).

## Program bytes and instrument fields

**CONFIRMED** The ScummVM reader treats program byte +0 as the channel and byte +1 as priority. Channels 0–8 have hardware voices, 9 is the control channel, and values above 9 are rejected by that reader. A program starts when its priority is ≥ the priority already playing on that channel. Bytecode starts at +2 (`engines/kyra/sound/drivers/adlib.cpp:534–566,682–685,886–890`).

| Bytecode form | Fields | ScummVM lines in `engines/kyra/sound/drivers/adlib.cpp` |
| --- | --- | --- |
| `00–7F duration` | Packed note byte and one-byte duration. The low nibble supplies the note and the high nibble the octave, with channel base offsets applied. | 703–742, 886–907 |
| `80 count`, `81 delta16` | Set loop count and decrement/test it with a signed relative branch when nonzero. | 1270–1286, 2051–2054 |
| `82 program` | Launch the referenced one-byte program ID on its own channel. | 1288–1346, 2055 |
| `84 delta16`, `85 delta16`, `86` | Jump, call, return. In this sound layout the signed displacement is relative to the position after the operands. | 1354–1397, 2058–2061 |
| `88`, `89 duration`, `8A register value` | Stop channel, play a rest, write an OPL register. | 1405–1421, 2064–2067 |
| `90 instrument`, `A6 tempo` | Select the one-byte instrument ID or set tempo. | 1503–1518, 2076–2077, 2106–2110 |
| Other `80–FF` | Function index is the low seven bits, clipped to the last entry by the reference. The opcode table specifies the byte count, including zero for stop-channel entries. | 703–723, 2051–2168 |

**CONFIRMED** An instrument record is 11 bytes. These are the OPL fields the reference consumes from the offset table. `r` is the operator-register offset for the current channel (`engines/kyra/sound/drivers/adlib.cpp:946–995,2170–2175`).

| Instrument field byte(s) | Contents | OPL destination |
| --- | --- | --- |
| 0, 1 | AM, vibrato, envelope type, key scale rate and frequency multiplier for operators 1 and 2 | `20h+r`, `23h+r` |
| 2 | Feedback and connection algorithm. Bit 0 controls whether both operators contribute directly. | `C0h+channel` |
| 3, 4 | Waveform selection for operators 1 and 2 | `E0h+r`, `E3h+r` |
| 5, 6 | Key-scale level and total level for operators 1 and 2. The player applies volume adjustments when writing them. | `40h+r`, `43h+r` |
| 7, 8 | Attack and decay rates for operators 1 and 2 | `60h+r`, `63h+r` |
| 9, 10 | Sustain levels and release rates for operators 1 and 2 | `80h+r`, `83h+r` |

## Worked examples

**CONFIRMED** CD `LORE01B.ADL` starts at `MUSIC.PAK+0x5398`. Track word 2 at `0x539C` is `0002`. Program table row 2 at `0x5590` is `1C38`. The program starts at `0x5398 + 0x1F4 + 0x1C38 = 0x71C4` with `09 04 AE 00 AF 00 A6 76 82 03 82 04 82 05 82 06 88`. Channel 9 and priority 4 precede the commands. The program sets tempo `0x76`, starts programs 3 through 6, and stops. The same file's instrument row 0 at `0x5974` holds `506E`, pointing to `21 21 0C 00 00 9F 00 53 6A 5A 1A` at `0xA5FA`. This gives operator multiplier fields `21 21`, feedback/connection `0C`, waveforms `00 00`, levels `9F 00`, attack/decay `53 6A`, and sustain/release `5A 1A` (opcode and instrument sources above).

**CONFIRMED** floppy `LORESFX.ADL` starts at `GENERAL.PAK+0x9D58` with `00 01 FF FF FF FF FF FF FF FF FF 40 41`. Program rows 0 and 1 at `0x9E52` and `0x9E54` hold `07D0` and `07EA`. Adding `B=0xFA` reaches valid channel-9 program headers `09 32` at `0xA622` and `0xA63C`. Treating the map as 500 bytes instead gives the apparent program-0 offset `0x0C2D` at `0x9F4C`, whose target begins with invalid channel `FF`. The 250-byte map gives valid program-data offsets, including 11-byte instrument records such as instrument 64 at `0xB53D`.

## Corpus checks and open details

**CONFIRMED** Read 16 CD and 18 floppy ADL files using the map width established from each file. All 3692 CD and 3761 floppy nonempty program offsets lie in the payload with at least two header bytes. All 3330 CD and 3448 floppy nonempty instrument offsets permit an 11-byte read. Nine CD and eight floppy track slots refer to empty program 37. Every nonempty CD program begins with a channel byte in 0–9. The 15 regular floppy level ADLs each have two out-of-range channel bytes at program IDs 217 and 218. For example, in `CHAPTER1.PAK` for `LORE01B.ADL`, words at `0x684CE, 0x684D0` point to `8E 20` and `8E 83` at `0x691C1, 0x691B4`. The corresponding CD programs begin with `06 40` at `MUSIC.PAK+0x61E7, +0x61F4`.

**UNCONFIRMED** No native playback trace identifies whether the floppy driver reads those two program entries or selects the short track map from a file-specific flag. The data test compared 250- and 500-byte bases against both offset tables, channel bytes and record bounds. To settle the native rules, trace the AdLib driver entry for a `LORESFX.ADL` track lookup and watch accesses to offset-table rows 217 and 218 during a floppy level sound event. The source reader's invalid-channel behavior is documented at `engines/kyra/sound/drivers/adlib.cpp:538–543,1305–1312`.

| ADL asset | CD archive and start | floppy archive and start |
| --- | --- | --- |
| `LORE01A` | `MUSIC.PAK+0x3C9` | `CHAPTER1.PAK+0x63159` |
| `LORE01B` | `MUSIC.PAK+0x5398` | `CHAPTER1.PAK+0x68128` |
| `LORE01C` | `MUSIC.PAK+0xA6F7` | `CHAPTER1.PAK+0x6D487` |
| `LORE01D` | `MUSIC.PAK+0xF32E` | `CHAPTER1.PAK+0x720F8` |
| `LORE02A` | `MUSIC.PAK+0x13CE4` | `CHAPTER2.PAK+0x26703` |
| `LORE03A` | `MUSIC.PAK+0x195A1` | `CHAPTER3.PAK+0x53D` |
| `LORE03B` | `MUSIC.PAK+0x1E9AD` | `CHAPTER3.PAK+0x5949` |
| `LORE04A` | `MUSIC.PAK+0x21488` | `CHAPTER4.PAK+0x4D1` |
| `LORE05A` | `MUSIC.PAK+0x24FCA` | `CHAPTER5.PAK+0x4C7` |
| `LORE05B` | `MUSIC.PAK+0x293B1` | `CHAPTER5.PAK+0x48AD` |
| `LORE06A` | `MUSIC.PAK+0x2F225` | `CHAPTER6.PAK+0x80D` |
| `LORE06B` | `MUSIC.PAK+0x339AF` | `CHAPTER6.PAK+0x4F97` |
| `LORE07A` | `MUSIC.PAK+0x39374` | `CHAPTER7.PAK+0x1C1` |
| `LORE08A` | `MUSIC.PAK+0x3BFE9` | `CHAPTER8.PAK+0x21E7` |
| `LORE08B` | `MUSIC.PAK+0x41A98` | `CHAPTER8.PAK+0x7C96` |
| `LOREFINL` | — | `FINALE2.PAK+0x77BED` |
| `LOREINTR` | — | `INTROVOC.PAK+0x8B4D5` |
| `LORESFX` | `GENERAL.PAK+0x466` | `GENERAL.PAK+0x9D58` |

## MIDI note projection

**CONFIRMED** `tools/adl_to_midi.py` reads the two original ADL track maps above, validates the program and instrument table offsets, and projects one track to Standard MIDI. The projection runs the timing and control instructions at 72 callbacks per second. A channel advances when its timer byte wraps, channels run in descending order, and channel 9 has no mapped notes. MIDI uses 36 ticks per quarter at 500,000 μs per quarter, making one MIDI tick one driver callback. Note selection uses the packed low nibble and octave block with the channel offsets. The MIDI pitch uses 12 times the adjusted block plus 12, then adds the adjusted note. This convention assigns MIDI note 12 to block 0 note 0. The reference is `engines/kyra/sound/drivers/adlib.cpp:45,147–155,494–507,650–743,872–907,1270–1433,1465–1501,1583–1638,1782–1798,2030–2039,2051–2166` at upstream `3b4db303`. The original CD `LORE01B.ADL` track-2 controller at `MUSIC.PAK+0x71C4` gives 94 note-on events over the first ten seconds, with the MIDI independently parsed after writing.

**CONFIRMED** The four-second check passes in each edition. It visits each distinct playable entry offset in each original file (archive offsets in the table above), records unavailable IDs and re-reads every generated MIDI stream. CD gives 2,207 entries, 2,158 with notes and nine unavailable IDs. floppy gives 2,235 entries, 2,181 with notes and 23 unavailable IDs, including programs with out-of-range channel bytes. floppy `LORESFX.ADL` ID 66 (slots 47, 211 and 228) reaches `81 41 22` at `GENERAL.PAK+0xA6DE`. Treating that as a relative repeat goes to sound-data offset `0x2AD0`, beyond the `0x1E2B`-byte sound data. The check expects this exact exception and the projection skips that branch, consistent with the guard in `adlib.cpp:1275–1285`.

**UNCONFIRMED** The native timing and note equivalence of FM-only effects is still open. The projection shows the note timeline with fixed MIDI velocity and default instrument sound, and reports unmapped opcodes. It does not project OPL instruments, OPL register writes, pitch effects, rhythm section controls or sound-trigger callbacks. For example, CD `MUSIC.PAK+0x71C4` runs `AE` and `AF`, which adjust OPL depth in `adlib.cpp:1684–1702`. This is a finite playback of looping material, with a selectable cutoff. A register-write capture from the original AdLib driver would settle the native effect order and the short-map repeat behavior.
