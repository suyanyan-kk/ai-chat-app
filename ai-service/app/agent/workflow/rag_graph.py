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

from app.agent.workflow.nodes.hybrid_retrieval_node import (
    hybrid_retrieval_node
)

from app.agent.workflow.nodes.rerank_node import (
    rerank_node
)

from app.agent.workflow.nodes.parent_chunk_node import (
    parent_chunk_node
)

from app.agent.workflow.nodes.context_node import (
    context_node
)


builder = StateGraph(
    RAGState
)

builder.add_node(
    "query_analysis",
    query_analysis_node
)

builder.add_node(
    "hybrid_retrieval",
    hybrid_retrieval_node
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
    "answer_generation",
    context_node
)

builder.add_edge(
    START,
    "query_analysis"
)

builder.add_edge(
    "query_analysis",
    "hybrid_retrieval"
)

builder.add_edge(
    "hybrid_retrieval",
    "rerank"
)

builder.add_edge(
    "rerank",
    "parent_chunk"
)

builder.add_edge(
    "parent_chunk",
    "answer_generation"
)

builder.add_edge(
    "answer_generation",
    END
)

rag_graph = builder.compile()