import json

with open('arxiv_latest.json') as f:
    papers = json.load(f)

categories = {
    'Pure Text LLMs': ['moe', 'mixture of expert', 'long context', 'pre-train', 'scaling law', 'architecture'],
    'LLM RL & Alignment': ['rlhf', 'rlaif', 'dpo', 'ppo', 'reinforcement learning', 'alignment', 'preference'],
    'LLM Agent': ['agent', 'tool use', 'planning', 'self-reflection', 'multi-agent', 'reasoning'],
    'Medical LLMs': ['medical', 'clinical', 'diagnosis', 'healthcare', 'radiology', 'mri', 'patient'],
    'IR & Medical Retrieval': ['rag', 'retrieval', 'dense retrieval', 'reranking', 'knowledge base']
}

selected = []
for p in papers:
    text = (p['title'] + " " + p['summary']).lower()
    matched_cat = None
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            matched_cat = cat
            break
    if matched_cat:
        p['category'] = matched_cat
        selected.append(p)

# We need between 10 and 15 papers. Let's aim for 3 per category (total 15), or at least 2 per category (total 10).
final_selection = []
counts = {cat: 0 for cat in categories}
for p in selected:
    cat = p['category']
    if counts[cat] < 3:
        final_selection.append(p)
        counts[cat] += 1

print(json.dumps(final_selection, indent=2))
