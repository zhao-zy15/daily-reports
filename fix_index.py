import re

html_file = "/Users/seanzyzhao/WorkBuddy/daily-reports/tech-news/index.html"
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the history list entirely to remove the duplicates
new_history = """            <ul class="history-list">
                <li>
                    <a href="report-2026-03-23.html">
                        <div class="date-info">
                            <span class="date">2026-03-23</span>
                            <span class="weekday">全领域版</span>
                        </div>
                        <span class="summary">20+ 深度追踪：大模型、脑机、具身智能等七大垂直赛道</span>
                    </a>
                </li>
                <li>
                    <a href="report-2026-03-19.html">
                        <div class="date-info">
                            <span class="date">2026-03-19</span>
                            <span class="weekday">周四</span>
                        </div>
                        <span class="summary">英伟达营收预期破400亿 / 苹果AI iPhone发力 / Kimi估值200亿</span>
                    </a>
                </li>
            </ul>"""

content = re.sub(r'<ul class="history-list">.*?</ul>', new_history, content, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")
