"""Improved institution extractor + PDF fallback for missing papers."""
import json
import re
import urllib.request
import time
import subprocess
from pathlib import Path
from html.parser import HTMLParser

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
FULL_DIR = DATA_DIR / "fulltext"
ABS_DIR = DATA_DIR / "abs"
PDF_DIR = DATA_DIR / "pdf"
TEXT_DIR = DATA_DIR / "text"
PDF_DIR.mkdir(parents=True, exist_ok=True)

selected = json.loads((DATA_DIR / "selected.json").read_text())

# Download PDFs for papers without HTML
NEED_PDF = ["2605.12227", "2605.12361", "2605.11814"]
UA = {"User-Agent": "Mozilla/5.0 (compatible; arxiv-fetcher)"}
for aid in NEED_PDF:
    pdf_path = PDF_DIR / f"{aid}.pdf"
    if pdf_path.exists():
        continue
    try:
        url = f"https://arxiv.org/pdf/{aid}"
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=120).read()
        pdf_path.write_bytes(r)
        print(f"  PDF {aid}: {len(r):,} bytes")
    except Exception as e:
        print(f"  PDF {aid} FAIL: {e}")
    time.sleep(2)

# Extract PDF text using pdftotext if available
for aid in NEED_PDF:
    pdf_path = PDF_DIR / f"{aid}.pdf"
    txt_path = PDF_DIR / f"{aid}.txt"
    if pdf_path.exists() and not txt_path.exists():
        try:
            subprocess.run(["pdftotext", "-layout", str(pdf_path), str(txt_path)],
                           check=True, capture_output=True)
            print(f"  txt {aid}: extracted via pdftotext, {txt_path.stat().st_size:,} bytes")
        except FileNotFoundError:
            print("  pdftotext not found, trying pypdf")
            try:
                import pypdf
                reader = pypdf.PdfReader(str(pdf_path))
                text = "\n".join(p.extract_text() or "" for p in reader.pages)
                txt_path.write_text(text, encoding="utf-8")
                print(f"  txt {aid}: extracted via pypdf, {len(text):,} chars")
            except Exception as e2:
                print(f"  pdf->text {aid} FAIL: {e2}")
        except Exception as e:
            print(f"  pdf->text {aid} FAIL: {e}")


def extract_institutions_v2(html):
    """Extract institutions from arxiv HTML5 ltx_personname / ltx_authors block."""
    insts = []
    # Find authors block
    m = re.search(r'<div class="ltx_authors">(.*?)</div>', html, re.S | re.I)
    if not m:
        return []
    block = m.group(1)
    # Extract texts after <sup> markers (institution numbering)
    # Each affiliation: <sup>N</sup>InstitutionName<br...>
    # Use pattern: </sup>([^<]+?)(?:<br|<span class="ltx_text ltx_font_typewriter")
    # First, replace <br> with newlines
    block_lines = re.sub(r'<br[^>]*>', '\n', block)
    # Strip tags after this point but split per line
    lines = block_lines.split('\n')
    for line in lines:
        # remove all tags
        clean = re.sub(r'<[^>]+>', ' ', line)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if not clean:
            continue
        # if starts with a number/superscript and has institutional keywords
        # Heuristic: contains "University", "Institute", "Lab", "Inc", "Research",
        # "School", "College", company names
        if re.search(r'(University|Institute|Lab|Laborator|Inc\.|Research|School|College|Universit[èé]|Tsinghua|Peking|MIT|Stanford|Berkeley|Microsoft|Google|DeepMind|Meta|OpenAI|Tencent|Alibaba|Baidu|Huawei|ByteDance|Apple|NVIDIA|IBM|Amazon|DeepSeek|Qwen|Anthropic|Hunyuan|Seed)', clean, re.I):
            # Strip leading numbers, commas
            clean = re.sub(r'^[\d\,\.\s\*†‡§¶]+', '', clean).strip()
            # Skip if too long (probably whole abstract)
            if len(clean) < 200 and clean not in insts:
                insts.append(clean)
    return insts


# Re-extract institutions for HTML papers + handle PDF for missing ones
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip > 0:
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


def extract_pdf_institutions(text):
    """Heuristic extraction from PDF text first page."""
    insts = []
    # Take first 3000 chars (title + authors + affil)
    head = text[:3000]
    lines = head.split("\n")
    for line in lines:
        clean = line.strip()
        if not clean or len(clean) > 200:
            continue
        if re.search(r'(University|Institute|Lab|Laborator|Inc\.|Research|School|College|Tsinghua|Peking|MIT|Stanford|Berkeley|Microsoft|Google|DeepMind|Meta|OpenAI|Tencent|Alibaba|Baidu|Huawei|ByteDance|Apple|NVIDIA|IBM|Amazon|DeepSeek|Qwen|Anthropic|Hunyuan|Seed|Hospital|Medical Center)', clean, re.I):
            # Cleanup
            clean = re.sub(r'^[\d\,\.\s\*†‡§¶]+', '', clean).strip()
            clean = re.sub(r'^\d+\s*', '', clean).strip()
            if 5 < len(clean) < 150 and clean not in insts:
                insts.append(clean)
    return insts


for sec, aid in selected:
    html_path = FULL_DIR / f"{aid}.html"
    pdf_text_path = PDF_DIR / f"{aid}.txt"

    text = ""
    insts = []
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8", errors="ignore")
        text = html_to_text(html)
        insts = extract_institutions_v2(html)
    if pdf_text_path.exists():
        pdf_text = pdf_text_path.read_text(encoding="utf-8", errors="ignore")
        if not text:
            text = pdf_text
        if not insts:
            insts = extract_pdf_institutions(pdf_text)

    out = {
        "id": aid,
        "section": sec,
        "fulltext": text,
        "fulltext_len": len(text),
        "institutions": insts,
    }
    (TEXT_DIR / f"{aid}.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(f"  {aid} [{sec}] len={len(text):,}  insts={insts[:5]}")

print("Done.")
