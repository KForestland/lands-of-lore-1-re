# Q14. Who loads CAV_PLT2.PAL, CAV_PLT4.PAL and ALTPAL3.PAL

The three files are 768-byte palette members. No script loads them, and no near call in the floppy executable pushes their filename. Who opens them is still open.

## Where the bytes are

CONFIRMED.

| File | CD archive | LANDSoL archive | Size |
| --- | --- | --- | --- |
| `CAV_PLT2.PAL` | `CAVE1.PAK` | `GENERAL.PAK` | 768 |
| `CAV_PLT4.PAL` | `CAVE1.PAK` | `GENERAL.PAK` | 768 |
| `ALTPAL3.PAL` | `FOREST1.PAK` | `GENERAL.PAK` | 768 |

`CAVE1.PAK` also holds `CAV_PLT3.PAL`, and `FOREST1.PAK` also holds `ALTPAL1.PAL` and `ALTPAL2.PAL`, the same 768-byte size. The CD root `GENERAL.PAK` has `FXPAL.COL` and does not have these six. None of the three names is a loose file in either data folder. `FILEDATA.FDT` lists the names. That list is a manifest. `loadFileList` only opens entries that end in `.PAK` (`engines/kyra/resource/resource.cpp:254`).

The graphics loader takes a palette name as its last argument (`olol_loadLevelGraphics`, `engines/kyra/script/script_lol.cpp:208-210`, which calls `loadLevelGraphics` at `engines/kyra/engine/scene_lol.cpp:300`). When the name is set, the first 384 bytes of that file replace the VCN palette (`scene_lol.cpp:361-362`).

The calls that do name a palette, found as plaintext in the level scripts of both editions:

| Script | Palette it names |
| --- | --- |
| `LEVEL2.INI` | `ALTPAL2` |
| `LEVEL3.INI` | `ALTPAL1` |
| `LEVEL24.INI` | `ALTPAL1` |
| `LEVEL25.INI` | `CAV_PLT3` |

`CAV_PLT2`, `CAV_PLT4` and `ALTPAL3` do not occur as plaintext in any root-archive member of either edition. The palettes that are used are stored as plaintext, so a script that named these three would have shown the same bytes. None did.

## The executable lists

CONFIRMED as filename bytes, not as calls. LANDSoL `MAIN.EXE` (373872 bytes) has the six names in one list at file `0x3a525`: `TRIG.TBL`, then `CAV_PLT2.PAL`, `CAV_PLT3.PAL`, `CAV_PLT4.PAL`, `ALTPAL1.PAL`, `ALTPAL2.PAL`, `ALTPAL3.PAL`, then `SWAMPICE.COL`. LANDSoL `FINALE.EXE` (162728 bytes) has the same run at file `0x235f9`.

Using the data-segment base at file `0x37860`, the near offsets are `CAV_PLT2` `0x2cc5`, `CAV_PLT4` `0x2cdf`, `ALTPAL3` `0x2d04`. A search for `push` of those three immediates, and of `TRIG.TBL` at `0x2cbc`, found no hit in `MAIN.EXE`. A far pointer at the same strings was not ruled out.

CD `DATA/HARDRIVE/MAIN.EXE` (356928 bytes), CD `ENG/LANDS.EXE` and CD `ENG/FINALE.EXE` do not contain the three names at all.

## What was tried

- Reading every palette member out of the area archives and out of `GENERAL.PAK` on both discs.
- Searching every root-archive member for the plaintext names. The four known loads are there. These three are not.
- Searching the six executables, then searching the floppy `MAIN.EXE` for a near `push` of each filename's data-segment offset.

## What would settle it

A script instruction that pushes the name into `loadLevelGraphics`, or a DOS call that passes file `0x3a525` (or the finale copy) to the palette loader. The files exist. No reader has been found. Until one of those calls turns up, "nobody loads them" stays a measured negative, not a proof that the original program never opens the file.
