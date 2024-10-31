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
You are very in detecting calculations.
If you detect a calculation, return TRUE. If not, return FALSE.

You should only respond with TRUE or FALSE. Absolutely no other information should be provided.
"""

# Get the prompt to use - you can modify this!
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember, only respond with TRUE or FALSE.",
        ),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    model="gpt-4o-mini",
    streaming=True,
    temperature=0.0,
)

sentinel_runnable = {"messages": RunnablePassthrough()} | prompt | llm
