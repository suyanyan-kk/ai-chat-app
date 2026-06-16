# app/stream/router/event_router.py

from app.stream.parser.graph_parser import (
    parse_graph_event
)

from app.stream.parser.chat_parser import (
    parse_chat_event
)
from app.stream.parser.tool_parser import (
    parse_tool_event
)
from app.stream.parser.state_parser import (
    parse_state_event
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
    print("\n==== Event Router start 开始判断走哪个parser ======")
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

        return parse_tool_event(
            event
        )

    return None

