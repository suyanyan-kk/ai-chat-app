# app/agent/graph/agent_node.py

from uuid import uuid4

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
)

from app.llm.model import model

from app.agent.graph.message_builder import (
    build_messages,
)

from app.agent.tools.rag_tool import (
    search_knowledge,
)

from app.agent.tools.weather_tool import (
    get_weather,
)

from app.agent.tools.time_tool import (
    get_current_time,
)

from app.agent.tools.calculator_tool import (
    calculator,
)

from app.agent.mcp.tools import (
    load_mcp_tools_sync,
)

from app.agent.mcp.router import (
    route_mcp_tool_call,
)


# ==========================
# RAG Tools
# ==========================

rag_tools = [

    search_knowledge,

]


# ==========================
# Local Tools
# ==========================

local_tools = [

    get_weather,

    get_current_time,

    calculator,

]


# ==========================
# MCP Tools
# ==========================

try:

    mcp_tools = load_mcp_tools_sync()

except Exception as e:

    print("===== MCP tools load failed =====")
    print(e)

    mcp_tools = []


# ==========================
# All Tools
# ==========================

tools = [
    *rag_tools,
    *local_tools,
    *mcp_tools,
]


llm_tools = [
    *local_tools,
    *mcp_tools,
]


available_tool_names = {
    tool.name
    for tool in tools
}


print("===== Agent available tools =====")
print(
    sorted(
        available_tool_names
    )
)


llm_with_tools = model.bind_tools(
    llm_tools
)


# ==========================
# Message Helpers
# ==========================

def get_latest_user_message(
    messages,
):

    for message in reversed(
        messages
    ):

        if isinstance(
            message,
            HumanMessage,
        ):

            return message

    return None


def get_latest_user_index(
    messages,
):

    for index in range(
        len(messages) - 1,
        -1,
        -1,
    ):

        if isinstance(
            messages[index],
            HumanMessage,
        ):

            return index

    return -1


def has_any_tool_after_latest_user(
    messages,
):
    latest_user_index = get_latest_user_index(
        messages
    )

    if latest_user_index == -1:

        return False

    for message in messages[
        latest_user_index + 1:
    ]:

        if isinstance(
            message,
            ToolMessage,
        ):

            return True

    return False


def has_tool_after_latest_user(
    messages,
    tool_name: str,
):
    latest_user_index = get_latest_user_index(
        messages
    )

    if latest_user_index == -1:

        return False

    for message in messages[
        latest_user_index + 1:
    ]:

        if isinstance(
            message,
            ToolMessage,
        ) and message.name == tool_name:

            return True

    return False


def build_tool_call_message(
    tool_route: dict,
):

    tool_name = tool_route["name"]

    tool_args = tool_route.get(
        "args",
        {},
    )

    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": tool_name,
                "args": tool_args,
                "id": f"tool_call_{uuid4().hex}",
                "type": "tool_call",
            }
        ],
    )


def get_mcp_tool_route(
    state,
):
    messages = state.get(
        "messages",
        []
    )

    latest_user_message = get_latest_user_message(
        messages
    )

    if latest_user_message is None:

        return None

    user_input = latest_user_message.content

    tool_route = route_mcp_tool_call(
        user_input=user_input,
        available_tool_names=available_tool_names,
    )

    if tool_route is None:

        return None

    tool_name = tool_route["name"]

    if has_tool_after_latest_user(
        messages,
        tool_name,
    ):

        return None

    return tool_route


KNOWLEDGE_SCOPE_KEYWORDS = [
    "知识库",
    "资料库",
    "文档库",
    "knowledge base",
]


DOCUMENT_SCOPE_KEYWORDS = [
    "内部资料",
    "上传文档",
    "上传的文档",
    "文档",
    "资料",
    "文件",
]


KNOWLEDGE_QUERY_KEYWORDS = [
    "查",
    "查询",
    "检索",
    "搜索",
    "找",
    "看看",
    "帮我看",
    "根据",
    "基于",
    "参考",
    "从",
    "search",
    "retrieve",
]


SCOPE_LOCATION_MARKERS = [
    "里",
    "中",
    "内",
    "里面",
    "当中",
]


def contains_any(
    text: str,
    keywords,
):
    return any(
        keyword in text
        for keyword in keywords
    )


def has_scoped_location(
    text: str,
    scopes,
):
    return any(
        f"{scope}{marker}" in text
        for scope in scopes
        for marker in SCOPE_LOCATION_MARKERS
    )


def is_knowledge_search_intent(
    user_input: str,
):
    """
    只有用户明确要求查询知识库或上传资料时，才进入 RAG。
    """

    if not isinstance(
        user_input,
        str,
    ):

        return False

    text = user_input.lower().strip()

    if not text:

        return False

    if text.startswith(
        (
            "知识库:",
            "知识库：",
            "kb:",
            "kb：",
        )
    ):

        return True

    has_knowledge_scope = contains_any(
        text,
        KNOWLEDGE_SCOPE_KEYWORDS,
    )

    has_document_scope = contains_any(
        text,
        DOCUMENT_SCOPE_KEYWORDS,
    )

    has_query_intent = contains_any(
        text,
        KNOWLEDGE_QUERY_KEYWORDS,
    )

    if (
        has_knowledge_scope
        and (
            has_query_intent
            or has_scoped_location(
                text,
                KNOWLEDGE_SCOPE_KEYWORDS,
            )
        )
    ):

        return True

    if (
        has_document_scope
        and has_query_intent
        and has_scoped_location(
            text,
            DOCUMENT_SCOPE_KEYWORDS,
        )
    ):

        return True

    return False


def should_force_search_knowledge(
    state,
):
    messages = state.get(
        "messages",
        []
    )

    latest_user_message = get_latest_user_message(
        messages
    )

    if latest_user_message is None:

        return False

    # 关键：
    # 如果当前用户问题已经执行过任意 Tool，
    # 就不要再强制调用 search_knowledge。
    # 否则 MCP 工具执行后，又会被 RAG 抢走。
    if has_any_tool_after_latest_user(
        messages
    ):

        return False

    # 如果已经执行过 search_knowledge，也不要重复执行
    if has_tool_after_latest_user(
        messages,
        "search_knowledge",
    ):

        return False

    return is_knowledge_search_intent(
        latest_user_message.content
    )


def build_search_knowledge_call(
    state,
):
    messages = state.get(
        "messages",
        []
    )

    latest_user_message = get_latest_user_message(
        messages
    )

    query = latest_user_message.content

    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": "search_knowledge",
                "args": {
                    "query": query,
                },
                "id": f"tool_call_{uuid4().hex}",
                "type": "tool_call",
            }
        ],
    )


def agent_node(
    state,
):
    print("===== agent node =====")

    # ==========================
    # 1. MCP 确定性路由优先
    # ==========================

    mcp_route = get_mcp_tool_route(
        state
    )

    if mcp_route:

        print("===== force MCP tool =====")
        print(mcp_route)

        return {
            "messages": [
                build_tool_call_message(
                    mcp_route
                )
            ]
        }

    # ==========================
    # 2. RAG 兜底
    # ==========================

    if should_force_search_knowledge(
        state
    ):

        print("===== force search_knowledge tool =====")

        return {
            "messages": [
                build_search_knowledge_call(
                    state
                )
            ]
        }

    # ==========================
    # 3. 正常 LLM 回答
    # ==========================

    messages = build_messages(
        state
    )

    response = llm_with_tools.invoke(
        messages
    )

    return {
        "messages": [
            response
        ]
    }
