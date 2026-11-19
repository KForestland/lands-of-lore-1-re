# LoL1 save-game format

This page documents original DOS `_SAVE%03d.DAT` files, native `_LEVELn.TMP` sidecars and ScummVM `WWSV` saves. **CONFIRMED** labels observations from the original executables, original sidecars or actual ScummVM saves. The four `_LEVELn.TMP` witnesses were written by the original floppy program while one installation was played (one is dated 2006, the others 2004); they are not shipped, and a fresh install has none. The ScummVM saves are the maintainer's own. **UNCONFIRMED** labels fields whose meaning or exact original bytes remain unverified. ScummVM line numbers refer to revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`. `Save` and `Header` mean `engines/kyra/gui/saveload_lol.cpp` and `engines/kyra/gui/saveload.cpp`, respectively.

The CD addresses are file offsets in `DATA/HARDRIVE/MAIN.EXE`, identical to the member at `WESTWOOD.001+0x28C46`. The second edition is the floppy `MAIN.EXE`. See [Executable tables](executable_tables.md) for both images. Native multi-byte integers are little-endian. ScummVM save fields are big-endian except the compressed wrapper and individual bytes (Save:55–56,346–494).

Reader: `tools/save_reader.py FILE` prints these fields for all three kinds of file (`--json` for every field).

## Native header and section boundaries

**CONFIRMED** The executables contain the save filename pattern at CD `MAIN.EXE+0x32CB4` and floppy `MAIN.EXE+0x38ED5`. Native serializers write fixed-length sections in this order.

| Section | CD 1.02, file offset | floppy, file offset | Native writer evidence |
| --- | --- | --- | --- |
| Description | `0x0000`, 60 bytes | `0x0000`, 60 bytes | CD `+0x48B4D–0x48B59`; floppy `+0x521B8–0x521C4`. |
| Format tag | `0x003C`, 5 bytes `CD04\0` | `0x003C`, 5 bytes `.13\0_` | CD writes 5 bytes from `+0x32A3A` at `+0x48B5D–0x48B6A`. Floppy writes 5 from `+0x3891D` at `+0x521C8–0x521D5`. Floppy's fifth byte comes from the following literal. |
| Version text | `0x0041`, 11 bytes including NUL, `V CD1.02 D` for MAIN | — | CD `+0x48B6D–0x48B7A`, literal at `+0x32A3F`. `MAINW.EXE+0x324DF` contains the corresponding `V CD1.02 W` string. |
| Characters | `0x004C`, 4 × 130 | `0x0041`, 4 × 130 | CD `+0x48B7D–0x48B8F`; floppy `+0x521D8–0x521EA`. |
| Global state | `0x0254`, 563 bytes | `0x0249`, 557 bytes | CD `+0x48B92–0x48BA2`; floppy `+0x521ED–0x521FD`. |
| Item instance slots | `0x0487`, 400 × 16 | `0x0476`, 400 × 16 | CD `+0x48BAD–0x48BBF`; floppy `+0x52208–0x5221A`. Save:189–202 reads 400. |
| Level snapshot slots | `0x1D87`, 30 × 2500 | `0x1D76`, 30 × 2500 | CD `+0x48BC7–0x48C49`; floppy `+0x52222–0x522A4`. |
| Calculated EOF | `0x1427F` | `0x1426E` | Sum of serialized section lengths in the preceding rows. |

