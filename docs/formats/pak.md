# PAK container

**What:** Westwood archive used for almost every LoL1 data file. The CD speech files `NN.TLK` use the same layout (see [tlk.md](tlk.md)).

**Edition read:** CD (`DATA/`, `DATA/ENG`) and LANDSoL.

## Layout

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint32 LE | start offset of member 0 (= end of the directory) |
| 4 | char[], NUL | name of member 0 |
| … | uint32 LE | start offset of member 1, then its name, … |
| end | | the directory stops at an empty name, or when an offset is 0 or equals the file size |

A member runs from its offset to the next member's offset (the last one to end of file). No sizes or checksums are stored.

Source: `engines/kyra/resource/resource_intern.cpp:296-380` (`ResLoaderPak::load`), `:246-294` (`isLoadable`, which also accepts a big-endian variant not used by DOS LoL1). UNCONFIRMED for the big-endian branch (no such file in either edition).

## Confirmed

CONFIRMED, `tools/pak_reader.py --check`:

- CD `DATA/`: `CHECK pak: 111 containers, 6075 members, bad=none` (81 PAK + 30 TLK; the 81 PAKs hold 1163 members).
- CD `DATA/ENG`: `17 containers, 378 members, bad=none` (FRE and GER the same counts).
- LANDSoL: `15 containers, 1213 members, bad=none`.

"bad" means the members do not tile the file exactly from the end of the directory to the end of the file.

## Tool

`tools/pak_reader.py list|extract <PAK> [member]`, `--check`. Library: `tools/lol1lib.py: pak_entries()`. `tools/pak_indexer.py` rebuilds `data/pak_index.json` (`--check` matches it: 81 PAKs, 1163 members).

## Open

- [Q9](../OPEN_QUESTIONS.md): which PAK wins when two PAKs hold the same member name (search order of `Resource::loadPakFile`). Not needed to read files; matters for the edition comparison. UNCONFIRMED.
