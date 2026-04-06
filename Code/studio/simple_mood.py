#!/usr/bin/env python
# coding: utf-8

# # The Simple Mood Graph
# 
# Let's build a simple graph with 3 nodes and one conditional edge. 
# 
# 
# <img src="../Images/Node_pic.png" width="400">
# 

# ## Define State and state schema

# In[44]:


from typing_extensions import TypedDict, Literal

class state(TypedDict):
    mood: str


# ## Define Nodes using state schema

# In[45]:


import random
def ask_mood_node_1(state)-> state:
    moods = ["happy", "sad", "excited"]
    return {"mood" : random.choice(moods)}
def happy_mood_node_2(state) ->state :
    print("Let's Party!")
    return state
def sad_mood_node_3(state) ->state:
    print("Need Comfort")
    return state

def mood_condition(state)-> Literal[ 'happy_node' , 'sad_node'] :
    if (state["mood"] == 'happy' or state["mood"] == 'excited') :
        return 'happy_node'
    return 'sad_node'





# ## Build the graph: You add nodes and connect them with edges

# In[46]:


from langgraph.graph import StateGraph

graph = StateGraph(state)
graph.add_node("ask_mood", ask_mood_node_1)
graph.add_node("happy_node_2", happy_mood_node_2)
graph.add_node("sad_node_3", sad_mood_node_3)



# ## Connect Edges

# In[47]:


graph.set_entry_point("ask_mood")

# add condition

graph.add_conditional_edges("ask_mood",mood_condition, {'happy_node' : 'happy_node_2',
                                                        'sad_node' : 'sad_node_3'
                                                       })


# ## Compile the graph, Turns your graph into a runnable agent.

# In[48]:


app = graph.compile()


# ## Run it : app.invoke({}) starts the workflow with an empty state.

# In[52]:


app.invoke({})


# In[ ]:





# In[ ]:




