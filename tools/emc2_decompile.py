#!/usr/bin/env python3
"""Read an original LoL1 EMC2 script from a file or PAK member."""

from cli_errors import ReaderArgumentParser, run_cli
from collections import defaultdict
from dataclasses import dataclass
import json
import os
from pathlib import Path
import struct
import sys


# ScummVM engines/kyra/script/script.cpp:29–55 and :228–453.
OPCODES = (
    "jmp", "setRetValue", "pushRetOrPos", "push", "push", "pushReg",
    "pushBPNeg", "pushBPAdd", "popRetOrPos", "popReg", "popBPNeg",
    "popBPAdd", "addSP", "subSP", "sysCall", "ifNotJmp", "negate",
    "eval", "setRetAndJmp",
)
NEGATE = ("not", "unary minus", "bitwise complement")
EVAL = ("and", "or", "==", "!=", ">", ">=", "<", "<=", "+", "-", "*", "/",
        ">>", "<<", "&", "|", "%", "^")

# ScummVM engines/kyra/script/script_lol.cpp:2683–2974.
# None marks entries with no ScummVM handler. Slot 0x7E has a native handler
# confirmed in both editions, documented in docs/emc2_scripts.md.
FUNCTIONS = (
    'setWallType', 'getWallType', 'drawScene', 'rollDice',  # 0x00
    'moveParty', None, 'delay', 'setGameFlag',  # 0x04
    'testGameFlag', 'loadLevelGraphics', 'loadBlockProperties', 'loadMonsterShapes',  # 0x08
    'deleteHandItem', 'allocItemPropertiesBuffer', 'setItemProperty', 'makeItem',  # 0x0C
    'placeMoveLevelItem', 'createLevelItem', 'getItemPara', 'getCharacterStat',  # 0x10
    'setCharacterStat', 'loadLevelShapes', 'closeLevelShapeFile', None,  # 0x14
    'loadDoorShapes', 'initAnimStruct', 'playAnimationPart', 'freeAnimStruct',  # 0x18
    'getDirection', 'characterSurpriseFeedback', 'setMusicTrack', 'setSequenceButtons',  # 0x1C
    'setDefaultButtonState', 'checkRectForMousePointer', 'clearDialogueField', 'setupBackgroundAnimationPart',  # 0x20
    'startBackgroundAnimation', 'hideMouse', 'showMouse', 'fadeToBlack',  # 0x24
    'fadePalette', 'loadBitmap', 'stopBackgroundAnimation', None,  # 0x28
    None, 'getGlobalScriptVar', 'setGlobalScriptVar', 'getGlobalVar',  # 0x2C
    'setGlobalVar', 'triggerDoorSwitch', 'checkEquippedItemScriptFlags', 'setDoorState',  # 0x30
    'updateBlockAnimations', 'assignLevelDecorationShape', 'resetBlockShapeAssignment', 'copyRegion',  # 0x34
    'initMonster', 'fadeClearSceneWindow', 'fadeSequencePalette', 'redrawPlayfield',  # 0x38
    'loadNewLevel', 'getNearestMonsterFromCharacter', 'dummy0', 'loadMonsterProperties',  # 0x3C
    'battleHitSkillTest', 'inflictDamage', None, None,  # 0x40
    'moveMonster', 'setupDialogueButtons', 'giveTakeMoney', 'checkMoney',  # 0x44
    'setScriptTimer', 'createHandItem', 'playAttackSound', 'addRemoveCharacter',  # 0x48
    'giveItem', None, 'loadTimScript', 'runTimScript',  # 0x4C
    'releaseTimScript', 'initSceneWindowDialogue', 'restoreAfterSceneWindowDialogue', 'getItemInHand',  # 0x50
    'checkMagic', 'giveItemToMonster', 'loadLangFile', 'playSoundEffect',  # 0x54
    'processDialogue', 'stopTimScript', 'getWallFlags', 'changeMonsterStat',  # 0x58
    'getMonsterStat', 'releaseMonsterShapes', 'playCharacterScriptChat', 'update',  # 0x5C
    'playEnvironmentalSfx', 'healCharacter', 'drawExitButton', 'loadSoundFile',  # 0x60
    'playMusicTrack', 'deleteMonstersFromBlock', 'countBlockItems', 'characterSkillTest',  # 0x64
    'countAllMonsters', 'playEndSequence', 'stopPortraitSpeechAnim', 'setPaletteBrightness',  # 0x68
    'calcInflictableDamage', 'getInflictedDamage', 'checkForCertainPartyMember', 'printMessage',  # 0x6C
    'deleteLevelItem', 'calcInflictableDamagePerItem', 'distanceAttack', 'removeCharacterEffects',  # 0x70
    'checkInventoryFull', 'moveBlockObjects', None, None,  # 0x74
    'addSpellToScroll', 'playDialogueText', 'playDialogueTalkText', 'checkMonsterTypeHostility',  # 0x78
    'setNextFunc', 'dummy1', 'exitGame', 'suspendMonster',  # 0x7C
    'setScriptTextParameter', 'triggerEventOnMouseButtonClick', 'printWindowText', 'countSpecificMonsters',  # 0x80
    'updateBlockAnimations2', 'checkPartyForItemType', 'blockDoor', 'resetTimDialogueState',  # 0x84
    'getItemOnPos', 'removeLevelItem', 'savePage5', 'restorePage5',  # 0x88
    'initDialogueSequence', 'restoreAfterDialogueSequence', 'setSpecialSceneButtons', 'restoreButtonsAfterSpecialScene',  # 0x8C
    None, None, 'prepareSpecialScene', 'restoreAfterSpecialScene',  # 0x90
    'assignCustomSfx', None, 'findAssignedMonster', 'checkBlockForMonster',  # 0x94
    'crossFadeRegion', 'calcCoordinatesAddDirectionOffset', 'resetPortraitsAndDisableSysTimer', 'enableSysTimer',  # 0x98
    'checkNeedSceneRestore', 'getNextActiveCharacter', 'paralyzePoisonCharacter', 'drawCharPortrait',  # 0x9C
    'removeInventoryItem', None, None, 'getAnimationLastPart',  # 0xA0
    'assignSpecialGuiShape', 'findInventoryItem', 'restoreFadePalette', 'calcNewBlockPosition',  # 0xA4
    'getSelectedCharacter', 'setHandItem', 'drinkBezelCup', 'changeItemTypeOrFlag',  # 0xA8
    'placeInventoryItemInHand', 'castSpell', 'pitDrop', 'increaseSkill',  # 0xAC
    'paletteFlash', 'restoreMagicShroud', 'dummy1', 'disableControls',  # 0xB0
    'enableControls', 'shakeScene', 'gasExplosion', 'calcNewBlockPosition',  # 0xB4
    'crossFadeScene', 'updateDrawPage2', 'setMouseCursor', 'characterSays',  # 0xB8
    'queueSpeech', 'getItemPrice', 'getLanguage', 'dummy0',  # 0xBC
)


