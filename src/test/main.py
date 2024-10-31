import sqlite3
from typing import Annotated

from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from src.example.langgraph_helper import graph_to_png
from src.test.calculator_agent import agent_tools
from src.test.calculator_agent import calculator_runnable
from src.test.memory_sentinel_agent import sentinel_runnable

llm = ChatOpenAI(
    model="gpt-4o-mini",
    streaming=True,
    temperature=0.0,
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def sentinel(state: State):
    # {"messages": [sentinel_runnable.invoke(state["messages"])]}
    response = sentinel_runnable.invoke(state["messages"])
    return {"messages": "TRUE" in response.content and "yes" or "no"}


def calculator(state: State):
    return {"messages": [calculator_runnable.invoke(state["messages"])]}


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def is_tools_call(state: State):
    messages = state["messages"]
    last_message = messages[-1]

    return len(last_message.tool_calls) > 0


tool_node = ToolNode(tools=agent_tools)

# Create the memory
conn = sqlite3.connect(":memory:", check_same_thread=False)
memory = SqliteSaver(conn)

# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("sentinel", sentinel)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("calculator", calculator)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_conditional_edges("sentinel",
                                    lambda x: "messages" in x and len(x["messages"]) > 0 and x["messages"][
                                        -1].content == 'yes',
                                    path_map={
                                        True: "calculator",
                                        False: "chatbot"
                                    })

# graph_builder.add_conditional_edges("calculator",
#                                     tools_condition)

graph_builder.add_conditional_edges("calculator",
                                    is_tools_call,
                                    path_map={
                                        True: "tools",
                                        False: END
                                    })

# Any time a tool is called, we return to the calculator
graph_builder.add_edge("tools", "chatbot")

graph_builder.set_entry_point("sentinel")
graph_builder.set_finish_point("chatbot")

graph = graph_builder.compile(checkpointer=memory)
graph_to_png(graph, "langgraph_test.png")

config = {"configurable": {"thread_id": "1"}}
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    events = graph.stream({"messages": ("user", user_input)}, config, stream_mode="values")
    for event in events:
        event["messages"][-1].pretty_print()
