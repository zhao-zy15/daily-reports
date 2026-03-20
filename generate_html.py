import json
import datetime
import os

with open("selected_10.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

date_str = "2026-03-20"
report_path = f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-papers/report-{date_str}.html"

# Group by category
grouped = {}
for p in papers:
    cat = p["category"]
    if cat not in grouped:
        grouped[cat] = []
    grouped[cat].append(p)

# We define the mapping of deep content manually below.
deep_contents = {
    # We will populate this with the rich HTML strings
}
