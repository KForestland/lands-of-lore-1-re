#!/usr/bin/env python3
"""Extract and catalogue all music files from LoL1 PAK archives."""

import json
import struct
import os

PAK_DIR = "/media/bob/Arikv/REFERENCE/game_files/lol1/DATA"
OUT_DIR = "/home/bob/lol1_music"
INDEX_PATH = "/home/bob/lol1_pak_index.json"
INVENTORY_PATH = "/home/bob/lol1_music_inventory.json"

MUSIC_EXTS = ('.XMI', '.C55', '.ADL', '.PCS')

os.makedirs(OUT_DIR, exist_ok=True)

with open(INDEX_PATH) as f:
    pak_index = json.load(f)

# Collect all music entries
music_entries = []
for pak_name, pak_info in pak_index['pak_files'].items():
    for entry in pak_info['entries']:
        if any(entry['name'].upper().endswith(ext) for ext in MUSIC_EXTS):
            music_entries.append({
                'pak': pak_name,
                'name': entry['name'],
                'offset': entry['offset'],
                'size': entry['size'],
            })

print(f"Found {len(music_entries)} music entries across PAK files")

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


# Extract and analyse
inventory = []
pak_cache = {}

for me in sorted(music_entries, key=lambda e: (e['pak'], e['name'])):
    pak_path = os.path.join(PAK_DIR, me['pak'])

    # Cache PAK reads
    if me['pak'] not in pak_cache:
        with open(pak_path, 'rb') as f:
            pak_cache[me['pak']] = f.read()
    pak_data = pak_cache[me['pak']]

    # Extract raw data
    raw = pak_data[me['offset']:me['offset'] + me['size']]
    assert len(raw) == me['size'], f"Short read for {me['name']}: got {len(raw)}, expected {me['size']}"

    # Save to output directory
    out_path = os.path.join(OUT_DIR, me['name'])
    with open(out_path, 'wb') as f:
        f.write(raw)

    ext = me['name'].rsplit('.', 1)[1].upper()

    entry_info = {
        'filename': me['name'],
        'source_pak': me['pak'],
        'format': ext,
        'size': me['size'],
        'pak_offset': me['offset'],
    }

    if ext == 'ADL':
        adl_info = analyse_adl(raw)
        entry_info['adl_info'] = adl_info
    else:
        # XMI, C55, PCS — all IFF-based
        try:
            chunks = parse_iff_chunks(raw)
            if chunks:
                entry_info['iff_structure'] = [chunk_tree_to_dict(c) for c in chunks]
                # Summarise top-level
                top = chunks[0]
                entry_info['container'] = top.get('form_type', top.get('tag', '?'))
            else:
                entry_info['iff_structure'] = []
                entry_info['parse_note'] = 'no IFF chunks found'
        except Exception as ex:
            entry_info['parse_error'] = str(ex)

    inventory.append(entry_info)
    print(f"  Extracted: {me['name']:20s}  {me['size']:8d} bytes  [{ext}]")

# Write inventory
with open(INVENTORY_PATH, 'w') as f:
    json.dump({
        'description': 'LoL1 music file inventory',
        'source': PAK_DIR,
        'output_dir': OUT_DIR,
        'total_files': len(inventory),
        'counts_by_format': {},
        'files': inventory,
    }, f, indent=2)

# Update counts
with open(INVENTORY_PATH) as f:
    inv = json.load(f)
counts = {}
for item in inv['files']:
    fmt = item['format']
    counts[fmt] = counts.get(fmt, 0) + 1
inv['counts_by_format'] = counts
with open(INVENTORY_PATH, 'w') as f:
    json.dump(inv, f, indent=2)

print(f"\nDone. {len(inventory)} files extracted to {OUT_DIR}")
print("Counts by format:")
for fmt, count in sorted(counts.items()):
    print(f"  {fmt}: {count}")
