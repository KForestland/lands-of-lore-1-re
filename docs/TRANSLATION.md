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

**The CSVs contain original game text. Keep them, the export manifest and the
rebuilt archives private. Share only a patch made from your own changes.**

**CONFIRMED.** The export includes separate language tables in PAKs or loose
files and TEXT chunks in EMC2 and AVFS scripts. CD `L01.PAK+0x6327` and floppy
`CHAPTER1.PAK+0x544AD` witness a language table. `LEVEL1.INI+0x20` in both
editions witnesses an EMC2 TEXT directory. See [the script format](emc2_scripts.md)
and [the lossless text writer](ROUND_TRIP.md). Limits in the CSV are encoded
bytes available for that row if no other edited row grows. Actual limits apply
to the whole table. The tool uses code page 437 and leaves script resource-like
single tokens locked. Alias rows must still share the same text.

## Check characters before building

```sh
python3 tools/lol.py translate fonts --data "/path/to/game"
```

The list comes from the installed bitmap fonts. Build warns if a replacement
uses a character absent from any listed font. Shorten or reword the translation
with characters the fonts have, or leave the original row. A glyph warning
still allows a copy to build. An input character the writer cannot encode stops
the build. A drawn glyph can look different across fonts.

**CONFIRMED.** The LoL1 check measures the normal, automap and other installed FNT files, including loose CD replacements. A FNT header has the glyph offset table pointer at
`+0x06`, widths pointer at `+0x08` and height table pointer at `+0x0C`. See
the edition comparison and source lines on the [FNT page](formats/fnt.md).
Floppy normal fonts have 128 indexed entries. For example, try an unaccented
replacement when a floppy font reports a missing accented letter.

## Make a small translation patch

```sh
python3 tools/lol.py patch make "/path/to/translated files" --data "/path/to/game" --title "My translation" --out "/path/to/translation.json"
python3 tools/lol.py patch apply "/path/to/translation.json" --data "/path/to/game" --out "/path/to/test copy"
```

The patch checks old bytes and makes a matching undo file. It carries the old
and new bytes for the changes, so keep it small and share it only where you
have permission to share those bytes. If the size limit rejects the patch,
use smaller batches or keep replacements the same encoded size. A single
longer early row can shift enough offsets to hit the limit. You can still
keep the rebuilt files for your private copy.
See the [shared patch format](formats/patch.md).
