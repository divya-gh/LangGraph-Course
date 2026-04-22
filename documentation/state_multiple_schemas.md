# ⭐ 1. What “Multiple Schemas” Means in LangGraph

#### Schema: A schema is the structure of your state — the fields, their types, and how they’re validated.

Real agents often need different schemas at different stages.

Example:

- Before the model runs — messages only
- After the model runs — include response
- After tools run — include tool_output

So LangGraph lets you define multiple schemas and switch between them depending on the node.

⭐ 2. Why Multiple Schemas Are Useful
✔ Different nodes need different state shapes
A tool node might need: python
```
{"query": str}
```
A model node might need: python
```
{"messages": list}
```
A summarizer node might need: python
```
{"messages": list, "summary": str}
```
✔ Prevents invalid state
If a node doesn’t need a field, it shouldn’t be required.

✔ Helps with validation

## ⭐ 3. Step 2 — Assign schemas to nodes
In LangGraph, each node can declare which schema it expects.

Example: python
```
graph = StateGraph(
    input=InputState,
    output=ModelState
)

graph.add_node("model", model_node, state_schema=ModelState)
graph.add_node("tool", tool_node, state_schema=ToolState)
```
This tells LangGraph:
    When entering the model node → validate state using ModelState
    When entering the tool node → validate using ToolState

## ⭐ 5. Step 3 — Reducers merge state safely
Reducers ensure that when a node returns updates, the state is merged without breaking the schema.

Example reducer: python
```
def add_response(state, update):
    return {**state, "response": update["response"]}
```
If the schema requires response, the reducer ensures it gets added.

## 6. Step 4 — Graph transitions switch schemas automatically
When the graph moves from one node to another:
- LangGraph checks the next node’s schema
- Validates the current state against that schema
- Filters out fields not allowed by the schema
- Ensures required fields are present
- Ensures field types match the schema
- Prevents bugs from missing, wrong, or extra fields


## ⭐ 7. Full Mini‑Example
Define schemas: python
```
class InputState(BaseModel):
    messages: list

class LLMState(BaseModel):
    messages: list
    response: str

class ToolState(BaseModel):
    messages: list
    response: str
    tool_output: str

#Define nodes 

def llm_node(state: InputState):
    return {"response": "Hello!"}

def tool_node(state: LLMState):
    return {"tool_output": "Tool ran successfully"}

#Build graph
graph = StateGraph(input=InputState, output=ToolState)

graph.add_node("llm", llm_node, state_schema=LLMState)
graph.add_node("tool", tool_node, state_schema=ToolState)

graph.add_edge("llm", "tool")
```
- Input → validated by InputState
- After LLM → validated by LLMState
- After tool → validated by ToolState

## ⭐ 8. Why This Matters for Real Agents
Multiple schemas let you build:

    - Chatbots
    - Tool‑using agents
    - Multi‑step workflows
    - Memory‑enhanced agents
    - Summarization pipelines
    - Each step can have its own state shape.

    -------------------------------------------------------------------
# 🟦 1. Input State
What it is:  The minimum information your graph needs to start running.

Think of it as:  “What does the user give me at the beginning?”

Example: python
```
class InputState(BaseModel):
    messages: list
```
This means:

    - The graph must receive messages when it starts.
    - Nothing else is required yet.

Why it matters:  It keeps your graph flexible and easy to call.

# 🟩 2. Output State
What it is:  The shape of the state when the graph finishes.

Think of it as:  “What should the graph produce at the end?”

Example: python
```
class OutputState(BaseModel):
    messages: list
    response: str
```
This means:

    - When the graph is done, it must return both messages and response.
    - If something is missing, LangGraph will throw an error.

Why it matters:  It guarantees your graph always returns a predictable result.

# 🟧 3. Private State
What it is:  Fields that nodes can use internally, but that are not required in the input or output.

Think of it as:  “Temporary scratch space for the agent.”

Example: python
```
class PrivateState(BaseModel):
    tool_output: str | None = None

```
This field:

    - Can be used by tool nodes
    - Is not required from the user
    - Does not need to appear in the final output

Why it matters:  
It keeps your input/output clean while still letting nodes store extra data.

## 🎯 Putting It All Together
Here’s a simple visual: 

User → [Input State] → Node 1 → Node 2 → Node 3 → [Output State]
                     ↑ private fields used here ↑

- Input state = what the user must provide
- Private state = what nodes can add/modify internally
- Output state = what the graph must return

## Example: 
```
#Step 1 — Define schemas

class InputState(BaseModel):
    messages: list

class PrivateState(BaseModel):
    tool_output: str | None = None

class OutputState(BaseModel):
    messages: list
    response: str

#Step 2 — Build graph

builder = StateGraph(Input_state,  input_schema= Input_state , output_schema=Output_State)

#Step 3 — Nodes use private state internally

def tool_node(state):
    return {"tool_output": "search results"}

def llm_node(state):
    return {"response": "Here is your answer!"}

#Step 4 — Output is clean
#The user only sees:

json
{
  "messages": [...],
  "response": "Here is your answer!"
}
```
The private tool_output never leaks out.

-------------------------------------------------------------------
