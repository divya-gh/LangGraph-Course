# Long Term Memory store - Collection Schema with TrustCall 

## 1. Why a “Collection Schema” Instead of a Profile?
Traditional chatbots store user info in one big profile object:

json
{
  "name": "Diya",
  "age": 31,
  "interests": ["gardening", "hiking"]
}
### This becomes a problem because:
- Updating the whole profile is error‑prone
- The model may overwrite or lose fields
- You can’t store multiple memories of the same type
- You can’t track when a memory was created
- You can’t store open‑ended facts

So instead, we use a collection of small memory entries, each representing one fact:
```
#json
{
  "content": "User likes gardening",
  "memory_type": "preference",
  "importance": 0.7
}
```
### This gives you:
- Flexibility
- Scalability
- Easy updates
- Better retrieval
- Better long‑term personalization

## 2. What Is a “Collection Schema”?

#### A collection schema is a Pydantic model that defines the structure of one memory item.

- Each memory item is stored as a separate document in your LangGraph store.
- Think of it like a row in a database table.

## 3. Step‑by‑Step: Defining a Collection Schema (Pydantic)
Below is the simplest and most useful schema for memory systems.
```
from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from datetime import datetime

class MemoryItem(BaseModel):
    content: str = Field(..., description="The main text of the memory")
    memory_type: Literal["fact", "preference", "goal", "identity", "other"] = Field(
        "other", description="Category of this memory"
    )
    importance: float = Field(
        0.5, ge=0.0, le=1.0, description="How important this memory is"
    )
    source: str = Field(
        "chat", description="Where this memory came from (chat, tool, system, etc.)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of memory creation"
    )
    tags: List[str] = Field(
        default_factory=list, description="Optional tags for filtering/search"
    )
```

✔ Why this schema works well
- content → the actual memory
- memory_type → helps categorize
- importance → helps ranking & forgetting
- source → helps debugging
- created_at → helps recency‑based retrieval
- tags → helps filtering
- This schema is open‑ended and grows with the user.

## 4. Step‑by‑Step: Creating a Memory Extractor (TrustCall)
We want the LLM to output a MemoryItem object whenever it detects something worth remembering.
```
from trustcall import create_extractor

memory_extractor = create_extractor(
    llm,
    tools=[MemoryItem],
    tool_choice="MemoryItem"
)
```
This forces the model to output a MemoryItem‑shaped dict.

## 5. Step‑by‑Step: Writing a Memory Node in LangGraph

This node:
- Reads the latest messages
- Asks the LLM if there is something worth remembering
- If yes → stores a new MemoryItem in the collection

```
from langchain_core.messages import SystemMessage

memory_sys_prompt = SystemMessage(content=""" You are a memory writer.

Your job:
- Read the latest conversation.
- Decide if there is a user fact, preference, goal, or identity worth remembering.
- If yes, create a MemoryItem.
- If not, return a MemoryItem with empty content.

Rules:
- Keep content short and factual.
- Do not invent information.
- Only store long-term relevant information.
""")

def memory_writer_node(state, store):
    messages = state["messages"]

    result: MemoryItem = memory_extractor.invoke({
        "messages": [memory_sys_prompt] + messages
    })

    if result.content.strip():
        namespace = (state["user_id"], "memories")
        store.put(namespace, None, result.

    return {}
```

### ✔ What this does
- Each memory becomes a new document
- Stored under namespace: (user_id, "memories")
- You build a growing memory collection

## 6. Step‑by‑Step: Retrieving Memories Later

When generating a response, you can retrieve relevant memories:

```
def retrieve_memories(store, user_id, query: str):
    namespace = (user_id, "memories")
    results = store.search(namespace, query=query, k=5)
    return [r.value for r in results]
```
You can feed these memories back into the LLM as context.

## 7. Why This Approach Is Better Than a Profile Schema

Profile Schema	                      Collection Schema

One big object	                      Many small entries
Hard to update	                      Easy to append
Risk of overwriting	                  No overwriting
Limited structure	                  Open‑ended
Hard to search	                      Easy to search
Not scalable	                      Scales naturally


**This is why modern agent architectures (LangGraph, ReAct, MemoryGPT, etc.) use collections instead of profiles.**

5. Why this collection approach is nice

