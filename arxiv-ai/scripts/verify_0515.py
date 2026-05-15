"""Verify selected papers via arXiv API: check submittedDate and get authors."""
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DATE = "2026-05-15"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")

SELECTED = {
    "llm": ["2605.14192", "2605.14589", "2605.14844", "2605.14071"],
    "rl": ["2605.14366", "2605.14539", "2605.13130"],
    "agent": ["2605.14037", "2605.14477", "2605.13037"],
    "medical": ["2605.15016", "2605.13542"],
    "multimodal": ["2605.14747"],
}

all_ids = []
for sect, ids in SELECTED.items():
    for aid in ids:
        all_ids.append((sect, aid))

ns = {"a": "http://www.w3.org/2005/Atom",
      "arxiv": "http://arxiv.org/schemas/atom"}

results = []
for sect, aid in all_ids:
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    print(f"Fetching {aid}...")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
            break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}")
            time.sleep(8)
    else:
        print(f"  GIVE UP on {aid}")
        continue
    root = ET.fromstring(data)
    entry = root.find("a:entry", ns)
    if entry is None:
        print(f"  no entry for {aid}")
        continue
    title = entry.findtext("a:title", default="", namespaces=ns).strip()
    published = entry.findtext("a:published", default="", namespaces=ns).strip()
    updated = entry.findtext("a:updated", default="", namespaces=ns).strip()
    summary = entry.findtext("a:summary", default="", namespaces=ns).strip()
    authors = [a.findtext("a:name", namespaces=ns) for a in entry.findall("a:author", ns)]
    affs = [a.findtext("arxiv:affiliation", namespaces=ns) for a in entry.findall("a:author", ns)]
    affs = [x for x in affs if x]
    pdf_url = None
    for link in entry.findall("a:link", ns):
        if link.get("title") == "pdf":
            pdf_url = link.get("href")
    print(f"  title: {title[:80]}")
    print(f"  published: {published}")
    print(f"  authors: {authors[:3]}")
    print(f"  affs: {affs[:3]}")
    results.append({
        "section": sect, "id": aid, "title": title, "published": published,
        "updated": updated, "summary": summary, "authors": authors, "affs": affs,
        "pdf_url": pdf_url,
    })
    time.sleep(4)

(DATA_DIR / "verified.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved {len(results)} verified papers to {DATA_DIR / 'verified.json'}")
