from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.services.llm_service import stream_llm, ask_llm, chatmemory_llm
import time
import uvicorn
app = FastAPI()

# 流式接口+多会话
@app.post("/langchain-practice")
def langchain_practice(data: dict): 
     session_id = data["session_id"]   # 前端需要传入 session_id 来区分不同用户的对话历史
     message = data["message"]
     answer = stream_llm(session_id, message)
     return StreamingResponse(
            answer,
            media_type="text/plain"
        )

@app.post("/chat-stream")
async def chat_stream(data: dict):
    return StreamingResponse(
        stream_llm(data["message"]),
        media_type="text/plain"
    )

@app.post("/chat") 
def chat(data: dict):
    answer = ask_llm(data["message"])
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "AI Service is running"}


def dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)