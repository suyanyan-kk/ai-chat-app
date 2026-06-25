# app/agent/mcp/servers.py

import os
import sys

from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEMO_MCP_SERVER_PATH = (
    PROJECT_ROOT
    / "app"
    / "mcp_servers"
    / "demo_server.py"
)

POSTGRES_MCP_SERVER_PATH = (
    PROJECT_ROOT
    /"app"
    / "mcp_servers"
    / "postgres_server.py"
)

FILESYSTEM_ROOT = (
    PROJECT_ROOT
    / "mcp_workspace"
)

GITHUB_TOKEN = os.getenv(
    "GITHUB_PERSONAL_ACCESS_TOKEN"
)


FILESYSTEM_ROOT.mkdir(
    parents=True,
    exist_ok=True,
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


# ==========================
# PostgreSQL MCP Server
# ==========================

if POSTGRES_MCP_SERVER_PATH.exists():

    MCP_SERVER_CONFIGS["postgres"] = {

        "transport": "stdio",

        "command": sys.executable,

        "args": [
            str(
                POSTGRES_MCP_SERVER_PATH
            )
        ],

        "cwd": str(
            PROJECT_ROOT
        ),
    }

# ==========================
# Remote Streamable HTTP MCP Server
# ==========================

MCP_SERVER_CONFIGS["remote_http"] = {

    "transport": "streamable_http",

    "url": "http://127.0.0.1:8765/mcp",

}
print("===== MCP server config =====")
print("PROJECT_ROOT:", PROJECT_ROOT)
print("DEMO_SERVER_EXISTS:", DEMO_MCP_SERVER_PATH.exists())
print("POSTGRES_SERVER_EXISTS:", POSTGRES_MCP_SERVER_PATH.exists())
print("FILESYSTEM_ROOT:", FILESYSTEM_ROOT)
print("FILESYSTEM_ROOT_EXISTS:", FILESYSTEM_ROOT.exists())
print("GITHUB_TOKEN_EXISTS:", bool(GITHUB_TOKEN))
print("MCP_SERVER_NAMES:", list(MCP_SERVER_CONFIGS.keys()))
print("PYTHON:", sys.executable)