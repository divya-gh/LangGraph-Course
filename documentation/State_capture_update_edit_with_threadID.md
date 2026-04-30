# State Checkpoints and history

Lets explore:
1. state capture
2. Editing/updating state messages
3. Human Feedback

#### Note: Graph must be built with memory to capture checkpoint

<img src="../Images/state_checkpoints_memory.png" width="350" height="400">

1. Get State: state capture
```
state = graph.get_state(thread)
```
where thread is : thread = {"configurable":{'thread_ID': "1"}}

Get the most recent and current checkpoints

2. Super- step : 
 Each super-step is a sequencial node collecting state information and its metadata as well as what's next .

3. checkpointer: 
stores and save state using a thread ID

4. Thread ID: collection of stored data or checkpointers

5. capture what's next:
superstep smartly notes what node comes next. we can use this to identify next execution task
```
state = graph.get_state(thread)
Next = state.next
```
- Shows what node is next wiht node name.

6. state_values = state = graph.get_state(thread).values
- gets key values that is stored in the thread
------------------------------------------------------------------------------
# State Updates:

State can be updated directly using the threadID that it uses to store checkpoints.

- Mainly used for human approval or modification in user information after a interruption usign a breakpoint.

## Ex:
```
Initial_input = {"messages": "Multiply 2 and 3"}

# Thread
thread_config = {"configurable": {"thread_id": "2"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event['messages'])

# Get State:
state = graph.get_state(thread_config)
state - Shows the state messages using the threadID
```

### update the state messages
As we know reducer 'MessagesState" uses add_messages Annotation in the state schema that ammends the messages , update also ammend messages to the state by default.

```
graph.update_state(
    thread,
    {"messages": [HumanMessage(content="No, actually multiply 3 and 3!")]},
)

# Check state again
state = graph.get_state(thread_config)
state
```
### Output: 
```
{'messages': [HumanMessage(content='Multiply 2 and 3', additional_kwargs={}, response_metadata={}, id='5d8f913f-69d8-437a-9cad-84aa98bfc67f'),
              HumanMessage(content='No, actually multiply 3 and 3!', additional_kwargs={}, response_metadata={}, id='7d501771-bd79-4d73-9fe4-ebd471dc2bf8')]}

```
- state contains original message with new updated message


--------------------------------------------------------------

## Human Feedback:








