# app/agent/workflow/nodes/hybrid_retrieval/bm25_retrieval_node.py

from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service
)
from langsmith import traceable
@traceable(name="bm25_retrieval")

def bm25_retrieval_node(state):

    analysis = state["analysis"]

    all_results = []

    for q in analysis.multi_queries:

        results = (
            hybrid_retrieval_service.bm25_search(
                query=q,
                top_k=20,
                metadata_filter=
                    analysis.metadata_filter
            )
        )

        all_results.extend(results)

    return {
        "bm25_results": all_results
    }