# app/agent/workflow/rag_graph.py

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.agent.workflow.rag_state import (
    RAGState
)

from app.agent.workflow.nodes.query_analysis_node import (
    query_analysis_node
)

from app.agent.workflow.nodes.hybrid_retrieval.vector_retrieval_node import (
    vector_retrieval_node
)

from app.agent.workflow.nodes.hybrid_retrieval.bm25_retrieval_node import (
    bm25_retrieval_node
)

from app.agent.workflow.nodes.hybrid_retrieval.rrf_fusion_node import (
    rrf_fusion_node
)
from app.agent.workflow.nodes.rerank_node import (
    rerank_node
)

from app.agent.workflow.nodes.parent_chunk_node import (
    parent_chunk_node
)

from app.agent.workflow.nodes.context_node import (
    build_context_node
)


builder = StateGraph(
    RAGState
)

builder.add_node(
    "query_analysis",
    query_analysis_node
)

builder.add_node(
    "vector_retrieval",
    vector_retrieval_node
)

builder.add_node(
    "bm25_retrieval",
    bm25_retrieval_node
)

builder.add_node(
    "rrf_fusion",
    rrf_fusion_node
)

builder.add_node(
    "rerank",
    rerank_node
)


builder.add_node(
    "parent_chunk",
    parent_chunk_node
)

builder.add_node(
    "build_context",
    build_context_node
)

builder.add_edge(
    START,
    "query_analysis"
)

builder.add_edge(
    "query_analysis",
    "vector_retrieval"
)

builder.add_edge(
    "vector_retrieval",
    "bm25_retrieval"
)

builder.add_edge(
    "bm25_retrieval",
    "rrf_fusion"
)

builder.add_edge(
    "rrf_fusion",
    "rerank"
)

builder.add_edge(
    "rerank",
    "parent_chunk"
)

builder.add_edge(
    "parent_chunk",
    "build_context"
)

builder.add_edge(
    "build_context",
    END
)

rag_graph = builder.compile()


# query_analysis
# ↓
# vector_retrieval
# ↓
# bm25_retrieval
# ↓
# rrf_fusion
# ↓
# rerank
# ↓
# parent_chunk
# ↓
# build_context