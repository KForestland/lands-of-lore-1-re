# How the Lands of Lore engine changed

The three games share some file formats and design ideas. Their programs store levels and run scripts in different ways. The comparisons below are **CONFIRMED** for the structures and readers named in the linked evidence.

| Area | The Throne of Chaos | Guardians of Destiny | Lands of Lore III |
|---|---|---|---|
| Archives and names | PAK directories store filenames | MIX directories store keys made from filenames | WSX directories use the MIX row layout with a different name hash |
| Compression | Frame4 (LCW) for images and animation data | LZO1X for level textures; one Westwood LZ77 decoder (LCW commands with a mode byte) for VQA chunks, interface shapes and WSA deltas | LZO1X for level textures and light maps, LCW in VQA |
| Level representation | A 32 × 32 grid with four wall types per square | Vertices and regions with portals between them | MAP surfaces with vertex and neighbor indices, plus waypoints and paths |
| Scripts | EMC2 programs and engine function calls | Level events and predicates select command groups | Separate MAP event pools select command groups with a new dispatch table |
| Saves | Fixed sections with party, items and level snapshots | A directory of global and per-level sections | Global and level directories with compressed sections and optional differences from base data |
| Sound and moving pictures | VOC samples, music driver files and WSA animations | AUD samples, AUD or HMI music, VQA version 2, WSA deltas | WAVE samples and music, VQA version 3 |

## Archives and name lookup

PAK stores the names directly alongside the positions. MIX and WSX keep a numeric key, a position and a size in each directory row. Both use signed key ordering. MIX uppercases and folds four-byte words with a rotate left and addition. WSX uppercases and folds individual bytes, after reducing each to `(b-0x30)&0x3F`, with a rotate right and addition. Their shared directory structure says nothing about whether a particular name will have the same key.

The shipped LoL3 `cdcache.wsx` and the four `.PHT` files sit outside that comparison. After the 114-byte header it shares with the game-written cache, the shipped cache is 51 copies of one 64,000-byte block. The four `.PHT` files are prefixes of one 0x1010000-byte block repeated end to end. No reader is known for either, and they are not counted as read.

[LoL1 PAK](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/pak.md) · [LoL2 MIX](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/mix.md) · [LoL3 WSX reader](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-wsx-reader.md#resource-name-key) · [LoL3 shipped cache](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/wsx.md#cdcachewsx) · [LoL3 PHT](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/pht.md)

## Compression

LoL1 uses Frame4 for files such as pictures and the compressed frame deltas in WSA. LoL2 keeps LCW commands in its movies. The same decoder, `0x158D58`, called Westwood LZ77 with a leading mode byte, also expands interface shapes such as `options.shp` and the WSA animation deltas in `LOCAL.MIX`. Its level texture banks use a different scheme, LZO1X in blocks. LoL3 retains the LZO1X texture wrapper, also uses LZO1X for its light-map groups and keeps LCW commands in its movies.

[LoL1 Frame4](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/lcw.md) · [LoL2 compression](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/compression.md) · [LoL3 textures](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/textures.md) · [LoL3 light maps](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-lmf-reader.md) · [LoL3 movie compression](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/vqa.md)

## Levels

In LoL1 the cell tells the game which wall type to use in each of four directions. In LoL2 the map supplies points and regions, with portals giving connections across region edges. LoL3 also stores points and connections, but its MAP reader builds a table of surfaces with explicit vertex and neighbor indices. Separate waypoint and path records describe positions a creature can move through.

[LoL1 grid](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/cmz.md) · [LoL2 geometry](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/geometry.md) · [LoL3 MAP reader](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-map-odf-readers.md)

## Scripts

LoL1's EMC2 bytecode calls functions in the executable. LoL2's object and region records point to command groups. A matching event can run a group when its predicate passes. LoL3 keeps distinct pools of object and region events and guarded command groups. Each game's executable defines the commands it can run.

[LoL1 EMC2](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/emc2.md) · [LoL2 events](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-script-events.md) · [LoL3 events](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-events.md) · [LoL3 opcodes](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-script-opcodes.md)

## Saves

LoL1's native save writer uses a fixed order for its blocks, including 30 level snapshot slots. LoL2 puts positions in a directory so that it can find its game-wide sections and numbered level blocks. LoL3 also uses positions and adds per-level sizes. Some of its sections are made relative to a base image by applying XOR before compression.

[LoL1 save format](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/savegame_format.md) · [LoL2 slot directory](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/lol2-save-format.md) · [LoL3 save stream](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/lol3-native-saves.md)

## Sound and moving pictures

LoL1 uses VOC samples and WSA frame deltas, with TIM scripts coordinating scenes. LoL2 has AUD samples, digital and HMI music paths, VQA version 2 video and WSA animation deltas in `LOCAL.MIX`. LoL3 keeps VQA for its outtakes and uses version 3 video. Its music and level samples reach Miles in WAVE containers, with MPEG audio for music and IMA ADPCM for level sounds.

[LoL1 samples](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/voc.md) · [LoL1 music](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/music.md) · [LoL1 scenes](https://github.com/KForestland/lands-of-lore-1-re/blob/main/docs/formats/tim.md) · [LoL2 audio](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/sound.md) · [LoL2 video](https://github.com/KForestland/lands-of-lore-2-re/blob/main/docs/formats/vqa.md) · [LoL3 audio](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/audio.md) · [LoL3 video](https://github.com/KForestland/Lands-of-lore-3-re/blob/main/docs/formats/vqa.md)
