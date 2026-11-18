#!/usr/bin/env python3
"""Extract a finite MIDI note timeline from an original LoL1 ADL track."""
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
import struct
import sys

import lol1lib as L
from xmi_to_midi import to_smf, verify_smf

# Operand widths, including stop aliases, from ScummVM adlib.cpp:2051–2166.
WIDTHS = (
    1, 2, 1, 1, 2, 2, 0, 1, 0, 1, 2, 2, 1, 5, 1, 1,
    1, 3, 0, 1, 0, 4, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0,
    1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 2, 2, 1, 1,
    1, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 1, 1, 0, 2,
    0, 9, 1, 0, 2, 2, 2, 1, 1, 2, 0,
)
STOP = {0x88, 0x94, 0x96, 0x97, 0x98, 0x99, 0x9B, 0x9F, 0xA2, 0xA3,
        0xA5, 0xA8, 0xAA, 0xB1, 0xB2, 0xB4, 0xB7, 0xB8, 0xBE, 0xCA}
CALLBACK_HZ = 72
MIDI_DIVISION = CALLBACK_HZ // 2


class Adl:
    def __init__(self, data):
        bases = [base for base in (250, 500)
                 if len(data) >= base + 2002 and data[base:base + 2] == b'\xd0\x07']
        if len(bases) != 1:
            raise ValueError("can't identify the original LoL1 ADL track map")
        base = bases[0]
        self.tracks = tuple(data[:base]) if base == 250 else struct.unpack_from("<250H", data)
        self.empty = 0xFF if base == 250 else 0xFFFF
        self.data = data[base:]
        programs = struct.unpack_from("<500H", self.data)
        instruments = struct.unpack_from("<500H", self.data, 1000)
        for offsets, size in ((programs, 2), (instruments, 11)):
            for offset in offsets:
                if offset not in (0, 0xFFFF) and not 2000 <= offset <= len(self.data) - size:
                    raise ValueError(f"out-of-bounds ADL table entry 0x{offset:X}")
        self.programs = programs

    def program(self, program_id):
        if program_id < len(self.programs):
            offset = self.programs[program_id]
            if offset not in (0, 0xFFFF) and self.data[offset] < 10:
                return offset


@dataclass
class Channel:
    pos: int | None = None
    priority: int = 0
    tempo: int = 255
    timer: int = 255
    duration: int = 1
    repeat: int = 0
    stack: list = field(default_factory=list)
    spacing: int = 1
    fractional: int = 0
    spacing2: int = 0
    randomness: int = 0
    octaves: int = 0
    base_note: int = 0
    pending: int = 0
    sounding: int | None = None
    tempo_reset: bool = False


def signed(value):
    return value if value < 128 else value - 256


