#!/usr/bin/env python3
"""Override 几篇机构（基于人工PDF首页阅读）。"""
import json
from pathlib import Path
DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
sel = json.loads((DATA_DIR / "final_ready.json").read_text())
# Override — accurate from PDF first-page reading
overrides = {
    "2604.20090": ["HIT", "SJTU"],  # no Alibaba/DeepSeek (those were refs)
}
for p in sel:
    if p["id"] in overrides:
        p["institutions"] = overrides[p["id"]]

for p in sel:
    print(f"  {p['id']}: {p['institutions']}")
(DATA_DIR / "final_ready.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2))
