import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
load_dotenv()

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
            # 每当接收到新的内容块时，yield 返回给前端
            # 这里可以根据需要对 chunk.content 进行处理，比如过滤掉空内容或者添加一些格式
            # 注意：yield 只能返回字符串类型，如果 chunk.content 是其他类型，需要先转换成字符串
            # 例如，如果 chunk.content 是一个字典，可以使用 json.dumps(chunk.content) 转换成 JSON 字符串
            yield chunk.content 

def ask_llm(message: str):
    response = chain.invoke([
        HumanMessage(content=message)
    ])
    return response.content
