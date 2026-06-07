from langgraph.prebuilt import ToolNode
import json
import traceback


class CustomToolNode(ToolNode):

    def invoke(
        self,
        state,
        config=None
    ):

        print("===== tool node start =====")

        try:

            result = super().invoke(
                state,
                config
            )

            print("===== tool result =====")
            print(result)

            sources = []

            for message in result["messages"]:

                try:

                    data = json.loads(
                        message.content
                    )

                    if "sources" in data:

                        sources.extend(
                            data["sources"]
                        )

                        message.content = (
                            data["context"]
                        )

                except Exception as e:

                    print("json parse error:", e)

            print("===== tool node end =====")

            return {
                "messages": result["messages"],
                "sources": sources
            }

        except Exception as e:

            print("===== tool exception =====")
            print(e)

            traceback.print_exc()

            raise