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
- Since SQLite is tiny, fast , filebased, Python bundles it so developers can use a database without installing anything.
- You interact with it using Python’s built‑in sqlite3 module.

### ⭐ Do you need to install SQLite?
No — you already have it. SQLite is built directly into Python.
Ex: python
```
import sqlite3
```
comes with every standard Python installation. Meaning, No pip install , No server, No configuration, No setup . ust import and use.

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

### Create the folder statedb first
Use Python to safely create it: python
```
import os
os.makedirs("state_db", exist_ok=True)
```
This works on Windows, Mac, Linux, and Jupyter.

Then you can safely run: python
```
import sqlite3
db_path = "state_db/example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
Now SQLite will create the file: state_db/example.db
```
### ⭐ Where is the folder located?
Folder is created in the same directory as the notebook.

### confirm it exists : python
```
import os
os.listdir("state_db")
```
You should see: ['example.db']

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
Note: - Every time you call graph.invoke with the same thread_id,
LangGraph will load previous state from SQLite, update it, and save it back.
      - start a new thread (new Id) to start a new session.

That’s how you get external memory for your chatbot.

----------------------------------------------------------------------
# Resetting and Deleting external DB

LangGraph memory is stored in your SQLite database file:

Code
```
state_db/example.db
```
To reset memory, you must clear or delete this file so the graph starts fresh.

## 3 Safe options

### Option 1 — Delete the database file (recommended)
This is the cleanest and most reliable method.

python
```
import os

db_path = "state_db/example.db"

if os.path.exists(db_path):
    os.remove(db_path)
    print("Memory reset: example.db deleted.")
else:
    print("Database file does not exist.")
```
Then recreate a fresh DB automatically: python
```
import sqlite3
conn = sqlite3.connect("state_db/example.db", check_same_thread=False)

```
This gives you a brand‑new empty memory.

### Option 2 — Delete the entire folder
If you want a full wipe: python
```
import shutil

shutil.rmtree("state_db")
print("state_db folder removed.")

```
Then recreate it: python
```
import os
os.makedirs("state_db", exist_ok=True)
```
And reconnect: python
```
import sqlite3
conn = sqlite3.connect("state_db/example.db", check_same_thread=False)
```
### Option 3 — Clear all tables inside the DB (advanced)
If you want to keep the file but erase all stored state:

python
```
import sqlite3

conn = sqlite3.connect("state_db/example.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    cursor.execute(f"DELETE FROM {table[0]};")

conn.commit()
conn.close()

print("All memory tables cleared.")
```
deletes all the tables: Keeps the file but clears the data
