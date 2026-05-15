"""Extract full text from all PDFs (NO truncation)."""
import json
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], check=True)
    from pypdf import PdfReader

DATE = "2026-05-15"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
PDF_DIR = DATA_DIR / "pdfs"
TXT_DIR = DATA_DIR / "fulltext"
TXT_DIR.mkdir(exist_ok=True)

for pdf in sorted(PDF_DIR.glob("*.pdf")):
    aid = pdf.stem
    out = TXT_DIR / f"{aid}.txt"
    if out.exists() and out.stat().st_size > 0:
        print(f"  skip {aid}")
        continue
    print(f"Extracting {aid}...")
    try:
        reader = PdfReader(str(pdf))
        text_parts = []
        for i, page in enumerate(reader.pages):
            try:
                t = page.extract_text() or ""
            except Exception as e:
                print(f"  page {i} error: {e}")
                t = ""
            text_parts.append(t)
        full = "\n\n".join(text_parts)
        out.write_text(full, encoding="utf-8", errors="replace")
        print(f"  pages: {len(reader.pages)}, chars: {len(full)}")
    except Exception as e:
        print(f"  ERROR: {e}")

# Summary
for f in sorted(TXT_DIR.glob("*.txt")):
    print(f"  {f.name}: {f.stat().st_size} bytes")
