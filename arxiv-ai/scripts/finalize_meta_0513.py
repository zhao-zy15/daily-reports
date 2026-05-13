"""Build final paper metadata with verified institutions."""
import json
from pathlib import Path

DATE = "2026-05-13"
DATA_DIR = Path(f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-ai/data/{DATE}")

# Manually verified institutions (after extraction + cross-check)
INSTITUTIONS = {
    "2605.11478": ["POSTECH"],
    "2605.11744": ["Inner Mongolia University"],
    "2605.12466": ["University of Southern California"],
    "2605.11262": ["University of Michigan"],
    "2605.11461": ["Sun Yat-sen University"],
    "2605.12227": ["Instituto Superior Técnico", "Instituto de Telecomunicações", "ELLIS Unit Lisbon"],
    "2605.11403": ["OPPO AI Center"],
    "2605.11467": ["Intuit"],
    "2605.11169": ["UC San Diego", "UIUC", "Adobe Research"],
    "2605.11556": ["Tsinghua University"],
    "2605.12361": ["National Library of Medicine (NIH)", "UIUC", "University of Michigan Medical School"],
    "2605.11814": ["Zhejiang University", "Ant Group", "Alibaba Group"],
    "2605.11629": ["Alibaba Group"],
}

verified = json.loads((DATA_DIR / "verified.json").read_text())

# Combine into final metadata
final = {}
for aid, meta in verified.items():
    final[aid] = {
        **meta,
        "institutions": INSTITUTIONS.get(aid, []),
    }

(DATA_DIR / "final_meta.json").write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(final)} papers to final_meta.json")
for aid, m in final.items():
    print(f"  {aid}: {m['institutions']}")
