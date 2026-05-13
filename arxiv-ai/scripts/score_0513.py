"""Score and classify candidate papers by section."""
import json
import re
from pathlib import Path

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
papers = json.loads((DATA_DIR / "papers_new.json").read_text(encoding="utf-8"))

# Keywords
LLM_KW = ["large language model", "language model", "pretrain", "pre-training", "fine-tun", "instruction tuning",
          "long context", "kv cache", "attention", "transformer", "tokeniz", "decoding", "speculative",
          "mixture of experts", "moe", "quantization", "distillation", "scaling law", "perplexity",
          "linear attention", "retrieval-augmented", "rag", "in-context learning", "chain-of-thought",
          "reasoning", "math reasoning", "code generation"]
RL_KW = ["reinforcement learning", "rlhf", "rlaif", "rlvr", "dpo", "ppo", "grpo", "reward model",
         "preference", "alignment", "exploration", "policy optimization", "online rl", "self-play",
         "rejection sampling", "verifier"]
AGENT_KW = ["agent", "tool use", "tool-use", "tool calling", "multi-agent", "web agent", "browser",
            "swe-bench", "software engineering agent", "computer use", "memory", "planning",
            "react agent", "gui agent", "operating system"]
MEDICAL_KW = ["clinical", "medical", "ehr", "electronic health record", "radiology", "pathology",
              "biomedical", "patient", "diagnos", "icd", "umls", "snomed", "drug", "disease",
              "healthcare", "medication"]
MULTIMODAL_KW = ["multimodal", "vision-language", "vlm", "image", "video", "visual", "image-text",
                 "vqa", "captioning", "audio", "speech", "diffusion model", "image generation",
                 "video generation", "screen", "ocr"]


def has_kw(text, kws):
    t = text.lower()
    return [kw for kw in kws if kw in t]


for p in papers:
    text = (p["title"] + " " + p["abstract"]).lower()
    p["mm_kw"] = has_kw(text, MULTIMODAL_KW)
    p["llm_kw"] = has_kw(text, LLM_KW)
    p["rl_kw"] = has_kw(text, RL_KW)
    p["agent_kw"] = has_kw(text, AGENT_KW)
    p["med_kw"] = has_kw(text, MEDICAL_KW)
    # Decide section
    is_mm = bool(p["mm_kw"]) and not all(k in ["image"] for k in p["mm_kw"])
    # More strict: if any strong multimodal keyword
    strong_mm = any(k in text for k in ["multimodal", "vision-language", "vlm", "video", "image generation",
                                          "video generation", "vqa", "speech", "audio", "captioning",
                                          "diffusion model", "ocr", "visual reasoning", "screen"])
    p["is_mm"] = strong_mm

    if p["med_kw"]:
        p["section"] = "medical"
    elif strong_mm:
        p["section"] = "multimodal"
    elif p["agent_kw"] and any(k in text for k in ["agent", "tool use", "tool-use"]):
        # but exclude vision agents
        p["section"] = "agent"
    elif p["rl_kw"]:
        p["section"] = "rl"
    elif p["llm_kw"]:
        p["section"] = "llm"
    else:
        p["section"] = "other"

# Score: prefer papers with strong novelty signals in title
NOVELTY = ["novel", "we propose", "we introduce", "we present", "framework", "benchmark", "method",
           "outperform", "state-of-the-art", "achieve"]


def score(p):
    s = 0
    text = (p["title"] + " " + p["abstract"]).lower()
    if any(w in p["title"].lower() for w in ["benchmark", "framework", "novel"]):
        s += 2
    s += len(p["llm_kw"]) + 2 * len(p["rl_kw"]) + 2 * len(p["agent_kw"]) + 3 * len(p["med_kw"])
    if "reasoning" in text: s += 2
    if "exploration" in text: s += 1
    if "long context" in text or "kv cache" in text: s += 2
    if "moe" in text or "mixture of experts" in text: s += 1
    if "quantization" in text: s += 1
    if "attention" in text: s += 1
    if "agent" in text: s += 1
    return s


for p in papers:
    p["score"] = score(p)

# Group
groups = {"llm": [], "rl": [], "agent": [], "medical": [], "multimodal": [], "other": []}
for p in papers:
    groups[p["section"]].append(p)

for k in groups:
    groups[k].sort(key=lambda x: -x["score"])

# Print top candidates
for sect, ps in groups.items():
    print(f"\n=== {sect.upper()} ({len(ps)} total, top 15) ===")
    for p in ps[:15]:
        print(f"  [{p['score']}] {p['id']}: {p['title'][:90]}")

# Save top candidates
candidates = {}
for sect in ["llm", "rl", "agent", "medical", "multimodal"]:
    candidates[sect] = groups[sect][:20]
(DATA_DIR / "candidates.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved candidates to {DATA_DIR / 'candidates.json'}")
