#!/usr/bin/env python3
"""Mode-byte stores, the finale catalog row, and three palette indexes.

Static read of the original programs and scripts. No game, no debugger.

  lol1_mode_paths.py --check --data DATA
  lol1_mode_paths.py --check --data DATA --floppy FLOPPY_DIR

On the CD folder the check reads HARDRIVE/MAIN.EXE, ENG/FINALE.EXE and
FILEDATA.FDT. On a floppy folder it reads MAIN.EXE. Pass --floppy as well
to check that edition in the same run.
"""
from cli_errors import ReaderArgumentParser, run_cli
import struct
import sys
from pathlib import Path

import emc2_decompile as E
import lol1lib as L

try:
    from capstone import CS_ARCH_X86, CS_MODE_16, Cs
    from capstone.x86_const import X86_OP_IMM
except ImportError:
    Cs = None


EVAL = {8: lambda b, a: b + a, 9: lambda b, a: b - a, 10: lambda b, a: b * a,
        12: lambda b, a: b >> a, 13: lambda b, a: b << a, 14: lambda b, a: b & a,
        15: lambda b, a: b | a, 17: lambda b, a: b ^ a}

# CD instance array is DS:0x15FA. Floppy is DS:0x15DC. Stride 0x2E.
CD_STORES = {
    0x11474: "writes 15, then the query restores the saved byte",
    0x114AC: "restores the byte saved at entry",
    0x118AC: "writes 7 into each slot whose mode is 1",
    0x118FA: "writes the caller argument",
    0x11920: "writes 0 when the argument is 13 and bit 0x20 is set",
    0x44806: "writes 0 when current HP is at most the compared word and bit 0x20 is set",
    0x448EC: "writes 0 when the mode is 11 and bit 0x20 is set",
    0x45FD1: "writes 16 into each of the 30 slots after clearing the slot",
    0x50B44: "writes 8 into each listed monster whose mode is below 13",
    0x50BBB: "restores the mode saved before that 8",
}
FL_STORES = {
    0x15F10: "writes 15, then the query restores the saved byte",
    0x15F48: "restores the byte saved at entry",
    0x16348: "writes 7 into each slot whose mode is 1",
    0x16396: "writes the caller argument",
    0x163BC: "writes 0 when the argument is 13 and bit 0x20 is set",
    0x4F791: "writes 16 into each of the 30 slots after clearing the slot",
    0x5A9C8: "writes 8 into each listed monster whose mode is below 13",
    0x5AA40: "restores the mode saved before that 8",
}
# Near and far calls of the CD setter, and the immediate they push. None means
# the value is a register or a script word, not an immediate.
CD_CALLS = {
    0x1193E: 14, 0x11E74: 8, 0x12149: None, 0x121EE: 7, 0x12273: 9,
    0x122A2: 7, 0x122CA: 7, 0x12421: 3, 0x12688: 7, 0x12827: 7,
    0x12947: 7, 0x12986: 5, 0x129FE: 7,
    0xAEC3: 14, 0xB265: 13, 0xD1F9: 14, 0x14826: None, 0x14FC1: None,
    0x15833: 14, 0x159E4: 14, 0x44824: 14, 0x4490A: 14,
}


# Two blit loops in each program. mov bx, es; add bx, 0x14; mov es, bx;
# mov bx, ds; add bx, 0x14; mov ds, bx. A picture segment step, not the mode byte.
BLIT_STEP = bytes.fromhex("8cc383c3148ec38cdb83c3148edb")
CD_BLIT = (0x1E577, 0x1E692)
FL_BLIT = (0x1EC0F, 0x1ED2A)
# Register adds of 20 other than add bx, 0x14 (83 C3 14) that a pointer to the
# mode byte would need: none of these encodings occurs in either file.
NO_ADD20 = ("81c31400", "83c614", "81c61400", "83c714", "81c71400")
# The three add dx, 0x14 in each file follow mov dx, es:[bx+array+0x21], the
# instance's definition offset, so dx points 20 bytes into the definition.
CD_DEF20 = bytes.fromhex("268b971b1683c214")
FL_DEF20 = bytes.fromhex("268b97fd1583c214")
# The one mov byte [mem], 10 in each whole file: les bx, [bp-4]; add bx, si;
# mov byte es:[bx+0x78], 10. [bp-4] is the party record base (segment, offset)
# stored at the routine's entry, stride 0x82, not the 46-byte monster array.
TEN_STORE = bytes.fromhex("c45efc03de26c647780a")
CD_TEN = (0xF649, 0xF503, bytes.fromhex("c746fe0328c746fc2d36"))
FL_TEN = (0x14037, 0x13EF1, bytes.fromhex("c746fecf2dc746fc0f36"))


