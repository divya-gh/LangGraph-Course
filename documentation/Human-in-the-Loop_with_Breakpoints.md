# Human in the Loop:

## Human in the loop (HITL): you pause the graph, a human looks at what the agent is about to do, then decides whether and how to continue. 

### Advantages: human-in-the-loop:

##### (1) Approval - We can interrupt our agent, surface state to a user, and allow the user to accept an action
##### (2) Debugging - We can rewind the graph to reproduce or avoid issues
##### (3) Editing - You can modify the state

## Breakpoints: predefined pause points in the graph where execution stops so a human can inspect/approve/modify state before continuing.

## 1: Understanding the core idea:

### Goal: Let the agent run most of the time, but pause at critical moments so a human can:

    - Approve an action (e.g., run a tool, send an email,check the draft)
    - Debug what went wrong
    - Edit the state (e.g., fix a tool input, change a message) 

### LangGraph gives you two main mechanisms: 
Two main ways to pause in LangGraph

##### 1. Static breakpoints → defined when you compile the graph
##### 2. Dynamic interruptions → raised at runtime from inside a node

## 1. Static breakpoints (interrupt_before / interrupt_after)
    - You tell LangGraph: “Pause before this node” or “Pause after this node.”

#### Example: interrupt_before=["tools"] → pause before the tools node runs.

## 2. Dynamic interrupts (interrupt())
    - You call a function inside a node that says: “Stop here and wait for human input.”

#### Example: approved = interrupt("Do you approve this action?")

Note: Both patterns are just two flavors of the same idea: stop → ask human → resume.

---------------------------------------------------

## 1. Static breakpoints (interrupt_before / interrupt_after)
- “Pause before any tool call so a human can approve it.”


### Example:

#### Step 1: Define your tools node
You usually have a node that actually executes tool calls (e.g., calling an API, checking a price, sending an email).

#### Step 2: Build your graph and add the tools node

#### Step 3: Compile with a breakpoint before tools
python
```
graph = builder.compile(
    interrupt_before=["tools"]  # <-- breakpoint
)
```
##### This tells LangGraph:

“Whenever execution is about to enter the tools node, pause and surface an interrupt instead of running it immediately.”

#### Step 4: Run the graph and detect the pause
When you run/stream the graph, you’ll see that it stops right before tools:
```
config = {"configurable": {"thread_id": "user-1"}}

for event in graph.stream({"input": "some request"}, config, stream_mode="updates"):
    print(event)
    # At some point you’ll see an interrupt instead of tools executing
```
At this moment, the graph is waiting for you.
The state is saved (via the checkpointer), and nothing in tools has run yet.

### Check state = graph.get_State(thread)
```
thread = {"configurable": {"thread_id": "1"}}
```
State shows what node is next.

#### Step 5: Show the pending action to the human
In your app (UI, notebook, CLI), you typically:

Read the current state (e.g., which tool the agent wants to call, with what arguments).

Display something like:

    “The agent wants to call check_price("laptop"). Approve?”
Note: This part is your UI logic, not LangGraph itself.

#### Step 6: Human decides: approve / edit / reject
You then collect human input, for example:

    Approve → “Yes, run this tool call.”

    Edit → “Change item from ‘laptop’ to ‘gaming laptop’.”

    Reject → “Don’t run this tool; ask the user for more info instead.”

You encode that decision into the next input or updated state you send when resuming.

#### Step 7: Resume the graph
To continue from the breakpoint, you call the graph again with the same thread_id and your human decision:
```
from langgraph.types import Command

config = {"configurable": {"thread_id": "user-1"}}

# Example: human approved
command = Command(resume={"approved": True})

for event in graph.stream(command, config, stream_mode="updates"):
    print(event)
```
Because the thread_id is the same, LangGraph:

    Loads the saved state at the breakpoint.
    Uses your Command(resume=...) as the “answer” to the interrupt.
    Continues execution—now it can safely run tools knowing a human approved.

---------------------------------------------
## 2. Dynamic interrupts (interrupt())