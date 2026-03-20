import time
import uuid

def create_message(role, content, msg_type="text", loading=False):
    return {
        "id": str(uuid.uuid4()),
        "role": role,
        "content": content,
        "type": msg_type,
        "time": int(time.time() * 1000),
        "loading": loading
    }