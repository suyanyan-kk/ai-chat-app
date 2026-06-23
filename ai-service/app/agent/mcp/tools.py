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


async def load_mcp_tools() -> list[BaseTool]:
    """
    异步加载 MCP Tools。
    """

    print("===== load MCP tools start =====")

    client = create_mcp_client()

    tools = await client.get_tools()

    print("===== MCP tools loaded =====")

    for tool in tools:

        print(
            f"MCP Tool: {tool.name}"
        )

    return tools


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
    """
    同步加载 MCP Tools。

    当前 agent_node.py 在模块加载阶段构造 tools，
    所以这里做同步包装。
    """

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