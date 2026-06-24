# app/agent/mcp/tools.py

import asyncio
import threading
import traceback

from typing import Optional

from langchain_core.tools import BaseTool

from app.agent.mcp.client import (
    create_mcp_client,
)


_mcp_tools_cache: Optional[list[BaseTool]] = None

_mcp_tools_lock = threading.Lock()


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

    tools = await client.get_tools()

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

    thread.join()

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