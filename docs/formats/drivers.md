# ADV, DRV, TBL

**What (from names and places only):** `DRIVERS.PAK` holds `ALGDIG.ADV`, `MT32MPU.ADV`, `PCSPKR.ADV`, `SBDIG.ADV`, `SBPDIG.ADV`, `TANDYDIG.ADV` (3779-10378 bytes) and `ALFX.DRV` (6960); `GENERAL.PAK` holds `TRIG.TBL` (166 bytes). CONFIRMED (names, sizes; CD `pak_reader.py list`). The language folders and LANDSoL carry the same set.

These are almost certainly DOS sound driver code (`.ADV` is the extension used by the Miles Sound System's audio drivers, which many DOS games licensed) and a small lookup table (trigonometry?); none of this is CONFIRMED. ScummVM does not load them (it emulates the sound devices itself).

## Open

What each is, which program reads it, and the format as far as it is data: [Q5](../OPEN_QUESTIONS.md).
