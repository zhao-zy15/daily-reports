# 2026-04-02 Execution Summary
- Fetched papers from arXiv RSS feeds (cs.CL, cs.AI, cs.LG) dated 2026-04-02. All filtered by `Announce Type: new`. Total 173 unique new papers.
- Whitelist check: thoroughly verified all 11 initially flagged papers via arXiv HTML5 pages. Only **1 paper** confirmed from whitelist institution (Google/DeepMind). The other 10 were false positives — they merely *used* whitelist models (e.g., "tested on DeepSeek-R1") but were from independent/university labs.
- Selected **15 papers** (14 regular + 1 whitelist): LLM(5) + RL(3) + Agent(3) + Medical(2) + Multimodal(1). No Industry Lab section needed.
- Generated 88.7KB HTML report via 6-part split-write strategy in `report_parts/2026-04-02/`.
- Updated `arxiv-papers/report-2026-04-02.html`, `arxiv-papers/index.html`, and main `index.html`.
- Git committed and pushed to main.

## Key Papers Highlights
- **OptiMer** (MIT, Harvard): Distribution vector merging outperforms data mixing for CPT; GSM8K 68.2% vs 64.8% best data-mixing baseline; works by decomposing training data into sub-distributions
- **Tucker Attention** (UC Berkeley): Unifies MHA/MQA/GQA/MLA as Tucker decomposition variants; 7.4× KV cache compression with only 0.9% MMLU loss; direct conversion from MHA without retraining
- **DUME** (Hanyang, LG AI): Training-free dynamic upcycling of expert LMs into MoE; token-level routing via weight-difference affinity; beats BTX (50B tok training) with zero extra training
- **PolarQuant** (Independent): Proves Hadamard rotation is optimal for Gaussianizing LLM weights; 3-bit Llama-70B with PPL 5.94 (QuaRot: 6.03); kurtosis reduction 98.8%
- **Simula** (Google/DeepMind, EPFL): Reasoning-driven synthetic data pipeline; multi-strategy generation + self-consistency + reasoning verifier + curriculum; Gemma-2-9B GSM8K 72.1%→83.6%
- **ShapE-GRPO** (PKU, Shanghai AI Lab): Shapley value-based reward allocation for GRPO; closed-form O(G log G) computation; MATH +3.6% over GRPO, gradient variance -35%
- **CoT Safety** (Google DeepMind): Three-way taxonomy (aligned/orthogonal/conflict) for CoT safety; tiered reward shaping; 95.2% safety + 4.15 helpfulness with only 4.8% over-refusal
- **PRoSFI** (Edinburgh, Allen AI): Structured Formal Intermediaries for verifiable step-by-step reasoning; Z3 SMT solver verification; 89.1% logic verification rate with RL
- **APEX-EM** (Georgia Tech): Procedural memory for autonomous agents; online extraction + confidence updating; WebArena SR 22.1% (+3.8 vs ExpeL)
- **MemFactory** (RUC, Tencent AI Lab): Unified agent memory framework; dual-channel (reasoning + training); memory consolidation with Ebbinghaus forgetting; ALFWorld SR 58.7%
- **AgentFixer** (IBM, MIT): Hierarchical fault taxonomy + detection + repair for LLM agents; 52.7% fault recovery rate; 4-level repair strategy
- **CPB-Bench** (UMich, Mayo Clinic): 8 challenging patient behaviors × 500 cases; Contradictory behavior causes -22% accuracy drop; Claude-3.5 best on empathy
- **ConRad** (Stanford, UCSF): Calibrated confidence expression for radiology reports; 5-level scale + hedging language; ECE 0.068 (vs 0.143 GPT-4V)
- **PID for VLMs** (Oxford, Turing Institute): Information decomposition analysis of VLM decisions; quantifies unique/redundant/synergistic info from vision vs language; GPT-4V highest synergy (0.31)

## Lessons Learned
- Whitelist matching must verify actual author affiliations, not just model name mentions in abstracts. Many papers mention "DeepSeek-R1" or "Qwen-72B" as evaluation baselines but are from unrelated institutions.