# Positions read with stackPosString. -1 is permitted for loadLevelGraphics arg 5.
STRING_ARGUMENTS = {
    0x09: (0, 5), 0x0A: (0,), 0x0B: (0,), 0x15: (0, 1), 0x18: (0,),
    0x19: (0,), 0x29: (0,), 0x4E: (1,), 0x56: (0,), 0x94: (0,),
}


@dataclass(frozen=True)
class Instruction:
    address: int
    opcode: int
    argument: int

    @property
    def target(self):
        if self.opcode == 0:
            return self.argument
        if self.opcode == 15:
            return self.argument & 0x7FFF
        return None


@dataclass(frozen=True)
class Script:
    chunks: dict
    entries: dict
    strings: list
    words: tuple
    instructions: list


def read_chunks(data):
    if len(data) < 12 or data[:4] != b"FORM" or data[8:12] != b"EMC2":
        raise ValueError("expected FORM/EMC2")
    declared, = struct.unpack_from(">I", data, 4)
    # The original LoL1 files store total length. Also accept standard IFF size.
    if declared not in (len(data), len(data) - 8):
        raise ValueError(f"FORM size 0x{declared:X} disagrees with file size 0x{len(data):X}")
    chunks = {}
    pos = 12
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError(f"truncated chunk header at file+0x{pos:X}")
        tag, size = struct.unpack_from(">4sI", data, pos)
        start = pos + 8
        end = start + size
        pos = end + (size & 1)
        if pos > len(data) or tag in chunks:
            raise ValueError(f"truncated or duplicate chunk {tag!r} at file+0x{start - 8:X}")
        chunks[tag] = (start, data[start:end])
    if not {b"ORDR", b"DATA"} <= chunks.keys():
        raise ValueError("ORDR and DATA are required")
    return chunks


