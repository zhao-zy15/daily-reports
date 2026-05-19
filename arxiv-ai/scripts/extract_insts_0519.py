"""Extract institutions from PDF first page or HTML."""
import json, re
from pathlib import Path

DATE = "2026-05-19"
DATA = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
papers = json.loads((DATA / "verified.json").read_text())
TXT_DIR = DATA / "fulltext"
HTML_DIR = DATA / "html"

# Common institutional keywords for fuzzy detection
INST_KEYWORDS = [
    "University", "Institute", "Laboratory", "Lab", "College",
    "Research", "Academy", "School", "Tsinghua", "Peking",
    "Stanford", "MIT", "Berkeley", "Harvard", "Princeton",
    "CMU", "Carnegie", "Microsoft", "Google", "Meta", "OpenAI",
    "DeepMind", "Anthropic", "Apple", "Amazon", "NVIDIA",
    "Baidu", "Alibaba", "Tencent", "ByteDance", "Huawei",
    "Xiaomi", "DeepSeek", "Hunyuan", "Qwen",
]


def extract_from_html(html_path):
    if not html_path.exists():
        return []
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    # Look for common author affiliation markup
    # arxiv html5: <span class="ltx_role_affiliation"> or <div class="ltx_authors">...
    insts = set()
    # 1) ltx_role_affiliation spans
    for m in re.finditer(r'class="ltx_role_affiliation"[^>]*>([^<]+)<', text):
        s = re.sub(r'\s+', ' ', m.group(1)).strip()
        if 3 < len(s) < 200:
            insts.add(s)
    # 2) ltx_personname / ltx_author_notes blocks containing 'University', etc.
    if not insts:
        for m in re.finditer(r'<div class="ltx_authors"[^>]*>(.*?)</div>', text, re.S):
            block = m.group(1)
            # Strip tags
            stripped = re.sub(r'<[^>]+>', ' ', block)
            stripped = re.sub(r'\s+', ' ', stripped).strip()
            # Find institution-like phrases
            for kw in INST_KEYWORDS:
                for mm in re.finditer(r'([A-Z][A-Za-z&\-\s\.]{2,80}\b' + kw + r'[A-Za-z\s]{0,50})', stripped):
                    s = re.sub(r'\s+', ' ', mm.group(1)).strip()
                    if 5 < len(s) < 120:
                        insts.add(s)
    return sorted(insts)


def extract_from_pdf_text(txt_path, title):
    if not txt_path.exists():
        return []
    text = txt_path.read_text(encoding="utf-8", errors="ignore")
    # Take first 4000 chars (after title)
    head = text[:5000]
    # Strip title to focus on author block
    insts = set()
    for kw in INST_KEYWORDS:
        for m in re.finditer(r'([A-Z][A-Za-z&\-\s\.,]{2,60}\b' + kw + r'\b[A-Za-z\s,\-]{0,60})', head):
            s = re.sub(r'\s+', ' ', m.group(1)).strip().rstrip(",.;:")
            if 5 < len(s) < 150 and not s.startswith("Abstract"):
                insts.add(s)
    return sorted(insts)


for p in papers:
    aid = p["id"]
    htmls = extract_from_html(HTML_DIR / f"{aid}.html")
    pdfs = extract_from_pdf_text(TXT_DIR / f"{aid}.txt", p["title"])
    insts = htmls if htmls else pdfs
    p["institutions_raw"] = insts[:10]
    print(f"{aid}: {p['title'][:60]}")
    for i in p["institutions_raw"]:
        print(f"    - {i}")

(DATA / "verified.json").write_text(json.dumps(papers, ensure_ascii=False, indent=2))
print(f"\nDone, updated verified.json")
