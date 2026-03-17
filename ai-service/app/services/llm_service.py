import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

deepSeek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepSeek_base_url = os.getenv("DEEPSEEK_BASE_URL")

# 创建 LLM 模型
chain = ChatOpenAI(
    model="deepseek-chat",
    base_url=deepSeek_base_url,
    api_key= deepSeek_api_key,
    streaming=True
)


def stream_llm(message):

    for chunk in chain.stream([
        HumanMessage(content=message)
    ]):

        if chunk.content:
            yield chunk.content 

def ask_llm(message: str):
    response = chain.invoke([
        HumanMessage(content=message)
    ])
    return response.content
# 如果想指定模型可以这样写
# llm = ChatOpenAI(model_name="gpt-4")

# 直接提供问题，并调用 llm
# 向模型提问
# 这里是 LangChain 统一的调用方式：
# response = llm.invoke("你好")

# 打印完整响应对象
# print(response)

# 打印模型返回的文本内容
# print(response.content)
