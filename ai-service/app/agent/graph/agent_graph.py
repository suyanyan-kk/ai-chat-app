from langgraph.graph import (
    StateGraph,
    START,
    END
)
 
# from langgraph.prebuilt import ToolNode
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
# 意思：

# 开始
#  ↓
# agent
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
# agent执行完
# ↓
# 调用 should_continue(state)
# ↓
# 拿到返回值
# ↓
# 查字典
# ↓
# 决定下一步去哪
# {

#         "tools": "tools",

#         END: END
#     }
# 其实就是：
# switch(result)

# case "tools":
#     goto tools

# case END:
#     goto END
builder.add_edge(
    "tools",
    "agent"
)
# 意思：

# tools执行完
# ↓
# agent

# 画图：

# tools -------> agent
graph = builder.compile()
# 把设计图
# ↓
# 变成真正可运行的Graph