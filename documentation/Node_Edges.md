










































# Built-in tool Node
```
from langgraph.prebuilt import ToolNode
```
  
langGraph has a built in Tool Node that :

➤ A node that receives a tool call from the LLM
➤ Executes the corresponding Python function
➤ Returns the result back into the message stream

- Graph node that executes bound Python tools
- Invoked when the LLM requests a tool call
- Runs the corresponding Python function and captures output
- Returns the result back into the conversation/message stream
- Serves as the agent's "hands" to perform external actions

It’s the “hands” of your agent — the part that actually does thing

# Tool-condition
```
from langgraph.prebuilt import tools_condition
```

*tools_condition* is a built‑in routing helper in LangGraph’s prebuilt ToolNode system.
It’s part of the langgraph.prebuilt.tool_node module, and it exists to make tool‑calling graphs easier to build without writing your own router logic.

## ⭐ What tools_condition is

It’s a prebuilt conditional router that looks at the last message in state and decides:

- Should the graph go to the tool‑execution node?
- Or should it skip tools and continue normally?

In other words:

tools_condition = a ready‑made version of the route() function you wrote manually.

It checks:

- Does the last AI message contain tool_calls?
- If yes → route to the tool execution node
- If no → route to END (or whatever you configure)

## ⭐ Why it exists
Because everyone who builds a tool‑calling graph ends up writing the same logic:

python
```
if last_message.tool_calls:
    go to tool_execute_node
else:
    end
```
So LangGraph provides a built‑in version to save you from writing your own router.

## How to use it?
```
from langgraph.prebuilt import tools_condition

builder2.add_conditional_edges(
    "Tool_Calling_Node",
    tools_condition,
    {
        "tool_execute_node": "tool_execute_node",
        END: END
    }
)
```