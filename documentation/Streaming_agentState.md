# 🌊 What “Streaming” Means in LangGraph ?

#### Streaming = getting partial results from your graph while it is still running.

Instead of waiting for the whole graph to finish, LangGraph lets you see:

    - messages as they are generated
    - node outputs as they happen
    - state updates step‑by‑step

- This makes your app feel fast, responsive, and alive — especially when LLMs take time to respond.
###### EX: Think of it like watching a YouTube video buffer vs. waiting for the whole video to download before watching.

## ⭐ Why Streaming Is Important?
- Without streaming:

    - Your app freezes until the LLM finishes
    - The user sees nothing happening
    - Long responses feel slow

With streaming:

    - You show text as it is generated
    - You can display progress
    - You can update UI in real time
    - The user feels the app is fast
    - Human in the loop system allows users to interact directly with graphs in various ways.

This is why LangGraph emphasizes streaming — it dramatically improves user experience.

## How Streaming Works in LangGraph :
LangGraph graphs run node‑by‑node.

Treditionally, When you use: python
```
graph.invoke(...)
```
You get only the final result.

When you use: python
```
graph.stream(...)
```
You get chunks of data as each node finishes.

## Types of streaming:
#### 1. syncronous *'graph.stream'* : normal Python code that runs one step at a time.
python
```
for chunk in graph.stream(...):
    print(chunk)
```
and Python yields each chunk synchronously, code is processed the data is delivered for every chunk generated.

#### When to use?
    - You’re in a Jupyter notebook 
    - You’re writing simple scripts
    - You don’t need concurrency
    - You want to see output as it happens
This is what the LangGraph course uses.

#### 2. Async streaming = streaming using Python’s async / await.
python
```
async for chunk in graph.astream(...):
    print(chunk)
```
This allows:
    concurrency
    non‑blocking execution
    running multiple tasks at the same time
integrating with async web servers (FastAPI, etc.)

#### when to use async streaming?:
    - You’re building a web app
    - You’re using FastAPI / Starlette / Sanic
    - You want multiple users at once
    - You want non‑blocking LLM calls
**❌ You do NOT need async streaming in a notebook.**

---------------------------------------------------------------------

# 🪜 Step‑by‑Step Guide
Let’s build a tiny example 

#### Step 1 — Define your state :
python
```
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

#### Step 2 — Create a simple LLM node
python
```
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def chatbot_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```
#### Step 3 — Build the graph
python
```
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()
```
#### Step 4 — Normal (non‑streaming) call
python
```
result = graph.invoke({"messages": [HumanMessage(content="Hi!") ]})
print(result)
```
You wait… then get the final answer.

#### ⭐ Step 5 — Streaming call (the important part)
python
```
for chunk in graph.stream(
    {"messages": [HumanMessage(content="Hi!") ]},
    stream_mode="messages"
):
    print("CHUNK:", chunk)
```
##### You will see output like: 
```
CHUNK: {'messages': [AIMessage(content='Hello!')]}

```
This appears as soon as the node finishes, not at the end of the whole graph.

----------------------------------------------------------------------
# 🎛 Streaming Modes :
- LangGraph supports different streaming modes depending on what you want to see.

##### 1. stream_mode="messages"
Streams chat messages as they are produced.

Best for: chat UIs

##### 2. stream_mode="updates"
Streams state updates after each node runs.

Best for: debugging or progress bars

##### 3. stream_mode="values"
Streams the entire state each time it changes.

###### Best for: dashboards or visualizations

##### 4. stream_mode="custom"
*"custom"* is a user‑defined streaming channel.  
- You only get "custom" events if you create them yourself inside your graph.
- If you don’t emit custom events, then "custom" will stream nothing.
- "custom" is not built‑in like "messages" or "updates".
    - It only streams events that you explicitly emit.
    - Useful for progress bars, logs, tool outputs, etc.
    - Safe to ignore if you don’t need custom events.

### 🧩 Example: Streaming all mode options
python
```
for chunk in graph.stream(
    {"messages": [HumanMessage(content="Tell me a joke")]},
    stream_mode=["messages", "updates",'values' , 'custom']
):
    print(chunk)
```
You’ll see:

    - the LLM message
    - messages data or values
    - the state update
    - the final output
    - custom events
All in real time.

### 🌟 Why does "custom" exist?
Sometimes you want to stream your own data, for example:

    - progress percentage
    - intermediate calculations
    - tool results
    - logs
    - UI updates
    - partial summaries
    - anything you want
very useful for tracing and debugging.

### How it works? 
LangGraph lets you send these custom events using: python
```
from langgraph.types import StreamEvent

yield StreamEvent("custom", {"progress": 50})
```
Then, if your app listens to: python
```
stream_mode=["updates", "custom"]
```
you will receive:
    - normal updates
    - your custom events

### 🌟 Step‑by‑Step Example for *'custom'* mode
##### 1. Create a node that emits a custom event
python
```
from langgraph.types import StreamEvent

def my_node(state):
    # send a custom event
    yield StreamEvent("custom", {"progress": "50%"})
    
    # return normal state
    return {"messages": ["Done!"]}
```

##### 2. Build your graph normally
python
```
builder.add_node("my_node", my_node)
```

##### 3. Stream with "custom"
python
```
for chunk in graph.stream(
    {"messages": []},
    stream_mode=["updates", "custom"]
):
    print(chunk)
```
#### 4. Output you will see
Code
```
{'type': 'custom', 'data': {'progress': '50%'}}
{'type': 'updates', 'data': {...}}
```
Note:  If you don’t emit custom events, only updates are streamed as there is nothing to stream.

---------------------------------------------------------------------

# What are the streaming formats in langGraph?

## 2 Types : LangGraph has two output formats for streaming:
#### 1. V1 : Old format **version="v1"** - default
This is the original streaming format.

Chunks look like: python
```
{'messages': [...]} 
or
{'updates': {...}}
```
It works fine, but it’s not standardized.
#### V2 : New format **version="v2"** -recomended
This is the new, structured, consistent streaming format.

Chunks look like: python
```
{
  "type": "messages",
  "data": {...}
}
or:

{
  "type": "updates",
  "data": {...}
}
```
## ✔ Why v2 exists:

    - cleaner
    - consistent
    - easier for UI frameworks
    - easier for debugging
    - supports custom event types

#### ✔ How to enable v2:
python
```
from langchain_core.messages import HumanMessage

for chunk in graph.stream(
    {"messages": [HumanMessage(content="Hi!")]},
    stream_mode=["messages", "updates"],
    version="v2"
):
    print(chunk)

# Output looks like: Code

{'type': 'messages', 'data': {...}}
{'type': 'updates', 'data': {...}}

```
✔ recomended :  V2
Yes — it’s clearer and easier to understand.

