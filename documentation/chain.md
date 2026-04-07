# What a chain is in LangGraph
In LangGraph, a chain is simply a graph with a single, linear path—each node runs after the previous one, with no branching, loops, or conditional routing. It’s the most basic form of a LangGraph workflow.

Even though LangGraph is designed for complex, stateful, multi‑agent graphs, you can still use it to build simple, sequential pipelines. 

## 🧠 How a chain works conceptually
A LangGraph chain typically involves:

- A shared state (often chat messages)
- A sequence of nodes (functions, LLM calls, tool calls)
- Edges that connect nodes in order
- Optional tool bindings inside nodes

LangGraph represents it as a graph, but the execution is still linear.

## 🧩 Why use LangGraph for a chain?
Even for a simple chain, LangGraph gives you:

- State management (messages, memory, tool outputs)
- Deterministic execution
- Easy expansion into conditional or multi‑agent flows later
- Observability via LangSmith

## 🧱 Minimal LangGraph chain (the pattern you’ll use)
Here’s the basic structure :

### 1. Define the state
    - Usually a TypedDict or dataclass:
python
    ```
class State(TypedDict):
    messages: list
    ```
### 2. Define a node
    - A node is just a Python function that takes state and returns updated state:
python
```
def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}
```
### 3. Build the graph
This is where LangGraph differs from LangChain:

python
```
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("model", call_model)
graph.set_entry_point("model")
chain = graph.compile()
```
### 4. Run it
python
```
chain.invoke({"messages": ["Hello!"]})
```
That’s it — you built a LangGraph chain.

## 🧠 Why LangGraph calls this a “chain”
Because:

- There is one path
- No branching
- No loops
- No conditional edges
- No agents
- No tool routing logic
- It’s literally a straight line of execution.

LangGraph just represents it as a graph because the same structure can later grow into something more complex.

