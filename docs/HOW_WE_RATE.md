# How we rate this repository

The README and [STATUS](STATUS.md) carry four counted lines instead of a
single percentage. `python3 tools/rating.py --data <DATA>` prints them from
your copy of the game and the pages; `--check` (part of `check_all.py`)
fails when the README or STATUS lines differ from the counts.

## The four lines

**Files read.** How many files in the CD edition's `DATA` folder (sub-folders
included) a reader in this repository accounts for to the last byte, by
count and by size. For a PAK archive, and for the CD speech files `NN.TLK`,
which are PAK archives, that means the name and offset directory ends at
the first member (after its zero terminator) and the members reach the end
of the file. A file that is not a PAK or a TLK counts when `tools/lol1_loose.py`
walks it to the last byte: a DOS font, a uint16 string table, the archive
inventory, a Windows icon, a Windows PIF, an MZ program whose declared image
is the whole file, an MZ stub plus a 32-bit LE (Linear Executable) Windows driver, an MZ program
whose overlay (Westwood's FBOV block) reaches the end, a file of whole text lines, or the
one COM program image. Files the walk refuses stay unread. The loose walk is
credited only on the CD layout (a `DATA` folder with `L01.PAK`, the same test
`lol1_loose.py` uses); on a floppy copy only PAK archives count.

A symbol block counts when the counts in its header give the size of every table, its name and index fields stay inside those counts, and the last table (four zero bytes per module) ends exactly where the string pool starts. A measured tail is not enough.

The blend tables are
65536 bytes that none of the eleven simple index formulas the tool tries
(min, max, average, product, sum, difference, OR, AND, XOR) reproduces.
A self-blend of the paired finale palette reproduces 65532 of 65536 bytes
of each table; the last four bytes are not explained, so the six files are
not yet counted as read.
No stored 768-byte palette (300 read, 109 different) keeps the colour on all
256 diagonal entries; the nearest keeps 240 of 256. Neither fact puts
the blend tables in the count. The [loose-file page](formats/loose.md) names the six
blend tables still in that set and the test that would finish each one. The rating
is counted on the CD edition; `--check` does not compare it on a floppy copy. It
does **not** mean that every entry inside is decoded or understood; the
[STATUS](STATUS.md) table says how far each format is read.

Only the folder given to `--data` is counted, every file in it and its
sub-folders. Files the game writes there while it runs (caches, saves)
are added to the total, and count as read only if a reader above walks
them, so a copy that has been played can give other numbers.

**Rules traced.** How many statements on the current pages carry the
evidence label CONFIRMED (backed by a program address or a file offset
that was checked) and how many carry UNCONFIRMED (a reading, with the test
that would settle it). Pages marked as history are left out. The glossary defines the label words; its labels are not counted. It counts
labels, not importance: one CONFIRMED may cover a whole table and one
UNCONFIRMED a single byte. It does **not** claim that unlabelled text is
wrong or that labelled text is complete.
Two samples of 30 CONFIRMED statements were re-derived from the bytes ([samples](CONFIRMED_SAMPLE.md)): the first, at most 27 held, 1 wrong (corrected), 2 not re-derived; the second, 20 held, 5 held in part, 3 corrected (1 wrong, 2 overstated), 2 not re-derived.

**Seen in the running game.** Of the probes on
[NEEDS_A_RUNNING_GAME.md](NEEDS_A_RUNNING_GAME.md) (tests that the files
and the program text cannot settle alone), how many were answered by
running the original game. It counts probe headings under "Answered
probes" and "Remaining probes", not numbered questions: a question can
have more than one probe, and a probe need not belong to a numbered
question. Each answer holds for the setup it names (one
display, one renderer, one save). Most documented facts were never
observed in a running game; they are proved from the program and the files
instead, and this line does **not** count them. Probes listed under
"Probes not yet run" are not counted in either number; Q7b and Q7c
also have a heading under "Remaining probes" and count there as not
answered.

The same line says how many answered probes rest on edited saves only.
An edited save is a copy of a game-written save with a few bytes
changed by hand; [edited saves](EDITED_SAVES.md) lists each such run.
An answered probe counts here when its section says "edited-save run"
and none of its bold labels says "answered" without "edited-save". A
label like that marks a run on a save the game wrote itself. A probe
that is still open is not counted, even when an edited-save run added
evidence to it.

**Open questions.** The state words of the At-a-glance table in
[OPEN_QUESTIONS.md](OPEN_QUESTIONS.md): answered, mostly answered, partly
answered. *Answered*: nothing is left to settle from the files or the program. *Mostly answered*: the main question is settled; named details remain. *Partly answered*: part is settled; the main point is open. A row that says 'answered for' a setup (one renderer, one device) counts as answered for that setup only.

## What the rating does not say

It is not a measure of completeness and cannot be turned into one: the
four lines count different things and none of them has a known total for
"everything the game does". Older notes in this repository that gave a
percentage are kept as history and are marked so.
