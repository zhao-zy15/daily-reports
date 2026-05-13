"""Verify selected papers via arxiv API and download metadata."""
import json
import urllib.request
import xml.etree.ElementTree as ET
import time
from pathlib import Path

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")

SELECTED = {
    "llm": ["2605.11478", "2605.11744", "2605.12466", "2605.11262"],
    "rl": ["2605.11461", "2605.12227", "2605.11403", "2605.11467"],
    "agent": ["2605.11169", "2605.11556"],
    "medical": ["2605.12361", "2605.11814"],
    "multimodal": ["2605.11629"],
}

all_ids = [aid for ids in SELECTED.values() for aid in ids]
print(f"Verifying {len(all_ids)} papers via arxiv API")

ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
results = {}

for aid in all_ids:
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    except Exception as e:
        print(f"  {aid}: ERROR {e}")
        continue
    root = ET.fromstring(data)
    entry = root.find("atom:entry", ns)
    if entry is None:
        print(f"  {aid}: no entry")
        continue
    title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
    summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
    published = entry.findtext("atom:published", default="", namespaces=ns)
    updated = entry.findtext("atom:updated", default="", namespaces=ns)
    authors = []
    for a in entry.findall("atom:author", ns):
        name = a.findtext("atom:name", default="", namespaces=ns)
        if name:
            authors.append(name)
    primary = entry.find("arxiv:primary_category", ns)
    primary_cat = primary.get("term") if primary is not None else ""
    results[aid] = {
        "id": aid,
        "title": title,
        "abstract": summary,
        "published": published,
        "updated": updated,
        "authors": authors,
        "primary_category": primary_cat,
    }
    print(f"  {aid}: {published[:10]}, {len(authors)} authors")
    time.sleep(0.7)

(DATA_DIR / "verified.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved verified to {DATA_DIR / 'verified.json'}")
print(f"Total verified: {len(results)}")
