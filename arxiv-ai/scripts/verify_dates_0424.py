#!/usr/bin/env python3
"""通过 arXiv API 批量验证日期 + 抓取作者。每次查询最多100篇。"""
import json, time, re
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
papers = json.loads((DATA_DIR / "papers_labeled.json").read_text())
ids = [p["id"] for p in papers]

NS = {"a": "http://www.w3.org/2005/Atom"}

def fetch_batch(batch):
    url = "http://export.arxiv.org/api/query?id_list=" + ",".join(batch) + "&max_results=" + str(len(batch))
    req = urllib.request.Request(url, headers={"User-Agent": "research-bot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")

meta = {}
batch_size = 50
for i in range(0, len(ids), batch_size):
    batch = ids[i:i+batch_size]
    try:
        xml = fetch_batch(batch)
    except Exception as e:
        print(f"Batch {i} failed: {e}; retry once")
        time.sleep(5)
        try:
            xml = fetch_batch(batch)
        except Exception as e2:
            print(f"Batch {i} giving up: {e2}")
            continue
    root = ET.fromstring(xml)
    for entry in root.findall("a:entry", NS):
        idtxt = entry.findtext("a:id", default="", namespaces=NS)
        idm = re.search(r"abs/([\d\.]+)", idtxt)
        if not idm:
            continue
        aid = idm.group(1)
        published = entry.findtext("a:published", default="", namespaces=NS)
        updated = entry.findtext("a:updated", default="", namespaces=NS)
        authors = [a.findtext("a:name", default="", namespaces=NS) for a in entry.findall("a:author", NS)]
        meta[aid] = {"published": published, "updated": updated, "authors": authors}
    print(f"Batch {i}: {len(meta)} so far")
    time.sleep(3)

# enrich papers
for p in papers:
    m = meta.get(p["id"])
    if m:
        p["published"] = m["published"]
        p["updated"] = m["updated"]
        p["authors"] = m["authors"]
(DATA_DIR / "papers_verified.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2))

# Date distribution
from collections import Counter
c = Counter((p.get("published") or "")[:10] for p in papers)
print("Published date distribution:", dict(c.most_common()))
print("Total enriched:", sum(1 for p in papers if p.get("published")))
