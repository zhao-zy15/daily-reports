#!/usr/bin/env python3
"""基于摘要、白名单、主题多样性，最终精选 12-14 篇论文。"""
import json
from pathlib import Path

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
cands = json.loads((DATA_DIR / "candidates_refined.json").read_text())
whitelist = json.loads((DATA_DIR / "whitelist_hits.json").read_text())
wl_ids = {w["id"]: w for w in whitelist}

# Manual selection based on title/abstract reading:
# LLM section (5): pure-text, well-motivated, diverse subtopics
# RL section (3-4): verifiable process supervision, hierarchical, deep research agent, preference
# Agent section (3): Self-improving multi-agent (Alibaba whitelist!), Coding agent user pressure, Meta-Tool
# Medical (1-2): MedSkillAudit
# Multimodal (2): V-tableR1, Where and What (or WebGen-R1)

selection_ids = {
    "LLM": [
        "2604.20564",  # Where Reasoning Breaks - logic-aware path selection
        "2604.20090",  # Less Languages, Less Tokens - cross-lingual CoT
        "2604.20098",  # Differentiable Conformal Training for Reasoning Factuality
        "2604.19835",  # Expert Upcycling - MoE frontier
        "2604.20487",  # Knowledge Capsules - Nonparametric memory
    ],
    "RL": [
        "2604.20659",  # GRPO-VPS - Verifiable Process Supervision
        "2604.20140",  # HiPO - Hierarchical Preference Optimization
        "2604.19859",  # DR-Venus - Deep Research Agents 10K
        "2604.20733",  # Near-Future Policy Optimization
    ],
    "Agent": [
        "2604.20714",  # Learning to Evolve (Alibaba WHITELIST)
        "2604.20200",  # Chasing the Public Score - user pressure
        "2604.20148",  # Meta-Tool - few-shot tool adaptation
    ],
    "Medical": [
        "2604.20441",  # MedSkillAudit
    ],
    "Multimodal": [
        "2604.20755",  # V-tableR1 (process-supervised MM table reasoning)
        "2604.20398",  # WebGen-R1
    ]
}

out = []
all_papers = json.loads((DATA_DIR / "papers_verified.json").read_text())
by_id = {p["id"]: p for p in all_papers}

for sec, ids in selection_ids.items():
    for aid in ids:
        p = by_id[aid].copy()
        p["_section"] = sec
        p["_whitelist"] = wl_ids.get(aid, {}).get("hits", [])
        out.append(p)

print(f"Final selection: {len(out)} papers")
for p in out:
    flag = f" [WL: {','.join(p['_whitelist'])}]" if p['_whitelist'] else ""
    print(f"  {p['_section']:10s} {p['id']} | {p['title'][:90]}{flag}")

(DATA_DIR / "final_selection.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
