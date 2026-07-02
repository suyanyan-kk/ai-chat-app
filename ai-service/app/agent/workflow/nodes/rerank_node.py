# app/agent/workflow/nodes/rerank_node.py

from langsmith import traceable

from app.rag.rerank.rerank_service import (
    rerank_documents,
)


@traceable(name="rerank")
def rerank_node(state):
    """
    Rerank Node。

    这里不直接关心 ENABLE_RERANK。
    是否开启真实 rerank，由 rerank_service 统一决定。

    好处：
    - Graph 节点保持稳定
    - rerank_service 负责开关、模型加载、降级
    - 后续开启 rerank 时，不需要改 Graph
    """

    fusion_results = state.get(
        "fusion_results",
        []
    )

    query = state.get(
        "query",
        ""
    )

    rerank_results = rerank_documents(
        query=query,
        documents=fusion_results,
        top_n=5
    )

    return {
        "rerank_results": rerank_results
    }
