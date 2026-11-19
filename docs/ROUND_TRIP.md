# Round-trip proof for LoL1

Two writers read the original files, build a replacement in memory and compare it with the original. Nothing is written to disk. "Byte-identical" means the rebuilt file equals the original file. "Decode-identical" means the rebuilt file reads back through the existing readers to the same pixels and palettes, while its compressed bytes differ.

The CD counts cover the `DATA` folder with its `ENG`, `FRE` and `GER` subfolders (CD1.02). The floppy counts are an English floppy installation.

| Writer | What is rebuilt | Comparison | CD | Floppy |
|---|---|---|---:|---:|
| `lol1_pak_writer.py` | PAK archives and PAK-layout TLK speech files, from their ordered members | Byte-identical | 132 PAKs and 30 TLKs, 7,209 members | 15 PAKs, 1,213 members |
| `lol1_compression_writer.py` | CPS, CMZ, VCN and VMP bitmaps, re-encoded with a new Frame4 encoder | Decode-identical: palette and expanded pixels | 320 files | 167 files |
| same | WSA animations: XOR deltas and Frame4 re-encoded, frame offsets regenerated | Decode-identical: every frame through the reader | 529 files, 12,785 deltas | 254 files, 5,420 deltas |
| same | SHP shapes: scanlines and Frame4 re-encoded, shape offsets and sizes regenerated | Decode-identical: flags, dimensions and pixels of every shape (colour tables copied) | 236 files, 7,299 shapes | 95 files, 3,601 shapes |

On both editions none of the 1,085 (CD) and 516 (floppy) re-encoded files is byte-identical to its original. All Frame4 streams in them (20,354 on the CD, 9,075 on the floppy) decode to the same bytes through both Frame4 readers.

## PAK and speech archives

**CONFIRMED.** A PAK directory is a list of u32 member offsets, each followed by the member's NUL-terminated name, starting at +0; members carry no length. In every original archive of both editions the last name is followed by one more u32 equal to the file size and then five zero bytes, after which member 0 starts. The writer emits that directory from the members' names and lengths, then the members in order, and every archive comes out byte for byte equal to the file. Example: the first offset in CD `GENERAL.PAK` is `0x466`. [PAK layout and the end of the directory](formats/pak.md#end-of-the-directory-in-the-original-files)

## Bitmaps, WSA and SHP

**CONFIRMED.** For a bitmap the writer keeps the header (compression type at +2, expanded size at +4, palette size at +8) and the palette at +0x0A, and re-encodes the pixels. For a WSA it re-encodes each stored XOR delta, including the closing one, and regenerates the frame offsets at +0x0E and the delta buffer size at +0x0A. For a SHP it regenerates the shape offsets, each 10-byte shape header's sizes and the scanlines with their transparent runs; shapes stored in a bitmap wrapper are then wrapped again. Each rebuilt file must read back through the existing readers with the same pictures. [Frame4 commands](formats/lcw.md) · [Bitmap header](formats/cps.md#layout) · [WSA layout](formats/wsa.md#layout) · [SHP shape layout](formats/shp.md#shape-layout)

This proves that the formats can be written, not that the original compressor is reproduced. The new encoder chooses a different mix of literal, fill and copy commands, and the WSA and SHP writers choose different XOR and transparent runs, so the rebuilt files are larger than the originals (see [tools/README](../tools/README.md#lol1_compression_writerpy)).

## Run the checks

```bash
python3 tools/lol1_pak_writer.py --data "$LOL1_DATA" --check
python3 tools/lol1_compression_writer.py --data "$LOL1_DATA" --check
python3 -m unittest tests.test_round_trip
```

Both checks run in `tools/check_all.py`; neither has an output option. The unit tests use synthetic archives and pictures and need no game files: member order, duplicate names and the end of the directory; refused names and a final empty member; Frame4 literals, fills, back-references and the end command; a WSA skip and closing delta; a SHP colour table and a long transparent run.
