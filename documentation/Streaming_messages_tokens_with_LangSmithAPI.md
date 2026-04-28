# Streaming with LangSmith API
LangSmith has built in memory and easy streaming of state, events, tokens , values with built in methods

## Setup LangSmith development framework:

##### 1. Steps:
Have Agent.py file ready in the studio folder(copy from Code/studio)
keep .env file with LangSmith API keys and GOOGle API keys ready
set langgraph.json file ready
To start the local development server, run the following command in your terminal in the /studio directory in this module: BAsh ' langgraph dev '
check for output:
API: http://127.0.0.1:2024

🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
📚 API Docs: http://127.0.0.1:2024/docs
This in-memory server is designed for development and testing. For production use, please use LangSmith Deployment.

Copy url = http://127.0.0.1:2024
Note:
check for more info : https://docs.langchain.com/langsmith/quick-start-studio#local-development-server

- check for LangSmith setup guide in the begining of the course.

#### 2. Connecting to the Local Server Using the SDK
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

#### 3. Create a thread for storing event checkpoints:
A thread is a conversation session.
It stores:

- messages
- memory
- state
- checkpoints
You create one like this: python
```
thread = await client.threads.create()
## This returns: python

{"thread_id": "abc123"}
```
- You will use this thread ID for the entire conversation.

#### 4. Running the Agent With Streaming
You run your agent like this: python

async for chunk in client.runs.stream(
        thread['thread_id'],   # which conversation
        "agent",               # which assistant
        input={'messages': msg_input},       # what the user said
        stream_mode="values",  # stream full state after each step
    ):
What happens? Your agent runs step by step:

- LLM node
- Tool node
- LLM node
- Final answer
After each step, LangGraph sends you a chunk containing the updated state.

### Note:
- Streamed obejects have event that is type and data = state with field values
- Event is streamed as the state gets updated

#### 5. Stream only messages :
You can filter the messages from the events streamed using,
*convert_to_messages* function
python
```
from langchain_core.messages import convert_to_messages

#set messages
input_message = HumanMessage(content="Multiply 20 and 3")

# stream agent
async for event in client.runs.stream(thread["thread_id"], assistant_id="agent", input={"messages": [input_message]}, stream_mode="values"):
    messages = event.data.get('messages',None)
    if messages:
        print(convert_to_messages(messages)[0])
        print('='*25)

## output:
content='Multiply 20 and 3' additional_kwargs={} response_metadata={} id='88e8af04-293e-444f-a1e3-04b4af5302d4'
=========================
content='Multiply 20 and 3' additional_kwargs={} response_metadata={} id='88e8af04-293e-444f-a1e3-04b4af5302d4'
```
## Stream_mode = 'messages':
LangSmith API comes with few streaming modes. one of them is *streaming messages*

All events emitted using messages mode have two attributes:

    - event: This is the name of the event
    - data: This is data associated with the event

#### Note:
metadata: metadata about the run
messages/complete: fully formed message
messages/partial: chat model tokens

### Filtering events and data :

You can filter following data,    
1. MeataData Run ID
2. Tool Calls
3. Invalid tool Calls
4. Usage metadata - finish reason , model_name
6. Response metadata
7. function call - name

#### EX: output:
```
Tool Calls:
Tool_Call_Name: multiply, Tool_Call_ID: 8efbdc8e-71fe-4a6d-b6bd-7f415a2c18a3, Arg: {'b': 50, 'a': 10}
Response MetaData:
model_name: None, Finish Reason: None
Usage MetaData:
Input Tokens: 254, Output Tokens: 18, Total Tokens: 272
--------------------
AI-content:  The result
Response MetaData:
model_name: None, Finish Reason: None
Usage MetaData:
Input Tokens: 284, Output Tokens: 2, Total Tokens: 286
```
## Full Example:
python:
```
thread = await client.threads.create()
input_message = HumanMessage(content="multiply 10 and 50")
events= []
async for event in client.runs.stream(thread["thread_id"], assistant_id="agent", input={"messages": [input_message]}, stream_mode="messages"):
    events.append(event)
    print(event)
    print("*"*30)

#print metaData Run-ID
for event in events:
    if event.event == 'metadata':
       print(f"MetaData- Run-ID: {event.data['run_id']}")

#Filter data for event: 'messages/partial'
for event in events:
    if event.event == 'messages/partial':
        content = event.data[0].get('content',"")
        tool_calls = event.data[0].get('tool_calls',[])
        invalid_tool_calls = event.data[0].get('invalid_tool_calls',[])
        response_metadata = event.data[0].get('response_metadata',{})
        usage_metadata = event.data[0].get('usage_metadata',{})
        if content:
            print("AI-content: ", content[0]['text'])
        if tool_calls:
            print("Tool Calls:")
            print(f"Tool_Call_Name: {tool_calls[-1]['name']}, Tool_Call_ID: {tool_calls[-1]['id']}, Arg: {tool_calls[-1]['args']}")
        if invalid_tool_calls :
            print("Invalid Tool Calls:")
            print(f"Tool_Call_Name: {tool_calls[-1]['name']}, Tool_Call_ID: {tool_calls[-1]['id']}, Arg: {tool_calls[-1]['args']}")
        if response_metadata:
            print("Response MetaData:")
            print(f"model_name: {response_metadata.get('model_name',"None")}, Finish Reason: {response_metadata.get('finish_reason',"None")}")
        if usage_metadata:
            print("Usage MetaData:")
            print(f"Input Tokens: {usage_metadata['input_tokens']}, Output Tokens: {usage_metadata['output_tokens']}, Total Tokens: {usage_metadata['total_tokens']}")

        print("-"*50)
```

