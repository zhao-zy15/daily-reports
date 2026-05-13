"""Extract text and institutions from HTML fulltext + abs pages, fallback to PDF."""
import json
import re
import urllib.request
from pathlib import Path
from html.parser import HTMLParser

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
FULL_DIR = DATA_DIR / "fulltext"
ABS_DIR = DATA_DIR / "abs"
PDF_DIR = DATA_DIR / "pdf"
TEXT_DIR = DATA_DIR / "text"
PDF_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)

selected = json.loads((DATA_DIR / "selected.json").read_text())


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
        self.skip_tags = {"script", "style"}
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip > 0:
            self.skip -= 1
    def handle_data(self, data):
        if self.skip == 0:
            self.parts.append(data)


def html_to_text(html):
    p = TextExtractor()
    try:
        p.feed(html)
    except Exception:
        pass
    text = " ".join(p.parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_institutions(html, abs_html):
    """Extract institutions from arxiv HTML5 (preferred) or abs page."""
    insts = []

    if html:
        # arxiv HTML5: look for <span class="ltx_role_affiliation"> or class="ltx_personname"
        # Affiliations often in <div class="ltx_authors"> blocks
        m = re.findall(r'<span[^>]*class="[^"]*ltx_role_affiliation[^"]*"[^>]*>(.*?)</span>',
                       html, re.S | re.I)
        for it in m:
            txt = re.sub(r"<[^>]+>", " ", it)
            txt = re.sub(r"\s+", " ", txt).strip()
            if txt and txt not in insts:
                insts.append(txt)
        # Some papers use <div class="ltx_personname"> with <a href="mailto:...@xxx.edu">
        if not insts:
            m = re.findall(r'<div[^>]*class="[^"]*ltx_role_institution[^"]*"[^>]*>(.*?)</div>',
                           html, re.S | re.I)
            for it in m:
                txt = re.sub(r"<[^>]+>", " ", it)
                txt = re.sub(r"\s+", " ", txt).strip()
                if txt and txt not in insts:
                    insts.append(txt)

    if not insts and abs_html:
        # Fallback: look for keywords in abs page (rare to have affil)
        pass

    return insts


for sec, aid in selected:
    out_path = TEXT_DIR / f"{aid}.json"
    html_path = FULL_DIR / f"{aid}.html"
    abs_path = ABS_DIR / f"{aid}.html"
    html = html_path.read_text(encoding="utf-8", errors="ignore") if html_path.exists() else ""
    abs_html = abs_path.read_text(encoding="utf-8", errors="ignore") if abs_path.exists() else ""

    text = ""
    if html:
        text = html_to_text(html)
    insts = extract_institutions(html, abs_html) if html else []

    out = {
        "id": aid,
        "section": sec,
        "fulltext": text,
        "fulltext_len": len(text),
        "institutions": insts,
        "html_available": bool(html),
    }
    out_path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"  {aid} [{sec}] text_len={len(text):,} insts={insts[:5]}")

print("Done.")
