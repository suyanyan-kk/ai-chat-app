import json
from ..chains import chat_chain
from ..memory import get_memory
from ..prompts import chat_prompt
from app.utils.message import create_message
from ..model import model

def stream_chat(session_id: str, user_input: str):
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