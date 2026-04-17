#!/usr/bin/env python
# coding: utf-8

# # Create a Re-Act Agent graph using llms , tools 
# 
# ## Goal:
#     - Chat model decides to call the tool
#     - agent output is chat model response
#     - pass that ToolMessage back to the model
#     - 
# <img src="../Images/agent_nodes.png" width="500" height="500">
# 
# ## General Agent Architechture
# 
#     act - let the model call specific tools
#     observe - pass the tool output back to the model
#     reason - let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly)

# In[1]:


# load api key
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_USE_V1"] = "true"


# In[2]:


from google import genai

#client = genai.client(api_key = os.environ["GOOGLE_API_KEY"])
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

for model in client.models.list():
    print(model.name)


# In[3]:


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-lite-latest",
    temperature=0.2
)

result = llm.invoke("Hi, What day is this?")
print(result.content)


# ## Create multiple arithmatic tools along with classifier tool
# 
# #### Addition
# #### Substraction
# #### Division
# #### Check if the result is even or odd
# 
# 

# In[4]:


#1.  Addition tool
def addition(a:float , b:float)->float :
    "add two numbers a and b "
    return a+b

#2. multiplication
def multiply(a:float , b:float)-> float:
    "multiply two numbers a and b "
    return a * b

# 3. division
def division(a:float , b:float)-> float:
    "divide number a by b"
    return a/b
# 4. check if number is even or odd
def check_evenOdd(num:float)->float:
    "Check if the number is even or odd"
    if num % 2 == 0 :
        return "even"
    return "Odd"
tools = [addition , multiply , division , check_evenOdd]


# ## Bind tool to the llm
# ### set parallel_tool_calls=False

# In[5]:


tools_with_llm = llm.bind_tools(tools)


# In[6]:


# check if tools work with llm
# Test

result = tools_with_llm.invoke("what tools are at your disposal?")
result.content[0]['text']


# ## Create a MessagesState and Graph

# In[7]:


from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage , SystemMessage 

# set system message

sys_message = SystemMessage(content= " You are a helpful assistant who can perform arithmatic operations on set of inputs given. Follow the instructions given and if information is not clear, ask for more details. Use tools in any order as suited")

# set llm assistant

def llm_assistant(state:MessagesState) :
    response = tools_with_llm.invoke([sys_message] + state['messages'])
    print(f"(LLM_Response : {response}")
    return {'messages' : [response]}


# ## Use built in ToolNode and tools_condition
# ## create a graph
# 
# 

# In[8]:


from langgraph.graph import START , END , StateGraph
from langgraph.prebuilt import ToolNode , tools_condition
from IPython.display import Image, display

# Build graph
builder = StateGraph(MessagesState)

# add nodes
builder.add_node('llm_assistant' , llm_assistant)
builder.add_node('tools' , ToolNode(tools))


# Define edges: determine how the control flow moves

builder.add_edge(START , 'llm_assistant')
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
builder.add_conditional_edges("llm_assistant" , tools_condition , {'tools': 'tools' , END :END })
builder. add_edge('tools', 'llm_assistant')

graph = builder.compile()
graph


# ## invoke graph

# In[9]:


result = graph.invoke({'messages' : [HumanMessage( Role ='User' , content="What can you do?" , name = 'Diya')]})


# In[10]:


result = graph.invoke({'messages' : [HumanMessage( Role ='User' , content="Add the numbers 25 and 50 ,  divide the result by 10 and then multiply the output by 20 and check if the result is even" , name = 'Diya')]}, config={"run_name": "agent_test"})
result


# In[11]:


result


# In[12]:


for m in result['messages']:
    m.pretty_print()


# # set Langchain tracing

# In[13]:


os.environ['LANGCHAIN_PROJECT'] = 'langGraph-Course'


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




