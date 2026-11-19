# How we rate this repository

The README and [STATUS](STATUS.md) carry four counted lines instead of a
single percentage. `python3 tools/rating.py --data <DAT>` prints them from
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
is the whole file, an MZ stub plus LE (Windows VxD) program, an MZ program
whose FBOV overlay body reaches the end, a file of whole text lines, or the
one COM program image. Files the walk refuses stay unread. The loose walk is
credited only on the CD layout (a `DATA` folder with `L01.PAK`, the same test
`lol1_loose.py` uses); on a floppy copy only PAK archives count. A measured tail is not enough: the symbol blocks end in a
string pool whose length is the uint32 at byte 4, and the blend tables are
65536 bytes that none of the eleven simple index formulas the tool tries
(min, max, average, product, sum, difference, OR, AND, XOR) reproduces;
palette-based formulas were not tried. Neither fact puts
those files in the count. The [loose-file page](formats/loose.md) names the twelve
CD files still in that set and the test that would finish each one. The rating
is counted on the CD edition; `--check` does not compare it on a floppy copy. It
does **not** mean that every entry inside is decoded or understood; the
[STATUS](STATUS.md) table says how far each format is read. Only the `DATA` folder is counted; files the game writes while it runs
(caches, saves) change the count on a copy that has been played.

**Rules traced.** How many statements on the current pages carry the
evidence label CONFIRMED (backed by a program address or a file offset
that was checked) and how many carry UNCONFIRMED (a reading, with the test
that would settle it). Pages marked as history are left out. It counts
labels, not importance: one CONFIRMED may cover a whole table and one
UNCONFIRMED a single byte. It does **not** claim that unlabelled text is
wrong or that labelled text is complete.

**Seen in the running game.** Of the probes on
[NEEDS_A_RUNNING_GAME.md](NEEDS_A_RUNNING_GAME.md) (questions that the files
and the program text cannot settle alone), how many were answered by
running the original game. Each answer holds for the setup it names (one
display, one renderer, one save). Most documented facts were never
observed in a running game; they are proved from the program and the files
instead, and this line does **not** count them.

**Open questions.** The state words of the At-a-glance table in
[OPEN_QUESTIONS.md](OPEN_QUESTIONS.md): answered, mostly answered, partly
answered. A question may be answered for one setup only; the table says so.

## What the rating does not say

It is not a measure of completeness and cannot be turned into one: the
four lines count different things and none of them has a known total for
"everything the game does". Older notes in this repository that gave a
percentage are kept as history and are marked so.
