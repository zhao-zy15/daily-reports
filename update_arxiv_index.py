import re
from datetime import datetime

file_path = "/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-papers/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update Latest Report
# Current: <div class="title">2026-03-23</div>
content = re.sub(r'<div class="title">.*?</div>', '<div class="title">2026-03-24</div>', content)
# Current: <a href="report-2026-03-23.html" class="btn">
content = re.sub(r'<a href="report-[0-9\-]+.html" class="btn">', '<a href="report-2026-03-24.html" class="btn">', content)

# Inject to History
new_history = """                <li>
                    <a href="report-2026-03-24.html">
                        <div class="date-info">
                            <span class="date">2026-03-24</span>
                            <span class="weekday">周二</span>
                        </div>
                        <span class="paper-count">12 篇论文</span>
                    </a>
                </li>\n"""
content = content.replace('<ul class="history-list">\n', '<ul class="history-list">\n' + new_history)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully.")
