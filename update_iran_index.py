import re

html_file = "/Users/seanzyzhao/WorkBuddy/daily-reports/iran-commodity/index.html"
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Latest Report
content = re.sub(
    r'<div class="title">.*?</div>',
    '<div class="title">2026-03-24 14:25</div>',
    content, count=1
)
content = re.sub(
    r'<a href="report-2026-03-23-1054.html" class="btn">',
    '<a href="report-2026-03-24-1425.html" class="btn">',
    content, count=1
)

# Prepend to history list
new_item = """                <li>
                    <a href="report-2026-03-24-1425.html">
                        <div class="date-info">
                            <span class="date">2026-03-24</span>
                            <span class="weekday">周二</span>
                        </div>
                        <span class="time">14:25</span>
                    </a>
                </li>\n"""

content = re.sub(
    r'<ul class="history-list">',
    '<ul class="history-list">\n' + new_item,
    content, count=1
)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")
