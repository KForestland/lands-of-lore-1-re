# LoL1 LANDSoL Comparison (2026-03-18)

Scope:
- existing LoL1 reference corpus indexed in `/home/bob/lol1_pak_index.json`
- new install tree at `/media/bob/Arikv/new files or things/LANDSoL`

## Main Result

- `LANDSoL` is a real LoL1 install tree, not just patch junk.
- It uses the same underlying LoL1 `PAK` container grammar already proven in the main LoL1 lane:
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

- The new `GENERAL.PAK` hash does **not** match the known LoL1 CD hash in `/home/bob/lol1_scummvm_references.md`.
- New `GENERAL.PAK` md5:
  - `74aa23c530155c2c9a7f894a616b4464`
- Known reference `GENERAL.PAK` md5:
  - `05a4f588fb81dc9c0ef1f2ec20d89e24`

Practical read:
- this is a materially different build / edition witness, not a duplicate of the existing reference corpus

## Content Comparison

- fully parsed new `LANDSoL` entries: `1213`
- unique filenames in new `LANDSoL` tree: `1199`
- shared filenames with existing LoL1 corpus: `1040`
- filenames only in `LANDSoL`: `159`
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
- `LANDSoL` appears more English-focused / chapter-packaged
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
- `VOC.PAK` and `DRIVERS.PAK` are structurally very stable across the two witnesses
- `GENERAL.PAK` changed more materially

## Best Use

- treat `LANDSoL` as a second strong LoL1 witness
- use it to:
  - confirm the `PAK` format across editions
  - compare stable versus drifting asset families
  - inspect whether chapter-based grouping simplifies any remaining LoL1 closure work
- do **not** treat it as the same indexed corpus already covered by the main LoL1 lane
