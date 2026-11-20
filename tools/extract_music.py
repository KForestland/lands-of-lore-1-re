#!/usr/bin/env python3
"""Catalogue (and optionally extract) every LoL1 music file: XMI, C55, ADL, PCS.

XMI, C55 and PCS are IFF (FORM XDIR + CAT XMID) containers; ADL has no IFF
header. See docs/formats/music.md. No conversion to MIDI is done here.

  extract_music.py                         # summary
  extract_music.py --out inventory.json    # same shape as data/music_inventory.json
  extract_music.py --out-dir music/        # also write the raw files
  extract_music.py --check                 # files, sizes and IFF trees vs data/music_inventory.json
"""

from cli_errors import run_cli
import json
import struct
import os

import lol1lib as L

MUSIC_EXTS = ('.XMI', '.C55', '.ADL', '.PCS')


def read_be_u32(data, off):
    return struct.unpack('>I', data[off:off+4])[0]

def read_le_u32(data, off):
    return struct.unpack('<I', data[off:off+4])[0]

def tag(data, off):
    return data[off:off+4].decode('ascii', errors='replace')

def parse_iff_chunks(data):
    """Parse IFF FORM/XDIR/XMID container structure.
    Returns list of chunks found with their positions and sizes."""
    chunks = []
    pos = 0
    length = len(data)

    def parse_at(pos, depth=0):
        if pos + 8 > length:
            return pos
        chunk_tag = tag(data, pos)
        chunk_size = read_be_u32(data, pos + 4)

        if chunk_tag == 'FORM':
            # FORM has a sub-type tag
            if pos + 12 > length:
                return pos + 8
            form_type = tag(data, pos + 8)
            chunk_info = {
                'tag': 'FORM',
                'form_type': form_type,
                'offset': pos,
                'size': chunk_size,
                'children': []
            }
            chunks.append(chunk_info)
            # Parse children inside the FORM
            child_pos = pos + 12
            end_pos = pos + 8 + chunk_size
            while child_pos < end_pos and child_pos + 8 <= length:
                child_tag = tag(data, child_pos)
                child_size = read_be_u32(data, child_pos + 4)
                if child_tag == 'FORM':
                    old_len = len(chunks)
                    parse_at(child_pos, depth + 1)
                    if len(chunks) > old_len:
                        chunk_info['children'].append(chunks.pop())
                    child_pos = child_pos + 8 + child_size
                elif child_tag == 'CAT ':
                    # CAT container
                    cat_info = {
                        'tag': 'CAT',
                        'offset': child_pos,
                        'size': child_size,
                        'children': []
                    }
                    chunk_info['children'].append(cat_info)
                    # Parse inside CAT
                    cat_type = tag(data, child_pos + 8) if child_pos + 12 <= length else '????'
                    cat_info['cat_type'] = cat_type
                    inner_pos = child_pos + 12
                    cat_end = child_pos + 8 + child_size
                    while inner_pos < cat_end and inner_pos + 8 <= length:
                        inner_tag = tag(data, inner_pos)
                        inner_size = read_be_u32(data, inner_pos + 4)
                        if inner_tag == 'FORM':
                            old_len2 = len(chunks)
                            parse_at(inner_pos, depth + 2)
                            if len(chunks) > old_len2:
                                cat_info['children'].append(chunks[-1])
                        else:
                            leaf = {
                                'tag': inner_tag,
                                'offset': inner_pos,
                                'data_offset': inner_pos + 8,
                                'size': inner_size,
                            }
                            cat_info['children'].append(leaf)
                        inner_pos = inner_pos + 8 + inner_size
                        # IFF chunks are word-aligned
                        if inner_pos % 2 != 0:
                            inner_pos += 1
                    child_pos = cat_end
                else:
                    leaf = {
                        'tag': child_tag,
                        'offset': child_pos,
                        'data_offset': child_pos + 8,
                        'size': child_size,
                    }
                    chunk_info['children'].append(leaf)
                    child_pos = child_pos + 8 + child_size
                # Word-align
                if child_pos % 2 != 0:
                    child_pos += 1
            return pos + 8 + chunk_size
        elif chunk_tag == 'CAT ':
            # Top-level CAT container
            cat_type = tag(data, pos + 8) if pos + 12 <= length else '????'
            cat_info = {
                'tag': 'CAT',
                'cat_type': cat_type,
                'offset': pos,
                'size': chunk_size,
                'children': []
            }
            chunks.append(cat_info)
            inner_pos = pos + 12
            cat_end = pos + 8 + chunk_size
            while inner_pos < cat_end and inner_pos + 8 <= length:
                inner_tag = tag(data, inner_pos)
                inner_size = read_be_u32(data, inner_pos + 4)
                if inner_tag == 'FORM':
                    old_len2 = len(chunks)
                    parse_at(inner_pos, depth + 1)
                    if len(chunks) > old_len2:
                        cat_info['children'].append(chunks.pop())
                else:
                    leaf = {
                        'tag': inner_tag,
                        'offset': inner_pos,
                        'data_offset': inner_pos + 8,
                        'size': inner_size,
                    }
                    cat_info['children'].append(leaf)
                inner_pos = inner_pos + 8 + inner_size
                if inner_pos % 2 != 0:
                    inner_pos += 1
            return pos + 8 + chunk_size
        else:
            chunk_info = {
                'tag': chunk_tag,
                'offset': pos,
                'data_offset': pos + 8,
                'size': chunk_size,
            }
            chunks.append(chunk_info)
            return pos + 8 + chunk_size

    pos = 0
    while pos < length:
        old_pos = pos
        pos = parse_at(pos)
        if pos <= old_pos:
            break
        # Word-align between top-level chunks
        if pos % 2 != 0:
            pos += 1
    return chunks


