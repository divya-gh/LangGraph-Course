#!/usr/bin/env python
# coding: utf-8

# ## Build a graph wiht parallelization Fan in and Fan out 
# 
# ### Build a reassearch agent:
# - We want to gather context from two external sources (Wikipedia and Web-Search) and have an LLM answer a question.

# In[1]:


# Load API key
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_USE_V1"] = "true"


# In[2]:


# create genai client and llm
from google import genai

client = genai.Client(api_key = os.environ["GOOGLE_API_KEY"])
for model in client.models.list():
    print(model.name)


# In[3]:


# create a llm using any of the above models
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI( model= "gemini-2.5-flash" , 
                              temperature = 0.2 )
llm.invoke("What day is this?").content


# In[4]:


# Set Tavily for web search
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

from tavily import TavilyClient

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

response = client.search("What is LangGraph?")
print(response)


# ### Build a graph

# In[5]:


from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated, List, Literal
from operator import add 
from langchain_core.messages import HumanMessage, AIMessage , SystemMessage 

# import WikipediaLoader and Tavily search module
from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch

# create a class for summary_context from websearch

class State(TypedDict):
    Question: str
    Answer:str
    summery_context: Annotated[list[str],add]




def webSearch(state:State):
    ''' retrive documents from the search'''
    tavily_Search = TavilySearch(max_results =3)
    response = tavily_Search.invoke({'query': state['Question']})
    results = response.get('results', response)
    formated_result =""
    for result in results:
        formated_result = formated_result + f"<Document Title: {result['title']} \n URL: {result['url']} \n content: {result['content']}\n--\n>Document"

    return {'summery_context': [formated_result] }

# Node for WikiSearch
def search_Wiki(state:State):
    ''' retrive wiki information'''
    search_docs = WikipediaLoader(query=state['Question'], load_max_docs=3, doc_content_chars_max=1000).load()
    formatted_data =""
    for doc in search_docs:
        formatted_data = formatted_data + f'<Document Title: {doc.metadata['title']}\n URL: {doc.metadata['source']}\n content: {doc.metadata['summary']}\n--\nDocument>'

    return {'summery_context': [formatted_data] }

# Node to get question
def get_question(state:State):
    print("finding the best answer....")
    return state

def generate_answer(state:State):
    '''Node to answer the questions'''
    question = state['Question']
    context = state['summery_context']

    sys_intru = SystemMessage(content=f"You are a Guide who is an expert in Answering the question {question} using the context {context} in a beautiful format")

    answer = llm.invoke([sys_intru]+[HumanMessage(content=f"Answer the question.")]) # llm needs human message as a prompt to respond
    return {'Answer' : answer}

# Build a graph
builder = StateGraph(State)

# add nodes and adges
builder.add_node('get_question' , get_question)
builder.add_node('webSearch' , webSearch)
builder.add_node('search_Wiki' , search_Wiki)
builder.add_node('generate_answer' , generate_answer)

# Flow
builder.add_edge(START, 'get_question')
builder.add_edge('get_question', 'webSearch')
builder.add_edge('get_question', 'search_Wiki')
builder.add_edge('search_Wiki', 'generate_answer')
builder.add_edge('webSearch', 'generate_answer')
builder.add_edge('generate_answer', END)

# Compile
graph = builder.compile()





# In[41]:


# invoke with a question
Question = "Do you support ICE? "

graph.invoke({'Question': Question})

