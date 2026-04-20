# 🌟 What are reducers in LangGraph?
#### A reducer is a small function that tells LangGraph how to combine new state with old state.
- Each key in the State has its own independent reducer function. 
- If no reducer function is explicitly specified then it is assumed that all updates to that key should override it. 

##### Think of it like this:
    - A reducer decides how the graph should update its memory when a node returns new data.

## 🔧 What a reducer looks like
Here’s a simple reducer for messages:

python
```
def append_messages(old, new):
    return old + new
```
#### This tells LangGraph: “When a node returns new messages, append them to the old ones.”

## 🧠 Where reducers appear in LangGraph
1. When defining state with TypedDict
You can attach reducers like this: python
```
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    mood: str
```
Here:
    - messages uses a reducer (add_messages)
    - mood uses default replace behavior

## 🧠 Why reducers matter for chat messages
Imagine your state looks like this: python
```
{"messages": [HumanMessage("Hi")]}
```
Then a node returns:python
```
{"messages": [AIMessage("Hello! How can I help?")]}
```
Without a reducer, LangGraph would overwrite the old list:Code
```
["Hello! How can I help?"]
```
You’d lose the conversation history.

With a reducer, LangGraph appends: Code
```
["Hi", "Hello! How can I help?"]
```
This is how chatbots remember context.

## Summary: 
Reducers tell LangGraph how to update the state when new data arrives.
They decide whether to append, replace, merge, or transform the state.

#  Example
```
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]
```

##### In this example, we’ve used the Annotated type to specify a reducer function (operator.add) for the second key (bar). 
Note that the first key remains unchanged. 
Let’s assume the input to the graph is {"foo": 1, "bar": ["hi"]}. 
Let’s then assume the first Node returns {"foo": 2}. 
This is treated as an update to the state. 
Notice that the Node does not need to return the whole State schema - just an update. 
After applying this update, the State would then be {"foo": 2, "bar": ["hi"]}.
If the second node returns {"bar": ["bye"]} then the State would then be {"foo": 2, "bar": ["hi", "bye"]}. 
Notice here that the bar key is updated by adding the two lists together.

## Updating Messages: add_messages

Sometimes messages in states need updating instead of preserving like AIMessages or messages from the llm. 
To achieve this, you can use the prebuilt add_messages function. For brand new messages, it will simply append to existing list, but it will also handle the updates for existing messages correctly.

#### Example:add_messages as its reducer function
```
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

## MessagesState
Since having a list of messages in your state is so common, there exists a prebuilt state called MessagesState which makes it easy to use messages. 

MessagesState is defined with a single messages key which is a list of AnyMessage objects and uses the add_messages reducer. 

Typically, there is more state to track than just messages, so we see people subclass this state and add more fields, like:
```
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]
```

## 2. When using MessagesState
LangGraph gives you built‑in reducers for chatbots: python
```
from langgraph.graph import MessagesState

class messages_state(MessagesState):
    pass
    
```
This automatically sets:
    -messages → append reducer
    -everything else → replace reducer