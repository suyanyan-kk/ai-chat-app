import json

from app.core.logger import logger
from app.core.exception import AppException

from app.agent.agent_service import (
    agent_chat_event_stream
)
from app.stream.router.event_router import (
    route_event
)
async def stream_chat(
    session_id: str,
    user_input: str
):
    async for event in agent_chat_event_stream(
                                    user_input,
                                    session_id
                    ):

        print("\n===== chat event =====")
        print(event)

    response = route_event(event)

    if response:

        yield response
    # logger.info(
    #     f"[聊天请求] session={session_id}, message={user_input}"
    # )

    # if not user_input:
    #     raise AppException("消息不能为空")
    # async for event in agent_chat_event_stream(
    #         user_input,
    #         session_id
    #     ):

    #         print("\n===== chat event =====")
    #         print(event)
    #         parsed = parse_event(event)

    #         if parsed is None:
    #             continue

    #         print(parsed)
    #         yield (
    #         json.dumps(
    #             event,
    #             ensure_ascii=False
    #         )
    #         + "\n"
    #     )
    # try:

    #     # =========================
    #     # start
    #     # =========================
    #     yield json.dumps(
    #         {
    #             "type": "start",
    #             "data": {}
    #         },
    #         ensure_ascii=False
    #     ) + "\n"

    #     final_answer = ""

    #     sources = []

    #     # =========================
    #     # graph stream
    #     # =========================
    #     async for event in agent_chat_event_stream(
    #         user_input,
    #         session_id
    #     ):

    #         print("\n===== chat event =====")
    #         print(event)

    #         # =====================================
    #         # Agent Node
    #         # =====================================
    #         if "agent" in event:

    #             node_data = event["agent"]

    #             # sources
    #             if "sources" in node_data:

    #                 sources = node_data.get(
    #                     "sources",
    #                     sources
    #                 )

    #             # messages
    #             messages = node_data.get(
    #                 "messages",
    #                 []
    #             )

    #             if messages:

    #                 last_message = messages[-1]

    #                 if hasattr(
    #                     last_message,
    #                     "content"
    #                 ):

    #                     final_answer = (
    #                         last_message.content
    #                     )

    #                     yield json.dumps(
    #                         {
    #                             "type": "stream",
    #                             "data": {
    #                                 "context":
    #                                     final_answer,
    #                                 "sources":
    #                                     sources
    #                             }
    #                         },
    #                         ensure_ascii=False
    #                     ) + "\n"

    #         # =====================================
    #         # Tool Node
    #         # =====================================
    #         if "tools" in event:

    #             tool_data = event["tools"]

    #             # 关键：
    #             # 保留知识库引用来源
    #             sources = tool_data.get(
    #                 "sources",
    #                 sources
    #             )

    #             yield json.dumps(
    #                 {
    #                     "type": "tool",
    #                     "data": {
    #                         "sources": sources
    #                     }
    #                 },
    #                 ensure_ascii=False
    #             ) + "\n"

    #     # =========================
    #     # end
    #     # =========================
    #     yield json.dumps(
    #         {
    #             "type": "end",
    #             "data": {
    #                 "context": final_answer,
    #                 "sources": sources
    #             }
    #         },
    #         ensure_ascii=False
    #     ) + "\n"

    # except Exception as e:

    #     logger.error(
    #         f"[LLM错误] {str(e)}"
    #     )

    #     yield json.dumps(
    #         {
    #             "type": "error",
    #             "data": {
    #                 "message": str(e)
    #             }
    #         },
    #         ensure_ascii=False
    #     ) + "\n"

    #     raise
