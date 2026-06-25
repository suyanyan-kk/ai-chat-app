# app/scripts/check_mcp_runtime.py
# 这个脚本的作用是：不用启动 FastAPI，也能单独检查 MCP Runtime 是否正常
# uv run python -m app.scripts.check_mcp_runtime
import asyncio

from app.agent.mcp.servers import (
    MCP_SERVER_CONFIGS,
)

from app.agent.mcp.client import (
    create_mcp_client,
)

from app.agent.mcp.tools import (
    SAFE_MCP_TOOL_NAMES,
)


def print_mcp_servers():

    print("\n===== MCP Servers =====")

    for server_name, config in MCP_SERVER_CONFIGS.items():

        transport = config.get(
            "transport"
        )

        print(f"- {server_name}")
        print(f"  transport: {transport}")

        if transport == "stdio":

            print(
                f"  command: {config.get('command')}"
            )

            print(
                f"  args: {config.get('args')}"
            )

        else:

            print(
                f"  url: {config.get('url')}"
            )


def classify_tool(
    tool_name: str,
):

    if tool_name in SAFE_MCP_TOOL_NAMES:

        return "safe"

    return "unsafe"


def guess_tool_group(
    tool_name: str,
):

    if tool_name.startswith(
        "pg_"
    ):

        return "postgres"

    if tool_name.startswith(
        "remote_"
    ):

        return "remote_http"

    github_keywords = [
        "repository",
        "repositories",
        "issue",
        "pull_request",
        "commit",
        "branch",
        "release",
        "tag",
        "code",
        "file_contents",
    ]

    for keyword in github_keywords:

        if keyword in tool_name:

            return "github"

    filesystem_keywords = [
        "file",
        "directory",
        "directories",
        "tree",
    ]

    for keyword in filesystem_keywords:

        if keyword in tool_name:

            return "filesystem"

    return "demo_or_other"


async def check_mcp_tools():

    print("\n===== Loading MCP Tools =====")

    client = create_mcp_client()

    tools = await client.get_tools()

    print(f"total tools: {len(tools)}")

    groups = {}

    for tool in tools:

        group = guess_tool_group(
            tool.name
        )

        groups.setdefault(
            group,
            []
        ).append(
            tool
        )

    print("\n===== MCP Tools By Group =====")

    for group_name, group_tools in groups.items():

        print(f"\n[{group_name}]")

        for tool in group_tools:

            status = classify_tool(
                tool.name
            )

            print(
                f"- {tool.name} [{status}]"
            )

    unsafe_tools = [
        tool.name
        for tool in tools
        if tool.name not in SAFE_MCP_TOOL_NAMES
    ]

    print("\n===== Unsafe Tools =====")

    if unsafe_tools:

        for name in unsafe_tools:

            print(f"- {name}")

    else:

        print("No unsafe tools found.")

    safe_tools = [
        tool.name
        for tool in tools
        if tool.name in SAFE_MCP_TOOL_NAMES
    ]

    print("\n===== Safe Tools Count =====")
    print(len(safe_tools))

    print("\n===== MCP Runtime Check Done =====")


async def main():

    print_mcp_servers()

    await check_mcp_tools()


if __name__ == "__main__":

    asyncio.run(
        main()
    )

# 结果：
#     ===== MCP Servers =====
# - demo
# - filesystem
# - github
# - postgres
# - remote_http

# ===== Loading MCP Tools =====
# total tools: xx

# ===== MCP Tools By Group =====

# [filesystem]
# - read_file [safe]
# - list_directory [safe]

# [github]
# - search_repositories [safe]
# - get_file_contents [safe]
# - create_repository [unsafe]

# [postgres]
# - pg_list_tables [safe]
# - pg_query_readonly [safe]

# [remote_http]
# - remote_echo [safe]
# - remote_add [safe]

# ===== Unsafe Tools =====
# - create_repository
# - delete_file
# - push_files
# - merge_pull_request
# ...