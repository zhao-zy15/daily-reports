import json
from datetime import datetime

with open('yf_data.json', 'r') as f:
    market_data = json.load(f)

with open('news_zh.json', 'r') as f:
    news_items = json.load(f)

news_html = ""

# 1. 核心焦点 (Detailed)
news_html += "<h3>🔴 核心焦点新闻</h3><div style='display:flex; flex-direction:column; gap:15px; margin-bottom: 25px;'>"
for n in news_items['focus']:
    news_html += f"<div style='background:#fff0f0; padding:15px; border-left:5px solid #ef4444; border-radius:6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>"
    news_html += f"<a href='{n['link']}' target='_blank' style='font-size:1.15em; color:#b91c1c;'><strong>{n['title']}</strong></a>"
    news_html += f"<div style='margin-top:10px; color:#333; line-height:1.6;'>{n['summary']}</div>"
    news_html += f"<div style='margin-top:8px; font-size:0.85em; color:#666;'>发布时间：{n['date']}</div>"
    news_html += "</div>"
news_html += "</div>"

# 2. 地区动态 (Brief)
news_html += "<h3>⚡ 周边冲突与地区动态</h3><ul style='margin-bottom: 25px; padding-left: 20px; line-height: 1.8;'>"
for n in news_items['regional']:
    news_html += f"<li style='margin-bottom:12px;'><a href='{n['link']}' target='_blank'><strong>{n['title']}</strong></a>：<span style='color:#555;'>{n['summary']}</span></li>"
news_html += "</ul>"

# 3. 国际反响 (Brief)
news_html += "<h3>🌍 国际视野与社会反响</h3><ul style='margin-bottom: 25px; padding-left: 20px; line-height: 1.8;'>"
for n in news_items['global']:
    news_html += f"<li style='margin-bottom:12px;'><a href='{n['link']}' target='_blank'><strong>{n['title']}</strong></a>：<span style='color:#555;'>{n['summary']}</span></li>"
news_html += "</ul>"

crude_dates = market_data.get('Brent', {}).get('dates', [])
brent_closes = market_data.get('Brent', {}).get('closes', [])
wti_closes = market_data.get('WTI', {}).get('closes', [])

charts_html = f"""
<div style="width: 48%; margin-bottom: 20px;">
    <canvas id="chartCrude"></canvas>
</div>
<script>
    new Chart(document.getElementById('chartCrude'), {{
        type: 'line',
        data: {{
            labels: {json.dumps(crude_dates)},
            datasets: [{{
                label: 'Brent 原油 (10日收盘价)',
                data: {json.dumps(brent_closes)},
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
                tension: 0.1
            }}, {{
                label: 'WTI 原油 (10日收盘价)',
                data: {json.dumps(wti_closes)},
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
                tension: 0.1
            }}]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: '原油价格双线走势 (Brent & WTI)' }} }} }}
    }});
</script>
"""

for asset, color, title in [('Natural Gas', 'rgba(75, 192, 192, 1)', '天然气'), ('Gold', 'rgba(255, 206, 86, 1)', '黄金'), ('Silver', 'rgba(153, 102, 255, 1)', '白银')]:
    data = market_data.get(asset, {})
    if 'dates' in data:
        charts_html += f"""
        <div style="width: 48%; margin-bottom: 20px;">
            <canvas id="chart{asset.replace(' ', '')}"></canvas>
        </div>
        <script>
            new Chart(document.getElementById('chart{asset.replace(' ', '')}'), {{
                type: 'line',
                data: {{
                    labels: {json.dumps(data['dates'])},
                    datasets: [{{
                        label: '{asset} (10日收盘价)',
                        data: {json.dumps(data['closes'])},
                        borderColor: '{color}',
                        fill: false,
                        tension: 0.1
                    }}]
                }},
                options: {{ responsive: true, plugins: {{ title: {{ display: true, text: '{title}价格走势' }} }} }}
            }});
        </script>
        """

market_table = "<table border='1' style='width:100%; text-align:center; border-collapse: collapse; margin-bottom: 30px;'><tr><th>资产类别</th><th>最新报价</th></tr>"
for asset in ['Brent', 'WTI', 'Natural Gas', 'Gold', 'Silver', 'S&P 500', 'USD/IRR', 'USD/CNY']:
    price = market_data.get(asset, {}).get('latest', 'N/A')
    market_table += f"<tr><td>{asset}</td><td>{price}</td></tr>"
market_table += "</table>"

now_str = "2026-03-24 14:25"
file_name = "report-2026-03-24-1425.html"

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>伊朗局势与大宗商品日报 - {now_str}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
        h1, h2, h3 {{ color: #0056b3; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        th, td {{ padding: 12px; border: 1px solid #ddd; }}
        th {{ background-color: #f4f4f4; color: #333; }}
        .charts-container {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
    </style>
</head>
<body>
    <h1>🌍 伊朗局势与大宗商品日报</h1>
    <p style="color: #666;"><strong>生成时间：</strong> {now_str}</p>
    
    <h2>📰 过去24小时中东局势深度追踪</h2>
    {news_html}

    <h2>📈 核心资产最新报价</h2>
    {market_table}

    <h2>📊 大宗商品10日走势分析 (独立折线图)</h2>
    <div class="charts-container">
        {charts_html}
    </div>
</body>
</html>
"""

with open(f"iran-commodity/{file_name}", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {file_name}")
