# app/agent/graph/message_builder.py

from copy import deepcopy

from app.agent.graph.state import AgentState


def build_messages(
    state: AgentState,
):
    """
    构建发送给 LLM 的 messages。

    当前第一版职责：
    1. 不直接修改 Graph State
    2. 后续 Memory / System Prompt / History Compress 都放这里
    """

    messages = deepcopy(
        state.get(
            "messages",
            []
        )
    )

    return messages