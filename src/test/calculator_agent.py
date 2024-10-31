from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI


@tool
def add(a: int, b: int) -> int:
    """Add two numbers a and b and return the sum"""
    return a + b


system_prompt_initial = """
You are very good in calculation.

If you get a calculation question, call the correct tool to get the answer.

Do not guess the answer. Always call your tool.
"""

# Get the prompt to use - you can modify this!
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember, always call a tool with the calculation question.",
        ),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    model="gpt-4o-mini",
    streaming=True,
    temperature=0.0,
)

agent_tools = [add]


calculator_runnable = {"messages": RunnablePassthrough()} | prompt | llm.bind_tools(agent_tools)
