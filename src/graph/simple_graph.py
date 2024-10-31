from typing import Annotated

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from src.planner.planning_agent import planning_agent_runnable


# contains just the planning agent

class State(TypedDict):
    messages: Annotated[list, add_messages]


def planning_agent(state: State):
    return {"messages": [planning_agent_runnable.invoke(state["messages"])]}


# Create the graph
graph = StateGraph(State)

graph.add_node("planning_agent", planning_agent)
graph.set_entry_point("planning_agent")
graph.set_finish_point("planning_agent")
