#!/usr/bin/env python3
"""重试未enriched的论文。"""
import json, time, re
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
papers = json.loads((DATA_DIR / "papers_verified.json").read_text())
missing = [p for p in papers if not p.get("published")]
print(f"Missing: {len(missing)}")
ids = [p["id"] for p in missing]

NS = {"a": "http://www.w3.org/2005/Atom"}

def fetch_batch(batch):
    url = "http://export.arxiv.org/api/query?id_list=" + ",".join(batch) + "&max_results=" + str(len(batch))
    req = urllib.request.Request(url, headers={"User-Agent": "research-bot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")

meta = {}
for i in range(0, len(ids), 25):
    batch = ids[i:i+25]
    ok = False
    for attempt in range(4):
        try:
            time.sleep(5 + attempt*5)
            xml = fetch_batch(batch)
            ok = True
            break
        except Exception as e:
            print(f"attempt {attempt} batch {i}: {e}")
    if not ok:
        continue
    root = ET.fromstring(xml)
    for entry in root.findall("a:entry", NS):
        idtxt = entry.findtext("a:id", default="", namespaces=NS)
        idm = re.search(r"abs/([\d\.]+)", idtxt)
        if not idm: continue
        aid = idm.group(1)
        published = entry.findtext("a:published", default="", namespaces=NS)
        updated = entry.findtext("a:updated", default="", namespaces=NS)
        authors = [a.findtext("a:name", default="", namespaces=NS) for a in entry.findall("a:author", NS)]
        meta[aid] = {"published": published, "updated": updated, "authors": authors}
    print(f"Batch {i}: got {len(meta)} total")

for p in papers:
    if not p.get("published"):
        m = meta.get(p["id"])
        if m:
            p["published"] = m["published"]
            p["updated"] = m["updated"]
            p["authors"] = m["authors"]
(DATA_DIR / "papers_verified.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2))

from collections import Counter
c = Counter((p.get("published") or "MISSING")[:10] for p in papers)
print("Updated distribution:", dict(c.most_common()))
