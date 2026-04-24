#!/usr/bin/env python3
"""关键词预筛，按板块打标签：LLM / RL / Agent / Medical / Multimodal。"""
import json, re
from pathlib import Path
from collections import Counter

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
papers = json.loads((DATA_DIR / "papers_new.json").read_text())

# Keyword sets (tuned)
MM_KW = ["vision", "video", "image", "multimodal", "mllm", "vlm", "vqa", "visual", "vision-language",
         "diffusion model", "text-to-image", "text-to-video", "image generation", "video generation",
         "vision transformer", "clip ", "audio ", "speech", "asr ", "tts "]
MED_KW = ["medical", "clinical", "health", "patient", "radiology", "pathology", "ehr", "electronic health",
          "biomed", "disease", "diagnosis", "hospital", "drug", "pharma", "medic"]
RL_KW = ["reinforcement learning", "rlhf", "rlvr", "dpo", "grpo", "ppo", "reward model", "reward hacking",
         "policy optimization", "exploration", "kl divergence", "alignment", "preference learning",
         "self-improvement", "self-rewarding", "process reward", "rlaif"]
AGENT_KW = ["agent", "tool use", "tool-use", "tool calling", "multi-agent", "web agent", "gui agent",
            "planning", "react ", "workflow", "orchestrat"]
LLM_GENERIC_KW = ["llm", "language model", "transformer", "attention", "fine-tun", "pretrain",
                  "instruction tuning", "reasoning", "chain-of-thought", "cot ", "in-context"]

def score(text, kws):
    t = text.lower()
    return sum(1 for k in kws if k in t)

labeled = []
for p in papers:
    txt = (p["title"] + " " + p["abstract"]).lower()
    mm = score(txt, MM_KW)
    med = score(txt, MED_KW)
    rl = score(txt, RL_KW)
    ag = score(txt, AGENT_KW)
    llm = score(txt, LLM_GENERIC_KW)
    # classification priority:
    # Multimodal if strong MM signal
    # Medical next
    # RL > Agent > LLM
    is_mm = mm >= 2 or "multimodal" in txt or "vision-language" in txt or "mllm" in txt or "vlm" in txt
    section = None
    if is_mm:
        section = "Multimodal"
    elif med >= 2:
        section = "Medical"
    elif rl >= 2:
        section = "RL"
    elif ag >= 2 and rl < 2:
        section = "Agent"
    elif llm >= 1:
        section = "LLM"
    else:
        section = "LLM"  # default bucket for CL/AI/LG
    p["section_guess"] = section
    p["_scores"] = dict(mm=mm, med=med, rl=rl, ag=ag, llm=llm)
    labeled.append(p)

c = Counter(p["section_guess"] for p in labeled)
print("Initial section guess distribution:", dict(c))

(DATA_DIR / "papers_labeled.json").write_text(json.dumps(labeled, ensure_ascii=False, indent=2))
