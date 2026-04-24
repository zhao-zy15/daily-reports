#!/usr/bin/env python3
"""为每篇论文提取 Abstract/Introduction 起始段、Method、Experiments、Ablation 关键段落，
保存便于后续写 part 文件时参考。"""
import json, re
from pathlib import Path

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
TXT_DIR = DATA_DIR / "txt"
sel = json.loads((DATA_DIR / "final_ready.json").read_text())

OUT = DATA_DIR / "per_paper_keyinfo"
OUT.mkdir(exist_ok=True)

def find_section(text, patterns):
    """Return section-like substring starting at first match."""
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return m.start()
    return -1

for p in sel:
    aid = p["id"]
    txt = (TXT_DIR / f"{aid}.txt").read_text(encoding="utf-8", errors="replace")
    # key anchor positions
    abs_start = find_section(txt, [r"\bAbstract\b"])
    intro_start = find_section(txt, [r"\n\s*1\s+Introduction\b", r"\nIntroduction\b"])
    method_start = find_section(txt, [r"\n\s*\d\s+(Method|Methodology|Approach|Framework|The\s+\w+\s+Method)\b",
                                       r"\nMethod\b", r"\nMethodology\b", r"\nApproach\b"])
    exp_start = find_section(txt, [r"\n\s*\d\s+(Experiments?|Experimental\s+Setup|Evaluation)\b",
                                   r"\nExperiments\b"])
    abl_start = find_section(txt, [r"\n.*Ablation\b"])
    concl_start = find_section(txt, [r"\n\s*\d\s+Conclusion\b", r"\nConclusion\b"])
    # abstract slice
    abstract_slice = txt[abs_start:intro_start] if abs_start >= 0 and intro_start > abs_start else txt[:2500]
    intro_slice = txt[intro_start:method_start] if intro_start >= 0 and method_start > intro_start else txt[intro_start:intro_start+5000] if intro_start>=0 else ""
    method_slice = txt[method_start:exp_start] if method_start >= 0 and exp_start > method_start else (txt[method_start:method_start+15000] if method_start >= 0 else "")
    exp_slice = txt[exp_start:concl_start] if exp_start >= 0 and concl_start > exp_start else (txt[exp_start:exp_start+10000] if exp_start >= 0 else "")
    abl_slice = txt[abl_start:abl_start+5000] if abl_start >= 0 else ""
    key = {
        "id": aid,
        "title": p["title"],
        "institutions": p["institutions"],
        "section": p["_section"],
        "abstract": abstract_slice[:4000],
        "intro": intro_slice[:6000],
        "method": method_slice[:20000],
        "experiments": exp_slice[:10000],
        "ablation": abl_slice,
        "fulltext_len": len(txt),
    }
    (OUT / f"{aid}.json").write_text(json.dumps(key, ensure_ascii=False, indent=2))
    print(f"{aid} | abs:{len(abstract_slice)} intro:{len(intro_slice)} meth:{len(method_slice)} exp:{len(exp_slice)} abl:{len(abl_slice)}")

print("Key info extracted.")
