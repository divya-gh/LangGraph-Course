# 1. Short term memory
    Agent built with short-term memory (MemorySaver) only persists untill the that perticular session runs. meaning, restaring the agent or notebook or karnel will erase the memory. 

#### Explaination : 
When you build a chatbot with LangGraph, it has state (messages, memory, summaries, etc.).

If you don’t save that state, it disappears when:

   - the process restarts
    - the server crashes
    - you close your notebook
    - A checkpointer is how LangGraph remembers past runs.
SqliteSaver is a checkpointer that stores this state in a database.

Database:  Storage where hystorical data can be stored permanently. 
Types: SQLite , PostGress etc

## 2. What is SQLite, in simple terms?
SQLite is a tiny database stored in a single file on your disk.
No server, no setup, no config.

Perfect for:
    local experiments
    small apps
    prototypes
You interact with it using Python’s built‑in sqlite3 module.

## 3. Two ways to create a SQLite connection:

### 3.1 In‑memory database (temporary)
- Creates a database in RAM (disappears when program ends)

python
```
import sqlite3
conn = sqlite3.connect(":memory:", check_same_thread=False)
```
####    Pros: fast, clean, nothing on disk
####    Cons: nothing is saved after restart

### 3.2 File‑based database (persistent)

EX: python
```
import sqlite3

db_path = "state_db/example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)

```
If example.db doesn’t exist, SQLite creates it.
Data is stored on disk → survives restarts.

you can also download a pre‑made DB if it doesn’t exist:
python
```
!mkdir -p state_db && [ ! -f state_db/example.db ] && wget -P state_db https://github.com/langchain-ai/langchain-academy/raw/main/module-2/state_db/example.db
```
- You can ignore that at first—it’s just pre‑seeding the file.

## . What is SqliteSaver?
*SqliteSaver* is a LangGraph checkpointer that uses your SQLite connection to store graph state.

EX: python
```
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver(conn)

```

*memory* is now an object that knows how to:
    - save state to SQLite
    - load state from SQLite
    - resume conversations / workflows

## 5. How to plug it into a LangGraph?

### 5.1 Build your graph as usual

EX: python
```
from langgraph.graph import StateGraph, START, END

def my_node(state):
    # ... do something ...
    return state

builder = StateGraph(dict)  # or our TypedDict state
builder.add_node("my_node", my_node)
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)
```
### 5.2 Compile with the SQLite checkpointer

EX: python :
```
graph = builder.compile(checkpointer=memory)

```
Now this graph:
    - will save state into example.db
    - can resume from previous runs using a thread_id (or similar config)

### 5.3 Running with a thread id
EX: python
```
config = {"configurable": {"thread_id": "diya-chat-1"}}

graph.invoke({"messages": []}, config=config)

```
Note: Every time you call graph.invoke with the same thread_id,
LangGraph will load previous state from SQLite, update it, and save it back.
That’s how you get external memory for your chatbot.