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

CONFIRMED as a filename in the finale programs, and not as a call. CD `ENG/FINALE.EXE` (132328 bytes) contains the ASCII string `00000.VOC` once, at file offset 123008 (`0x1E080`). The bytes around it are a flat list: `TROT5.VOC`, then `00000.VOC`, then `CONGRATK.VOC`, `CONGRATA.VOC`, `CONGRATM.VOC`, `CONGRATC.VOC`, then `INTRO.FNT`. One relocated far pointer targets that string: the 20-byte catalog row at file `0x1D1D0` (segment `0x1ACB`, offset `0x320`, row 40). Its dword at +4 is `0xAC53` (44115), the same length as each speech-archive copy, and the word at +0x12 is `0x1000`. Startup sets DS to `0x1B5B` (`mov dx, 0x1B5B` at file `0x2200`). The name's offset in that segment is `0x08D0`, and those two bytes occur once in the file, inside the row. The lookup at file `0xCDD1` (`BA 14 00 F7 EA BA CB 1A`) multiplies an index from `es:[bx+0xC]` by `0x14` and uses segment `0x1ACB`. It does not name row 40; its index comes from a second 20-byte table at `0x1B41:0` that is zero in the file and filled at run time, so which rows it selects is not readable statically. It is one of about 20 sites that index segment `0x1ACB` by 20; the loop at `+0xF0B0–0xF118` compares every row's name with a requested name. French `FINALE.EXE` has the one string at `0x1E782` and German at `0x1E7DC`; each row is the same size and flags. The string is absent from CD `DATA/HARDRIVE/MAIN.EXE` (356928 bytes), from `ENG/LANDS.EXE` (357509 bytes, the intro), from `SETUP.EXE` and from `INSTALL.EXE`, and from every archive payload. Floppy `MAIN.EXE`, `LANDS.EXE` and `FINALE.EXE` were already searched and do not contain it.

ScummVM's outro command copies a name out of the TIM text and then deletes the last four characters (`engines/kyra/script/script_tim.cpp:699-731`). For talkie outro slot 2 it ignores that text and forces `CONGRATA.VOC`, then writes K, A, M or C at character 7 (`script_tim.cpp:705-723`). The play call appends `.VOC` again (`script_tim.cpp:746` through `sound.cpp:79-87`). No TIM member in any archive contains `00000.VOC`. No ScummVM source contains that filename.

## What was tried

- Hashing all 59 entries. One clip.
- Searching script text, TIM text and the effect-name list for the stem.
- Reading the speech-name builder, the effect player, the custom-effect opcode, the intro and character-select calls, and the outro command.
- Searching the six executables for the filename, then the installer, the setup program and the French and German finale programs.
- Resolving the one far pointer at `ENG/FINALE.EXE+0x1D1D0` and the index times 20 lookup at `+0xCDD1`.

## What would settle it

A caller that reaches row 40 by index through one of the segment-`0x1ACB` lookups (for example `ENG/FINALE.EXE+0xCDD1`), a by-name open of `00000.VOC` through the row-name scan at `+0xF0B0`, or code that copies the name at DS:`0x08D0`. The catalog row is a registration of a 44115-byte file, not a play call. Until one of those turns up, the player of `00000.VOC` stays UNCONFIRMED. The identity of the 59 entries is CONFIRMED: one 44115-byte clip, duplicated. `lol1_name_callers.py --check` re-reads the row, the lookup bytes and the absence from programs, payloads and the installer.
