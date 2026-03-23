import json
from datetime import datetime

with open('yf_data.json', 'r') as f:
    market_data = json.load(f)

with open('news_out.json', 'r') as f:
    news_items = json.load(f)

military_news = []
diplomatic_news = []
keywords_military = ['strike', 'war', 'attack', 'military', 'missile', 'forces', 'kill', 'retaliate']

for n in news_items:
    title = n['title'].lower()
    if any(k in title for k in ['madrid', 'cuba', 'ukraine', 'shutdown', 'vinicius']):
        continue
    if any(k in title for k in keywords_military) or any(k in n['summary'].lower() for k in keywords_military):
        military_news.append(n)
    else:
        diplomatic_news.append(n)

news_html = "<h3>⚔️ 军事冲突与战场动态</h3><ul>"
for n in military_news:
    news_html += f"<li><a href='{n['link']}' target='_blank'><strong>{n['title']}</strong></a> - {n['summary']} ({n['pubDate']})</li>"
news_html += "</ul><h3>🌐 国际社会与各方表态</h3><ul>"
for n in diplomatic_news:
    news_html += f"<li><a href='{n['link']}' target='_blank'><strong>{n['title']}</strong></a> - {n['summary']} ({n['pubDate']})</li>"
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
                label: 'Brent 过去10个交易日',
                data: {json.dumps(brent_closes)},
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
                tension: 0.1
            }}, {{
                label: 'WTI 过去10个交易日',
                data: {json.dumps(wti_closes)},
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
                tension: 0.1
            }}]
        }},
        options: {{ responsive: true, plugins: {{ title: {{ display: true, text: '原油(Brent & WTI)' }} }} }}
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
                        label: '{asset} 过去10个交易日',
                        data: {json.dumps(data['closes'])},
                        borderColor: '{color}',
                        fill: false,
                        tension: 0.1
                    }}]
                }},
                options: {{ responsive: true, plugins: {{ title: {{ display: true, text: '{title}' }} }} }}
            }});
        </script>
        """

market_table = "<table border='1' style='width:100%; text-align:center; border-collapse: collapse; margin-bottom: 30px;'><tr><th>资产</th><th>最新价格</th></tr>"
for asset in ['Brent', 'WTI', 'Natural Gas', 'Gold', 'Silver', 'S&P 500', 'USD/IRR', 'USD/CNY']:
    price = market_data.get(asset, {}).get('latest', 'N/A')
    market_table += f"<tr><td>{asset}</td><td>{price}</td></tr>"
market_table += "</table>"

now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
file_name = f"report-{datetime.now().strftime('%Y-%m-%d-%H%M')}.html"

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
        th, td {{ padding: 10px; border: 1px solid #ddd; }}
        th {{ background-color: #f4f4f4; }}
        .charts-container {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
    </style>
</head>
<body>
    <h1>🌍 伊朗局势与大宗商品日报</h1>
    <p><strong>生成时间：</strong> {now_str}</p>
    
    <h2>📰 过去24小时中东局势追踪</h2>
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

with open(f"iran-commodity/{file_name}", "w") as f:
    f.write(html_content)

print(f"Generated {file_name}")
