# Examples

Three small images made by today's tools from the English CD edition, to show what the output looks like. `tools/example_images.py --check` (part of `check_all.py`) regenerates each one from the game files and fails if a tracked image differs from today's output, so a stale picture cannot stay. It also checks the two level schematics in `docs/images/` (levels 1 and 12). Make them yourself with your own copy of the game:

| Image | Command | What it shows |
|-------|---------|---------------|
| `guard_frame_000.png` | `python3 tools/shp_renderer.py GUARD.SHP --level 1 --out out/` | Shape 0 of the guard sprite set, in level 1's scene palette (the palette the 3D view draws it with). |
| `knowltk1_frame_000.png` | `python3 tools/wsa_extract.py KNOWLTK1.WSA --pal-from KNOWLTK.CPS --out out/` | Frame 0 of a talking-head animation, in the palette of the backdrop `KNOWLTK.CPS` that level 23's script loads with it. |
| `level01_schematic.png` | `python3 tools/level_renderer.py --level 1 --schematic --out out/` | Level 1 from above, drawn from the map and wall tables only (no game pixels): open floor light, solid wall dark, doors, switches and part walls orange, decorated walls marked red. |

The tools write `guard_000.png`, `knowltk1_000.png` and `level01_schematic.png`; the examples are those files renamed. The repository holds no other game-derived images; see the asset policy in the [README](../README.md).
