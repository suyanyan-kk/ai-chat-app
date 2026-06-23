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


llm_with_tools = model.bind_tools(
    llm_tools
)


# ==========================
# Message Helpers
# ==========================

def get_latest_user_message(
    messages,
):
    for message in reversed(messages):

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

        if (
            isinstance(
                message,
                ToolMessage,
            )
            and message.name == tool_name
        ):

            return True

    return False


# ==========================
# MCP Router
# ==========================

def build_mcp_tool_call(
    tool_route,
):
    tool_name = tool_route["name"]

    tool_args = tool_route.get(
        "args",
        {}
    )

    return AIMessage(

        content="",

        tool_calls=[
            {
                "name": tool_name,

                "args": tool_args,

                "id": f"call_{tool_name}_{uuid4().hex}",

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

    route = route_mcp_tool_call(
        user_input=user_input,
        available_tool_names=available_tool_names,
    )

    if route is None:

        return None

    tool_name = route["name"]

    if has_tool_after_latest_user(
        messages,
        tool_name,
    ):

        return None

    return route


# ==========================
# RAG Router
# ==========================

KNOWLEDGE_SCOPE_KEYWORDS = [
    "知识库",
    "资料库",
    "文档库",
    "knowledge base",
]


DOCUMENT_SCOPE_KEYWORDS = [
    "文档",
    "资料",
    "文件",
    "内部资料",
    "上传文档",
    "上传的文档",
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
    只有用户明确要查知识库 / 上传资料时，才进入 RAG。
    普通聊天、MCP 问答、天气、时间、计算都不走 search_knowledge。
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
    latest_user_message = get_latest_user_message(
        state.get(
            "messages",
            []
        )
    )

    query = latest_user_message.content

    return AIMessage(

        content="",

        tool_calls=[
            {
                "name": "search_knowledge",

                "args": {
                    "query": query
                },

                "id": f"call_search_knowledge_{uuid4().hex}",

                "type": "tool_call",
            }
        ],
    )


# ==========================
# Agent Node
# ==========================

def agent_node(
    state,
):
    print("===== agent node =====")

    # ==========================
    # 1. MCP Router 优先
    # ==========================

    mcp_route = get_mcp_tool_route(
        state
    )

    if mcp_route is not None:

        print("===== force MCP tool =====")
        print(mcp_route)

        return {
            "messages": [
                build_mcp_tool_call(
                    mcp_route
                )
            ]
        }

    # ==========================
    # 2. RAG Router
    # ==========================

    if should_force_search_knowledge(
        state
    ):

        print("===== force search_knowledge =====")

        return {
            "messages": [
                build_search_knowledge_call(
                    state
                )
            ]
        }

    # ==========================
    # 3. Normal LLM
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