def fail(message):
    print(f"CHECK mode_paths FAILED: {message}")
    return 1


def need_capstone():
    if Cs is None:
        sys.exit("lol1_mode_paths.py needs the Capstone disassembler: "
                 "pip install -r requirements.txt (or pip install capstone)")


def header_size(data):
    return struct.unpack_from("<H", data, 8)[0] * 16


def seeds(data):
    hdr = header_size(data)
    found = {hdr}
    i = hdr
    while True:
        j = data.find(b"\x55\x8B\xEC", i)
        if j < 0:
            break
        found.add(j)
        i = j + 1
    for i in range(hdr, len(data) - 3):
        if data[i] == 0xE8:
            rel = struct.unpack_from("<h", data, i + 1)[0]
            tgt = i + 3 + rel
            if hdr <= tgt < len(data):
                found.add(tgt)
    return found


def walk(data):
    need_capstone()
    md = Cs(CS_ARCH_X86, CS_MODE_16)
    md.detail = True
    seen = set()
    queue = list(seeds(data))
    ins_at = {}
    while queue:
        addr = queue.pop()
        if addr in seen or not (0 <= addr < len(data) - 1):
            continue
        ins = next(md.disasm(data[addr:addr + 15], addr, 1), None)
        if ins is None:
            seen.add(addr)
            continue
        seen.add(addr)
        ins_at[addr] = ins
        nxt = addr + ins.size
        mnem = ins.mnemonic
        flow = []
        if mnem.startswith("j") and mnem != "jmp":
            flow.append(nxt)
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                flow.append(ins.operands[0].imm)
        elif mnem == "jmp":
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                flow.append(ins.operands[0].imm)
        elif mnem in ("call", "lcall", "loop", "loope", "loopne"):
            flow.append(nxt)
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                flow.append(ins.operands[0].imm & 0xFFFFF)
        elif mnem not in ("ret", "retf", "iret", "hlt"):
            flow.append(nxt)
        for target in flow:
            if target not in seen:
                queue.append(target)
    return ins_at


def imul_reg_imm8(window, imm):
    """True when window holds imul r16, r16, imm8 (opcode 6B, register ModRM)."""
    for i in range(len(window) - 2):
        if window[i] == 0x6B and window[i + 1] >= 0xC0 and window[i + 2] == imm:
            return True
    return False


def function_end(data, start):
    """Address of the last ret or retf reached from start, without following calls."""
    need_capstone()
    md = Cs(CS_ARCH_X86, CS_MODE_16)
    md.detail = True
    seen = set()
    queue = [start]
    end = None
    limit = start + 0x400
    while queue:
        addr = queue.pop()
        if addr in seen or not (start <= addr < limit) or addr >= len(data) - 1:
            continue
        ins = next(md.disasm(data[addr:addr + 15], addr, 1), None)
        if ins is None:
            continue
        seen.add(addr)
        if ins.mnemonic in ("ret", "retf", "iret", "hlt"):
            end = addr if end is None else max(end, addr)
            continue
        nxt = addr + ins.size
        if ins.mnemonic == "jmp":
            if ins.operands and ins.operands[0].type == X86_OP_IMM:
                queue.append(ins.operands[0].imm)
            continue
        queue.append(nxt)
        if (ins.mnemonic.startswith("j") or ins.mnemonic in ("loop", "loope", "loopne")) \
                and ins.operands and ins.operands[0].type == X86_OP_IMM:
            queue.append(ins.operands[0].imm)
    return end


