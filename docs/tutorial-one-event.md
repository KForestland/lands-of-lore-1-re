# Follow one wall click in Lands of Lore

This example is the click on the east face of block 74 in level 4.
Block 74 is at grid position (10, 2). The block numbers count across
each 32-column row starting from zero. The [level 4 sheet](levels/level04.md)
lists its original script and walls.

## From the click to the script

1. **CONFIRMED.** Start on the east side, at block 75, and face
   west. Block 74's north, east, south and west wall bytes are
   `01 2A 02 02` at decompressed `LEVEL4.CMZ+0x12E`.
   Block 75's four wall bytes are zero at `+0x132`.
   The two CMZ members start at CD `L04.PAK+0x8F29` and
   floppy `CHAPTER1.PAK+0x1CC6`. The wall-42 WLL row has special
   type 4 in its byte +6: the row starts at CD `L04.PAK+0xD8AC`
   (floppy `CHAPTER1.PAK+0x14E0`), and byte +6 (CD `+0xD8B2`) is 04.
2. **CONFIRMED.** Clicking the wall selects the face of the next
   block, opposite the party's direction. Type 4 calls the script
   directly with event `0x40`. The native handler pushes that event
   at CD `MAIN.EXE+0x1785F` or floppy `+0x1BE8A` and passes
   block 74 as the entry number. See upstream ScummVM
   `engines/kyra/gui/gui_lol.cpp:1410–1431` and
   `engines/kyra/engine/scene_rpg.cpp:616–619` at revision `3b4db303`.
3. **CONFIRMED.** The script's entry table, ORDR, stores the target
   DATA word for block 74. In the CD archive entry 74 is at
   `L04.PAK+0xA68A` and targets word `0x02E8`. The event
   mask at CD `+0xB41C` is `0x0040`. The floppy entry at
   `CHAPTER1.PAK+0x5F585` targets DATA word `0x02C8`, whose mask at
   `+0x602C1` is also `0x0040`. The native CD interpreter tests the mask
   against the incoming event at `MAIN.EXE+0xCFF8–0xD010`.
   The shared bit admits this click. See upstream
   `engines/kyra/script/script_lol.cpp:64–92`.

## From script to screen

**CONFIRMED.** The script pushes numeric arguments and executes
EMC opcode 14 to call two native functions. After each call it
discards the corresponding arguments. Both editions return after
the second call (CD `L04.PAK+0xB42E`, floppy `CHAPTER1.PAK+0x602D3`).

| CD call | Floppy call | Command and result |
|---|---|---|
| `+0xB420` | `+0x602C5` | Function `0x57` plays sound 38. Native CD wrapper `MAIN.EXE+0x14E52–0x14E66`; upstream `engines/kyra/script/script_lol.cpp:1168–1172`. |
| `+0xB42A` | `+0x602CF` | Function `0x00` takes block 74, side −1 and wall 0. The native CD wrapper calls the wall setter at `MAIN.EXE+0x134AE`. The loop at `+0x16C09–0x16C22` writes 0 to all four sides, and `+0x16C64–0x16C65` requests a scene update. Upstream `engines/kyra/engine/scene_lol.cpp:1240–1254`. |

**CONFIRMED state change (from the CD code above; not observed in a running game).** All four sides of block 74 become wall 0: the clicked east face (42),
north (1), and south and west (2). The wall-0 WLL record at CD
`L04.PAK+0xD738` has VMP and shape zero. The handler requests sound 38. The expected visible change is that
wall 42 disappears from the east face when the view updates. See the
[wall graphics mapping](formats/vcn_vmp.md) and [function table](emc2_scripts.md#lol1-system-functions).

Read the entry locally from your own CD edition. The disassembler
prints the entry's mask and the two system calls. Use the
[EMC2 format page](formats/emc2.md) to read its output.

```sh
python3 tools/emc2_decompile.py --data "$LOL1_DATA" L04.PAK --entry LEVEL4.INF |
  grep -A9 'ORDR\[0x4A\]'
```
