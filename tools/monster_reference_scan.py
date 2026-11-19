#!/usr/bin/env python3
"""Check the encoded original LoL1 DOS monster definition access paths. Requires Capstone."""
import argparse
import struct
from collections import Counter
from pathlib import Path

from capstone import CS_ARCH_X86, CS_MODE_16, Cs
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_DS, X86_REG_ES

FIELDS = (0x0C, 0x0E, 0x10, 0x3D, 0x40)


def decoded_at(decoder, image, position):
    return next(decoder.disasm(image[position:position + 15], position, 1), None)


def pointer_accesses(decoder, image, load, adjustment):
    """Follow straight-line offsets and register copies within the load's block."""
    segment = X86_REG_ES if load.mnemonic == "les" else X86_REG_DS
    aliases = {load.operands[0].reg: adjustment}
    start = load.address + load.size
    for instruction in decoder.disasm(image[start:start + 140], start):
        operands = instruction.operands
        if instruction.mnemonic != "lea":
            for operand in operands:
                if (operand.type != X86_OP_MEM or operand.mem.index
                        or operand.mem.base not in aliases
                        or operand.mem.segment not in ((0, segment) if segment == X86_REG_DS else (segment,))):
                    continue
                field = aliases[operand.mem.base] + operand.mem.disp
                if any(field <= key < field + operand.size for key in (*FIELDS, 0x0A)):
                    yield instruction.address, field, operand.access
        if (instruction.mnemonic in ("les", "lds", "jmp", "ljmp", "call", "lcall", "ret", "retf", "iret")
                or segment in instruction.regs_access()[1]):
            break
        transferred = {}
        if len(operands) == 2 and operands[0].type == X86_OP_REG:
            destination, source = operands
            if instruction.mnemonic == "mov" and source.type == X86_OP_REG and source.reg in aliases:
                transferred[destination.reg] = aliases[source.reg]
            if (instruction.mnemonic in ("add", "sub") and source.type == X86_OP_IMM
                    and destination.reg in aliases):
                delta = source.imm if instruction.mnemonic == "add" else -source.imm
                transferred[destination.reg] = aliases[destination.reg] + delta
        for register in instruction.regs_access()[1]:
            name = instruction.reg_name(register)
            # The compiler can overwrite a byte of a 16-bit offset register.
            full = {"bl": "bx", "bh": "bx", "al": "ax", "ah": "ax",
                    "cl": "cx", "ch": "cx", "dl": "dx", "dh": "dx"}.get(name, name)
            aliases = {reg: offset for reg, offset in aliases.items() if instruction.reg_name(reg) != full}
        aliases.update(transferred)
        if not aliases:
            break


def word_offsets(image, value, start):
    needle = struct.pack("<H", value)
    position = image.find(needle, start)
    while position >= 0:
        yield position
        position = image.find(needle, position + 1)


def scan(path, bank, instance_alias, setter, far_setter):
    image = path.read_bytes()
    if image[:2] != b"MZ":
        raise ValueError("expected a DOS MZ program")
    start = 16 * struct.unpack_from("<H", image, 8)[0]
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    counts = Counter()
    reads = set()
    for position in range(start, len(image) - 1):
        first = image[position]
        if first in (0x26, 0x3E):
            if image[position + 1] not in (0xC4, 0xC5):
                continue
        elif first not in (0xC4, 0xC5) or image[position - 1] in (0x26, 0x3E):
            continue
        load = decoded_at(decoder, image, position)
        if not load or load.mnemonic not in ("les", "lds") or load.operands[1].type != X86_OP_MEM:
            continue
        displacement = load.operands[1].mem.disp
        if displacement in (0x21, instance_alias):
            counts["instance"] += 1
            reads.update(pointer_accesses(decoder, image, load, 0))
        elif displacement == 0x14:
            counts["stat"] += 1
            reads.update(pointer_accesses(decoder, image, load, 2))

    direct = set()
    for field in FIELDS:
        for slot in range(5):
            address = bank + 0x53 * slot + field
            for operand_at in word_offsets(image, address, start):
                for position in range(max(start, operand_at - 7), operand_at):
                    instruction = decoded_at(decoder, image, position)
                    if (instruction and instruction.disp_size == 2
                            and position + instruction.disp_offset == operand_at
                            and any(o.type == X86_OP_MEM and o.mem.segment == X86_REG_ES
                                    and o.mem.disp == address for o in instruction.operands)):
                        direct.add(position)

    calls = []
    literal_mode_writes = []
    for position in range(start, len(image) - 4):
        if (image[position] == 0xE8
                and position + 3 + struct.unpack_from("<h", image, position + 1)[0] == setter):
            calls.append(position)
        if (image[position:position + 2] == b"\x26\xC6"
                and image[position + 2] & 0xF8 == 0x40
                and image[position + 3:position + 5] == b"\x14\x0A"):
            literal_mode_writes.append(position)
    far = image.count(far_setter, start)
    return counts, sorted(reads), direct, calls, far, literal_mode_writes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cd", type=Path, required=True)
    parser.add_argument("--floppy", type=Path, required=True)
    parser.add_argument("--check", action="store_true", required=True)
    args = parser.parse_args()
    try:
        for label, path, bank, alias, setter, far, expected, read_sites, stores in (
            ("CD", args.cd, 0x1B5E, 0x161B, 0x11855, "9a95096c0d", (57, 7, 13, 7),
             (0xAD87, 0x12744, 0x12997), (0x47992, 0x479BC, 0x479E6, 0x47AC4, 0x47ADD)),
            ("floppy", args.floppy, 0x1B40, 0x15FD, 0x162F1, "9a91091611", (58, 7, 13, 8),
             (0xACC8, 0x170E2, 0x17336), (0x51171, 0x5119B, 0x511C5, 0x512A3, 0x512BC)),
        ):
            counts, accesses, direct, calls, remote, literal_writes = scan(path, bank, alias, setter, bytes.fromhex(far))
            expected_reads = list(zip(read_sites, (0x3D, 0x0A, 0x0A), (1, 1, 1)))
            if ((counts["instance"], counts["stat"], len(calls), remote) != expected
                    or accesses != expected_reads or direct or literal_writes):
                raise ValueError(f"{label} reference census changed")
            image = path.read_bytes()
            for address, field in zip(stores, (0x0C, 0x0E, 0x10, 0x40, 0x40)):
                if image[address:address + 4] != bytes((0x26, 0x89, 0x47, field)):
                    raise ValueError(f"{label} setter store 0x{address:X}")
            print(f"CHECK {label} monster references: {counts['instance']} instance and {counts['stat']} "
                  f"stat load candidates, 1 critical read, 2 speed controls, 5 definition stores; "
                  f"{len(calls)} near and {remote} far mode setter encodings")
    except (OSError, struct.error, ValueError) as error:
        parser.exit(1, f"CHECK monster reference scan: {error}\n")


if __name__ == "__main__":
    main()
