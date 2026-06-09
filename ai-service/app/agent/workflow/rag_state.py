# app/agent/workflow/rag_state.py

from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage
class RAGState(TypedDict):
    messages: list[BaseMessage]
    # 用户问题
    query: str

    # QueryAnalysis对象
    analysis: Any

    # Vector Recall
    vector_results: List[Dict]

    # BM25 Recall
    bm25_results: List[Dict]

    # RRF Fusion
    fusion_results: List[Dict]

    # Rerank
    rerank_results: List[Dict]

    # Parent Chunk Expand
    parent_results: List[Dict]

    # Final Context
    context: str

    # Sources
    sources: List[Dict]

    # Final Chunks
    chunks: List[Dict]