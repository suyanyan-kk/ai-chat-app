import json
from ..chains import chat_chain
from ..memory import get_memory
from ..prompts import chat_prompt
from app.utils.message import create_message
from ..model import model
from app.core.logger import logger
from app.core.exception import AppException
 
# from app.rag.retrieval.retrieval_service import build_rag_context
from app.rag.retrieval.retrieval_service import retrieval_pipeline
from app.agent.agent_service import agent_chat


def stream_chat(session_id: str, user_input: str):
    logger.info(f"[聊天请求] session={session_id}, message={user_input}")
    if not user_input:
        raise AppException("消息不能为空")
    try:
        memory = get_memory(session_id)
        history = memory.load_memory_variables({})["history"]

        # start   
        yield json.dumps({"type": "start", "data": {}}) + "\n"

        result = agent_chat(user_input, history)
        context = result["answer"]
        sources = result["sources"]
        # stream
        yield json.dumps(
            {"type": "stream", "data": {"context": context, "sources": sources}},
            ensure_ascii=False,
        ) + "\n"

        # end
        yield json.dumps(
            {"type": "end", "data": {"context": context, "sources": sources}},
            ensure_ascii=False,
        ) + "\n"
        # 保存memory
        memory.save_context({"input": user_input}, {"output": context})
  
    except Exception as e:
        logger.error(f"[LLM错误] {str(e)}")
        raise






        # =========================
        # RAG
        # =========================
        # 1、
        # rag_data = build_rag_context(user_input)
        # 2、
        # rag_data = retrieval_pipeline(user_input)

        # context = rag_data["context"]
        # sources = rag_data["sources"]
        # # =========================
        # # prompt
        # # =========================
        # messages = chat_prompt.invoke(
        #     {"input": user_input, "history": history, "context": context}
        # )
        # 3、
        # full_response = ""