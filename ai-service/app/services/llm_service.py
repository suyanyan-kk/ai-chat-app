import os
from dotenv import load_dotenv
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from app.utils.message import create_message
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
        memory_store[session_id] = ConversationBufferMemory(
            llm=model,
            # max_token_limit 定义了 memory 中保留的对话历史的最大 token 数量，超过这个限制时会丢弃最早的对话
            max_token_limit=100,
            return_messages=True,
            # 这里可以将"history"替换成更具体的名字，比如"user_history"，
            # 并在 Prompt 中对应修改 MessagesPlaceholder 的 variable_name
            memory_key="history",
            # input_key 和 output_key 定义了在 memory 中存储对话时，
            # 用户输入和模型输出的键名
            input_key="input",
            output_key="output"
            )
    return memory_store[session_id]

# ===== 流式输出（升级版：带 Prompt + Memory）=====
def stream_llm(session_id: str, user_input: str):
    memory = get_memory(session_id)

    history = memory.load_memory_variables({})["history"]
    # print("👉 memory有哪些方法:", dir(memory))

    # 用 prompt 构造完整消息
    messages = prompt.invoke({
        "input": user_input,
        "history": history
    })

    full_response = ""
  # 👉 先发一个“空AI消息”（前端用来占位）
    ai_msg = create_message("AI", "", loading=True)
    yield json.dumps({"type": "start", "data": ai_msg}) + "\n"

    for chunk in model.stream(messages):
        #   print("👉 chunk对象:", chunk)           # 看整体
        #   print("👉 chunk.content:", chunk.content)  # 看内容
        #   print("👉 类型:", type(chunk))
        #   print("------")
        if chunk.content:
            full_response += chunk.content
             # 👉 每一段流式返回
            yield json.dumps({
                "type": "stream",
                "data": chunk.content
                }) + "\n"
 # 👉 结束
    yield json.dumps({
        "type": "end",
        "data": full_response
    }) + "\n"
    # 存入 memory
    memory.save_context(
        {"input": user_input},
        {"output": full_response.strip()}
    )



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


# ===== 简单问答（无记忆）=====
def ask_llm(message: str):
    response = model.invoke([
        HumanMessage(content=message)
    ])
    return response.content