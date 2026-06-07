# app/agent/agents/rag_agent.py

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage
)
import json
from app.llm.model import model

from app.agent.tools.rag_tool import (
    search_knowledge
)

from app.agent.tools.time_tool import (
    get_current_time
)

from app.agent.tools.calculator_tool import (
    calculator
)
from app.agent.tools.weather_tool import (
    get_weather
)
# 加入 Tool Router Prompt
SYSTEM_PROMPT = """
你是一个智能助手。

你拥有以下工具：

1. search_knowledge
用于查询知识库内容

2. get_current_time
用于获取当前时间

3. calculator
用于数学计算

4. get_weather
用于获取天气信息

请优先使用工具。

不要编造结果。
"""
class RAGAgent:

    def __init__(self):
        self.tools = {

            "search_knowledge":
                search_knowledge,

            "get_current_time":
                get_current_time,

            "calculator":
                calculator,

            "get_weather":
                get_weather
        }

        self.llm_with_tools = (

            model.bind_tools(

                [
                    search_knowledge,
                    get_current_time,
                    calculator,
                    get_weather
                ]
            )
        )

    def invoke(
            self,
            query: str,
            history: str = None
    ):
        last_sources = []
        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT
            )
        ]
        if history:

            messages.append(
                HumanMessage(
                    content=f"""
                    历史对话:

                    {history}

                    当前问题:

                    {query}
                 """
                )
            )

        else:

            messages.append(
                HumanMessage(
                    content=query
                )
            )
        # =====================
        # 第一次 LLM
        # =====================

        ai_message = (

            self.llm_with_tools.invoke(
                messages
            )
        )

        # 不需要工具

        if not ai_message.tool_calls:

            return ai_message.content

        messages.append(
            ai_message
        )

        # =====================
        # Tool Calling
        # =====================

        for tool_call in ai_message.tool_calls:

            print(
                "\n========== TOOL CALL ==========\n"
            )

            print(
                tool_call["name"]
            )

            print(
                tool_call["args"]
            )

            tool_name = (
                tool_call["name"]
            )

            tool_args = (
                tool_call["args"]
            )

            tool = self.tools[
                tool_name
            ]

            tool_result = (
                tool.invoke(
                    tool_args
                )
            )
            if tool_name == "search_knowledge":

                try:

                    data = json.loads(
                        tool_result
                    )

                    self.last_sources = (
                        data["sources"]
                    )

                    tool_result = (
                        data["context"]
                    )
                except Exception:
                    pass
    
            messages.append(

                ToolMessage(

                    content=
                        tool_result,

                    tool_call_id=
                        tool_call["id"]
                )
            )

        # =====================
        # 第二次 LLM
        # =====================

        final_response = (

            self.llm_with_tools.invoke(
                messages
            )
        )

        return {

            "answer":
                final_response.content,

            "sources":
                self.last_sources
        }