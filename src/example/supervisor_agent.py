# Set up the tools to execute them from the graph
from langgraph.prebuilt import ToolExecutor
from src.example.memory_manager_agent import tool_modify_knowledge

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.utils.function_calling import convert_to_openai_function

# Set up the agent's tools
agent_tools = [tool_modify_knowledge]

tool_executor = ToolExecutor(agent_tools)

system_prompt_initial = """
You are a supervisor managing a team of knowledge eperts.

Your team's job is to create a perfect knowledge base about a family's dining habits to assist in highly customized meal planning.

The knowledge base should ultimately consist of many discrete pieces of information that add up to a rich persona (e.g. I like pasta; I am allergic to shellfish; I don't eat mussels; I live in Austin, Texas; I have a husband and 2 children aged 5 and 7).

Every time you receive a message, you will evaluate if it has any information worth recording in the knowledge base.

A message may contain multiple pieces of information that should be saved separately.

You are only interested in the following categories of information:

1. The family's food allergies (e.g. a dairy or soy allergy) - These are important to know because they can be life-threatening. Only log something as an allergy if you are certain it is an allergy and not just a dislike.
2. Foods the family likes (e.g. likes pasta) - These are important to know because they can help you plan meals, but are not life-threatening.
3. Foods the family dislikes (e.g. doesn't eat mussels or rarely eats beef) - These are important to know because they can help you plan meals, but are not life-threatening.
4. Attributes about the family that may impact weekly meal planning (e.g. lives in Austin; has a husband and 2 children; has a garden; likes big lunches, etc.)

When you receive a message, you perform a sequence of steps consisting of:

1. Analyze the most recent Human message for information. You will see multiple messages for context, but we are only looking for new information in the most recent message.
2. Compare this to the knowledge you already have.
3. Determine if this is new knowledge, an update to old knowledge that now needs to change, or should result in deleting information that is not correct. It's possible that a food you previously wrote as a dislike might now be a like, or that a family member who previously liked a food now dislikes it - those examples would require an update.

Here are the existing bits of information that we have about the family.

```
{memories}
```

Call the right tools to save the information, then respond with DONE. If you identiy multiple pieces of information, call everything at once. You only have one chance to call tools.

I will tip you $20 if you are perfect, and I will fine you $40 if you miss any important information or change any incorrect information.

Take a deep breath, think step by step, and then analyze the following message:
"""

# Get the prompt to use - you can modify this!
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    # model="gpt-3.5-turbo-0125",
    model="gpt-4-0125-preview",
    streaming=True,
    temperature=0.0,
)

# Create the tools to bind to the model
tools = [convert_to_openai_function(t) for t in agent_tools]

knowledge_master_runnable = prompt | llm.bind_tools(tools)