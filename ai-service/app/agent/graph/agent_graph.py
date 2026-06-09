from langgraph.graph import (
    StateGraph,
    START,
    END
)
 
from app.agent.graph.custom_tool_node import (
    CustomToolNode
)
from app.agent.graph.state import (
    AgentState
)

from app.agent.graph.agent_node import (
    agent_node,
    tools 
)

builder = StateGraph(
    AgentState
)

builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    CustomToolNode(tools)
)

builder.add_edge(
    START,
    "agent"
)
def should_continue(
    state: AgentState
):

    messages = state["messages"]

    last_message = messages[-1]

    if last_message.tool_calls:

        return "tools"

    return END


builder.add_conditional_edges(

    "agent",

    should_continue,

    {

        "tools": "tools",

        END: END
    }
)
builder.add_edge(
    "tools",
    "agent"
)
graph = builder.compile()