# Long-term Memory & Project Conventions

- **工作区目录结构 (2026-04-02 重组)**：`daily-reports/` 按五大任务组织，根目录只保留 `index.html` 主导航。各任务文件夹及输出路径：
  - `arxiv-ai/` — arXiv AI 日报。报告输出到 `arxiv-ai/reports/report-YYYY-MM-DD.html`，分片写入 `arxiv-ai/parts/YYYY-MM-DD/`，脚本在 `arxiv-ai/scripts/`，数据在 `arxiv-ai/data/`
  - `iran-commodity/` — 伊朗局势与大宗商品。报告输出到 `iran-commodity/reports/report-YYYY-MM-DD-HHMM.html`，脚本在 `iran-commodity/scripts/`，数据在 `iran-commodity/data/`
  - `tech-news/` — 科技与财经每日动态。报告输出到 `tech-news/reports/report-YYYY-MM-DD.html`，脚本在 `tech-news/scripts/`
  - `cn-hk-market/` — A股港股市场分析。报告输出到 `cn-hk-market/reports/report-YYYY-MM-DD-HHMM.html`，脚本在 `cn-hk-market/scripts/`
  - `_archive/` — 历史废弃文件
  - 每个任务文件夹根目录有 `index.html` 子导航页，历史链接格式为 `reports/report-xxx.html`
  - **⚠️ 自动化任务 prompt 中引用的文件路径必须与此结构一致**（原 `arxiv-papers/` 已重命名为 `arxiv-ai/`）

- **arXiv Automation Constraint (2026-03-20, critical update 2026-03-27)**: For the arXiv AI daily report automation (`arxiv-ai`), always strictly fetch the current day's real papers. **CRITICAL: When using arXiv RSS feeds, MUST filter by `Announce Type: new` in the `<description>` field. RSS feeds contain three types: `new` (truly new papers), `cross` (cross-listed from other categories), and `replace` (updated versions of old papers). Only `new` type papers should be included.** Never use outdated papers, simulate data, or hallucinate content. After selection, verify published dates via arXiv API before generating the report.
- **arXiv Advanced Formatting & Volume (2026-03-20, updated 2026-03-24)**: 
  - **Volume**: The daily report MUST contain exactly 10 to 15 papers.
  - **Typography**: Do not use raw text code blocks (`<div class="code">`) for Deep Case Studies / Reasoning Traces. Always use elegant HTML structures like `<div class="example-box">` with `<strong>` and `<ol>`/`<ul>` lists.
  - **Math**: All equations inside reasoning traces or methods must be properly rendered with MathJax inline `\(\)` or block `$$` syntax.
  - **Method Detail (2026-03-24)**: The "核心方法详解" section is the MOST important part of each paper. It MUST be split into 3-4 numbered sub-modules (①②③④), each independently explaining a key component of the method. Each sub-module must include: LaTeX math formulas, specific algorithm step decomposition, and design intuition explanations. A single paragraph overview is NOT acceptable.
  - **Report Generation Strategy (2026-03-24, updated 2026-04-02)**: Large HTML reports (70-100KB) exceed `write_to_file` token limits. Use split-write strategy: create `arxiv-ai/parts/YYYY-MM-DD/` date-named subdirectory with 5-6 part files (header+CSS+TOC, LLM papers, RL papers, Agent+Medical papers, Multimodal papers+reflection+footer), then concatenate with Python and output to `arxiv-ai/reports/`. Do NOT clean old part files — each day's parts live in their own date folder. **Section structure**: LLM + RL + Agent + Medical + Multimodal (≤3 papers). NO IR section.
  - **Institution Metadata (2026-03-27)**: Each paper's `paper-meta` div MUST include a `🏛` institution line. Obtain affiliations from arXiv HTML5 full-text (`/html/<id>v1`) pages. Display rule: ≤3 institutions → list all; >3 institutions → list top 3 only. Format: `<span>🏛 Inst1, Inst2, Inst3</span>` placed between the date and tag lines.
