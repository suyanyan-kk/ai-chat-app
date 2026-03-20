from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.request import ChatRequest
from app.llm.services.chat_service import stream_chat
from app.llm.services.simple_service import ask_llm

router = APIRouter()

# 流式
@router.post("/chat-stream")
def chat_stream(req: ChatRequest):
    answer = stream_chat(req.session_id, req.message)
    return StreamingResponse(answer, media_type="text/plain")

# 普通
@router.post("/chat")
def chat(req: ChatRequest):
    answer = ask_llm(req.message)
    return {"answer": answer}