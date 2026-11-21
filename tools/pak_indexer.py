#!/usr/bin/env python3
"""Read all LoL1 PAK directories or survey the loose game files.

Rebuilds data/pak_index.json (pak_files: name/offset/header_pos/size per
member; flat_index). header_pos = position of the member's offset field in
the PAK directory. Layout: docs/formats/pak.md.

  pak_indexer.py                       # summary
  pak_indexer.py --out pak_index.json
  pak_indexer.py --check               # compare with data/pak_index.json
  pak_indexer.py --survey --out s.json # the March loose-file survey (every file
                                       # under --game-dir grouped by extension)
"""

from cli_errors import run_cli
import os
import json
import struct
from pathlib import Path
from collections import defaultdict


import lol1lib as L

GAME_DIR = Path(L.DEFAULT_DATA).parent if L.DEFAULT_DATA else None

def scan_all_files():
    """Scan all files in the game directory and group by extension."""
    files_by_ext = defaultdict(list)
    
    for root, dirs, files in os.walk(GAME_DIR):
        for name in files:
            filepath = Path(root) / name
            ext = filepath.suffix.lower() if filepath.suffix else '(no_ext)'
            size = filepath.stat().st_size
            files_by_ext[ext].append({
                'path': str(filepath.relative_to(GAME_DIR)),
                'size': size,
                'abs_path': str(filepath)
            })
    
    return files_by_ext

def read_header(filepath, nbytes=64):
    """Read first nbytes of file as hex."""
    try:
        with open(filepath, 'rb') as f:
            return f.read(nbytes).hex()
    except Exception as e:
        return f"error: {e}"

def detect_magic(data):
    """Detect known magic signatures."""
    magic_map = {
        b'Creative Voice File': 'VOC (Creative Voice)',
        b'DOS/4G': 'DOS/4G executable',
        b'MZ': 'DOS executable (MZ)',
        b'BM': 'BMP image',
    }
    for magic, desc in magic_map.items():
        if data.startswith(magic):
            return desc
    return None

def analyze_file_structure(filepath, size):
    """Basic structural analysis of a file."""
    try:
        with open(filepath, 'rb') as f:
            data = f.read(min(size, 4096))  # Read first 4KB max
        
        if len(data) < 4:
            return {'error': 'file too small'}
        
        result = {
            'size': size,
            'first_16_hex': data[:16].hex(),
            'first_16_ascii': ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[:16]),
            'detected_magic': detect_magic(data),
        }
        
        # Check for repeated patterns (possible offset tables)
        if len(data) >= 64:
            # Try 20-byte stride (FILEDATA.FDT pattern)
            if size >= 100:
                f.seek(0)
                sample = f.read(min(200, size))
                # Check if bytes 4-8 look like offsets (small values)
                vals_20 = []
                for i in range(0, min(len(sample) - 20, 100), 20):
                    val = struct.unpack('<I', sample[i:i+4])[0]
                    vals_20.append(val)
                if all(v < size * 2 for v in vals_20[:5]):
                    result['possible_20byte_stride'] = True
                    result['stride_20_samples'] = vals_20[:5]
        
        return result
    except Exception as e:
        return {'error': str(e)}

def survey(out_path):
    """The March step-1 inventory, kept for reference."""
    files_by_ext = scan_all_files()
    inventory = {}
    for ext, files in sorted(files_by_ext.items()):
        sizes = [f['size'] for f in files]
        inventory[ext] = {
            'count': len(files),
            'size_range': {'min': min(sizes), 'max': max(sizes)} if sizes else None,
            'total_bytes': sum(sizes),
            'sample_analysis': [{'file': sf['path'], 'analysis': analyze_file_structure(sf['abs_path'], sf['size'])}
                                for sf in files[:5]],
        }
    with open(out_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    print('wrote', out_path)


def build_index(data_dir):
    pak_files = {}
    flat = []
    for pak in L.list_paks(data_dir):
        blob = open(os.path.join(data_dir, pak), 'rb').read()
        pak = pak.upper()
        entries = []
        pos = 0
        for name, off, size in L.pak_entries(blob):
            entries.append({'name': name, 'offset': off, 'header_pos': pos, 'size': size})
            flat.append({'pak': pak, 'name': name, 'offset': off, 'size': size})
            pos += 4 + len(name) + 1
        pak_files[pak] = {'size': len(blob), 'entry_count': len(entries), 'entries': entries}
    return {'description': 'Complete file index for all LoL1 PAK containers',
            'total_paks': len(pak_files), 'total_entries': len(flat),
            'pak_files': pak_files, 'flat_index': flat}


def main():
    global GAME_DIR
    ap = L.tool_args(__doc__)
    ap.add_argument('--survey', action='store_true', help='run the loose-file survey instead (needs --out)')
    ap.add_argument('--game-dir', default=None, help='folder for --survey (default: parent of --data)')
    a = ap.parse_args()
    if a.survey:
        GAME_DIR = Path(a.game_dir) if a.game_dir else Path(a.data).parent
        if not a.out:
            ap.error('--survey needs --out')
        survey(a.out)
        return 0
    idx = build_index(a.data)
    if a.check:
        ref = L.repo_json('pak_index.json', a.data)
        key = lambda d: sorted((x['pak'], x['name'], x['offset'], x['size']) for x in d['flat_index'])
        skipped = ref is None
        same = skipped or ref['pak_files'] == idx['pak_files'] and key(ref) == key(idx)
        print(f"CHECK pak_index: {idx['total_paks']} PAKs, {idx['total_entries']} members, "
              f"matches data/pak_index.json: {'skipped (not the CD layout)' if skipped else same}")
        return 0 if same else 1
    print(f"{idx['total_paks']} PAKs, {idx['total_entries']} members")
    if a.out:
        L.write_json(a.out, idx)
    return 0


if __name__ == '__main__':
    raise SystemExit(run_cli(main))