def mode_stores(data, array_add):
    """Byte stores to the mode byte of a monster instance.

    Four shapes count. A store of es:[bx+base+0x14] indexes the array itself
    (bx is the slot times 0x2E, set by imul just before). An indexed slot is imul by 0x2E plus the array base
    within 0x60 bytes before the store. The collision query stores 15 and
    later restores the saved byte, with the definition load between them.
    The setter is the function that writes the array base into [bp+6] and
    compares the mode byte with 13; every such store in that function counts.
    """
    ins_at = walk(data)
    candidates = [addr for addr, ins in ins_at.items()
                  if ins.mnemonic == "mov" and ins.op_str.startswith("byte ptr es:[bx + 0x14]")]
    accepted = set()
    add_le = struct.pack("<H", array_add)
    indexed = f"byte ptr es:[bx + {array_add + 0x14:#x}]"
    for addr, ins in ins_at.items():
        if ins.mnemonic == "mov" and ins.op_str.startswith(indexed) \
                and imul_reg_imm8(data[max(0, addr - 0x10):addr], 0x2E):
            accepted.add(addr)
    for addr in candidates:
        window = data[max(0, addr - 0x60):addr]
        if imul_reg_imm8(window, 0x2E) and add_le in window:
            accepted.add(addr)
    for addr in candidates:
        if data[addr:addr + 5] != b"\x26\xC6\x47\x14\x0F":
            continue
        span = data[addr + 5:addr + 0x48]
        rel = span.find(b"\x26\x88\x47\x14")
        if rel < 0 or b"\x26\xC4\x5F\x21" not in data[addr:addr + 5 + rel]:
            continue
        restore = addr + 5 + rel
        if restore not in ins_at:
            continue
        accepted.add(addr)
        accepted.add(restore)
    sig = b"\xC7\x46\x06" + add_le
    hits = []
    at = 0
    while True:
        found = data.find(sig, at)
        if found < 0:
            break
        hits.append(found)
        at = found + 1
    if len(hits) != 1:
        return None, f"instance-array base store count is {len(hits)}"
    prologue = data.rfind(b"\x55\x8B\xEC", header_size(data), hits[0])
    if prologue < 0 or hits[0] - prologue > 0x80:
        return None, "setter prologue is not near the array base store"
    end = function_end(data, prologue)
    if end is None:
        return None, "setter does not return"
    if b"\x26\x80\x7F\x14\x0D" not in data[prologue:end + 1]:
        return None, "setter does not compare the mode with 13"
    for addr in candidates:
        if prologue <= addr <= end:
            accepted.add(addr)
    return sorted(accepted), None


def call_immediates(data, sites):
    """The push-imm8 nearest each call, within 24 bytes, or None when there is none.

    One site pushes 3 on one branch and 4 on the other. The byte immediately
    before that call is the push of 4. The caller checks both immediates.
    """
    out = {}
    for addr in sites:
        if data[addr:addr + 1] not in (b"\xE8", b"\x9A"):
            return None, f"call missing at {addr:#x}"
        prev = data[max(0, addr - 24):addr]
        k = prev.rfind(b"\x6A")
        if k >= 0 and k + 1 < len(prev):
            out[addr] = prev[k + 1]
        else:
            out[addr] = None
    return out, None


