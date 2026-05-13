"""Concatenate parts to a single report."""
from pathlib import Path

DATE = "2026-05-13"
PARTS_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/parts/{DATE}")
OUT = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/reports/report-{DATE}.html")
OUT.parent.mkdir(parents=True, exist_ok=True)

parts = sorted(PARTS_DIR.glob("part*.html"))
print(f"Concatenating {len(parts)} parts:")
content = []
for p in parts:
    print(f"  {p.name}")
    content.append(p.read_text(encoding="utf-8"))

OUT.write_text("\n".join(content), encoding="utf-8")
print(f"\nWrote {OUT} ({OUT.stat().st_size:,} bytes)")
