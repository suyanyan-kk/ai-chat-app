from langchain_core.prompts import ChatPromptTemplate

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
你是一个智能助手。  

你拥有以下工具：

1. search_knowledge
用于查询知识库内容

2. get_current_time
用于获取当前时间

3. calculator
用于数学计算

4. get_weather
用于获取天气信息

优先使用工具。

不要编造答案。

{agent_scratchpad}
"""
        ),
        (
            "human",
            "{input}"
        )
    ]
)

# {agent_scratchpad} = Agent的思考过程