# MAP-Reduce and Send API with LLM

### What is Map‑Reduce with LLMs?
You use an LLM to:

    MAP → break a big input into smaller chunks
    PROCESS → run the LLM on each chunk in parallel
    REDUCE → merge all LLM outputs into a final answer

This is perfect for:
- Generate specic doc for  a list of subjects
- Summarizing long documents
- Extracting facts from many paragraphs
- Running multiple LLM calls at once
- Multi‑agent fan‑out tasks
- And LangGraph’s Send API makes this easy.

## Problem

Map-reduce operations are essential for efficient task decomposition and parallel processing. 

It has two phases:

(1) `Map` - Break a task into smaller sub-tasks, processing each sub-task in parallel.

(2) `Reduce` - Aggregate the results across all of the completed, parallelized sub-tasks.

## Goal: build an LLM agent that uses map-reduce and send API to summerize an article from wikipedia .  Use LLm to classify the document into a list of paragraphs and summerize them simultaniously.

### Mental model:
Imagine you have a long article split into 5 paragraphs: Code
```
[p1, p2, p3, p4, p5]
```
You want the LLM to summarize each paragraph in parallel, then combine them.

**Map‑reduce does:**

`Map: `
- For each paragraph → send to LLM

`Reduce: `
- Combine all summaries → final summary

## Step 1 — Define your State
python
```
from typing_extensions import TypedDict , List , Annotated
from operator import add
from langchain_community.document_loaders import WikipediaLoader


class overallState(TypedDict):
    question: str
    Doc:str
    paragraph_list: List[str]
    summarized_list: Annotated[List[str] , add]
    final_summary:str
```
## Step 2 — Create the LLM (Gemini, OpenAI, etc.)
Example with Gemini: python
```
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
```
##  Step 3 — Generate document using wikipedia
```
def get_doc(state:overallState):
    ''' extract document via wikipedia'''
    
    doc = WikipediaLoader(query=state['question'], load_max_docs=1, doc_content_chars_max=5000).load()
    return {'Doc' : doc[0].metadata['summary'] }
```
- Generates document from wikipedia model

## Step 4 — clssify the document into list of 4 paragraphs using LLM
```

class list_prompt(BaseModel):
    para_list: List[str]

def set_para(state):
    ''' classify the doc into paragraphs'''
    prompt = f"classify the following doc into a list of 4 paragraphs. doc = {state['Doc']}. Create a list"
    response = llm.with_structured_output(list_prompt).invoke(prompt)
    return {'paragraph_list': response.para_list }

```
- Use pydantic model to generate json output
- This node function creates a lsit of paragraph

## Step 5 — Write the MAP node
This node uses Send to create one task per chunk.

```
from langgraph.graph import Send

def map_summarize(state):
    para_list = state['paragraph_list']
    return [Send('summarize' , {'paragraph' : paragraph}) for paragraph in para_list]

```
- maps each paragraph to the state and summerizes it parallelly
- state is auto created and isn't connected to the original state. 

## Step 6 — Write the LLM “summarizer” node
python
```
def summarize(state):
    para = state['paragraph']
    summary_prompt = " Just summerize the paragraph given {} in 3 sentences without providing the guide.".format(para)
    response  = llm.invoke(summary_prompt)
    return {'summarized_list': [response.content[-1]['text']] }
```
Important:
- It returns a list so LangGraph can merge them
- Each LLM call handles one paragraph

## step 7 — Write the REDUCE node
This merges all partial summaries and produces a final summary.

python
```
def reduce_final_summary(state):
    '''reduce the partial summaries into one final summary '''
    
    partial_summary = state['summarized_list']
    final_sum_prompt = f"combine the list of partial summaries into one final summary without explaining.{partial_summary}"
    response = llm.invoke(final_sum_prompt)
    return {'final_summary' : response.content[-1]['text'] }

```
## Step 8 — Build the graph
```
# build graph
from langgraph.graph import StateGraph, START , END

builder = StateGraph(overallState)

# add nodes
builder.add_node('get_doc' , get_doc)
builder.add_node('set_paragraph' , set_para)
builder.add_node('summarize' , summarize)
builder.add_node('reduce_final_summary' , reduce_final_summary)

# add flow
builder.set_entry_point('get_doc')
builder.add_edge('get_doc', 'set_paragraph')
builder.add_conditional_edges('set_paragraph' , map_summarize, ['summarize'])
builder.add_edge('summarize', 'reduce_final_summary')
builder.add_edge('reduce_final_summary', END)

# compile
graph = builder.compile()

graph
```
## Step 9 — Run it

```
question = "what is AI?"
chunks = []
for chunk in graph.stream({"question": question } , stream_mode="updates"): 
    chunks.append(chunk)
    print(chunk)
    print("-"*40)
```





