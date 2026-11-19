# What the three games share

For a comparison of how the programs load levels, run scripts and save, see [how the engine changed](engine-evolution.md).

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
| Cache archive | — | `CDCACHE.MIX`, written by the game at run time: the header covers less than the file; one copy holds decoded level textures. It is not a shipped archive ([mix](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/mix.md)) | the game-written `cdcache.wsx` beside the install holds texture records. The shipped `DAT` copy is a different file: after the shared 114-byte header it is 51 copies of one 64,000-byte block, and it is not counted as read ([wsx](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/wsx.md#cdcachewsx)) |
| Repeated block, not counted as read | — | — | four `.PHT` files, each a prefix of one 0x1010000-byte cycle. What the bytes mean and what reads them is open, so the files are not counted as read ([pht](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/pht.md)) |

## Compression

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| LCW ("format 80") | classic form, called Frame4: CPS, CMZ, VCN, VMP, WSA and SHP frames ([lcw](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/lcw.md)) | LCW in the movie chunks (the `LOCAL.MIX` entry once read as LCW room sections is `options.shp`, Westwood LZ77) ([compression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/compression.md), [vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) | LCW in the CBFZ and VPRZ movie chunks ([vqa](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/vqa.md)) |
| LZO1X | — | level texture containers, in 1 MiB blocks ([compression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/compression.md)) | level texture banks in 1 MiB chunks, and light-map groups in the LMF entries ([textures](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/textures.md), [lmf](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/lmf.md)) |

## Sound, music and movies

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Sound | Creative VOC, 8-bit PCM ([voc](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/voc.md)) | Westwood AUD, IMA ADPCM, codec 99 ([sound](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/sound.md)) | RIFF WAVE, format 17 (IMA ADPCM), in the level sound archives ([level sheets](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/levels/README.md)) |
| Music | XMIDI, AdLib and other driver files ([music](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/music.md)) | AUD tracks in `DMUSIC.MIX`; HMI MIDI songs in `LOCAL.MIX`. The credits score is `MUSIC\CREDITS.HMI` ([sound](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/sound.md), [credits](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-music-selection.md#the-direct-credits-path)) | 38 RIFF WAVE tracks, format tag 0x55, MPEG Layer 3 frames, in `MUSIC1..4`, streamed through Miles. One directory key has no stored name ([audio](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/audio.md)) |
| Movies and animation | WSA delta animations ([wsa](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/wsa.md)) | VQA version 2 ([vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) | 19 version-3 VQA movies in `MOVIES1..4`, opened at `0x50DF70` ([vqa](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/vqa.md)) |

## Pictures and palettes

| | LoL1 | LoL2 | LoL3 |
|---|---|---|---|
| Palette | 256 × 3 bytes of 6-bit VGA colour ([palette](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/palette.md)) | the same 6-bit form inside the movie frames ([vqa](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md)) and texture containers | 16-bit colours baked from palette sources ([texture bake](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-texture-bake.md)) |
| Wall and texture art | VCN/VMP tile sets ([vcn_vmp](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/vcn_vmp.md)) | per-level texture containers ([texture container](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/texture-container.md)) | row-span texture records, flags 0x028E / 0x828E ([textures](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/textures.md)) |

## How the comparison was made

Each fact comes from that game's own files and program, as documented on the linked page. No format is assumed to carry over from one game to the next. Where two games look alike, both pages measured it, for example the MIX layout of LoL2 and the WSX layout of LoL3.
