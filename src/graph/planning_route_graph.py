from typing import Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from src.planner.planning_agent import planning_agent_runnable
from src.route.route_agent import route_agent_tools, route_agent_runnable


# contains just the planning agent

class State(TypedDict):
    messages: Annotated[list, add_messages]


def planning_agent(state: State):
    return {"messages": [planning_agent_runnable.invoke(state["messages"])]}


def sub_agent(state: State):
    messages = state["messages"]
    last_message = messages[-1]

    if "ROUTE PLANNING" in last_message.content:
        return "route_agent"

    return "end"


def route_agent(state: State):
    return {"messages": [route_agent_runnable.invoke(state["messages"])]}


def is_tools_call(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    return len(last_message.tool_calls) > 0


route_agent_tools = ToolNode(tools=route_agent_tools)

# Create the graph
graph = StateGraph(State)

# create the nodes
graph.add_node("planning_agent", planning_agent)
graph.add_node("route_agent", route_agent)
graph.add_node("route_agent_tools", route_agent_tools)

# create the edges

# from planning agent to route agent
graph.add_conditional_edges("planning_agent",
                            sub_agent,
                            path_map={
                                "route_agent": "route_agent",
                                "end": END
                            })

# from route agent to its tools
graph.add_conditional_edges("route_agent",
                            is_tools_call,
                            path_map={
                                True: "route_agent_tools",
                                False: END
                            })
graph.add_edge("route_agent_tools", "route_agent")

graph.set_entry_point("planning_agent")
graph.set_finish_point("planning_agent")
