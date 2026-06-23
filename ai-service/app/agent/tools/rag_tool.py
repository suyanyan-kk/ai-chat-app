from langchain.tools import tool

import json

from app.agent.workflow.rag_service import (
    run_rag_graph
)


@tool
def search_knowledge(query: str):

    """
    查询企业知识库。

    仅当用户明确要求查询知识库、资料库、上传文档或内部资料时使用。
    不要用于普通聊天、MCP 咨询、天气、时间、计算或一般百科问题。
    """

    rag_data = run_rag_graph(query)

    return json.dumps({

        "context":
            rag_data["context"],

        "sources":
            rag_data["sources"]

    }, ensure_ascii=False)
