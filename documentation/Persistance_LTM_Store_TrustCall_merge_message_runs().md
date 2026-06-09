# ⭐ What merge_message_runs() Does (Simple Explanation)

**merge_message_runs() is a LangChain utility that cleans up and normalizes a list of chat messages before sending them to the LLM.**

- Think of it as a message sanitizer.

#### It takes a list of messages like:
- SystemMessage
- HumanMessage
- AIMessage
- ToolMessage
- FunctionMessage

`…and merges or restructures them so the LLM receives a clean, consistent conversation history.`

## ⭐ Why You Need It in TrustCall
**TrustCall expects:**
- A clean list of messages
- No duplicates
- No fragmented tool calls
- No broken message sequences
- No repeated system prompts

**But in LangGraph, messages often accumulate like this:**
```
SystemMessage
HumanMessage
AIMessage
ToolCall
ToolResult
AIMessage
HumanMessage
...
```
- This can confuse the model.
- **merge_message_runs()** fixes that.

## ⭐ What It Actually Does (Step‑by‑Step)
#### ✔ 1. It merges consecutive messages from the same sender

**Example:**
```
Human: hi
Human: I like gardening
```
**Becomes:**
```
Human: hi\nI like gardening
```
#### ✔ 2. It collapses tool call + tool result pairs
- So the LLM sees a clean representation of the tool interaction.

#### ✔ 3. It ensures the system instruction is at the top
**code:**
```
[SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state["messages"]
```
- adds the TrustCall instruction as the first message.
- merge_message_runs() ensures it stays there.

#### ✔ 4. It removes redundant or malformed message chunks
- This prevents TrustCall from failing validation.

#### ✔ 5. It returns a clean, linear conversation
- Perfect for structured extraction.

## ⭐ Why This Matters for TrustCall Updates
**When you do:**
```
trust_extractor.invoke({
    "messages": updated_messages,
    "existing": existing_memory
})
```
**TrustCall needs:**
- A clean conversation
- A single system instruction
- No broken tool messages
- No duplicate messages

**Otherwise:**
- JSON Patch generation fails
- Tool calls break
- The model misinterprets the conversation
- You get weird errors
- merge_message_runs() prevents all of that.

## ⭐ Example Before and After
**Before merging:**
```
System: instruction
Human: hi
AI: hello
AI: how can I help?
Human: update my age
ToolCall: update_profile
ToolResult: {"age": 31}
AI: done
```
**After merging:**
```
System: instruction
Human: hi
AI: hello\nhow can I help?
Human: update my age
AI: (tool call + result merged cleanly)
```
Much cleaner for the model.

## ⭐ Final Summary
**merge_message_runs():**
- Cleans the conversation
- Merges consecutive messages
- Normalizes tool call sequences
- Ensures the system instruction is first
- Produces a clean message list for TrustCall
- Prevents JSON Patch errors
- Prevents malformed tool calls
- It’s a required step when using TrustCall inside LangGraph.

##  Example
```
#import 
from langchain_core.messages import merge_message_runs

# Trustcall instruction
TRUSTCALL_INSTRUCTION = """Reflect on following interaction.
Use the provided tools to retain any necessary memories about the user. 
Use parallel tool calling to handle updates and insertions simultaneously:"""

# Merge the chat history and the instruction
updated_messages=list(merge_message_runs(messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION)] + state["messages"]))

# Invoke the extractor
result = trustcall_extractor.invoke({"messages": updated_messages, 
                                    "existing": existing_memories})
```



