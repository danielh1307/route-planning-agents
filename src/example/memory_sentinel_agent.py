from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI

system_prompt_initial = """
Your job is to assess a brief chat history in order to determine if the conversation contains any details about a family's dining habits. 

You are part of a team building a knowledge base regarding a family's dining habits to assist in highly customized meal planning.

You play the critical role of assessing the message to determine if it contains any information worth recording in the knowledge base.

You are only interested in the following categories of information:

1. The family's food allergies (e.g. a dairy or soy allergy)
2. Foods the family likes (e.g. likes pasta)
3. Foods the family dislikes (e.g. doesn't eat mussels)
4. Attributes about the family that may impact weekly meal planning (e.g. lives in Austin; has a husband and 2 children; has a garden; likes big lunches; etc.)

When you receive a message, you perform a sequence of steps consisting of:

1. Analyze the message for information.
2. If it has any information worth recording, return TRUE. If not, return FALSE.

You should ONLY RESPOND WITH TRUE OR FALSE. Absolutely no other information should be provided.

Take a deep breath, think step by step, and then analyze the following message:
"""

# Get the prompt to use - you can modify this!
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember, only respond with TRUE or FALSE. Do not provide any other information.",
        ),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    streaming=True,
    temperature=0.0,
)

sentinel_runnable = {"messages": RunnablePassthrough()} | prompt | llm
