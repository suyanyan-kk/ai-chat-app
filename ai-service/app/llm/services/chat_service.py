# app/chat/chat_service.py

import json

from app.core.logger import logger
from app.core.exception import AppException

from app.agent.agent_service import (
    agent_chat_stream,
)

from app.stream.router.graph_stream_router import (
    route_graph_stream,
)


async def stream_chat(
    session_id: str,
    user_input: str,
):
    """
    Agent Streaming

    企业级双通道：

    messages:
        token streaming

    updates:
        sources streaming
    """

    logger.info(
        f"[聊天请求] session={session_id}, message={user_input}"
    )

    if not user_input:

        raise AppException(
            "消息不能为空"
        )

    current_answer = ""

    current_sources = []

    last_sources = []

    try:

        # ==========================
        # Start
        # ==========================

        yield json.dumps(

            {
                "type": "start",

                "data": {}
            },

            ensure_ascii=False

        ) + "\n"

        async for stream_item in agent_chat_stream(

            user_input,

            session_id

        ):
            # print("=====graph.astream item=========")
            # print(stream_item)
            event = route_graph_stream(
                stream_item
            )

            if event is None:

                continue

            event_type = event["type"]

            # ==========================
            # Sources
            # ==========================

            if event_type == "sources":

                sources = event.get(
                    "sources",
                    []
                )

                if sources != last_sources:

                    current_sources = sources

                    last_sources = sources.copy()
                    print('========current_sources====')
                    print(current_sources)

                    yield json.dumps(

                        {
                            "type": "sources",

                            "data": {
                                "sources": current_sources
                            }
                        },

                        ensure_ascii=False

                    ) + "\n"

            # ==========================
            # Token
            # ==========================

            elif event_type == "token":

                token = event.get(
                    "content",
                    ""
                )

                if not token:

                    continue

                current_answer += token
                # print('========token====')
                # print(token)
                yield json.dumps(

                    {
                        "type": "stream",

                        "data": {
                            "answer": token
                        }
                    },

                    ensure_ascii=False

                ) + "\n"

        # ==========================
        # End
        # ==========================
        print("=======End=======")
        print(current_answer)
        print(current_sources)

        yield json.dumps(
            {
                "type": "end",

                "data": {

                    "answer": current_answer,

                    "sources": current_sources

                }
            },

            ensure_ascii=False

        ) + "\n"

    except Exception as e:

        logger.exception(e)

        raise AppException(
            "聊天过程中发生错误"
        )

# import json

# from app.core.logger import logger
# from app.core.exception import AppException

# from app.agent.agent_service import (
#     agent_chat_event_stream
# )

# from app.stream.router.event_router import (
#     route_event
# )


# async def stream_chat(
#     session_id: str,
#     user_input: str
# ):
#     """
#     Agent Streaming

#     整个 Streaming 生命周期：

#     graph_start
#             ↓
#     tool_start
#             ↓
#     tool_end
#             ↓
#     graph_state（sources）
#             ↓
#     token
#             ↓
#     token
#             ↓
#     token
#             ↓
#     graph_end
#     """

#     logger.info(
#         f"[聊天请求] session={session_id}, message={user_input}"
#     )

#     if not user_input:
#         raise AppException("消息不能为空")

#     # ===================================
#     # 整个回答
#     # ===================================

#     current_answer = ""

#     # ===================================
#     # 当前 Sources
#     # ===================================

#     current_sources = []

#     # ===================================
#     # 上一次 Sources
#     #
#     # 防止重复发送
#     # ===================================

#     last_sources = []

#     try:

#         async for raw_event in agent_chat_event_stream(

#             user_input,

#             session_id

#         ):

#             print("\n===== chat_server  =====")

#             # ==========================
#             # LangGraph Event
#             #
#             # ↓
#             #
#             # Business Event
#             # ==========================

#             event = route_event(
#                 raw_event
#             )

#             if event is None:

#                 continue



#             event_type = event["type"]
#             print("\n===== 走完event router parser后返回的 eventName=====")
#             print(event_type)
#             # ===================================
#             # Graph Start
#             # ===================================

#             if event_type == "graph_start":

#                 yield json.dumps(

#                     {
#                         "type": "start",

#                         "data": {}
#                     },

#                     ensure_ascii=False

#                 ) + "\n"

#             # ===================================
#             # Tool Start
#             # ===================================

#             elif event_type == "tool_start":

#                 yield json.dumps(

#                     {
#                         "type": "tool_start",

#                         "data": {

#                             "tool":

#                                 event["tool_name"]

#                         }

#                     },

#                     ensure_ascii=False

#                 ) + "\n"

#             # ===================================
#             # Tool End
#             # ===================================

#             elif event_type == "tool_end":

#                 yield json.dumps(

#                     {
#                         "type": "tool_end",

#                         "data": {

#                             "tool":

#                                 event["tool_name"]

#                         }

#                     },

#                     ensure_ascii=False

#                 ) + "\n"

#             # ===================================
#             # Graph State
#             #
#             # Sources 更新
#             # ===================================

#             elif event_type == "graph_state":

#                 sources = event.get(

#                     "sources",

#                     []

#                 )
#                 print("=======graph_state sources=========")
#                 print(sources)
#                 if sources != last_sources:

#                     current_sources = sources

#                     last_sources = sources.copy()

#                     yield json.dumps(

#                         {

#                             "type": "sources",

#                             "data": {

#                                 "sources":

#                                     current_sources

#                             }

#                         },

#                         ensure_ascii=False

#                     ) + "\n"

#             # ===================================
#             # Token Streaming
#             # ===================================

#             elif event_type == "token":

#                 token = event.get(

#                     "content",

#                     ""

#                 )

#                 current_answer += token

#                 yield json.dumps(

#                     {

#                         "type": "stream",

#                         "data": {

#                             "answer":

#                                 token

#                         }

#                     },

#                     ensure_ascii=False

#                 ) + "\n"

#             # ===================================
#             # Graph End
#             # ===================================

#             elif event_type == "graph_end":

#                 yield json.dumps(

#                     {

#                         "type": "end",

#                         "data": {

#                             "answer":

#                                 current_answer,

#                             "sources":

#                                 current_sources

#                         }

#                     },

#                     ensure_ascii=False

#                 ) + "\n"
#             print("\n===== chat_server end  =====")

#     except Exception as e:

#         logger.exception(e)

#         raise AppException("聊天过程中发生错误")