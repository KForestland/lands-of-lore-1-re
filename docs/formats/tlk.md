# TLK speech containers (CD edition)

**What:** one speech archive per level: `00.TLK` … `29.TLK` in the CD `DATA/` folder. Each member is a Creative Voice (VOC) sample.

**Edition read:** CD. floppy (the floppy edition, see [README](README.md)) has no TLK files: it has no speech.

## Correction to the closure memo

The memo (section A, "TLK: uint16 count + 8-byte entries (uint32 ID + uint32 offset)") describes ScummVM's `ResLoaderTlk` (`resource/resource_intern.cpp:453-492`), which serves `%08u.AUD` members (`:118-143`). **LoL1 CD TLK files are not in that layout.** They are PAK archives:

- `LoLEngine::loadTalkFile` opens `"%02d.TLK"` with `_res->loadPakFile` — `engines/kyra/engine/lol.cpp:1892-1902`. CONFIRMED in code.
- On the data: `01.TLK` starts `f0 19 00 00 "00000.VOC\0"` — a PAK directory (first member at 0x19F0 = 6640). CONFIRMED.
- All 30 parse as PAK: 4912 members, every one starts with `Creative Voice File`. CONFIRMED (`tools/voc_reader.py --check`: `215 in PAKs + 4912 in TLKs ... bad=none`).

The memo's "Parsed + validated" for TLK came from `tools/tlk_verify.py`, whose own report already reads the files as name+offset directories ("directory size 6640 … first payload Creative Voice File"). The March version of that tool paired each name with the *next* offset in its sample list (it printed `00000.VOC@50755`; the true start is 6640). Today's tool reads the directory correctly.

## Member names

Built by `LoLEngine::snd_playCharacterSpeech`, `engines/kyra/sound/sound_lol.cpp:59-81`:

| Pattern | Used when |
|---------|-----------|
| `%03d` + speaker letter + part digit + `.` + `%02d` (TLK number) | id < 1000; speaker = first letter of the character's name, parts `0`, `1`, … are played in sequence |
| `%03d` + `_` + part + `.%02d` | same, no speaker-specific take |
| `%03X` … `.00` | id has bit 0x4000 (global lines, TLK number forced to 00) |
| `@%04d` + speaker + `.%02d` | id >= 1000 |

Example on the data: `01.TLK` holds `00000.VOC`, `000_0.01`, `000_1.01`, `001A0.01`, … CONFIRMED (`pak_reader.py list 01.TLK`). The `NNNNN.VOC` members (59 in total) are one 44115-byte clip named `00000.VOC`, stored as the first and last entry of each TLK (once in `25.TLK`). CONFIRMED. These patterns never produce that name. Who plays it is UNCONFIRMED, [Q10](../OPEN_QUESTIONS.md): every catalog index in `ENG/FINALE.EXE` is computed and none is the constant 40, and startup sorts catalog rows 4 to 92 by name, so the file row number 40 need not be the row used in memory. Who requests the name stays open.

## Confirmed

`tools/tlk_verify.py --check` (CD): `30 files, 4912 members, all VOC: 4912/4912, speech-pattern names 4853, NNNNN.VOC names 59, bad=none`. Every speech-pattern name carries its own TLK number or 00.


## Worked example

First 32 bytes of CD `01.TLK`:

```
f0 19 00 00  30 30 30 30 30 2e 56 4f 43 00  43 c6 00 00  30 30 30 5f 30 2e 30 31 00  ea 69 01 00 …
```

| Bytes | Meaning |
|-------|---------|
| `f0 19 00 00` | first member at 0x19F0 = 6640: a PAK directory, not a count |
| `30 30 30 30 30 2e 56 4f 43 00` | `00000.VOC` |
| `43 c6 00 00` | next member at 0xC643 = 50755 |
| `30 30 30 5f 30 2e 30 31 00` | `000_0.01`: line 000, no speaker letter (`_`), part 0, TLK 01 |

## Tool

`tools/pak_reader.py list 01.TLK`; `tools/voc_reader.py 01.TLK:000_0.01 --wav out.wav`; `tools/tlk_verify.py`.
