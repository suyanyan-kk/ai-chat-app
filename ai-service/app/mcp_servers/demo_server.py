# mcp_servers/demo_server.py

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "ai-service-demo-mcp"
)


@mcp.tool()
def echo(
    text: str,
) -> str:
    """
    测试 MCP 调用链路。
    """

    return f"MCP Echo: {text}"


@mcp.tool()
def get_project_status() -> str:
    """
    获取当前 AI 项目的阶段状态。
    """

    return """
当前 AI 项目状态：

1. 已完成企业级 RAG Workflow
2. 已完成 Agent Runtime 第一阶段
3. 已完成 Streaming Runtime
4. 已完成 Conversation Memory
5. 当前正在进入 MCP Runtime 阶段
"""


@mcp.tool()
def get_learning_route() -> str:
    """
    获取当前 AI 项目的学习路线。
    """

    return """
当前学习路线：

1. RAG 工程
2. Agent Runtime
3. Streaming Runtime
4. Conversation Memory
5. MCP Runtime
6. Summary Memory
7. Long Memory
8. Multi-Agent Runtime
"""


if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )