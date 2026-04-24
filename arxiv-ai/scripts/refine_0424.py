#!/usr/bin/env python3
"""精细化筛选：仅保留真正涉及 LLM/Transformer/reasoning 的 LLM 桶。"""
import json, re
from pathlib import Path

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
papers = json.loads((DATA_DIR / "papers_verified.json").read_text())
recent = [p for p in papers if (p.get("published") or "")[:10] >= "2026-04-20"]

# For LLM section: require strong LLM/language-model keywords in title or abstract
LLM_STRONG = ["llm", "large language model", "language model", "pretrain", "pre-train", 
              "fine-tun", "instruction tun", "sft", "chain-of-thought", "reasoning model",
              "gpt", "qwen", "llama", "mistral", "transformer-based language", "decoder-only",
              "autoregressive language", "tokenizer", "pre-training", "in-context learning"]
# exclude non-llm domains
NON_LLM = ["stock ranking", "federated learning", "graph neural network", "propagation",
           "financial", "market", "defi", "automated market maker", "active learning for object",
           "retail", "power grid", "electricity", "manifold", "sheaf", "anomaly detection",
           "optimization problem solving", "ontology", "bayesian equipment", "ice-layer"]

def is_real_llm(p):
    t = (p["title"] + " " + p["abstract"]).lower()
    if any(k in t for k in NON_LLM):
        return False
    return any(k in t for k in LLM_STRONG)

llm_papers = [p for p in recent if p["section_guess"] == "LLM" and is_real_llm(p)]
print(f"Real LLM papers (filtered): {len(llm_papers)}")

# Score them
HIGH = ["we propose", "we introduce", "novel", "significant", "sota", "outperform", "achieve",
        "surpass", "first", "we show", "we prove", "we find"]
def sc(p):
    t = (p["title"]+" "+p["abstract"]).lower()
    s = sum(2 for k in HIGH if k in t)
    s += min(len(p["abstract"])/300, 5)
    if re.search(r"\b\d{1,3}\.?\d*\s*%", t): s += 2
    if "ablation" in t: s += 2
    if "benchmark" in t: s += 1
    # boost reasoning/RL/SFT papers
    for hi in ["rlhf", "rlvr", "dpo", "grpo", "reasoning", "reward", "preference", "verifier",
               "distill", "quantiz", "kv cache", "attention", "speculative", "moe ", "mixture of expert",
               "reinforcement", "efficien", "scaling", "alignment", "hallucina", "jailbreak", "safety"]:
        if hi in t: s += 1.5
    return s

for p in llm_papers:
    p["_score"] = round(sc(p), 1)
llm_papers.sort(key=lambda p: -p["_score"])

print("\n=== Top 25 Real LLM papers ===")
for p in llm_papers[:25]:
    print(f"  [{p['_score']:5.1f}] {p['id']} | {p['title'][:100]}")

# Also re-examine RL section
rl_papers = [p for p in recent if p["section_guess"] == "RL"]
for p in rl_papers:
    p["_score"] = round(sc(p), 1)
rl_papers.sort(key=lambda p: -p["_score"])
print("\n=== RL Top ===")
for p in rl_papers[:15]:
    print(f"  [{p['_score']:5.1f}] {p['id']} | {p['title'][:100]}")

# Save
out = {
    "LLM_real": llm_papers[:20],
    "RL": rl_papers[:15],
    "Agent": sorted([p for p in recent if p["section_guess"]=="Agent"], key=lambda x:-sc(x))[:15],
    "Medical": sorted([p for p in recent if p["section_guess"]=="Medical"], key=lambda x:-sc(x))[:12],
    "Multimodal": sorted([p for p in recent if p["section_guess"]=="Multimodal"], key=lambda x:-sc(x))[:12],
}
for sec in ["Agent", "Medical", "Multimodal"]:
    for p in out[sec]:
        p["_score"] = round(sc(p), 1)

(DATA_DIR / "candidates_refined.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"\nSaved. Totals: LLM={len(out['LLM_real'])}, RL={len(out['RL'])}, Agent={len(out['Agent'])}, Med={len(out['Medical'])}, MM={len(out['Multimodal'])}")
