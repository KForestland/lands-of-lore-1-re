# Q10. The 59 speech-archive entries named 00000.VOC

They are not 59 names. They are one clip, stored under the single name `00000.VOC`, twice in most of the speech archives. No script, sound list or play call found in this pass opens that name. Who plays it is still open.

## What was measured

CONFIRMED on the CD speech archives `00.TLK` through `29.TLK`. LANDSoL has no `.TLK` files. This question is the CD edition.

There are 59 directory entries. Every one is named `00000.VOC`, every one is 44115 bytes, and every one shares MD5 prefix `d454b505`. The first 19 bytes are `Creative Voice File`. Archives 00 through 24 and 26 through 29 each hold two copies. `25.TLK` holds one. 29 times 2, plus 1, is 59.

In `01.TLK` the two copies sit at archive offsets 6640 and 26362517. Same length, same hash. The second copy is the same bytes again, not a second line of speech.

A search of the root PAK files for the ASCII name `00000.VOC`, and for a `00000` string ending in a zero byte inside a `.TIM`, `.INF` or `.INI` member, found nothing. The character-speech builder never produces this name. For a line under 1000 it builds `%03d` plus a speaker character plus a digit plus `.` plus the two-digit archive number (`engines/kyra/sound/sound_lol.cpp:63-75`). `isVoicePresent` then appends `.VOC` (`engines/kyra/sound/sound.cpp:53-61` and the extension table at `:345-347`). A speaker of `0` and a line of 0 in archive 01 looks up `00000.01.VOC`, not `00000.VOC`. The five-digit form `@%04d` is used only for ids of 1000 and above, and it keeps the speaker character (`sound_lol.cpp:66`).

The effect player speaks whatever string is in the effect slot (`sound_lol.cpp:180-190`). The CD slot list is the placeholder `XXXXXXXX` (`devtools/create_kyradat/resources/lol_dos_cd.h:65`), not `00000`. A script can replace a slot through `olol_assignCustomSfx` (`engines/kyra/script/script_lol.cpp:1835-1850`, opcode `0x94` at `:2911`). No script string in the PAK files is the stem `00000`.

The intro calls play `KING01`, `KING02`, `KING03` and `star2`. The character-select lines use stems such as `000A0` and `000M0`. None of those is `00000`.

## Where the name does sit

CONFIRMED as a filename in one executable, and not as a call. CD `ENG/FINALE.EXE` (132328 bytes) contains the ASCII string `00000.VOC` at file offset 123008. The bytes around it are a flat list: `TROT5.VOC`, then `00000.VOC`, then `CONGRATK.VOC`, `CONGRATA.VOC`, `CONGRATM.VOC`, `CONGRATC.VOC`, then `INTRO.FNT`. The same string is absent from CD `DATA/HARDRIVE/MAIN.EXE` (356928 bytes), CD `ENG/LANDS.EXE` (357509 bytes), and from LANDSoL `MAIN.EXE`, `LANDS.EXE` and `FINALE.EXE`.

ScummVM's outro command copies a name out of the TIM text and then deletes the last four characters (`engines/kyra/script/script_tim.cpp:699-731`). For talkie outro slot 2 it ignores that text and forces `CONGRATA.VOC`, then writes K, A, M or C at character 7 (`script_tim.cpp:705-723`). The play call appends `.VOC` again (`script_tim.cpp:746` through `sound.cpp:79-87`). No TIM member in the root archives contains `00000.VOC`. No ScummVM source contains that filename.

## What was tried

- Hashing all 59 entries. One clip.
- Searching script text, TIM text and the effect-name list for the stem.
- Reading the speech-name builder, the effect player, the custom-effect opcode, the intro and character-select calls, and the outro command.
- Searching the six executables for the filename.

## What would settle it

A call in CD `FINALE.EXE` that opens the filename at file offset 123008, or a TIM string stored in a form this scan does not see (the extension stripped already, or the text living outside the root archives). The filename's presence in that list is not a play call. Until one of those turns up, the player of `00000.VOC` stays UNCONFIRMED. The identity of the 59 entries is CONFIRMED: one 44115-byte clip, duplicated.
