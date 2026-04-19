# What is TypeDict
TypedDict is a Python feature that lets you create dictionary‑like objects with fixed keys and expected types.

Its a dictionary that comes with rules about what keys it must have and what type each value should be. It’s part of Python’s typing module.

## 🎯 In one sentence
TypedDict lets you define a dictionary with fixed keys and types, making it perfect for describing your LangGraph agent’s state.

## 🧩 A normal dictionary vs. TypedDict
#### ❌ Normal dictionary

Python doesn’t enforce structure: python
```
state = {
    "messages": ["hello"],
    "foo": 123,
    "bar": True
}
```
You can add anything, and Python won’t complain.

#### ✔ TypedDict
You define the structure up front: python
```
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: List[BaseMessage]
    result : int
    tools_used : list[str]
    
```
This means:

    - The state must have a key called messages
    - messages must be a list of BaseMessage objects
    - result key is a number
    - tools_used must contain list of strings
If a node tries to return something else, LangGraph can warn you.

##  Think of TypedDict like a backpack with labeled pockets
Imagine your agent carries a backpack (the state) through the graph.

A TypedDict is like saying:

    - Pocket 1: messages → must contain a list of messages
    - Pocket 2: result → must contain a number
    - Pocket 3: tools_used → must contain a list of strings

Every node knows exactly where to put things.

### Why TypedDict is perfect for beginners
    It’s simple
    It looks like a normal dictionary
    It’s easy to read
    It’s easy to extend
    LangGraph understands it well
That’s why the notebook you’re reading starts with TypedDict as the first schema option

-------------------------------------------------------

# 🌟 What Is a Literal Type?
A Literal type in Python is a way to say:

“This value must be exactly one of these specific options.”

It’s like giving Python a fixed list of allowed values.

You import it like this: python
```
from typing import Literal
```

## ⭐ Why Do We Use Literal in LangGraph?
LangGraph uses Literal types to:

✔ restrict certain fields to specific values
For example, message roles: python
```
role: Literal["user", "assistant"]
```
✔ prevent mistakes
If you accidentally type "User" instead of "user", Python can catch it.

✔ make your state schema safer
Nodes know exactly what values to expect.

## 🎯 In One Sentence
A Literal type lets you restrict a value to a small set of allowed options, making your code safer and easier to understand.