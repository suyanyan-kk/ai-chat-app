 # 模型初始化
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.core.config import settings

load_dotenv()

model = ChatOpenAI(
    model="deepseek-chat",
    base_url=settings.DEEPSEEK_BASE_URL,
    api_key=settings.DEEPSEEK_API_KEY,
    temperature=0.7,
    streaming=True,
    max_tokens=2048
)
