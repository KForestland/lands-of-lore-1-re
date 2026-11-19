# YVEL2.VCN and YVEL2.VMP

YVEL2 is a second tileset for level 22. Level scripts load it by syscall 9, `olol_loadLevelGraphics`. The wall file and the decoration shapes stay on YVEL1. "Level 22 sub-area" matches these scripts. A compass name for direction 3, and a prose name for flag 357, are UNCONFIRMED. The DOS block step adds a table word to the block index and masks with `0x3FF`. The words are −32, +1, +32 and −1 for directions 0 to 3 (CD `MAIN.EXE+0xD426–0xD436`, table at `+0x33D06`; floppy table at `+0x3CC5C`). Direction 3 therefore steps one block towards lower x. A compass word for it needs the DOS compass or automap drawing code.

## The files

CONFIRMED. Both editions contain `YVEL2.VCN` (32680 bytes) and `YVEL2.VMP` (3412 bytes). CD stores them in `YVEL.PAK`. floppy stores them in `CHAPTER6.PAK`. Each file is byte-identical across the editions. There is no `YVEL2.SHP` and no `YVEL2.DAT` in the CD tree.

`YVEL1.VCN` is 33532 bytes and `YVEL1.VMP` is 3369 bytes, also byte-identical across the editions, in the same PAKs.

These files are compression-4 bitmaps (`screen.cpp:3368-3392`). The uint16 at file offset 0 is the bitmap wrapper size, not the tile count. After decompression:

| File | Image size | uint16 at image 0 | Check |
| --- | --- | --- | --- |
| YVEL1.VCN | 49585 | 1487 | `2 + 1487 + 128 + 384 + 1487 * 32 = 49585` |
| YVEL2.VCN | 46021 | 1379 | `2 + 1379 + 128 + 384 + 1379 * 32 = 46021` |
| YVEL1.VMP | 4110 | 2054 | `2 + 2054 * 2 = 4110` |
| YVEL2.VMP | 4110 | 2054 | `2 + 2054 * 2 = 4110` |

CONFIRMED. That layout is what `loadLevelGraphics` reads (`engines/kyra/engine/scene_lol.cpp:339-402`): VCN count, shift bytes, 128-byte colour table, 384-byte palette, then `count * 32` tile bytes; VMP count, then that many uint16s. The YVEL1 and YVEL2 images differ. YVEL1.VCN begins `cf 05 70 70`. YVEL2.VCN begins `63 05 70 50`. YVEL1.VMP begins `06 08 01 00 01 00 01 00`. YVEL2.VMP begins `06 08 01 00 02 00 03 00`.

`LEVEL22.WLL` byte 0 is 8, which is `YVEL1.SHP` in `kLoLLevelShpListDOS` (`lol_dos.h:678`) and `kLoLLevelShpListDOSCD` (`lol_dos_cd.h:732`). CONFIRMED.

The only C++ mention of the string "YVEL2" is the 16-colour branch (`scene_lol.cpp:311-315`): if the special colour is 0x66 it becomes 0x44 when the loaded name is YVEL2, and 0xCC otherwise. `LOL_CD_FLAGS` and `LOL_FLOPPY_FLAGS` (`detection_tables.h:56` and `:58`) leave `use16ColorMode` clear, so that branch does not run for these two editions. CONFIRMED.

## How a script asks for it

CONFIRMED. Syscall 9 is `olol_loadLevelGraphics` (`engines/kyra/script/script_lol.cpp:2701` and `:208-210`). Arguments are last-push-first: string id of the file stem, special colour, weight, VCN length, VMP length, palette string id. A length of -1 makes `loadLevelGraphics` trust the file's own count (`scene_lol.cpp:345-346` and `:394-395`). A uint16 cast of the length turns the int16 value -15536 into 50000.

Syscall 8 is `olol_testGameFlag` (`script_lol.cpp:2701`, `:200-205`). Syscall 7 is `olol_setGameFlag` (`script_lol.cpp:2698`, `:189-196`): stack value 0 is the flag id, stack value 1 sets it when nonzero and resets it when zero. Syscall 1 is `olol_getWallType` (`script_lol.cpp:2690`, `:105-107`): block, then side. Syscall 33 is `olol_checkRectForMousePointer` (`script_lol.cpp:2738`, `:555-557`), which calls `posWithinRect(mouseX, mouseY, x1, y1, x2, y2)` (`engines/kyra/engine/kyra_rpg.cpp:246-249`). The four stack values are x1, y1, x2, y2 with x1 the last push. Syscall 28 is `olol_getDirection` (`script_lol.cpp:2731`, `:518-520`), returning `_currentDirection`.

