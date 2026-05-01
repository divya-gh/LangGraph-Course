# 📘 Dynamic Breakpoints in LangSmith API

Dynamic Breakpoints (also called interrupts) allow your LangGraph agent to pause execution, wait for human input, and then resume exactly where it left off.

This is essential for human‑in‑the‑loop workflows such as approvals, confirmations, or branching decisions.

## 1. What Are Dynamic Breakpoints?
A dynamic breakpoint is created by calling:

python
```
from langgraph.types import interrupt

value = interrupt("Your message here")
```
#### When the graph reaches this line:

    - Execution pauses
    - LangSmith saves the state
    - The interrupt message is streamed back to your client
    - The graph waits until you resume it
    - When resumed, interrupt() returns the value you provide.

## 2. Example Graph (Dynamic Breakpoint)
python
```
from langgraph.graph import StateGraph
from langgraph.types import interrupt
from typing import TypedDict, Optional

class State(TypedDict):
    input: str
    approved: Optional[bool]

def approval_node(state: State):
    approved = interrupt("Do you want to approve this action?")
    return {"approved": approved}

builder = StateGraph(State)
builder.add_node("approval", approval_node)
builder.set_entry_point("approval")
```

### IMPORTANT: 
- Do NOT pass a custom checkpointer in LangSmith API graph = builder.compile()
- When deployed to LangSmith API, persistence is handled automatically.
- Do not use InMemorySaver() or any custom checkpointer.

## 3. Running the Graph in LangSmith API (Streaming)
python
```
input_dict = {"input": "Tell me a joke!"}

async for chunk in client.runs.stream(
    thread["thread_id"],
    assistant_id="Dynamic_Breakpoints",
    input=input_dict,
    stream_mode="values"
):
    print("Event:", chunk.event)
    print(chunk.data)
```
#### Gives interrupt output: python
```
{
  "input": "Tell me a joke!",
  "__interrupt__": [
    {
      "value": "Do you want to approve this action?",
      "id": "743d2be80f6b3dd27fccccd11e7d00cc"
    }
  ]
}
```
#### This means:

    - The graph paused
    - It is waiting for your response
    - You must now resume using the interrupt ID

## 4. Resuming After an Interrupt
When you detect an interrupt, extract its ID: python
```
interrupt_id = chunk.data["__interrupt__"][0]["id"]
```
#### Then resume the run: python
```
await client.runs.wait(
    thread['thread_id'],
    assistant_id = 'Dynamic_Breakpoints',
    command=Command(resume="YES")   # (3)!
)
```
#### What happens now?
Inside your node: python
```
approved = interrupt("Do you want to approve this action?")
```
#### becomes:
```
approved = True
```
#### And the graph continues execution normally.

## Capture State
Shows exactly where the state is and can be used to extract interrupt_id
```
state = await client.threads.get_state(thread['thread_id'])
state
```
## 6. Key Rules to Remember
    - Do not use custom checkpointers in LangSmith API
    - Always resume using client.runs.wait()
    - command=Command(resume="YES")  becomes the return value of interrupt()
    - Interrupts can return any JSON‑serializable value