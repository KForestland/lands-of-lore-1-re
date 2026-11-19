# Music: XMI, C55, ADL, PCS

**What:** one music track set per area/scene, in four driver flavours: XMI (MIDI / MT-32), C55 (meaning OPEN), ADL (AdLib), PCS (PC speaker).

**Edition read:** CD `DATA/` (18 XMI, 17 C55, 16 ADL, 16 PCS), floppy (20, 19, 18, 18).

## Containers

| Type | Header on the data | State |
|------|--------------------|-------|
| XMI | `FORM` … `XDIR` (IFF, XMIDI) | CONFIRMED (18/18 start `FORM`, bytes 8-11 `XDIR`) |
| C55 | `FORM` … `XDIR` | CONFIRMED (17/17) |
| PCS | `FORM` … `XDIR` | CONFIRMED (16/16) |
| ADL | no IFF: 250 track ids, then 500 program and 500 instrument offsets, then program bytecode and 11-byte instruments ([`../unknowns/15_adl_and_c55.md`](../unknowns/15_adl_and_c55.md)) | CONFIRMED |

ScummVM plays XMI through its XMIDI parser and ADL through `engines/kyra/sound/drivers/adlib.cpp` (Westwood AdLib driver; the driver version it uses for LoL is not checked here). The ADL layout (track map, program and instrument offset tables, program headers, 11-byte instruments) is checked field by field on the data of both editions, including the floppy `LORESFX.ADL` short track map: CONFIRMED ([Q15](../unknowns/15_adl_and_c55.md)). Still open there: how the native floppy driver treats programs 217 and 218.

C55 is the XMIDI set for General MIDI / Roland GS: the executable's sound selector pairs the MT-32/MPU driver with XMI and again with C55, and `LOLSYSEX.C55` holds Roland's GS reset ([`../unknowns/15_adl_and_c55.md`](../unknowns/15_adl_and_c55.md)). What the letters stand for (the closure memo says "Creative Music File"; the files are XMIDI containers like XMI) is OPEN, [Q15](../OPEN_QUESTIONS.md). Which driver file plays it: [Q5](../OPEN_QUESTIONS.md) ([drivers.md](drivers.md)).


## XMIDI to MIDI

`tools/xmi_to_midi.py` follows ScummVM's XMIDI reader (`audio/midiparser_xmidi.cpp`, upstream `3b4db303`): delays are runs of bytes below 0x80, summed (`:104-110`); there is no running status; a note-on carries its duration as a variable-length number and there are no note-off events (`:166-186`); sysex and meta events have a variable-length size (`:296-311`); the timebase is 60 ticks per quarter at 500000 us per quarter, i.e. 120 ticks per second, with tempo events forced to that value (`:510-512`). The converter writes format-0 MIDI with that division and tempo and generates the note-offs from the durations.

CONFIRMED (`tools/xmi_to_midi.py --check`, CD): 18 XMI files, 220 sequences, 27,696 notes; 17 C55 files, 210 sequences; 16 PCS files, 190 sequences. Every sequence parses to its end-of-track event, the sequence count equals the INFO count in every file, and every written file re-reads as valid MIDI with every note closed. In 368 sequences one zero byte follows the end-of-track (padding inside the EVNT chunk). `LOLTITLE.XMI` and `LOLSYSEX.XMI` each hold one sequence of sysex setup data (94 and 135 sysex events) and no notes.

## Worked example

First 40 bytes of CD `LORESFX.XMI`:

```
46 4f 52 4d 00 00 00 0e 58 44 49 52  49 4e 46 4f 00 00 00 02 35 00  43 41 54 20 00 00 10 72 58 4d 49 44  46 4f 52 4d …
```

| Bytes | Meaning |
|-------|---------|
| `FORM`, `00 00 00 0e`, `XDIR` | IFF form of 14 bytes, type XDIR (an XMIDI directory) |
| `INFO`, `00 00 00 02`, `35 00` | 0x35 = 53 sequences in this file (the catalogue below has 53 `FORM XMID` children, `data/music_inventory.json`) |
| `CAT `, `00 00 10 72`, `XMID` | a catalogue of 4210 bytes holding the sequences |
| `FORM` … | the first sequence (`FORM XMID`, then its `EVNT` events) |

ADL files have no IFF header; CD `LORESFX.ADL` starts `00 00 01 00 ff ff ff ff …`; the layout is documented field by field in [Q15](../unknowns/15_adl_and_c55.md), and `tools/adl_to_midi.py` projects ADL tracks to a MIDI note timeline.

## Tool

`tools/extract_music.py` (inventory, `--out-dir` for raw files, `--check` rebuilds the file list and IFF trees of `data/music_inventory.json`: 67 files, no IFF parse errors). `tools/xmi_to_midi.py` converts XMI (and the XMIDI-container C55 and PCS files) to standard MIDI, one file per sequence.
