"""Fetch arXiv RSS feeds for cs.CL, cs.AI, cs.LG and filter Announce Type: new."""
import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path

DATE = "2026-05-20"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
DATA_DIR.mkdir(parents=True, exist_ok=True)

categories = ["cs.CL", "cs.AI", "cs.LG"]
papers_by_id = {}

for cat in categories:
    url = f"http://rss.arxiv.org/rss/{cat}"
    print(f"Fetching {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    except Exception as e:
        print(f"  ERROR: {e}")
        continue
    (DATA_DIR / f"rss_{cat}.xml").write_text(data, encoding="utf-8")
    root = ET.fromstring(data)
    items = root.findall(".//item")
    print(f"  Total items: {len(items)}")
    new_cnt = 0
    for it in items:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = (it.findtext("description") or "").strip()
        m = re.search(r"Announce Type:\s*(\w+)", desc, re.I)
        atype = m.group(1).lower() if m else "unknown"
        if atype != "new":
            continue
        idm = re.search(r"(\d{4}\.\d{4,5})", link)
        if not idm:
            continue
        aid = idm.group(1)
        abstract = re.sub(r"^.*?Announce Type:\s*\w+\s*", "", desc, flags=re.S).strip()
        abstract = re.sub(r"<[^>]+>", " ", abstract)
        abstract = re.sub(r"\s+", " ", abstract).strip()
        ns = {"dc": "http://purl.org/dc/elements/1.1/"}
        creator_el = it.find("dc:creator", ns)
        creator = (creator_el.text or "").strip() if creator_el is not None else ""
        if aid not in papers_by_id:
            papers_by_id[aid] = {
                "id": aid, "title": title, "abstract": abstract,
                "link": link, "categories": [cat], "authors": creator,
            }
            new_cnt += 1
        else:
            if cat not in papers_by_id[aid]["categories"]:
                papers_by_id[aid]["categories"].append(cat)
    print(f"  New papers (Announce Type: new): {new_cnt}")

papers = list(papers_by_id.values())
print(f"\nTotal unique NEW papers: {len(papers)}")
out = DATA_DIR / "papers_new.json"
out.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved to {out}")
