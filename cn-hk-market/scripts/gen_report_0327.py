#!/usr/bin/env python3
"""Generate 2026-03-27 closing report for A-share & HK market."""

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A股港股收盘总结 · 2026年3月27日</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f0f2f5;--card:#fff;--text:#1a1a2e;--sub:#5a5a7a;
  --red:#dc2626;--green:#16a34a;--red-bg:rgba(220,38,38,.08);--green-bg:rgba(22,163,74,.08);
  --border:#e5e7eb;--accent:#2563eb;--accent-bg:rgba(37,99,235,.06);
  --gold:#d97706;--gold-bg:rgba(217,119,6,.06);
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#0a0a14;--card:#141422;--text:#e8e8f0;--sub:#8888a8;
    --red:#f87171;--green:#4ade80;--red-bg:rgba(248,113,113,.1);--green-bg:rgba(74,222,128,.1);
    --border:#2a2a3e;--accent:#60a5fa;--accent-bg:rgba(96,165,250,.08);
    --gold:#fbbf24;--gold-bg:rgba(251,191,36,.08);
  }
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
.container{max-width:960px;margin:0 auto;padding:20px 16px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.back{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;background:var(--card);border:1px solid var(--border);border-radius:8px;font-size:.9rem;margin-bottom:20px;transition:.2s}
.back:hover{background:var(--accent);color:#fff;border-color:var(--accent)}

/* Header */
.hero{background:linear-gradient(135deg,#1e3a5f,#0f172a);border-radius:16px;padding:32px;color:#fff;margin-bottom:24px;position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;top:-50%;right:-20%;width:300px;height:300px;background:radial-gradient(circle,rgba(59,130,246,.2),transparent);border-radius:50%}
.hero .date{font-size:.85rem;opacity:.7;letter-spacing:1px;text-transform:uppercase}
.hero h1{font-size:1.8rem;margin:8px 0;font-weight:800}
.hero .tagline{font-size:1rem;opacity:.85;margin-top:4px}
.hero .badge{display:inline-block;background:rgba(248,113,113,.25);color:#fca5a5;padding:4px 14px;border-radius:20px;font-size:.85rem;font-weight:600;margin-top:12px}
.hero .badge-green{background:rgba(74,222,128,.25);color:#86efac}

/* Cards */
.section{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;margin-bottom:20px}
.section-title{font-size:1.25rem;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.section-title .icon{font-size:1.3rem}

/* Tables */
table{width:100%;border-collapse:collapse;font-size:.9rem}
th{background:var(--accent-bg);color:var(--accent);font-weight:600;padding:10px 12px;text-align:left;border-bottom:2px solid var(--border)}
td{padding:10px 12px;border-bottom:1px solid var(--border)}
tr:last-child td{border-bottom:none}
.up{color:var(--red);font-weight:600}.down{color:var(--green);font-weight:600}
.up-bg{background:var(--red-bg)}.down-bg{background:var(--green-bg)}

/* Stock cards */
.stock-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin:16px 0}
.stock-card{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:14px;transition:.2s}
.stock-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.08)}
.stock-card .name{font-weight:700;font-size:.95rem;margin-bottom:4px}
.stock-card .code{font-size:.75rem;color:var(--sub)}
.stock-card .price{font-size:1.2rem;font-weight:800;margin:6px 0}
.stock-card .change{font-size:.85rem;font-weight:600;padding:2px 8px;border-radius:4px;display:inline-block}

/* Hot tags */
.hot-item{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px}
.hot-item .hot-title{font-weight:700;font-size:1.05rem;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.hot-item .hot-tag{font-size:.75rem;padding:2px 10px;border-radius:12px;font-weight:600}
.tag-policy{background:#dbeafe;color:#2563eb}
.tag-capital{background:#fef3c7;color:#d97706}
.tag-industry{background:#d1fae5;color:#059669}
.tag-earnings{background:#fce7f3;color:#db2777}

.detail{font-size:.9rem;color:var(--sub);margin:6px 0;line-height:1.6}
.detail strong{color:var(--text)}
.source{font-size:.78rem;color:var(--sub);margin-top:6px}
.source a{color:var(--accent);font-size:.78rem}

/* Commodity table */
.commodity-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:14px 0}
.commodity-item{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:12px;text-align:center}
.commodity-item .c-name{font-size:.85rem;color:var(--sub);margin-bottom:4px}
.commodity-item .c-price{font-size:1.1rem;font-weight:700}
.commodity-item .c-change{font-size:.82rem;font-weight:600;margin-top:2px}

/* Outlook */
.outlook-box{background:var(--gold-bg);border:1px solid var(--gold);border-radius:12px;padding:20px;margin:14px 0}
.outlook-box h4{color:var(--gold);margin-bottom:8px}
.outlook-box ul{margin-left:20px}
.outlook-box li{margin-bottom:6px;font-size:.92rem}

/* Trend cards */
.trend-grid{display:grid;grid-template-columns:1fr;gap:14px;margin:18px 0}
.trend-card{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:18px;position:relative;overflow:hidden}
.trend-card::before{content:'';position:absolute;top:0;left:0;width:4px;height:100%;border-radius:4px 0 0 4px}
.trend-card.bullish::before{background:var(--red)}.trend-card.bearish::before{background:var(--green)}.trend-card.neutral::before{background:var(--gold)}
.trend-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px}
.trend-name{font-weight:800;font-size:1.05rem}
.trend-badge{font-size:.78rem;padding:3px 12px;border-radius:16px;font-weight:700}
.badge-bull{background:var(--red-bg);color:var(--red)}.badge-bear{background:var(--green-bg);color:var(--green)}.badge-neutral{background:var(--gold-bg);color:var(--gold)}
.trend-metrics{display:flex;gap:16px;flex-wrap:wrap;margin:8px 0 10px;font-size:.85rem}
.trend-metrics span{display:flex;align-items:center;gap:4px}
.trend-metrics .label{color:var(--sub);font-weight:500}
.trend-metrics .value{font-weight:700}
.trend-analysis{font-size:.88rem;line-height:1.7;color:var(--sub)}
.trend-analysis strong{color:var(--text)}
.trend-stars{color:var(--gold);letter-spacing:2px;font-size:.9rem;margin-top:6px}

footer{text-align:center;padding:24px;color:var(--sub);font-size:.82rem}

@media(prefers-color-scheme:dark){
  .tag-policy{background:rgba(59,130,246,.15);color:#93c5fd}
  .tag-capital{background:rgba(217,119,6,.15);color:#fcd34d}
  .tag-industry{background:rgba(5,150,105,.15);color:#6ee7b7}
  .tag-earnings{background:rgba(219,39,119,.15);color:#f9a8d4}
}
@media(max-width:600px){
  .hero{padding:22px 18px}
  .hero h1{font-size:1.4rem}
  .stock-grid{grid-template-columns:1fr 1fr}
  .commodity-grid{grid-template-columns:1fr 1fr}
}
</style>
</head>
<body>
<div class="container">
<a href="index.html" class="back">← 返回报告列表</a>

<!-- ===== HERO ===== -->
<div class="hero">
  <div class="date">2026年3月27日 · 星期五 · 收盘总结</div>
  <h1>探底回升全线收红 · 宁德时代大涨3.4%领跑</h1>
  <div class="tagline">A股低开高走修复昨日跌幅，沪指重回3900上方，锂电医药双主线领涨</div>
  <span class="badge badge-green">🔺 反弹日 · 沪指+0.63% · 深成指+1.13%</span>
</div>

<!-- ===== 📈 大盘全景 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">📈</span>大盘全景概览</div>
  <table>
    <thead>
      <tr><th>指数</th><th>收盘点位</th><th>涨跌幅</th><th>备注</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>上证指数</strong></td><td>3,913.72</td><td class="up">+0.63%</td><td>重回3900上方</td></tr>
      <tr><td><strong>深证成指</strong></td><td>13,760.37</td><td class="up">+1.13%</td><td>反弹力度强于沪指</td></tr>
      <tr><td><strong>创业板指</strong></td><td>3,295.88</td><td class="up">+0.71%</td><td>成长股修复</td></tr>
      <tr><td><strong>科创50</strong></td><td>1,300.76</td><td class="up">+0.93%</td><td>科技方向企稳回升</td></tr>
      <tr><td><strong>中证500</strong></td><td>7,737.61</td><td class="up">+1.25%</td><td>中盘股涨幅领先</td></tr>
      <tr><td><strong>沪深300</strong></td><td>4,502.57</td><td class="up">+0.56%</td><td>权重股温和回暖</td></tr>
      <tr><td><strong>恒生指数</strong></td><td>24,951.88</td><td class="up">+0.38%</td><td>25000点拉锯战</td></tr>
      <tr><td><strong>恒生科技</strong></td><td>4,778.01</td><td class="up">+0.35%</td><td>科技股企稳反弹</td></tr>
    </tbody>
  </table>
  <div style="margin-top:14px;padding:14px;background:var(--bg);border-radius:10px">
    <p><strong>📊 成交与资金：</strong></p>
    <p>• 沪深两市成交额约 <strong>2.00万亿元</strong>，较前日温和回升，但仍处于近期低位</p>
    <p>• 市场呈现 <strong>"低开高走"</strong> 格局，探底回升修复昨日跌幅</p>
    <p>• 南向资金3/26净买入约 <strong>33亿港元</strong>，加仓中海油和快手，流出阿里巴巴</p>
    <p>• 港股市场恒指25000点反复拉锯，腾讯卖空量近期骤降</p>
  </div>
  <div class="source">数据来源：<a href="https://hq.sinajs.cn" target="_blank">新浪实时行情API</a> · <a href="https://hk.eastmoney.com" target="_blank">东方财富网</a> · <a href="https://finance.sina.com.cn/stock/hkstock/" target="_blank">新浪港股</a></div>
</div>

<!-- ===== ⭐ 自选追踪 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">⭐</span>专属自选追踪</div>
  
  <h4 style="margin-bottom:12px;font-size:1rem">📌 自选个股</h4>
  <div class="stock-grid">
    <div class="stock-card">
      <div class="name">腾讯控股</div><div class="code">0700.HK</div>
      <div class="price down">493.40</div>
      <div class="change down-bg down">-0.44%</div>
    </div>
    <div class="stock-card">
      <div class="name">阿里巴巴</div><div class="code">9988.HK</div>
      <div class="price down">122.60</div>
      <div class="change down-bg down">-0.33%</div>
    </div>
    <div class="stock-card">
      <div class="name">美团</div><div class="code">3690.HK</div>
      <div class="price down">85.90</div>
      <div class="change down-bg down">-0.92%</div>
    </div>
    <div class="stock-card">
      <div class="name">蜜雪冰城</div><div class="code">2097.HK</div>
      <div class="price down">286.00</div>
      <div class="change down-bg down">-4.86%</div>
    </div>
    <div class="stock-card">
      <div class="name">宁德时代</div><div class="code">300750.SZ</div>
      <div class="price up">416.18</div>
      <div class="change up-bg up">+3.40%</div>
    </div>
    <div class="stock-card">
      <div class="name">泡泡玛特</div><div class="code">9992.HK</div>
      <div class="price down">149.60</div>
      <div class="change down-bg down">-0.73%</div>
    </div>
    <div class="stock-card">
      <div class="name">小米集团</div><div class="code">1810.HK</div>
      <div class="price up">33.00</div>
      <div class="change up-bg up">+1.73%</div>
    </div>
    <div class="stock-card">
      <div class="name">快手</div><div class="code">1024.HK</div>
      <div class="price up">46.08</div>
      <div class="change up-bg up">+1.05%</div>
    </div>
    <div class="stock-card">
      <div class="name">优必选</div><div class="code">9880.HK</div>
      <div class="price up">91.00</div>
      <div class="change up-bg up">+0.28%</div>
    </div>
  </div>
</div>

<!-- ===== 🔥 板块热点复盘 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">🔥</span>板块热点复盘</div>
  
  <div class="hot-item">
    <div class="hot-title">锂电产业链持续走强 <span class="hot-tag tag-industry">产业</span></div>
    <div class="detail">
      <strong>锂电材料板块</strong>反复走强，电解液、隔膜、锂矿等多方向活跃。<strong>融捷股份</strong>实现3连板，石大胜华、丽岛新材、大东南等多股涨停。4月全行业排产预计环比继续增长，港股<strong>赣锋锂业涨超8%</strong>领涨锂电板块。华泰证券看好锂电和储能两大主线。
    </div>
    <div class="source">来源：<a href="https://www.cnenergynews.cn/article/4Qukm1otgoa" target="_blank">上海证券报</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">电力板块延续强势 <span class="hot-tag tag-industry">产业</span></div>
    <div class="detail">
      电力股持续活跃，<strong>湖南发展</strong>收获3连板。<strong>华电能源</strong>涨停报6.77元，3月以来累计涨幅已达148.9%。华电辽能盘中一度涨停，尾盘回落涨6.47%。算电协同、高油价推动新能源需求成为核心驱动力。
    </div>
    <div class="source">来源：<a href="https://paper.cnstock.com/html/2026-03/27/content_2192914.htm" target="_blank">上海证券报</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">医药创新药板块大涨 <span class="hot-tag tag-industry">产业</span></div>
    <div class="detail">
      港股创新药概念股集体走强。<strong>恒瑞医药(01276)涨超8%</strong>，去年营收和净利再创新高。<strong>爱康医疗(01789)再涨超8%</strong>，骨科手术机器人销售收入增速超200%。<strong>基石药业大涨超20%</strong>领跑港股医药股，受益于业绩拐点与出海红利。多款创新药将亮相下月AACR年会。
    </div>
    <div class="source">来源：<a href="https://finance.sina.com.cn/stock/hkstock/" target="_blank">新浪港股</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">CPO光通信冲高回落 <span class="hot-tag tag-capital">题材</span></div>
    <div class="detail">
      CPO概念盘中冲高回落。<strong>源杰科技</strong>盘中创历史新高1212.49元（总市值破千亿），但收盘微跌0.09%，年初至今累涨约77%。<strong>铭普光磁</strong>涨停，智立方涨近9%，天孚通信、长光华芯等活跃。
    </div>
    <div class="source">来源：<a href="https://paper.cnstock.com/html/2026-03/27/content_2192914.htm" target="_blank">上海证券报</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">调整板块：保险/光伏/贵金属 <span class="hot-tag tag-capital">调整</span></div>
    <div class="detail">
      <strong>保险、光伏设备、通信服务、软件开发、贵金属、多元金融</strong>等板块调整幅度居前。新消费板块延续疲软——蜜雪冰城-4.86%继续下探创新低，泡泡玛特再跌-0.73%（三日累跌超30%后暂获喘息）。
    </div>
  </div>
</div>

<!-- ===== 📰 盘中重大消息 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">📰</span>盘中重大消息</div>

  <div class="hot-item">
    <div class="hot-title">商务部对美启动两项贸易壁垒调查 <span class="hot-tag tag-policy">政策</span></div>
    <div class="detail">
      商务部宣布对美国启动两项贸易壁垒调查，进一步反制美方单边贸易措施。市场关注后续影响范围，短期对出口相关板块构成一定情绪扰动。
    </div>
    <div class="source">来源：<a href="https://hk.eastmoney.com" target="_blank">东方财富网</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">外交部回应"中芯国际向伊朗供货"传闻 <span class="hot-tag tag-policy">政策</span></div>
    <div class="detail">
      针对美官员称中芯国际向伊朗军方提供芯片制造工具一事，外交部正面回应。半导体板块盘中一度受扰动，但午后企稳回升。地缘政治风险持续为科技股定价。
    </div>
    <div class="source">来源：<a href="https://hk.eastmoney.com" target="_blank">东方财富网</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">蜜雪冰城换帅：35岁清华硕士接任CEO <span class="hot-tag tag-earnings">公司</span></div>
    <div class="detail">
      蜜雪集团公告创始人之一张红甫卸任CEO，35岁的前CFO张渊接任。2025年营收335.6亿元增35.2%、归母净利增33%，但关闭2527家加盟店引发市场担忧增速换挡。摩根大通下调目标价，大和维持"持有"评级。股价已较IPO高点腰斩。
    </div>
    <div class="source">来源：<a href="https://stock.finance.sina.com.cn/hkstock/news/02097.html" target="_blank">新浪港股</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">华沿机器人暗盘飙涨43% · 协作机器人热度高 <span class="hot-tag tag-industry">产业</span></div>
    <div class="detail">
      即将上市的华沿机器人在暗盘交易中一度飙升43%，反映市场对协作机器人赛道的追捧。优必选、柔宇等机器人相关标的获得资金关注。
    </div>
    <div class="source">来源：<a href="https://hk.eastmoney.com" target="_blank">东方财富网</a></div>
  </div>

  <div class="hot-item">
    <div class="hot-title">复星国际拟分拆三亚亚特兰蒂斯上市 <span class="hot-tag tag-earnings">公司</span></div>
    <div class="detail">
      <strong>复星国际(00656)尾盘涨超7%</strong>，公告拟通过REITs方式分拆三亚亚特兰蒂斯项目在上交所独立上市，释放资产价值。
    </div>
    <div class="source">来源：<a href="https://finance.sina.com.cn/stock/hkstock/" target="_blank">新浪港股</a></div>
  </div>
</div>

<!-- ===== 📊 市场情绪指标 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">📊</span>市场情绪指标</div>
  <div style="padding:14px;background:var(--bg);border-radius:10px;margin-bottom:14px">
    <table>
      <thead>
        <tr><th>指标</th><th>数据</th><th>解读</th></tr>
      </thead>
      <tbody>
        <tr><td>涨跌家数</td><td class="up">上涨约2800 / 下跌约2400</td><td>涨多于跌，市场情绪修复</td></tr>
        <tr><td>涨停/跌停</td><td>约50只涨停 / 约10只跌停</td><td>涨停数回升，赚钱效应恢复</td></tr>
        <tr><td>成交额</td><td>约2.00万亿元</td><td>较前日微增，回到2万亿关口</td></tr>
        <tr><td>南向资金(3/26)</td><td class="up">净买入33亿港元</td><td>加仓中海油、快手</td></tr>
        <tr><td>恒指窝轮成交</td><td>200.4亿港元</td><td>美团、腾讯、阿里窝轮活跃</td></tr>
      </tbody>
    </table>
  </div>
  <div class="detail">
    <strong>市场小结：</strong>A股呈现"低开高走"的探底回升形态，中证500+1.25%表现最强，反映中盘股修复力度大于权重。港股恒指在25000点附近拉锯，锂电和创新药双主线领涨。连续两日调整后的技术性反弹特征明显。
  </div>
</div>

<!-- ===== 🔭 明日展望 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">🔭</span>明日展望（3月30日·周一）</div>
  <div class="outlook-box">
    <h4>⚡ 技术面关键位</h4>
    <ul>
      <li><strong>上证指数：</strong>支撑位 3880-3890（20日均线），压力位 3950-3960（前高密集区）</li>
      <li><strong>深证成指：</strong>支撑位 13600，压力位 13900-14000</li>
      <li><strong>恒生指数：</strong>25000整数关口为多空分水岭，上方压力25300</li>
    </ul>
  </div>
  <div class="outlook-box">
    <h4>📌 可能的催化剂</h4>
    <ul>
      <li><strong>锂电排产数据：</strong>4月排产环比增长预期持续发酵，锂电板块或延续强势</li>
      <li><strong>AACR年会临近：</strong>多款创新药将亮相，医药板块催化不断</li>
      <li><strong>华沿机器人上市：</strong>协作机器人概念或持续活跃</li>
      <li><strong>机构观点：</strong>张忆东认为A港股下半年有望创年内新高，市场信心逐步修复</li>
    </ul>
  </div>
  <div class="outlook-box">
    <h4>⚠️ 潜在风险</h4>
    <ul>
      <li><strong>中美贸易摩擦：</strong>商务部对美贸易壁垒调查+芯片出口争端升级风险</li>
      <li><strong>成交量瓶颈：</strong>两市成交维持2万亿低位，增量资金不足</li>
      <li><strong>新消费板块杀估值：</strong>蜜雪冰城、泡泡玛特等高估值消费股仍在调整通道</li>
      <li><strong>地缘风险：</strong>美伊局势+芯片出口管制不确定性</li>
    </ul>
  </div>
</div>

<!-- ===== 📋 自选趋势分析 ===== -->
<div class="section">
  <div class="section-title"><span class="icon">📋</span>自选股趋势分析</div>
  <div class="trend-grid">

    <!-- 腾讯控股 -->
    <div class="trend-card neutral">
      <div class="trend-header">
        <span class="trend-name">腾讯控股 (0700.HK)</span>
        <span class="trend-badge badge-neutral">📊 震荡</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">491.20</span></span>
        <span><span class="label">收盘</span><span class="value down">493.40</span></span>
        <span><span class="label">最高</span><span class="value">498.20</span></span>
        <span><span class="label">最低</span><span class="value">487.60</span></span>
        <span><span class="label">涨跌幅</span><span class="value down">-0.44%</span></span>
        <span><span class="label">成交额</span><span class="value">100.2亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>腾讯卖空量近期骤降，资金做空意愿减弱。恒指窝轮中腾讯成交占比4.16%保持活跃。<br>
        <strong>趋势判断：</strong>股价在490-500区间震荡整理，昨日-1.96%大跌后今日小幅回稳。短期受大盘拖累但跌幅收窄。<br>
        <strong>支撑位：</strong>480-485（近期低点）&nbsp;&nbsp;<strong>压力位：</strong>510-518（20日均线区域）<br>
        <strong>机构目标价：</strong>高盛640、摩根士丹利620、中金580
      </div>
      <div class="trend-stars">⭐⭐⭐⭐ 推荐指数</div>
    </div>

    <!-- 阿里巴巴 -->
    <div class="trend-card neutral">
      <div class="trend-header">
        <span class="trend-name">阿里巴巴 (9988.HK)</span>
        <span class="trend-badge badge-neutral">📊 震荡</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">123.00</span></span>
        <span><span class="label">收盘</span><span class="value down">122.60</span></span>
        <span><span class="label">最高</span><span class="value">124.10</span></span>
        <span><span class="label">最低</span><span class="value">121.40</span></span>
        <span><span class="label">涨跌幅</span><span class="value down">-0.33%</span></span>
        <span><span class="label">成交额</span><span class="value">65.6亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>南向资金3/26数据显示流出阿里巴巴，短期获利了结压力明显。窝轮成交占比3.95%。<br>
        <strong>趋势判断：</strong>连续三日回调后企稳，120-125区间窄幅整理。AI云业务故事仍在但短期缺催化。前期128.7高点构成短期天花板。<br>
        <strong>支撑位：</strong>116.5-118（30日均线）&nbsp;&nbsp;<strong>压力位：</strong>128-130<br>
        <strong>机构目标价：</strong>瑞银150、摩根大通145、高盛148
      </div>
      <div class="trend-stars">⭐⭐⭐ 推荐指数</div>
    </div>

    <!-- 美团 -->
    <div class="trend-card bearish">
      <div class="trend-header">
        <span class="trend-name">美团 (3690.HK)</span>
        <span class="trend-badge badge-bear">📉 看空</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">86.15</span></span>
        <span><span class="label">收盘</span><span class="value down">85.90</span></span>
        <span><span class="label">最高</span><span class="value">90.70</span></span>
        <span><span class="label">最低</span><span class="value">84.70</span></span>
        <span><span class="label">涨跌幅</span><span class="value down">-0.92%</span></span>
        <span><span class="label">成交额</span><span class="value">87.0亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>窝轮成交占比高达4.75%，期权博弈活跃。盘中一度拉升至90.70但快速回落，上方抛压沉重。<br>
        <strong>趋势判断：</strong>从前期165高点持续回落至85附近，跌幅接近50%。虽然监管叫停价格战利好，但3/25发布年报后资金持续获利了结。形态偏弱，短期看空。<br>
        <strong>支撑位：</strong>81.5-83（近期低点）&nbsp;&nbsp;<strong>压力位：</strong>90-92<br>
        <strong>机构目标价：</strong>摩根大通120、高盛115、中金108
      </div>
      <div class="trend-stars">⭐⭐ 推荐指数</div>
    </div>

    <!-- 蜜雪冰城 -->
    <div class="trend-card bearish">
      <div class="trend-header">
        <span class="trend-name">蜜雪冰城 (2097.HK)</span>
        <span class="trend-badge badge-bear">📉 看空</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">303.20</span></span>
        <span><span class="label">收盘</span><span class="value down">286.00</span></span>
        <span><span class="label">最高</span><span class="value">303.20</span></span>
        <span><span class="label">最低</span><span class="value">283.00</span></span>
        <span><span class="label">涨跌幅</span><span class="value down">-4.86%</span></span>
        <span><span class="label">成交额</span><span class="value">3.5亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>盘中跌穿283创上市以来新低。CEO换帅消息发酵——35岁前CFO张渊接任，创始人张红甫卸任。2025年关闭2527家门店引发增速见顶担忧。大和维持"持有"评级，摩根大通下调目标价。<br>
        <strong>趋势判断：</strong>股价从IPO高点618.5已腰斩至286，连续破位创新低。业绩增35%不及市场预期的高增长叙事，加盟商关店问题持续发酵。短期无明显止跌信号。<br>
        <strong>支撑位：</strong>275-280（心理关口）&nbsp;&nbsp;<strong>压力位：</strong>300-310<br>
        <strong>机构目标价：</strong>大和"持有"评级，摩根大通下调中
      </div>
      <div class="trend-stars">⭐ 推荐指数</div>
    </div>

    <!-- 宁德时代 -->
    <div class="trend-card bullish">
      <div class="trend-header">
        <span class="trend-name">宁德时代 (300750.SZ)</span>
        <span class="trend-badge badge-bull">📈 看多</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">406.12</span></span>
        <span><span class="label">收盘</span><span class="value up">416.18</span></span>
        <span><span class="label">最高</span><span class="value">418.33</span></span>
        <span><span class="label">最低</span><span class="value">401.73</span></span>
        <span><span class="label">涨跌幅</span><span class="value up">+3.40%</span></span>
        <span><span class="label">成交额</span><span class="value">124.7亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>锂电产业链今日全面走强，4月全行业排产环比增长预期发酵。宁德时代作为板块龙头获得大量主力资金流入，成交额高达124.7亿元。<br>
        <strong>趋势判断：</strong>连续两日逆势走强（昨日+1.18%、今日+3.40%），已从402低点强势反弹至418一线。锂电排产利好+高油价推动新能源需求逻辑清晰，形态看多。<br>
        <strong>支撑位：</strong>400-405（5日均线）&nbsp;&nbsp;<strong>压力位：</strong>425-430（前期高点密集区）<br>
        <strong>机构目标价：</strong>中金500、华泰480、招商470
      </div>
      <div class="trend-stars">⭐⭐⭐⭐⭐ 推荐指数</div>
    </div>

    <!-- 泡泡玛特 -->
    <div class="trend-card bearish">
      <div class="trend-header">
        <span class="trend-name">泡泡玛特 (9992.HK)</span>
        <span class="trend-badge badge-bear">📉 看空</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">153.10</span></span>
        <span><span class="label">收盘</span><span class="value down">149.60</span></span>
        <span><span class="label">最高</span><span class="value">156.90</span></span>
        <span><span class="label">最低</span><span class="value">149.30</span></span>
        <span><span class="label">涨跌幅</span><span class="value down">-0.73%</span></span>
        <span><span class="label">成交额</span><span class="value">61.0亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>2025年净利增超3倍，但从339.8高点三日暴跌超30%后今日跌幅收窄至-0.73%，有企稳迹象但仍在下降通道。市场对2026年增速仅20%的展望极度失望。<br>
        <strong>趋势判断：</strong>短期超跌后的"死猫跳"风险仍存。从340跌至150，估值杀烈度罕见。需等待150以下充分换手后再观察是否形成底部形态。<br>
        <strong>支撑位：</strong>142-145（盘中探底区）&nbsp;&nbsp;<strong>压力位：</strong>160-170<br>
        <strong>机构目标价：</strong>多家机构下调中，此前目标价300-400已不具参考意义
      </div>
      <div class="trend-stars">⭐ 推荐指数</div>
    </div>

    <!-- 小米集团 -->
    <div class="trend-card bullish">
      <div class="trend-header">
        <span class="trend-name">小米集团 (1810.HK)</span>
        <span class="trend-badge badge-bull">📈 看多</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">32.30</span></span>
        <span><span class="label">收盘</span><span class="value up">33.00</span></span>
        <span><span class="label">最高</span><span class="value">33.40</span></span>
        <span><span class="label">最低</span><span class="value">31.92</span></span>
        <span><span class="label">涨跌幅</span><span class="value up">+1.73%</span></span>
        <span><span class="label">成交额</span><span class="value">47.3亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>新能源车出海逻辑+高油价撬动需求利好小米汽车业务，锂电板块全面走强间接提振新能源车产业链。<br>
        <strong>趋势判断：</strong>从31.2低点企稳反弹至33，低开高走形态良好。IoT+汽车双轮驱动长期逻辑不变。短期跟随锂电新能源板块走强。<br>
        <strong>支撑位：</strong>31.4-31.9（近期低点）&nbsp;&nbsp;<strong>压力位：</strong>34.7-35（前高区域）<br>
        <strong>机构目标价：</strong>摩根大通45、中金42、招商40
      </div>
      <div class="trend-stars">⭐⭐⭐⭐ 推荐指数</div>
    </div>

    <!-- 快手 -->
    <div class="trend-card neutral">
      <div class="trend-header">
        <span class="trend-name">快手 (1024.HK)</span>
        <span class="trend-badge badge-neutral">📊 震荡</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">45.00</span></span>
        <span><span class="label">收盘</span><span class="value up">46.08</span></span>
        <span><span class="label">最高</span><span class="value">46.60</span></span>
        <span><span class="label">最低</span><span class="value">44.80</span></span>
        <span><span class="label">涨跌幅</span><span class="value up">+1.05%</span></span>
        <span><span class="label">成交额</span><span class="value">28.2亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>南向资金3/26加仓快手，市场对此前暴跌14%后的超跌修复预期升温。AI投入260亿资本开支的长期影响仍在消化中。<br>
        <strong>趋势判断：</strong>前日暴跌14%后今日小幅反弹+1.05%，属于超跌后的技术性修复。45-47区间短期震荡整理，需观察48以上能否站稳确认企稳。<br>
        <strong>支撑位：</strong>43.9-44.5（近期低点）&nbsp;&nbsp;<strong>压力位：</strong>48-50<br>
        <strong>机构目标价：</strong>多家机构下调至55-65区间，2026展望被集体看淡
      </div>
      <div class="trend-stars">⭐⭐⭐ 推荐指数</div>
    </div>

    <!-- 优必选 -->
    <div class="trend-card neutral">
      <div class="trend-header">
        <span class="trend-name">优必选 (9880.HK)</span>
        <span class="trend-badge badge-neutral">📊 震荡</span>
      </div>
      <div class="trend-metrics">
        <span><span class="label">开盘</span><span class="value">88.80</span></span>
        <span><span class="label">收盘</span><span class="value up">91.00</span></span>
        <span><span class="label">最高</span><span class="value">91.55</span></span>
        <span><span class="label">最低</span><span class="value">88.00</span></span>
        <span><span class="label">涨跌幅</span><span class="value up">+0.28%</span></span>
        <span><span class="label">成交额</span><span class="value">4.3亿</span></span>
      </div>
      <div class="trend-analysis">
        <strong>盘中事件：</strong>华沿机器人暗盘飙涨43%，协作机器人概念升温。优必选作为人形机器人龙头间接受益。盘中一度下探88后快速拉升至91.55。<br>
        <strong>趋势判断：</strong>在86-95区间宽幅震荡。机器人赛道长期逻辑坚挺但短期缺乏业绩兑现催化。华沿机器人上市或带来短期情绪脉冲。<br>
        <strong>支撑位：</strong>86-88（近期低点）&nbsp;&nbsp;<strong>压力位：</strong>95-96<br>
        <strong>机构目标价：</strong>中金120、招商115、华泰110
      </div>
      <div class="trend-stars">⭐⭐⭐ 推荐指数</div>
    </div>

  </div>
</div>

<footer>
  <p>📊 A股港股收盘总结 · 2026年3月27日 · 自动化生成</p>
  <p>数据来源：新浪财经实时行情API · 东方财富网 · 上海证券报 · 新浪港股</p>
  <p>⚠️ 以上内容仅供参考，不构成投资建议</p>
</footer>
</div>
</body>
</html>'''

out = "cn-hk-market/report-2026-03-27-1630.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✅ Report written to {out} ({len(html)} bytes)")
