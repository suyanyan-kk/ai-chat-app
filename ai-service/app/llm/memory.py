 # memory管理
from langchain.memory import ConversationBufferMemory
from .model import model

memory_store = {}

def get_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferMemory(
            llm=model,
            max_token_limit=100,
            return_messages=True,
            memory_key="history",
            input_key="input",
            output_key="output"
        )
    return memory_store[session_id]