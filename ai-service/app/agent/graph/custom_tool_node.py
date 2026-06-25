# app/agent/graph/custom_tool_node.py

import json

from langgraph.prebuilt import ToolNode

from langchain_core.messages import ToolMessage


def merge_sources(
    old_sources,
    new_sources,
):
    old_sources = old_sources or []
    new_sources = new_sources or []

    merged = []
    seen = set()

    for item in old_sources + new_sources:

        key = json.dumps(
            item,
            ensure_ascii=False,
            sort_keys=True,
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        merged.append(
            item
        )

    return merged


class CustomToolNode(ToolNode):
    """
    职责：
    1. 执行官方 ToolNode
    2. 解析 Tool 返回结果
    3. 把 RAG Tool 返回的 JSON 拆成：
        - ToolMessage.content = context
        - State.sources = sources
    4. 同时兼容 invoke / ainvoke
    5. 如果是 MCP Tool 普通字符串，则原样交给 LLM
    """

    def _process_result(
        self,
        state,
        result,
    ):
        print("===== custom tool node process result =====")
        print(result)

        old_sources = state.get(
            "sources",
            []
        )

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

                if isinstance(
                    content,
                    str,
                ):

                    data = json.loads(
                        content
                    )

                else:

                    data = content

            except Exception:

                # MCP 普通字符串结果会走这里
                processed_messages.append(
                    message
                )

                continue

            if not isinstance(
                data,
                dict,
            ):

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

        merged_sources = merge_sources(
            old_sources,
            new_sources,
        )

        print("===== custom tool node current turn sources =====")
        print(merged_sources)

        return {
            "messages": processed_messages,
            "sources": merged_sources,
        }

    def invoke(
        self,
        state,
        config=None,
    ):
        print("===== custom tool node invoke =====")

        result = super().invoke(
            state,
            config,
        )

        return self._process_result(
            state,
            result,
        )

    async def ainvoke(
        self,
        state,
        config=None,
    ):
        print("===== custom tool node ainvoke =====")

        result = await super().ainvoke(
            state,
            config,
        )

        return self._process_result(
            state,
            result,
        )