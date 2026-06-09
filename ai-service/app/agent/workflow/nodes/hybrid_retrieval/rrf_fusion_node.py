
# app/agent/workflow/nodes/hybrid_retrieval/rrf_fusion_node.py

from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service
)
from langsmith import traceable

@traceable(name="rrf_fusion")
def rrf_fusion_node(state):

    vector_results = state["vector_results"]

    bm25_results = state["bm25_results"]

    fusion_results = (
        hybrid_retrieval_service
        .reciprocal_rank_fusion(
            vector_results,
            bm25_results
        )
    )

    return {
        "fusion_results": fusion_results
    }