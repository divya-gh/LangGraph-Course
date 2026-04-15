# API
```
from dotenv import load_dotenv
```
# genai
```
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
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

```
# using inbuilt messagesState
```
from langgraph.graph import MessagesState

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
