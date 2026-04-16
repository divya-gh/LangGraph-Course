
# ⭐ What is LangSmith tracing?
LangSmith tracing is a visual debugger and analytics layer for AI applications.

When your agent runs — especially a LangGraph agent — a lot happens behind the scenes:

- The LLM receives messagesages
- It decides whether to call a tool
- Tools run and return resultstool
- The LLM responds again
- The graph moves from node to nodeults
- Errors may happen
- Inputs and outputs flow through the systemgain
LangSmith tracing captures all of this, step by step, and shows it to you in a clean, interactive dashboard.

## Think of it as: 🧠 “X‑ray vision for your AI agent.”
You see:
- Every message sent to the LLM
- Every tool call
- Every tool result
- Every node transition in LangGraph
- Timing, metadata, and errors
- The entire reasoning chain
It’s like watching your agent think in slow motion.

# ⭐ Why use LangSmith tracing?
Here are the biggest reasons developers rely on it:

### 1. Debugging becomes dramatically easier : Without tracing, when your agent misbehaves, you’re guessing:

- LLM misunderstood the prompt
- Tool returned the wrong format
- Graph routed incorrectly
- System message was included unexpectedly
- Tracing pinpoints the exact failure point and data

### 2. You can inspect tool calls in detail :For tool‑calling agents, this is huge.

- The exact tool name requested by the LLMsee:
- The arguments passed to the tool
- The tool’s outputsted
- Whether the LLM used the tool result correctly
This is essential when you’re building multi‑tool agents.

### 3. You can visualize LangGraph execution : LangGraph is powerful, but it can be tricky to understand how your graph flows.

- Node → Node transitions
- Conditional routing
- Parallel branches
- State updates
It’s like watching your graph come alive.

### 4. You get a full history of every run as LangSmith stores:
- Inputs
- Outputs
- Intermediate steps
- Errors
- Metadata
- Tags
- Run names
- Compare versions
- Share runs with teammates
- Reproduce bugs
- Audit behavior

5. It works automatically with LangChain and LangGraph
Once you set these in .env file
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=...
```
everything is traced automatically: example,

    - llm.invoke()
    - tools_with_llm.invoke()
    - graph.invoke()
No extra code needed.

### Basically with LangSmith tracing you can
- See what the model was thinking
- See why the tool was called
- See why the graph took that branch
- See what the system message looked like

### It helps you answer questions like:
- Was the system message included in the model input?
- Did the LLM select the correct tool?
- Did the tool output match expected results?
- Did the graph follow the intended route?
- If the tool was skipped, why did the LLM omit it?
- Why did the agent stop early?
Instead of guessing, you see everything.

---------------------------------------------------------------------------------
# 📘 LangSmith Tracing set-up Guide for LangGraph Agents

## 🚀 1. Install Required Dependencies
Run this once in your environment: bash
```
pip install -U langsmith google-genai python-dotenv
```
    - langsmith → enables tracing
    - google-genai → required for Gemini models
    - python-dotenv → loads environment variables from .env

## 📥 Follow the set up on https://smith.langchain.com/

- Create a project 'langGraph-Course' or any name
- Follow the steps for the framework used
    ex: google gemini /python
- Copy dependencies for .env file


## 🔧 2. Set Up Environment Variables
Create a .env file in your project root or use the same .env file
- Add the following in .env file if using google gemini

``` 
export LANGSMITH_TRACING=true
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
export LANGSMITH_API_KEY=your-langsmith-api-key
export LANGSMITH_PROJECT="langGraph-Course"
export GOOGLE_API_KEY=your-google-api-key
```
⚠️ Important:  
Do NOT use quotes.
Do NOT use angle brackets.

# 📥 3. Load Environment Variables in Your Notebook

At the top of your Jupyter notebook: python
```
from dotenv import load_dotenv
load_dotenv()
```

# 🔄 4. Restart Your Kernel
Jupyter notebooks do not reload environment variables automatically.
After creating .env or setting os.environ, restart:

    - Kernel → Restart
    - Re-run all cells
This ensures LangChain picks up the tracing settings.

# run all the cells in your notebook

# 🧠 5. Run Your LangGraph Agent With a Run Name
LangSmith works automatically once the environment variables are set.

But adding a run name makes your traces easier to find:python 
```
result = graph.invoke(
    {"messages": [HumanMessage(content="What can you do?")]},
    config={"run_name": "agent_test_run"}
)

