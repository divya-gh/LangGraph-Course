# LangSmith Developement Environment -Streaming and Breakpoints

## Stream 'messages' :
You can stream only 'messages' with 
```
from langchain_core.messages import convert_to_messages
```
### EX:
```thread = await client.threads.create()
input_message = HumanMessage(content="Multiply 20 and 3")
async for event in client.runs.stream(thread["thread_id"], assistant_id="agent", input={"messages": [input_message]}, stream_mode="values"):
    messages = event.data.get('messages',None)
    if messages:
        print(convert_to_messages(messages)[0])
    print('='*25)
```
## # Streaming mode in LangSmith API
** stream_mode = 'messages' **

#### All events emitted using messages mode have two attributes:
- event: This is the name of the event
- data: This is data associated with the event

#### Note:
- metadata: metadata about the run
- messages/complete: fully formed message
- messages/partial: chat model tokens

### EX:
```

thread = await client.threads.create()
input_message = HumanMessage(content="add 100 and 50")
async for event in client.runs.stream(thread["thread_id"], assistant_id="agent", input={"messages": [input_message]}, stream_mode="messages"):
    print(event.event)
```

Output looks like:
```
metadata
messages/metadata
messages/partial
messages/partial
messages/partial
messages/metadata
messages/complete
messages/metadata
messages/partial
messages/partial
```
## Filtering tokens and contents from streamed data
Using python filter out streamed data for debugging and analysis
- metadata: metadata about the run
- messages/complete: fully formed message
- messages/partial: chat model tokens

```
if event.event == "metadata":
        print(f"Metadata: Run ID - {event.data['run_id']}")
        print("-" * 50)
    
    # Handle partial message events
    elif event.event == "messages/partial":
        for data_item in event.data:
            # Process user messages
            if "role" in data_item and data_item["role"] == "user":
                print(f"Human: {data_item['content']}")
            else:
                # Extract relevant data from the event
                tool_calls = data_item.get("tool_calls", [])
                invalid_tool_calls = data_item.get("invalid_tool_calls", [])
                content = data_item.get("content", "")
                response_metadata = data_item.get("response_metadata", {})

                if content:
                    print(f"AI: {content}")

                if tool_calls:
                    print("Tool Calls:")
                    print(format_tool_calls(tool_calls))

                if invalid_tool_calls:
                    print("Invalid Tool Calls:")
                    print(format_tool_calls(invalid_tool_calls))

                if response_metadata and response_metadata.get("finish_reason"):
                    print(f"Response Metadata: Finish Reason - {response_metadata['finish_reason']}")                    
        print("-" * 50)
```
# Breakpoints in LangSmith API

# Static interrupts
- Static interrupts (also known as static breakpoints) are triggered either before or after a node executes.
- Static interrupts are not recommended for human-in-the-loop workflows. They are best used for debugging and testing.
#### Method 1:  You can set static interrupts by specifying interrupt_before and interrupt_after at compile time:
```
graph = graph_builder.compile( # (interrupt 1)!
    interrupt_before=["node_a"], # (interrupt 2)!
    interrupt_after=["node_b", "node_c"], # (interrupt 3)!
)
```

- The breakpoints are set during compile time.
- interrupt_before specifies the nodes where execution should pause before the node is executed.
- interrupt_after specifies the nodes where execution should pause after the node is executed.

#### Method 2: Alternatively, you can set static interrupts at run time:
```
await client.runs.wait( # (1)!
    thread_id,
    assistant_id,
    inputs=inputs,
    interrupt_before=["node_a"], # (2)!
    interrupt_after=["node_b", "node_c"] # (3)!
)
```
- client.runs.wait is called with the interrupt_before and interrupt_after parameters. This is a run-time configuration and can be changed for every invocation.
- interrupt_before specifies the nodes where execution should pause before the node is executed.
- interrupt_after specifies the nodes where execution should pause after the node is executed.

OR

```
Initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}
thread = await client.threads.create()
async for chunk in client.runs.stream(
    thread["thread_id"],
    assistant_id="agent",
    input=initial_input,
    stream_mode="values",
    interrupt_before=["tools"],
):
    print(f"Receiving new event: {chunk}...")

```
# User Assistatnce
Graph can be resumes after an interruption
```
if toolcall:
    user_approval = input("Do you want to continue?(yes/no): ").lower()
    if user_approval == 'yes':
        # pass None as input to the graph and continue from the last statenusing the thread_ID
        async for event in client.runs.stream(
            thread["thread_id"],
            "agent",
            input=None,
            stream_mode="values",
            interrupt_before=["tools"],
        ):
            print(f"Receiving new event of type: {event.event}...")
            messages = event.data.get('messages', [])
            if messages:
                print(messages[-1])
            print("-" * 50)
```
- Graph stops before the tool node
- Set up user approval
- If user approves, run the graph with None input.
- Since state checkpoints (data) are stored in the thread_id, using the same thread will rerun the graph.

OR for await client.runs.wait, use:
```

# Resume the graph
await client.runs.wait(
    thread_id,
    assistant_id,
    input=None   # (2)!
)
```


