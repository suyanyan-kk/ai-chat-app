# app/agent/graph/custom_tool_node.py

import json

from langgraph.prebuilt import ToolNode

from langchain_core.messages import ToolMessage


class CustomToolNode(ToolNode):
    """
    企业级 Tool Runtime Node。

    职责：
    1. 执行官方 ToolNode
    2. 解析 Tool 返回结果
    3. 把 RAG Tool 返回的 JSON 拆成：
        - ToolMessage.content = context
        - State.sources = sources
    4. 同时兼容 invoke / ainvoke
    """

    def _process_result(
        self,
        result,
    ):
        print("===== custom tool node process result =====")
        print(result)

        messages = result.get(
            "messages",
            []
        )

        processed_messages = []
        new_sources = []

        for message in messages:

            if not isinstance(
                message,
                ToolMessage,
            ):
                processed_messages.append(
                    message
                )
                continue

            content = message.content

            try:
                if isinstance(content, str):
                    data = json.loads(content)
                else:
                    data = content
            except Exception:
                processed_messages.append(
                    message
                )
                continue

            if not isinstance(data, dict):
                processed_messages.append(
                    message
                )
                continue

            context = data.get(
                "context"
            )

            sources = data.get(
                "sources",
                []
            )

            if sources:
                new_sources.extend(
                    sources
                )

            if context:
                new_message = ToolMessage(
                    content=context,
                    tool_call_id=message.tool_call_id,
                    name=message.name,
                    id=message.id,
                    artifact=data,
                )

                processed_messages.append(
                    new_message
                )
            else:
                processed_messages.append(
                    message
                )

        print("===== custom tool node sources =====")
        print(new_sources)

        return {
            "messages": processed_messages,
            "sources": new_sources,
        }

    def invoke(
        self,
        state,
        config=None,
    ):
        print("===== custom tool node invoke =====")

        result = super().invoke(
            state,
            config
        )

        return self._process_result(
            result
        )

    async def ainvoke(
        self,
        state,
        config=None,
    ):
        print("===== custom tool node ainvoke =====")

        result = await super().ainvoke(
            state,
            config
        )

        return self._process_result(
            result
        )


# # app/agent/graph/custom_tool_node.py

# from langgraph.prebuilt import ToolNode

# import json
# import traceback

# class CustomToolNode(ToolNode):

#     def invoke(
#         self,
#         state,
#         config=None
#     ):

#         print("===== tool node start =====")

#         result = super().invoke(
#             state,
#             config
#         )
#         print("===== tool result =====")
#         print(result)

#         old_sources = state.get(
#             "sources",
#             []
#         )

#         new_sources = []

#         for message in result["messages"]:
#              # Tool返回内容
#             content = message.content

#             # =========================
#             # 尝试解析 JSON
#             # =========================
#             try:

#                 data = json.loads(content)

#                 # -------------------------
#                 # context
#                 # -------------------------
#                 if isinstance(data, dict):    
#                     if "context" in data:

#                         message.content = data["context"]

                
#                     # -------------------------
#                     # sources
#                     # -------------------------
#                     if "sources" in data:

#                         new_sources.extend(
#                             data["sources"]
#                         )

#             except json.JSONDecodeError:

#                 pass

#         # =========================
#         # 去重
#         # =========================

#         merged_sources = []

#         seen = set()

#         for item in old_sources + new_sources:

#             key = json.dumps(
#                 item,
#                 ensure_ascii=False,
#                 sort_keys=True
#             )

#             if key in seen:
#                 continue

#             seen.add(key)

#             merged_sources.append(item)
        
#         print("===== tool node end =====")
#         print("========== merged_sources ==========")
#         print(merged_sources)
#         return {

#             "messages": result["messages"],

#             "sources": merged_sources

#         }
    



# class CustomToolNode(ToolNode):

#     def invoke(
#         self,
#         state,
#         config=None
#     ):

#         print("===== tool node start =====")

#         try:

#             result = super().invoke(
#                 state,
#                 config
#             )

#             print("===== tool result =====")
#             print(result)

#             sources = []

#             for message in result["messages"]:

#                 # Tool返回内容
#                 content = message.content

#                 # =========================
#                 # 尝试解析 JSON
#                 # =========================
#                 try:

#                     data = json.loads(content)

#                     # -------------------------
#                     # context
#                     # -------------------------
#                     if isinstance(data, dict):

#                         if "context" in data:

#                             message.content = (
#                                 data["context"]
#                             )

#                         # -------------------------
#                         # sources
#                         # -------------------------
#                         if "sources" in data:

#                             sources.extend(
#                                 data["sources"]
#                             )

#                 except json.JSONDecodeError:

#                     # 普通字符串Tool
#                     # 例如天气、时间、计算器
#                     pass

#             print("===== tool node end =====")

#             return {

#                 "messages":
#                     result["messages"],

#                 "sources":
#                     sources

#             }

#         except Exception as e:

#             print("===== tool exception =====")
#             print(e)

#             traceback.print_exc()

#             raise