#!/usr/bin/env python
# coding: utf-8

# 
# # Simple Mood Graph with mermaid diagram
# 
# <img src="../Images/mood_mermaid.png" width="500">

# In[51]:


import sys
#sys.executable


# In[52]:


from typing_extensions import TypedDict, Literal



# ## Define state schema or memory box

# In[53]:


class state(TypedDict):
    mood: str


# ## Create Nodes and Node functions
# 
# #### Each node function receives the current state and returns a new value, which overrides the graph state.
# 

# In[54]:


def ask_mood(state):
    print("Node1: ")
    original_mood = state["mood"]
    return {"mood": original_mood +".  " + "I am"}

# Node 2 Name : "Happy_Node" 

def happy_node(state):
    print("node 2: ")
    New_mood = state["mood"] + " " + "Happy"
    print(f"{New_mood} , Let's Party!")
    return {"mood" : New_mood }

# Node 3 Name : "Sad_Node" 

def sad_node(state):
    print("Node3: ")
    New_mood = state["mood"] + " " + "Sad"
    print(f"{New_mood} , I Need Comfort!")
    return {"mood" : New_mood }



# ## Set Edges :
# #### Normal Edges are used if you want to always go from, for example, node_1 to node_2.
# 
# #### Conditional Edges are used if you want to optionally route between nodes.
# 
# ##### Conditional edges are implemented as functions that return the next node to visit based on some logic.

# In[55]:


import random

def decide_mood(state) -> Literal["Happy_Node" , "Sad_Node"]:
    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:

        # 50% of the time, we return Node 2
        return "Happy_Node"
    else :
        # 50% of the time, we return Node 3
        return "Sad_Node"



# ## Graph Construction
# 
# #### Initialize a StateGraph with the State class 
# #### use the START Node, a special node that sends user input to the graph, to indicate where to start our graph.
# #### The END Node is a special node that represents a terminal node.
# #### Finally, we compile our graph to perform a few basic checks on the graph structure.
# 

# In[56]:


from langgraph.graph import START , END, StateGraph

builder = StateGraph(state)
# Build graph

builder.add_node("Ask_node" , ask_mood)        # node1_name = Ask_node  node1_function = ask_mood
builder.add_node("Happy_Node" , happy_node)    # node2_name = Happy_Node  node2_function = happy_node
builder.add_node("Sad_Node" , sad_node)    # node3_name = Sad_Node  node3_function = sad_node

# Build Logic

builder.add_edge(START , "Ask_node" )
builder.add_conditional_edges("Ask_node" , decide_mood )
builder.add_edge("Happy_Node" , END)
builder.add_edge("Sad_Node" , END)


#Compile
graph = builder.compile()


# ## Invoke graph
# 
# `invoke` runs the entire graph synchronously.
# 
# This waits for each step to complete before moving to the next.
# 
# It returns the final state of the graph after all nodes have executed.

# In[57]:


graph.invoke({"mood" : "Hi, I'm Diya"})


# In[58]:


from IPython.display import Image, display
# View
display(Image(graph.get_graph().draw_mermaid_png()))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




