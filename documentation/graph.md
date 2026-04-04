
🌱 What is a graph ?

When you build an agent in LangGraph, you’re really building a graph:

    - You define the state schema eg: using stateGraph (what the agent remembers)
    - You define nodes (what the agent does)
    - You define edges (how the agent moves between steps)
Studio then visualizes this graph so you can see your agent’s reasoning.

#### Graph : A graph is just a way of organizing steps so you can control what happens next.
    - Think of it like:
    - a map of your agent
    - made of nodes (steps)
    - connected by edges (arrows showing what comes next)
It’s not a picture you draw — it’s a structure your program uses to decide how to move from one step to another.

#### 🧩 Graph = Nodes + Edges
Nodes: Perform

    - call an LLM
    - call a tool
    - check the state
    - decide something
    - return an answer

Edges: Connections between steps.

They tell the agent:

    “After this step, go to that step.”
    “If condition A, go to node_2; if B, go to node_3.”

### 🎒 Why LangGraph uses a graph
LangGraph builds multi‑step agents, and those agents need:

    - loops
    - branching
    - retries
    - conditional logic
    - human‑in‑the‑loop
    - state updates
A graph makes all of this possible.

Every node receives the state (your agent’s “backpack”) and returns an updated state.
The edges decide which node runs next.

🎨 A simple analogy
Imagine a flowchart:
```
Code
Start → Think → Search → Think → Answer
That flowchart is the graph.
```

LangGraph just turns that flowchart into code.

## 🌱 What is a StateGraph?
A StateGraph is the core structure you build when creating an agent in LangGraph. It’s basically a flowchart made of Python functions, where each function updates and passes along a shared state.


Which is a :

    a map of your agent    
    made of nodes (steps your agent performs)    
    connected by edges (rules about what happens next)    
    all operating on a shared state (your agent’s memory)

## 🎒 What the StateGraph controls
A StateGraph lets you define:

1. The State Schema
What your agent remembers (messages, tool results, decisions, etc.)

2. Nodes
What your agent does at each step
(e.g., call an LLM, call a tool, decide something)

3. Edges
How your agent moves from one step to the next
(e.g., always go to node_2, or choose between node_2 and node_3)

## 🎨 A simple analogy
graph as a flowchart:

Code
```
Start → Think → Search → Think → Answer
```
A StateGraph is that flowchart turned into code, with the state passed through each step.
Studio then visualizes this so you can see your agent’s reasoning .

## 🧠 Why LangGraph uses a StateGraph
Because agents need:

    - loops
    - branching
    - retries
    - conditional logic
    - human‑in‑the‑loop
    - state updates

A StateGraph makes all of this possible in a clean, predictable way.

## 🌱 Simple StateGraph Example
This example has: 
    a State schema, two nodes, one conditional edge, a graph that runs from start → next step → end
```
    from typing import TypedDict, Literal
    from langgraph.graph import StateGraph

    # 1. Define the State schema

    class State(TypedDict):
        mood: str  
        #This defines what the agent remembers. Here, it only remembers one thing: "mood".

    # 2. Define node functions
    # Each node is just a Python function that:     
            - receives the state
            - returns an updated state

    def ask_mood(state: State) -> State:
        # Pretend we got this from the user or an LLM
        return {"mood": "happy"}

    def respond_happy(state: State) -> State:
        print("You seem happy today!")
        return state

    def respond_sad(state: State) -> State:
        print("I'm here for you.")
        return state

    # 3. Define a router (decides which node to go to), The Literal[...] tells LangGraph the only valid next steps.

    def decide_mood(state: State) -> Literal["happy_node", "sad_node"]:
        if state["mood"] == "happy":
            return "happy_node"
        else:
            return "sad_node"

    # 4. Build the graph: You add nodes and connect them with edges

    graph = StateGraph(State)

    graph.add_node("ask_mood", ask_mood)
    graph.add_node("happy_node", respond_happy)
    graph.add_node("sad_node", respond_sad)

    graph.set_entry_point("ask_mood")

    # Add conditional edges with router output. ie, router_output → next_node_name
    graph.add_conditional_edges(
        "ask_mood",
        decide_mood,
        {
            "happy_node": "happy_node",   
            "sad_node": "sad_node"
        }
    )

    # 5. Compile the graph, Turns your graph into a runnable agent.

    app = graph.compile()

    # 6. Run it : app.invoke({}) starts the workflow with an empty state.
    app.invoke({})

```

# Display Graph

code 
```
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```
It renders a picture of your LangGraph so you can see the nodes and edges.
Think of it as:

“Show me a diagram of my agent.”

1. app.get_graph()
This gets the internal graph structure from your compiled LangGraph app.

2. .draw_mermaid_png()
This converts the graph into a Mermaid diagram and then into a PNG image.

Mermaid is a simple language for drawing flowcharts.
LangGraph uses it to visualize:

    - nodes
    - edges
    - conditional branches
    - loops

3. Image(...)
This wraps the PNG bytes into an image object that Jupyter/Colab can display.

4. display(...)
This tells the notebook:

“Render this image in the output cell.”

ask_mood → decide_mood → happy_node
                        → sad_node

## 🧠 Why LangGraph includes this
Because agents can get complex fast.
Visualizing the graph helps you:

- debug

    - understand flow
    - see branching
    - catch mistakes
    - explain your agent to others

It’s one of the best features of LangGraph Studio and the Python API.
