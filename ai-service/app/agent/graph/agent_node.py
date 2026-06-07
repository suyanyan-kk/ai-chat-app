from app.llm.model import model

from app.agent.tools.rag_tool import (
    search_knowledge
)

from app.agent.tools.weather_tool import (
    get_weather
) 

from app.agent.tools.time_tool import (
    get_current_time
)

from app.agent.tools.calculator_tool import (
    calculator
)

tools = [

    search_knowledge,

    get_weather,

    get_current_time,

    calculator
]

llm_with_tools = model.bind_tools(
    tools
)


def agent_node(state):
    print("===== agent node =====")
    response = llm_with_tools.invoke(
        state["messages"]
    )
    print(response)
    return {

        "messages": [
            response
        ],

        "sources":
            state.get(
                "sources",
                []
            )
    }