- Flexible: you can add new memory types without changing a big profile.
- Robust: one bad memory doesn’t corrupt the whole profile.
- Searchable: semantic search over many small docs works better.
- Composable: different agents/nodes can write different kinds of memories into the same collection.

## Important :  To store collection as individual memory or object, make sure key is unique fo reach collection or JSON doc.

EX:
```
# define memory
class memory(BaseModel):
    content: str = Field(description="Content of the memory .For Example: User said he likes to travel to Europe")

#Define main memory collection schema
class Memory_collection(BaseModel):
    memories: List[memory] = Field(description="list of memories about the user")

# set up chat messages
msg = HumanMessage(content="Hi, Im Diya. I love reading books. I would love to visit the Library tomorrow")

# get response from the LLM
response = llm.with_structured_output(Memory_collection).invoke([msg])
response.memories

# define user_id and  namespace 
user_id = "1"
namespace = ('memories' , user_id)
# get key
import uuid


# set store
from langgraph.store.memory import InMemoryStore
store_memory = InMemoryStore()

# store memory objects as individual values with different keys
for m in response.memories:
    value = m.model_dump()
    print(value)
    key  = str(uuid.uuid4())
    print(key)
    store_memory.put(namespace, key , value)

```
Output:
```
memory = store_memory.search(namespace)
for m in memory:
    print(m.dict())
    print("\n")
```
- individual key and value are individual collection of profile about the user.
```
{'namespace': ['memories', '1'], 'key': '8c8e2937-bf9d-4d03-9b58-facf40482922', 'value': {'content': "User's name is Diya."}, 'created_at': '2026-06-07T19:53:18.409691+00:00', 'updated_at': '2026-06-07T19:53:18.409691+00:00', 'score': None}


{'namespace': ['memories', '1'], 'key': 'ac8d72ae-9826-4d7f-b598-bb559ef3faab', 'value': {'content': 'Diya loves reading books.'}, 'created_at': '2026-06-07T19:53:18.409691+00:00', 'updated_at': '2026-06-07T19:53:18.409691+00:00', 'score': None}


{'namespace': ['memories', '1'], 'key': '3a07f5fb-26e9-42fd-871e-349ae5f72b08', 'value': {'content': 'Diya plans to visit the library tomorrow.'}, 'created_at': '2026-06-07T19:53:18.409691+00:00', 'updated_at': '2026-06-07T19:53:18.409691+00:00', 'score': None}
```

------------------------------------------------------------------------
# ⭐ TrustCall does NOT support nested Pydantic models as tools.

### Schema:
```
class Memory_collection(BaseModel):
    memories: List[memory]
```
- contains a nested model (memory inside Memory_collection).
- Pydantic generates a $defs section for nested models.
- TrustCall cannot handle $defs and therefore ignores it.

#### That’s why you see:
```
Key '$defs' is not supported in schema, ignoring
```
And that’s why extraction fails silently.

## ⭐ The fix is simple: TrustCall tools must be FLAT models.
#### Meaning:
- No nested models
- No lists of models
- No union types
- No recursive structures
- TrustCall is designed to extract one object at a time, not collections.

## ⭐ Correct approach: Extract ONE memory at a time
#### Instead of:
```
tools=[Memory_collection]
```
#### You must use:
```
tools=[memory]
```

EX:Schema should be:
```
class memory(BaseModel):
    content: str = Field(description="Content of the memory")

# extractor
trustcall_extractor = create_extractor(
    llm,
    tools=[memory],
    tool_choice="memory",
    enable_inserts=True
)
```
This works perfectly.

## ⭐ Why TrustCall cannot extract lists
#### TrustCall internally:
- Validates a single schema
- Generates a JSON Patch for a single object
- Applies updates to a single object

#### It cannot:
- Patch a list
- Insert into a list
- Validate nested models
- Handle $defs from Pydantic
- So this will never work:

```
class Memory_collection(BaseModel):
    memories: List[memory]
```
**TrustCall will always ignore $defs and fail.**

## ⭐ The correct LangGraph pattern (recommended by LangChain team)

✔ Extract one memory
✔ Store it as one document
✔ Build a collection over time

#### Example:
```
result = trustcall_extractor.invoke({...})

if result.content.strip():
    store.put(namespace, None, result.model_dump())
```
Passing **None** lets the store auto‑generate a unique key.

### This is exactly how:
- MemoryGPT
- LangGraph course examples
- ReAct agents
- Long‑term memory agents
are built.
