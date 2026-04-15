# How do the LLM model coommunicate with external Tools?

### Analogy:
- Talking to an LLM is like talking to a person.
- Talking to an API is like filling out a form.
- The “payload” is the filled-out form.

#### Humans talk in natural language.
```
You can say: “Book me a flight to New York tomorrow.”
```

#### APIs do NOT understand natural language.
They expect a structured payload, like:
```
json
{
  "destination": "New York",
  "date": "2026-04-10",
  "seat_class": "economy"
}
```
# Payload : Input schema
This is what “input schema or payload” means:

    - A strict, machine-readable structure that an API requires.
    - If you send natural language to an API, it will fail.

## 🌟 Why this matters for agents and LangGraph
When an LLM calls a tool (like a weather API, database, calculator, or search engine), it must output structured data, not a sentence.

Example: ❌ Bad (natural language)
Code
```
Can you check the weather in Austin for me?
```

✅ Good (payload) :
```
json
{
  "location": "Austin, TX",
  "units": "metric"
}
```
##### LangChain, LangGraph, and MCP all rely on this idea: The LLM must produce a payload that matches the tool’s schema.

## 🌟 Why LLMs need schemas ?
APIs are strict.
If the schema says:
```
json
{
  "city": "string",
  "date": "string"
}
```
Then this will fail:
json
```
{
  "location": "Austin"
}
```

##### this is why tools define schemas to ensure:
- predictable inputs
- correct types
- no missing fields
- no extra fields
- no ambiguity

This is why LangChain uses Pydantic models, and MCP uses JSON schemas.

## Example from LangGraph
If you define a tool like: python
```
class WeatherInput(BaseModel):
    city: str
    date: str
```
Then the LLM must output: json
```
{
  "city": "San Antonio",
  "date": "2026-04-10"
}
```
NOT: “What’s the weather in San Antonio tomorrow?”

That’s the difference between natural language and payload.

## 🌟 Why this matters for you right now
We’re learning:
- LangGraph
- Gemini
- Tools
- Agents
- MCP

All of these require the LLM to produce structured payloads when interacting with external systems. This is the core idea behind tool calling.

# Tool Binding

In langchain , Langgraph , binding a tools help model access its input-schema as "blueprint" that lets the model identify the tool(name), what it does(description), what inputs it needs and what types those inputs must be.

## 🌟 First: What is a “tool” in LLMs?
A tool is just a function you let the model call. 

Example:python
```
def get_weather(city: str, units: str):
    ...
```
When you “bind” this function as a tool, you’re telling the model:
```
“Hey, you’re allowed to call this function.
Here’s what it’s called, what it does, and what inputs it needs.”
```
## 🌟 What does “input schema” mean?
The input schema is the shape of the data the tool expects.
For example, this function: 
```
def get_weather(city: str, units: str):
```
has this schema: json
```
{
  "type": "object",
  "properties": {
    "city": {"type": "string"},
    "units": {"type": "string"}
  },
  "required": ["city", "units"]
}
```
This tells the model:

    - it must provide a city (string)
    - it must provide units (string)
    - both are required

## 🌟 Why this matters in LangGraph
In LangGraph, tools are often used inside nodes.
When you bind a tool: python
```
llm = llm.bind_tools([get_weather])
```


- You’re giving the LLM:
    - the tool name
    - the description
    - the input schema
- This lets the model:
    - decide when to call the tool
    - generate the correct arguments
    - follow the schema exactly

Without this, the model would not know how to call the tool.

## Example:
Below is an example where a model must pull a list of addresses from an input and pass it along into a tool:
```
from typing import List
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic

class Address(TypedDict):
    street: str
    city: str
    state: str

def validate_user(user_id: int, addresses: List[Address]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id: (int) the user ID.
        addresses: Previous addresses.
    """
    return True

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229"
).bind_tools([validate_user])

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)
result.tool_calls
```
#### output:
```
[{'name': 'validate_user',
  'args': {'user_id': 123,
   'addresses': [{'street': '123 Fake St', 'city': 'Boston', 'state': 'MA'},
    {'street': '234 Pretend Boulevard', 'city': 'Houston', 'state': 'TX'}]},
  'id': 'toolu_011KnPwWqKuyQ3kMy6McdcYJ',
  'type': 'tool_call'}]
  ```

# Built-in tool Node

  langGraph has a built in Tool Node that :

➤ A node that receives a tool call from the LLM
➤ Executes the corresponding Python function
➤ Returns the result back into the message stream
This node:

  - reads the last AI message
  - checks if it contains tool_calls
  - finds the matching tool
  - executes it

returns a ToolMessage
- Graph node that executes bound Python tools
- Invoked when the LLM requests a tool call
- Runs the corresponding Python function and captures output
- Returns the result back into the conversation/message stream
- Serves as the agent's "hands" to perform external actions

It’s the “hands” of your agent — the part that actually does thing
Note:  always use node name 'tools' as tool condition returns to node name 'tools'

# Tool-condition

tools_condition is a built‑in routing helper in LangGraph’s prebuilt ToolNode system.
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