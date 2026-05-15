# 所有Prompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 聊天
chat_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        你是一个 AI 助手。
        请优先根据知识库内容回答问题。
        如果知识库没有相关内容，
        再使用你自己的知识回答。
        知识库内容：
        {context}
        """
    ),
    MessagesPlaceholder(
        variable_name="history"
    ),
    (
        "human",
        "{input}"
    )
])
# 标题
title_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个标题生成助手"),
    ("human", """
        请根据用户的问题生成一个简短的会话标题（10字以内）：
        只输出标题：
        {input}""")
    ])

# 简单问答
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的AI助手"),
    ("human", "{input}")
])