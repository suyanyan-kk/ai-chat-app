# app/agent/workflow/nodes/parent_chunk_node.py

from app.rag.retrieval.retrieval_service import (
    get_parent_chunk
)
from langsmith import traceable

@traceable(name="parent_chunk")

def parent_chunk_node(state):

    final_results = []

    seen_parent_ids = set()

    for item in state["rerank_results"]:

        metadata = item["metadata"]

        chunk_type = metadata.get(
            "chunk_type"
        )

        if chunk_type == "child":

            parent_id = metadata.get(
                "parent_id"
            )

            if parent_id in seen_parent_ids:

                continue

            seen_parent_ids.add(
                parent_id
            )

            parent_chunk = get_parent_chunk(
                parent_id
            )

            if parent_chunk:

                final_results.append({

                    "content":
                        parent_chunk.content,

                    "metadata":
                        parent_chunk.meta_info,

                    "rerank_score":
                        item["rerank_score"]
                })

    return {

        "parent_results":
            final_results

    }