# Examples

Three small images made by the tools from the CD edition, to show what the output looks like. Make them yourself with your own copy of the game:

| Image | Command |
|-------|---------|
| `level01_keep.png` | `python3 tools/level_renderer.py --level 1 --out-dir out/` (a top-down map using the game's wall tiles) |
| `guard_frame_000.png` | `python3 tools/shp_renderer.py GUARD.SHP --out-dir out/` (shape 0 of the guard sprite set) |
| `knowltk1_frame_000.png` | `python3 tools/wsa_extract.py KNOWLTK1.WSA --out-dir out/` (frame 0 of an animation) |

These were made with the March 2026 tools, so colours may differ slightly from today's output. The repository holds no other game-derived images; see the asset policy in the [README](../README.md).
