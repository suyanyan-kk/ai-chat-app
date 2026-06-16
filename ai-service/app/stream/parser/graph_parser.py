# app/stream/parser/graph_parser.py

import json


def parse_graph_event(event: dict) -> str | None:
    """
    解析 LangGraph 生命周期事件。

    这里只处理 Graph 自身的开始和结束事件，
    不处理 Token、Tool、RAG 等其他类型事件。

    参数：
        event: graph.astream_events() 返回的单个事件

    返回：
        如果是 Graph 生命周期事件，返回前端可直接消费的 JSON 字符串；
        否则返回 None。
    """

    event_name = event.get("event")

    # Graph 开始
    if event_name == "on_chain_start":
        print("===== graph start parser=====")
        return {
                "type": "graph_start"
            }
    
    if event_name == "on_chain_stream":

        chunk = event.get(
            "data",
            {}
        ).get(
            "chunk",
            {}
        )
        print("===== graph stream parser=====")
        print(event)
        print(chunk.get("sources",[]))
        print(chunk.get("messages",[]))
        return {

            "type": "graph_state",

            "messages":
                chunk.get(
                    "messages",
                    []
                ),

            "sources":
                chunk.get(
                    "sources",
                    []
                )

            }
    
    # Graph 结束
    if event_name == "on_chain_end":
        print("===== graph end parser=====")
        print(event)
        return {

            "type": "graph_end"

        }

    return None