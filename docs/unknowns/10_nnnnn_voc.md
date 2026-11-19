# Q10. The 59 speech-archive entries named 00000.VOC

They are not 59 names. They are one clip, stored under the single name `00000.VOC`, twice in most of the speech archives. No script, sound list or play call found so far opens that name. Who plays it is still open.

## What was measured

CONFIRMED on the CD speech archives `00.TLK` through `29.TLK`. floppy has no `.TLK` files. This question is the CD edition.

There are 59 directory entries. Every one is named `00000.VOC`, every one is 44115 bytes, and every one shares MD5 prefix `d454b505`. The first 19 bytes are `Creative Voice File`. Archives 00 through 24 and 26 through 29 each hold two copies. `25.TLK` holds one. 29 times 2, plus 1, is 59.

In `01.TLK` the two copies sit at archive offsets 6640 and 26362517. Same length, same hash. The second copy is the same bytes again, not a second line of speech. The two copies are the first and the last directory entries (indexes 0 and 505 of 507 in `01.TLK`); the other members are named like `000_0.01`, without `.VOC`. That position suggests a padding or marker entry (UNCONFIRMED). The same holds in every archive: `00000.VOC` is the first and the last directory entry of each of the 29 archives with two copies, and the only entry of `25.TLK`. The clip is not silence. It is one 8-bit block at 22222 Hz, 44082 samples (about 2 seconds), with values from 48 to 206. A reader that opens the first or last member of a `.TLK` would settle its role.

A search of every PAK (root, `ENG/` and floppy) for the ASCII name `00000.VOC`, and for a `00000` string ending in a zero byte inside a `.TIM`, `.INF` or `.INI` member, found nothing. That includes the outro TIM files in `ENG/FINALE2.PAK`, which belongs to `FINALE.EXE`. The character-speech builder never produces this name. For a line under 1000 it builds `%03d` plus a speaker character plus a digit plus `.` plus the two-digit archive number (`engines/kyra/sound/sound_lol.cpp:63-75`). `isVoicePresent` then appends `.VOC` (`engines/kyra/sound/sound.cpp:53-61` and the extension table at `:345-347`). A speaker of `0` and a line of 0 in archive 01 looks up `00000.01.VOC`, not `00000.VOC`. The five-digit form `@%04d` is used only for ids of 1000 and above, and it keeps the speaker character (`sound_lol.cpp:66`).

The effect player speaks whatever string is in the effect slot (`sound_lol.cpp:180-190`). The CD slot list is the placeholder `XXXXXXXX` (`devtools/create_kyradat/resources/lol_dos_cd.h:65`), not `00000`. A script can replace a slot through `olol_assignCustomSfx` (`engines/kyra/script/script_lol.cpp:1835-1850`, opcode `0x94` at `:2911`). No script string in the PAK files is the stem `00000`.

The intro calls play `KING01`, `KING02`, `KING03` and `star2`. The character-select lines use stems such as `000A0` and `000M0`. None of those is `00000`.

## Where the name does sit

CONFIRMED as a filename in the finale programs, and not as a call. CD `ENG/FINALE.EXE` (132328 bytes) contains the ASCII string `00000.VOC` once, at file offset 123008 (`0x1E080`). The bytes around it are a flat list: `TROT5.VOC`, then `00000.VOC`, then `CONGRATK.VOC`, `CONGRATA.VOC`, `CONGRATM.VOC`, `CONGRATC.VOC`, then `INTRO.FNT`. One relocated far pointer targets that string: the 20-byte catalog row at file `0x1D1D0` (segment `0x1ACB`, offset `0x320`, row 40). Its dword at +4 is `0xAC53` (44115), the same length as each speech-archive copy, and the word at +0x12 is `0x1000`. Startup sets DS to `0x1B5B` (`mov dx, 0x1B5B` at file `0x2200`). The name's offset in that segment is `0x08D0`, and those two bytes occur once in the file, inside the row. The lookup at file `0xCDD1` (`BA 14 00 F7 EA BA CB 1A`) multiplies an index from `es:[bx+0xC]` by `0x14` and uses segment `0x1ACB`. It does not name row 40; its index comes from a second 20-byte table at `0x1B41:0` that is zero in the file and filled at run time, so which rows it selects is not readable statically. It is one of about 20 sites that index segment `0x1ACB` by 20. The loop at `+0xF0B0–0xF127` does not look up a requested name: it compares each row's name with `.PAK` (see the startup sort below). French `FINALE.EXE` has the one string at `0x1E782` and German at `0x1E7DC`; each row is the same size and flags. The string is absent from CD `DATA/HARDRIVE/MAIN.EXE` (356928 bytes), from `ENG/LANDS.EXE` (357509 bytes, the intro), from `SETUP.EXE` and from `INSTALL.EXE`, and from every archive payload. Floppy `MAIN.EXE`, `LANDS.EXE` and `FINALE.EXE` were already searched and do not contain it.

