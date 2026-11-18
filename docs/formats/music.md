# Music: XMI, C55, ADL, PCS

**What:** one music track set per area/scene, in four driver flavours: XMI (MIDI / MT-32), C55 (meaning OPEN), ADL (AdLib), PCS (PC speaker).

**Edition read:** CD `DATA/` (18 XMI, 17 C55, 16 ADL, 16 PCS), LANDSoL (20, 19, 18, 18).

## Containers

| Type | Header on the data | State |
|------|--------------------|-------|
| XMI | `FORM` … `XDIR` (IFF, XMIDI) | CONFIRMED (18/18 start `FORM`, bytes 8-11 `XDIR`) |
| C55 | `FORM` … `XDIR` | CONFIRMED (17/17) |
| PCS | `FORM` … `XDIR` | CONFIRMED (16/16) |
| ADL | no IFF; starts `00 00 01 00` on all 16 | CONFIRMED (bytes); meaning UNCONFIRMED |

ScummVM plays XMI through its XMIDI parser and ADL through `engines/kyra/sound/drivers/adlib.cpp` (Westwood AdLib driver; the driver version it uses for LoL is not checked here). The ADL layout (track table, program table) is described by that driver; not checked field by field in this repo. UNCONFIRMED.

"C55" is a file extension; what it stands for (the closure memo says "Creative Music File"; the files are XMIDI containers like XMI) is OPEN, [Q15](../OPEN_QUESTIONS.md). Which driver file plays it: [Q5](../OPEN_QUESTIONS.md) ([drivers.md](drivers.md)).

## Tool

`tools/extract_music.py` (inventory, `--out-dir` for raw files, `--check` rebuilds the file list and IFF trees of `data/music_inventory.json`: 67 files, no IFF parse errors). No decoder to MIDI in this repo.
