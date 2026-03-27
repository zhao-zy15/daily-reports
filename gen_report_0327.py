#!/usr/bin/env python3
"""Generate arXiv daily report for 2026-03-27 by concatenating part files."""
import os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
PARTS_DIR = os.path.join(BASE, 'report_parts', '2026-03-27')
OUT = os.path.join(BASE, 'arxiv-papers', 'report-2026-03-27.html')

os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Collect all parts in order
parts = sorted(glob.glob(os.path.join(PARTS_DIR, 'part_*.html')))
if not parts:
    print("No parts found in", PARTS_DIR)
    exit(1)

print(f"Found {len(parts)} parts, writing to {OUT}")
with open(OUT, 'w', encoding='utf-8') as out:
    for p in parts:
        with open(p, 'r', encoding='utf-8') as f:
            out.write(f.read())
        print(f"  Added {os.path.basename(p)}")

sz = os.path.getsize(OUT)
print(f"Done! Output: {OUT} ({sz:,} bytes)")
