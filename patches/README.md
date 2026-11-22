# Patches

Small checked edits for a reader's own copy of the original game. A patch records the replacement bytes and a hash of the span it replaces. A patch must not remove or bypass a disc check, a serial check or any other copy protection, and none here does. The format and its limits are on the [patch format page](../docs/formats/patch.md).

The format is `lol-patch-3`. Each change lists its file, entry, offset, old span length and SHA-256, and new bytes. Keep `undo.json` private. It holds original game bytes from your copy.

How to start the game on a current machine is [Running](RUNNING.md).

Apply and undo with the patch tool on a copy:

```sh
python3 tools/patch.py apply --data "/path/to/your/DATA" --out "../patched files" patches/item-name-spellings.json
# copy "../patched files/STARTUP.PAK" into a copy of your game; to undo:
python3 tools/patch.py apply --data "/path/to/your game copy/DATA" --out "../restored files" "../patched files/undo.json"
```

## Shipped patch

`item-name-spellings.json` is a data patch for CD `DATA/STARTUP.PAK`. The startup script `ONETIME.INF` stores each item's name as a string id in `LANDS.ENG`, `LANDS.FRE` or `LANDS.GER` (syscall `setItemProperty`, second argument). Those tables use the Westwood bigram codec: a byte below `0x80` is one character, and a byte at or above `0x80` is two characters.

| Item | String | Member | Entry | Offset | Old | New | Displayed before | Displayed after |
| --- | ---: | --- | ---: | ---: | --- | --- | --- | --- |
| 228 | 358 | `LANDS.ENG` | 3 | 6103 | `75` | `b3` | Duble ring | Double ring |
| 199 | 436 | `LANDS.ENG` | 3 | 7148 | `9b` | `8e` | Nathanial's Key | Nathaniel's Key |
| 228 | 358 | `LANDS.FRE` | 4 | 7155 | `75` | `b3` | Anneau Duble | Anneau Double |
| 228 | 358 | `LANDS.GER` | 5 | 7062 | `75` | `b3` | Duble-Ring | Double-Ring |

`0x75` is the single letter u. `0xb3` is the bigram ou, so the compressed string stays the same length and no later string moves. `0x9b` is the bigram al and `0x8e` is el. French string 436 already reads "Clef de Nathaniel" and German string 436 already reads "Nathaniels Schlüssel", so only the English key byte changes. The talkie engine loads `STARTUP.PAK` and then `LANDS.<lang>`, so the same data file is what ScummVM reads. `STARTUP.PAK` is not one of the ScummVM detection filenames.

An edited level-1 save placed items 228 and 199 in the pack. The first test was repeated under the [launch-record rules](../docs/NEEDS_A_RUNNING_GAME.md#launch-record-rule-and-the-runs-of-20-november) on 20 November 2026, using the original English CD game under DOSBox. The unpatched run used a fresh copy and showed the two old spellings. The patched run used a separate copy and showed both corrected spellings. The two `STARTUP.PAK` files differed only at these four bytes. Both runs left game memory unchanged. The French and German entries were checked by decoding the patched archive. ScummVM reads the same data file, and its run remains unverified. Applying `undo.json` restored the original archive byte for byte.

## Further text-table candidates

`tools/list_likely_spellings.py` decodes the text tables and prints an English word that is one small edit from a word in the system word list. French and German are checked for a broken offset table or a bigram outside the decode tables, not for spelling. The tool writes no patch.

```sh
python3 tools/list_likely_spellings.py --data DATA --check
```

On the unpatched CD text (the four item-name bytes still the old ones) it reported 30 English files, 30 French, 30 German, 6,495 strings, no bad offset table, no bigram outside the tables, and 32 candidate rows. The rows include the two English words the patch above already covers (`Duble`, `Nathanial's`). No new patch file was written.

This pass judges these remaining rows as the ones to look at, and leaves them unpatched:

| File | String | Word | Suggestion |
| --- | ---: | --- | --- |
| `LEVEL01.ENG` | 128 | everthing | everything |
| `LEVEL02.ENG` | 69 | embarrasing | embarrassing |
| `LEVEL10.ENG` | 29 | intersted | interested |
| `LEVEL10.ENG` | 36 | nevir | never |
| `LEVEL28.ENG` | 48 | dispell | dispel |
| `LANDS.ENG` | 426 | Elixer | elixir |
| `LANDS.ENG` | 561 | Dispell | dispel |
| `LANDS.ENG` | 580 | Shiney | shine |

`intersted` and `nevir` sit in lines already written as speech. `dispell` is the fantasy spelling. The other rows from that run are names, speech, or item words, including `Elvni`, `Tyrus`, `Hallo`, `mudder`, `Zooks`, `oughta`, `ROSEA`, `Jarod`, `Splitter`, `Biter`, `Dicer`, `Treant`, `bracers` and `laird`. A reader can disagree. None of them is patched.

## Named faults with no patch in this folder

- Dawn's Key softlock on floppy v1.05. Notes on later floppy builds report a fix in v1.22. The cause and the applicability of the report to the CD edition were not traced here.
- Lora remaining in the party after the Draracle, then a crash when Paulson would join. The party-size check is a possible cause. Its link to this failure remains open. No few-byte correction is isolated here.
- White Tower level 3. A thrown item aimed at the stairs (level 21, block `0x3E0`) is deleted. A send to the wrong level has been proposed. The responsible command has not been isolated.
- A click one pixel outside the view control can take an item and lock the view. The view-button test has been suggested. No instruction has been tied to the reported lock. No few-byte correction is isolated here.
- Large fireballs read a width of 63. Keeping 63 is what lets them travel a corridor. This is not a correction.
- White Tower monsters can carry sound id 255, which the program happens to play as silence. No player-facing correction.
- Portrait speech can freeze, French automap labels sit two pixels left, and a damage target above 3 is treated as a character id. Program or script behaviour. No scene-and-byte pair is isolated here.
- Heal III and IV underhealing, a King Richard dialogue hang, a Castle Cimmeria niche that eats items, Scotia's third form against the Whole Truth, and an endless cave-dweller spawn. Named reports. No root byte is known, so none is patched.
- A leading zero byte on the `NECROSAP.SHP` script name has been reported. Removing it can shift later script offsets, so it is not a one-byte replace.
- Official CD update 1.02, described in `LOLCDPCH.TXT` (24 May 1994), patches the installed program for fast-machine timing. That is an official program update, not one of these files. Floppy CPU patches are a DOS loader issue and are not included.
- ScummVM notes that an early unpatched floppy lets item 264 be equipped as a weapon (type 5) and forces the type to 0. The CD `STARTUP.PAK/ONETIME.INF+0x2214` call already supplies type 0. [Item definition table](../docs/NUMBERS.md#item-might-and-armour) No CD patch.
