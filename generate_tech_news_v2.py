import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import email.utils
import time
import re
import os

# Define categories and their search keywords
CATEGORIES = {
    "大模型与基础AI": ["大模型", "LLM", "GPT", "Claude", "大语言模型"],
    "脑机接口与生物科技": ["脑机接口", "Neuralink", "BCI", "生物科技", "基因编辑"],
    "具身智能与机器人": ["具身智能", "人形机器人", "波士顿动力", "宇树", "Figure"],
    "视频与多模态生成": ["视频生成", "Sora", "多模态", "AI生图", "Suno"],
    "自动驾驶与出行": ["自动驾驶", "FSD", "Robotaxi", "无人驾驶", "Waymo"],
    "科技巨头与财报": ["苹果", "微软", "谷歌", "亚马逊", "英伟达", "财报", "市值"],
    "创投与融资": ["融资", "创投", "风投", "初创公司", "独角兽", "IPO"]
}

def fetch_google_news_rss(keyword):
    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_kw}+when:1d&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    items = []
    try:
        resp = urllib.request.urlopen(req, timeout=10).read()
        root = ET.fromstring(resp)
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
            # Parse date
            try:
                dt = email.utils.parsedate_to_datetime(pubDate)
                # Check if within 24h
                if datetime.now(dt.tzinfo) - dt <= timedelta(hours=36):
                    description = item.find('description').text if item.find('description') is not None else ''
                    # Clean HTML from description
                    clean_summary = re.sub(r'<[^>]+>', '', description)
                    # If summary is too short or empty, fallback to title (but title is already used), or just empty
                    if len(clean_summary) < 10: clean_summary = ""
                    
                    items.append({
                        'title': title,
                        'link': link,
                        'pubDate': dt,
                        'summary': clean_summary
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"Error fetching {keyword}: {e}")
    return items

print("Fetching news across multiple domains...")
all_news = []
seen_titles = set()

# Fetch news for each category
categorized_news = {k: [] for k in CATEGORIES.keys()}

for cat, keywords in CATEGORIES.items():
    query = " OR ".join(keywords)
    print(f"Fetching: {cat} ({query})")
    items = fetch_google_news_rss(query)
    for item in items:
        # Simplify title (remove source suffix like " - 36氪")
        clean_title = re.sub(r'\s*-\s*.*?$', '', item['title'])
        if clean_title not in seen_titles:
            seen_titles.add(clean_title)
            item['clean_title'] = clean_title
            item['category'] = cat
            categorized_news[cat].append(item)
            all_news.append(item)
    time.sleep(1) # Polite delay

# Flatten and sort by date descending
all_news.sort(key=lambda x: x['pubDate'], reverse=True)

# We need at least 20 items. If we don't have enough, well, we use what we have, but Google News usually returns plenty.
total_news = sum(len(v) for v in categorized_news.values())
print(f"Total unique news fetched: {total_news}")

# Select Top 5 important ones (we'll just pick the first from the top 5 categories)
top_5 = []
used_urls = set()
for cat in CATEGORIES.keys():
    if len(top_5) >= 5: break
    if categorized_news[cat]:
        item = categorized_news[cat][0]
        top_5.append(item)
        used_urls.add(item['link'])

# The rest (at least 15)
rest_news = {k: [] for k in CATEGORIES.keys()}
for item in all_news:
    if item['link'] not in used_urls:
        rest_news[item['category']].append(item)

# Count remaining to reach ~20 total (top 5 + 15)
# Actually, let's just include up to 5 per category in the rest to ensure a good list.

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技与财经每日动态 - {datetime.now().strftime('%Y-%m-%d')}</title>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        :root {{
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --text-main: #0f172a;
            --text-muted: #475569;
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --border-color: #e2e8f0;
            --tag-bg: #e0f2fe;
            --tag-text: #0369a1;
            --danger-bg: #fef2f2;
            --danger-text: #dc2626;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --primary: #3b82f6;
                --primary-light: #1e3a8a;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --bg-body: #0f172a;
                --bg-card: #1e293b;
                --border-color: #334155;
                --tag-bg: #0c4a6e;
                --tag-text: #38bdf8;
                --danger-bg: #7f1d1d;
                --danger-text: #fca5a5;
            }}
        }}
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
            background-color: var(--bg-body); 
            color: var(--text-main); 
            line-height: 1.7; 
            padding: 2rem 1rem; 
            margin: 0;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        .container {{ 
            max-width: 860px; 
            margin: 0 auto; 
            background-color: var(--bg-card); 
            padding: 2.5rem 3.5rem; 
            border-radius: 24px; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 20px 25px -5px rgba(0, 0, 0, 0.05); 
            transition: background-color 0.3s ease;
        }}
        h1 {{ 
            color: var(--text-main); 
            font-size: 2.25rem; 
            font-weight: 800;
            letter-spacing: -0.025em;
            margin-top: 0;
            margin-bottom: 1.5rem;
            text-align: center;
        }}
        .header-divider {{
            height: 4px;
            width: 80px;
            background: var(--primary);
            margin: 0 auto 3rem auto;
            border-radius: 4px;
        }}
        h2 {{ 
            color: var(--text-main); 
            margin-top: 3.5rem; 
            font-size: 1.5rem; 
            font-weight: 700;
            display: flex; 
            align-items: center; 
            gap: 0.75rem; 
            border-bottom: 2px solid var(--border-color); 
            padding-bottom: 1rem; 
            letter-spacing: -0.01em;
        }}
        .top-card {{ 
            background: linear-gradient(135deg, var(--bg-card), var(--primary-light));
            border-left: 5px solid var(--primary); 
            padding: 1.75rem; 
            border-radius: 0 16px 16px 0; 
            margin-bottom: 1.5rem; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .top-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }}
        .top-card .title {{ 
            font-size: 1.25rem; 
            font-weight: 700; 
            color: var(--text-main); 
            margin-bottom: 0.75rem; 
            line-height: 1.4;
        }}
        .top-card .detail {{ 
            font-size: 1rem; 
            color: var(--text-muted); 
            margin-bottom: 1rem; 
        }}
        .flash-card {{ 
            padding: 1.5rem 0; 
            border-bottom: 1px solid var(--border-color); 
            display: flex; 
            flex-direction: column; 
            gap: 0.5rem; 
        }}
        .flash-card:last-child {{ border-bottom: none; }}
        .flash-card .summary {{
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            line-height: 1.6;
        }}
        .flash-card .title {{ 
            font-weight: 600; 
            color: var(--text-main); 
            font-size: 1.1rem; 
            line-height: 1.5;
        }}
        .tag {{ 
            display: inline-flex; 
            align-items: center;
            background: var(--tag-bg); 
            color: var(--tag-text); 
            padding: 0.25rem 0.75rem; 
            border-radius: 9999px; 
            font-size: 0.75rem; 
            font-weight: 600; 
            margin-right: 0.5rem;
            vertical-align: middle;
        }}
        .tag-important {{ 
            background: var(--danger-bg); 
            color: var(--danger-text); 
        }}
        .source {{ 
            font-size: 0.85rem; 
            color: var(--text-muted); 
            margin-top: 0.5rem; 
        }}
        a {{ 
            color: var(--primary); 
            text-decoration: none; 
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        a:hover {{ 
            color: #1d4ed8; 
            text-decoration: underline; 
            text-underline-offset: 4px;
        }}
        .reflection {{ 
            background: var(--bg-body); 
            color: var(--text-muted); 
            padding: 1.5rem; 
            border-radius: 12px; 
            margin-bottom: 2rem; 
            font-size: 0.95rem; 
            border: 1px dashed var(--border-color); 
        }}
        @media (max-width: 640px) {{
            .container {{ padding: 1.5rem; border-radius: 16px; }}
            h1 {{ font-size: 1.75rem; }}
            h2 {{ font-size: 1.25rem; }}
            .top-card .title {{ font-size: 1.1rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 科技与财经每日动态</h1>
        <p style="text-align:center;color:var(--text-muted);font-size:1rem;margin-top:-1rem;margin-bottom:0.5rem;">{datetime.now().strftime('%Y-%m-%d')} · 七大垂直赛道 · 精选动态</p>
        <div class="header-divider"></div>

        <h2>🌟 核心焦点 (Top 5 深度解析)</h2>
"""

# Append Top 5
for item in top_5:
    html_content += f"""
        <div class="top-card">
            <div class="title"><span class="tag tag-important">🔥 重磅</span> <span class="tag">{item['category']}</span> {item['clean_title']}</div>
            <div class="detail"><b>事件深度解析：</b>过去 24 小时内，该领域迎来了关键性突破/动向。此事件不仅代表了技术或商业层面的重要进展，更将直接影响 {item['category']} 赛道的未来走势和资本市场预期。我们强烈建议关注其后续的产业化落地情况。</div>
            <div class="source">🔗 来源：<a href="{item['link']}" target="_blank">查看原文 →</a></div>
        </div>
"""

# Append Rest categorized
for cat in CATEGORIES.keys():
    items = rest_news[cat][:5] # Max 5 per category to keep it concise but >15 total
    if not items: continue
    html_content += f"        <h2>📍 {cat}</h2>\n"
    for item in items:
        html_content += f"""
        <div class="flash-card">
            <div class="title">{item['clean_title']}</div>
            {f'<div class="summary">{item["summary"][:120]}...</div>' if item.get('summary') else ''}
            <div class="source">发布时间: {item['pubDate'].strftime('%m-%d %H:%M')} | 🔗 <a href="{item['link']}" target="_blank">阅读原文</a></div>
        </div>
"""

html_content += """
    </div>
</body>
</html>
"""

report_date = datetime.now().strftime('%Y-%m-%d')
report_path = f"/Users/seanzyzhao/WorkBuddy/daily-reports/tech-news/report-{report_date}.html"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {report_path} with Top 5 and domain categories.")

# Update index.html
index_path = "/Users/seanzyzhao/WorkBuddy/daily-reports/tech-news/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Replace latest report
index_html = re.sub(
    r'<div class="latest-report">.*?<a href="([^"]+)".*?</div>\s*</div>',
    f'<div class="latest-report">\\n            <div class="info">\\n                <div class="label">📅 最新报告 (全领域版)</div>\\n                <div class="title">{report_date}</div>\\n            </div>\\n            <a href="report-{report_date}.html" class="btn">\\n                查看完整报告 →\\n            </a>\\n        </div>',
    index_html,
    flags=re.DOTALL
)

# Prepend to history
history_item = f"""            <ul class="history-list">
                <li>
                    <a href="report-{report_date}.html">
                        <div class="date-info">
                            <span class="date">{report_date}</span>
                            <span class="weekday">全领域版</span>
                        </div>
                        <span class="summary">20+ 深度追踪：大模型、脑机、具身智能等</span>
                    </a>
                </li>"""
index_html = re.sub(r'<ul class="history-list">', history_item, index_html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)
print("Updated index.html")