```
other optional tags: python
```
config={"run_name": "agent_test_run", "tags": ["langgraph", "gemini"]}
```

# 📡 6. What Gets Traced Automatically
With tracing enabled, LangSmith logs:

- LLM calls
- Tool calls
- Node transitions
- Inputs and outputs
- Errors
- Execution time
- Metadata
You don’t need to wrap Gemini manually — LangChain handles it.

🔍 7. View Your Traces
Go to: 👉 https://smith.langchain.com

Then open:
- Your organization
- Your project (langGraph-Course)
- Traces tab
- You’ll see:
- Each graph run
- Each node execution
- Tool calls
- LLM messages
- System messages (if included in the LLM input)

# 🧪 8. Verify Tracing Works
Run a simple test: python
```
tools_with_llm.invoke("hello", config={"run_name": "hello_test"})
```
Then check LangSmith — you should see the trace instantly.

## 🎉 Done!
Your LangGraph agent is now fully integrated with LangSmith tracing.

You can now:

- Debug tool calls
- Inspect LLM reasoning
- Visualize graph execution
- Share traces with teammates

-----------------------------------------------------------------------------
# 🌐 Visual Diagram: How LangSmith Traces a LangGraph Run

┌──────────────────────────────────────────────────────────────┐
│                        Your Application                       │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                 (1) graph.invoke(input, config)
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        LangGraph Engine                       │
│  - Executes nodes                                              │
│  - Manages state                                               │
│  - Routes between nodes                                        │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (2) LLM Node Calls the Model
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      LangChain LLM Wrapper                    │
│  - Adds system messages                                        │
│  - Applies tool schemas                                        │
│  - Sends request to Gemini/OpenAI/etc.                         │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (3) LangSmith Intercepts the Call
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        LangSmith Tracing                      │
│  - Records input messages                                      │
│  - Records system prompt                                       │
│  - Records tool definitions                                    │
│  - Logs metadata (run_name, tags)                              │
│  - Captures model response                                     │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (4) LLM Returns Output to LangGraph
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     LangGraph Continues Flow                  │
│  - If tool call → routes to Tool Node                         │
│  - If final answer → returns to user                          │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (5) Tool Node Executes Tool
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        LangSmith Tracing                      │
│  - Logs tool name                                              │
│  - Logs tool arguments                                         │
│  - Logs tool output                                            │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (6) Tool Result Returned to LLM Node
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      LLM Final Response                       │
│  - Uses tool output                                            │
│  - Generates final answer                                      │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                (7) LangSmith Logs Final Output
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     LangSmith Dashboard UI                    │
│  - Full trace tree                                             │
│  - Node-by-node execution                                      │
│  - LLM messages                                                │
│  - Tool calls                                                  │
│  - Errors                                                      │
│  - Timing + metadata                                           │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                         You View the Trace

## 🧠 What This Diagram Shows You
    ✔ Every LLM call is traced
    Inputs, outputs, system messages, tool schemas.

    ✔ Every tool call is traced
    Arguments, results, errors.

    ✔ Every LangGraph node transition is visible
    You can see exactly how your graph executed.

    ✔ You get a full “flight recorder” of your agent
    Perfect for debugging, teaching, or sharing with teammates.

## 🎯 Why This Diagram Matters
LangGraph agents can be complex:
- multiple nodes
- conditional routing
- tool calls
- state updates
- visual timeline of all events
- where LangSmith hooks in
- what LangSmith records
- how the flow moves: graph → LLM → tools → back

-----------------------------------------------------------------------------

## Example: LangSmith Tracing

1. set up environment
2. open ./code/agent.ipynb
3. set .venv kernel (check virtual environment set-up guide in documents).
4. Restart kernel
5. Run agent 
    - graph.invoke({'messages':[HumanMessage(content='What can you do?')]})
    check for tracing (no tools executed).
    - - graph.invoke({'messages':[HumanMessage(content='Multiply 20 and 10, add the result to 30 and then divide it by 3. Check if the final result is odd or even')]})

6. Go to api.smith.langchain.com
7. check for tracing

