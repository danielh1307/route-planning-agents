from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

planning_agent_system_prompt = """
You are a helpful assistant tasked with planning my next hiking or bike tour.

This tour requires:

A route: consists of a specific start point, end point and a vehicle. Unless you are told to choose something randomly, ask for this information. Ask as long as you have all information.
A specific date: This date must be available on my calendar, meaning no other events are scheduled.
Weather conditions: Provide details on the weather forecast for the chosen date and location.

What you must know: Today, we have Wednesday, October 30th in 2024. I live in Switzerland.

You must not plan the tour alone. Use the following helpers:

ROUTE PLANNING: To get a detailed route from one place to another, say "ROUTE PLANNING" followed by the starting point, end point, and whether it's by foot or bike. Example: "ROUTE PLANNING from City Park to Mountain View by bike."
WEATHER CHECK: To get specific weather conditions for a place or region, say "WEATHER" followed by a desired date and place. Example: "WEATHER CHECK for July 15th 2024 in Miami." Always check the weather only for one day, not multiple days.
DATE CHECK: To check my availability and find a date with no other events, say "DATE" followed by a specific day you're considering. Example: "DATE CHECK for July 15th 2024." Always check the date only for one day, not multiple days.
Please follow these instructions and use your helpers. Avoid making up information if a helper can provide the answer.
"""

planning_agent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(planning_agent_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember to use your helper.",
        ),
    ]
)

llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    temperature=0.0,
)

planning_agent_runnable = {"messages": RunnablePassthrough()} | planning_agent_prompt | llm
