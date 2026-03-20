import json

with open('selected_papers.json') as f:
    papers = json.load(f)

for cat in ['Pure Text LLMs', 'LLM RL & Alignment', 'LLM Agent', 'Medical LLMs', 'IR & Medical Retrieval']:
    print(f"\n\n{'='*50}\nCATEGORY: {cat}\n{'='*50}")
    for p in papers:
        if p['category'] == cat:
            print(f"\n[{p['id']}] {p['title']}")
            print(f"URL: https://arxiv.org/abs/{p['id']}")
            print(f"SUMMARY: {p['summary']}")
