# app/agent/workflow/rag_state.py

from typing import TypedDict, List, Dict, Any
class RAGState(TypedDict):

    query: str

    analysis: Dict[str, Any]

    hybrid_results: List[Dict]

    rerank_results: List[Dict]

    final_results: List[Dict]

    context: str

    sources: List[Dict]

    chunks: List[Dict]
