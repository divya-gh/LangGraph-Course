# Parallel Node Execution
Parallelization = letting multiple nodes run at once when they’re independent.

## 1. What “parallelization” means here
In LangGraph (and similar agent frameworks):

### Sequential:  
- Node A → Node B → Node C (one after another)

### Parallel:  
- Node A → Node B
     ↘ Node C
B and C can run at the same time if:

- they both have enough info in the state, and
- they don’t depend on each other’s outputs.

## 2. Step 1 – when to parrallelize? 

### Identify independent work : 
Ask yourself: What can happen at the same time?
    
    - Call multiple tools?
    - Hit multiple APIs?
    - Generate multiple drafts?
    - Analyze different parts of the same input?

### Example: You have a user query.
##### You want to:

    - Search the web
    - Query a database
    - Call a recommendation model
None of these depend on each other → perfect for parallelization.

#### Write this down in your notebook as: markdown
Independent tasks:
    - web_search
    - db_lookup
    - recommend_model`

## 3. Step 2 – Design state to support parallel nodes

1. Parallel nodes will read from the same state and write to different keys.

#### Example state shape: python
```
from typing import TypedDict, List, Any

class State(TypedDict):
    user_query: str
    web_results: List[str]
    db_results: List[str]
    model_suggestions: List[str]

```
- All nodes read user_query.
- Each node writes to its own key:
- web_results
- db_results
- model_suggestions
This avoids conflicts when merging.

2. Use reducers to ammend the state if nodes write to the same key

#### Example state QA: python
```
from typing import TypedDict, List, Any
from operator import add 
from typing import Annotated

class State(TypedDict):
    Question: str
    Answer : List[str]
    Context: Annotated[list[str],add]

```
- appends the context

## 4. Step 3 – Create one node per independent task

#### Example (pseudo‑LangGraph): python
```
from langgraph.graph import StateGraph

graph = StateGraph(State)

def web_search_node(state: State) -> State:
    # call your search tool / API
    results = ["result 1", "result 2"]
    return {"web_results": results}

def db_lookup_node(state: State) -> State:
    # query your DB
    results = ["row 1", "row 2"]
    return {"db_results": results}

def model_recommend_node(state: State) -> State:
    # call an LLM or model
    suggestions = ["suggestion 1", "suggestion 2"]
    return {"model_suggestions": suggestions}

graph.add_node("web_search", web_search_node)
graph.add_node("db_lookup", db_lookup_node)
graph.add_node("model_recommend", model_recommend_node)
```
- Each node is small, focused, and writes to a different part of state.

## 5. Step 4 – Wire the graph so nodes can run in parallel
You need a parent node that sets up the state, then fan‑out to multiple children.

python
```
def start_node(state: State) -> State:
    # maybe just pass through user_query
    return state

graph.add_node("start", start_node)

# Edges: start → web_search, db_lookup, model_recommend
graph.add_edge("start", "web_search")
graph.add_edge("start", "db_lookup")
graph.add_edge("start", "model_recommend")
```
Because:

    - All three children depend only on start
    - None of them depend on each other
→ the runtime is free to run them in parallel.

### Then you add a join/merge node: python
```
def combine_node(state: State) -> State:
    # here you have web_results, db_results, model_suggestions
    # you can build a final answer
    return state

graph.add_node("combine", combine_node)

# All parallel nodes → combine
graph.add_edge("web_search", "combine")
graph.add_edge("db_lookup", "combine")
graph.add_edge("model_recommend", "combine")

graph.set_entry_point("start")
graph.set_finish_point("combine")
```
The runtime will:

    - Run *start*
    - Run *web_search, db_lookup, model_recommend* (in parallel)
    - Wait until all three finish
    - Run *combine*

## 6. Step 5 – Parallel tool calls (bonus mental model)
If you’re using an LLM that returns multiple tool calls in one response (e.g., Gemini, OpenAI):

- he model might say:
- call web_search
- call db_lookup
- call recommend_model

Your agent framework (or a ToolNode) can:
- See all tool calls
- Execute them concurrently
- Merge their results back into state

So parallelization can happen at two levels:

    - Graph level: multiple nodes at once
    - Tool level: multiple tools at once inside a node

## 7. Step 6 – How to think about it while coding
When you’re writing your notebook, keep this checklist:

### Parallelization checklist

- Do I have multiple tasks that:
  - read the same input?
  - don’t depend on each other’s outputs?

- Did I:
  - give each task its own node?
  - make each node write to a separate state key?

- Did I:
  - fan-out from a common parent node?
  - fan-in to a combine node?

If yes → the runtime can parallelize 