from typing import Annotated
from typing import Any
from typing import TypedDict

from langchain_core.messages import AnyMessage

from langgraph.graph.message import add_messages


def replace(_, new):
    return new


class AgentState(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    sources: Annotated[
        list[dict],
        replace
    ]

    metadata: Annotated[
        dict[str, Any],
        replace
    ]
