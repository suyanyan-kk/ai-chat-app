import os
from uuid import uuid4
from app.knowledgedb import models, schemas
from app.rag.chunk.chunk_service import create_chunks
from app.utils.parsers.parser_factory import parse_by_file_type
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

async def save_upload_file(file, db):

    # 读取文件
    content = await file.read()

    # uuid 文件名
    ext = file.filename.split(".")[-1]

    uuid_name = f"{uuid4()}.{ext}"

    # 创建目录
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 保存路径
    file_path = os.path.join(
        UPLOAD_DIR,
        uuid_name
    )

    # 写文件
    with open(file_path, "wb") as f:
        f.write(content)

    # 提取文本
    text_content = parse_by_file_type(file_path, ext)

    # 创建文件记录
    file_item = models.KnowledgeFile(
        original_name=file.filename,
        uuid_name=uuid_name,
        file_url=file_path,
        file_size=len(content),
        file_type=file.content_type,
        content=text_content,
        embedding_status="pending"
    )

    db.add(file_item)
    db.commit()
    db.refresh(file_item)

    # 创建 chunks
    create_chunks(
        db=db,
        file_id=file_item.id,
        uuid_name=uuid_name,
        file_path=file_path,
        text=text_content 
    )

    return file_item

# def parse_text_content(content):

#     try:
#         return content.decode("utf-8") 
#         # 只能解析：txt md json csv

#     except Exception:
#         return "暂不支持该文件解析"