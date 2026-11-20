# Translate the original text

Use Python 3.10 or newer. These commands read the installation you supply and
write to new folders you name. Run them from this repository. Give `--data`
the same original game folder each time.

```sh
python3 tools/lol.py translate export --data "/path/to/game" --out "/path/to/private tables"
python3 tools/lol.py translate build --data "/path/to/game" --work "/path/to/private tables" --out "/path/to/translated files"
python3 tools/lol.py translate verify --data "/path/to/game" --work "/path/to/private tables" --out "/path/to/translated files"
```

Open a CSV from the export and import all four columns as text. Set only the
`new` column. A blank cell keeps the current string. Type `\e` for an empty
string. Copy codes such as `\x0D` when they appear in the original and use
`\\` for a literal backslash. Keep UTF-8 CSV, the column names, the row order
and the manifest. A locked row has another use in the game. Keep its new cell
blank. Build rereads each changed archive. Verify compares every output byte to
the result computed from the original and your CSVs. To try the output, copy it
over a separate copy of your game.

**Keep your CSVs, the manifest and the rebuilt files private. The CSVs
contain original game text.**

**CONFIRMED.** The export includes separate language tables in PAKs or loose
files and TEXT chunks in EMC2 and AVFS scripts. CD `L01.PAK+0x6327` and floppy
`CHAPTER1.PAK+0x544AD` witness a language table. `LEVEL1.INI+0x20` in both
editions witnesses an EMC2 TEXT directory. See [the script format](emc2_scripts.md)
and [the lossless text writer](ROUND_TRIP.md). Limits in the CSV are encoded
bytes available for that row if no other edited row grows. Actual limits apply
to the whole table. The tool uses code page 437 and leaves script resource-like
single tokens locked. Alias rows must still share the same text.

**CONFIRMED in ScummVM.** The root `DATA/STARTUP.PAK` provides the in-game
`LANDS` tables when `FILEDATA.FDT` is loaded. The prologue loads the selected
language's `ENG/STARTUP.PAK`, `FRE/STARTUP.PAK` or `GER/STARTUP.PAK` for
`LOLINTRO.TIM` and its fonts. Both are exported with their own paths. In the CD witness, the root
text resources begin at `STARTUP.PAK+0x8AE8, +0xB233, +0xDFE1, +0x10D25`.
All three language archives carry the prologue TIM at `+0x14F2F`.
The prologue TIM name is absent from the root archive, so the two
`STARTUP.PAK` names do not duplicate any exported table.
Upstream `engines/kyra/engine/lol.cpp:531–538` and
`engines/kyra/sequence/sequences_lol.cpp:151–156,176–186`.
**UNCONFIRMED.** A conflicting resource's priority in the original DOS
opener. [PAK load order](unknowns/09_pak_order.md#cd)

## Check characters before building

```sh
python3 tools/lol.py translate fonts --data "/path/to/game"
```

The list comes from the installed bitmap fonts. Build checks each edited
row against the font or fonts identified for that table. The warning names
the CSV row and suggests a substitute when one is available. An input
character the writer cannot encode stops the build. For a table whose
font is still unconfirmed, use the font listing to check likely choices.

**CONFIRMED.** The LoL1 check measures the normal, automap and other installed FNT files, including loose CD replacements. A FNT header has the glyph offset table pointer at
`+0x06`, widths pointer at `+0x08` and height table pointer at `+0x0C`. See
the edition comparison and source lines on the [FNT page](formats/fnt.md).
Floppy normal fonts have 128 indexed entries. Build checks base language
tables against `FONT6P` and `FONT9P`, and CD `LOLINTRO.TIM` against the
selected language folder's two prologue fonts (upstream
`engines/kyra/sequence/sequences_lol.cpp:249–253`). For example, try an unaccented
replacement when a floppy font reports a missing accented letter.

## Verify a private translation patch

```sh
python3 tools/lol.py patch make "/path/to/translated files" --data "/path/to/game" --title "My translation" --out "/path/to/translation.json"
python3 tools/lol.py patch apply "/path/to/translation.json" --data "/path/to/game" --out "/path/to/test copy"
```

The patch checks the SHA-256 of each replaced span and makes a matching
undo file. Keep `undo.json` private because it holds original game bytes. If the size limit rejects the patch,
use smaller batches or keep replacements the same encoded size. A single
longer early row can shift enough offsets to hit the limit. You can still
keep the rebuilt files for your private copy.
See the [shared patch format](formats/patch.md).
