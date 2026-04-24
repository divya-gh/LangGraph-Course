#!/usr/bin/env python
# coding: utf-8

# # Goal : Build a Long-term memory chatbot
# 
# ## General Agent Architechture
# act - let the model call specific tools
# observe - pass the tool output back to the model
# reason - let the model reason about the tool output to decide what to do next (e.g., call another tool or just respond directly)
# 
# ## Objective: 
#     - remove messages to save token usage, latency and cost
#     - filter messages 


# Load API key
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_USE_V1"] = "true"



# create genai client and llm
from google import genai

client = genai.Client(api_key = os.environ["GOOGLE_API_KEY"])
for model in client.models.list():
    print(model.name)


# In[53]:


# create a llm
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI( model= "gemini-flash-latest" , 
                              temperature = 0.2 )
llm.invoke("What day is this?")


# # Messages as state
# 

# In[12]:
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import MessagesState , START , StateGraph , END


# Create some dummy messages for the state

messages = [AIMessage(content="Hi, I'm a bot" , name ="AI" , id ="1"), 
            HumanMessage(content= "What can you do?" , name="Diya" , id= "2"),
            AIMessage(content="What do you line to learn about?" , name ="AI" , id = "3"),
            HumanMessage(content= "Teach me Langgraph" , name="Diya" , id ="4")
           ]         




# In[116]:


# Build a new graph filtering messages in the nodes





from langchain_core.messages import trim_messages

# create a graph with nodes using tocken limit

def model_with_trimmer(state:MessagesState):
    messages = trim_messages(
               state['messages'],
               max_tokens = 300,
               strategy = 'last',
               token_counter = ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
               allow_partial=False,
               )
    print("Trimmed Messages: " , messages)
    return {'messages': llm.invoke(messages)}

# build graph
builder = StateGraph(MessagesState)

builder.add_node('chat_model', model_with_trimmer)

builder.add_edge(START, 'chat_model')
builder.add_edge('chat_model', END)

graph = builder.compile()
# View


# In[162]:



messages.append(HumanMessage(content="List few strtup comapnies I can apply to after learnign langgraph." , name='Diya' , id = '7'))


# Invoke
result = graph.invoke({'messages': messages})