def be_words(data):
    if len(data) & 1:
        raise ValueError("expected an even-length word array")
    return tuple(word for word, in struct.iter_unpack(">H", data))


def read_strings(data):
    if not data:
        return []
    if len(data) < 2:
        raise ValueError("truncated TEXT offset table")
    first, = struct.unpack_from(">H", data)
    if not 2 <= first < len(data):
        raise ValueError("invalid first TEXT offset")
    strings = []
    for offset in be_words(data[:first]):
        end = data.find(b"\0", offset)
        if offset < first or end < 0:
            raise ValueError(f"invalid TEXT string offset 0x{offset:X}")
        strings.append((offset, data[offset:end]))
    return strings


def decode_words(words, entries):
    instructions = []
    address = 0
    while address < len(words):
        pos = address
        word = words[address]
        address += 1
        if pos in entries:
            continue
        opcode = (word >> 8) & 0x1F
        argument = 0
        if word & 0x8000:
            opcode, argument = 0, word & 0x7FFF
        elif word & 0x4000:
            argument = word & 0xFF
            if argument >= 0x80:
                argument -= 0x100
        elif word & 0x2000:
            if address == len(words) or address in entries:
                raise ValueError(f"missing operand word at DATA word 0x{pos:X}")
            argument = words[address]
            if argument >= 0x8000:
                argument -= 0x10000
            address += 1
        if opcode >= len(OPCODES):
            raise ValueError(f"unknown opcode 0x{opcode:X} at DATA word 0x{pos:X}")
        if opcode == 14:
            argument &= 0xFF
            if argument >= len(FUNCTIONS):
                raise ValueError(f"unknown function 0x{argument:02X} at DATA word 0x{pos:X}")
        if opcode in (16, 17):
            names = NEGATE if opcode == 16 else EVAL
            if not 0 <= argument < len(names):
                raise ValueError(f"unknown {OPCODES[opcode]} selector {argument} at DATA word 0x{pos:X}")
        instructions.append(Instruction(pos, opcode, argument))
    return instructions


def read_script(data):
    chunks = read_chunks(data)
    words = be_words(chunks[b"DATA"][1])
    entries = defaultdict(list)
    for index, offset in enumerate(be_words(chunks[b"ORDR"][1])):
        if offset == 0xFFFF:
            continue
        if offset + 1 >= len(words):
            raise ValueError(f"ORDR entry 0x{index:X} outside DATA")
        entries[offset].append(index)
    strings = read_strings(chunks.get(b"TEXT", (0, b""))[1])
    instructions = decode_words(words, entries)
    boundaries = {instruction.address for instruction in instructions}
    for offset in entries:
        if offset + 1 not in boundaries:
            raise ValueError(f"ORDR entry at DATA word 0x{offset:X} has no instruction")
    for instruction in instructions:
        target = instruction.target
        if target is not None and target not in boundaries:
            raise ValueError(f"invalid branch target 0x{target:X} at DATA word 0x{instruction.address:X}")
    return Script(chunks, dict(entries), strings, words, instructions)


def quoted_string(raw):
    # Both English witnesses contain ASCII. Preserve other bytes as escapes.
    return json.dumps(raw.decode("latin-1"), ensure_ascii=True)