`op_ifNotJmp` jumps when the popped value is 0, and masks the target with `0x7FFF` (`engines/kyra/script/script.cpp:323-327`). `op_eval` case 2 is equality and case 3 is inequality (`script.cpp:370-375`). EMC data words are big-endian. A syscall whose parameter fits in a signed byte is one word: opcode 14 with bit 0x4000 set. Syscall 9 is the word `4E 09`.

Strings cited below come from the script's TEXT chunk.

## LEVEL22.INI, both editions

The two INI files are byte-identical, 1364 bytes, CD `L22.PAK` and floppy `CHAPTER6.PAK`. DATA starts at file offset 186. TEXT starts at file offset 24. CONFIRMED.

| String | TEXT offset | File offset | Bytes |
| --- | --- | --- | --- |
| 0 `YVEL1` | 28 | 60 | `59 56 45 4c 31 00` |
| 1 `YVEL2` | 34 | 66 | `59 56 45 4c 32 00` |
| 6 `YVEL1.DAT` | 81 | 113 | `59 56 45 4c 31 2e 44 41 54 00` |
| 7 `YVEL1.SHP` | 91 | 123 | `59 56 45 4c 31 2e 53 48 50 00` |

CONFIRMED. Word 67 (file 320) pushes 357. Word 69 (file 324) is syscall 8. Word 72 pushes 1. Word 73 is eval `==`. Word 74 is ifNotJmp to word 97.

When flag 357 is set, the fall-through runs. Word 84 (file 354) is syscall 9 with string 0, `YVEL1`. Word 94 (file 374) is syscall 9 with string 1, `YVEL2`. Word 96 jumps to word 107. Both calls push palette -1, VMP length 4500, VCN length -15536, weight 12, special colour 102. Colour 102 is 0x66. The second call replaces `_vcnBlocks` and `_vmpPtr` (`scene_lol.cpp:348-402`), so the live tileset is YVEL2.

When flag 357 is clear, word 74 jumps to word 97. Word 105 (file 396) is syscall 9 with string 0, `YVEL1`, and the same lengths. That path does not push string 1.

Word 123 pushes 6, word 124 pushes 7, word 125 (file 436) is syscall 21, `olol_loadLevelShapes` (`script_lol.cpp:2720`, `:452-455`). Stack string 0 is string 7 `YVEL1.SHP` and stack string 1 is string 6 `YVEL1.DAT`. Decorations stay YVEL1 on both branches. CONFIRMED.

The script's VCN length 50000 is larger than YVEL2's own tile bytes `1379 * 32 = 44128`. CONFIRMED. Both lengths are byte counts in the DOS loader. It copies exactly the VCN length from the image after the palette, and exactly the VMP length from image offset 2. A length of −1 becomes `count * 32` for the VCN, and the load call's returned size minus 2 for the VMP (CD `MAIN.EXE+0x46573–0x46586, +0x46685–0x46692, +0x466B2–0x46725`; floppy `+0x4FD34–0x4FD47, +0x4FF18–0x4FF25, +0x4FF45–0x4FFB8`). So the VMP request is 4500 bytes against 4108 bytes of entries (2054 × 2), not 4500 entries. Both copies run past the end of the decoded image, by 5872 and 392 bytes, and take whatever follows it in the load buffer. Every YVEL2.VMP entry, masked with `0x3FFF`, is at most 1378, so no VMP entry selects a tile in the extra VCN bytes. Whether the renderer ever reads a VMP entry past 2054 is UNCONFIRMED; it needs the DOS rule that turns level 22's wall pages into VMP indexes.

## LEVEL22.INF, CD

CD `LEVEL22.INF` in `L22.PAK` is 20442 bytes. DATA starts at file offset 2574. TEXT starts at file offset 2078. String 4 `YVEL2` is TEXT offset 126, file offset 2212, bytes `59 56 45 4c 32 00`. String 5 `YVEL1` is TEXT offset 132, file offset 2218, bytes `59 56 45 4c 31 00`. CONFIRMED. ORDR function 122 enters at word 8428. ORDR function 152 enters at word 8512.

Three sites call syscall 9. Each uses palette -1, VMP 4500, VCN -15536, weight 12, special colour 102.

**Local BP-1.** Word 1344 pushes BP-1, word 1345 (file 5264) pushes 357, word 1347 (file 5268) is syscall 7, so flag 357 is set from that local. Word 1349 pushes BP-1 again. Word 1350 is ifNotJmp to word 1363. A nonzero local falls through: word 1360 (file 5294) is syscall 9 with string 4 `YVEL2`, and word 1362 jumps to word 1373, past the other load. A zero local jumps to word 1363: word 1371 (file 5316) is syscall 9 with string 5 `YVEL1`. CONFIRMED. CONFIRMED. The local is written earlier in the same subroutine, which starts at word 1123 (`subSP 3`). Word 1125 tests flag 357. With the flag set, the local becomes 0 (words 1154–1155) only when syscall 28 returns the caller's direction XOR 2. With the flag clear, it becomes 1 (words 1175–1176) only when syscall 28 returns the caller's direction. Any other facing calls the routine at word 1094, sets flag 585 and returns. Fifteen block functions enter this subroutine with a block and a direction; for example ORDR 913 at word 2404 passes block 913 and direction 2. floppy has the same subroutine at word 1083.

