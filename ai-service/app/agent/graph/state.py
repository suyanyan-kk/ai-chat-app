from typing import TypedDict
from typing import Annotated

from langgraph.graph.message import (
    add_messages
)
from operator import add

class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]

    sources: Annotated[
        list,
        add
    ]
