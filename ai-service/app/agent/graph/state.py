from typing import TypedDict
from typing import Annotated

from langgraph.graph.message import (
    add_messages
)
 

class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]
# messages 是消息列表，Annotated不要覆盖
# 更新时使用 add_messages 合并策略

    sources: list