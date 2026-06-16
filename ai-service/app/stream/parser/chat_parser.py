# app/stream/parser/chat_parser.py

import json


def parse_chat_event(
    event: dict
):
    """
    ChatModel Event Parser

    LangGraph
            ↓
    Frontend Event

    负责解析：

    on_chat_model_start

    on_chat_model_stream

    on_chat_model_end
    """

    event_name = event.get(
        "event"
    )

    data = event.get(
        "data",
        {}
    )
    print("======chat parser ==========")
    print(event_name)
    print(data)
    # =========================
    # LLM Start
    # =========================
    if event_name == "on_chat_model_start":

        return {

                "type": "llm_start"

            }

    # =========================
    # Token
    # =========================
    elif event_name == "on_chat_model_stream":

        chunk = data.get(
            "chunk"
        )

        if chunk is None:

            return None

        token = getattr(
            chunk,
            "content",
            ""
        )

        if token == "":

            return None
        print("======chat parser stream ==========")
        print(event_name)
        print(token)
        return {

                "type": "token",

                "content": token

            }

    # =========================
    # LLM End
    # =========================
    elif event_name == "on_chat_model_end":

        return {

                "type": "llm_end"

            }

    return None

# def parse_chat_event(event: dict):
#     """
#     ChatModel Event Parser

#     专门负责解析：

#     on_chat_model_start
#     on_chat_model_stream
#     on_chat_model_end

#     返回：
#         None
#         或
#         json字符串
#     """

#     event_name = event.get("event")

#     data = event.get("data", {})

#     # ==========================
#     # ChatModel Start
#     # ==========================
#     if event_name == "on_chat_model_start":

#         print("===== chat model start =====")
#         print(event)

#         return json.dumps(

#             {
#                 "type": "llm_start"
#             },

#             ensure_ascii=False

#         ) + "\n"

#     # ==========================
#     # Token Streaming
#     # ==========================
#     if event_name == "on_chat_model_stream":
#         print("===== chat model stream =====")
#         print(event)

#         chunk = data.get("chunk")

#         print("===== chunk =====")
#         print(chunk)

#         if chunk is None:

#             return None

#         token = chunk.content

#         if not token:

#             return None

#         return json.dumps(

#             {

#                 "type": "token",

#                 "content": token

#             },

#             ensure_ascii=False

#         ) + "\n"

#     # ==========================
#     # ChatModel End
#     # ==========================
#     if event_name == "on_chat_model_end":

#         print("===== chat model end =====")
#         print(event)

#         return json.dumps(

#             {

#                 "type": "llm_end"

#             },

#             ensure_ascii=False

#         ) + "\n"

#     return None

# 返回的结构
# {
#     "event":"on_chat_model_stream",

#     "data":{

#         "chunk":

#             AIMessageChunk(

#                 content="你"

#             )

#     }

# }