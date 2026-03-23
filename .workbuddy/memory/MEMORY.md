# Long-term Memory & Project Conventions

- **arXiv Automation Constraint (2026-03-20)**: For the arXiv AI daily report automation (`arxiv-ai`), always strictly fetch the current day's real papers from the arXiv API (e.g., using `submittedDate` matching the current context date). Never use outdated papers, simulate data, or hallucinate content. The prompt has been permanently updated to enforce this.
- **arXiv Advanced Formatting & Volume (2026-03-20)**: 
  - **Volume**: The daily report MUST contain exactly 10 to 15 papers.
  - **Typography**: Do not use raw text code blocks (`<div class="code">`) for Deep Case Studies / Reasoning Traces. Always use elegant HTML structures like `<div class="example-box">` with `<strong>` and `<ol>`/`<ul>` lists.
  - **Math**: All equations inside reasoning traces or methods must be properly rendered with MathJax inline `\(\)` or block `$$` syntax.
- **arXiv Preferences (2026-03-23)**: User explicitly disikes multi-modal (visual/video/image) papers and wants the report to focus strictly on pure Text LLMs, RL, and Agents. Keywords like "exploration" and "reward" should be used to capture RL papers (e.g. "Experience is the Best Teacher").
- **Iran Commodity Daily Report Refinement (2026-03-20)**: The `automation` task has been strictly upgraded to fetch at least 10 news items categorized into "Military" and "Diplomatic Reactions". For data visualization, it MUST use 10-day historical data from Yahoo Finance to plot 4 independent line charts for Crude, Natural Gas, Gold, and Silver, completely abandoning the single unified bar chart layout.

- **科技与财经每日动态 (automation-2) (2026-03-23)**: 彻底重构了报告结构。不再仅限于简单的四大类，而是拆分为七大垂直赛道：大模型与基础AI、脑机接口与生物科技、具身智能与机器人、视频与多模态生成、自动驾驶与出行、科技巨头与财报、创投与融资。
  - 数量：每天至少抓取 20 条过去 24 小时内的最新新闻（真实信源URL）。
  - 重要性分级：Top 5 最重要的跨界新闻组成“核心焦点 (深度解析)”，详细阐述事件背景、资本影响；其余 15 条以上作为各赛道的“前沿快讯”简要列出。
  - 自动化要求：以后必须使用类似 `generate_tech_news_v2.py` 的脚本大规模聚合多个垂直领域的新闻数据，确保全面覆盖用户关注的所有科技行业赛道。