#!/usr/bin/env python3
"""解析 RSS，过滤 Announce Type: new，输出 unique 论文列表。"""
import re, json, os, sys
from pathlib import Path
import xml.etree.ElementTree as ET

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")

papers = {}
for cat in ["cs.CL", "cs.AI", "cs.LG"]:
    xml = (DATA_DIR / f"rss_{cat}.xml").read_text(encoding="utf-8", errors="replace")
    # Parse via regex (RSS is simple enough; handle CDATA)
    items = re.findall(r"<item>(.*?)</item>", xml, flags=re.S)
    for it in items:
        link_m = re.search(r"<link>(.*?)</link>", it, flags=re.S)
        title_m = re.search(r"<title>(.*?)</title>", it, flags=re.S)
        desc_m = re.search(r"<description>(.*?)</description>", it, flags=re.S)
        if not (link_m and title_m and desc_m):
            continue
        link = link_m.group(1).strip()
        title = title_m.group(1).strip()
        # Strip CDATA
        title = re.sub(r"^<!\[CDATA\[|\]\]>$", "", title)
        desc = desc_m.group(1).strip()
        desc = re.sub(r"^<!\[CDATA\[|\]\]>$", "", desc)
        # Filter Announce Type: new
        m = re.search(r"Announce Type:\s*(\w+)", desc)
        if not m or m.group(1) != "new":
            continue
        # extract arxiv id from link
        idm = re.search(r"arxiv\.org/abs/([\d\.]+)", link)
        if not idm:
            continue
        aid = idm.group(1)
        # abstract
        abs_m = re.search(r"Abstract:\s*(.*)", desc, flags=re.S)
        abstract = abs_m.group(1).strip() if abs_m else ""
        # clean html
        abstract = re.sub(r"<[^>]+>", "", abstract)[:2000]
        if aid not in papers:
            papers[aid] = {
                "id": aid,
                "title": re.sub(r"\s+", " ", title),
                "abstract": abstract,
                "categories": [cat],
                "link": link,
            }
        else:
            if cat not in papers[aid]["categories"]:
                papers[aid]["categories"].append(cat)

out = list(papers.values())
(DATA_DIR / "papers_new.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"Total unique new papers: {len(out)}")
# category counts
from collections import Counter
c = Counter()
for p in out:
    for cat in p["categories"]:
        c[cat] += 1
print("Category coverage:", dict(c))
