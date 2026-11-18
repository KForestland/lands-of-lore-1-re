# Text files: ENG, FRE, GER

**What:** string tables. `LANDS.<lang>` holds the global strings (ids with bit 0x4000); `LEVELnn.<lang>` (loaded by the level script) holds the level strings.

**Edition read:** CD (30 files per language). LANDSoL has the 30 ENG files only.

## Layout

| Offset | Type | Meaning |
|--------|------|---------|
| 0 | uint16 x n | offset of each string from file start; n = first offset / 2 |
| … | | NUL-terminated strings, Westwood-compressed |

Source: `LoLEngine::getTableEntry` `engines/kyra/engine/lol.cpp:1100-1104`; `getLangString` `:1066-1097` picks `_landsFile` for ids with 0x4000, else the level file, then decodes with `Util::decodeString1` + `decodeString2` (`engines/kyra/engine/util.cpp:29-68`, `:70-90`). `LANDS.<lang>` is loaded at `lol.cpp:602-605`; level files by script function `olol_loadLangFile` `engines/kyra/script/script_lol.cpp:1160-1165`.

Compression: bytes >= 0x80 expand to two characters from two fixed tables; 0x1B + byte is an escape for high characters (accents).

## Confirmed

String count = first offset / 2, summed over the 30 files: ENG 2165, FRE 2165, GER 2165. CONFIRMED (CD, `lol1lib` scan) — matches the closure memo's 2165 per language / 6495 total.


## Worked example

CD `LEVEL01.ENG` starts `48 01  76 01  ad 01 …`: string 0 at 0x148 = 328, so there are 328 / 2 = 164 strings. String 0 begins:

```
57 8e da f8 80 b2 …
```

| Byte | Meaning |
|------|---------|
| `57` | `W` (below 0x80: itself) |
| `8e` | bit 7 set, v = 0x0E: table 1 index (0x0E & 0x78) >> 3 = 1 → `e`, table 2 index 14 → `l` |
| `da` | v = 0x5A → `c` `o` |
| `f8` | v = 0x78 → `m` `e` |
| `80` | v = 0 → ` ` `t` |
| `b2` | v = 0x32 → `o` ` ` |

So far: "Welcome to ". The whole string decodes to "Welcome to Gladstone Keep.  King Richard awaits you in the throne room." (`tools/decode_dialogue.py LEVEL01.ENG --index 0`).

## Tool

`tools/decode_dialogue.py LEVEL01.GER [--index n]` decodes straight from the game data (`--check`: 6495 strings, every bigram byte inside the tables, 1967 strings with accented characters). `tools/extract_dialogue.py --out-dir d/` writes the raw strings (`--check` matches `data/dialogue_summary.json`). The decode tables were compared with `engines/kyra/engine/util.cpp:30-48`: identical.
