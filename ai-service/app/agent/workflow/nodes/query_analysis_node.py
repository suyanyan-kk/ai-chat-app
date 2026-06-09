# app/agent/workflow/nodes/query_analysis_node.py

from app.rag.query.query_analysis_service import (
    analyze_query
)
from app.agent.workflow.rag_state import (
    RAGState
)
from app.knowledgedb.db import SessionLocal
from langsmith import traceable

@traceable(name="query_analysis")
def query_analysis_node(state: RAGState):
    db = SessionLocal()
    try:
        analysis = analyze_query(
            db,
            state["query"]
        )

        return {
            "analysis": analysis
        }
    finally:

        db.close()
    