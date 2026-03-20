from ..chains import title_chain
from app.core.logger import logger
def generate_title(message: str):
    logger.info(f"[生成标题] {message}")
    return title_chain.invoke({
        "input": message
    })