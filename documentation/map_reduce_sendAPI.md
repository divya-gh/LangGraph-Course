# Map-reduce-Send API

## Map‑Reduce in LangGraph = Break a big task into many small tasks (map) → run them in parallel → merge results (reduce).

## Send API = A special LangGraph feature that lets a node dynamically send work to other nodes at runtime.

This is how LangGraph does:

    - Map‑reduce
    - Dynamic branching
    - Fan‑out based on data
    - Multi‑agent dispatching
    - Parallel task creation

### First: The mental model
#### Imagine you have a list of items: Code
```
["apple", "banana", "orange"]
```
You want to process each item with the same node.

#### Instead of manually creating 3 nodes, you tell LangGraph:
- “For each item, send it to this node.”

##### LangGraph will:
- create 3 tasks
- run them in parallel
- collect their results
- pass them to the reducer node
This is map‑reduce.

### Exaample: Step 1 — Define your State
python
```
from typing import TypedDict, List

class State(TypedDict):
    items: List[str]
    processed: List[str]
```
- items → the list you want to map over
- processed → where results will be collected

### Step 2 — Write the “map” node
This node processes one item at a time.
python
```
def process_item(state: State):
    item = state["item"]   # single item
    return {"processed": [item.upper()]}
```
This node:
- receives one item
- returns a list with the processed value

### Step 3 — Use the Send API to fan‑out dynamically
This is the magic.

python
```
from langgraph.graph import Send

def map_node(state: State):
    # Create a Send task for each item
    return Send(
        "process_item",   # node to send work to
        [{"item": x} for x in state["items"]]  # one state per task
    )
```
What this does:
- For each item in state["items"]
- LangGraph creates a new task
- Each task runs process_item with its own mini‑state
- All tasks run in parallel
This is the map step.

### Step 4 — Write the “reduce” node
This node receives all processed results merged.
python
```
def reduce_node(state: State):
    # state["processed"] now contains all results
    print("All processed:", state["processed"])
    return state
```
LangGraph automatically merges:

["APPLE"]

["BANANA"]

["ORANGE"]

into:

Code
["APPLE", "BANANA", "ORANGE"]

### Step 5 — Build the graph
python
```
from langgraph.graph import StateGraph

graph = StateGraph(State)

graph.add_node("map", map_node)
graph.add_node("process_item", process_item)
graph.add_node("reduce", reduce_node)

graph.add_edge("map", "process_item")
graph.add_edge("process_item", "reduce")

graph.set_entry_point("map")
graph.set_finish_point("reduce")
```

### Step 6 — Run it
python
```
app = graph.compile()

result = app.invoke({"items": ["apple", "banana", "orange"]})
print(result)
Output:

Code
{'items': [...], 'processed': ['APPLE', 'BANANA', 'ORANGE']}
```

## Summary:
## Map-Reduce with the Send API (Beginner Guide)
```
from langgraph.types import Send
```

### What is Map-Reduce?
- Map: break a big task into many small tasks
- Reduce: merge all results into one final output

### What is the Send API?
Send lets a node dynamically create tasks at runtime.
Each task runs the same node with different input.
LangGraph runs all tasks in parallel.
```
return [send(node_name , {'key': value}) for value in state['key']]
```
sends state value as an input to the node 

### Steps:
1. Create a state with a list of items.
2. Write a map node that returns Send("process_item", list_of_states).
3. Write a process_item node that handles one item.
4. Write a reduce node that receives all merged results.
5. Build the graph and run it.

### Why this is powerful?
- Perfect for parallel processing
- Great for multi-agent dispatching
- Works with LLMs, tools, and subgraphs
- Lets you scale tasks dynamically