def script_modes(data_dir):
    """Resolved initMonster modes and changeMonsterStat selector-0 values."""
    modes = {}
    sel0 = {}
    raw38 = 0
    for suffix in (".INF", ".INI"):
        for pak, name, blob in L.find_all(suffix, data_dir):
            if not blob.startswith(b"FORM"):
                continue
            script = E.read_script(blob)
            ins = script.instructions
            at = {item.address: k for k, item in enumerate(ins)}

            def sim(start, stop, caller, depth, budget):
                stack = []
                k = at.get(start + 1)
                if k is None:
                    return
                steps = 0
                while k < len(ins) and budget[0] > 0 and steps < 8000:
                    budget[0] -= 1
                    steps += 1
                    item = ins[k]
                    if stop is not None and item.address >= stop:
                        break
                    op, arg = item.opcode, item.argument
                    if op in (3, 4):
                        stack.append(arg)
                    elif op == 7 and caller is not None:
                        stack.append(caller[-arg] if 0 < arg <= len(caller) else None)
                    elif op in (5, 6, 7) or (op == 2 and arg == 0):
                        stack.append(None)
                    elif op == 2 and arg == 1:
                        nxt = ins[k + 1] if k + 1 < len(ins) else None
                        if nxt is not None and nxt.opcode == 0 and depth < 6:
                            sim(nxt.argument - 1, None, list(stack), depth + 1, budget)
                            k += 2
                            continue
                        stack.clear()
                    elif op == 17 and len(stack) >= 2:
                        a, b = stack.pop(), stack.pop()
                        stack.append(EVAL[arg](b, a) if a is not None and b is not None and arg in EVAL else None)
                    elif op == 16 and stack:
                        value = stack.pop()
                        stack.append(-value if value is not None and arg == 1 else None)
                    elif op == 14:
                        n = ins[k + 1].argument if k + 1 < len(ins) and ins[k + 1].opcode == 12 else 0
                        args = list(reversed(stack[-n:])) if n else []
                        while len(args) < n:
                            args.append(None)
                        key = (name, item.address)
                        if arg == 0x38:
                            modes.setdefault(key, set()).add(args[6] if len(args) > 6 else None)
                        if arg == 0x5B and len(args) > 1 and args[1] == 0:
                            sel0.setdefault(key, set()).add(args[2] if len(args) > 2 else None)
                    elif op == 12:
                        if arg and len(stack) >= arg:
                            del stack[-arg:]
                        elif arg:
                            stack.clear()
                    elif op in (9, 10, 11, 15) or (op == 8 and arg == 0):
                        if stack:
                            stack.pop()
                    elif depth and (op == 18 or (op == 8 and arg == 1)):
                        break
                    else:
                        stack.clear()
                    k += 1

            starts = sorted(script.entries)
            budget = [400000]
            for i, head in enumerate(starts):
                stop = starts[i + 1] if i + 1 < len(starts) else len(script.words)
                sim(head, stop, None, 0, budget)
            for item in ins:
                if item.opcode == 14 and item.argument == 0x38:
                    raw38 += 1
    return raw38, modes, sel0


