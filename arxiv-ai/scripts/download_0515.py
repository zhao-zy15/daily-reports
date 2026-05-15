"""Download PDFs for all 13 verified papers."""
import json
import time
import urllib.request
from pathlib import Path

DATE = "2026-05-15"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
PDF_DIR = DATA_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

verified = json.loads((DATA_DIR / "verified.json").read_text())
print(f"Downloading {len(verified)} PDFs")

for p in verified:
    aid = p["id"]
    out = PDF_DIR / f"{aid}.pdf"
    if out.exists():
        print(f"  skip {aid} (exists)")
        continue
    url = f"https://arxiv.org/pdf/{aid}"
    print(f"  fetching {aid}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        out.write_bytes(data)
        print(f"    {len(data)} bytes")
    except Exception as e:
        print(f"    ERROR: {e}")
    time.sleep(3)

print("\nFiles:")
for f in sorted(PDF_DIR.iterdir()):
    print(f"  {f.name}: {f.stat().st_size} bytes")
