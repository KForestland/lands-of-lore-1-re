# Follow LoL1 level 1 from map to exit

Start with the CD edition's level 1. The map locates the blocks. The sheet ties those blocks to the wall table and scripts. The disassembly shows which branch actually requests a level change.

![Level 1 grid drawn from the CMZ and WLL data](images/level01_schematic.png)

## Draw the grid and write the sheet

```bash
export LOL1_DATA=/path/to/your/LoL1/DATA
mkdir -p ../lol1-tour
python3 tools/level_renderer.py --level 1 --schematic --out ../lol1-tour
python3 tools/level_report.py --level 1 --out ../lol1-tour
```

**CONFIRMED.** The renderer lays out the 32 × 32 grid from `L01.PAK+0x61EF`. Each expanded block has four wall bytes. The wall table at `L01.PAK+0x109C3` assigns graphics, interaction types and flags to those IDs. The light areas are open blocks. Orange fills blocks with mixed sides (partial walls, doors, switches or niches), and a red mark sits on each wall side with a decoration. [Level assembly](HOW_A_LEVEL_IS_PUT_TOGETHER.md) · [Level 1 sheet](levels/level01.md)

## Follow the exit at block 621

```bash
python3 tools/emc2_decompile.py "$LOL1_DATA/L01.PAK" --entry LEVEL1.INF \
  --out ../lol1-tour/level1.inf.txt
```

**CONFIRMED.** In `LEVEL1.INF` at `L01.PAK+0xC259`, ORDR entry `0x26D` for block 621 (13, 19) starts at DATA word `0x12D2`. Its event mask is `0x0041`, for stepping in or clicking a wall. At `0x12D9–0x12E9`, a nonzero hostility check takes the chat path and returns. After a zero result, the branch at `0x12EA–0x12EE` tests current facing against 2. The matching arm reaches `loadNewLevel(2, 106, 2)` at DATA word `0x130C`. The other facing takes the alternate arm at `0x130F`. [Script entry list](levels/level01.md#script-entry-points) · [Native syscall table](emc2_scripts.md)

## Read a creature definition

```bash
python3 tools/emc2_decompile.py "$LOL1_DATA/L01.PAK" --entry LEVEL1.INI \
  --out ../lol1-tour/level1.ini.txt
python3 tools/lol1_numbers.py --out ../lol1-tour/numbers.md
```

**CONFIRMED.** Look for `initMonster` at INI DATA word `0x0A`, in the helper at `0x0000` that INI entry 1 (`0x009F`) jumps to once per placement. The sheet traces four type-1 placement requests, including a repeat at block 271. The definition call for slot 1 is at INI DATA word `0x7C` (file `+0x18E` inside the member at `L01.PAK+0xF225`). It supplies base HP 200 and might 90 in the first attack category. The native constructor scales the HP by difficulty and a random factor. [Placement rows](levels/level01.md#monsters-placed-by-the-scripts) · [Creature numbers and HP formula](NUMBERS.md#creature-definitions-by-level)
