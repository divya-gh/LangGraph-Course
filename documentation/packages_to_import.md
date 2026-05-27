# API
```
from dotenv import load_dotenv
```
# genai
```
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
```
# Create state and stateSchema
```
from typing_extensions import TypedDict
from typing import Literal , Any , List

class TypedDictState(TypedDict):
    name: str
    mood: Literal["happy","sad"]
```
# state schema with data class
```
from dataclasses import dataclass
```

## 2. Install Pydantic
In a terminal: bash
```
pip install pydantic
```

3. Your first Pydantic model
python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
BaseModel is the base class for all Pydantic models. 

# pydantic field description
```
from pydantic import BaseModel ,Field
class Analyst(BaseModel):
    name:str = Field(description="Name of the analyst.")
    role:str = Field(description="Role of the analyst in the context of the topic.",)
```

# Set pydantic Validation Error: python
```
from pydantic import BaseModel , field_validator , ValidationError

try:
    p = Person(name="Lance", age="thirty")
except ValidationError as e:
    print(e)
# You’ll see a clear error telling you age must be an integer. 
```

# Writing tools
 - use @tool beofre writing a tool function
```
from langchain_core.tools import tool
```
# creating state:
```
from typing_extensions import TypedDict
from typing import TypeDict , Optional, Literal
```

# Creating Messages 
```
from langchain_core.messages import AIMessage , HumanMessage, SystemMessage 

```
# messages as state
```
from langchain_core.messages import AnyMessage
```

# Reducers
```
from typing import Annotated
from langgraph.graph.message import add_messages
from operator import add

```
# using inbuilt MessagesState reducer
```
from langgraph.graph import MessagesState

```
# remove message reducer
```
from langchain_core.messages import RemoveMessage

```
# Trim messages reducer
```
from langchain_core.messages import trim_messages

from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately  
)

```
# Create mermaid graph
```
from IPython.display import Image, display
```

# create graph
```
from langgraph.graph import StateGraph, START, END
```
# Built-in messagesState
```
from langgraph.graph import MessagesState

```

# built in toolNode
```
from langgraph.prebuilt import ToolNode
```
# Built in tool COndition
```
from langgraph.prebuilt import tools_condition
```
# Persistance : Memory Checkpointer
```
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

```
# External-DB : SQLite
```
import sqlite3
conn = sqlite3.connect(":memory:", check_same_thread=False)

OR

db_path = "state_db/example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
```
# SqliteSaver checkpointer
```
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver(conn)
```

# if langgraph.checkpointer.sqlite isnt installed
```
#!pip install --upgrade langgraph.checkpoint.sqlite
```

# 2. AsyncSqliteSaver
The SqliteSaver does not support async methods. Consider using **AsyncSqliteSaver** instead.
```
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

#Note: AsyncSqliteSaver requires the aiosqlite package to use.

#Install with:
`pip install aiosqlite`
```
# Install LangSmith API for local development deployment
```
pip install -U langgraph-api
```
# use langraph sdk for Local Deployment in langSmithAPI
```
from langgraph_sdk import get_client
```
# Breakpoint inturrupt()
```
from langgraph.types import interrupt
```
# Run interrupt with command
```
from langgraph.types import Command
```

# Install Tavily -search
```
pip install tavily-python
```
# Set Tavily on jupyter notebook
```
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

from tavily import TavilyClient

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

response = client.search("What is LangGraph?")
print(response)

```
# install Tavily websearch engine - langchain-tavily
```
!pip install langchain-tavily

from langchain_tavily import TavilySearch

tavily_Search = TavilySearch(max_results =3)
data = tavily_Search.invoke({'query': question})
print(data)
```
# install Wikipedia
```
pip install wikipedia

```
# Wikipedia import
```
from langchain_community.document_loaders import WikipediaLoader

#load data
search_docs = WikipediaLoader(query=state['Question'], load_max_docs=3, doc_content_chars_max=1000).load()

```
# Newer Wikipedia wrapper:
```
newer, more stable loader
Replace:

python
from langchain_community.utilities import WikipediaAPIWrapper
with:
wiki = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=2000)
docs = wiki.load("what is love")

for d in docs:
    print(d[:500])

```

# map-reduce with send API
```
from langgraph.types import Send
```

# Install WebBaseLoader :
```
pip install langchain langchain-community beautifulsoup4 requests
OR
pip install -qU langchain-community beautifulsoup4
```
# . Import WebBaseLoader
```
from langchain_community.document_loaders import WebBaseLoader
oR
from langchain.document_loaders import WebBaseLoader

```
# Load WebBaseLoader:
```
Load a single web page
python
url = "https://academy.langchain.com/courses/take/intro-to-langgraph/lessons/58239974-lesson-4-research-assistant"

loader = WebBaseLoader(url)
docs = loader.load()

print(len(docs))
print(docs[0].page_content[:500])
#You should see the cleaned text from the page.
```
# Convert a list of messages Into a single formatted string
```
from langchain_core.messages import get_buffer_string
messages_to_string = get_buffer_string(messages)

```
# import markdown:
```
from IPython.display import Markdown

Markdown(variable to markdown)
```