class Projection:
    def __init__(self, adl):
        self.adl = adl
        self.channels = [Channel() for _ in range(10)]
        self.events = []
        self.unmapped = Counter()
        self.faults = Counter()
        self.tick = 0
        self.tempo = 0
        self.beat_divider = self.beat_countdown = self.beat = self.beat_wait = 0
        self.beat_timer = 255
        self.random = 0x1234

    def key_off(self, number):
        channel = self.channels[number]
        if channel.sounding is not None:
            self.events.append((self.tick, len(self.events), bytes((0x80 + number, channel.sounding, 0))))
            channel.sounding = None

    def pitch(self, number, raw, key_on):
        if number == 9:
            return
        channel = self.channels[number]
        if raw is not None:
            note = (raw & 15) + channel.base_note
            block = ((raw + channel.octaves) >> 4) & 15
            channel.pending = max(0, min(127, 12 * (block + 1) + note))
        if key_on or channel.sounding is not None:
            self.key_off(number)
            channel.sounding = channel.pending
            self.events.append((self.tick, len(self.events), bytes((0x90 + number, channel.pending, 80))))

    def stop(self, number):
        self.key_off(number)
        self.channels[number].pos = None
        self.channels[number].priority = 0

    def start(self, offset, caller=None):
        number, priority = self.adl.data[offset:offset + 2]
        if priority >= self.channels[number].priority:
            self.key_off(number)
            pos = caller.pos if caller is self.channels[number] else offset + 2
            self.channels[number] = Channel(pos=pos, priority=priority)

    def set_duration(self, channel, duration):
        if channel.randomness:
            value = (self.random + 0x9248) & 0xFFFF
            self.random = (value >> 3) | ((value & 7) << 13)
            duration += self.random & channel.randomness
        elif channel.fractional:
            channel.spacing2 = (duration >> 3) * channel.fractional
        channel.duration = duration & 0xFF

    def step_channel(self, number):
        channel = self.channels[number]
        if channel.pos is None:
            return
        if channel.tempo_reset:
            channel.tempo = self.tempo
        elapsed = channel.timer + channel.tempo
        channel.timer = elapsed & 0xFF
        if elapsed < 256:
            return
        channel.duration = (channel.duration - 1) & 0xFF
        if channel.duration:
            if channel.duration in (channel.spacing, channel.spacing2):
                self.key_off(number)
            return
        for _ in range(4096):
            channel = self.channels[number]
            pos = channel.pos
            data = self.adl.data
            if pos is None:
                return
            if not 0 <= pos < len(data):
                self.faults["instruction outside data"] += 1
                break
            opcode = min(data[pos], 0xCA)
            width = WIDTHS[opcode - 0x80] if opcode >= 0x80 else 1
            end = pos + 1 + width
            if end > len(data):
                self.faults["truncated instruction"] += 1
                break
            args = data[pos + 1:end]
            channel.pos = end
            if opcode < 0x80:
                self.pitch(number, opcode, True)
                self.set_duration(channel, args[0])
                if args[0]:
                    return
            elif self.command(number, opcode, args):
                return
        else:
            self.faults["instruction budget"] += 1
        self.stop(number)

    def command(self, number, opcode, args):
        channel = self.channels[number]
        value = args[0] if args else 0
        if opcode in STOP:
            self.stop(number)
            return True
        if opcode in (0x81, 0x84, 0x85):
            if opcode == 0x81:
                channel.repeat = (channel.repeat - 1) & 0xFF
                if not channel.repeat:
                    return False
            dest = channel.pos + int.from_bytes(args, "little", signed=True)
            if not 0 <= dest < len(self.adl.data):
                self.faults["branch outside data"] += 1
                if opcode == 0x84:
                    self.stop(number)
                    return True
                return False
            if opcode == 0x85:
                if len(channel.stack) == 4:
                    self.faults["call stack full"] += 1
                    return False
                channel.stack.append(channel.pos)
            channel.pos = dest
        elif opcode == 0x86:
            if channel.stack:
                channel.pos = channel.stack.pop()
            else:
                self.faults["return without call"] += 1
                self.stop(number)
                return True
        elif opcode in (0x89, 0x8B, 0xA0, 0xA1):
            if opcode == 0x89:
                self.key_off(number)
            elif opcode in (0x8B, 0xA1):
                self.pitch(number, value if opcode == 0x8B else None, opcode == 0xA1)
            self.set_duration(channel, args[-1])
            return bool(args[-1])
        elif opcode in (0x82, 0x8F):
            if opcode == 0x82 and value == 0xFF:
                return False
            offset = self.adl.program(value)
            if offset is not None:
                if opcode == 0x82:
                    self.start(offset, channel)
                elif self.channels[self.adl.data[offset]].pos is not None:
                    channel.pos -= 2
                    return True
        elif opcode in (0x8E, 0xB3) and value < 10:
            pos = channel.pos
            self.stop(value)
            self.channels[value].duration = 0
            channel.pos = pos
        elif opcode == 0x9C:
            self.beat_divider = self.beat_countdown = value >> 1
            self.beat_timer = 255
            self.beat = self.beat_wait = 0
        elif opcode == 0x9D:
            if self.beat & value and self.beat_wait:
                self.beat_wait = 0
            else:
                if not self.beat & value:
                    self.beat_wait = (self.beat_wait + 1) & 0xFF
                channel.pos -= 2
                channel.duration = 1
                return True
        elif opcode == 0xA6:
            self.tempo = value
        elif opcode == 0xBA:
            channel.tempo = self.tempo
        elif opcode == 0xBD:
            channel.tempo = max(1, min(255, channel.tempo + signed(value)))
        elif opcode in (0x80, 0x83, 0x87, 0x8C, 0x9A, 0xA4, 0xA9, 0xBC, 0xC8):
            field, value = {
                0x80: ("repeat", value), 0x83: ("spacing", value), 0x87: ("octaves", signed(value)),
                0x8C: ("base_note", signed(value)), 0x9A: ("priority", value),
                0xA4: ("fractional", value & 7), 0xA9: ("tempo", value),
                0xBC: ("randomness", value), 0xC8: ("tempo_reset", bool(value)),
            }[opcode]
            setattr(channel, field, value)
        elif opcode not in (0xBB, 0xC0):
            self.unmapped[opcode] += 1
        return False

    def run(self, offset, limit):
        self.start(offset)
        for self.tick in range(limit):
            if all(channel.pos is None for channel in self.channels):
                break
            for number in range(9, -1, -1):
                self.step_channel(number)
            elapsed = self.beat_timer + self.tempo
            self.beat_timer = elapsed & 0xFF
            if elapsed >= 256:
                self.beat_countdown = (self.beat_countdown - 1) & 0xFF
                if not self.beat_countdown:
                    self.beat_countdown = self.beat_divider
                    self.beat = (self.beat + 1) & 0xFF
        capped = any(channel.pos is not None for channel in self.channels)
        if capped:
            self.tick = limit
        for number in range(9):
            self.key_off(number)
        return to_smf(self.events, self.tick, MIDI_DIVISION), capped


