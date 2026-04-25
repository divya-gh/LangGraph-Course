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
from typing import Literal

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

# Messages
```
from typing_extensions import TypedDict

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

# use langraph sdk for Deployment
from langgraph_sdk import get_client
