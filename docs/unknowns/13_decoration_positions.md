# Q13 — How DAT decoration slots map to visible wall faces

**CONFIRMED** A DAT record supplies ten slots. The DOS scene renderer chooses a slot from a signed table indexed by `2 × view cell + pass`. It checks pass 1 before pass 0 and skips a pass with zero width or height scale. The absolute value selects the slot. The negative sign requests a mirrored draw, subject to the record's own flags. The wall face is `(party facing + signed wall delta) & 3`. The selected wall's WLL shape mapping supplies the decoration record. CD `MAIN.EXE+0x3E611–0x3E6A6, +0x3E830–0x3E88C, +0x3E989–0x3E995`; LANDSoL `+0x47757–0x477EC, +0x47976–0x479D2, +0x47ACF–0x47ADB`. Upstream ScummVM reproduces the loop in `engines/kyra/engine/scene_lol.cpp:1443–1458,1505–1527`.

| Table, 36 entries each | CD `MAIN.EXE` | LANDSoL `MAIN.EXE` |
| --- | --- | --- |
| Wall-face delta bytes | `0x32017` | `0x37E29` |
| Signed decoration slot bytes | `0x3203B` | `0x37E4D` |
| Width scale words | `0x32069` | `0x37E7B` |
| Height scale words | `0x320B1` | `0x37EC3` |

**CONFIRMED** The four tables produce the same mapping in both files. The view-cell numbering is shown in upstream `engines/kyra/engine/scene_rpg.cpp:128–148`. The party occupies cell 16 and faces toward the top here. To rotate the view, add the party facing to each listed wall face. ScummVM's byte and word tables are also in `devtools/create_kyradat/resources/lol_dos_cd.h:812–855`.

```text
00  01  02  03  04  05  06
    07  08  09  10  11
        12  13  14
        15  16  17
             ↑ party faces north
```

| DAT slot | Active cells and facing-north wall faces |
| --- | --- |
| 0 | Cell 16 south face, on the party's square. |
| 1 | South faces of cells 12–14, one step ahead. |
| 2 | South faces of cells 7–11, two steps ahead. |
| 3 | South faces of cells 1–5, three steps ahead. The west faces of far corner cells 0 and 6 also use this slot. |
| 4 | Cell 15 east and cell 17 west. Adjacent side walls. |
| 5 | Cell 12 east and cell 14 west. Side walls one step ahead. |
| 6 | Cell 8 east and cell 10 west. Inner side walls two steps ahead. |
| 7 | Cell 2 east and cell 4 west. Inner side walls three steps ahead. |
| 8 | Cell 1 east and cell 5 west. Outer side walls three steps ahead. |
| 9 | Cell 7 east and cell 11 west. Outer side walls two steps ahead. |

**CONFIRMED** The table supplies a negative signed slot for the second cell listed in each of rows 4–9. A wall delta byte `FF` is signed −1, so it means west when facing north. It can be active. For example, cell 0 pass 0 has wall delta `FF`, slot 3 and nonzero scale. Cell 0 pass 1 has slot 9 but zero scale (CD `0x32017, 0x3203B, 0x32069`, LANDSoL `0x37E29, 0x37E4D, 0x37E7B`).

**CONFIRMED** In the decoration record, `scaleFlag[slot] & 1` uses that slot's X/Y nudges and remaps the shape lookup through a ten-entry table. Its values are `0,1,1,1,4,5,5,5,5,4` at CD `MAIN.EXE+0x3205F` and LANDSoL `+0x37E71`. A record flags byte containing 8 skips the current record outside the centre-line view cells 3, 9 and 13. CD code `0x3E6AB–0x3E6D4, 0x3E70F–0x3E74C`, LANDSoL `0x477F1–0x4781A, 0x47855–0x47892`. Upstream `engines/kyra/engine/scene_lol.cpp:1466–1493`.

## Worked example

**CONFIRMED** Record 1 of `KEEP.DAT` begins at file offset `0x4A`, which is CD `KEEP.PAK+0x98` and LANDSoL `CHAPTER1.PAK+0x534EB`. In both editions the first four words are `FFFF 0011 0014 0015`, so slots 1, 2 and 3 select shape IDs 17, 20 and 21. The other slots are empty and all ten scale flags are zero. The record ends with next byte `00`, flags `08` (CD `KEEP.PAK+0xDE–0xDF`, LANDSoL `CHAPTER1.PAK+0x53531–0x53532`). The flags test makes it a centre-line decoration at one, two or three steps ahead. For instance, cell 13 pass 0 selects its slot 1 and draws shape 17 on the south face when facing north.
