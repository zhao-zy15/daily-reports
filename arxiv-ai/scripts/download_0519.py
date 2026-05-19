"""Download PDFs and HTML5 fulltext for selected papers."""
import json, time, urllib.request
from pathlib import Path

DATE = "2026-05-19"
DATA = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
PDF_DIR = DATA / "pdfs"
HTML_DIR = DATA / "html"
PDF_DIR.mkdir(exist_ok=True)
HTML_DIR.mkdir(exist_ok=True)

papers = json.loads((DATA / "verified.json").read_text())

for p in papers:
    aid = p["id"]
    pdf_path = PDF_DIR / f"{aid}.pdf"
    html_path = HTML_DIR / f"{aid}.html"

    if not pdf_path.exists():
        url = p["pdf_url"] or f"http://arxiv.org/pdf/{aid}"
        print(f"PDF {aid}: {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read()
            pdf_path.write_bytes(data)
            print(f"  saved {len(data)//1024} KB")
        except Exception as e:
            print(f"  FAIL: {e}")
        time.sleep(3)
    else:
        print(f"PDF {aid}: cached")

    if not html_path.exists():
        url = f"https://arxiv.org/html/{aid}v1"
        print(f"HTML {aid}: {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")
            html_path.write_text(data, encoding="utf-8")
            print(f"  saved {len(data)//1024} KB")
        except Exception as e:
            print(f"  FAIL: {e}")
        time.sleep(3)
    else:
        print(f"HTML {aid}: cached")
