import json

with open("arxiv_today.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

# strict keywords
keywords = {
    "Pure Text LLMs": ["long context", "moe", "pre-train", "transformer", "scaling", "parameter"],
    "LLM RL & Alignment": ["rlhf", "dpo", "ppo", "preference", "alignment", "reward"],
    "LLM Agent": ["agent", "tool", "plan", "reason", "multi-agent"],
    "Medical LLMs": ["medical", "clinical", "disease", "health", "patient"],
    "IR & Medical Retrieval": ["retrieval", "rag", "dense", "rerank", "search"]
}

selected = []
counts = {k: 0 for k in keywords}

for p in papers:
    text = (p["title"] + " " + p["summary"]).lower()
    for cat, kws in keywords.items():
        if counts[cat] < 2 and any(k in text for k in kws):
            p["category"] = cat
            selected.append(p)
            counts[cat] += 1
            break

# If any category is short, fill with remaining
for cat in keywords:
    while counts[cat] < 2:
        for p in papers:
            if p not in selected:
                p["category"] = cat
                selected.append(p)
                counts[cat] += 1
                break

with open("selected_10.json", "w", encoding="utf-8") as f:
    json.dump(selected[:10], f, indent=2, ensure_ascii=False)
