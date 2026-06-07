# app/agent/graph/custom_tool_node.py

from langgraph.prebuilt import ToolNode

import json
import traceback


class CustomToolNode(ToolNode):

    def invoke(
        self,
        state,
        config=None
    ):

        print("===== tool node start =====")

        try:

            result = super().invoke(
                state,
                config
            )

            print("===== tool result =====")
            print(result)

            sources = []

            for message in result["messages"]:

                # Tool返回内容
                content = message.content

                # =========================
                # 尝试解析 JSON
                # =========================
                try:

                    data = json.loads(content)

                    # -------------------------
                    # context
                    # -------------------------
                    if isinstance(data, dict):

                        if "context" in data:

                            message.content = (
                                data["context"]
                            )

                        # -------------------------
                        # sources
                        # -------------------------
                        if "sources" in data:

                            sources.extend(
                                data["sources"]
                            )

                except json.JSONDecodeError:

                    # 普通字符串Tool
                    # 例如天气、时间、计算器
                    pass

            print("===== tool node end =====")

            return {

                "messages":
                    result["messages"],

                "sources":
                    sources

            }

        except Exception as e:

            print("===== tool exception =====")
            print(e)

            traceback.print_exc()

            raise