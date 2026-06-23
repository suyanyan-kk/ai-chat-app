# app/agent/mcp/servers.py

import sys

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEMO_MCP_SERVER_PATH = (
    PROJECT_ROOT
    /"app"
    / "mcp_servers"
    / "demo_server.py"
)

FILESYSTEM_ROOT = (
    PROJECT_ROOT
    / "mcp_workspace"
)


print("===== MCP server config =====")
print("PROJECT_ROOT:", PROJECT_ROOT)
print("DEMO_MCP_SERVER_PATH:", DEMO_MCP_SERVER_PATH)
print("DEMO_SERVER_EXISTS:", DEMO_MCP_SERVER_PATH.exists())
print("FILESYSTEM_ROOT:", FILESYSTEM_ROOT)
print("FILESYSTEM_ROOT_EXISTS:", FILESYSTEM_ROOT.exists())
print("PYTHON:", sys.executable)


FILESYSTEM_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


MCP_SERVER_CONFIGS = {}


# ==========================
# Demo MCP Server
#
# 可选：
# 如果文件存在，就加载；
# 如果不存在，不影响主服务启动。
# ==========================

if DEMO_MCP_SERVER_PATH.exists():

    MCP_SERVER_CONFIGS["demo"] = {

        "transport": "stdio",

        "command": sys.executable,

        "args": [
            str(
                DEMO_MCP_SERVER_PATH
            )
        ],

        "cwd": str(
            PROJECT_ROOT
        ),

    }


# ==========================
# Filesystem MCP Server
# ==========================

MCP_SERVER_CONFIGS["filesystem"] = {

    "transport": "stdio",

    "command": "npx",

    "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        str(
            FILESYSTEM_ROOT
        ),
    ],

    "cwd": str(
        PROJECT_ROOT
    ),

}