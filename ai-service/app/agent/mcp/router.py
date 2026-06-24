# app/agent/mcp/router.py

import re


def normalize_text(
    text: str,
) -> str:

    return (
        text
        .lower()
        .strip()
    )


def find_tool_name(
    available_tool_names: set[str],
    candidates: list[str],
):

    for name in candidates:

        if name in available_tool_names:

            return name

    return None


def extract_repo_full_name(
    user_input: str,
):
    """
    提取 owner/repo
    例如：
    langchain-ai/langgraph
    """

    match = re.search(
        r"([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)",
        user_input,
    )

    if not match:

        return None

    return {
        "owner": match.group(1),
        "repo": match.group(2),
    }


def extract_github_search_query(
    user_input: str,
):
    query = user_input

    keywords = [
        "搜索 GitHub 仓库",
        "搜索github仓库",
        "搜索 GitHub",
        "搜索github",
        "GitHub 搜索",
        "github 搜索",
        "search github repositories",
        "search github repository",
        "search repositories",
        "search repository",
    ]

    lower_query = query.lower()

    for keyword in keywords:

        lower_keyword = keyword.lower()

        if lower_keyword in lower_query:

            index = lower_query.find(
                lower_keyword
            )

            query = query[
                index + len(keyword):
            ].strip()

            break

    if not query:

        query = user_input

    return query


def extract_github_file_path(
    user_input: str,
):
    """
    默认读 README.md。
    如果用户显式提到某个文件，则读那个文件。
    """

    known_files = [
        "README.md",
        "readme.md",
        "pyproject.toml",
        "package.json",
        "requirements.txt",
        "app/main.py",
        "src/main.py",
    ]

    for file_name in known_files:

        if file_name in user_input:

            return file_name

    match = re.search(
        r"(?:文件|路径|path|file)\s*[:：]?\s*([A-Za-z0-9_./-]+\.[A-Za-z0-9_]+)",
        user_input,
    )

    if match:

        return match.group(1)

    return "README.md"


def route_mcp_tool_call(
    user_input: str,
    available_tool_names: set[str],
):
    text = normalize_text(
        user_input
    )

    # ==========================
    # Demo: echo
    # ==========================

    if (
        "mcp" in text
        and "echo" in text
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "echo",
            ],
        )

        if tool_name:

            echo_text = user_input

            for keyword in [
                "调用 MCP 的 echo 工具，输入",
                "调用MCP的echo工具，输入",
                "echo 工具，输入",
                "echo工具，输入",
                "输入",
            ]:
                if keyword in echo_text:

                    echo_text = echo_text.split(
                        keyword,
                        1,
                    )[-1].strip()

                    break

            return {
                "name": tool_name,

                "args": {
                    "text": echo_text,
                },
            }

    # ==========================
    # Demo: project status
    # ==========================

    if (
        "project_status" in text
        or "get_project_status" in text
        or "项目状态" in user_input
        or "当前项目状态" in user_input
        or "AI 项目状态" in user_input
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "get_project_status",
            ],
        )

        if tool_name:

            return {
                "name": tool_name,
                "args": {},
            }

    # ==========================
    # Demo: learning route
    # ==========================

    if (
        "learning_route" in text
        or "get_learning_route" in text
        or "学习路线" in user_input
        or "路线" in user_input
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "get_learning_route",
            ],
        )

        if tool_name:

            return {
                "name": tool_name,
                "args": {},
            }

    # ==========================
    # Filesystem: list directory
    # ==========================

    if (
        "filesystem" in text
        and (
            "列出" in user_input
            or "查看目录" in user_input
            or "目录下" in user_input
            or "list directory" in text
            or "list files" in text
        )
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "list_directory",
            ],
        )

        if tool_name:

            return {
                "name": tool_name,

                "args": {
                    "path": ".",
                },
            }

    # ==========================
    # Filesystem: read file
    # ==========================

    if (
        "filesystem" in text
        and (
            "读取文件" in user_input
            or "查看文件" in user_input
            or "read file" in text
            or "test.txt" in text
        )
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "read_file",
                "read_text_file",
            ],
        )

        if tool_name:

            path = "test.txt"

            return {
                "name": tool_name,

                "args": {
                    "path": path,
                },
            }

    # ==========================
    # GitHub: search repositories
    # ==========================

    if (
        "github" in text
        and (
            "搜索" in user_input
            or "search" in text
        )
        and (
            "仓库" in user_input
            or "repository" in text
            or "repositories" in text
            or "repo" in text
        )
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "search_repositories",
            ],
        )

        if tool_name:

            query = extract_github_search_query(
                user_input
            )

            return {
                "name": tool_name,

                "args": {
                    "query": query,
                    "per_page": 5,
                },
            }

    # ==========================
    # GitHub: get file contents
    # ==========================

    if (
        "github" in text
        and (
            "读取" in user_input
            or "查看" in user_input
            or "read" in text
            or "get file" in text
            or "README" in user_input
            or "readme" in text
        )
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "get_file_contents",
            ],
        )

        repo = extract_repo_full_name(
            user_input
        )

        if tool_name and repo:

            path = extract_github_file_path(
                user_input
            )

            return {
                "name": tool_name,

                "args": {
                    "owner": repo["owner"],
                    "repo": repo["repo"],
                    "path": path,
                },
            }

    # ==========================
    # GitHub: list issues
    # ==========================

    if (
        "github" in text
        and (
            "issue" in text
            or "issues" in text
            or "问题" in user_input
        )
        and (
            "列出" in user_input
            or "查看" in user_input
            or "list" in text
        )
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "list_issues",
            ],
        )

        repo = extract_repo_full_name(
            user_input
        )

        if tool_name and repo:

            return {
                "name": tool_name,

                "args": {
                    "owner": repo["owner"],
                    "repo": repo["repo"],
                    "state": "open",
                    "per_page": 5,
                },
            }

    return None