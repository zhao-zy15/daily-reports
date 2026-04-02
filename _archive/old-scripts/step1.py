import json

with open("selected_10.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

# Group papers
groups = {}
for p in papers:
    cat = p.get("category", "Uncategorized")
    if cat not in groups:
        groups[cat] = []
    groups[cat].append(p)

date_str = "2026-03-20"
report_path = f"/Users/seanzyzhao/WorkBuddy/daily-reports/arxiv-papers/report-{date_str}.html"

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>arXiv 顶级论文深度追踪报告 - {date_str}</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; padding: 20px; max-width: 1200px; margin: auto; background: #f8f9fa; color: #333; }}
h1 {{ color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 30px; }}
h2 {{ color: #2980b9; margin-top: 50px; border-bottom: 2px solid #bdc3c7; padding-bottom: 5px; }}
h3 {{ color: #e67e22; margin-top: 30px; }}
.toc {{ background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 50px; border-left: 5px solid #2980b9; }}
.toc ul {{ list-style-type: none; padding-left: 0; }}
.toc li {{ margin-bottom: 12px; font-size: 1.1em; }}
.toc a {{ text-decoration: none; color: #34495e; transition: color 0.3s; }}
.toc a:hover {{ color: #3498db; font-weight: bold; }}
.category-title {{ font-weight: bold; color: #8e44ad; font-size: 1.2em; margin-top: 15px; margin-bottom: 10px; }}
.paper-card {{ background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); margin-bottom: 40px; transition: transform 0.2s; }}
.paper-card:hover {{ transform: translateY(-5px); }}
.paper-title {{ font-size: 1.8em; font-weight: bold; color: #2c3e50; margin-bottom: 15px; line-height: 1.3; }}
.paper-meta {{ font-size: 0.95em; color: #7f8c8d; margin-bottom: 25px; display: flex; flex-wrap: wrap; gap: 15px; }}
.paper-meta span {{ background: #ecf0f1; padding: 5px 10px; border-radius: 4px; }}
.paper-meta a {{ color: #2980b9; text-decoration: none; }}
.paper-meta a:hover {{ text-decoration: underline; }}
.section-title {{ font-weight: bold; color: #34495e; margin-top: 25px; font-size: 1.3em; border-left: 4px solid #e74c3c; padding-left: 10px; }}
.content-text {{ margin-top: 10px; font-size: 1.05em; color: #444; }}
.example-box {{ background: #fdfefe; border: 1px solid #dcdde1; border-left: 5px solid #27ae60; padding: 20px; margin: 20px 0; border-radius: 6px; }}
.example-box strong {{ color: #2c3e50; }}
.example-box ol, .example-box ul {{ margin-top: 15px; padding-left: 25px; margin-bottom: 0; }}
.example-box li {{ margin-bottom: 10px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
th, td {{ border: 1px solid #bdc3c7; padding: 15px; text-align: center; }}
th {{ background-color: #f2f6f8; color: #2c3e50; font-weight: bold; }}
tr:nth-child(even) {{ background-color: #f9fbfb; }}
.ablation {{ background: #fff3e0; padding: 15px; border-radius: 6px; border-left: 4px solid #e67e22; margin-top: 20px; }}
</style>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

<h1>arXiv AI 顶级论文深度追踪报告 ({date_str})</h1>

<div class="toc">
    <h2>今日论文方向导航 (TOC)</h2>
"""

for cat, lst in groups.items():
    html += f"    <div class='category-title'>📌 {cat}</div>\n    <ul>\n"
    for i, p in enumerate(lst):
        html += f"        <li><a href='#paper-{p['title'][:10].replace(' ', '-')}'>[{i+1}] {p['title']}</a></li>\n"
    html += "    </ul>\n"

html += "</div>\n\n"

with open(report_path, "w", encoding="utf-8") as f:
    f.write(html)
