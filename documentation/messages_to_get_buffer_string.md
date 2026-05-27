# What is get_buffer_string ?
It’s a helper function used by LangChain’s memory classes (like ConversationBufferMemory) to:

## ➜ Convert a list of messages
[HumanMessage, AIMessage, HumanMessage, ...]

## ➜ Into a single formatted string
Code
```
Human: Hello
AI: Hi there!
Human: Tell me about LangChain
```
This is the “buffer string” — a plain text version of the conversation history.

## Use it in LangChain when:

    - passing chat history into an LLM prompt
    - summarizing memory
    - storing memory
    - retrieving memory
    - debugging multi‑turn flows
You rarely call it manually — it’s mostly internal.


### Example (simple)
python
```
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)

memory.chat_memory.add_user_message("Hello")
memory.chat_memory.add_ai_message("Hi!")

print(memory.buffer)
```
Internally, this calls: python
```
get_buffer_string(memory.chat_memory.messages)
```
## Example (manual use)
python
```
from langchain.memory.utils import get_buffer_string
from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="Hello"),
    AIMessage(content="Hi there!")
]
print(get_buffer_string(messages))
```
Output: Code
```
Human: Hello
AI: Hi there!
```

## When you should care
You should pay attention to get_buffer_string if:

✔ You’re debugging memory
✔ You’re converting messages into a prompt
✔ You’re summarizing interviews
✔ You’re building a STORM‑style multi‑turn interview loop
✔ You’re storing messages inside LangGraph state
Otherwise, you can safely ignore it.

-----------------------------------------------------------
## Optional: Custom Prefix Style
If you prefer: Code
```
Interviewer: ...
Expert: ...
```
Use a custom formatter: python
```
def custom_buffer(messages):
    lines = []
    for m in messages:
        role = m.name or "AI"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines)
```

---------------------------------------------------------
## Using prefix for AIMessage , SystemMessage and HumanMessage

To use the prefix with prefered names instead of AI: or Human: in the string conversion,
- use parameters Human_prefix = "name" or AI_prefix = "name"
- seperater \n to seperate the messages

Example:
```
messages = HumanMessage(content='Hello, I am Aris Thorne, a Senior Systems Analyst. It is a privilege to sit down with you, Dr. Elena Vance, to dissect the architectural intricacies of LangGraph.\n\nGiven your focus on state persistence and data flow integrity, let’s begin: \n\nIn a distributed, long-running agentic process, how does LangGraph’s state management prevent "state drift" when multiple asynchronous nodes attempt to mutate the shared state simultaneously?', additional_kwargs={}, response_metadata={}, name='Interviewer', id='993c7d93-8b8f-4c5a-97de-c1a6fbe21c1f'), 
AIMessage(content='In LangGraph, state management is architected around a single shared memory object that acts as the source of truth for the entire workflow [3]. To maintain integrity during mutations, LangGraph utilizes reducer logic, which governs how updates from various nodes are merged into the shared state [3])

# save messages as interview
    
interview = get_buffer_string(messages, human_prefix= "Interviewer" , ai_prefix="Expert", message_separator="\n")
```
Output:
```
Interviewer: Hello, I am Aris Thorne, a Senior Systems Analyst. It is a privilege to sit down with you, Dr. Elena Vance, to dissect the architectural intricacies of LangGraph.

Given your focus on state persistence and data flow integrity, let’s begin:
In a distributed, long-running agentic process, how does LangGraph’s state management prevent "state drift" when multiple asynchronous nodes attempt to mutate the shared state simultaneously?

Expert: In LangGraph, state management is architected around a single shared memory object that acts as the source of truth for the entire workflow [3]. To maintain integrity during mutations, LangGraph utilizes reducer logic, which governs how updates from various nodes are merged into the shared state [3]. By defining clear state schemas and controlling these merge operations through reducers, the system ensures that concurrent or sequential updates are handled consistently rather than causing uncontrolled state drift [3].

-------------------------------------------------------

