#!/usr/bin/env python3
"""从 PDF 首页文本提取机构（更可靠），并结合 HTML 补充。"""
import json, re
from pathlib import Path

DATA_DIR = Path("/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/2026-04-24")
TXT_DIR = DATA_DIR / "txt"
HTML_DIR = DATA_DIR / "html"

sel = json.loads((DATA_DIR / "final_full.json").read_text())

KNOWN_ORGS = [
    ("Alibaba", ["alibaba", "taobao", "tmall", "qwen", "tongyi"]),
    ("Tencent", ["tencent", "hunyuan", "wechat ai"]),
    ("ByteDance", ["bytedance", "tiktok", "doubao"]),
    ("ByteDance Seed", ["bytedance seed", "seed (", "seed,"]),
    ("Google DeepMind", ["google deepmind", "deepmind"]),
    ("Google", ["google research", "google,"]),
    ("DeepSeek", ["deepseek"]),
    ("OpenAI", ["openai"]),
    ("Microsoft", ["microsoft research", "microsoft,"]),
    ("Meta AI", ["meta ai", "meta platforms", "facebook ai research"]),
    ("NVIDIA", ["nvidia"]),
    ("Apple", ["apple inc"]),
    ("IBM Research", ["ibm research"]),
    ("Salesforce", ["salesforce"]),
    ("Amazon", ["amazon", "aws ai"]),
    ("Huawei", ["huawei"]),
    ("Baidu", ["baidu"]),
    ("Xiaomi", ["xiaomi"]),
    ("Meituan", ["meituan", "longcat"]),
    ("Kuaishou", ["kuaishou"]),
    ("Tsinghua University", ["tsinghua"]),
    ("Peking University", ["peking university"]),
    ("Fudan University", ["fudan"]),
    ("Zhejiang University", ["zhejiang univ"]),
    ("SJTU", ["shanghai jiao tong", "sjtu"]),
    ("Renmin University", ["renmin univ"]),
    ("HKUST", ["hong kong university of science", "hkust"]),
    ("HKU", ["university of hong kong"]),
    ("CUHK", ["chinese university of hong kong", "cuhk"]),
    ("Stanford", ["stanford"]),
    ("MIT", ["massachusetts institute of technology"]),
    ("UC Berkeley", ["uc berkeley", "university of california, berkeley"]),
    ("CMU", ["carnegie mellon"]),
    ("Princeton", ["princeton"]),
    ("Harvard", ["harvard"]),
    ("Yale", ["yale univ"]),
    ("Columbia", ["columbia univ"]),
    ("Oxford", ["university of oxford"]),
    ("Cambridge", ["university of cambridge"]),
    ("NYU", ["new york university"]),
    ("UCLA", ["university of california, los angeles", "ucla"]),
    ("UCSD", ["university of california, san diego", "ucsd"]),
    ("NUS", ["national university of singapore"]),
    ("NTU", ["nanyang technological"]),
    ("KAIST", ["kaist", "korea advanced institute"]),
    ("ETH Zurich", ["eth zurich", "eth zürich"]),
    ("EPFL", ["epfl"]),
    ("Edinburgh", ["university of edinburgh"]),
    ("Shanghai AI Lab", ["shanghai artificial intelligence laboratory", "shanghai ai lab"]),
    ("CAS", ["chinese academy of sciences"]),
    ("UCAS", ["university of chinese academy of sciences"]),
    ("HIT", ["harbin institute of technology"]),
    ("UIUC", ["university of illinois"]),
    ("University of Michigan", ["university of michigan"]),
    ("University of Washington", ["university of washington"]),
    ("Waterloo", ["university of waterloo"]),
    ("Toronto", ["university of toronto"]),
    ("McGill", ["mcgill"]),
    ("Northeastern", ["northeastern university"]),
    ("BIT", ["beijing institute of technology"]),
    ("BUPT", ["beijing university of posts"]),
    ("SCUT", ["south china university of technology"]),
    ("USTC", ["university of science and technology of china"]),
]

def detect_from_text(text, window=2000):
    # focus on first 2500 chars (usually has author affiliations)
    header = text[:window]
    low = header.lower()
    out = []
    for canonical, kws in KNOWN_ORGS:
        for kw in kws:
            if kw in low:
                if canonical not in out:
                    out.append(canonical)
                break
    return out

for p in sel:
    aid = p["id"]
    txt = (TXT_DIR / f"{aid}.txt").read_text(encoding="utf-8", errors="replace") if (TXT_DIR / f"{aid}.txt").exists() else ""
    insts_pdf = detect_from_text(txt)
    insts_html = p.get("institutions", [])
    # merge (prefer PDF-detected)
    merged = list(dict.fromkeys(insts_pdf + insts_html))
    p["institutions"] = merged
    print(f"  {aid}: {merged}")

(DATA_DIR / "final_with_insts.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2))
