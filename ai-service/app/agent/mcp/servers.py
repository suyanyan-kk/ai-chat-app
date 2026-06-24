# app/agent/mcp/servers.py

import os
import sys

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


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

GITHUB_TOKEN = os.getenv(
    "GITHUB_PERSONAL_ACCESS_TOKEN"
)


print("===== MCP server config =====")
print("PROJECT_ROOT:", PROJECT_ROOT)
print("DEMO_MCP_SERVER_PATH:", DEMO_MCP_SERVER_PATH)
print("DEMO_SERVER_EXISTS:", DEMO_MCP_SERVER_PATH.exists())
print("FILESYSTEM_ROOT:", FILESYSTEM_ROOT)
print("FILESYSTEM_ROOT_EXISTS:", FILESYSTEM_ROOT.exists())
print("GITHUB_TOKEN_EXISTS:", bool(GITHUB_TOKEN))
print("PYTHON:", sys.executable)


FILESYSTEM_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


MCP_SERVER_CONFIGS = {}


# ==========================
# Demo MCP Server
# 可选
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


# ==========================
# GitHub MCP Server
#
# 第一阶段只加载只读类 toolsets：
# repos / issues / pull_requests
# ==========================

if GITHUB_TOKEN:

    MCP_SERVER_CONFIGS["github"] = {

        "transport": "stdio",

        "command": "docker",

        "args": [
            "run",
            "-i",
            "--rm",

            "-e",
            f"GITHUB_PERSONAL_ACCESS_TOKEN={GITHUB_TOKEN}",

            "-e",
            "GITHUB_TOOLSETS=repos,issues,pull_requests",

            "ghcr.io/github/github-mcp-server",
        ],

        "cwd": str(
            PROJECT_ROOT
        ),

    }

else:

    print(
        "===== GitHub MCP skipped: GITHUB_PERSONAL_ACCESS_TOKEN not found ====="
    )