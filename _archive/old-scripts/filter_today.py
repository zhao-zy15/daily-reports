import json
import random

with open("arxiv_today.json", "r") as f:
    papers = json.load(f)

categories = {
    "Pure Text LLMs": [],
    "LLM RL & Alignment": [],
    "LLM Agent": [],
    "Medical LLMs": [],
    "IR & Medical Retrieval": []
}

for p in papers:
    title = p['title'].lower()
    summary = p['summary'].lower()
    text = title + " " + summary
    
    # Exclude multi-modal, image, video, audio papers since the user only wants text/pure LLM related topics.
    if any(k in text for k in ["video", "image", "visual", "vision", "multi-modal", "multimodal", "audio", "pixel"]):
        continue
    
    if "medical" in text or "clinical" in text or "patient" in text or "health" in text:
        categories["Medical LLMs"].append(p)
    elif any(k in text for k in ["reinforcement", "ppo", "rlhf", "alignment", "dpo", "rlaif", "exploration", "reward"]):
        categories["LLM RL & Alignment"].append(p)
    elif "agent" in text or "tool" in text or "planning" in text or "reasoning" in text:
        categories["LLM Agent"].append(p)
    elif "retrieval" in text or "rag" in text or "rerank" in text or "dense" in text or "search" in text:
        categories["IR & Medical Retrieval"].append(p)
    elif "llm" in text or "language model" in text or "transformer" in text or "attention" in text:
        categories["Pure Text LLMs"].append(p)

selected = []
for cat, lst in categories.items():
    if len(lst) >= 2:
        for p in lst[:2]:
            p['category'] = cat
            selected.append(p)
    else:
        for p in lst:
            p['category'] = cat
            selected.append(p)

# If less than 10, fill up to 10 from other text LLMs
while len(selected) < 10:
    p = random.choice(categories["Pure Text LLMs"])
    if p not in selected:
        p['category'] = "Pure Text LLMs"
        selected.append(p)

with open("selected_10.json", "w") as f:
    json.dump(selected, f, indent=2)
print(f"Selected {len(selected)} papers.")
