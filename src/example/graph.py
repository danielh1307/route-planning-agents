import json
from typing import TypedDict, Sequence

from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolInvocation

from src.example.memory_sentinel_agent import sentinel_runnable
from src.example.supervisor_agent import knowledge_master_runnable
from src.example.supervisor_agent import tool_executor


class AgentState(TypedDict):
    # The list of previous messages in the conversation
    messages: Sequence[BaseMessage]
    # The long-term memories to remember
    memories: Sequence[str]
    # Whether the information is relevant
    contains_information: str


def call_sentinel(state):
    messages = state["messages"]

    response = sentinel_runnable.invoke(messages)
    return {"contains_information": "TRUE" in response.content and "yes" or "no"}


# Define the function that determines whether to continue or not
def should_continue(state):
    last_message = state["messages"][-1]
    # If there are no tool calls, then we finish
    if "tool_calls" not in last_message.additional_kwargs:
        return "end"
    # Otherwise, we continue
    else:
        return "continue"


# Define the function that calls the knowledge master
def call_knowledge_master(state):
    messages = state["messages"]
    memories = state.get("memories", "")
    response = knowledge_master_runnable.invoke(
        {"messages": messages, "memories": memories}
    )
    return {"messages": messages + [response]}


# Define the function to execute tools
def call_tool(state):
    messages = state["messages"]
    # We know the last message involves at least one tool call
    last_message = messages[-1]

    # We loop through all tool calls and append the message to our message log
    for tool_call in last_message.additional_kwargs["tool_calls"]:
        action = ToolInvocation(
            tool=tool_call["function"]["name"],
            tool_input=json.loads(tool_call["function"]["arguments"]),
            id=tool_call["id"],
        )

        # We call the tool_executor and get back a response
        response = tool_executor.invoke(action)
        # We use the response to create a FunctionMessage
        function_message = ToolMessage(
            content=str(response), name=action.tool, tool_call_id=tool_call["id"]
        )

        # Add the function message to the list
        messages.append(function_message)
    return {"messages": messages}
