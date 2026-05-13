"""Retry failed verifications with longer delay."""
import json, urllib.request, xml.etree.ElementTree as ET, time
from pathlib import Path

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
results = json.loads((DATA_DIR / "verified.json").read_text(encoding="utf-8"))

ALL = ["2605.11478","2605.11744","2605.12466","2605.11262","2605.11461","2605.12227","2605.11403","2605.11467","2605.11169","2605.11556","2605.12361","2605.11814","2605.11629"]
missing = [a for a in ALL if a not in results]
print(f"Retrying {len(missing)} missing: {missing}")

ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

for aid in missing:
    time.sleep(5)
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
            break
        except Exception as e:
            print(f"  {aid} attempt {attempt+1}: {e}")
            time.sleep(10)
    else:
        continue
    root = ET.fromstring(data)
    entry = root.find("atom:entry", ns)
    if entry is None:
        continue
    title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
    summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
    published = entry.findtext("atom:published", default="", namespaces=ns)
    updated = entry.findtext("atom:updated", default="", namespaces=ns)
    authors = [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)]
    primary = entry.find("arxiv:primary_category", ns)
    primary_cat = primary.get("term") if primary is not None else ""
    results[aid] = {
        "id": aid, "title": title, "abstract": summary, "published": published,
        "updated": updated, "authors": authors, "primary_category": primary_cat,
    }
    print(f"  {aid}: {published[:10]}, {len(authors)} authors, OK")

(DATA_DIR / "verified.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nTotal verified: {len(results)}")
