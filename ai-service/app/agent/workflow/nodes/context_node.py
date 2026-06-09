# app/agent/workflow/nodes/context_node.py

from collections import OrderedDict

from langsmith import traceable

@traceable(name="build_context")
def build_context_node(state):

    dedup_results = list(

        OrderedDict(

            (
                item["content"],
                item
            )

            for item in state["parent_results"]

        ).values()
    )

    context_list = []

    sources = []

    seen_sources = set()

    for item in dedup_results:

        metadata = item["metadata"]

        context_list.append(

            item["content"]
        )

        source_key = (

            metadata.get(
                "file_id"
            ),
        )

        if source_key not in seen_sources:

            seen_sources.add(
                source_key
            )

            sources.append({

                "file_id":
                    metadata.get(
                        "file_id"
                    ),

                "file_name":
                    metadata.get(
                        "file_name"
                    ),

                "file_type":
                    metadata.get(
                        "file_type"
                    ),

                "page":
                    metadata.get(
                        "page"
                    )
            })

    context = "\n\n".join(
        context_list
    )

    return {

        "context":
            context,

        "sources":
            sources,

        "chunks":
            dedup_results
    }