def check(data_dir):
    assets = projections = audible = missing = known_stops = 0
    problems = []
    for _pak, name, blob in L.find_all(".ADL", data_dir):
        assets += 1
        adl = Adl(blob)
        ids = {program for program in adl.tracks if program != adl.empty}
        missing += sum(adl.program(program) is None for program in ids)
        for offset in sorted({adl.program(program) for program in ids} - {None}):
            player = Projection(adl)
            midi, _ = player.run(offset, CALLBACK_HZ * 4)
            valid, notes = verify_smf(midi, MIDI_DIVISION)
            if not valid:
                raise ValueError(f"{name} program at 0x{offset:X}: MIDI round-trip failed")
            if player.faults:
                # The short-map floppy LORESFX has one out-of-range repeat
                # target. See docs/unknowns/15_adl_and_c55.md.
                if (adl.empty == 0xFF and name == "LORESFX.ADL" and offset == 0x878
                        and adl.data[0x88C:0x88F] == b"\x81\x41\x22"
                        and player.faults == {"branch outside data": 1}):
                    known_stops += 1
                else:
                    problems.append(f"{name}+0x{offset:X}: {dict(player.faults)}")
            projections += 1
            audible += bool(notes)
    print(f"CHECK ADL: {assets} assets, {projections} entry projections ({audible} with notes), "
          f"{missing} unavailable entry IDs, {known_stops} documented out-of-range repeats, "
          f"unexpected issues: {problems or 'none'}")
    return 0 if assets and audible and not problems else 1


def main():
    ap = L.tool_args(__doc__, out_help="write Standard MIDI File to this local path")
    ap.add_argument("name", nargs="?", help="original member, e.g. LORE01B.ADL")
    ap.add_argument("--track", type=int, default=2, help="track map slot, 0–249")
    ap.add_argument("--seconds", type=int, default=90, help="timeline cutoff, 1–600")
    a = ap.parse_args()
    if a.check:
        return check(a.data)
    if not a.name or not 0 <= a.track < 250 or not 1 <= a.seconds <= 600:
        ap.error("provide an ADL member, a track in 0–249 and a cutoff in 1–600 seconds")
    if a.out:
        target = Path(a.out).resolve()
        repo = Path(__file__).resolve().parents[1]
        if target.suffix.lower() != ".mid" or target.is_relative_to(repo) or target.is_relative_to(Path(a.data).resolve()):
            ap.error("--out needs a .mid path outside the repository and game data")
    _pak, blob = L.find_member(a.name, a.data)
    adl = Adl(blob)
    track = adl.tracks[a.track]
    offset = None if track == adl.empty else adl.program(track)
    if offset is None:
        ap.error("track has no playable program")
    player = Projection(adl)
    midi, capped = player.run(offset, CALLBACK_HZ * a.seconds)
    valid, notes = verify_smf(midi, MIDI_DIVISION)
    if not valid:
        raise ValueError("MIDI round-trip failed")
    if a.out:
        target.write_bytes(midi)
    unmapped = ", ".join(f"{op:02X}" for op in sorted(player.unmapped)) or "none"
    print(f"{a.name} slot {a.track}: {notes} notes, {player.tick} callbacks"
          f"{' (time cutoff)' if capped else ''}; unmapped controls: {unmapped}; stops: {dict(player.faults)}")
    return bool(player.faults)


if __name__ == "__main__":
    sys.exit(main())
