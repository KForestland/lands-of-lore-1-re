# Q17 — Fields skipped when importing a DOS save

[Save file layout](../savegame_format.md) · [Executable locations](../executable_tables.md)

This page uses offsets from the start of the saved global-state block. Its file start is CD `0x0254` or floppy `0x0249`. In the tables below, both executable columns mean file offsets in that edition's `MAIN.EXE`. The comparison uses the English CD DOS 1.02 and English floppy writers and loaders. ScummVM's import path is `engines/kyra/gui/saveload_lol.cpp:55–67,107–186,237–245,255–289` at revision `3b4db3035ac68d06391bbb23a15a8ff6cb9801a3`.

## Global-state block

**CONFIRMED** The native writer copies consecutive bytes directly from the same data-segment range the corresponding reader fills. CD uses `DS:7FD0` and 563 bytes. Floppy uses `DS:B476` and 557 bytes. CD `+0x4898D–0x4899D, +0x48B92–0x48BA2`; floppy `+0x5204C–0x5205C, +0x521ED–0x521FD`. Subtract the saved range's base displacement from a native data address to locate the corresponding field in a save.

| Relative save offset | Measured layout and use | Native evidence |
| ---: | --- | --- |
| `0x00A` | **CONFIRMED** A `u16 LE` options word. Bits 4–5 select difficulty. Masks 1 and 2 are the effects and music toggles respectively. Mask 4 enables the floating cursor and mask 8 enables smooth scrolling. | CD `+0xCC86–0xCC93, +0x4B523–0x4B535, +0x4B566–0x4B58F, +0x4BF8A–0x4BFC9`. Floppy `+0x10498–0x104A5, +0x5205F–0x52094, +0x54DA9–0x54DE9, +0x54E73–0x54EF6`. The option order is at CD `+0x29BA1–0x29BD2`, floppy `+0x38E63–0x38EA8`. CD `STARTUP.PAK+0x8BBC–0x8BC7` has the label pointers. |
| `0x014` | **UNCONFIRMED** One intervening byte. The selected character at `0x013` and current level at `0x015` are both single-byte native reads. | CD `+0x162A4–0x162A9, +0x48B02–0x48B0C`; floppy `+0x1AB94–0x1AB99, +0x52173–0x5217D`. |
| `0x07C`–`0x143` | **CONFIRMED** 200 saved bytes from the flag-table base to the next table, enough for 100 consecutive flag words. For flag `k`, the native syscalls index word `k / 16` and mask `1 << (k % 16)`. ScummVM reads the first 40 words and advances over the following 120 bytes. Use of the high word indexes by original gameplay remains **UNCONFIRMED**. | CD `+0x13670–0x13701, +0x1416C–0x141B2`; floppy `+0x18033–0x180C4, +0x18B2E–0x18B74`; ScummVM `saveload_lol.cpp:134–164`. |
| `0x144`–`0x20B` | **CONFIRMED** 200 saved bytes from the indexed script-global table base through the byte before brightness. The native getters and setters use a two-byte stride. ScummVM reads indices 0–23, then skips the following 152 bytes. Gameplay uses of indices 24–99 remain **UNCONFIRMED**. | CD `+0x1416C–0x141B2, +0x1420E`; floppy `+0x18B2E–0x18B74, +0x18BD0`; ScummVM `saveload_lol.cpp:164–172`. |
| `0x20F` | **UNCONFIRMED** One intervening byte. Lamp effect at `0x20E` is a byte and credits at `0x210` are a word. | CD `+0xFC34, +0xFD06, +0x14213`; floppy `+0x145FD, +0x146CF, +0x18BD5`. |

## Six CD-only bytes after the level mask

**CONFIRMED** The CD global block extends through relative `0x232`. The floppy block ends at `0x22D` exclusive, immediately after the four-byte level mask. CD `+0x48B92–0x48BA2`; floppy `+0x521ED–0x521FD`.

| Block offset | CD save offset | Interpretation and evidence |
| ---: | ---: | --- |
| `0x22D` | `0x481` | **CONFIRMED** Language index. The menu displays localized ID `0x42D6 + index`. A change copies it to the live language selector and calls the language reload routine. CD `+0x4BED3–0x4BEDA, +0x4C187–0x4C1A6`. The English/French/German labels are CD `STARTUP.PAK+0x9094, +0x9096, +0x9098` (pointer words). |
| `0x22E` | `0x482` | **CONFIRMED** Dialogue text switch. The menu can toggle the byte, and the system forces text to 1 when speech is unavailable. CD `+0x4729F–0x472C7, +0x489F8–0x48A09, +0x4BEDC–0x4BEEB, +0x4BFDF–0x4C001`. CD `STARTUP.PAK+0x908C` points to the text toggle label. |
| `0x22F` | `0x483` | **CONFIRMED** Talking volume. UI selector 5 reads the byte, and the apply branch uses it for the talking-volume update. CD `+0x4B1F2–0x4B21F, +0x4B5BB–0x4B5F7`, and the selector/label row at `+0x29C30–0x29C3D`. Text ID `0x42DC` uses CD `STARTUP.PAK+0x90A0`. |
| `0x230` | `0x484` | **CONFIRMED** Sound-effect volume. UI selector 4 reads the byte and the load path sets effects availability from it. CD `+0x4B201–0x4B219, +0x489C6–0x489F2, +0x29C22–0x29C2F`. Text ID `0x42DA` uses CD `STARTUP.PAK+0x909C`. |
| `0x231` | `0x485` | **CONFIRMED** Music volume. UI selector 3 reads it and the load path enables or stops music according to the byte. CD `+0x4B200–0x4B214, +0x489A0–0x489C5, +0x29C14–0x29C21`. Text ID `0x42DB` uses CD `STARTUP.PAK+0x909E`. |
| `0x232` | `0x486` | **UNCONFIRMED** One final byte copied in the block. The next call serializes the independent item array. CD `+0x48B92–0x48BBF`. |

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

**UNCONFIRMED** The zero initialization and narrow accesses to the adjacent fields make alignment or unused space plausible. The targeted static check compared literal data addresses, direct memory operands, and accesses beginning at the preceding field. For example, the CD occurrence of word `81DF` at `MAIN.EXE+0x1EE77` straddles `add bx, di` and the next instruction, while `+0x4A8E1` is part of `mov bx, di` followed by `and bx, 0x7FFF`. Neither is a memory access. The individual meanings remain open because a pointer-relative access can avoid the literal address. The floppy witness is a level sidecar. The CD round trip below exercises the full save and load paths.


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
roles and the floppy runtime result remain open.
