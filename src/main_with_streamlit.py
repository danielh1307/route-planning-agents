import sqlite3

import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from src.graph.full_graph import graph

st.title("ChatGPT-like clone")

# Create the memory


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.config = {"configurable": {"thread_id": "1"}}
    st.session_state.conn = sqlite3.connect(":memory:", check_same_thread=False)
    st.session_state.memory = SqliteSaver(st.session_state.conn)
    st.session_state.agent_system = graph.compile(checkpointer=st.session_state.memory)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        events = st.session_state.agent_system.stream({"messages": ("user", user_input)}, st.session_state.config,
                                                      stream_mode="values")
        for event in events:
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage):
                st.session_state.messages.append({"role": "assistant", "content": last_message.content})
                print({"role": "assistant", "content": last_message.content})
            if isinstance(last_message, ToolMessage):
                st.session_state.messages.append({"role": "tool", "content": last_message.content})
                print({"role": "tool", "content": last_message.content})
            last_message.pretty_print()
            st.write(last_message.content)
