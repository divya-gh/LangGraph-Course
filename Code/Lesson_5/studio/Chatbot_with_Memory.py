

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


# In[4]:


# create a llm using any of the above models
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI( model= "gemini-flash-lite-latest" , 
                              temperature = 0.2 )
llm.invoke("What day is this?").content


# ### Step 1 :  Set the credentials
# 
# 

# In[7]:


# create namespace for the memory to save
import uuid
from langgraph.store.memory import InMemoryStore

Inmemory_store = InMemoryStore()


from langchain_core.messages import HumanMessage , SystemMessage
from langgraph.graph import MessagesState , StateGraph , START , END
from langchain_core.runnables.config import RunnableConfig
from langgraph.store.base import BaseStore 
import configuration
# Create a node for retrival

response_SysIstr = """ You are a helpul assistant with 'past(exisitng) memory: '{memory} who can provide helpful, factual information about the user. 
            If the memory exists , use it to personalize your response to the user. Sometimes 'memory' may not exist. """

# get structure output blue print
from pydantic import BaseModel
class LLM_Response(BaseModel):
    result: str

# create a node function for LLm reponse to user query after reviewing existing memory
def LLM_Retrive_and_respond(state:MessagesState , config: RunnableConfig, store: BaseStore):
    """Load memory from the store and use it to personalize the chatbot's response."""

    # capture user_id from the runnableConfig
    key = "user_memory"
    user_id = config['configurable']['user_id']
    namespace = ("memory" , user_id) # user and his memory

    # get existing memory
    existing_memory = store.get(namespace , key) # provide namespace  and key to get information

    # if memory exists
    if existing_memory:
        existing_memory_content = existing_memory.value.get("memory")
    else:
        existing_memory_content = "No existing memory"
    # get LLm response
    response = llm.invoke([SystemMessage(content=response_SysIstr.format(memory = existing_memory_content))] + state['messages'])
    return { 'messages' : [response] }


#----------------------------------------------------------------------------------------------------------------------------#

# create a node to write memory into the 
write_sys_instr1 = '''     You are collecting information about the user and his interests to personalize your responses.

CURRENT USER INFORMATION:
{memory}

INSTRUCTIONS:
1. Review the chat history below carefully
2. Identify new information about the user, such as:
   - Personal details (name, location)
   - Preferences (likes, dislikes)
   - Interests and hobbies
   - Past experiences
   - Goals or future plans
3. Merge any new information with existing memory
4. Format the memory as a clear, bulleted list
5. If new information conflicts with existing memory, keep the most recent version

Remember: Only include factual information directly stated by the user. Do not make assumptions or inferences.

Based on the chat history below, please update the user information:'''

write_sys_instr2 = ''' You are a memory‑review assistant. Your task is to analyze the current conversation messages or chat history and the existing memory store about the user. 
Compare both to detect new facts, preferences, interests, or updates about the user.
Here is the existing memory: {memory}

Output a bullet list summarizing ONLY new or changed information about the user. 
Each bullet should be short, factual, and written in natural language.

Follow these rules:
- Do not repeat existing memory items unless they have changed.
- if there is a confict , use updated or new information.
- Focus on new insights, preferences, goals, or behaviors revealed in the latest messages.
- Include any new interests, favorites, or contextual details that help personalize future interactions.
- Avoid speculation or assumptions; base your list strictly on observable information.
- Format output as a clean bullet list (no numbering, no extra commentary).
- merge old and new with updated information to write back to the memory store for future reference.
- do not ommit information
- chat history will be given to you.
''' 
# create blueprint for structured output
class Write_LLM(BaseModel):
    content: str

# create a node to write new momory into the store
def write_to_store(state:MessagesState , config: RunnableConfig , store: BaseStore):
    ''' reflect on the history and write the updated information about the user to the store'''

    # Get configuration for LangSmith API
    configurable = configuration.Configuration.from_runnable_config(config)

    # Get the user ID from the config
    user_id = configurable.user_id


    key = "user_memory"
    namespace = ("memory" , user_id)

    # retrive memory from the store
    existing_memory = store.get(namespace , key)

    # extract memory content
    if existing_memory:
        existing_memory_content = existing_memory.value.get("memory")
    else:
        existing_memory_content = "No memory exists"

    # extract user information
    sys_info = SystemMessage(content= write_sys_instr2.format(memory = existing_memory_content))

    response = llm.with_structured_output(Write_LLM).invoke([sys_info]+ state['messages'])

    # Update store
    store.put(namespace , key , {'memory' : response.content })
    return state


#--------------------------------------------------------------------------------------------------#

# build graph
builder = StateGraph(MessagesState)

# add nodes
builder.add_node('LLM_Retrive_and_respond' , LLM_Retrive_and_respond)
builder.add_node('write_to_store' , write_to_store)

# add edges or flow
builder.set_entry_point('LLM_Retrive_and_respond')
builder.add_edge('LLM_Retrive_and_respond' , 'write_to_store')
builder.add_edge('write_to_store',END)

# create checkpointers for both session memory and Long term store memory
from langgraph.checkpoint.memory import MemorySaver

session_memory = MemorySaver() # within thread memory
Long_memory = InMemoryStore() # across session/thread memory

# compile with noth checkpointer for thread and store for across thread
graph = builder.compile()

#view
from IPython.display import Image, display

display(Image(graph.get_graph(xray=1).draw_mermaid_png()))


# %%
