# app/agent/mcp/tools.py

import asyncio
import os
import threading
import traceback

from typing import Optional

from langchain_core.tools import BaseTool

from app.agent.mcp.client import (
    create_mcp_client,
)


_mcp_tools_cache: Optional[list[BaseTool]] = None

_mcp_tools_lock = threading.Lock()

MCP_TOOL_LOAD_TIMEOUT_SECONDS = float(
    os.getenv(
        "MCP_TOOL_LOAD_TIMEOUT_SECONDS",
        "8",
    )
)

MCP_TOOL_LOAD_THREAD_GRACE_SECONDS = 3


SAFE_MCP_TOOL_NAMES = {

    # ==========================
    # Demo
    # ==========================

    "echo",
    "get_project_status",
    "get_learning_route",

    # ==========================
    # Filesystem Readonly
    # ==========================

    "read_file",
    "read_text_file",
    "read_media_file",
    "read_multiple_files",
    "list_directory",
    "list_directory_with_sizes",
    "directory_tree",
    "search_files",
    "get_file_info",
    "list_allowed_directories",

    # ==========================
    # GitHub Readonly
    # ==========================

    "get_commit",
    "get_file_contents",
    "get_label",
    "get_latest_release",
    "get_release_by_tag",
    "get_tag",
    "issue_read",
    "list_branches",
    "list_commits",
    "list_issue_types",
    "list_issues",
    "list_pull_requests",
    "list_releases",
    "list_repository_collaborators",
    "list_tags",
    "pull_request_read",
    "search_code",
    "search_commits",
    "search_issues",
    "search_pull_requests",
    "search_repositories",

    # ==========================
    # PostgreSQL Readonly
    # ==========================

    "pg_list_tables",
    "pg_describe_table",
    "pg_query_readonly",
    "pg_get_knowledge_files",

    # ==========================
    # Remote HTTP MCP
    # ==========================

    "remote_echo",
    "remote_project_runtime_status",
    "remote_add",
}


def print_exception_detail(
    error: BaseException,
):
    print("===== MCP load exception detail =====")
    print(type(error))
    print(repr(error))

    if hasattr(
        error,
        "exceptions"
    ):
        print("===== MCP ExceptionGroup children =====")

        for index, child in enumerate(
            error.exceptions
        ):
            print(f"----- child exception {index} -----")
            print(type(child))
            print(repr(child))

            traceback.print_exception(
                type(child),
                child,
                child.__traceback__,
            )

    traceback.print_exception(
        type(error),
        error,
        error.__traceback__,
    )


def filter_safe_mcp_tools(
    tools: list[BaseTool],
) -> list[BaseTool]:

    safe_tools = []

    skipped_tools = []

    for tool in tools:

        if tool.name in SAFE_MCP_TOOL_NAMES:

            safe_tools.append(
                tool
            )

        else:

            skipped_tools.append(
                tool.name
            )

    print("===== MCP safe tools =====")
    print(
        [
            tool.name
            for tool in safe_tools
        ]
    )

    print("===== MCP skipped unsafe tools =====")
    print(skipped_tools)

    return safe_tools


async def load_mcp_tools() -> list[BaseTool]:

    print("===== load MCP tools start =====")

    client = create_mcp_client()

    async def load_server_tools(
        server_name: str,
    ) -> list[BaseTool]:

        try:

            server_tools = await asyncio.wait_for(
                client.get_tools(
                    server_name=server_name
                ),
                timeout=MCP_TOOL_LOAD_TIMEOUT_SECONDS,
            )

        except asyncio.TimeoutError:

            print(
                "===== MCP server load timeout =====",
                server_name,
                f"{MCP_TOOL_LOAD_TIMEOUT_SECONDS}s",
            )

            return []

        except Exception as error:

            print(
                "===== MCP server load failed =====",
                server_name,
                repr(error),
            )

            return []

        print(
            "===== MCP server tools loaded =====",
            server_name,
        )

        return server_tools

    server_names = list(
        client.connections
    )

    tool_groups = await asyncio.gather(
        *[
            load_server_tools(
                server_name
            )
            for server_name in server_names
        ]
    )

    tools = [
        tool
        for tool_group in tool_groups
        for tool in tool_group
    ]

    print("===== MCP tools loaded raw =====")

    for tool in tools:

        print(
            f"MCP Tool: {tool.name}"
        )

    safe_tools = filter_safe_mcp_tools(
        tools
    )

    return safe_tools


def _run_async_in_new_thread() -> list[BaseTool]:

    result = {
        "tools": None,
        "error": None,
    }

    def runner():

        try:

            result["tools"] = asyncio.run(
                load_mcp_tools()
            )

        except BaseException as e:

            result["error"] = e

    thread = threading.Thread(
        target=runner,
        daemon=True,
    )

    thread.start()

    thread.join(
        MCP_TOOL_LOAD_TIMEOUT_SECONDS
        + MCP_TOOL_LOAD_THREAD_GRACE_SECONDS
    )

    if thread.is_alive():

        raise TimeoutError(
            "MCP tools load thread did not finish "
            f"within {MCP_TOOL_LOAD_TIMEOUT_SECONDS}s"
        )

    if result["error"] is not None:

        print_exception_detail(
            result["error"]
        )

        raise result["error"]

    return result["tools"] or []


def load_mcp_tools_sync() -> list[BaseTool]:

    global _mcp_tools_cache

    with _mcp_tools_lock:

        if _mcp_tools_cache is not None:

            return _mcp_tools_cache

        try:

            loop = asyncio.get_running_loop()

        except RuntimeError:

            loop = None

        try:

            if loop and loop.is_running():

                tools = _run_async_in_new_thread()

            else:

                tools = asyncio.run(
                    load_mcp_tools()
                )

        except BaseException as e:

            print_exception_detail(
                e
            )

            raise e

        _mcp_tools_cache = tools

        return tools
