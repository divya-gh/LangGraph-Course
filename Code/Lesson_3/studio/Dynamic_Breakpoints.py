

# Define the state
from typing import TypedDict, Optional

class State(TypedDict):
    input:str
    approved: Optional[bool]

# Create a Node That Uses interrupt()
from langgraph.types import interrupt
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def approval_node(state:State):
    # pause exeution for approval
    aprroval = interrupt("Do you want to approive this action?")

    #when resumed, aprroval is the return value for approve field
    return {'approved': aprroval }

# continue to the next node
def action(state:State)->State:
    joke = "can eggs crack jokes? NO! they crack each other"
    return {'input': joke }


# Build the Graph
builder =StateGraph(State)

# Add nodes
builder.add_node("approval_node" , approval_node)
builder.add_node("action" , action)

# add edges
builder.add_edge(START, "approval_node")
builder.add_edge("approval_node", 'action')
builder.add_edge('action', END)

# compile with memory
graph = builder.compile()






