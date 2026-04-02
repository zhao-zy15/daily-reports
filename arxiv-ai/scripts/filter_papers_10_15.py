import json

with open('arxiv_today.json') as f:
    papers = json.load(f)

categories = {
    '🧠 纯文本大语言模型 (Pure Text LLMs)': [' moe ', 'mixture of expert', 'long context', 'pre-train', 'scaling law', 'architecture', 'transformers', 'tokenization', 'text generation', 'language model'],
    '🎯 LLM 强化学习与对齐 (LLM RL & Alignment)': ['rlhf', 'rlaif', 'dpo', 'ppo', 'reinforcement learning', 'alignment', 'preference', 'exploration', 'reward', 'reinforcement'],
    '🤖 LLM Agent (智能体)': [' agent', 'tool use', 'planning', 'self-reflection', 'multi-agent', 'reasoning', 'autonomous'],
    '⚕️ 医学 LLM (Medical LLMs)': ['medical', 'clinical', 'diagnosis', 'healthcare', 'radiology', 'mri', 'patient', 'biomedical', 'psychiatric'],
    '🔍 信息检索与医学检索 (IR & Medical Retrieval)': [' rag ', 'retrieval', 'dense retrieval', 'reranking', 'knowledge base', ' search ']
}

exclude_words = ['video', 'vision', 'visual', 'image', 'multimodal', 'multi-modal', 'audio', 'speech', 'diffusion', 'unet', 'camera', 'segmentation', 'pixel', 'anode', 'battery', 'quantum']

selected = []
for p in papers:
    text = (p['title'] + " " + p['summary']).lower()
    
    matched_cat = None
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            matched_cat = cat
            break

    # Exclude multi-modal papers unless they are medical
    if matched_cat != '⚕️ 医学 LLM (Medical LLMs)' and any(ew in text for ew in exclude_words):
        continue

    if matched_cat:
        p['category'] = matched_cat
        selected.append(p)

# Select max 3 per category to get a balanced list of 10-15
final_selection = []
counts = {cat: 0 for cat in categories}
for p in selected:
    cat = p['category']
    if counts[cat] < 3:
        final_selection.append(p)
        counts[cat] += 1

with open('selected_papers.json', 'w') as f:
    json.dump(final_selection, f, indent=2)

print(f"Selected {len(final_selection)} papers.")
