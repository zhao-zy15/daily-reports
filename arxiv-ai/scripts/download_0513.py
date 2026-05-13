"""Download HTML5 full-text + abs page for the 13 selected papers."""
import urllib.request
import json
import time
from pathlib import Path

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
FULL_DIR = DATA_DIR / "fulltext"
ABS_DIR = DATA_DIR / "abs"
FULL_DIR.mkdir(parents=True, exist_ok=True)
ABS_DIR.mkdir(parents=True, exist_ok=True)

SELECTED = [
    ("llm", "2605.11478"),
    ("llm", "2605.11744"),
    ("llm", "2605.12466"),
    ("llm", "2605.11262"),
    ("rl",  "2605.11461"),
    ("rl",  "2605.12227"),
    ("rl",  "2605.11403"),
    ("rl",  "2605.11467"),
    ("agent","2605.11169"),
    ("agent","2605.11556"),
    ("medical","2605.12361"),
    ("medical","2605.11814"),
    ("multimodal","2605.11629"),
]

(DATA_DIR / "selected.json").write_text(json.dumps(SELECTED, ensure_ascii=False, indent=2), encoding="utf-8")

UA = {"User-Agent": "Mozilla/5.0 (compatible; arxiv-fetcher)"}

for sec, aid in SELECTED:
    html_path = FULL_DIR / f"{aid}.html"
    if not html_path.exists():
        try:
            url = f"https://arxiv.org/html/{aid}v1"
            req = urllib.request.Request(url, headers=UA)
            r = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")
            html_path.write_text(r, encoding="utf-8")
            print(f"  HTML  {aid} ({len(r):,} chars)")
        except Exception as e:
            print(f"  HTML  {aid} FAIL: {e}")
        time.sleep(1.0)
    abs_path = ABS_DIR / f"{aid}.html"
    if not abs_path.exists():
        try:
            url = f"https://arxiv.org/abs/{aid}"
            req = urllib.request.Request(url, headers=UA)
            r = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", errors="ignore")
            abs_path.write_text(r, encoding="utf-8")
            print(f"  ABS   {aid}")
        except Exception as e:
            print(f"  ABS   {aid} FAIL: {e}")
        time.sleep(1.0)

print("Done.")
