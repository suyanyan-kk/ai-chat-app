# app/agent/workflow/rag_state.py

from typing import TypedDict


class RAGState(TypedDict):

    query: str

    analysis: object

    hybrid_results: list

    rerank_results: list

    final_results: list

    context: str

    sources: list

    chunks: list