def finale_facts(data):
    if len(data) != 132328:
        return f"ENG/FINALE.EXE is {len(data)} bytes"
    base = 0x2200 + 0x1ACB * 16
    row = base + 40 * 0x14
    if row != 0x1D1D0:
        return f"row 40 file offset is {row:#x}"
    size = struct.unpack_from("<I", data, row + 4)[0]
    flags = struct.unpack_from("<H", data, row + 0x12)[0]
    if size != 44115 or flags != 0x1000:
        return f"row 40 is size {size} flags {flags:#x}"
    # Name pointer of row 93 is zero; rows 0-92 are occupied.
    end = base + 93 * 0x14
    if data[end:end + 4] != b"\x00\x00\x00\x00":
        return "catalog row 93 is not a zero name pointer"
    if struct.unpack_from("<HH", data, base + 92 * 0x14) == (0, 0):
        return "row 92 has a zero name pointer"
    needle = bytes.fromhex("ba1400f7eabacb1a")
    sites = [i for i in range(len(data) - 8) if data.startswith(needle, i)]
    if sites != [0xCDD1, 0xCE81, 0xCF2F, 0xEA8C, 0xEB29, 0xF0BC, 0xF0DE, 0xF107, 0xF138, 0xF160, 0xF17F, 0xF1B0]:
        return f"catalog index sites are {[hex(s) for s in sites]}"
    # None of the 12 loads the constant 40 in the preceding six bytes.
    for site in sites:
        if b"\xB8\x28\x00" in data[site - 6:site] or b"\x6A\x28" in data[site - 6:site]:
            return f"index site {site:#x} is fed by the constant 40"
    # 0xCE4D indexes the catalog with add ax, 0 before the segment.
    if data[0xCE4D:0xCE5A] != bytes.fromhex("ba1400f7ea050000c746e4cb1a"):
        return "the index site at 0xCE4D is not a stride-20 catalog index"
    # Startup sort, called once at 0xEC3F: skip the rows whose name holds
    # DS:0x123E (".PAK"), count the rest, sort them with width 0x14.
    if data[0xF0B3:0xF0B9] != bytes.fromhex("c70676370000"):
        return "the startup sort does not start its index at 0"
    if data[0xEC3F] != 0xE8 or 0xEC42 + struct.unpack_from("<h", data, 0xEC40)[0] != 0xF0B0:
        return "0xEC3F does not call the startup sort"
    pattern = 0x2200 + 0x1B5B * 16 + 0x123E
    if data[0xF100:0xF103] != b"\xB8\x3E\x12" or data[pattern:pattern + 5] != b".PAK\x00":
        return "the startup sort does not test for .PAK"
    if data[0xF1A5:0xF1A8] != b"\xB8\x14\x00" or data[0xF1BD] != 0x9A:
        return "the startup sort call is not width 0x14"
    # Direct index argument: callers push a register or a computed word, not 40.
    for caller in (0xE85A, 0xE8A7):
        if data[caller] != 0xE8:
            return f"index caller missing at {caller:#x}"
        if b"\x6A\x28" in data[caller - 8:caller] or b"\x68\x28\x00" in data[caller - 8:caller]:
            return f"caller {caller:#x} pushes 40"
    return None


def palette_rows_cd(fdt):
    # FILEDATA.FDT rows 122, 204, 206: size 0x300 at +4, member offset at +0x0C, flags 0x1000 at +0x12.
    expect = {122: (0x988, 0x1B8B5), 204: (0xFF0, 0x1D72C), 206: (0x1018, 0x1DD2C)}
    for index, (at, member) in expect.items():
        size = struct.unpack_from("<I", fdt, at + 4)[0]
        got = struct.unpack_from("<I", fdt, at + 0x0C)[0]
        flags = struct.unpack_from("<H", fdt, at + 0x12)[0]
        if (size, got, flags) != (0x300, member, 0x1000):
            return f"FDT row {index} is size {size:#x} member {got:#x} flags {flags:#x}"
    return None


def palette_rows_floppy(data):
    expect = {227: (0x2E21C, b"CAV_PLT2.PAL"), 229: (0x2E244, b"CAV_PLT4.PAL"), 232: (0x2E280, b"ALTPAL3.PAL")}
    for index, (at, _name) in expect.items():
        size = struct.unpack_from("<I", data, at + 4)[0]
        flags = struct.unpack_from("<H", data, at + 0x12)[0]
        if (size, flags) != (0x300, 0x1000):
            return f"floppy row {index} is size {size:#x} flags {flags:#x}"
    return None


def no_constant_index(data, rows):
    """No mov/push of these row numbers is multiplied by 0x14."""
    for row in rows:
        immediate = struct.pack("<H", row)
        # push imm8 of the low byte is too common (coordinates). Require the
        # word immediate within four bytes before mov dx, 0x14; imul dx.
        start = 0
        while True:
            at = data.find(b"\xBA\x14\x00\xF7\xEA", start)
            if at < 0:
                break
            if immediate in data[at - 6:at]:
                return f"stride-20 site {at:#x} is fed by row {row}"
            start = at + 1
    return None


