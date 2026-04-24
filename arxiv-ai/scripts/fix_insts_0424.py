#!/usr/bin/env python3
"""手动补全机构信息（基于上面PDF首页文本观察）。"""
import json
from pathlib import Path

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
sel = json.loads((DATA_DIR / "final_with_insts.json").read_text())

# Manual supplements based on PDF reading
manual = {
    "2604.20564": ["University of Florida"],
    "2604.20487": ["Zhejiang Angel Medical AI", "Miti AI"],
    "2604.19859": ["Ant Group"],  # Venus Team
    "2604.20148": ["LexisNexis"],
    # For 2604.20090 remove DeepSeek if it's just cited - check PDF more carefully
}

for p in sel:
    aid = p["id"]
    if aid in manual:
        # Use manual entries (replace, but dedupe-merge with existing)
        existing = p.get("institutions", []) or []
        merged = list(dict.fromkeys(manual[aid] + existing))
        p["institutions"] = merged

# Check 2604.20090 (DeepSeek shown — verify)
# Print
for p in sel:
    print(f"  {p['id']}: {p['institutions']}")

(DATA_DIR / "final_ready.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2))
