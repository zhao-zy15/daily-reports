"""Extract institutions from PDF first page."""
import json
import re
from pathlib import Path
from pypdf import PdfReader

DATE = "2026-05-15"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")
PDF_DIR = DATA_DIR / "pdfs"

verified = json.loads((DATA_DIR / "verified.json").read_text())

# Common institution patterns
INST_KEYWORDS = [
    "University", "Institute", "Lab", "Laboratory", "College", "School",
    "Research", "Corporation", "Inc", "Ltd", "AI", "Microsoft", "Google",
    "OpenAI", "DeepMind", "Meta", "Apple", "Amazon", "Adobe", "NVIDIA",
    "Tencent", "Alibaba", "Baidu", "ByteDance", "Huawei", "Anthropic",
    "Hospital", "Medical Center", "Clinic", "Health", "Academy",
    "CNRS", "INRIA", "MIT", "ETH", "EPFL", "CMU", "Stanford", "Berkeley"
]


def extract_insts_from_page1(pdf_path):
    try:
        reader = PdfReader(str(pdf_path))
        if len(reader.pages) == 0:
            return []
        text = reader.pages[0].extract_text() or ""
        # Split by lines
        lines = text.split("\n")
        # Find lines that contain institution keywords, in the first 40 lines
        candidates = []
        for line in lines[:60]:
            line = line.strip()
            if len(line) < 4 or len(line) > 200:
                continue
            # Skip pure numbers, all caps single words, etc.
            if re.match(r"^[\d\s\.,;:]+$", line):
                continue
            if any(kw.lower() in line.lower() for kw in INST_KEYWORDS):
                # Clean up
                line = re.sub(r"^\d+\s*", "", line)  # leading numbers (footnote markers)
                line = re.sub(r"\s+", " ", line).strip()
                if line and line not in candidates:
                    candidates.append(line)
        return candidates
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


for p in verified:
    aid = p["id"]
    pdf = PDF_DIR / f"{aid}.pdf"
    print(f"\n{aid}: {p['title'][:60]}")
    insts = extract_insts_from_page1(pdf)
    for inst in insts[:8]:
        print(f"  - {inst}")
    p["candidate_insts"] = insts

(DATA_DIR / "verified.json").write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nUpdated verified.json with candidate institutions")
