# LangGraph-Course
Course from LangGraph Academy designed to learn fundamentals of graph-based LLM workflows to building sophisticated, production-ready multi-agent applications.

#  📖 Course Overview : This curriculum is divided into six modules. Each module transitions from foundational concepts to advanced orchestration techniques.
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
pip install -r requirements.txt

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
#### OpenAI: Required for primary course lessons. Set up OpenAI API key 
  * Add this line in lc-academy-env → Scripts/activate file: export OPENAI_API_KEY="your-openai-key"
  * Save the file.
  * Reactivate your environment: Code source lc-academy-env/Scripts/activate
  * 🧪 Verify it worked Run: echo $OPENAI_API_KEY
  * If it prints your key, you're all set.
#### Tavily for web search:Tavily Search API is a search engine optimized for LLMs and RAG, aimed at efficient, quick, and persistent search results.
  * Add your Tavily key in lc-academy-env → Scripts/activate file: export TAVILY_API_KEY="your-tavily-key"
  * Reactivate your environment: Code source lc-academy-env/Scripts/activate
  * 🧪 Verify it worked Run: echo $TAVILY_API_KEY If it prints your key, you’re good to go.

# 🎨 Setting Up LangSmith Studio (formerly LangGraph Studio)
##### LangSmith Studio is a specialized local development environment (IDE) designed specifically for LangGraph. It allows you to visualize, test, and debug your agents in real-time through a web-based interface that connects to your local machine.

##  🚀 Why Use LangSmith Studio?
  * Visual Inspection: See your graph's nodes and edges in action.
  * Real-time Tracing: Watch how data flows between LLMs and tools.
  * Interactive Debugging: Modify the state and re-run steps without restarting your entire script.
  * Local Execution: Your agents run on your hardware, while the UI provides a professional management layer.
### 🚀 How to start LangSmith Studio locally Open your terminal?
  * Activate your virtual environment
  * Navigate into a module’s studio folder, for example: cd module-1/studio
  * Run:langgraph dev
  * This starts a local development server.
  * Think of it as a mini IDE built specifically for LangGraph workflows.
  * You run it locally, but the UI opens in your browser.
  * See traces in real time, Interact with your graph through a UI
  * Think of it as a mini IDE built specifically for LangGraph workflows.

### 🌐 What the output means When you run langgraph dev, you’ll see something like:
Code 🚀 API: http://127.0.0.1:2024 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024 📚 API Docs: http://127.0.0.1:2024/docs Here’s what each line means:
### 🚀 API: http://127.0.0.1:2024 This is the local server running your graph.
Your graph’s endpoints live here.
### 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024 This is the web interface where you interact with your graph.
Even though the UI is hosted on LangSmith’s website, it connects to your local graph through the baseUrl parameter.
This is why your API keys matter — they authenticate you to the Studio UI.
### 📚 API Docs: http://127.0.0.1:2024/docs This opens Swagger-style documentation for your graph’s API. 

## 🧠 Why this matters for the course LangGraph Academy uses Studio heavily:
  * You build a graph
  * You run it locally
  * You open Studio UI
  * You test your agent visually
  * You debug step-by-step
  * It’s one of the best ways to understand how LangGraph works. You can test endpoints directly from here.

# 📁 Repository Structure
##### The Studio configuration is modular. You must run the studio commands from within the specific module directory you are studying:

langchain-academy/
├── module-1/
│   └── studio/      <-- Run 'langgraph dev' here
├── module-2/
│   └── studio/
└── ...

# 🛠️ Installation & Setup
1. Create .env Files
Each module requires its own environment variables to authenticate with OpenAI and other services. Run this bash script from the root of the repository to automate the setup for Modules 1–5:

Bash
for i in 1 2 3 4 5; do
  cp module-$i/studio/.env.example module-$i/studio/.env
  echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> module-$i/studio/.env
done

# Special addition for Module 4 (Tavily Search)
echo "TAVILY_API_KEY=$TAVILY_API_KEY" >> module-4/studio/.env
2. Launch the Studio
To start the local development server:

Open your terminal and activate your virtual environment.

Navigate to the desired module's studio folder: cd module-1/studio

Run the development command:

Bash
langgraph dev

#🧠 Workflow Summary
* Build/Modify your graph in the provided Jupyter Notebooks.
* Launch the Studio via langgraph dev in the terminal.
* Open the Studio UI link in your browser.
* Interact with your agent visually to verify its logic and tool-calling capabilities.

Citation: LangGraph Academy course, which teaches developers how to build stateful, multi-agent AI applications using graph-based workflows. 
