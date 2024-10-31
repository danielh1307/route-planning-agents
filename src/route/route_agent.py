from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

from src.route.route_tools import get_coordinates, get_detailed_route

route_agent_system_prompt = """
You are a helpful assistant in route planning, both for hiking and biking.

You will get a starting point, an end point and a vehicle (either bike or foot).

Your task is to provide details of the route. Details include the distance and the duration.

Use your available tools to get this information. In most cases, you must first get the
coordinates of the start and end point and afterwards you can get the details of the route.
"""

route_agent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(route_agent_system_prompt),
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

route_agent_tools = [get_coordinates, get_detailed_route]

route_agent_runnable = {"messages": RunnablePassthrough()} | route_agent_prompt | llm.bind_tools(route_agent_tools)
