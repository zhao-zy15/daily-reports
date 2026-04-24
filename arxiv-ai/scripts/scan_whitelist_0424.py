#!/usr/bin/env python3
"""扫描所有 recent 论文的 HTML5 页面提取机构信息，找出白名单命中。
白名单：DeepSeek, Qwen/阿里, OpenAI, Google/DeepMind, Scale AI, Seed/ByteDance, Hunyuan/Tencent.
"""
import json, re, time
from pathlib import Path
import urllib.request

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
HTML_DIR = DATA_DIR / "html"
HTML_DIR.mkdir(exist_ok=True)

papers = json.loads((DATA_DIR / "papers_verified.json").read_text())
recent = [p for p in papers if (p.get("published") or "")[:10] >= "2026-04-20"]
print(f"To scan: {len(recent)}")

WHITELIST = {
    "DeepSeek": [r"\bdeepseek\b"],
    "Qwen/Alibaba": [r"\bqwen\b", r"\balibaba\b", r"alibaba\s+group", r"tongyi"],
    "OpenAI": [r"\bopenai\b"],
    "Google": [r"google\s+deepmind", r"\bdeepmind\b", r"google\s+research", r"\bgoogle\b"],
    "ScaleAI": [r"\bscale\s+ai\b"],
    "Seed/ByteDance": [r"\bbytedance\b", r"\bseed\b\s+(team|research|foundation)", r"doubao", r"tiktok"],
    "Hunyuan/Tencent": [r"\btencent\b", r"hunyuan", r"wechat\s+ai"],
}

def extract_affiliations(html):
    # arXiv HTML5 has class="ltx_author_notes" or "ltx_personname"
    # Fallback: look for affiliations after author names
    text = html
    # strip scripts
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S)
    # find the author block
    m = re.search(r"<div[^>]*ltx_authors[^>]*>(.*?)</div>", text, flags=re.S)
    if m:
        block = re.sub(r"<[^>]+>", " ", m.group(1))
        return re.sub(r"\s+", " ", block)[:3000]
    # fallback: arxiv abs page
    m2 = re.search(r"Comments:</span>(.*?)</td>", text, flags=re.S)
    return None

def fetch_html(aid):
    cache = HTML_DIR / f"{aid}.html"
    if cache.exists():
        return cache.read_text(encoding="utf-8", errors="replace")
    url = f"https://arxiv.org/html/{aid}v1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", errors="replace")
        cache.write_text(html, encoding="utf-8")
        return html
    except Exception as e:
        return ""

results = []
for i, p in enumerate(recent):
    html = fetch_html(p["id"])
    if not html:
        continue
    affs = extract_affiliations(html)
    if not affs:
        # try the body text for any hit
        text_only = re.sub(r"<[^>]+>", " ", html[:20000])
        affs = text_only
    affs_low = affs.lower()
    hits = []
    for name, pats in WHITELIST.items():
        for pat in pats:
            if re.search(pat, affs_low):
                hits.append(name)
                break
    if hits:
        results.append({"id": p["id"], "title": p["title"], "hits": hits, "aff_snippet": affs[:300]})
    if (i+1) % 20 == 0:
        print(f"  scanned {i+1}/{len(recent)}, whitelist hits so far: {len(results)}")
    time.sleep(0.3)

print(f"\n=== Whitelist hits: {len(results)} ===")
for r in results:
    print(f"  {r['id']} [{', '.join(r['hits'])}] | {r['title'][:90]}")
    print(f"    ... {r['aff_snippet'][:200]}")

(DATA_DIR / "whitelist_hits.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