- **arXiv Preferences (2026-03-23, updated 2026-04-01)**: Report has 5+1 sections: **LLM** (pure text), **RL** (pure text), **Agent** (pure text), **Medical** (Medical LLMs), **Multimodal** (≤3 papers, vision/video LLMs), and optionally **🏢 Industry Lab** (catch-all for whitelist papers that don't fit other sections). The LLM/RL/Agent/Medical sections MUST NOT include any multimodal papers — keep them strictly text-modality. The Multimodal section is independent and should only pick the most impactful 1-3 papers. **Removed**: IR section is no longer included. Keywords like "exploration" and "reward" should be used to capture RL papers. User confirmed satisfaction with the current dark-theme visual style (deep color theme + MathJax + elegant example-box + HTML tables) on 2026-03-26 — keep this style consistent going forward.
- **arXiv Institution Whitelist (2026-04-01 新增)**: Papers from the following institutions MUST be included in the report — no exceptions: **DeepSeek, Qwen (阿里通义千问), OpenAI, Google (DeepMind/Google Research), Scale AI, Seed (字节跳动), Hunyuan (腾讯混元)**. Whitelist papers are first classified into existing sections (LLM/RL/Agent/Medical/Multimodal); if they don't fit any, they go into the **🏢 Industry Lab** section (gold/amber gradient style, `tag-industry` class). Whitelist papers do NOT count toward the 10-15 paper cap — they are always additional. Part files may expand to 5-7 parts to accommodate the Industry Lab section.
- **Iran Commodity Daily Report Refinement (2026-03-20 & 2026-03-24)**: The `automation` task has been strictly upgraded to fetch at least 10 news items categorized into "Military" and "Diplomatic Reactions" (or the new 3-tier structure). For data visualization, it MUST use 10-day historical data. Since Yahoo Finance API frequently returns 403 Forbidden or Rate Limited, use Sina Finance API (`hq.sinajs.cn/list=hf_OIL,hf_CL,hf_NG,hf_GC,hf_SI...`) with a `Referer: https://finance.sina.com.cn` header for live quotes, and extract historical data from previous HTML reports or alternative stable APIs.

- **科技与财经每日动态 (automation-2) (2026-03-23, updated 2026-04-02)**: 报告按七大垂直赛道组织：大模型与基础AI、脑机接口与生物科技、具身智能与机器人、视频与多模态生成、自动驾驶与出行、科技巨头与财报、创投与融资。
  - **⚠️ 导航页更新必须使用脚本 (2026-04-02 新增)**：生成报告后，**禁止手工用 replace_in_file 更新导航页**，必须运行 `python3 tech-news/scripts/update_nav.py <date> <news_count> "<summary>"` 来自动更新 `tech-news/index.html` 和 `index.html` 两个导航页。脚本内置验证逻辑，更新后会自动校验结果。这是为了彻底杜绝之前手工替换时"最新报告"区块未生效的bug。

- **GitHub Auth (2026-04-02)**：用户已通过 `gh auth login` 配置 GitHub 认证，git push 可正常工作，无需再担心认证问题。

- **主页同步更新约定 (2026-04-02 新增)**：所有 automation 生成报告后，除了更新各自子目录的 `index.html` 外，还必须同步更新根目录 `index.html` 主导航页对应卡片的「最新报告」标题/日期和历史报告列表。用户已在 a-2（收盘总结）的 prompt 中加入此要求，其他 automation（a-7 盘前前瞻等）也应遵循此约定。

- **A股港股自选股列表 (2026-03-26 创建, 2026-03-27 更新)**：自选股共 9 只：腾讯控股(0700.HK)、阿里巴巴(9988.HK)、美团(3690.HK)、蜜雪冰城(2097.HK)、宁德时代(300750.SZ)、泡泡玛特(9992.HK)、小米集团(1810.HK)、快手(1024.HK)、优必选(9880.HK)。已同步更新至 a-6（收盘总结）和 a-7（盘前前瞻）两个 automation 的 prompt 中。
- **A股港股收盘报告 — 自选股趋势判断 (2026-03-26 新增)**：用户要求在收盘报告的自选股模块中增加趋势判断。每只自选股需包含：趋势定性（看多/震荡/看空）、关键技术位（支撑位/压力位）、机构目标价参考、推荐星级（⭐1-5）。使用三色趋势卡片样式（bullish=红左边栏, bearish=绿左边栏, neutral=金左边栏）。此功能应在后续每日收盘报告（a-6 automation）中持续保留。
  - **结构（2026-03-24 重大更新）**：取消 Top 5 核心焦点的筛选机制，不再区分"核心焦点"和"前沿快讯"。所有新闻统一按七大赛道分类，每条新闻都用核心焦点级别的深度详细写（事件背景、数据亮点、技术细节、产业/资本影响），不再有简短快讯。
  - 数量：每天至少抓取 20 条过去 24 小时内的最新新闻（真实信源URL）。
  - 生成要求：在回答中，必须在草稿区输出 `<Reflection>` 进行自我拷问（如新闻数量、24h时效、链接有效性），反思通过后方可生成最终报告。
  - 自动化要求：输出文件名应严格遵循 `report-YYYY-MM-DD.html`。