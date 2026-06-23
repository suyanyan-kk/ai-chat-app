# app/agent/mcp/router.py


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


def route_mcp_tool_call(
    user_input: str,
    available_tool_names: set[str],
):
    """
    MCP Router

    根据用户输入，判断是否需要强制调用 MCP Tool。
    """

    text = normalize_text(
        user_input
    )

    # ==========================
    # demo echo
    # ==========================

    if (
        "mcp" in text
        and "echo" in text
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "echo",
                "demo_echo",
            ]
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
                        1
                    )[-1].strip()

                    break

            return {
                "name": tool_name,

                "args": {
                    "text": echo_text
                }
            }

    # ==========================
    # demo project status
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
                "demo_get_project_status",
            ]
        )

        if tool_name:

            return {
                "name": tool_name,
                "args": {}
            }

    # ==========================
    # demo learning route
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
                "demo_get_learning_route",
            ]
        )

        if tool_name:

            return {
                "name": tool_name,
                "args": {}
            }

    # ==========================
    # filesystem list directory
    # ==========================

    if (
        "列出" in user_input
        or "查看目录" in user_input
        or "目录下" in user_input
        or "list directory" in text
        or "list files" in text
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "list_directory",
                "filesystem_list_directory",
            ]
        )

        if tool_name:

            return {
                "name": tool_name,

                "args": {
                    "path": "."
                }
            }

    # ==========================
    # filesystem read file
    # ==========================

    if (
        "读取文件" in user_input
        or "查看文件" in user_input
        or "read file" in text
        or "test.txt" in text
    ):

        tool_name = find_tool_name(
            available_tool_names,
            [
                "read_file",
                "filesystem_read_file",
            ]
        )

        if tool_name:

            path = "test.txt"

            # 简单提取：如果用户明确说了 test.txt，就读 test.txt
            if "test.txt" in user_input:
                path = "test.txt"

            return {
                "name": tool_name,

                "args": {
                    "path": path
                }
            }

    return None