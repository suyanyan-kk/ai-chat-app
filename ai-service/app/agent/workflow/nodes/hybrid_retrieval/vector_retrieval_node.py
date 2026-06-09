
# app/agent/workflow/nodes/hybrid_retrieval/vector_retrieval_node.py

from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service
)
from langsmith import traceable

@traceable(name="vector_retrieval")
def vector_retrieval_node(state):

    analysis = state["analysis"]

    all_results = []

    for q in analysis.multi_queries:

        results = (
            hybrid_retrieval_service.vector_search(
                query=q,
                top_k=20,
                metadata_filter=
                    analysis.metadata_filter
            )
        )

        all_results.extend(results)

    return {
        "vector_results": all_results
    }