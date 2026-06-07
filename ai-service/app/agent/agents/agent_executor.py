from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from app.llm.model import model

from app.agent.prompts.agent_prompt import (
    agent_prompt 
)

from app.agent.tools.rag_tool import (
    search_knowledge
)

from app.agent.tools.time_tool import (
    get_current_time
)

from app.agent.tools.calculator_tool import (
    calculator
)

from app.agent.tools.weather_tool import (
    get_weather
)

tools = [

    search_knowledge,

    get_current_time,

    calculator,

    get_weather
]
 
agent = create_tool_calling_agent(

    llm=model,

    tools=tools,

    prompt=agent_prompt
)
 
agent_executor = AgentExecutor(

    agent=agent,

    tools=tools,

    verbose=True,
    # 以后控制台会打印：
    # Thought:
    # ...
    # Action:
    # search_knowledge
    # Observation:
    # ...
    return_intermediate_steps=True
)