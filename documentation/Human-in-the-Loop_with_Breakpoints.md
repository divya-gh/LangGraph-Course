# Human in the Loop:

## Human in the loop (HITL): you pause the graph, a human looks at what the agent is about to do, then decides whether and how to continue. 

### Advantages: human-in-the-loop:

(1) Approval - We can interrupt our agent, surface state to a user, and allow the user to accept an action
(2) Debugging - We can rewind the graph to reproduce or avoid issues
(3) Editing - You can modify the state

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

#### 1. User Aproval: 
- Ask the user to continue with the tool_Call
- If user approves,  pass"None" to the graph and continue

```
# user approval
if toolcall:
    user_approval = input("Do you want to continue?(yes/no): ").lower()
    if user_approval == 'yes':
        # pass None as input to the graph and continue from the last statenusing the thread_ID
        async for event in client.runs.stream(
            thread["thread_id"],
            "agent",
            input=None,
            stream_mode="values",
            interrupt_before=["tools"],
        ):
            print(f"Receiving new event of type: {event.event}...")
            messages = event.data.get('messages', [])
            if messages:
                print(messages[-1])
            print("-" * 50)
        
```
#### Editing state:
- You can modify the state after the graph interrupted.
```
# Get State
state = graph.get_state(thread_config)

#update with the new message
graph.update_state(
    thread,
    {"messages": [HumanMessage(content="No, actually multiply 3 and 3!")]},
)
# re-run to continue
for event in graph.stream(None, config, stream_mode="values"):
        print(event)

```
- Messages will be annotated to the state with add_messages function since we use the reducer *'MessagesStte'*.


#### Step 7: Resume the graph - Method 1
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

#### Step 7: Resume the graph - Method 2

If user says run-tool, using the same thread_ID which saves previous state, send empty msg as *intput(None)* to the graph and re-run the graph as before
```
for event in graph.stream(None, config, stream_mode="values"):
        print(event)
```

---------------------------------------------
## 2. Dynamic interrupts (interrupt())



Step‑by‑step: using interrupt() inside a node
Sometimes you want to pause inside a node, not just before/after it. That’s where interrupt() comes in.

Step 1: Create a node that calls interrupt()
python
from langgraph.types import interrupt

def approval_node(state):
    # Ask for approval and pause here
    approved = interrupt("Do you approve this action?")
    return {"approved": approved}
Step 2: Add it to the graph
python
builder.add_node("approval", approval_node)
builder.add_edge("agent", "approval")
builder.add_edge("approval", "tools")

Step 3: Compile with a checkpointer
Interrupts require a checkpointer:

python
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)
Step 4: Run until interrupt
python
config = {"configurable": {"thread_id": "user-1"}}

for event in graph.stream({"input": "hello"}, config, stream_mode="updates"):
    print(event)
    # You’ll see an interrupt event when approval_node runs
The graph pauses at interrupt(...) and returns the message "Do you approve this action?" to you.

Step 5: Resume with human answer
Once the human answers (e.g., True or "No, change X"), you resume:

python
from langgraph.types import Command

command = Command(resume=True)  # or some other JSON-serializable value

for event in graph.stream(command, config, stream_mode="updates"):
    print(event)
That True becomes the value of approved inside approval_node, and the graph continues.

