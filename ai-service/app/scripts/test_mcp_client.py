# scripts/test_mcp_client.py

import asyncio

from app.agent.mcp.client import (
    create_mcp_client,
)


async def main():

    print("===== test mcp client start =====")

    client = create_mcp_client()

    tools = await client.get_tools()

    print("===== tools loaded =====")
    print("total:", len(tools))

    for tool in tools:

        print("tool name:", tool.name)
        # print("tool description:", tool.description)
        # print("args schema:", tool.args_schema)
        print("-----")


if __name__ == "__main__":

    asyncio.run(
        main()
    )