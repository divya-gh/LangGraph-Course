# 🌟 What are chat models in LangGraph?
### A chat model is just an AI model that talks in a conversation format.

    - A chat model is the AI brain you call inside a LangGraph node.
    - It takes chat messages and returns a chat response.
    - LangGraph just uses it as part of your graph’s logic.

## Think of it like this:

    - A normal LLM takes one big text input and gives one big text output.
    - A chat model takes a list of messages (system, user, assistant) and responds like a chatbot.

### LangGraph doesn’t create chat models —
    It uses chat models from LangChain (OpenAI, Gemini, Groq, etc.) inside your graph nodes.

So in LangGraph: A chat model is simply the LLM you call inside a node.

## 💬 What makes a model a “chat model”?
It understands chat messages like:

    - system → rules
    - user → what the human says
    - assistant → what the AI said before

Example:
```
python
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "Tell me a joke."}
]
```
A chat model reads these and replies with:

python
```
{"role": "assistant", "content": "Why did the robot cross the road..."}
```

## 🧠 Why does LangGraph care about chat models?
Because LangGraph nodes often need to:

- call an LLM
- generate text
- answer questions
- decide routing
- summarize
- classify
- chat with the user
A chat model is the easiest way to do that.

## 🔧 How chat models fit inside a LangGraph node
Here’s the mental picture:
```
[State] → [Node] → calls chat model → returns new state
```
Example node: python
```
def chat_node(state):
    messages = [
        {"role": "system", "content": "You are a mood assistant."},
        {"role": "user", "content": state["mood"]}
    ]
    response = llm.invoke(messages)
    return {"mood": response.content}
```
The chat model is just a tool the node uses.

## 🧩 Chat models vs LangGraph messages
Clean distinction: Concept	Meaning :

Chat messages	- What you send to the LLM (system/user/assistant)
LangGraph messages	- The state updates passed between nodes

* They are different things.*

You can use chat messages inside LangGraph messages.

## 🧪 Examples of chat models you can use in LangGraph
#### OpenAI
python
```
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
```

#### Gemini
python
```
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")
result = llm.invoke(messages)
print(result.content)

```
#### Groq
python
```
from langchain_groq import ChatGroq
llm = ChatGroq(model="mixtral-8x7b")
```

### Local models (Ollama)
python
```
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3")
```





