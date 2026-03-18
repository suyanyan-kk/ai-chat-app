from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1️⃣ 模型
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# 2️⃣ Prompt（重点）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个前端开发专家，回答要简洁清晰"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 3️⃣ Memory（记忆）
memory = ConversationBufferMemory(
    return_messages=True
)

# 4️⃣ 输出解析
parser = StrOutputParser()

# 5️⃣ 组合 Chain
chain = prompt | model | parser


# ===== 封装一个函数 =====
def chat(user_input):
    # 取历史记录
    history = memory.load_memory_variables({})["history"]

    # 调用链
    response = chain.invoke({
        "input": user_input,
        "history": history
    })

    # 存回记忆
    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

    return response


# ===== 测试 =====
print(chat("你好"))
print(chat("我刚才说了什么？"))