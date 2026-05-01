# Breakpoints: predefined pause points in the graph where execution stops so a human can inspect/approve/modify state before continuing.

human-in-the-loop:

(1) Approval - We can interrupt our agent, surface state to a user, and allow the user to accept an action
(2) Debugging - We can rewind the graph to reproduce or avoid issues
(3) Editing - You can modify the state

## 🧠 Why Interrupts Matter
Interrupts let you build:

    - Human approval steps
    - “Choose your own adventure” flows
    - Multi‑turn agent conversations
    - Workflows that need human decisions
    - Error‑recovery steps (“What should I do now?”)


## Two main ways to pause in LangGraph

##### 1. Static breakpoints → defined when you compile the graph
##### 2. Dynamic interruptions → raised at runtime from inside a node

## 1. Static breakpoints (interrupt_before / interrupt_after)
    - You tell LangGraph: “Pause before this node” or “Pause after this node.”

#### Example: interrupt_before=["tools"] → pause before the tools node runs.

## 2. Dynamic interrupts (interrupt()):
    - You call a function inside a node that says: “Stop here and wait for human input.”

#### Example: approved = interrupt("Do you approve this action?")

## Basics:
Before interrupt: your graph is running node by node.

At interrupt(): execution stops, state is saved, and a message is sent back to you (the caller).

After human responds: you “resume” the graph, and it continues as if interrupt() just returned that human’s answer.

Note: **Important: interrupts require a checkpointer.**

## How it works?:

1. - Unlike static breakpoints (which pause before or after specific nodes), interrupts are dynamic: they can be placed anywhere in your code and can be conditional based on your application logic.
python
```
from langgraph.types import interrupt

def approval_node(state: State):
    # Pause and ask for approval
    approved = interrupt("Do you approve this action?")

    # When resumed, `approved` will be whatever you passed to Command(resume=...)
    return {"approved": approved}
```
#### What happens when this line runs?
python
```
approved = interrupt("Do you approve this action?")
```
        - The graph stops right there.
        - LangGraph saves the current state (so it can continue later).
        - The value "Do you approve this action?" is sent back to the caller as an interrupt payload.
        - The node does not continue yet.

2. - Checkpointing keeps your **place**(memory saved): the checkpointer writes the exact graph state so you can resume later, even when in an error state.

    -  (e.g., in-memory or database) to store:

        - Which node you were in.
        - The current state.
        - The fact that you stopped at an interrupt.
        - This is what lets you resume later, even if your process restarts.

3. - thread_id is your pointer: set config={"configurable": {"thread_id": ...}} to tell the checkpointer which state to load.
    - You pass a thread_id in config: python
```
config = {"configurable": {"thread_id": "thread-1"}}
```
This tells LangGraph:
    “Use the saved state for this specific thread when resuming.”

- Same thread_id = continue the same run  
- New thread_id = start a fresh run with empty state.

4. - Interrupt payloads surface via chunk["interrupts"]: 
when streaming with version="v2", the values you pass to interrupt() appear in the interrupts field of values stream parts so you know what the graph is waiting on.
python
```
from langgraph.types import Command  # you'll use this later to resume

config = {"configurable": {"thread_id": "thread-1"}}

result = graph.invoke({"input": "data"}, config=config, version="v2")
```
    - The graph runs.

#### When it hits interrupt("Do you approve this action?"):

    - Execution pauses.
    - State is saved.
    - result contains an interrupt.

In v2, you’ll see something like: python
```
print(result.interrupts)
# > (Interrupt(value='Do you approve this action?'),)
```
#### This tells you:
    “Your graph is waiting for an answer to this question.”

5. - The thread_id you choose is effectively your persistent cursor. Reusing it resumes the same checkpoint; using a new value starts a brand-new thread with an empty state.

#### resuming after the interrupt
    - Now you have to resume with the human’s answer.

#### Get the human’s response:
- Example: user clicks “Approve” in your UI → you decide True.

#### Call invoke again with Command(resume=...)
python
```
from langgraph.types import Command

config = {"configurable": {"thread_id": "thread-1"}}  # same thread_id!

graph.invoke(Command(resume=True), config=config, version="v2")
```
- You must use the same thread_id as before.

#### Command(resume=True) means:
    “Continue the graph, and inside the node, make interrupt() return True.”

#### Inside approval_node, this line now behaves like:
python
```
approved = interrupt("Do you approve this action?")
# On resume, this becomes:
approved = True
```
#### Then the node returns:  python
```
return {"approved": approved}
# => {"approved": True}
```
- And the graph continues to the next node as normal.

## Important details to remember:

1. Where does the node restart?

    - When you resume, the node restarts from the beginning, but:
    - When it reaches interrupt() again, it does not pause.
    - Instead, interrupt() immediately returns the value you passed in Command(resume=...).

2. What can you pass to interrupt() and resume?

    - Any JSON-serializable value: String, number, list, dict, etc.

3. Example: python
```
feedback = interrupt({"question": "Approve?", "options": ["yes", "no"]})
```
Later: python
```
graph.invoke(Command(resume="yes"), config=config, version="v2")
```
- Command(resume=...) is special

- It’s the only Command pattern you pass as input to invoke()/stream() to continue an interrupted run.

- Other Command options like update, goto, graph are meant to be returned from nodes, not passed as input.

## When you call interrupt, here’s what happens:

- Graph execution gets suspended at the exact point where interrupt is called
- State is saved using the checkpointer so execution can be resumed later, In production, this should be a persistent checkpointer (e.g. backed by a database)
- Value is returned to the caller under __interrupt__; it can be any JSON-serializable value (string, object, array, etc.)
- Graph waits indefinitely until you resume execution with a response
- Response is passed back into the node when you resume, becoming the return value of the interrupt() call