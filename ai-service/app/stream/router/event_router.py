# app/stream/router/event_router.py

from app.stream.parser.graph_parser import (
    parse_graph_event
)

from app.stream.parser.chat_parser import (
    parse_chat_event
)


def route_event(event):
    """
    Event Router

    负责根据 Event 类型
    分发给不同 Parser

    自己不解析数据
    """

    event_name = event.get(
        "event",
        ""
    )
    print("\n==== Event Router======")
    print(event_name)
    # ==========================
    # Graph
    # ==========================
    if event_name.startswith(
        "on_chain"
    ):

        return parse_graph_event(
            event
        )

    # ==========================
    # Chat Model
    # ==========================
    if event_name.startswith(
        "on_chat_model"
    ):

        return parse_chat_event(
            event
        )

    # ==========================
    # Tool
    # ==========================
    if event_name.startswith(
        "on_tool"
    ):

        return None

    return None


# 先不要处理 Token。
# 先只处理 Graph 生命周期。
# def route_event(event):
#     """
#     LangGraph Event
#             ↓
#     Frontend JSON
#     """

#     event_name = event.get("event")

#     # =========================
#     # Graph Start
#     # =========================
#     if event_name == "on_chain_start":

#         return json.dumps({

#             "type": "graph_start"

#         }, ensure_ascii=False) + "\n"

#     # =========================
#     # Graph End
#     # =========================
#     if event_name == "on_chain_end":

#         return json.dumps({

#             "type": "graph_end"

#         }, ensure_ascii=False) + "\n"

#     return None