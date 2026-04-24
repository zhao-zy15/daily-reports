#!/usr/bin/env python3
"""基于标题/摘要，打分每篇论文的"报告价值"并按板块挑出初步候选。
后续再做白名单扫描以确保白名单论文必被选。"""
import json, re
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
papers = json.loads((DATA_DIR / "papers_verified.json").read_text())

# Only keep recent (04-20 or later)
recent = [p for p in papers if (p.get("published") or "")[:10] >= "2026-04-20"]
print(f"Recent papers (>=04-20): {len(recent)}")

# Scoring heuristics — prefer strong novelty signals & experimental substance
HIGH_SIGNAL = ["we propose", "we introduce", "novel", "benchmark", "state-of-the-art", "sota",
               "significantly outperform", "new framework", "first", "we show", "we prove",
               "we find", "achieves", "surpass", "superior"]
METHOD_SIGNAL = ["algorithm", "objective", "loss function", "framework", "method", "approach",
                 "theorem", "theoretical", "proof", "analysis"]
EXP_SIGNAL = ["experiments", "empirical", "benchmark", "evaluation", "ablation", "compared",
              "accuracy", "% improvement"]

def value_score(p):
    t = (p["title"] + " " + p["abstract"]).lower()
    s = 0
    s += sum(1 for k in HIGH_SIGNAL if k in t) * 2
    s += sum(1 for k in METHOD_SIGNAL if k in t)
    s += sum(1 for k in EXP_SIGNAL if k in t) * 1.5
    # Boost for strong numbers
    if re.search(r"\b\d{1,2}\.\d\s*%", t) or re.search(r"\b\d{1,2}\s*%", t):
        s += 2
    if "ablation" in t:
        s += 2
    # Penalize survey/review only
    if "survey" in (p["title"].lower()) or "review" in (p["title"].lower()):
        s -= 5
    # prefer papers with longer abstracts (richer content)
    s += min(len(p["abstract"])/400, 4)
    return s

for p in recent:
    p["value"] = round(value_score(p), 2)

by_section = defaultdict(list)
for p in recent:
    by_section[p["section_guess"]].append(p)
for sec in by_section:
    by_section[sec].sort(key=lambda p: -p["value"])

# Print top 10 per section for candidate selection
for sec, items in by_section.items():
    print(f"\n=== {sec} ({len(items)}) ===")
    for p in items[:15]:
        print(f"  [{p['value']:5.1f}] {p['id']} | {p['title'][:100]}")

# Save top 25 per section
candidates = {sec: items[:25] for sec, items in by_section.items()}
(DATA_DIR / "candidates_raw.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2))