The floppy reader compares the five-byte field as a C string against `.13` at `MAIN.EXE+0x3890C`; the comparison stops at NUL (floppy `+0x51F95–0x51FC8`). **CONFIRMED** ScummVM's original-save recognition checks for `CD04` at a candidate description boundary and ` CD1` after advancing past two bytes. This matches the native CD header at the 60-byte boundary and brings its reader to offset `0x4C`. The branch recognizes only the CD signature for LoL (Header:54–101). **CONFIRMED** Three original CD 1.02 slots end at `0x1427F`. Their level, character, position and isolated-byte offsets match the native layout. **CONFIRMED** The floppy writer makes only fixed-length writes between its open at `+0x521AE` and its close at `+0x522A5`, all through the same write routine: `0x3C`, 5, `0x208`, `0x22D` and `0x1900` bytes, then 30 slots of (4 + `0x9C0`) bytes for a stored level or `0x9C4` bytes otherwise, 2,500 bytes each. There is no seek. The end at `0x1426E` assumes the open (floppy `+0x521AE` → `+0xB442`, mode 2) starts an empty file; that was not traced. A floppy save therefore ends at `0x1426E`. No floppy save file was checked. The general meanings of the skipped bytes remain **UNCONFIRMED**; [Q17](unknowns/17_native_save_fields.md) gives the memory-watch test for them. [CD save and load comparison](unknowns/17_native_save_fields.md#cd-movement-and-save-round-trip)

## ScummVM header

**CONFIRMED** In eleven local `lol-cd.*` save files, on-disk offset `0x00` is gzip magic `1F 8B`. The following layout uses the decompressed stream, with `lol-cd.001` as an example. The file is version 21. The current reference writer uses version 24 and emits these same header fields (Header:31,104–149,203–258; `backends/saves/default/default-saves.cpp:130,170`).

| Offset in decompressed stream | Field | `lol-cd.001` example |
| --- | --- | --- |
| `0x0000` | 4-byte `WWSV` | `WWSV` |
| `0x0004` | `u8` game ID | 4 |
| `0x0005` | `u32` save version | 21 |
| `0x0009` | NUL-terminated description. Versions up to 8 had a 31-byte field. Versions below 20 undergo conversion to UTF-8 on read. | Ends at `0x000D` inclusive. |
| After description | `u32` edition flags from version 2. Bit 0 floppy, bit 1 talkie/CD, bit 2 FM Towns/PC-98. | `0x000E` = 2 |
| After flags | Thumbnail from version 14. Its size field includes header and pixels. | `0x0012`, 32022 bytes |
| After thumbnail | Seven `i32` time/date fields in order: second, minute, hour, day of month, month, year, weekday. Present from version 21. | `0x7D28` |
| After date | `u32` total play seconds from version 21. | `0x7D44` |
| After header | 4 × 126-byte character records, then global state. | `0x7D48` |

**CONFIRMED** Thumbnail v2 starts with `THMB`, `u32` size, `u8` version, `u16` width and height, `u8` bytes per pixel, then RGBA loss and RGBA shift bytes. At relative `0x16` come row-major 2- or 4-byte big-endian pixels. `lol-cd.001+0x12` through `+0x7D27` has a 160 × 100, 2-byte-per-pixel thumbnail. Earlier thumbnail v1 uses RGB565 and a shorter header, and the reader also accepts the historical `BMHT` tag. `graphics/thumbnail.cpp:44,55–104,178–194,230–273`.

## Character records

