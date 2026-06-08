# app/agent/workflow/nodes/hybrid_retrieval_node.py

from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service
)


def hybrid_retrieval_node(state):

    analysis = state["analysis"]

    all_results = []

    for q in analysis.multi_queries:

        results = (

            hybrid_retrieval_service.search(

                query=q,

                top_k=20,

                metadata_filter=analysis.metadata_filter
            )
        )

        all_results.extend(results)

    unique_results = {}

    for item in all_results:

        metadata = item["metadata"]

        doc_id = (

            metadata.get("file_id"),

            metadata.get("parent_id")
        )

        if doc_id not in unique_results:

            unique_results[doc_id] = item

    return {

        "hybrid_results":
            list(unique_results.values())

    }