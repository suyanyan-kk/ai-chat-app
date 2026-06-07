import json

from app.llm.services.llm_service import (
    llm_chat
)


def generate_multi_queries_llm(
        query: str
):
    """
    生成多个检索Query
    """

    prompt = f"""
你是企业RAG检索优化器。

请根据用户问题生成4个不同表达方式的检索问题。

要求：

1 保持同一个意思

2 使用不同关键词

3 不要回答问题

4 返回JSON数组

示例：

[
  "Vue3组件通信方式有哪些",
  "Vue3 props emit provide inject",
  "Vue3父子组件通信",
  "Vue3组件数据传递"
]

用户问题：

{query}
"""

    try:

        result = llm_chat( 
            prompt
        )

        print(
            "LLM Multi Query Raw:",
            result
        )

        queries = json.loads(
            result
        )

        if query not in queries:

            queries.insert(
                0,
                query
            )

        return list(
            dict.fromkeys(queries)
        )

    except Exception as e:

        print(
            "LLM Multi Query Error:",
            e
        )

        return [query]