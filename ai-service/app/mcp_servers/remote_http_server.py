# mcp_servers/remote_http_server.py

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "ai-service-remote-http-mcp",
    stateless_http=True,
    json_response=True,
    host="127.0.0.1",
    port=8765,
)


@mcp.tool()
def remote_echo(
    text: str,
) -> str:
    """
    Streamable HTTP MCP 测试工具。
    """

    return f"Remote HTTP MCP Echo: {text}"


@mcp.tool()
def remote_project_runtime_status() -> str:
    """
    获取远程 MCP Runtime 状态。
    """

    return """
Remote HTTP MCP Server 已连接成功。
"""


@mcp.tool()
def remote_add(
    a: int,
    b: int,
) -> int:
    """
    远程 MCP 加法工具。
    """

    return a + b


if __name__ == "__main__":

    mcp.run(
        transport="streamable-http"
    )