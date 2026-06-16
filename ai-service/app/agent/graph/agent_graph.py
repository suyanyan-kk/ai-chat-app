# app/agent/graph/agent_graph.py

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.memory import (
    MemorySaver,
)

from app.agent.graph.state import (
    AgentState,
)

from app.agent.graph.agent_node import (
    agent_node,
    tools,
)

from app.agent.graph.custom_tool_node import (
    CustomToolNode,
)


builder = StateGraph(
    AgentState
)

memory = MemorySaver()


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    CustomToolNode(
        tools
    )
)


builder.add_edge(
    START,
    "agent"
)


def should_continue(
    state: AgentState,
):
    messages = state["messages"]

    last_message = messages[-1]

    if getattr(
        last_message,
        "tool_calls",
        None,
    ):
        return "tools"

    return END


builder.add_conditional_edges(

    "agent",

    should_continue,

    {
        "tools": "tools",
        END: END,
    }

)


builder.add_edge(
    "tools",
    "agent"
)


graph = builder.compile(
    checkpointer=memory
)