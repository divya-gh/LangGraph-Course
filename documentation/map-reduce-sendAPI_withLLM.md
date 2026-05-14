# MAP-Reduce and Send API with LLM

### What is Map‑Reduce with LLMs?
You use an LLM to:

    MAP → break a big input into smaller chunks
    PROCESS → run the LLM on each chunk in parallel
    REDUCE → merge all LLM outputs into a final answer

This is perfect for:
- Generate specic doc for  a list of subjects
- Summarizing long documents
- Extracting facts from many paragraphs
- Running multiple LLM calls at once
- Multi‑agent fan‑out tasks
- And LangGraph’s Send API makes this easy.

## Problem

Map-reduce operations are essential for efficient task decomposition and parallel processing. 

It has two phases:

(1) `Map` - Break a task into smaller sub-tasks, processing each sub-task in parallel.

(2) `Reduce` - Aggregate the results across all of the completed, parallelized sub-tasks.

## Goal: build an LLM agent that uses map-reduce and send API to summerize an article paragraphs simultaniously .

### Mental model:
Imagine you have a long article split into 5 paragraphs: Code
```
[p1, p2, p3, p4, p5]
```
You want the LLM to summarize each paragraph in parallel, then combine them.

**Map‑reduce does:**

`Map: `
- For each paragraph → send to LLM

`Reduce: `
- Combine all summaries → final summary



