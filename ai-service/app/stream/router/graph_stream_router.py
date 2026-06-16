# app/stream/router/graph_stream_router.py


def extract_token_content(chunk):
    content = getattr(
        chunk,
        "content",
        ""
    )

    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_list = []

        for item in content:

            if isinstance(item, str):
                text_list.append(item)

            elif isinstance(item, dict):
                text = item.get("text", "")

                if text:
                    text_list.append(text)

        return "".join(text_list)

    return str(content)


def route_graph_stream(stream_item):
    """
    graph.astream(stream_mode=["messages", "updates"])
        ↓
    业务事件
    """

    if not isinstance(stream_item, tuple):
        return None

    if len(stream_item) != 2:
        return None

    mode, payload = stream_item

    # ==========================
    # messages -> token
    # ==========================

    if mode == "messages":

        if not isinstance(payload, tuple):
            return None

        if len(payload) != 2:
            return None

        chunk, metadata = payload

        node_name = metadata.get(
            "langgraph_node"
        )

        if node_name != "agent":
            return None

        token = extract_token_content(
            chunk
        )

        if not token:
            return None

        return {
            "type": "token",
            "content": token
        }

    # ==========================
    # updates -> sources
    # ==========================

    if mode == "updates":

        if not isinstance(payload, dict):
            return None

        print("===== graph updates payload =====")
        print(payload)

        for node_name, update in payload.items():

            if not isinstance(update, dict):
                continue

            sources = update.get(
                "sources",
                []
            )

            if sources:
                return {
                    "type": "sources",
                    "sources": sources
                }

        return None

    return None