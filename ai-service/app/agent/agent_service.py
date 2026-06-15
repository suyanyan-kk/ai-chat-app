
# 第二版agent_service.py，改成调用agent_graph.py
from langchain_core.messages import (
    HumanMessage
)

from app.agent.graph.agent_graph import (
    graph
)
 
# 第四版agent_chat_event_stream，改成async generator，供chat_service调用
async def agent_chat_event_stream(
    query: str,
    session_id: str
):
    """
    LangGraph Event Streaming

    返回 LangGraph 官方 Event
    """

    print("===== agent event stream start =====")

    async for event in graph.astream_events(

        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ],

            # 保留 sources
            "sources": []
        },

        config={
            "configurable": {
                "thread_id": session_id
            }
        },

        version="v2"

    ):
        event_type = event["event"]

        # print("\n==========")
        # print(event_type)

        yield event


# 第三版 graph.stream改成 graph.invoke_stream，返回最终结果，供chat_service调用
# def agent_chat_stream(
#     query,
#     session_id
# ):

#     print("===== agent stream start =====")

#     for event in graph.stream(

#         {
#             "messages": [
#                 HumanMessage(
#                     content=query
#                 )
#             ],
#             "sources": []
#         },

#         config={
#             "configurable": {
#                 "thread_id": session_id
#             }
#         },

#         stream_mode="updates"
#     ):

#         print("\n===== graph event =====")

#         print(event)

#         yield event


# 第二版agent_chat，改成调用graph.invoke
# def agent_chat(
#         query,
#         session_id
# ):
#     print("===== agent start =====")
#     result = graph.invoke(

#     {
#         "messages": [
#             HumanMessage(
#                 content=query
#             )
#         ],
#         "sources": []
#     },

#     config={
#         "configurable": {
#             "thread_id": session_id
#         }
#     }
# )

#     print("===== graph result =====")
#     print(result)
#     return {

#         "answer":
#             result["messages"][-1].content,

#         "sources":
#             result.get(
#                 "sources",
#                 []
#             )
# }
# 第一版agent_excutor.py，后续会改成agent_graph.py
# import json
 
# from app.agent.agents.agent_executor import (
#     agent_executor
# )


# def agent_chat(
#         query,
#         history=""
# ):

#     result = agent_executor.invoke(
#         {
#             "input": query
#         }
#     )

#     sources = []

#     for action, observation in result.get(
#         "intermediate_steps",
#         []
#     ):
#         print(f"Action: {action}, Observation: {observation}")
#         if action.tool == "search_knowledge":

#             try:

#                 data = json.loads(
#                     observation
#                 )

#                 sources.extend(
#                     data["sources"]
#                 )

#             except Exception:
#                 pass

#     return {

#         "answer":
#             result["output"],

#         "sources":
#             sources
#     }