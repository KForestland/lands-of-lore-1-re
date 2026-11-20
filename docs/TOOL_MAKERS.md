# Next steps for tool makers

## Map viewer

Start with the numbered level reports and the schematic in
`tools/level_renderer.py`. The CMZ body gives four wall bytes per cell and
the WLL entries map the types to visual and collision properties. CMZ
stores compressed walls starting at its header's offset word. A viewer
can first draw a 32×32 overhead grid. To draw decorated walls, join the
level's VCN tile pixels, VMP tile indices and DAT decoration rows using
`tools/vcn_vmp_reader.py` and `tools/tileset_mapper.py`. The format pages
give the stored offsets and the call sites for these joins.
[CMZ](formats/cmz.md) · [WLL](formats/wll.md) · [VCN and VMP](formats/vcn_vmp.md) · [DAT](formats/dat.md)

## Map editor

`tools/lol1_level_writer.py` already writes CMZ, WLL, DAT and localized
strings. `tools/lol1_pak_writer.py` writes the PAK directory and
`tools/lol1_script_writer.py` assembles EMC2 and AVFS listings. An editor
would need to keep changes to adjacent wall faces, decorations and
script block operands in sync, then verify reads of the affected archive.
Keep any opaque spans and edition-specific resources with their source.
The kit exposes script operands and strings. A wall editor and automatic
repair of cross-file references remain to be built.
[Writer checks](ROUND_TRIP.md) · [Script operands](formats/emc2.md) ·
[Level details](levels/README.md)
