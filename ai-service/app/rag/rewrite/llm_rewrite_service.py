from app.llm.services.llm_service import (
    llm_chat
)


def rewrite_query_llm(
        query: str
):
    """
    Query Rewrite

    用户自然语言
    ↓
    标准检索问题
    """

    prompt = f"""
你是企业知识库检索优化器。

请把用户问题改写成更适合知识库检索的问题。

要求：

1 保留原意

2 保留关键实体

3 不要回答问题

4 不要解释

5 只返回改写后的问题

用户问题：

{query}
"""

    try:

        rewritten = llm_chat(
            prompt
        )

        return rewritten.strip()

    except Exception as e:

        print(
            "LLM Rewrite Error:",
            e
        )

        return query