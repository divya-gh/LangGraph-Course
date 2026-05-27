# 🧠 Research Assistant Agent
**Agentic Research Pipeline using LangGraph, Gemini, RAG, Parallelization & Persistent State**

The Research Assistant Agent is an end‑to‑end automated research system built using LangGraph, Gemini, and retrieval‑augmented generation (RAG).

It performs multi‑step reasoning, expert‑style analysis, automated interviews, and structured report generation — all orchestrated through deterministic, debuggable agentic workflows.

This project demonstrates how to combine LLMs + sub‑graphs + memory + parallelization + map‑reduce to build a reliable, extensible research automation pipeline.

## 🚀 Features

`🔹 1. Human‑in‑the‑Loop Topic Refinement`
    
    - User provides a research topic
    - Agent generates 3 subtopics
    - User can refine, modify, or expand them
    - Agent creates expert analyst personas for each subtopic
    - User can refine personas as well
This ensures the system stays aligned with user intent.

**Parallelization** 

`🔹 2. Automated Expert Interviews (ReAct‑Style Subgraph)`
A dedicated interview sub‑graph handles:

    - Question generation
    - Parallel Tavily Web Search + Wikipedia retrieval
    - RAG‑style context construction
    - Evidence‑based answer generation
    - Full Q&A transcript storage
This produces grounded, transparent, expert‑like insights.

`🔹 3. Retrieval‑Augmented Research`
The agent integrates:

    - LLM for serch_query based on the questions
    - Tavily Search API
    - Wikipedia extraction
    - Context merging
    - Error‑resilient fallbacks
Every answer is backed by real‑world information.

`🔹 4. Multi‑Agent Technical Report Generation`
Each analyst persona produces a structured technical report:

    - Deep analysis
    - Evidence‑based reasoning
    - Context‑aware insights
    - Domain‑specific perspective
These reports form the foundation for the final synthesis.

**Map‑Reduce Orchestration**

`🔹 5. Final Report Synthesis`
##### The system merges:

    - Introduction
    - Technical reports
    - Interview insights
    - Conclusion

##### The final output is:

    - Markdown‑formatted
    - Easy to understand
    - Insight‑driven
    - Fully grounded in provided documents
    -  Includes source citations for authenticity

## 🧩 Architecture Overview
✔ LangGraph Orchestration
- Main graph handles topic → subtopics → analysts → interviews → synthesis
- Sub‑graphs handle interviews and retrieval
- Persistent state ensures deterministic execution
- Map‑reduce pattern used for multi‑analyst synthesis

✔ Agentic Workflow
- ReAct‑style reasoning
- Parallel retrieval
- Memory‑aware state transitions
- Human‑in‑the‑loop checkpoints

## 🛠 Tech Stack
- LangGraph — workflow orchestration
- LangChain — LLM integration
- Gemini — analyst personas & report generation
- Python — implementation
- RAG Components:
    - Tavily Search API — web retrieval
    - Wikipedia Loader — structured knowledge extraction


## 📄 Project Goals
This project demonstrates how to build AI systems that are:

    - Modular — clean separation of concerns
    -Reliable — deterministic state transitions
    - Transparent — full traceability of reasoning
    - Extensible — easy to add new agents or workflows

It shows how agentic systems can move beyond simple Q&A to perform multi‑step reasoning, evidence gathering, and structured synthesis.

## 🤝 Contributing
- Contributions, ideas, and improvements are welcome.
- If you're exploring agentic systems, feel free to open issues, submit PRs, or reach out.

## ⭐ Acknowledgements
**Thanks to the LangGraph and LangChain teams for enabling powerful agentic workflows, and to the Gemini ecosystem for high‑quality LLM reasoning.**

`This project was built as part of my learning journey through LangGraph Academy.`