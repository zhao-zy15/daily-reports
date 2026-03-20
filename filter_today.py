import json
import re

with open("arxiv_today.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

categories = {
    "LLM": [],
    "RL_Alignment": [],
    "Agent": [],
    "Medical": [],
    "IR": []
}

def classify(title, summary):
    text = (title + " " + summary).lower()
    if any(k in text for k in ["medical", "clinical", "health", "ehr", "diagnosis", "doctor"]):
        return "Medical"
    if any(k in text for k in ["retrieval", "rag", "dense retrieval", "rerank", "bm25"]):
        return "IR"
    if any(k in text for k in ["agent", "tool use", "planning", "multi-agent", "action space"]):
        return "Agent"
    if any(k in text for k in ["ppo", "dpo", "rlhf", "rlaif", "reinforcement learning", "alignment", "human feedback", "preference"]):
        return "RL_Alignment"
    if any(k in text for k in ["llm", "language model", "moe", "pre-train", "transformer", "context length"]):
        return "LLM"
    return None

for p in papers:
    cat = classify(p["title"], p["summary"])
    if cat:
        categories[cat].append(p)

selected = []
for cat, lst in categories.items():
    # Take up to 3 from each category to get around 15
    for p in lst[:3]:
        p["category"] = cat
        selected.append(p)

# Adjust to be between 10 and 15
if len(selected) > 15:
    selected = selected[:15]
elif len(selected) < 10:
    # Need to add more
    for p in papers:
        cat = classify(p["title"], p["summary"])
        if cat and p not in selected:
            p["category"] = cat
            selected.append(p)
        if len(selected) == 10:
            break

with open("selected_12.json", "w", encoding="utf-8") as f:
    json.dump(selected, f, indent=2, ensure_ascii=False)

print(f"Selected {len(selected)} papers.")
for p in selected:
    print(p["category"], ":", p["title"])
