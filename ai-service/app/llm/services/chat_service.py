import json
from ..chains import chat_chain
from ..memory import get_memory
from ..prompts import chat_prompt
from app.utils.message import create_message
from ..model import model
from app.core.logger import logger
from app.core.exception import AppException
def stream_chat(session_id: str, user_input: str):
    logger.info(f"[聊天请求] session={session_id}, message={user_input}")
    if not user_input:
        raise AppException("消息不能为空")
    try:
        memory = get_memory(session_id)
        history = memory.load_memory_variables({})["history"]

        messages = chat_prompt.invoke({
            "input": user_input,
            "history": history
         })

        full_response = ""

        ai_msg = create_message("AI", "", loading=True)
        yield json.dumps({"type": "start", "data": ai_msg}) + "\n"

        for chunk in model.stream(messages):
            if chunk.content:
                full_response += chunk.content
                yield json.dumps({
                    "type": "stream",
                    "data": chunk.content
                }) + "\n"

                yield json.dumps({
                    "type": "end",
                     "data": full_response
                }) + "\n"

        memory.save_context(
            {"input": user_input},
            {"output": full_response.strip()}
         )
    except Exception as e:
        logger.error(f"[LLM错误] {str(e)}")
        raise