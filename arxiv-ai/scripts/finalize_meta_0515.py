"""Manually finalize institutions and section labels."""
import json
from pathlib import Path

DATE = "2026-05-15"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")

verified = json.loads((DATA_DIR / "verified.json").read_text())

# Manual mapping {id: (institutions, section)}
# Limit to ≤3 institutions
INSTS = {
    # LLM
    "2605.14192": ["Michigan State University", "MIT"],
    "2605.14589": ["Nankai University", "Baidu", "Shanghai Jiao Tong University"],
    "2605.14005": ["Harbin Institute of Technology Shenzhen", "Tsinghua University", "Huawei"],
    "2605.14071": ["George Mason University"],
    # RL
    "2605.14366": ["Minzu University of China", "Ant Group", "Shanghai Jiao Tong University"],
    "2605.14539": ["Chinese Academy of Sciences", "UCAS", "Xiaohongshu"],
    "2605.13130": ["HIT Shenzhen", "HK Baptist University", "City University of Hong Kong"],
    # Agent
    "2605.14037": ["Meta FAIR", "CentraleSupélec"],
    "2605.14477": ["Microsoft Research"],
    "2605.13037": ["USTC", "Meituan", "CASIA"],
    # Medical
    "2605.15016": ["The University of Hong Kong", "UESTC", "The University of Sydney"],
    "2605.13542": ["Technical University of Munich", "LMU Munich", "Imperial College London"],
    # Multimodal
    "2605.14747": ["Peking University", "Xiaomi LLM-Core", "Renmin University of China"],
}

for p in verified:
    aid = p["id"]
    if aid in INSTS:
        p["institutions"] = INSTS[aid]
    else:
        p["institutions"] = []

(DATA_DIR / "verified.json").write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding="utf-8")

print("Section breakdown:")
from collections import defaultdict
by_sect = defaultdict(list)
for p in verified:
    by_sect[p["section"]].append(p)
for sect in ["llm", "rl", "agent", "medical", "multimodal"]:
    print(f"\n{sect.upper()}:")
    for p in by_sect[sect]:
        print(f"  {p['id']}: {p['title'][:70]}")
        print(f"    Inst: {p['institutions']}")
        print(f"    Pub: {p['published']}")