**CONFIRMED** Native records use 130 bytes, with the same field boundaries as the [native character default record](executable_tables.md#character-default-record). The native loader rebinds the four-byte pointer at `+0x13`. ScummVM skips that field when importing and writes 126-byte records without it. For every field from native offset `+0x17` onward, subtract four for ScummVM. The 11 equipment words in saves contain item handles. The native writer ranges above and ScummVM `lol-cd.001+0x7D48` through `+0x7F3F` establish the strides (Save:55–105,346–384; CD `MAIN.EXE+0x48923–0x4898B`, floppy `+0x51FE2–0x5204A`).

## Global state

[Native fields skipped during ScummVM import](unknowns/17_native_save_fields.md) gives the original options and audio fields.

Offsets below are decimal relative to the start of global state, using version 21 for the ScummVM column. Field order comes from Save:107–202 and 386–430. **CONFIRMED** The serialization boundaries, native level index and mask are also anchored by CD `MAIN.EXE+0x48B02, +0x48BD8` and floppy `+0x52173, +0x52233`. Native fields that the reference skips are **UNCONFIRMED** except where noted. [Q17](unknowns/17_native_save_fields.md) gives the memory-watch test for each. In ScummVM rows after the flags, `F` is the stored flag byte count.

| Native | ScummVM | Type and field |
| ---: | ---: | --- |
| 0, 2, 4, 6 | 0, 2, 4, 6 | `u16` current block, party X, party Y, update flags |
| 8, 9 | 8, 9 | `u8` script direction, selected spell |
| 10 | — | A native `u16` options word with difficulty in bits 4–5 in both editions. See CD `MAIN.EXE+0xCC86–0xCC93` and floppy `MAIN.EXE+0x10498–0x104A5`; ScummVM skips both bytes (Save:114–115). |
| 12, 13, 14 | 10, 11, 12 | `u8` scene default update, compass broken, drain magic |
| 15, 17 | 13, 15 | `u16` facing, compass direction |
| 19 | 17 | `i8` selected character |
| 20 | — | 1 original byte skipped |
| 21 | 18 | `u8` current level |
| 22 | 19 | 48 × `i16` inventory item handles |
| 118, 120, 122 | 115, 117, 119 | `i16` inventory cursor/scroll index, held item handle, last mouse region |
| — | 121 | `u32` byte count `F` of flags, 100 in the checked version 21 files |
| 124 | 125 | Native 40 × `u16` game-flag words, ScummVM `F` raw packed bytes. Flag ID is 16 × word index plus bit index in native saves. Save:134–159. |
| 204 | — | 120 additional bytes from the native flag-table span, skipped |
| 324 | 125 + F | 24 × `u16` script globals |
| 372 | — | 152 additional bytes from the native script-global span, skipped |
| 524, 525, 526 | 173 + F, 174 + F, 175 + F | `u8` brightness, `u8` lamp oil, `i8` lamp effect |
| 527 | — | 1 original byte skipped |
| 528 | 176 + F | `u16` money/credits |
| 530 | 178 + F | 8 × `u16` secondary script globals |
| 546 | 194 + F | Seven available-spell bytes |
| 553 | 201 + F | `u32` level mask. Bit 0 is the level 1 snapshot. |
| 557 | — | Six more bytes in CD only. The first five are language, dialogue text, talking volume, sound volume and music volume. The last byte is **UNCONFIRMED**. It is zero after startup, and only the bulk save and load touched it in the CD round trip. A memory watch on CD `DS:8202` during a lamp change, a party change and a level transition would settle it. See [Q17](unknowns/17_native_save_fields.md) for the native readers. |

**UNCONFIRMED** Legacy ScummVM layouts have no example files checked here. A ScummVM LoL save of version 14, 15 or 16 would settle them. The reader skips 80 bytes after characters for versions below 17, and four bytes after each item slot. Its version 14 flags comprise words 0–15, 26 and 36. Version 15 reads 40 words. Version 16 onward reads a count and a byte array (Save:104–105,134–159,189–202).

## Item instance record

The **CONFIRMED** block boundaries above give 400 packed 16-byte item records in both native saves and the checked ScummVM saves. Field offsets here are hex, using the serialized layout in Save:189–202,419–429 and `engines/kyra/engine/lol.h:114–121,150–154`. Item property indexes refer to the script definitions described in [Executable tables](executable_tables.md#item-types-and-item-properties).

| Offset | Field |
| --- | --- |
| `00`, `02` | `u16` next assigned-object handle and next draw-object handle |
| `04` | `u8` flying height |
| `05`, `07`, `09` | `u16` block, X, Y |
| `0B` | `i8` level |
| `0C` | `u16` item property index |
| `0E` | `u16` current shape/frame and flag bits |

## Level snapshots

**CONFIRMED** The original save writer iterates 30 slots. For a set mask bit, it stores a `u32 LE` sidecar length followed by `0x9C0` sidecar buffer bytes. For a clear bit it writes `0x9C4` bytes from that buffer, and the reader seeks past the whole slot. Each slot is always 2500 bytes. CD `MAIN.EXE+0x48BC7–0x48C49` and `+0x48A70–0x48AEC`; floppy `+0x52222–0x522A4` and `+0x520E1–0x5215D`. The ScummVM original-save path reads up to 29 levels using the same slot stride (Save:210–245,309–313).

**CONFIRMED** Four floppy sidecars have this little-endian layout. In a used original save slot, start the sidecar layout at slot offset `+0x04`. **CONFIRMED** Bytes left after the length-delimited sidecar in that slot are not part of its payload. The writer reads `_LEVELn.TMP` into the shared buffer at `DS:4EDC`, stores the returned length, then writes `0x9C0` bytes of that buffer whatever the length (CD `+0x48BDF–0x48C38`). The floppy writer does the same with `DS:8382` (`+0x5223E–0x52293`). The reader writes back only the stored length (CD `+0x48A83–0x48ACA`). The tail bytes are whatever that buffer held before the read, so they have no fixed meaning.

| Sidecar section | Layout | Witness and source |
| --- | --- | --- |
| Compressed map | `u16` length `C` followed by `C` Frame4 bytes. Decodes to 4096 wall XOR bytes then 1024 block flag bytes. | `_LEVEL1.TMP+0x00`, `C=101`; all four decode to 5120 bytes. Save:237–245, `engines/kyra/graphics/screen.cpp:2484–2540`. |
| Difficulty | `u16` at offset `2 + C`. | `_LEVEL1.TMP+0x67`, value 1. Save:252–253. |
| Monsters | 30 × 46-byte records at `4 + C`. | `_LEVEL1.TMP+0x69`, `_LEVEL2.TMP+0x4B`, `_LEVEL3.TMP+0x25`, `_LEVEL5.TMP+0x4F`. Save:255–290. |
| Flying objects | 8 × 17-byte records immediately after monsters. | `_LEVEL1.TMP+0x5CD`, `_LEVEL2.TMP+0x5AF`, `_LEVEL3.TMP+0x589`, `_LEVEL5.TMP+0x5B3`. Save:292–307, `engines/kyra/engine/kyra_rpg.cpp:37`. |

| Native sidecar | Compressed bytes | File bytes |
| --- | ---: | ---: |
| `_LEVEL1.TMP` | 101 | 1621 |
| `_LEVEL2.TMP` | 71 | 1591 |
| `_LEVEL3.TMP` | 33 | 1553 |
| `_LEVEL5.TMP` | 75 | 1595 |

**CONFIRMED** ScummVM saves serialize only mask-selected levels in bit order, across 29 bits. Each observed slot is 6517 bytes: 4096 wall deltas, 1024 flag bytes, 30 × 42-byte monsters, eight × 17-byte flying objects, then one difficulty byte. To recover a changed wall, XOR the delta with the corresponding first-four wall byte in the original CMZ block. `lol-cd.001` has mask `0x00000003` at `0x806D`, first level at `0x9971`, second at `0xB2E6`, EOF `0xCC5B`. All eleven checked saves end at the expected offset for their mask. Save:434–495, `engines/kyra/gui/saveload_rpg.cpp:33–90`.

### Monster slot

Field offsets are decimal. **CONFIRMED** The 46-byte native and 42-byte ScummVM strides match the sidecar and save boundaries above. ScummVM reconstructs the property pointer from the monster's type. The base layout and signedness are from Save:255–289,446–475. The native 16:16 pointer occupies the four bytes ScummVM omits, visible at `_LEVEL1.TMP+0x8A` in the first active monster.

| Native | ScummVM | Field |
| ---: | ---: | --- |
| 0, 2 | 0, 2 | `u16` next assigned, next draw |
| 4 | 4 | `u8` flying height |
| 5, 7, 9 | 5, 7, 9 | `u16` block, X, Y |
| 11 | 11 | `i8` shift step |
| 12, 14 | 12, 14 | `u16` destination X, destination Y |
| 16 | 16 | `u8` destination direction |
| 17, 18 | 17, 18 | `i8` hit offsets X and Y |
| 19, 20 | 19, 20 | `u8` subframe, mode |
| 21 | 21 | `i8` current fight tick |
| 22, 23, 24 | 22, 23, 24 | `u8` ID, direction, facing |
| 25, 27 | 25, 27 | `u16` flags, damage received |
| 29 | 29 | `i16` hit points |
| 31, 32 | 31, 32 | `u8` speed tick, property type index |
| 33 | — | Four-byte native property pointer |
| 37, 38, 39 | 33, 34, 35 | `u8` ranged attacks, `u8` current ranged weapon, `i8` ranged tick |
| 40 | 36 | `u16` assigned item handle |
| 42 | 38 | Four equipment shape bytes |

### Flying object slot

Offsets are decimal. **CONFIRMED** The same 17-byte boundaries fit both sets of examples. See Save:292–307,478–493. The purposes of `field_D` and `c` remain **UNCONFIRMED**. The DOS launch routine (CD `+0xF1DF–0xF321`) fills a free slot of the 8 × 17-byte array at `DS:4DCC`. It has three callers: `+0x10456` (a thrown item) and `+0x12601` pass 0x3F as the last argument, and `+0x15647` (the script function) passes script argument 7. It copies its last stack argument into byte 14 (`c`); the call at CD `+0x12601` passes `0x3F`. It never writes byte 13. No direct access to bytes 13 or 14 of that array was found in CD `+0xE000–0x10800`. Finding the routine that walks `DS:4DCC` with stride `0x11` and reads bytes 13 and 14 would settle both.

| Offset | Field |
| ---: | --- |
| 0, 1 | `u8` enabled flag, object type |
| 2, 4 | `u16` attacker ID, `i16` item handle |
| 6, 8 | `u16` X and Y |
| 10, 11, 12 | `u8` flying height, direction, distance |
| 13 | `i8` `field_D` |
| 14, 15, 16 | `u8` `c`, flags, wall flags |

## Editing a copy of an original slot

**CONFIRMED, edited-save run.** CD 1.02 accepted same-length
edits to party position (`+0x254/+0x256/+0x258/+0x263`),
level (`+0x269`), flag words and a referenced item row.
For a centered position in block `b`, use X =
`256 × (b mod 32) + 128` and Y = `256 × floor(b / 32) + 128`.
The level-8 copy loaded at block 113 and the writer saved back
a level-8 slot with mask `0x81` at `+0x47D` and a 1,554-byte
level-8 sidecar length at `+0x61E3`. No digest or header stamp was
recomputed for these edits. This is acceptance by the tested
CD build, whose fixed-length reads and snapshot loop are at
`MAIN.EXE+0x48A70–0x48BBF`.

Keep the version header, total size, fixed 2,500-byte stride and
level-mask/sidecar pairing. A clear destination bit let the
native loader initialize the three tested levels. For initialized
levels, the stored wall XOR, flags, monsters and flying objects
stay associated with their level. An incoming item handle must
name a valid 16-byte row. The lamp trial set the handle, carried
level and definition, cleared the row's free flag and kept its
links zero. The program consumed it and freed the row. Character
defaults hold equipment property IDs, while saved equipment holds
row handles. The far pointer at character `+0x13` is rebound on load.
[Wall recipe](unknowns/07_native_rules.md#level-8-wall-click-from-an-edited-copy)
and [oil and party recipes](unknowns/17_native_save_fields.md#level-1-oil-refill-on-an-edited-copy).

**UNCONFIRMED.** Whether all native versions accept the same
classes of edits. The floppy has different header and global
offsets. A separate native floppy round trip would establish
acceptance without applying the CD offsets to its shorter block.
