"""
State Parser

负责解析：

LangGraph Node 执行状态

例如：

query_analysis
vector_retrieval
rerank
...

转换为统一 Business Event
"""


def parse_state_event(event: dict):
    """
    Raw Event
        ↓
    Business Event
    """

    event_name = event.get(
        "event",
        ""
    )
    
    # 目前先只解析 Node 开始
    if event_name == "on_chain_start":

        node_name = event.get(
            "name",
            ""
        )

        # LangGraph 自己忽略
        if node_name == "LangGraph":
            return None

        return {

            "type": "state",

            "status": "start",

            "node": node_name

        }

    # Node 完成
    if event_name == "on_chain_end":

        node_name = event.get(
            "name",
            ""
        )

        if node_name == "LangGraph":
            return None

        return {

            "type": "state",

            "status": "end",

            "node": node_name

        }

    return None