def chunk_tree_to_dict(chunk):
    """Convert chunk tree to JSON-serialisable dict."""
    result = {'tag': chunk.get('tag', '?')}
    if 'form_type' in chunk:
        result['form_type'] = chunk['form_type']
    if 'cat_type' in chunk:
        result['cat_type'] = chunk['cat_type']
    result['offset'] = chunk.get('offset', 0)
    result['size'] = chunk.get('size', 0)
    if 'data_offset' in chunk:
        result['data_offset'] = chunk['data_offset']
    if 'children' in chunk:
        result['children'] = [chunk_tree_to_dict(c) for c in chunk['children']]
    return result


def analyse_adl(data):
    """ADL files are raw Westwood AdLib music — no IFF header.
    Try to identify structure from first few bytes."""
    info = {
        'format': 'ADL',
        'raw_size': len(data),
        'header_bytes': data[:16].hex(),
    }
    # ADL files typically start with instrument data
    # First 2 bytes might be number of tracks or a version marker
    if len(data) >= 2:
        info['first_word'] = struct.unpack('<H', data[:2])[0]
    return info


def build(data_dir, out_dir=None):
    inventory = []
    for pak in L.list_paks(data_dir):
        blob = open(os.path.join(data_dir, pak), 'rb').read()
        for name, off, size in L.pak_entries(blob):
            if not name.upper().endswith(MUSIC_EXTS):
                continue
            raw = blob[off:off + size]
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                with open(os.path.join(out_dir, name), 'wb') as f:
                    f.write(raw)
            ext = name.rsplit('.', 1)[1].upper()
            info = {'filename': name, 'source_pak': pak.upper(), 'format': ext, 'size': size, 'pak_offset': off}
            if ext == 'ADL':
                info['adl_info'] = analyse_adl(raw)
            else:
                try:
                    chunks = parse_iff_chunks(raw)
                    if chunks:
                        info['iff_structure'] = [chunk_tree_to_dict(c) for c in chunks]
                        top = chunks[0]
                        info['container'] = top.get('form_type', top.get('tag', '?'))
                    else:
                        info['iff_structure'] = []
                        info['parse_note'] = 'no IFF chunks found'
                except Exception as ex:
                    info['parse_error'] = str(ex)
            inventory.append(info)
    inventory.sort(key=lambda e: (e['source_pak'], e['filename']))
    counts = {}
    for item in inventory:
        counts[item['format']] = counts.get(item['format'], 0) + 1
    return {'description': 'LoL1 music file inventory', 'total_files': len(inventory),
            'counts_by_format': counts, 'files': inventory}


def main():
    ap = L.tool_args(__doc__)
    ap.add_argument('--out-dir', help='also write the raw music files here')
    a = ap.parse_args()
    inv = build(a.data, a.out_dir)
    if a.check:
        ref = L.repo_json('music_inventory.json', a.data)
        skipped = ref is None
        same = skipped or sorted(ref['files'], key=lambda e: (e['source_pak'], e['filename'])) == inv['files']
        errors = [f['filename'] for f in inv['files'] if 'parse_error' in f or f.get('parse_note')]
        print(f"CHECK music: {inv['total_files']} files {inv['counts_by_format']}, IFF parse errors: {errors or 'none'}, "
              f"matches data/music_inventory.json files list: {'skipped (not the CD layout)' if skipped else same}")
        return 0 if same and not errors else 1
    print(f"{inv['total_files']} files {inv['counts_by_format']}")
    if a.out:
        L.write_json(a.out, inv)
    return 0


if __name__ == '__main__':
    raise SystemExit(run_cli(main))
