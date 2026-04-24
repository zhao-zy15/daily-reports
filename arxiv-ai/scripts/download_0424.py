#!/usr/bin/env python3
"""下载 15 篇论文 PDF，提取全文，并从 HTML5 页面提取机构。"""
import json, re, time, os
from pathlib import Path
import urllib.request
import subprocess

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
PDF_DIR = DATA_DIR / "pdf"
TXT_DIR = DATA_DIR / "txt"
HTML_DIR = DATA_DIR / "html"
PDF_DIR.mkdir(exist_ok=True)
TXT_DIR.mkdir(exist_ok=True)

sel = json.loads((DATA_DIR / "final_selection.json").read_text())

def download_pdf(aid):
    pdf_path = PDF_DIR / f"{aid}.pdf"
    if pdf_path.exists() and pdf_path.stat().st_size > 10000:
        return pdf_path
    url = f"https://arxiv.org/pdf/{aid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        pdf_path.write_bytes(data)
        return pdf_path
    except Exception as e:
        print(f"  PDF {aid} fail: {e}")
        return None

def extract_text(pdf_path):
    txt_path = TXT_DIR / (pdf_path.stem + ".txt")
    if txt_path.exists() and txt_path.stat().st_size > 5000:
        return txt_path.read_text(encoding="utf-8", errors="replace")
    # try pdftotext
    try:
        subprocess.run(["pdftotext", "-layout", str(pdf_path), str(txt_path)], 
                       check=True, timeout=120, capture_output=True)
        return txt_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  pdftotext fail {pdf_path}: {e}")
        return ""

def extract_institutions(html):
    """Extract top-level institutions from arXiv HTML5 author block."""
    # ltx_authors block
    m = re.search(r'<div[^>]*ltx_authors[^>]*>(.*?)</div>\s*</div>', html, flags=re.S)
    if not m:
        m = re.search(r'<div[^>]*ltx_authors[^>]*>(.*?)</div>', html, flags=re.S)
    if not m:
        return []
    block = m.group(1)
    # Remove links but keep text
    text = re.sub(r"<[^>]+>", "|", block)
    text = re.sub(r"\s+", " ", text)
    # Split by | and look for institution-ish tokens
    # Get all affiliation labels (ltx_contact ltx_role_affiliation)
    affs = re.findall(r'ltx_role_affiliation[^>]*>([^<]+)<', block)
    if not affs:
        # fallback: parse raw text
        affs = []
    # also add explicit institutional mentions in the text
    cand_insts = set()
    KNOWN = ["deepseek", "openai", "google", "deepmind", "microsoft", "meta ai", "facebook",
             "alibaba", "qwen", "tongyi", "taobao", "tmall",
             "tencent", "hunyuan", "wechat",
             "bytedance", "seed", "tiktok", "doubao",
             "stanford", "mit", "berkeley", "cmu", "carnegie mellon", "princeton", "harvard",
             "oxford", "cambridge", "eth", "epfl", "nvidia", "apple", "amazon", "ibm",
             "tsinghua", "peking", "pku", "fudan", "shanghai", "zhejiang", "hkust",
             "nanyang", "ntu", "national university of singapore", "nus",
             "illinois", "uiuc", "michigan", "washington", "new york university", "nyu",
             "columbia", "yale", "cornell", "purdue", "mcgill", "toronto",
             "kaist", "seoul", "riken", "tsukuba", "tokyo",
             "allen institute", "ai2",
             "scale ai", "cohere", "mistral", "anthropic",
             "xai ", "x.ai",
             "baidu", "huawei", "shopee", "meituan", "jd ai", "kuaishou", "xiaomi",
             "northeastern", "ucla", "ucsd", "ucsb", "uc davis",
             "indian institute", "iit ", "iisc",
             "technion", "tel aviv",
             "ucl", "imperial", "edinburgh", "mcgill"]
    for ln in affs:
        for k in KNOWN:
            if k in ln.lower():
                cand_insts.add(ln.strip())
                break
    # Also try to capture from raw block
    raw = re.sub(r"<[^>]+>", " ", block)
    raw = re.sub(r"\s+", " ", raw)
    for k in KNOWN:
        m2 = re.search(rf"([A-Z][A-Za-z &/\-]*{re.escape(k)}[A-Za-z &/\-]*)", raw, flags=re.I)
        if m2:
            cand_insts.add(m2.group(1).strip()[:60])
    # Dedupe by base name
    out = []
    seen_keys = set()
    # manual mappings
    def normalize(s):
        low = s.lower()
        if "alibaba" in low or "taobao" in low or "tmall" in low or "qwen" in low: return "Alibaba"
        if "tencent" in low or "hunyuan" in low or "wechat" in low: return "Tencent"
        if "bytedance" in low or "seed" in low or "tiktok" in low or "doubao" in low: return "ByteDance"
        if "deepmind" in low or "google" in low: return "Google"
        if "deepseek" in low: return "DeepSeek"
        if "openai" in low: return "OpenAI"
        if "microsoft" in low: return "Microsoft"
        if "meta " in low or "facebook" in low: return "Meta"
        if "tsinghua" in low: return "Tsinghua University"
        if "peking" in low or "pku" in low: return "Peking University"
        if "stanford" in low: return "Stanford"
        if "mit " in low or "massachusetts institute" in low: return "MIT"
        if "berkeley" in low: return "UC Berkeley"
        if "cmu" in low or "carnegie mellon" in low: return "CMU"
        if "princeton" in low: return "Princeton"
        if "harvard" in low: return "Harvard"
        if "oxford" in low: return "Oxford"
        if "cambridge" in low: return "Cambridge"
        if "hkust" in low or "hong kong university of science" in low: return "HKUST"
        if "fudan" in low: return "Fudan University"
        if "zhejiang" in low: return "Zhejiang University"
        if "shanghai jiao" in low or "sjtu" in low: return "SJTU"
        if "nyu" in low or "new york university" in low: return "NYU"
        if "ucla" in low: return "UCLA"
        if "ucsd" in low: return "UCSD"
        if "nus" in low or "national university of singapore" in low: return "NUS"
        if "ntu" in low or "nanyang" in low: return "NTU"
        if "kaist" in low: return "KAIST"
        if "huawei" in low: return "Huawei"
        if "baidu" in low: return "Baidu"
        if "xiaomi" in low: return "Xiaomi"
        if "nvidia" in low: return "NVIDIA"
        if "apple" in low: return "Apple"
        return s.strip()
    for s in cand_insts:
        norm = normalize(s)
        if norm and norm not in seen_keys:
            seen_keys.add(norm)
            out.append(norm)
    return out[:5]

for p in sel:
    aid = p["id"]
    print(f"Processing {aid}: {p['title'][:60]}...")
    # download PDF
    pdf = download_pdf(aid)
    if pdf:
        txt = extract_text(pdf)
        p["fulltext_chars"] = len(txt)
        # store first 80K chars for analysis (keep full text in file)
        p["fulltext_preview"] = txt[:80000]
    # institutions
    html = (HTML_DIR / f"{aid}.html").read_text(encoding="utf-8", errors="replace") if (HTML_DIR / f"{aid}.html").exists() else ""
    if html:
        insts = extract_institutions(html)
        p["institutions"] = insts
    else:
        p["institutions"] = []
    print(f"  fulltext: {p.get('fulltext_chars',0)} chars | Institutions: {p['institutions']}")
    time.sleep(0.5)

(DATA_DIR / "final_with_fulltext.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2))
print("\nAll done. Total papers:", len(sel))
