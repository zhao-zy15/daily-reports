import re

file_path = "/Users/seanzyzhao/WorkBuddy/daily-reports/iran-commodity/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update Latest Report
content = re.sub(r'(<div class="label">📅 最新报告</div>\s*<div class="title">).*?(</div>)', r'\g<1>2026-03-20 19:30\g<2>', content)
content = re.sub(r'(<a href=")report-.*?\.(html" class="btn">)', r'\g<1>report-2026-03-20-1930.\g<2>', content)

# Inject to History
new_history = """                <li>
                    <a href="report-2026-03-20-1930.html">
                        <div class="date-info">
                            <span class="date">2026-03-20</span>
                            <span class="weekday">周五</span>
                        </div>
                        <span class="time">19:30</span>
                    </a>
                </li>\n"""
content = content.replace('<ul class="history-list">', '<ul class="history-list">\n' + new_history)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully.")
