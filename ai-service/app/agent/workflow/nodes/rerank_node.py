# app/agent/workflow/nodes/rerank_node.py

from app.rag.rerank.rerank_service import (
    rerank_documents
)


def rerank_node(state):

    rerank_results = rerank_documents(

        query=state["query"],

        documents=state["hybrid_results"],

        top_n=5
    )

    return {

        "rerank_results":
            rerank_results

    }