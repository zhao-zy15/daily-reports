import json
with open("selected_12.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

# Keep exactly 2 per category = 10 papers
final_list = []
counts = {"LLM":0, "RL_Alignment":0, "Agent":0, "Medical":0, "IR":0}
for p in papers:
    c = p.get("category")
    if counts[c] < 2:
        final_list.append(p)
        counts[c] += 1

with open("selected_10.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=2, ensure_ascii=False)
