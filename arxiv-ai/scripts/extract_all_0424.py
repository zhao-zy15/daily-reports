#!/usr/bin/env python3
"""用 pypdf 提取 PDF 全文（不截断），并改进机构提取。"""
import json, re, time
from pathlib import Path
import pypdf

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
PDF_DIR = DATA_DIR / "pdf"
TXT_DIR = DATA_DIR / "txt"
HTML_DIR = DATA_DIR / "html"
TXT_DIR.mkdir(exist_ok=True)

sel = json.loads((DATA_DIR / "final_selection.json").read_text())

def extract_pdf_text(pdf_path):
    txt_path = TXT_DIR / (pdf_path.stem + ".txt")
    if txt_path.exists() and txt_path.stat().st_size > 5000:
        return txt_path.read_text(encoding="utf-8", errors="replace")
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        texts = []
        for page in reader.pages:
            try:
                texts.append(page.extract_text() or "")
            except Exception:
                texts.append("")
        full = "\n\n".join(texts)
        txt_path.write_text(full, encoding="utf-8")
        return full
    except Exception as e:
        print(f"  fail: {e}")
        return ""

def norm_inst(s):
    low = s.lower()
    if "alibaba" in low or "taobao" in low or "tmall" in low or "qwen" in low or "tongyi" in low: return "Alibaba"
    if "tencent" in low or "hunyuan" in low or "wechat" in low: return "Tencent"
    if "bytedance" in low or "tiktok" in low or "doubao" in low: return "ByteDance"
    if "deepmind" in low: return "Google DeepMind"
    if "google " in low or "google research" in low: return "Google"
    if "deepseek" in low: return "DeepSeek"
    if "openai" in low: return "OpenAI"
    if "microsoft" in low: return "Microsoft"
    if "meta ai" in low or "meta platforms" in low or "facebook ai" in low: return "Meta AI"
    if "tsinghua" in low: return "Tsinghua University"
    if "peking" in low or ("pku" in low and "university" in low): return "Peking University"
    if "stanford" in low: return "Stanford"
    if "mit" == low.strip() or "massachusetts institute" in low: return "MIT"
    if "berkeley" in low and "uc" in low: return "UC Berkeley"
    if "carnegie mellon" in low or low.strip() == "cmu": return "CMU"
    if "princeton" in low: return "Princeton"
    if "harvard" in low: return "Harvard"
    if "oxford" in low: return "Oxford"
    if "cambridge" in low and "university" in low: return "Cambridge"
    if "hkust" in low or "hong kong university of science" in low: return "HKUST"
    if "fudan" in low: return "Fudan University"
    if "zhejiang university" in low: return "Zhejiang University"
    if "shanghai jiao" in low or "sjtu" in low: return "SJTU"
    if "renmin university" in low: return "Renmin University"
    if "beijing institute" in low: return "BIT"
    if "nyu" in low.replace("inyu","") or "new york university" in low: return "NYU"
    if "ucla" in low: return "UCLA"
    if "ucsd" in low: return "UCSD"
    if "nus" == low.strip() or "national university of singapore" in low: return "NUS"
    if "ntu" == low.strip() or "nanyang" in low: return "NTU"
    if "kaist" in low: return "KAIST"
    if "huawei" in low: return "Huawei"
    if "baidu" in low: return "Baidu"
    if "xiaomi" in low: return "Xiaomi"
    if "meituan" in low or "longcat" in low: return "Meituan"
    if "kuaishou" in low: return "Kuaishou"
    if "nvidia" in low: return "NVIDIA"
    if "apple" in low: return "Apple"
    if "amazon" in low and ("research" in low or "aws" in low or "science" in low): return "Amazon"
    if "ibm research" in low: return "IBM Research"
    if "salesforce" in low: return "Salesforce"
    if "scale ai" in low: return "Scale AI"
    if "anthropic" in low: return "Anthropic"
    if "cohere" in low: return "Cohere"
    if "hugging face" in low: return "Hugging Face"
    if "allen institute" in low or low.strip() == "ai2": return "AI2"
    if "ethz" in low or "eth zurich" in low: return "ETH Zurich"
    if "epfl" in low: return "EPFL"
    if "ucl" in low: return "UCL"
    if "imperial college" in low: return "Imperial College"
    if "edinburgh" in low and "university" in low: return "Edinburgh"
    if "hku" == low.strip() or "university of hong kong" in low: return "HKU"
    if "cuhk" in low or "chinese university of hong kong" in low: return "CUHK"
    if "city university of hong kong" in low: return "CityU HK"
    if "cas" == low.strip() or "chinese academy of science" in low: return "CAS"
    if "shanghai ai" in low: return "Shanghai AI Lab"
    if "bjut" in low: return "BJUT"
    if "ucas" == low.strip(): return "UCAS"
    if "harbin institute" in low or "hit" == low.strip(): return "HIT"
    if "seed" in low and "bytedance" not in low: return "ByteDance Seed"
    if "purdue" in low: return "Purdue"
    if "university of illinois" in low or "uiuc" in low: return "UIUC"
    if "university of michigan" in low or "umich" in low: return "Michigan"
    if "university of washington" in low: return "UW"
    if "waterloo" in low: return "Waterloo"
    if "toronto" in low and "university" in low: return "Toronto"
    if "mcgill" in low: return "McGill"
    if "oxford" in low: return "Oxford"
    # strip common suffixes for shorter display
    s_clean = re.sub(r"\b(university|institute of technology|department of .*)\b", "", s, flags=re.I).strip()
    # fallback — keep shorter form
    s_clean = s_clean.strip().strip(",").strip()
    # only keep if not too long
    if len(s_clean) > 5 and len(s_clean) < 35 and "." not in s_clean and "," not in s_clean:
        return s_clean
    return None

