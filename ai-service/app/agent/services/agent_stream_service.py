from langchain_core.messages import (
    HumanMessage
)

from app.agent.graph.agent_graph import (
    graph
)


def agent_stream(
        query
):

    for event in graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ],
            "sources": []
        }
    ):

        print(event)

        yield event