**Register 0 and direction.** Function 122, word 8428 (file 19430): push register 0, push 1, eval `==`, ifNotJmp to word 8466. Register 0 not equal to 1 jumps to word 8466. That run reaches word 8489 (file 19552), syscall 9 with string 5 `YVEL1`, then word 8491 pushes 0, word 8492 pushes 357, word 8494 (file 19562) is syscall 7, which resets flag 357. CONFIRMED.

Register 0 equal to 1 falls through to word 8433 (file 19440), syscall 28. Word 8435 pushes 3. Word 8436 is eval `!=`. Word 8437 is ifNotJmp to word 8460. Direction 3 takes word 8460, one syscall 48, and returns at word 8465. Direction other than 3 falls through a short run of other syscalls and jumps to the same return at word 8465. Neither arm of the direction test reaches a syscall 9. CONFIRMED. Which compass point direction 3 is, and what register 0 holds, are UNCONFIRMED. Direction 3 steps the block index by −1 (see the top of this page). Register 0 is set by the native code that runs ORDR function 122; reading that caller's register setup in `MAIN.EXE` would name it. `_currentDirection` is only the uint8 returned by syscall 28.

**Wall type 8 and the mouse.** Function 152, word 8512. Word 8526 is syscall 33. The four pushes are 130, 321, 112, 262, so the rectangle is x1 262, y1 112, x2 321, y2 130. The ifNotJmp at word 8529 goes to word 8550 when the pointer is outside that rectangle. The inside arm jumps to word 1016 and does not load a tileset. CONFIRMED.

Word 8550 (file 19674) pushes 0, word 8551 pushes 145, word 8553 is syscall 1, so block 145 side 0. Word 8556 pushes 8, word 8557 is eval `==`, word 8558 is ifNotJmp to word 8609 when the wall type is not 8. Word 8565 is syscall 33 with pushes 51, 151, 23, 121, so x1 121, y1 23, x2 151, y2 51. Word 8568 is ifNotJmp to word 8608 when the pointer is outside. The arm that passes both tests reaches word 8594 (file 19762), syscall 9 with string 4 `YVEL2`, then word 8596 pushes 1, word 8597 pushes 357, word 8599 (file 19772) is syscall 7, which sets flag 357. CONFIRMED.

Flag 357 is therefore the flag the INI tests to decide whether to restore YVEL2. The click path sets it. The register-0 path that loads YVEL1 resets it.

## LEVEL22.INF, floppy

floppy `LEVEL22.INF` in `CHAPTER6.PAK` is 19894 bytes. DATA starts at file offset 2562. TEXT starts at file offset 2078. String 4 `YVEL2` is TEXT offset 124, file offset 2210. String 5 `YVEL1` is TEXT offset 130, file offset 2216. CONFIRMED. The file is not byte-identical to the CD INF. The same four syscall-9 words are 1320, 1331, 8221, and 8326.

The BP-1 site matches. Word 1305 pushes 357, word 1307 is syscall 7, word 1309 pushes BP-1, word 1310 is ifNotJmp to word 1323. Word 1320 (file 5202) is syscall 9 with string 4. Word 1322 jumps to word 1333. Word 1331 (file 5224) is syscall 9 with string 5. CONFIRMED.

ORDR function 122 enters at word 8160 (file 18882): push register 0, push 1, eval `==`, ifNotJmp to word 8198. Word 8165 is syscall 28, word 8167 pushes 3, word 8168 is eval `!=`, word 8169 is ifNotJmp to word 8192. Word 8192 is the same small syscall-48 block as the CD word 8460, and word 8197 returns. Word 8198 is the other arm and reaches word 8221 (file 19004), syscall 9 with string 5, then word 8224 pushes 357 and word 8226 is syscall 7 with a preceding push of 0, resetting the flag. CONFIRMED.

ORDR function 152 enters at word 8244. Word 8282 pushes 0, word 8283 pushes 145, word 8285 is syscall 1, word 8288 pushes 8, word 8289 is eval `==`. Word 8297 is syscall 33 with the same pushes 51, 151, 23, 121. Word 8326 (file 19214) is syscall 9 with string 4. Word 8329 pushes 357 and word 8331 is syscall 7 with a preceding push of 1, setting the flag. CONFIRMED.
