# Q9. Which PAK wins when the name is shared

A loose file wins over every archive. Among archives, the one loaded earlier wins. Inside one archive, the later directory entry replaces the earlier one. On these two discs the only names that actually collide are in the prologue, plus two identical pairs inside single archives: `CIMMERIA.DAT` twice in the floppy `CHAPTER8` and `GONG.VOC` twice in the CD `ENG/INTROVOC.PAK` (30155 bytes each, identical bytes).

## The three rules

CONFIRMED in ScummVM.

1. The resource search list is kept in descending priority (`common/archive.cpp:334-340`). A new entry is inserted before the first entry of lower priority, so an earlier load stays ahead of a later load of the same priority. The first hit is the file that is opened (`common/archive.cpp:562-568` and `:578-588`).
2. Priorities for Lands of Lore (`engines/kyra/resource/resource.cpp:78-82`): loose files and the data folder at priority 3, an installer at 2, protected archives at 1, ordinary archives at 0. A loose file beats every PAK.
3. Inside one PAK the directory is a map from name to entry (`engines/kyra/resource/resource_intern.cpp:75-77`). A second entry of the same name replaces the first. Loading an archive whose name is already loaded does nothing (`resource.cpp:223-224`).

The DOS program's own search order was not traced. The rules below are ScummVM's, applied to the bytes on the two discs.

## Floppy

CONFIRMED. `LOL_FLOPPY_FLAGS` has the talkie flag clear (`engines/kyra/detection_tables.h:58`, the flag is `detection.h:52`). On a non-demo floppy, `Resource::reset` puts `GENERAL.PAK` in the protected set (`resource.cpp:193-198`). Protected priority 1 beats every ordinary archive.

The in-game list is `VOC.PAK`, `GENERAL.PAK`, `CHAPTER1.PAK` through `CHAPTER8.PAK`, `DRIVERS.PAK` (`devtools/create_kyradat/resources/lol_dos.h:1-12`). `loadFileList` walks that array from the end (`resource.cpp:277`), so the first archive searched would be `DRIVERS.PAK` and the last would be `VOC.PAK`. `GENERAL.PAK` is already protected, so the second load is skipped and the protected copy stays in front.

During the prologue the floppy list is `INTRO.PAK` then `INTROVOC.PAK` (`engines/kyra/sequence/sequences_lol.cpp:165-167`), loaded at priority 0. `processPrologue` also calls `loadPakFile("GENERAL.PAK")` (`sequences_lol.cpp:38`), which finds the protected copy and returns.

Worked example. `ITEMICN.SHP` is 22733 bytes in `GENERAL.PAK` and 361 bytes in `INTRO.PAK`. The protected archive is searched first, so the game reads the 22733-byte file. `FACE08.SHP` is 11475 bytes in `GENERAL.PAK` and 11503 bytes in `INTRO.PAK`. Same rule, the general copy wins. `FACE01.SHP`, `FACE05.SHP` and `FACE09.SHP` are in both archives at the same sizes (10569, 8269, 9778). The search still returns the general copy; the sizes happen to match.

Across the eleven in-game archives the only repeated member name is `CIMMERIA.DAT`, twice inside `CHAPTER8.PAK`. Both copies are 8210 bytes and share MD5 prefix `28843e83`. The later directory entry replaces the earlier one, and the bytes do not change. No name is shared by two of those eleven archives.

## CD

CONFIRMED. `LOL_CD_FLAGS` sets the talkie flag (`detection_tables.h:56`), so `GENERAL.PAK` is not protected.

`FILEDATA.FDT` lists 1274 names. The first 81 are the PAK files, and `loadFileList` loads only names that end in `.PAK` (`resource.cpp:235-266`). The order is `CATWALK`, `CAVE1`, `CIMMERIA`, `DRIVERS`, `FOREST1`, `GENERAL`, `KEEP`, `L01` through `L29`, then the area, monster, music, speech and `YVEL` archives. Among those 81 archives there is no repeated member name, inside one archive or across two. A name that lives in the level data therefore has only one source once play has started.

The prologue is the collision. `processPrologue` loads the root `GENERAL.PAK` first (`sequences_lol.cpp:38`). `setupPrologueData` then loads `ENG/GENERAL.PAK`, `ENG/INTROVOC.PAK`, `ENG/STARTUP.PAK`, `ENG/INTRO1.PAK` through `ENG/INTRO9.PAK` and `ENG/HISTORY.PAK` (`sequences_lol.cpp:151-156` and `:176-186`; the language directory is prefixed for a talkie build that is not the demo). Those are different archive names from the root file, so both stay loaded. The root archive was inserted first and is searched first.

Worked example (the root and language-directory copies of several other files differ too, for example `AUTOBUT`, `FACE02`-`FACE06`, `HEALI.SHP`, `WRITE3E/4E.WSA` and `LORESFX.ADL`). `FACE08.SHP` is 11462 bytes in the root `GENERAL.PAK`, 11475 bytes in `ENG/GENERAL.PAK`, and 11491 bytes in `ENG/INTRO9.PAK`. The root file wins while the prologue archives are loaded. `FACE01.SHP` is 10563 in the root file and 10569 in both `ENG/GENERAL.PAK` and `ENG/INTRO9.PAK`. The prologue loads `ENG/STARTUP.PAK`, whose 11 members are the `LOREINTR` music files, four fonts, `LOLINTRO.TIM` and the two DIP files; it holds neither `ITEMICN.SHP` nor `LANDS.ENG`. Those two (22733 and 10059 bytes) are in the root `STARTUP.PAK`, one of the 81 `FILEDATA.FDT` archives, which is not loaded during the prologue. So during the CD prologue the only `ITEMICN.SHP` is the 361-byte copy in `ENG/INTRO9.PAK`.

`setupPrologueData(false)` unloads the language-directory list and does not unload the root `GENERAL.PAK` loaded at line 38. `go` then loads `FILEDATA.FDT` (`engines/kyra/engine/lol.cpp:537-538` upstream). `GENERAL.PAK` is already present, so it is not moved. Because the 81 archives share no member names, that leftover copy does not hide a different file of the same name.

If a saved game is started, `go` skips the prologue (`lol.cpp:531-535` upstream) and the file list is loaded on its own. `GENERAL.PAK` is then sixth. The 81 archives still share no names, so the bytes returned for a level file do not change.

Neither disc has `LEVEL1.CMZ`, `CAV_PLT2.PAL`, `CAV_PLT4.PAL` or `ALTPAL3.PAL` as a loose file next to the archives. A loose file of one of those names would win, at priority 3. There is not one.

## What was not traced

The original DOS search order. ScummVM's three rules, and the sizes they select on these two discs, are CONFIRMED. A matching trace of the DOS open call would say whether the original program uses the same order.