def byte_ten_stores(data):
    """File offsets of every mov byte [mem], 10 (C6 /0 ib) at any byte offset after the header."""
    hits = []
    for i in range(header_size(data), len(data) - 6):
        if data[i] != 0xC6:
            continue
        modrm = data[i + 1]
        mod, reg, rm = modrm >> 6, (modrm >> 3) & 7, modrm & 7
        if reg or mod == 3:
            continue
        disp = 2 if mod == 2 or (mod == 0 and rm == 6) else mod
        if data[i + 2 + disp] == 10:
            hits.append(i)
    return hits


def byte_ten(data, site, label):
    """The one byte store of 10 in the file writes a party record, not the mode byte."""
    at, entry, base = site
    hits = byte_ten_stores(data)
    if hits != [at + 6]:
        return f"{label} mov byte [mem], 10 at {[hex(h) for h in hits]}, not {at + 6:#x}"
    if data[at:at + len(TEN_STORE)] != TEN_STORE:
        return f"{label} byte store of 10 at {at:#x} differs"
    if data[entry:entry + 3] != b"\x55\x8B\xEC" or data[entry + 8:entry + 18] != base:
        return f"{label} routine {entry:#x} does not load the party record base"
    return None


def blit_steps(data, sites, def20, label):
    """The only add bx, 0x14 encodings are the two picture-segment steps.

    No other add of 20 to bx, si or di is encoded, and every add dx, 0x14
    steps a definition offset just loaded from an instance."""
    if data.count(bytes.fromhex("83c214")) != 3 or data.count(def20) != 3:
        return f"{label} add dx, 0x14 is not the three definition-offset steps"
    if data.count(bytes.fromhex("83c314")) != 4:
        return f"{label} add bx, 0x14 count is not 4"
    for pattern in NO_ADD20:
        if bytes.fromhex(pattern) in data:
            return f"{label} contains {pattern}, an add of 20 to bx, si or di"
    for offset in sites:
        if data[offset:offset + len(BLIT_STEP)] != BLIT_STEP:
            return f"{label} blit step at {offset:#x} differs"
    return None


def check_image(data, expected, array_add, label):
    found, error = mode_stores(data, array_add)
    if error:
        return error
    if set(found) != set(expected):
        return f"{label} mode stores {[hex(a) for a in found]} != {[hex(a) for a in sorted(expected)]}"
    # No store in that set writes the immediate 10 or 11.
    for addr in found:
        if data[addr:addr + 2] == b"\x26\xC6":
            imm = data[addr + 4] if data[addr + 2] == 0x47 else data[addr + 5]
            if imm in (10, 11):
                return f"{label} store {addr:#x} writes {imm}"
    return None


def check_cd(data_dir):
    main = Path(data_dir) / "HARDRIVE" / "MAIN.EXE"
    finale = Path(data_dir) / "ENG" / "FINALE.EXE"
    fdt = Path(data_dir) / "FILEDATA.FDT"
    if not main.is_file():
        return fail("CD MAIN.EXE is not in HARDRIVE")
    image = main.read_bytes()
    if len(image) != 0x57240:
        return fail(f"CD MAIN.EXE is {len(image):#x} bytes")
    error = check_image(image, CD_STORES, 0x15FA, "CD")
    if error:
        return fail(error)
    error = byte_ten(image, CD_TEN, "CD") or blit_steps(image, CD_BLIT, CD_DEF20, "CD")
    if error:
        return fail(error)
    pushed, error = call_immediates(image, CD_CALLS)
    if error:
        return fail(error)
    for addr, expect in CD_CALLS.items():
        if expect is None:
            if pushed[addr] in (10, 11):
                return fail(f"call {addr:#x} pushes {pushed[addr]}")
            continue
        if pushed[addr] != expect:
            return fail(f"call {addr:#x} pushes {pushed[addr]}, not {expect}")
    # File +0x12149 is reached by push 3 or push 4. Neither is 10 or 11.
    if image[0x1213E:0x12144] != b"\x6A\x03\xEB\x02\x6A\x04":
        return fail("the two-immediate setter call is not push 3 or push 4")
    if 10 in pushed.values() or 11 in pushed.values():
        return fail("a setter call pushes 10 or 11")
    raw38, modes, sel0 = script_modes(data_dir)
    if raw38 != 308:
        return fail(f"{raw38} initMonster calls, not 308")
    if len(modes) != 304:
        return fail(f"{len(modes)} reached initMonster calls, not 304")
    values = {v for group in modes.values() for v in group}
    if not values <= {1, 2, 3, 4, 7, 12, None}:
        return fail(f"initMonster modes {sorted(v for v in values if v is not None)}")
    if any(10 in group or 11 in group for group in modes.values()):
        return fail("a script passes mode 10 or 11 to initMonster")
    elevens = [key for key, group in sel0.items() if 11 in group]
    if len(elevens) != 3 or any(name != "LEVEL23.INF" for name, _addr in elevens):
        return fail(f"mode 11 sites {elevens}")
    if any(10 in group for group in sel0.values()):
        return fail("a script passes mode 10 to changeMonsterStat")
    error = finale_facts(finale.read_bytes())
    if error:
        return fail(error)
    error = palette_rows_cd(fdt.read_bytes())
    if error:
        return fail(error)
    error = no_constant_index(image, (122, 204, 206))
    if error:
        return fail(error)
    print("CHECK mode_paths: 10 CD mode-byte stores, none stores 10, the file's one byte store of 10 writes a party record, "
          "add bx, 0x14 only steps blit segments, no resolved caller or script passes 10, "
          "3 LEVEL23 calls pass 11; finale row 40 is one of 93 catalog rows, no index site loads the constant 40, "
          "startup sorts rows 4-92; no stride-20 site loads palette rows 122, 204 or 206 as a constant")
    return 0


