## Node Classes in LangGraph

### What is a node class?
A Python class that implements `__call__`, so it behaves like a function.

### Why use it?
- To store configuration in `__init__`
- To create multiple nodes with different behavior
- To keep code clean when many nodes share logic
- To support parallelization patterns

### When to use a simple function?
- When the node has no internal state
- When the behavior is always the same
- When you only need one instance

### Key idea
Functions are stateless.
Node classes are stateful.

## 🌟 What is a “node class”?
A node class is simply a Python class that behaves like a function because it implements __call__.

### Example: python
```
class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state):
        return {"state": [self._value]}
```
This object can be passed to graph.add_node() exactly like a function.

## 🧠 Why do node classes exist?
Because sometimes a node needs to remember something.

A plain function:
- has no memory
- has no configuration
- behaves the same every time

A node class:
- stores configuration in __init__
- uses that configuration in __call__
- lets you create many different nodes from one class

This is the key idea:
- Functions are stateless. 
- Node classes are stateful.

## 🟦 When should you use a node class?
Use a node class when:

✔ You want multiple nodes with different behavior

Example: 10 nodes that each return a different value.
python
```
graph.add_node("A", ReturnNodeValue("A"))
graph.add_node("B", ReturnNodeValue("B"))
graph.add_node("C", ReturnNodeValue("C"))
```
One class → many nodes.

✔ You want to store configuration

Examples:
- API keys
- model names
- thresholds
- prompt templates
- node‑specific parameters

✔ You want cleaner code for parallelization
Instead of writing 10 nearly identical functions, you write one class.

## 🟩 When should you NOT use a node class?
Use a simple function when:
- The node always does the same thing
- You don’t need configuration
- You only need one instance

Example: python
```
def summarize(state):
    return {"summary": "short summary"}
```
This is perfect as a function.

## 🟧 How __init__ and __call__ work together

**__init__**
Runs once when the node is created.
Stores configuration.

**__call__**
Runs every time the node executes in the graph.
Uses the stored configuration.

Example:python
```
node = ReturnNodeValue("hello")

node(state)  
# calls __call__
```

## 🟪 Why LangGraph supports callable classes
Because LangGraph treats nodes as:
- functions
- or any object that behaves like a function

This gives you flexibility:
- simple nodes → use functions
- configurable nodes → use classes


