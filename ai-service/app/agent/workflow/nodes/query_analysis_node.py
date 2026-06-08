# app/agent/workflow/nodes/query_analysis_node.py

from app.knowledgedb.db import (
    SessionLocal
)

from app.rag.query.query_analysis_service import (
    analyze_query
)


def query_analysis_node(state):

    query = state["query"]

    db = SessionLocal()

    analysis = analyze_query(
        db,
        query
    )

    db.close()

    return {

        "analysis": analysis

    }