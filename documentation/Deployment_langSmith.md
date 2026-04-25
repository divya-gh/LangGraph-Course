# What is agent Deployment?
Agent deployment means turning your LangGraph agent into a running service that apps can call.
You do it by:
- Building your graph
- Adding persistence (optional)
- Wrapping it in a server
- Running it locally
- Deploying it to the cloud

Once deployed, your agent can:

    - handle multiple users
    - remember conversations
    - run continuously
    - integrate with apps

# 🌟 Two Types of Deployment in LangGraph
There are two ways to “deploy” a LangGraph agent:

### 1. Local Development Deployment (what we're doing now)
This uses: Bash
```
langgraph dev
```
This launches:

    🚀 A local API server
    🎨 A Studio UI connected to your local agent
    📚 Local API docs

This is a deployment for development, meaning:

    - Test your agent
    - Stream runs
    - Inspect state
    - Use threads
    - Debug tools
    - You can connect from Python using the SDK
    - Runs only on your machine.
This is perfect for learning, debugging, and building.

## 2. Production Deployment (cloud)
This is when you:

    - host your agent on a server
    - expose it to real users
    - give it persistent memory
    - integrate it into apps
    - run it 24/7

    This can be done using:

    - LangGraph Cloud (coming soon)
    - LangSmith Studio hosted agents
    - Your own server (Docker, Render, AWS, etc.)

## ⭐ Deployment with LangSmith Studio - Local Development Deployment: 
LangSmith Studio gives you a hosted environment where you can:

    - Upload your LangGraph agent
    - Run it as a hosted API
    - Get a public endpoint
    - Manage threads, state, and memory
    - View traces and tool calls
    - Test your agent in the built-in chat UI

In simple terms:

LangSmith Studio turns your local LangGraph agent into a cloud‑hosted service you can call from anywhere.
You don’t need to set up servers, Docker, or cloud infrastructure.
Studio handles all of that.

## 🌱 Why Deploy to LangSmith Studio?
For a beginner, Studio is the easiest way to:
- Run your agent 24/7
- Give it persistent memory
- Test with real users
- Integrate into apps
- Debug with full tracing
- Avoid managing servers
- Fastest path from notebook prototype to real agent

# LangSmith Studio local development workflow
Here’s the whole workflow in plain English:

bash 
```
langgraph dev  
```
This starts your agent locally.

Open Studio UI  
You get a visual interface connected to your local agent.

Use the SDK to connect  
```
client = get_client(url)
```

Create a thread  
This is your conversation session.

Send a message  
```
Using client.runs.stream(...)
```

Watch the agent respond step‑by‑step  
You print each chunk of state.

See everything in Studio  
Messages, memory, tools, state, traces.

This is the easiest way to learn LangGraph and debug your agent.

### 🌱 Why do we use langgraph dev?
Because it lets you:

    - Test your agent locally
    - Use LangSmith Studio as a frontend
    - See memory and state updates
    - Debug your graph step‑by‑step
    - Stream results
    - Avoid deploying to the cloud yet
    - Perfect beginner workflow

## Set up:

To start the local development server, run the following command in your terminal in the /studio directory in this module: BAsh

langgraph dev
You should see the following output:

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
Open your browser and navigate to the Studio UI URL shown above.

### Connecting to the Local Server Using the SDK
You use the LangGraph SDK to talk to your local agent: python
```
from langgraph_sdk import get_client

url = "http://127.0.0.1:2024"
client = get_client(url=url)
```
This client object lets you:

    - list assistants
    - create threads
    - run your agent
    - stream results

### 🤖 What is an “assistant”?
In LangGraph Studio, an assistant = your agent. 
You can list them: python
```
assistants = await client.assistants.search()
assistants
```
You can lsit allt he hosted graphs in the studio

### 🧵 What is a “thread”?
A thread is a conversation session.

It stores:

    - messages
    - memory
    - state
    - checkpoints

You create one like this: python
```
thread = await client.threads.create()
```
This returns: python
```
{"thread_id": "abc123"}
```
You will use this thread ID for the entire conversation.

### Preparing the Input Message
You send messages to your agent like this: python
```
from langchain_core.messages import HumanMessage

msg_input = {
    "messages": [
        HumanMessage(
            role="user",
            content="Add 30 to 20",
            name="Diya"
        )
    ]
}
```
This is just a structured way of saying: “User Diya says: Add 30 to 20”

### Running the Agent With Streaming
You run your agent like this: python
```
async for chunk in client.runs.stream(
        thread['thread_id'],   # which conversation
        "agent",               # which assistant
        input=msg_input,       # what the user said
        stream_mode="values",  # stream full state after each step
    ):
```
What happens?
Your agent runs step by step:

LLM node

Tool node

LLM node

Final answer
After each step, LangGraph sends you a chunk containing the updated state.

