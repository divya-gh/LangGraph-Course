from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState, StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.tools import tool
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_USE_V1"] = "true"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

llm_with_tool = llm.bind_tools([multiply])

def tool_calling_llm(state: MessagesState):
    response = llm_with_tool.invoke(state["messages"])
    return {"messages": state['messages'] + [response]}

def tool_execute(state: MessagesState):
    msgs = state.get("messages", [])
    if not msgs:
        return {"messages": []}

    last = msgs[-1]
    calls = getattr(last, "tool_calls", None)
    if not calls:
        return {"messages": []}

    for call in calls:
        if call["name"] == "multiply":
            result = multiply.invoke(call["args"])
            return {
                "messages": state['messages'] + [
                    ToolMessage(
                        content=str(result),
                        tool_call_id=call["id"]
                    )
                ]
            }

    return {"messages": []}

def route(state):
    msgs = state.get("messages", [])
    if not msgs:
        return END

    last = msgs[-1]
    calls = getattr(last, "tool_calls", None)

    if calls:
        return "tool_execute_node"
    return END


builder2 = StateGraph(MessagesState)
builder2.add_node("Tool_Calling_Node", tool_calling_llm)
builder2.add_node("tool_execute_node", tool_execute)

builder2.set_entry_point("Tool_Calling_Node")
builder2.add_edge(START, "Tool_Calling_Node")

builder2.add_conditional_edges(
    "Tool_Calling_Node",
    route,
    {"tool_execute_node": "tool_execute_node", END: END}
)

builder2.add_edge("tool_execute_node", "Tool_Calling_Node")

graph2 = builder2.compile()


graph2.invoke({"messages": [HumanMessage(content="What is 5 multiplied by 3?")]})
