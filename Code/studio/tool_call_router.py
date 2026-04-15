#!/usr/bin/env python
# coding: utf-8

# # create routing for calling a condition
# 
# In our last chail_tool_tool_Calling notebook We saw that the graph can:
# 
# - Return a tool call
# - Return a natural language response
# 
# ## Lets build a router graph:
# 
# <img src="../Images/router_graph.png" width="650" height="500">
# 
# ### Goal:
# (1) Add a node that will call our tool.
# 
# (2) Add a conditional edge that will look at the chat model output, and route to our tool calling node or simply end if no tool call is performed.

# In[2]:


# Check virtual envirnment path is set

import sys
#sys.executable


# In[6]:


# load api key
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_USE_V1"] = "true"


# In[9]:


# Configure google‑genai (the new SDK)

from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

'''for model in client.models.list():
    print(model.name) '''


# In[12]:


# Build llm model
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

result = llm.invoke("Hi What can you do?")
print(result.content)


# ## Create a tool and bind to LLM 

# In[17]:


# create a tool to check if number is even
def check_even(num :int):
    "check if number is even"
    if num % 2 == 0 :
        return "Even"
    else:
        return "Odd"

e = check_even(3)
e


# In[18]:


# bind tool to llm
llm_with_tools = llm.bind_tools([check_even])


# In[23]:


# bind tool to llm
check = llm_with_tools.invoke("Check if 34556is even")
check.tool_calls


# ## Use built in MessagesState, toolNode and toolCondition
# This node:
# 
#     reads the last AI message
#     checks if it contains tool_calls
#     finds the matching tool
#     executes it
#     returns a ToolMessage
# 
# ToolNode gives you:
# 
#     automatic argument validation
#     automatic error handling
#     automatic multiple tool support
#     automatic multiple tool calls in one message
#     no need to write your own router
#     no need to write your own executor
#     It’s the recommended way to build tool‑calling graphs in LangGraph.

# In[19]:


from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


# In[20]:


# Create Node1 function

def call_llm(state : MessagesState):
    response = llm_with_tools.invoke(state['messages'])
    return {'messages' : [response]}



# ## Build graph

# In[28]:


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

builder = StateGraph(MessagesState)

# add nodes

builder.add_node('llm_node', call_llm)
builder.add_node('tools', ToolNode([check_even])) # built in object uses node name 'tools'

# add edges with router
builder.add_edge(START , 'llm_node')
builder.add_conditional_edges('llm_node',tools_condition, )
builder.add_edge('tools' , END)

# compile
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))




# In[31]:


graph.invoke({'messages':["What can you do?"]})


# In[34]:


from langchain_core.messages import HumanMessage
result = graph.invoke({'messages':[HumanMessage(role= "user", content ="the number 76534 is odd or even?", name = 'Diya')]})
for msg in result['messages']:
    msg.pretty_print()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




