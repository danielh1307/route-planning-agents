from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

from src.cal.calendar_tools import get_events

calendar_agent_system_prompt = """
You are a helpful assistant and part of a trip planning system.

Your task is to determine the free time of a user at a specific date. 

Use your available tools to get this information. You will be provided with a date, and your 
task is to get the user's events at this date. 

Use your tool only once, and then give a clear and concise answer. Do not use your tools multiple times!

Summarize the events and free time clear and concise.
"""

calendar_agent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(calendar_agent_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember to use your available tools.",
        ),
    ]
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    streaming=True,
    temperature=0.0,
)

calendar_agent_tools = [get_events]

calendar_agent_runnable = {"messages": RunnablePassthrough()} | calendar_agent_prompt | llm.bind_tools(
    calendar_agent_tools)
