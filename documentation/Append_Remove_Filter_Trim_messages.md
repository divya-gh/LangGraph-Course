
# Append messages - Reducers add_message , MessageState
    - Basic graph usualy replaces the original state when state is updated in the node.
    - Reducers add the old state to new state creating a list that gets appended everytime its updated.
    -Reducers like add and add_messages append the value to the state field which is a list
    - Reducers like removeMessages help delete the unwantd messages from the state which helps maintain token usage , latency and cost
    - reducers like trimMessages help guide llms to only use certain amount of tokens which improves latency and cost while keeping the state messages intact.
    -llms only use grab the content specified to answer the question or generate content.

-----------------------------------------------------------------------
# Remove Message reducer - RemoveMessage

*RemoveMessage* is a reducer that removes a message from a list of messages stored in your graph state.

## Why it exists
LangGraph uses reducers to safely update state in a predictable way.

If your state contains a list of messages (like a chat history), you sometimes want to:

- add a message
- remove a message
- replace a messages

*RemoveMessage* is the reducer that handles the “remove” part.

## 🌱 How it works conceptually
Imagine your state looks like this: python
```
    messages = [
        {"id": "1", "content": "Hello"},
        {"id": "2", "content": "Teach me Agentic AI"}
    ]

```
If you call: python
```
from langchain_core.messages import RemoveMessage

deleted message = [RemoveMessage(id=m.id) for m in messages[:-1]]
new_message = add_messages()
```
This is removing all messages in the list but last one.
The reducer returns: python
```
{
    new_message =  [{"id": "2", "content": "Teach me Agentic AI"}]
}

```
It simply filters out the message with the matching ID.

## using RemoveMessage with MessagesState reducer

RemoveMessage automatically removes messages from the state list for the id's supplied.
MessagesState knows that if the {'messages': RemoveMessage(ids=[msg_id])} , apply removal.

------------------------------------------------------------------------------
# Filtering Messages
Messages cna be filtered before passing into the graph state to avoid token usage or reduce cost and latency

For example, just pass in a filtered list: llm.invoke(messages[-1:]) to the model.

Example: 
```
def chat_model(state:MessagesState):
    return {'messages': llm.invoke(state['messages'][-1:])}

#build graph
builder =StateGraph(MessagesState)

builder.add_node('chat_model',chat_model)

builder.add_edge(START, 'chat_model')
builder.add_edge('chat_model',END)

graph = builder.compile()

result = graph.invoke({'messages': messages})

```
Explaination :
- filter is applied in the node while calling the llm
-state['messages'] are retained but llm only recieves the messages that are specified in the slice.
ex: llm.invoke(state['messages'][-1:])
- response is added to the state messages 
- result contains all the original state messages + llm response

----------------------------------------------------------------------------

# Trimming Messages in LangGraph
Trimming allows LLms only capture the content according to the max_tokens set in the trimmer function.

When you build a chatbot, the conversation history grows longer and longer.
If you send all messages to the model every time, it becomes:

    - slow
    - expensive
    - and may exceed the model’s token limit
    - So we trim the messages — meaning we keep only the most important recent ones.
Your code uses LangChain’s built‑in trim_messages function to do this.

## What is Trimming - Cutting down the conversation history so the model only sees the most important recent messages.

##### Conversations can get very long, and AI models have limits:

    They can only read a certain number of tokens (pieces of text)
    More text = more cost
    More text = slower responses

##### So we “trim” the conversation:

    Keep the most recent messages
    Remove the older ones
    Make sure the total stays under a token limit
This keeps the chatbot fast, cheap, and within the model’s memory limits.

## Reducer function - trim_messages
python
``
from langchain_core.messages import trim_messages
```
This imports a helper that can shorten a list of messages based on token count.

## 🧠 Why trimming is necessary
Without trimming:

    The model might hit its token limit
    The conversation becomes expensive
    The model may get confused by too much old context

With trimming:

    The model sees only what it needs
    The conversation stays focused
    You avoid token overflow errors

## Example: python
```
from langchain_core.messages import trim_messages

def chat_model_node(state: MessagesState):
    messages = trim_messages(
            state["messages"],
            max_tokens=100,
            strategy="last",
            token_counter=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
            allow_partial=False,
        )
    return {"messages": [llm.invoke(messages)]}
```
#### Let’s break it down simply:

#### 1. trim_messages(...)
This function takes the whole conversation and shortens it.

#### 2. max_tokens=100
We want the trimmed conversation to be no more than 100 tokens.mostly last message in the state['messages'] if tokens are set to 100.

#### 3. strategy="last"
Keep the most recent messages.

Like scrolling to the bottom of a chat and ignoring the old stuff.

#### 4. token_counter=ChatGoogleGenerativeAI(...)
Different models count tokens differently. This tells the trimmer how to count them.

#### 5. allow_partial=False
Don’t cut a message in half. Only remove whole messages.

### What happens after trimming?
python
```
return {"messages": [llm.invoke(messages)]}
```

- The trimmed messages are sent to the model.
- The model replies.
- The reply is added to the conversation.

### Summary: Trimming = keeping the conversation short enough for the AI to handle.

--------------------------------------------------------------------


