# LangGraph-Course
Course from LangGraph Academy designed to learn fundamentals of graph-based LLM workflows to building sophisticated, production-ready multi-agent applications.

###  📖 Course Overview : This curriculum is divided into six modules. Each module transitions from foundational concepts to advanced orchestration techniques.
* Video Lessons: Conceptual deep dives.
* Jupyter Notebooks: Hands-on coding exercises.
* Studio Subdirectories: Pre-configured graphs to explore via the LangGraph Studio IDE.

# 🧩 What is LangGraph?
##### LangGraph is an open-source Python framework designed to orchestrate stateful, multi-agent LLM applications using graph-based workflows.

### Key Differences: LangChain vs. LangGraph
Feature                                               LangChain                                     LangGraph
FlowType                                            Linear chains / DAGs                           Cyclical / Looping workflows
State                                              Short-term memory                               Persistent, centralized state
Control                                            High-level abstraction                          Granular node-level control
Use Case                                           Simple RAG / Sequences                          Complex Agents / Workflows

## Core Concepts
### Nodes: Python functions representing units of work (e.g., calling an LLM or an API).
### Edges: The paths between nodes.
  * Simple Edges: Direct transitions.
  * Conditional Edges: Logic-based branching (if/else).
### State Management: A central object that tracks the application's current status across all agents.
### Cycles: Allows agents to loop back, self-correct, and iterate on tasks.

# 🛠️ Environment Setup
1. PrerequisitesPython Version: $3.11 \le x < 3.14$ (Recommended: 3.12)
2. Tools: Git, Terminal (Bash/PowerShell), and a LangSmith Account.
#### Bash
git clone https://github.com/langchain-ai/langchain-academy.git
cd langchain-academy

3. Virtual Environment (Windows Focus)
Create and activate your environment:
Bash
# Create the environment
python -m venv lc-academy-env

# Activate (Windows Git Bash)
source lc-academy-env/Scripts/activate

# Install dependencies
pip install langchain-core
pip install langchain

# Jupyter Notebook: 
Bash:
jupiter Notebook (ctr C to exit)

# 🔑 API Configuration
You must set your API keys as environment variables. For a permanent setup, add these to your lc-academy-env/Scripts/activate file manualy.

## LangSmith (Observability & Tracing)
Required for debugging and visualizing your agent's thought process.
#### Sign up for LangSmith: Create a LangSmith account and API key. You can reference LangSmith docs here.

##✏️ How to edit it (step‑by‑step) Open File Explorer: 
  * Go to your project folder
    * Open: Code lc-academy-env → Scripts Right‑click the file named activate (no extension)
    * Choose Open with → Notepad
    * Scroll to the bottom and add these lines:
  
      "export LANGSMITH_API_KEY="your-key"
      export LANGSMITH_TRACING_V2=true
      export LANGSMITH_PROJECT="langchain-academy"
      # Add ONLY if using the EU instance:
      # export LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com"
    * Reactivate your environment: Code source lc-academy-env/Scripts/activate
    * 🧪 Verify it worked Run: Code echo $LANGSMITH_API_KEY If it prints your key, everything is set correctly.
Note:  nce you selected US, you do not need the EU endpoint line.

# LLM & Tools
This langgraph course uses Gemini model instead of open AI as openAi isn't free

#### Set up : GenAI: Required for primary course lessons. Set up GenAI API key 
1.  Got o aistudio.google.com to create an API key
2. Activate virtual environment 
3. Install Gemini SDK : Install Google’s newer, lighter-weight SDK designed to avoid protobuf conflicts -google genai
bash
  ```
  source venv/Scripts/activate

  pip install google-genai
  pip install langchain-google-genai

```

  * Add the google API ke in .env → OPENAI_API_KEY="your-openai-key"
  * Save and add it to gitignore to protect the API key.
  * Reactivate your environment: Code source venv/Scripts/activate
  * 🧪 Verify it worked Run: echo $OPENAI_API_KEY
  * If it prints your key, you're all set.
4. activate api key for genai
  * If you’re using a .env file, load it in your notebook:
  python
  ```
    from dotenv import load_dotenv
    load_dotenv()

```
5.connect to genai:
notebook:
```
import google.generativeai as genai
import os
os.environ["GOOGLE_API_USE_V1"] = "true"     #LangChain defaults to the old API.


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
print([m.name for m in genai.list_models()])
```
prints available models. use one.

5.  LangChain’s Gemini wrapper supports:

- gemma-3-4b-it
- gemini-2.5-flash-lite
- veo-3.1-lite-generate-preview
- gemini-2.5-flash
- gemini-2.5-pro
- gemini-3.1-flash-live-preview and more!

(Use any of the above)
6. example code:
notebook:
    ```
    from dotenv import load_dotenv
    load_dotenv()
    os.environ["GOOGLE_API_USE_V1"] = "true"

    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    messages = [
        ("human", "Hello Gemini, how are you?")
    ]

    result = llm.invoke(messages)
    print(result.content)

    ```

#### Tavily for web search:Tavily Search API is a search engine optimized for LLMs and RAG, aimed at efficient, quick, and persistent search results.
  * Add your Tavily key in lc-academy-env → Scripts/activate file: export TAVILY_API_KEY="your-tavily-key"
  * Reactivate your environment: Code source lc-academy-env/Scripts/activate
  * 🧪 Verify it worked Run: echo $TAVILY_API_KEY If it prints your key, you’re good to go.



Citation: LangGraph Course is derived from LangGraph academy course and built with genAI and Jetson AI 
          - Learn how to build stateful, multi-agent AI applications using graph-based workflows. 
