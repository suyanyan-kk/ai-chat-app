
from langchain.tools import tool

from app.agent.schemas.tool_schema import (
    SearchKnowledgeInput
)

# from app.rag.retrieval.retrieval_service import (
#     retrieval_pipeline
# )
from app.agent.workflow.rag_graph import rag_graph 

import json
# agent tool: 搜索知识库内容
# Tool的参数定义在 schemas/tool_schema.py 中，
# 使用 Pydantic 的 BaseModel 定义输入参数的结构和校验规则。
@tool(
    args_schema=SearchKnowledgeInput
)
def search_knowledge(
    query: str
) -> str:
    """
    搜索知识库内容
    """
    # 1、retrieval_pipeline 是一个函数，负责执行 RAG 流程，包括检索、重排序和上下文构建等步骤。
    # result = retrieval_pipeline(
    #     query=query
    # )
    
    # 2、workflow 方式调用 RAG 流程
    
    result = rag_graph.invoke(
    {
        "query": query
    }
)
    return json.dumps({

        "context":
            result["context"],

        "sources":
            result["sources"]

    }, ensure_ascii=False)