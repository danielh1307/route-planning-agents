from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

from src.route.route_tools import get_coordinates
from src.weather.weather_tools import get_weather

weather_agent_system_prompt = """
You are a helpful assistant in weather prediction.

You will get a date and a Region. Your task is to provide a detailed weather prediction for the date.

Use your available tools to get this information. In most cases, you must first get the
coordinates of the start and end point and afterwards you can get the details of the route.
"""

weather_agent_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(weather_agent_system_prompt),
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

weather_agent_tools = [get_coordinates, get_weather]

weather_agent_runnable = {"messages": RunnablePassthrough()} | weather_agent_prompt | llm.bind_tools(weather_agent_tools)