def format_listing(script, name):
    yield f"; {name} | {len(script.words)} DATA words | {len(script.strings)} TEXT strings"
    for tag, (pos, payload) in script.chunks.items():
        yield f"; {tag.decode('ascii')} payload at file+0x{pos:X} ({len(payload)} bytes)"
    for index, (offset, raw) in enumerate(script.strings):
        yield f"; TEXT[{index}] +0x{offset:04X} {quoted_string(raw)}"

    branch_targets = {ins.target for ins in script.instructions}
    recent_pushes = []
    for ins in script.instructions:
        header = ins.address - 1
        if header in script.entries:
            ids = ", ".join(f"0x{index:X}" for index in script.entries[header])
            yield f"\n; ORDR[{ids}] at word 0x{header:04X}, header 0x{script.words[header]:04X}"
            recent_pushes.clear()
        if ins.address in branch_targets:
            yield f"L_{ins.address:04X}:"
            recent_pushes.clear()

        opcode, argument = ins.opcode, ins.argument
        operand = str(argument)
        if ins.target is not None:
            operand = f"L_{ins.target:04X}"
        elif opcode == 14:
            name = FUNCTIONS[argument] or "unimplemented (ScummVM)"
            operand = f"0x{argument:02X} {name}"
            for slot in STRING_ARGUMENTS.get(argument, ()):
                if slot < len(recent_pushes):
                    index = recent_pushes[-1 - slot]
                    if 0 <= index < len(script.strings):
                        raw = script.strings[index][1]
                        operand += f" [arg{slot}=TEXT[{index}] {quoted_string(raw)}]"
        elif opcode in (16, 17):
            label = (NEGATE if opcode == 16 else EVAL)[argument]
            operand = f"{argument} ({label})"
        elif opcode == 18:
            operand = ""
        yield f"  {ins.address:04X}  {OPCODES[opcode]:<16} {operand}".rstrip()
        if opcode in (3, 4):
            recent_pushes.append(argument)
        else:
            recent_pushes.clear()


def pak_entries(path):
    """Yield DOS PAK entry names, offsets and lengths in directory order."""
    with path.open("rb") as stream:
        size = path.stat().st_size
        first, = struct.unpack("<I", stream.read(4))
        if not 4 <= first <= size:
            raise ValueError(f"{path.name}: invalid first PAK offset")
        directory = stream.read(first - 4)
    start, pos = first, 0
    while pos < len(directory) and directory[pos]:
        name_end = directory.find(b"\0", pos)
        if name_end < 0:
            raise ValueError(f"{path.name}: unterminated PAK name")
        name = directory[pos:name_end].decode("ascii")
        pos = name_end + 1
        if pos == len(directory):
            end = size
        else:
            if pos + 4 > len(directory):
                raise ValueError(f"{path.name}: truncated PAK offset")
            end, = struct.unpack_from("<I", directory, pos)
            pos += 4
            end = end or size
        if not start <= end <= size:
            raise ValueError(f"{path.name}: invalid PAK range for {name}")
        yield name, start, end - start
        if end == size:
            break
        start = end


def read_entry(path, offset, size):
    with path.open("rb") as stream:
        stream.seek(offset)
        return stream.read(size)


def quiet_broken_pipe():
    """The reader closed the pipe (e.g. `| head`): stop quietly, as cat does.
    Point stdout at devnull so the interpreter's final flush does not complain."""
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    except (OSError, ValueError):
        pass


def write_stdout(text, stream=None):
    """Write text to stdout and flush, so a closed pipe shows up here, not at exit."""
    stream = stream or sys.stdout
    stream.write(text)
    stream.flush()


def main():
    parser = ReaderArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Loose INF/INI script, or DOS PAK with --entry; "
                        "a bare name such as L01.PAK is looked up in --data")
    parser.add_argument("--data", type=Path, default=os.environ.get("LOL1_DATA"),
                        help="the game's DATA folder for bare names (default: $LOL1_DATA)")
    parser.add_argument("--entry", help="INF/INI name within the PAK (case-insensitive)")
    parser.add_argument("-o", "--out", "--output", type=Path, help="Write listing here instead of stdout")
    args = parser.parse_args()
    try:
        if not args.input.exists() and args.data and (args.data / args.input).exists():
            args.input = args.data / args.input
        name = args.input.name
        if args.entry:
            for entry, offset, size in pak_entries(args.input):
                if entry.casefold() == args.entry.casefold():
                    data = read_entry(args.input, offset, size)
                    name += f"/{entry} (PAK+0x{offset:X})"
                    break
            else:
                raise ValueError(f"{args.entry} is absent from the PAK")
        else:
            data = args.input.read_bytes()
        listing = "\n".join(format_listing(read_script(data), name)) + "\n"
        if args.out:
            with args.out.open("x", encoding="utf-8") as output:
                output.write(listing)
        else:
            write_stdout(listing)
    except BrokenPipeError:
        quiet_broken_pipe()
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, str(error))


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