def extract_institutions_from_html(html):
    if not html:
        return []
    # Focus on ltx_authors
    m = re.search(r'<div[^>]*class="[^"]*ltx_authors[^"]*"[^>]*>(.*?)</div>\s*(?=<div|<section|<h)', html, flags=re.S)
    if not m:
        m = re.search(r'<div[^>]*class="[^"]*ltx_authors[^"]*"[^>]*>(.*?)</div>', html, flags=re.S)
    if not m:
        return []
    block = m.group(1)
    # Find <span class="ltx_role_affiliation"> or <span class="ltx_role_institutetext">
    affs = []
    for pat in [r'<span[^>]*ltx_role_institutetext[^>]*>([^<]+)</span>',
                r'<span[^>]*ltx_role_affiliation[^>]*>([^<]+)</span>',
                r'<span[^>]*institution[^>]*>([^<]+)</span>']:
        affs += re.findall(pat, block, flags=re.I)
    # Also raw block for cases where institutes are in <br> separated lines
    raw = re.sub(r"<br\s*/?>", "|", block)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = re.sub(r"\s+", " ", raw)
    # Heuristic extraction from raw
    cand = []
    for a in affs:
        a = re.sub(r"\s+", " ", a).strip()
        if len(a) > 3:
            cand.append(a)
    # Scan raw block for known org names
    KNOWN_ORGS = ["Alibaba", "Qwen", "Tongyi", "Taobao", "Tmall",
                  "Tencent", "Hunyuan", "WeChat AI",
                  "ByteDance", "Doubao",
                  "DeepMind", "Google Research", "Google DeepMind", "Google",
                  "DeepSeek", "OpenAI", "Microsoft Research", "Microsoft",
                  "Meta AI", "Meta Platforms", "Facebook AI",
                  "Stanford", "MIT", "UC Berkeley", "Berkeley", "CMU", "Carnegie Mellon",
                  "Princeton", "Harvard", "Yale", "Columbia",
                  "Oxford", "Cambridge", "NYU", "UCLA", "UCSD",
                  "Tsinghua", "Peking", "Fudan", "Zhejiang University", "SJTU", "Renmin",
                  "HKUST", "HKU", "CUHK", "NUS", "NTU", "KAIST",
                  "Huawei", "Baidu", "Xiaomi", "Meituan", "Longcat", "Kuaishou",
                  "NVIDIA", "Apple", "Amazon", "IBM", "Salesforce",
                  "Scale AI", "Anthropic", "Cohere", "Mistral",
                  "Allen Institute", "AI2",
                  "ETH Zurich", "EPFL", "Edinburgh",
                  "Shanghai AI Lab",
                  "CAS", "UCAS",
                  "HIT", "BIT",
                  "UIUC", "Michigan", "Washington",
                  "Waterloo", "Toronto", "McGill"]
    for org in KNOWN_ORGS:
        if re.search(rf'\b{re.escape(org)}\b', raw):
            cand.append(org)
    # Normalize & dedupe
    out = []
    seen = set()
    for s in cand:
        n = norm_inst(s)
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out[:6]

for p in sel:
    aid = p["id"]
    print(f"== {aid}: {p['title'][:60]}")
    pdf = PDF_DIR / f"{aid}.pdf"
    if pdf.exists():
        txt = extract_pdf_text(pdf)
        p["fulltext_chars"] = len(txt)
    else:
        p["fulltext_chars"] = 0
        txt = ""
    html_path = HTML_DIR / f"{aid}.html"
    html = html_path.read_text(encoding="utf-8", errors="replace") if html_path.exists() else ""
    p["institutions"] = extract_institutions_from_html(html)
    print(f"  {p['fulltext_chars']} chars | Inst: {p['institutions']}")

# keep preview (first 80K for analysis decisions)
for p in sel:
    aid = p["id"]
    txt = (TXT_DIR / f"{aid}.txt").read_text(encoding="utf-8", errors="replace") if (TXT_DIR / f"{aid}.txt").exists() else ""
    p["fulltext"] = txt  # full text, no truncation
(DATA_DIR / "final_full.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2))
print(f"\nAll {len(sel)} papers enriched. Total fulltext chars: {sum(p.get('fulltext_chars',0) for p in sel)}")
