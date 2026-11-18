# Q12. Bit 0x8000 on an automap legend string

On both retail discs the bit is clear on every legend string. ScummVM masks it off and never tests it. It does not select a different string.

## What the loader does

CONFIRMED. `loadMapLegendData` (`engines/kyra/engine/lol.cpp:4250-4280` upstream) reads up to 32 records of 12 bytes. The uint16 at offset 10 of each record is the string id, stored for the draw as `l[2]`. `printMapText` passes that id straight to `getLangString` (`lol.cpp:4595` upstream). It does not test bit 0x8000.

`getLangString` (`lol.cpp:1066` upstream) returns nothing when the id is `0xFFFF`. Otherwise:

```
realId = id & 0x3FFF
if (id & 0x4000) use the LANDS string file
else use the level's own language file
```

The mask `0x3FFF` (`lol.cpp:1070` upstream) drops both `0x8000` and `0x4000`. Bit `0x4000` is tested on its own (`lol.cpp:1073`) and chooses `LANDS.ENG` (or the French or German file) rather than the level file. Bit `0x8000` is not tested. The string is then run through `decodeString1` and `decodeString2` (`lol.cpp:1090-1091` upstream, the tables in `engines/kyra/engine/util.cpp:30-48`).

A different `0x8000` lives on the message-type word in the text drawer (`engines/kyra/text/text_lol.cpp:221`). That bit skips a sound effect on a message. It is not the legend string id.

## What the files store

CONFIRMED, both editions, all 29 `LEVEL*.XXX` files, 73 records. The top two bits of the string id are `01` on 71 records and the id is `0xFFFF` on 2 records. Bit `0x8000` is clear on all 73. No record has top bits `10` (`0x8000` alone) or a real string id with top bits `11`. The two `0xFFFF` ids are the only values whose top bits look like `11`, and the draw skips them (`lol.cpp:4375` upstream, `if (l[2] == 0xFFFF) continue`).

The two editions' legend files match except level 22, where both files are 72 bytes and differ. The string-id column of all 73 records still follows the same rule on both editions.

The built-in legend rows, the eleven lines the map adds for doors and such, use the same shape of id. The CD table is 5 bytes per row (`devtools/create_kyradat/resources/lol_dos_cd.h:1451-1459`). The string ids are `0x4207` through `0x4210`, then `0x4251`. The floppy table omits the y byte (`lol_dos.h:1386-1393`) and keeps those same ids. Bit `0x8000` is clear on all eleven. Bit `0x4000` is set.

## Worked example

CD `LEVEL1.XXX` record 0, 12 bytes:

```
0d 00 0d 00 01 00 0d 00 0e 00 d0 41
```

| Bytes | Meaning |
| --- | --- |
| `0d 00`, `0d 00` | symbol on square x 13, y 13 |
| `01 00` | automap symbol 1 |
| `0d 00`, `0e 00` | draw the line once square x 13, y 14 is explored |
| `d0 41` | string id `0x41D0` |

`0x41D0` is `0x4000 | 0x01D0`. Bit `0x8000` is 0. Bit `0x4000` selects the `LANDS` file. The low 14 bits are `0x1D0`, decimal 464. `getTableEntry` reads the little-endian uint16 at byte `464 * 2` and decodes from there. In the CD `STARTUP.PAK` copy of `LANDS.ENG` (10059 bytes, 735 strings) that text is `FOUNTAIN`. The LANDSoL `GENERAL.PAK` copy is 9924 bytes and is not the same file; index 464 still decodes to `FOUNTAIN`. Record 1 is `0x41D1`, index 465, `THRONE ROOM`. The built-in id `0x4207` is index `0x207`, which decodes to `Niche`.

## What was not traced

The DOS automap string fetch. ScummVM ignores the bit, and neither retail file sets it, so on these discs there is no row where a DOS test of the bit could choose a different string. A DOS routine that tested `0x8000` would have nothing to do on this data. Whether that routine exists was not opened, and stays UNCONFIRMED. The bit's effect in ScummVM, and its value on both discs, are CONFIRMED: no effect, and clear.
