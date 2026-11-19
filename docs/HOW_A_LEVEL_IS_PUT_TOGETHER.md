# How a LoL1 level is put together

A level combines a grid of wall IDs, a table that gives those IDs their properties, and a script that picks the graphics and supplies the objects. The CD's level 1 provides a concrete example. All PAK offsets below are member starts. [Level 1 sheet](levels/level01.md)

## Pieces

| Piece | Level 1 witness | What the program uses |
|---|---|---|
| Grid | `L01.PAK+0x61EF`, LEVEL1.CMZ | The expanded grid has 1,024 blocks. Four bytes at each block's start name its walls. CD copies them at `MAIN.EXE+0x48540` and `+0x48764`. [CMZ](formats/cmz.md) |
| Wall definitions | `L01.PAK+0x109C3`, LEVEL1.WLL | Each 12-byte row joins a wall ID to its graphic, collision and interaction properties. The native reader consumes the rows at CD `MAIN.EXE+0x47350–0x47421`. [WLL](formats/wll.md) |
| Tiles and decorations | KEEP.VCN and KEEP.VMP at `KEEP.PAK+0x9675` and `+0xF8F4`; KEEP.DAT and KEEP.SHP at `+0x4E` and `+0x7A0` | INI syscall 0x09 chooses the tile set. The VCN supplies tiles and the VMP assembles wall pages. Syscall 0x15 requests decoration shapes and placement definitions. [Tiles and wall pages](formats/vcn_vmp.md) · [Script call table](emc2_scripts.md) |
| Scripts and placements | `L01.PAK+0xF225`, LEVEL1.INI; `+0xC259`, LEVEL1.INF | The INI calls define creatures and create creature and item instances, for example DATA words `0x7C`, `0x0A` and `0x11`. The INF supplies the event functions. [EMC2](formats/emc2.md) · [Native record layouts](unknowns/18_native_records.md) |
| Text | English table at `L01.PAK+0x6327`, LEVEL01.ENG | LEVEL1.INI DATA word `0x29` calls 0x56 to load the level's language table. IDs with bit 0x4000 select global text in the reference reader at `engines/kyra/engine/lol.cpp:1066–1104`. [Text format](formats/text.md) |
| Sound | CD `01.TLK`, first member at `+0x19F0`; INI sound requests at DATA `0x97` and `0x9C` | The TLK archive holds speech samples. Syscall 0x63 requests a sound set. The reference opens the numbered archive at `engines/kyra/engine/lol.cpp:1892–1902`. [TLK](formats/tlk.md) · [Sound syscalls](emc2_scripts.md) |

## Load order

1. **CONFIRMED.** On the native CD path, the level entry at `MAIN.EXE+0x47086` releases the previous tile buffers through the call at `+0x470AD` before reading the WLL at `+0x47109`. The reference mounts the level speech archive immediately before the wall table at `engines/kyra/engine/scene_lol.cpp:64–66`. [Tile buffers and WLL load](formats/vcn_vmp.md)
2. **CONFIRMED.** The CD path builds the INI filename using the format at `MAIN.EXE+0x32983` and calls `+0x4744E` at `+0x4714D`. The initializer loads the script at `+0x47473`, asks its runner for entry 0 at `+0x4747B–0x47482` and calls the same runner with the optional nonzero entry argument at `+0x47483–0x4748D`. The per-level bit in DS:81F9 selects the optional argument at `+0x47129–0x4714D`. [EMC2 dispatcher](emc2_scripts.md)
3. The script's own branches determine resource order. One straight-line span of LEVEL1.INI requests level graphics, language, door shapes, block properties, monster graphics and decorations at DATA words `0x26`, `0x29`, `0x30`, `0x33`, `0x38` and `0x3C`, respectively. The CD graphics loader at `MAIN.EXE+0x464DB` handles the VCN and VMP data. [Script disassembly](formats/emc2.md)
4. **CONFIRMED.** After the INI and a conditional call at `MAIN.EXE+0x47175`, the CD loader formats the INF name with the string at `+0x3298F`. Its call at `+0x47196` enters `+0x47422`, which loads the event script and dispatches entry 0x400 at `+0x4743E–0x47444`. The reference orders saved block restoration between the INI and INF at `engines/kyra/engine/scene_lol.cpp:69–79`. [EMC2 dispatch](emc2_scripts.md) · [Saved level data](savegame_format.md)

**UNCONFIRMED.** The exact native speech mount and optional restore call on this CD path remain to be tied to their overlays. Resolve the targets of `MAIN.EXE+0x470FA` and `+0x47175` through the overlay stubs, then check for the `%02d.TLK` and temporary-level format strings in their callees. The floppy carries its level members in chapter archives. Its event script uses the same load-entry mechanism at `MAIN.EXE+0x50C21`. [Chapter and CD archive layouts](formats/pak.md)
