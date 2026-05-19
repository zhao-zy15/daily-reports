"""Build curated paper meta for 2026-05-19 report."""
import json
from pathlib import Path

DATA = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-05-19")
verified = {p["id"]: p for p in json.loads((DATA / "verified.json").read_text())}

# Curated metadata: institutions per paper (from PDF first-page reading)
INST = {
    "2605.17757": ["Together AI", "University of Sydney", "UIUC"],
    "2605.16928": ["Nanjing University", "Alibaba Group"],
    "2605.18226": ["Institute of Science Tokyo", "Imperial College London"],
    "2605.17026": ["Penn State University"],
    "2605.18721": ["Stanford University", "University of Oklahoma"],
    "2605.15726": ["KAIST", "DeepAuto.ai"],
    "2605.18374": ["ETH Zürich", "University of Maryland"],
    "2605.16143": ["USTC", "Meituan"],
    "2605.15224": ["HKUST (Guangzhou)", "Nanjing University", "Microsoft Research"],
    "2605.18421": ["BIT", "BUPT", "HKUST"],
    "2605.17101": ["CUHK", "Wuhan University of Technology"],
    "2605.17228": ["Johns Hopkins University"],
    "2605.15777": ["UniPat AI", "Peking University", "HKU"],
}

# Section ordering
ORDER = {
    "llm": ["2605.17757", "2605.16928", "2605.18226", "2605.17026"],
    "rl": ["2605.18721", "2605.15726", "2605.18374"],
    "agent": ["2605.16143", "2605.15224", "2605.18421"],
    "medical": ["2605.17101", "2605.17228"],
    "multimodal": ["2605.15777"],
}

meta = {}
for sect, ids in ORDER.items():
    for aid in ids:
        v = verified[aid]
        meta[aid] = {
            "id": aid,
            "section": sect,
            "title": v["title"],
            "authors": v["authors"][:3],
            "n_authors": len(v["authors"]),
            "published": v["published"][:10],
            "summary": v["summary"],
            "institutions": INST[aid],
        }

(DATA / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2))
print(f"Wrote {len(meta)} papers to meta.json")
for aid, m in meta.items():
    print(f"  [{m['section']}] {aid}: {m['title'][:60]}  |  {m['institutions']}")
