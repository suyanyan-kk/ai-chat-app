# app/agent/workflow/nodes/query_analysis_node.py

from app.rag.query.query_analysis_service import (
    analyze_query
)
from app.agent.workflow.rag_state import (
    RAGState
)
def query_analysis_node(state: RAGState):

    analysis = analyze_query(
        db,
        state["query"]
    )

    return {
        "analysis": analysis
    }
    