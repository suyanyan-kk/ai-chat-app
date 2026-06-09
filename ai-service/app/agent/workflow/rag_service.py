from app.agent.workflow.rag_graph import (
    rag_graph
)
from langsmith import traceable

@traceable(name="rag_workflow")
def run_rag_graph(query):

    result = rag_graph.invoke({

        "query": query
    })
  
    return {

        "context":
            result["context"],

        "sources":
            result["sources"],

        "chunks":
            result["chunks"]
    }