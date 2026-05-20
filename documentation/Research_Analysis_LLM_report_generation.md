# Research Assistant Agent- 
Agent built with LLM , Parallelization, sub-graph, persistance, map-reduce

## Goal : Our goal is to build a lightweight, multi-agent system around chat models that customizes the research process.

1. Source Selection
Users can choose any set of input sources for their research:
websites, PDFs, reports, internal docs, or curated datasets.

The system adapts to whatever sources the user trusts.

🧠 2. Planning
Users provide a topic.
The system generates a team of AI analysts, each assigned to a different sub‑topic.

Before research begins, a human‑in‑the‑loop step lets the user refine or adjust these sub‑topics.

This ensures the research direction is aligned with the user’s goals.

3. LLM Utilization (STORM‑style Interviews)
Each analyst conducts a multi‑turn interview with an expert AI, using the selected sources as context.

This mirrors the STORM paper approach:

Analysts ask questions

Experts answer using the chosen sources

Analysts dig deeper

Insights accumulate over multiple turns

Each interview runs inside a sub‑graph, maintaining its own internal state.

4. Research Process (Map‑Reduce)
All expert interviews run in parallel.

Using LangGraph’s map‑reduce pattern:

Map: Each analyst → one interview

Reduce: All insights → merged into a unified knowledge base

This massively speeds up research and ensures depth + breadth.

📝 5. Output Format
All gathered insights are synthesized into a final report.

The report format is fully customizable:

executive summary

bullet‑point insights

competitor analysis

market trends

recommendations

citations

Users can choose the style, tone, and structure.

Why this matters
This isn’t “chat with your documents.”
It’s a full research pipeline:

structured

multi‑agent

parallel

explainable

customizable

repeatable

It produces business‑ready deliverables, not chatbot answers.