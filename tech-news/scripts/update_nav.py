#!/usr/bin/env python3
"""
update_nav.py — 科技与财经每日动态导航页自动更新脚本

用法:
    python3 update_nav.py <date> <news_count> <summary>

示例:
    python3 update_nav.py 2026-04-02 24 "Qwen3.6-Plus发布·Anthropic源码泄露·Q1创投3000亿破纪录"

功能:
    1. 更新 tech-news/index.html 的最新报告区块 + 历史列表
    2. 更新主导航 index.html 的科技卡片最新报告 + 历史列表
    3. 自动验证报告文件是否存在
"""

import sys
import os
import re
from datetime import datetime

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tech-news/
ROOT_DIR = os.path.dirname(BASE_DIR)  # daily-reports/
TECH_INDEX = os.path.join(BASE_DIR, "index.html")
MAIN_INDEX = os.path.join(ROOT_DIR, "index.html")


def get_weekday_cn(date_str):
    """获取中文星期"""
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return days[dt.weekday()]


def update_tech_index(date, news_count, summary):
    """更新 tech-news/index.html"""
    with open(TECH_INDEX, "r", encoding="utf-8") as f:
        html = f.read()

    report_path = f"reports/report-{date}.html"
    report_file = os.path.join(BASE_DIR, report_path)
    if not os.path.exists(report_file):
        print(f"[ERROR] 报告文件不存在: {report_file}")
        sys.exit(1)

    # 1) 更新最新报告区块 — 用正则精确匹配
    html = re.sub(
        r'(<div class="latest-report">.*?<div class="title">)(.*?)(</div>.*?<a href=")(.*?)(" class="btn">)',
        rf'\g<1>{date}\g<3>{report_path}\g<5>',
        html,
        count=1,
        flags=re.DOTALL
    )

    # 2) 在历史列表最前面插入上一个最新报告（如果还没有的话）
    #    找到 <ul class="history-list"> 后面的第一个 <li>，检查日期
    first_history_match = re.search(
        r'<ul class="history-list">\s*<li>\s*<a href="reports/report-(\d{4}-\d{2}-\d{2})\.html">',
        html
    )

    if first_history_match:
        first_history_date = first_history_match.group(1)
        # 如果历史列表第一条不是今天的前一天（即今天的报告还没被加入历史），
        # 我们不需要处理——因为今天是"最新报告"，不进历史列表。
        # 但如果历史列表里已经有今天的日期（不应该出现），就跳过。
        if first_history_date == date:
            print(f"[WARN] 历史列表已包含 {date}，跳过插入")
    else:
        print("[WARN] 无法解析历史列表")

    with open(TECH_INDEX, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] tech-news/index.html 已更新: 最新报告 → {date}")


def update_main_index(date, news_count, summary):
    """更新主导航 index.html 的科技卡片"""
    with open(MAIN_INDEX, "r", encoding="utf-8") as f:
        html = f.read()

    # 定位科技卡片区域 (class="report-card tech")
    tech_card_match = re.search(
        r'(<div class="report-card tech">)(.*?)(</div>\s*</div>\s*<!-- |\Z)',
        html,
        flags=re.DOTALL
    )
    if not tech_card_match:
        # 备选：用更宽泛的方式定位
        print("[WARN] 无法用class定位tech卡片，尝试用标题定位")

    # 1) 更新最新报告日期
    #    找 tech 卡片内的 <div class="title">xxxx</div>
    html = re.sub(
        r'(<!-- 科技与 AI 日报 -->.*?<div class="title">)(.*?)(</div>\s*</div>\s*<a href="tech-news/" class="btn">)',
        rf'\g<1>{date} 17:30\g<3>',
        html,
        count=1,
        flags=re.DOTALL
    )

    # 2) 在科技卡片的历史列表最前面插入新条目（如果还没有的话）
    tech_history_pattern = r'(<!-- 科技与 AI 日报 -->.*?<ul class="history-list">)\s*(<li>)'
    tech_history_match = re.search(tech_history_pattern, html, flags=re.DOTALL)

    if tech_history_match:
        # 检查是否已有今天的条目
        existing_check = re.search(
            rf'<!-- 科技与 AI 日报 -->.*?<ul class="history-list">.*?report-{date}\.html',
            html,
            flags=re.DOTALL
        )
        if not existing_check:
            new_entry = f'''
                        <li>
                            <a href="tech-news/reports/report-{date}.html">
                                <span class="date">{date}</span>
                                <span class="time">17:30</span>
                            </a>
                        </li>
                        '''
            html = re.sub(
                tech_history_pattern,
                rf'\g<1>{new_entry}\g<2>',
                html,
                count=1,
                flags=re.DOTALL
            )
            print(f"[OK] 主导航 历史列表已插入 {date}")
        else:
            print(f"[OK] 主导航 历史列表已包含 {date}，跳过")

    with open(MAIN_INDEX, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] index.html 已更新: 科技卡片最新 → {date}")


def verify(date):
    """验证更新结果"""
    errors = []

    with open(TECH_INDEX, "r", encoding="utf-8") as f:
        tech_html = f.read()

    with open(MAIN_INDEX, "r", encoding="utf-8") as f:
        main_html = f.read()

    # 检查 tech-news/index.html
    if f'<div class="title">{date}</div>' not in tech_html:
        errors.append(f"tech-news/index.html 最新报告标题未更新为 {date}")
    if f'href="reports/report-{date}.html"' not in tech_html:
        errors.append(f"tech-news/index.html 最新报告链接未更新")

    # 检查 index.html
    if f'report-{date}.html' not in main_html:
        errors.append(f"index.html 未包含 {date} 报告链接")

    if errors:
        print("\n[FAIL] 验证失败:")
        for e in errors:
            print(f"  ❌ {e}")
        sys.exit(1)
    else:
        print(f"\n[PASS] 验证通过 ✅ — 两个导航页均已正确更新为 {date}")


def main():
    if len(sys.argv) < 4:
        print("用法: python3 update_nav.py <date> <news_count> <summary>")
        print('示例: python3 update_nav.py 2026-04-02 24 "Qwen3.6发布·源码泄露"')
        sys.exit(1)

    date = sys.argv[1]
    news_count = sys.argv[2]
    summary = sys.argv[3]

    # 验证日期格式
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(f"[ERROR] 日期格式错误: {date}，需要 YYYY-MM-DD")
        sys.exit(1)

    print(f"=== 更新科技与财经导航页 ===")
    print(f"日期: {date} | 新闻数: {news_count} | 摘要: {summary}")
    print()

    update_tech_index(date, news_count, summary)
    update_main_index(date, news_count, summary)
    verify(date)


if __name__ == "__main__":
    main()
