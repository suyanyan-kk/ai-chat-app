from langchain_core.messages import (
    HumanMessage
)

from app.llm.model import model


def llm_chat(
        prompt: str
):
    """
    统一LLM调用入口

    后续：
    Rewrite
    Multi Query
    Conversation Summary
    Agent Planner

    都调用这里
    """

    response = model.invoke(

        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    return response.content.strip()