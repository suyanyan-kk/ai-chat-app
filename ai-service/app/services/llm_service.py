import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

deepSeek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepSeek_base_url = os.getenv("DEEPSEEK_BASE_URL")

# ===== 模型 =====
model = ChatOpenAI(
    model="deepseek-chat",
    base_url=deepSeek_base_url,
    api_key=deepSeek_api_key,
    temperature=0.7,
    streaming=True,
    max_tokens=100
)

# ===== Prompt =====
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个前端开发专家，回答要简洁清晰"),
    # ("system", "你是一个可以从我私人知识库里提取答案的专家，回答要简洁清晰"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# ===== Parser =====
parser = StrOutputParser()

# ===== Chain =====
chain = prompt | model | parser

# ===== Memory 管理（按用户隔离）=====
memory_store = {}

def get_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferMemory(return_messages=True)
    return memory_store[session_id]


# ===== 普通聊天（带记忆）=====
def chatmemory_llm(session_id: str, user_input: str):
    memory = get_memory(session_id)

    history = memory.load_memory_variables({})["history"]

    response = chain.invoke({
        "input": user_input,
        "history": history
    })

    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

    return response


# ===== 流式输出（升级版：带 Prompt + Memory）=====
def stream_llm(session_id: str, user_input: str):
    memory = get_memory(session_id)
    history = memory.load_memory_variables({})["history"]

    # 用 prompt 构造完整消息
    messages = prompt.invoke({
        "input": user_input,
        "history": history
    })

    full_response = ""

    for chunk in model.stream(messages):
        if chunk.content:
            full_response += chunk.content
            yield chunk.content

    # 存入 memory
    memory.save_context(
        {"input": user_input},
        {"output": full_response}
    )


# ===== 简单问答（无记忆）=====
def ask_llm(message: str):
    response = model.invoke([
        HumanMessage(content=message)
    ])
    return response.content