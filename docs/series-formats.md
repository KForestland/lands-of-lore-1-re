# What the three games share

*Lands of Lore: The Throne of Chaos* (1993), *Lands of Lore: Guardians of Destiny* (1997) and *Lands of Lore III* (1999) were made by Westwood Studios. Each game is documented in its own repository:
- **LoL1:** [lands-of-lore-1-re](https://github.com/KForestland/lands-of-lore-1-re)
- **LoL2:** [lands-of-lore-2-re](https://github.com/KForestland/lands-of-lore-2-re)
- **LoL3:** [Lands-of-lore-3-re](https://github.com/KForestland/Lands-of-lore-3-re)

This page lines up the formats that recur across them. Every row only restates what the linked page establishes, with its evidence. "Open" means it is not documented yet.

## Archives

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Archive | PAK: a directory of (u32 offset, NUL-terminated name) rows, then the data ([pak](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/pak.md)) | MIX: u16 count, u32 data size, 12-byte rows of key, offset and size ([mix](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/mix.md)) | WSX: the same layout as LoL2's MIX ([wsx](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/wsx.md)) |
| Entry lookup | by the stored name | by a 32-bit key from the name; rows sorted by signed key | by a 32-bit key from the name; rows sorted by signed key |
| Name hash | none (names are stored) | Westwood's rotate-left-1-and-add over 4-byte words (`ww_hash_v1`) | a different hash: rotate right 6 and add `(byte − 0x30) & 0x3F`, over the uppercased name ([reader](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-wsx-reader.md)) |
| Cache archive | — | `CDCACHE.MIX`: the header covers less than the file; it holds decoded level textures ([mix](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/mix.md)) | `cdcache.wsx`: the header covers less than the file; it holds texture records and grows at run time ([textures](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/textures.md)) |

## Compression

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| LCW ("format 80") | classic form, called Frame4: CPS, CMZ, VCN, VMP, WSA and SHP frames ([lcw](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/lcw.md)) | a variant in the `LOCAL.MIX` room sections, plus LCW in the movie chunks ([compression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/compression.md), [vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) | open |
| LZO1X | — | level texture containers, in 1 MiB blocks ([compression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/compression.md)) | light-map groups in the LMF entries ([lmf](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/lmf.md)) |

## Sound, music and movies

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Sound | Creative VOC, 8-bit PCM ([voc](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/voc.md)) | Westwood AUD, IMA ADPCM, codec 99 ([sound](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/sound.md)) | RIFF WAVE, format 17 (IMA ADPCM), in the level sound archives ([level sheets](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/levels/README.md)) |
| Music | XMIDI, AdLib and other driver files ([music](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/music.md)) | AUD tracks in `DMUSIC.MIX`; HMI MIDI songs in `LOCAL.MIX` ([sound](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/sound.md)) | open |
| Movies and animation | WSA delta animations ([wsa](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/wsa.md)) | VQA version 2 ([vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) | open |

## Pictures and palettes

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Palette | 256 × 3 bytes of 6-bit VGA colour ([palette](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/palette.md)) | the same 6-bit form inside the movie frames ([vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) and texture containers | 16-bit colours baked from palette sources ([texture bake](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-texture-bake.md)) |
| Wall and texture art | VCN/VMP tile sets ([vcn_vmp](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/vcn_vmp.md)) | per-level texture containers ([texture container](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/texture-container.md)) | row-span texture records, flags 0x028E / 0x828E ([textures](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/textures.md)) |

## How the comparison was made

Each fact comes from that game's own files and program, as documented on the linked page. No format is assumed to carry over from one game to the next. Where two games look alike, both pages measured it, for example the MIX layout of LoL2 and the WSX layout of LoL3.
