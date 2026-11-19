# Runs on edited saves

Some probes on [NEEDS_A_RUNNING_GAME](NEEDS_A_RUNNING_GAME.md) need a
place in the game that no game-written save reached. For those, a copy of
a save the game wrote was changed by hand and loaded in the original
English CD 1.02 game. The original slots were not changed. Each run used
one edited copy in its own scratch install
([launch](NEEDS_A_RUNNING_GAME.md#working-launch-for-the-english-dos-cd)).

An edited save shows what the original program does with that state. It
does not show that ordinary play reaches the same state. A native save
(one the game wrote during normal play) is still needed for that. The
rules an edit must keep (same section lengths, same file size, no
checksum to update) are in
[editing a copy of an original slot](savegame_format.md#editing-a-copy-of-an-original-slot).

All eight runs below belong to probes that are still open. None of them
answers a probe on its own; the [rating](../README.md#rating) counts how
many answered probes rest on edited saves only.

## Q17. Oil refill on level 1

- **Question:** are the three isolated save bytes touched during play?
  ([probe](NEEDS_A_RUNNING_GAME.md#q17-are-the-isolated-save-bytes-touched-during-play))
- **Edited:** flag 251, 26 oil and one carried oil item in item row 11
  ([byte table](unknowns/17_native_save_fields.md#level-1-oil-refill-on-an-edited-copy)).
- **Showed:** the game took the oil onto the lamp. The lamp handler
  added 100 oil at `MAIN.EXE+0x1065B`. The three isolated bytes were
  touched only by the bulk write when saving.
- **A native save would add:** the brightness writer and the
  oil-depletion event in ordinary play, from a dark level with flags
  250 and 251 set (the [dark-lamp run](#q17-dark-lamp-on-level-8)
  saw the decrement only on an edited copy).

## Q17. Dark lamp on level 8

- **Question:** the same probe, with the lamp lit and burning down.
- **Edited:** level 8, block 113, flags 250 and 251, 2 oil and lamp
  effect 0xFF
  ([byte table](unknowns/17_native_save_fields.md#dark-lamp-depletion-on-an-edited-level-8-copy)).
- **Showed:** after the load the lamp held brightness 4, oil 1,
  effect 7. The oil fell 1 → 0 at `MAIN.EXE+0xF9FF`, the gated
  `dec byte [0x81DD]`. The slot the game then wrote holds brightness
  4, oil 0, effect 8 and flag 250 clear. The three isolated bytes were
  touched only by the bulk write when saving, and are zero in that
  slot.
- **A native save would add:** a watch from the load through the
  first decrement, so that writes during load and a level event's
  writes can be told apart, and which code clears flag 250.

## Q17. Level 8 to level 7

- **Question:** the same probe, through a level change.
- **Edited:** level 8, block 208, facing west
  ([byte table](unknowns/17_native_save_fields.md#level-8-to-level-7-with-the-isolated-bytes-watched)).
- **Showed:** one step west ran block 207's event, which loaded level
  7 at block 206 facing west (`L07.PAK` opened). The three isolated
  bytes stayed zero with no watch hit.
- **A native save would add:** a level change and party changes from
  ordinary play; other levels could still touch a byte.

## Q17. Two portraits on level 1

- **Question:** the same probe, for the selected-character byte.
- **Edited:** a second character row filled from the program's own
  defaults record
  ([byte table](unknowns/17_native_save_fields.md#selecting-between-two-portraits-in-an-edited-copy)).
- **Showed:** two portraits. Clicks changed the selected byte 0 → 1 → 0
  → 1, with no access to the isolated bytes. The menu save wrote no new
  slot, so the live watch is the only witness. A separate copy that set
  only flag 39 reached the poisoned-king scene, but no second portrait.
- **A native save would add:** a slot after a follower joins, to test
  the selection and keep it through a normal save.

## Q7a. Wall click on level 8

- **Question:** can wall bit 0x40 change anything besides the script's
  byte test?
  ([probe](NEEDS_A_RUNNING_GAME.md#q7a-can-wall-bit-0x40-change-anything-besides-the-emc-byte-test))
- **Edited:** level 8, block 113, facing north, holding a key in item
  row 11
  ([byte table](unknowns/07_native_rules.md#level-8-wall-click-from-an-edited-copy)).
- **Showed:** the key click ran the level-8 wall query. It read wall
  ID 2 as `0x07` at `MAIN.EXE+0x13522`, and the game wrote a new slot.
- **A native save would add:** the bit-0x40 contrast, which needs a
  level-8 save written by the game (or level 7 before the pit).

## Q7b. Pose squares on level 23

- **Question:** which animation shows when a script selects mode 11?
  ([probe](NEEDS_A_RUNNING_GAME.md#q7b-which-animation-actually-displays-when-a-script-selects-mode-11))
- **Edited:** level 23, with the party placed at block 812 in one copy
  and block 105 in another
  ([byte table](unknowns/07_native_rules.md#level-23-pose-squares-from-edited-placements)).
- **Showed:** the second copy loaded on the pose square, block 105. No
  monster stood on a pose square in either sample, so no mode-11 frame
  was seen.
- **A native save would add:** an active monster approaching a pose
  square, so the monster-leaves event fires and its frame can be traced.

## Q18. Fight on level 27

- **Question:** which monster definition fields does a fight use?
  ([probe](NEEDS_A_RUNNING_GAME.md#q18-which-monster-definition-fields-does-an-actual-fight-use))
- **Edited:** level 27, facing west, with the party next to slot-1
  monsters in one copy and next to the slot-2 Hatchet placement in
  another
  ([byte table](unknowns/18_native_records.md#level-27-fight-from-an-edited-placement)).
- **Showed:** the slot-1 fight read the critical byte at
  `MAIN.EXE+0xAD87` and speed at `+0x12744`. The watches saw no
  fight-time access to the three modifier words. The Hatchet copy
  reached defeat before any watch hit.
- **A native save would add:** a longer-lived party with watches armed
  before the load, to catch the first slot-2 attack (the
  [Hatchet run](#q18-hatchet-fight-on-level-27) did this on an edited
  copy).

## Q18. Hatchet fight on level 27

- **Question:** the same probe, for the slot-2 Hatchet definition.
- **Edited:** the block-497 Hatchet placement with current and
  maximum HP raised from 20 to 500
  ([byte table](unknowns/18_native_records.md#read-watches-on-the-hatchet-definition)).
- **Showed:** under read watches on the slot-2 definition, the fight,
  a reload and a short replay read the critical byte at
  `MAIN.EXE+0xAD87` and speed at `+0x12997`. No read after
  initialization touched the modifiers `+0x0C/+0x0E/+0x10` or the
  word at `+0x40`. The ranged click left the item in the hand, so no
  ranged attack was seen.
- **A native save would add:** a party with a ranged weapon ready,
  to follow a real projectile through the release routine.
