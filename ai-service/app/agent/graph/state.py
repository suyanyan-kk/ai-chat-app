from typing import Annotated
from typing import Any
from typing import TypedDict

import json

from langchain_core.messages import AnyMessage

from langgraph.graph.message import add_messages


def replace(_, new):
    return new


def merge_sources(old, new):
    old = old or []
    new = new or []

    merged = []
    seen = set()

    for item in old + new:
        key = json.dumps(
            item,
            ensure_ascii=False,
            sort_keys=True
        )

        if key in seen:
            continue

        seen.add(key)
        merged.append(item)

    return merged


class AgentState(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    sources: Annotated[
        list[dict],
        merge_sources
    ]

    metadata: Annotated[
        dict[str, Any],
        replace
    ]