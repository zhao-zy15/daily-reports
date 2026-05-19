"""Retry failed paper verifications with longer cool-down."""
import json, time, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

DATE = "2026-05-19"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
existing = json.loads((DATA_DIR / "verified.json").read_text())
done_ids = {p["id"] for p in existing}
SELECTED = json.load(open(DATA_DIR / "selected.json"))
candidates = json.load(open(DATA_DIR / "candidates.json"))

# Build candidate lookup
cand_lookup = {}
for sect, ps in candidates.items():
    for p in ps:
        cand_lookup[p["id"]] = (sect, p)

missing = []
for sect, ids in SELECTED.items():
    for aid in ids:
        if aid not in done_ids:
            missing.append((sect, aid))
print(f"Missing {len(missing)}: {[m[1] for m in missing]}")

ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

print("Sleeping 60s before retry...")
time.sleep(60)

results = list(existing)
for sect, aid in missing:
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    print(f"Fetching {aid}...")
    success = False
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=40).read().decode("utf-8")
            success = True
            break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}")
            time.sleep(20 + attempt * 10)
    if not success:
        print(f"  GIVE UP {aid}")
        continue
    root = ET.fromstring(data)
    entry = root.find("a:entry", ns)
    if entry is None:
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
    print(f"  OK: {title[:80]}  ({published[:10]})")
    results.append({
        "section": sect, "id": aid, "title": title, "published": published,
        "updated": updated, "summary": summary, "authors": authors, "affs": affs,
        "pdf_url": pdf_url,
    })
    time.sleep(15)

(DATA_DIR / "verified.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(f"\nNow have {len(results)} verified papers")
