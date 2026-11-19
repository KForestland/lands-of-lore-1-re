# LoL1 floppy Comparison (2026-03-18)

Scope:
- the CD edition's `DATA/` folder, indexed in [`../data/pak_index.json`](../data/pak_index.json)
- floppy, an English floppy-edition installation (no speech, chapter-based PAKs)

## Main Result

- `floppy` is a real LoL1 install tree, not just patch junk.
- It uses the same underlying LoL1 `PAK` container grammar documented in `formats/pak.md`:
  - leading absolute offset
  - null-terminated filename
  - repeated directory entries until payload area
- It is **not** the same packaging as the existing `81`-PAK reference corpus.
- The new tree is chapter-based:
  - `CHAPTER1.PAK` .. `CHAPTER8.PAK`
  - `GENERAL.PAK`
  - `VOC.PAK`
  - `INTRO.PAK`
  - `INTROVOC.PAK`
  - `DRIVERS.PAK`
  - `FINALE1.PAK`
  - `FINALE2.PAK`

## Direct Structural Proof

- `GENERAL.PAK`
  - first offset: `1292`
  - first name: `TRIG.TBL`
- `CHAPTER1.PAK`
  - first offset: `3104`
  - first name: `LEVEL1.XXX`
- `VOC.PAK`
  - first offset: `3435`
  - first name: `1BOLTC.VOC`

These match the already-proven LoL1 `PAK` directory model.

## Edition / Build Difference

ScummVM identifies a LoL release by the MD5 of the first 1 MiB of `GENERAL.PAK` (Kyra sets `_md5Bytes = 1024 * 1024`, `engines/kyra/detection.cpp:58`). Measured that way:

| Copy | MD5 of first 1 MiB of `GENERAL.PAK` | ScummVM detection entry |
|------|-------------------------------------|-------------------------|
| CD `DATA/` | `05a4f588fb81dc9c0ef1f2ec20d89e24` | "Lands of Lore CD", English (`engines/kyra/detection_tables.h:1349`) |
| CD `DATA/ENG` (also FRE, GER) | `2dd5305434b11b40cbda565c0f729913` | the warning entry "You added the game incorrectly. Please add the root folder of the game." (`:1434`): the language folders are part of the CD layout, not a game on their own |
| floppy | `0f1fabc1f67b772a30d8e05ece720ac5` | English floppy, labelled "Extracted", no speech (`:1716`, `LOL_FLOPPY_FLAGS`) |

Full-file MD5s: CD `DATA/` `a7dbbf23c4438967f89dc221bc659e88`, floppy `74aa23c530155c2c9a7f894a616b4464`.

Practical read:
- floppy is a different edition (the floppy release), not a copy of the CD corpus

## Content Comparison

- fully parsed new `floppy` entries: `1213`
- unique filenames in new `floppy` tree: `1199`
- shared filenames with existing LoL1 corpus: `1040`
- filenames only in `floppy`: `159`
- filenames only in existing corpus: `123`

### New-only filename examples

- `AK'SHEL.CPS`
- `AKSHEL.TIM`
- `BACKGRND.CPS`
- `BLINK.WSA`
- `BRIDGE.WSA`
- `CHARGEN.WSA`
- `CLOSEUP.WSA`
- `CONGRAT.VOC`
- `DAWNFIN.WSA`
- `DEATH.WSA`
- `DOOR.SHP`
- `FINAL.LBM`

### Old-only filename examples

- `BUCKBUY.TIM`
- `COMPASSE.TIM`
- `COMPASSE.WSA`
- `COMPASSF.TIM`
- `COMPASSF.WSA`
- `COMPASSG.TIM`
- `COMPASSG.WSA`
- `LANDS.FRE`
- `LANDS.GER`
- `LEVEL01.FRE`
- `LEVEL01.GER`
- many `LEVELxx.TLC` dialogue files

Practical read:
- `floppy` appears more English-focused / chapter-packaged
- the existing corpus carries more language-specific material and per-level dialogue packaging

## Shared Content Stability

- among shared-name entries in the new tree:
  - same-size match against existing corpus: `877`
  - different-size match: `176`

Examples of shared filenames with different sizes:
- `LEVEL01.ENG`
- `LEVEL1.INF`
- `LORE01C.ADL`
- `GUARD.SHP`
- `ORC.SHP`
- multiple `BUCK*.TIM` and other portrait/timing assets

Practical read:
- this is not only a repack; some payloads differ in size as well
- likely causes:
  - build/version drift
  - language/content edits
  - chapter-oriented repack changing asset variants

## Matching PAK Names Across Editions

- `VOC.PAK`
  - new entry count: `215`
  - old entry count: `215`
- `DRIVERS.PAK`
  - new entry count: `7`
  - old entry count: `7`
- `GENERAL.PAK`
  - new entry count: `84`
  - old entry count: `73`

Practical read:
- `VOC.PAK` and `DRIVERS.PAK` are structurally very stable across the two editions
- `GENERAL.PAK` changed more materially

## Best Use

- treat `floppy` as the second edition to check against
- use it to:
  - confirm the `PAK` format across editions
  - compare stable versus drifting asset families
  - inspect whether chapter-based grouping simplifies any remaining LoL1 closure work
- do **not** treat it as the same indexed corpus as the CD `DATA/` folder
