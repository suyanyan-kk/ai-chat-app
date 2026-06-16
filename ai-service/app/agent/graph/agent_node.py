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


tools = [

    search_knowledge,

    get_weather,

    get_current_time,

    calculator,

]


llm_with_tools = model.bind_tools(
    tools
)


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


def has_search_knowledge_after_latest_user(
    messages,
):
    latest_user_index = -1

    for index in range(
        len(messages) - 1,
        -1,
        -1,
    ):

        if isinstance(
            messages[index],
            HumanMessage,
        ):
            latest_user_index = index
            break

    if latest_user_index == -1:
        return False

    for message in messages[
        latest_user_index + 1:
    ]:

        if isinstance(
            message,
            ToolMessage,
        ) and message.name == "search_knowledge":

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

    if has_search_knowledge_after_latest_user(
        messages
    ):
        return False

    return True


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
        ]
    )


def agent_node(
    state,
):
    print("===== agent node =====")

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


# # app/agent/graph/agent_node.py

# from app.llm.model import model

# from app.agent.graph.message_builder import (
#     build_messages,
# )

# from app.agent.tools.rag_tool import (
#     search_knowledge,
# )

# from app.agent.tools.weather_tool import (
#     get_weather,
# )

# from app.agent.tools.time_tool import (
#     get_current_time,
# )

# from app.agent.tools.calculator_tool import (
#     calculator,
# )


# tools = [

#     search_knowledge,

#     get_weather,

#     get_current_time,

#     calculator,

# ]


# llm_with_tools = model.bind_tools(
#     tools
# )


# def agent_node(
#     state,
# ):
#     print("===== agent node =====")

#     messages = build_messages(
#         state
#     )

#     response = llm_with_tools.invoke(
#         messages
#     )

#     return {
#         "messages": [
#             response
#         ]
#     }

