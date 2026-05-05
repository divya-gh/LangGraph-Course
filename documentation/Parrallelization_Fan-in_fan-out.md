# 🌟 Fan‑Out and Fan‑In in LangGraph (Beginner‑Friendly)
Think of your graph like a river:

- Fan‑out = the river splits into multiple smaller streams
- Fan‑in = the streams merge back into one river

This is exactly how parallelization works in LangGraph.

## 🟦 1. What is Fan‑Out?
#### Fan‑out = one node sends the state to multiple child nodes at the same time.

### When does this happen?

When multiple nodes:
- depend on the same input
- do NOT depend on each other
- write to different parts of the state

##### Visual 
Code
```
        ┌─── Node B
Node A ─┤
        └─── Node C
```
#### Meaning
Node A finishes → LangGraph sees that B and C can run independently → it runs them in parallel.

### Example: If the user asks:
- “Summarize this text, extract keywords, and detect sentiment.”

You can fan‑out like this: Code
```
start → summarize
      → extract_keywords
      → sentiment
```
All three run at the same time.

## 🟩 2. What is Fan‑In?
#### Fan‑in = multiple parallel nodes finish, and their outputs merge into a single node.

##### Visual
```
        ┌─── Node B ───┐
Node A ─┤               ├──→ Node D
        └─── Node C ───┘
```

#### Meaning
Node D waits until:
- B is done
- C is done
Then it receives both outputs and continues.

#### Example
After summarizing, extracting keywords, and detecting sentiment, you might want to combine everything:

Code
```
summarize ───────┐
extract_keywords ─┼──→ combine_results
sentiment ───────┘
```
combine_results is the fan‑in node.

## 🟧 3. Why Fan‑Out + Fan‑In = Parallelization
Parallelization happens automatically when:

    - A node fans out to multiple children
    - Those children do not depend on each other
    - They eventually fan in to a merge node

LangGraph sees this structure and runs the children concurrently.

- You don’t need to write threading code.
- You don’t need async/await.
- You don’t need multiprocessing.
The graph structure itself tells LangGraph what can run in parallel.

### 🟪 4. Minimal Code Example (Perfect for Your Notebook)
python
```
from langgraph.graph import StateGraph
from typing import TypedDict, List

class State(TypedDict):
    text: str
    summary: str
    keywords: List[str]
    sentiment: str


graph = StateGraph(State)

def start(state):
    return state

def summarize(state):
    return {"summary": "short summary"}

def extract_keywords(state):
    return {"keywords": ["ai", "agents"]}

def detect_sentiment(state):
    return {"sentiment": "positive"}

def combine(state):
    return state

graph.add_node("start", start)
graph.add_node("summarize", summarize)
graph.add_node("keywords", extract_keywords)
graph.add_node("sentiment", detect_sentiment)
graph.add_node("combine", combine)

# Fan-out
graph.add_edge("start", "summarize")
graph.add_edge("start", "keywords")
graph.add_edge("start", "sentiment")

# Fan-in
graph.add_edge("summarize", "combine")
graph.add_edge("keywords", "combine")
graph.add_edge("sentiment", "combine")

graph.set_entry_point("start")
graph.set_finish_point("combine")
```
This graph will run:
- summarize
- keywords
- sentiment
in parallel, then merge them into combine.