**CONFIRMED** The catalog holds 93 occupied rows, indexes 0 through 92. Row 93, at file `0x1D5F4`, has a zero name pointer, and row 92 does not. Twelve instructions have the eight bytes `BA 14 00 F7 EA BA CB 1A` (multiply an index by `0x14`, segment `0x1ACB`), at file offsets `0xCDD1`, `0xCE81`, `0xCF2F`, `0xEA8C`, `0xEB29`, `0xF0BC`, `0xF0DE`, `0xF107`, `0xF138`, `0xF160`, `0xF17F` and `0xF1B0`. Other catalog accesses do not have that byte form: `0xCE4D` has `add ax, 0` before the segment; `0xEB47` and `0xEB9E` multiply by `0x14` and add the result to the catalog far pointer at `DS:0x1233`; `0xEA16`, `0xEA3F` and `0xEA7D–0xEAB3` pass that pointer (or row `[0x3776]`), a row count and the width `0x14` to library search calls, which look a row up by its contents rather than by a number. This list is what the review read, not a proof that no other access exists. Every index in it is computed: a run-time word (`[0x3776]`, `[0x3774]` plus `[0x3776]`, word +0xC of a row of the table at segment `0x1B41`), a register (`0xEB29` uses the function argument), or, at `0xCE4D`, the result of a library lookup on a name read byte by byte from an open file. No instruction loads the constant 40 as an index, and the two near callers of `0xEB05` (`0xE85A`, `0xE8A7`) do not push 40. That rules out only a literal 40; a computed index can still reach the row. `lol1_mode_paths.py --check` re-reads the row count, the twelve eight-byte sites and the absence of a literal 40 before them.

**CONFIRMED** Startup reorders the catalog. The routine at `0xF0B0`, called once at `0xEC3F` right after `DS:0x1233` is set to `0x1ACB:0`, upper-cases each name and steps `[0x3776]` while the name contains `.PAK` (library `strstr` at file `0x60F1`, pattern `DS:0x123E` = `.PAK`), which stops at row 4. It then counts the following rows with a nonzero, non-empty name into `[0x3774]` (89, rows 4 to 92) and calls the library routine at file `0x593D` with base row 4, count 89, width `0x14` and the compare function at file `0xF08D`, which compares the two rows' names.

**UNCONFIRMED** If `0x593D` is the C library sort, as its arguments indicate, the clip's row is 4 in memory after startup, not 40: `00000.VOC` sorts before every other name. Row 40 is then only its position in the file.

ScummVM's outro command copies a name out of the TIM text and then deletes the last four characters (`engines/kyra/script/script_tim.cpp:699-731`). For talkie outro slot 2 it ignores that text and forces `CONGRATA.VOC`, then writes K, A, M or C at character 7 (`script_tim.cpp:705-723`). The play call appends `.VOC` again (`script_tim.cpp:746` through `sound.cpp:79-87`). No TIM member in any archive contains `00000.VOC`. No ScummVM source contains that filename.

## What was tried

- Hashing all 59 entries. One clip.
- Searching script text, TIM text and the effect-name list for the stem.
- Reading the speech-name builder, the effect player, the custom-effect opcode, the intro and character-select calls, and the outro command.
- Searching the six executables for the filename, then the installer, the setup program and the French and German finale programs.
- Resolving the one far pointer at `ENG/FINALE.EXE+0x1D1D0` and the index times 20 lookup at `+0xCDD1`.

## What would settle it

A by-name request for `00000.VOC` that reaches the catalog (for example through the lookup that feeds `+0xCE4D`), or a writer that stores the clip's row index into word +0xC of a `0x1B41` row used at `+0xCDD1`, `+0xCE81` and `+0xCF2F`. No catalog-index instruction loads the constant 40, but every index is computed, and the startup sort (above) can move the clip to another row in memory. The catalog row is a registration of a 44115-byte file, not a play call. Until one of those turns up, the player of `00000.VOC` stays UNCONFIRMED. The identity of the 59 entries is CONFIRMED: one 44115-byte clip, duplicated. `lol1_name_callers.py --check` re-reads the row, the lookup bytes and the absence from programs, payloads and the installer. `lol1_mode_paths.py --check` re-reads the 93 rows, the twelve eight-byte index sites and the startup sort call.

## Close-out

**What was measured.** `ENG/FINALE.EXE` contains the eight bytes `BA 14 00 F7 EA BA CB 1A` at 12 file offsets, each a multiply by `0x14` then segment `0x1ACB`; `0xCE4D`, `0xEB47` and `0xEB9E` index the catalog by 20 in other forms. None is fed by the constant 40; all take a computed index. Row 93's name pointer is zero, so the occupied rows are 0 through 92. The routine at `0xF0B0` sorts rows 4 to 92 by name at startup.

**What was tried.** The scan counted that eight-byte sequence through the finale program, listed every relocated `0x1ACB` segment word (20) and every multiply by `0x14`, and read what feeds each catalog index. The page already resolved the catalog row at file `+0x1D1D0` and the lookup at `+0xCDD1`.

**What would settle it.** The test is the one under [What would settle it](#what-would-settle-it) above. The running-game test is not yet run ([probes not yet run](../NEEDS_A_RUNNING_GAME.md#probes-not-yet-run)).
