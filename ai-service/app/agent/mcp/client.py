# MCP Client 初始化
# app/agent/mcp/client.py

from langchain_mcp_adapters.client import (
    MultiServerMCPClient,
)

from app.agent.mcp.servers import (
    MCP_SERVER_CONFIGS,
)


def create_mcp_client():
    """
    创建 MCP Client。

    MultiServerMCPClient 可以同时连接多个 MCP Server。
    """

    return MultiServerMCPClient(
        MCP_SERVER_CONFIGS
    )