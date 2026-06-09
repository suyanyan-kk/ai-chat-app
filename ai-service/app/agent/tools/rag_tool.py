from langchain.tools import tool

import json

from app.agent.workflow.rag_service import (
    run_rag_graph
)


@tool
def search_knowledge(query: str):

    """
    查询企业知识库
    """

    rag_data = run_rag_graph(query)

    return json.dumps({

        "context":
            rag_data["context"],

        "sources":
            rag_data["sources"]

    }, ensure_ascii=False)