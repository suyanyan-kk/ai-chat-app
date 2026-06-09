
# 第二版agent_service.py，改成调用agent_graph.py
from langchain_core.messages import (
    HumanMessage
)

from app.agent.graph.agent_graph import (
    graph
)
 

def agent_chat(
        query,
        session_id
):
    print("===== agent start =====")
    result = graph.invoke(

    {
        "messages": [
            HumanMessage(
                content=query
            )
        ],
        "sources": []
    },

    config={
        "configurable": {
            "thread_id": session_id
        }
    }
)

    print("===== graph result =====")
    print(result)
    return {

        "answer":
            result["messages"][-1].content,

        "sources":
            result.get(
                "sources",
                []
            )
}
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