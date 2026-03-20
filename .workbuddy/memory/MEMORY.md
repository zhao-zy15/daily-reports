# Long-term Memory & Project Conventions

- **arXiv Automation Constraint (2026-03-20)**: For the arXiv AI daily report automation (`arxiv-ai`), always strictly fetch the current day's real papers from the arXiv API (e.g., using `submittedDate` matching the current context date). Never use outdated papers, simulate data, or hallucinate content. The prompt has been permanently updated to enforce this.
- **arXiv Advanced Formatting & Volume (2026-03-20)**: 
  - **Volume**: The daily report MUST contain exactly 10 to 15 papers.
  - **Typography**: Do not use raw text code blocks (`<div class="code">`) for Deep Case Studies / Reasoning Traces. Always use elegant HTML structures like `<div class="example-box">` with `<strong>` and `<ol>`/`<ul>` lists.
  - **Math**: All equations inside reasoning traces or methods must be properly rendered with MathJax inline `\(\)` or block `$$` syntax.