def check_floppy(data_dir):
    main = Path(data_dir) / "MAIN.EXE"
    if not main.is_file():
        return fail("floppy MAIN.EXE is not in the folder")
    image = main.read_bytes()
    if len(image) != 0x5B470:
        return fail(f"floppy MAIN.EXE is {len(image):#x} bytes")
    error = check_image(image, FL_STORES, 0x15DC, "floppy")
    if error:
        return fail(error)
    error = byte_ten(image, FL_TEN, "floppy") or blit_steps(image, FL_BLIT, FL_DEF20, "floppy")
    if error:
        return fail(error)
    error = palette_rows_floppy(image)
    if error:
        return fail(error)
    error = no_constant_index(image, (227, 229, 232))
    if error:
        return fail(error)
    raw38, modes, sel0 = script_modes(data_dir)
    if raw38 != 308 or len(modes) != 304:
        return fail(f"floppy scripts {raw38} raw, {len(modes)} reached")
    if any(10 in group or 11 in group for group in modes.values()):
        return fail("floppy initMonster passes 10 or 11")
    if any(10 in group for group in sel0.values()):
        return fail("floppy changeMonsterStat passes 10")
    elevens = [key for key, group in sel0.items() if 11 in group]
    if len(elevens) != 3 or any(name != "LEVEL23.INF" for name, _addr in elevens):
        return fail(f"floppy mode 11 sites {elevens}")
    print("CHECK mode_paths: floppy layout, 8 mode-byte stores, none stores 10, the file's one byte store of 10 writes a party record, "
          "add bx, 0x14 only steps blit segments, no resolved script passes 10, "
          "3 LEVEL23 calls pass 11; no stride-20 site loads palette rows 227, 229 or 232 as a constant")
    return 0


def main():
    parser = ReaderArgumentParser(description=__doc__, formatter_class=argparse_format())
    parser.add_argument("--data", default=L.DEFAULT_DATA, required=L.DEFAULT_DATA is None)
    parser.add_argument("--floppy", help="floppy install folder, checked in addition to --data")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")
    if L.is_cd_layout(args.data):
        rc = check_cd(args.data)
    else:
        rc = check_floppy(args.data)
    if rc:
        return rc
    if args.floppy:
        return check_floppy(args.floppy)
    return 0


def argparse_format():
    import argparse
    return argparse.RawDescriptionHelpFormatter


if __name__ == "__main__":
    raise SystemExit(run_cli(main))
