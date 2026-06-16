from langchain_core.messages import HumanMessage

from app.agent.graph.agent_graph import graph


async def agent_chat_stream(
    query: str,
    session_id: str
):
    print("===== agent graph stream start =====")

    async for item in graph.astream(

        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ],
            "sources": [],
            "metadata": {}
        },

        config={
            "configurable": {
                "thread_id": session_id
            }
        },

        stream_mode=[
            "messages",
            "updates"
        ]
    ):

        # print("===== graph stream item =====")
        # print(item)

        yield item