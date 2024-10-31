from langgraph.graph import StateGraph, END

from src.example.graph import AgentState
from src.example.graph import call_sentinel, call_tool, call_knowledge_master, should_continue
from langchain_core.messages import HumanMessage


# Initialize a new graph
graph = StateGraph(AgentState)

# Define the two "Nodes"" we will cycle between
graph.add_node("sentinel", call_sentinel)
graph.add_node("knowledge_master", call_knowledge_master)
graph.add_node("action", call_tool)

# Define all our Edges

# Set the Starting Edge
graph.set_entry_point("sentinel")

# We now add Conditional Edges
graph.add_conditional_edges(
    "sentinel",
    lambda x: x["contains_information"],
    {
        "yes": "knowledge_master",
        "no": END,
    },
)
graph.add_conditional_edges(
    "knowledge_master",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# We now add Normal Edges that should always be called after another
graph.add_edge("action", END)

# We compile the entire workflow as a runnable
app = graph.compile()

message = "There are 6 people in my family. My wife doesn't eat meat and my youngest daughter is allergic to dairy."

inputs = {
    "messages": [HumanMessage(content=message)],
}

for output in app.with_config({"run_name": "Memory"}).stream(inputs):
    # stream() yields dictionaries with output keyed by node name
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("---")
        print(value)
    print("\n---\n")