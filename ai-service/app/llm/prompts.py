# 所有Prompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 聊天
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的AI助手"),
    # ("system", "你是一个前端开发专家，回答要简洁清晰"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
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