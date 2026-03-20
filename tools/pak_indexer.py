#!/usr/bin/env python3
"""
LoL1 Investigation Step 1: Build baseline structural inventory.
Phase 1: Local file archaeology
"""

import os
import json
import struct
from pathlib import Path
from collections import defaultdict

GAME_DIR = Path("/media/bob/Arikv/REFERENCE/game_files/lol1")
OUTPUT_DIR = Path("/home/bob")

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

def main():
    print("LoL1 Investigation Step 1: Building structural inventory...")
    
    files_by_ext = scan_all_files()
    
    # Build inventory
    inventory = {}
    for ext, files in sorted(files_by_ext.items(), key=lambda x: -len(x[1])):
        print(f"\nProcessing {ext}: {len(files)} files")
        
        sizes = [f['size'] for f in files]
        sample_files = files[:min(5, len(files))]  # Sample up to 5
        
        ext_entry = {
            'count': len(files),
            'size_range': {'min': min(sizes), 'max': max(sizes)} if sizes else None,
            'total_bytes': sum(sizes),
            'sample_analysis': []
        }
        
        for sf in sample_files:
            analysis = analyze_file_structure(sf['abs_path'], sf['size'])
            ext_entry['sample_analysis'].append({
                'file': sf['path'],
                'analysis': analysis
            })
        
        inventory[ext] = ext_entry
    
    # Write inventory
    output_path = OUTPUT_DIR / 'lol1_inventory_step1.json'
    with open(output_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"\nInventory written to: {output_path}")
    
    # Summary
    print("\n=== SUMMARY ===")
    for ext, data in sorted(inventory.items(), key=lambda x: -x[1]['count']):
        print(f"{ext}: {data['count']} files, {data['total_bytes']:,} bytes")
        for sample in data['sample_analysis'][:2]:
            a = sample['analysis']
            magic = a.get('detected_magic', 'none')
            print(f"  - {sample['file']}: magic={magic}")

if __name__ == '__main__':
    main()
