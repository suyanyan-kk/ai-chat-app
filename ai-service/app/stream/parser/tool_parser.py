
import json
"""
Tool Event Parser

负责解析 Tool Event

只负责：
LangGraph Event
↓

统一 Tool Event
"""


def parse_tool_event(event: dict):

    event_name = event.get(
        "event",
        ""
    )

    # ==========================
    # Tool Start
    # ==========================
    if event_name == "on_tool_start":
        print("===== tool start parser=====")
        print(event_name)
        return {

            "type": "tool_start",

            "tool_name": event.get(
                "name",
                ""
            )
        }
    # ==========================
    # Tool End
    # ==========================
    if event_name == "on_tool_end":
        print("===== tool end parser=====")
        print(event.get("data",{}))
        return {

            "type": "tool_end",

            "tool_name": event.get(
                "name",
                ""
            ),
            "run_id":event.get(
                "run_id"
            ),
            # 以后这里会继续扩展
            "output": event.get(
                "data",
                {}
            )
        }

    return None