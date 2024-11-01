import sqlite3

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from src.graph.full_graph import graph
from src.langgraph_helper import graph_to_png

JUST_PRINT_GRAPH = False

# Create the memory
conn = sqlite3.connect(":memory:", check_same_thread=False)
memory = SqliteSaver(conn)

agent_system = graph.compile(checkpointer=memory)
graph_to_png(agent_system, "agent_system.png")

if not JUST_PRINT_GRAPH:
    config = {"configurable": {"thread_id": "1"}}
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        events = agent_system.stream({"messages": ("user", user_input)}, config, stream_mode="values")
        for event in events:
            last_message = event["messages"][-1]
            if isinstance(last_message, HumanMessage) or (
                    isinstance(last_message, AIMessage) and not last_message.tool_calls):
                last_message.pretty_print()
    # cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = cursor.fetchall()
    # print("Tables:", tables)
    #
    # cursor.execute("PRAGMA table_info(checkpoints);")
    # schema = cursor.fetchall()
    # print("Schema:", schema)
    #
    # cursor.execute("PRAGMA table_info(writes);")
    # schema = cursor.fetchall()
    # print("Schema:", schema)
    #
    #
    # cursor.execute("SELECT * FROM checkpoints")
    # all_messages = cursor.fetchall()
    # for msg in all_messages:
    #     print(msg)  # Adjust based on actual column names and message format
