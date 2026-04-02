import re

# 1. Update generate_tech_news_v2.py
gen_file = "/Users/seanzyzhao/WorkBuddy/daily-reports/generate_tech_news_v2.py"
with open(gen_file, 'r', encoding='utf-8') as f:
    gen_content = f.read()

new_style_gen = """    <style>
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
    </style>"""

# Replace style block
gen_content = re.sub(r'<style>.*?</style>', new_style_gen, gen_content, flags=re.DOTALL)

# Add header-divider
if '<div class="header-divider"></div>' not in gen_content:
    gen_content = re.sub(r'(<h1>.*?</h1>)', r'\1\n        <div class="header-divider"></div>', gen_content)

with open(gen_file, 'w', encoding='utf-8') as f:
    f.write(gen_content)

print("Updated generate_tech_news_v2.py")

# 2. Update tech-news/report-2026-03-23.html
report_file = "/Users/seanzyzhao/WorkBuddy/daily-reports/tech-news/report-2026-03-23.html"
with open(report_file, 'r', encoding='utf-8') as f:
    report_content = f.read()

# The same CSS but without double braces for the static HTML
new_style_html = new_style_gen.replace("{{", "{").replace("}}", "}")

report_content = re.sub(r'<style>.*?</style>', new_style_html, report_content, flags=re.DOTALL)

# Fix stripped attributes and classes
report_content = report_content.replace('lang="zhCN"', 'lang="zh-CN"')
report_content = report_content.replace('charset="UTF8"', 'charset="UTF-8"')
report_content = report_content.replace('name="viewport" content="width=devicewidth, initialscale=1.0"', 'name="viewport" content="width=device-width, initial-scale=1.0"')

report_content = report_content.replace('class="topcard"', 'class="top-card"')
report_content = report_content.replace('class="flashcard"', 'class="flash-card"')
report_content = report_content.replace('class="tag tagimportant"', 'class="tag tag-important"')

# Add header-divider if not exists
if '<div class="header-divider"></div>' not in report_content:
    report_content = re.sub(r'(<h1>.*?</h1>)', r'\1\n        <div class="header-divider"></div>', report_content)

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report_content)

print("Updated report-2026-03-23.html")
