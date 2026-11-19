# PAK container

**What:** Westwood archive used for almost every LoL1 data file. The CD speech files `NN.TLK` use the same layout (see [tlk.md](tlk.md)).

**Edition read:** CD (`DATA/`, `DATA/ENG`) and floppy.

## Layout

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint32 LE | start offset of member 0 (= end of the directory) |
| 4 | char[], NUL | name of member 0 |
| … | uint32 LE | start offset of member 1, then its name, … |
| end | | the directory stops at an empty name, or when an offset is 0 or equals the file size |

A member runs from its offset to the next member's offset (the last one to end of file). No sizes or checksums are stored.

Source: `engines/kyra/resource/resource_intern.cpp:296-380` (`ResLoaderPak::load`), `:246-294` (`isLoadable`, which also accepts a big-endian variant not used by DOS LoL1). The big-endian branch does not apply: every container in both editions reads as little-endian and its members tile the file exactly (`pak_reader.py --check`, counts below). CONFIRMED.

## Confirmed

CONFIRMED, `tools/pak_reader.py --check`:

- CD `DATA/`: `CHECK pak: 111 containers, 6075 members, bad=none` (81 PAK + 30 TLK; the 81 PAKs hold 1163 members).
- CD `DATA/ENG`: `17 containers, 378 members, bad=none` (FRE and GER the same counts).
- floppy: `15 containers, 1213 members, bad=none`.

"bad" means the members do not tile the file exactly from the end of the directory to the end of the file.


## Worked example

First 40 bytes of CD `GENERAL.PAK` (`tools/pak_reader.py list GENERAL.PAK` shows the same entries):

```
66 04 00 00  4c 4f 52 45 53 46 58 2e 41 44 4c 00   3e 28 00 00  4c 4f 4c 53 59 53 45 58 2e 43 35 35 00   ea 31 00 00 …
```

| Bytes | Meaning |
|-------|---------|
| `66 04 00 00` | member 0 starts at 0x466 = 1126 (also: the directory is 1126 bytes long) |
| `4c 4f … 00` | name `LORESFX.ADL` |
| `3e 28 00 00` | member 1 starts at 0x283E = 10302, so member 0 is 10302 − 1126 = 9176 bytes |
| `4c 4f … 35 00` | name `LOLSYSEX.C55` |
| `ea 31 00 00` | member 2 starts at 0x31EA = 12778 (`LORESFX.C55`) |

## Tool

`tools/pak_reader.py list|extract <PAK> [member]`, `--check`. Library: `tools/lol1lib.py: pak_entries()`. `tools/pak_indexer.py` rebuilds `data/pak_index.json` (`--check` matches it: 81 PAKs, 1163 members).

## Open

- [Q9](../OPEN_QUESTIONS.md): which PAK wins when two PAKs hold the same member name **Answered** ([unknowns/09](../unknowns/09_pak_order.md)): a loose file beats every PAK; an earlier-loaded archive beats a later one.
